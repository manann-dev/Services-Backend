from flask import url_for, jsonify, request
from flask_restx import Namespace, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jti
from authlib.integrations.flask_client import OAuth
from flask import current_app
from schema.models.user import User
from schema.database import db_session
import os
import redis

auth_ns = Namespace('auth', description='Authentication and Authorization')

redis_client = redis.Redis()

oauth = OAuth(current_app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_SECRET_KEY"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',
    redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
)


@auth_ns.route('/login/google')
class GoogleLoginResource(Resource):
    def get(self):
        redirect_uri = url_for('auth_google_authorize_resource', _external=True)
        return google.authorize_redirect(redirect_uri)


# OAuth Callback
@auth_ns.route('/google/callback')
class GoogleAuthorizeResource(Resource):
    def get(self):
        token = google.authorize_access_token()
        resp = google.get('userinfo', token=token)
        user_info = resp.json()

        user = db_session.query(User).filter(User.email==user_info['email']).first()

        if not user:
            user = User(
                email=user_info['email'],
                first_name=user_info['given_name'],
                last_name=user_info['family_name'],
            )
            db_session.add(user)
            db_session.commit()
        
        access_token = create_access_token(identity=user.id)
                
        access_jti = get_jti(access_token)
        exp_days = 30 * 24 * 60 * 60
        
        redis_client.setex(user.id, exp_days, access_jti)  # Mark as an access token
        
        return jsonify(access_token=access_token)


def revoke_token(token_key):
    if redis_client.get(token_key):
        redis_client.delete(token_key)  # Revoke the current access token
        message = "You have been logged out."
    else:
        message = "Token not found or expired."
    return message

# Logout Endpoint
@auth_ns.route('/logout')
class LogoutResource(Resource):
    @jwt_required()
    @auth_ns.doc(security='Bearer Auth')
    def post(self):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):

                current_token = get_jwt()

                message = revoke_token(current_token["sub"])

                response = jsonify({"msg": message})

                return response

            else:
                return jsonify({"error": "Authorization header is missing or not valid."}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 400

# Check Token Expired or Delted Endpoint
@auth_ns.route('/token')
class TokenExpiredResource(Resource):
    @jwt_required()
    @auth_ns.doc(security='Bearer Auth')
    def post(self):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):

                current_user_id = get_jwt()['sub']

                if redis_client.get(current_user_id):
                    message = "Token is not expired"
                else:
                    message = "Token not found or expired."
                
                response = jsonify({"msg": message})
                
                return response
            else:
                return jsonify({"error": "Authorization header is missing or not valid."}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 400



# # Token Refresh Endpoint
# @auth_ns.route('/token/refresh')
# class TokenRefreshResource(Resource):
#     @auth_ns.doc(security='Bearer Auth')
#     @jwt_required(refresh=True)
#     def post(self):
#         try:
#             auth_header = request.headers.get('Authorization')
        
#             if auth_header and auth_header.startswith('Bearer '):
#                 # Extract the token from the header
#                 token = auth_header.split(" ")[1]
#                 current_user = get_jwt_identity()
#                 refresh_jti = get_jwt()['jti']  # Get the unique identifier for the refresh token
#                 refresh_exp = get_jwt()['exp']
#                 # Check if the refresh token is revoked
#                 token_in_redis = redis_client.get(refresh_jti)
#                 if not token_in_redis:
#                     return {'msg': 'Refresh token has been revoked'}, 401
                    # token_value = r.get(token_key)

                    # if token_value is not None:
                    #     token_value = token_value.decode("utf-8")
                    #     print("Token:", token_value)
                    # else:
                    #     print("Token not found or expired.")

#                 # Issue a new access token
#                 new_access_token = create_access_token(identity=current_user, expires_delta=refresh_exp)
#                 new_access_jti = new_access_token['jti']
#                 new_access_exp = new_access_token['exp']
#                 # Store the new access token in Redis
#                 redis_client.setex(new_access_jti, timedelta(minutes=30), 'access')

#                 return jsonify(access_token=new_access_token)
#             else:
#                 return jsonify({"error": "Authorization header is missing or not valid."}), 401
#         except Exception as e:
#             return jsonify({"error": str(e)}), 400


# peridically clean up expired tokens from the db to keep the token table size manageable.


