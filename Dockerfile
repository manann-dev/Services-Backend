# FROM python:3.9

# WORKDIR /usr/src/app

# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     libtesseract-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt /usr/src/app/
# #COPY celery_worker/requirements_new.txt /celery_worker/

# RUN pip install --no-cache-dir -r requirements.txt
# #RUN pip install --no-cache-dir -r /celery_worker/requirements_new.txt

# COPY src/ /usr/src/app/src/
# COPY ./config.yml /usr/src/app/config/

# COPY schema/ /usr/src/app/schema/

# WORKDIR /celery_worker
# COPY celery_worker/ .
# COPY ./config.yml ./config/

# WORKDIR /usr/src/app

# ENV OPENAI_API_KEY=${OPENAI_API_KEY}
# ENV CONFIG_FILE=${CONFIG_FILE}
# ENV CELERY_BROKER_URL=${CELERY_BROKER_URL}
# ENV CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}

# CMD ["python", "./src/main.py"]

# # for running the Celery worker, comment out the above CMD line
# #and uncomment the following ENTRYPOINT line when building the image for a worker
# # ENTRYPOINT ["celery", "-A", "chatGPTAsk", "worker", "-l", "info", "-E"]


# FROM python:3.9

# WORKDIR /usr/src/app

# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     libtesseract-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt /usr/src/app/
# RUN pip install --no-cache-dir -r requirements.txt

# COPY src/ /usr/src/app/src/
# COPY config/config.yml /usr/src/app/config/

# COPY schema/ /usr/src/app/schema/

# WORKDIR /celery_worker
# COPY celery_worker/ .
# COPY config/config.yml ./config/

# WORKDIR /usr/src/app

# ENV OPENAI_API_KEY=${OPENAI_API_KEY}
# ENV CONFIG_FILE=/usr/src/app/config/config.yml
# ENV CELERY_BROKER_URL=${CELERY_BROKER_URL}
# ENV CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}
# ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

# CMD ["python", "./src/main.py"]
# # ENTRYPOINT ["celery", "-A", "chatGPTAsk", "worker", "-l", "info", "-E"]



FROM python:3.9

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY celery_worker/ ./celery_worker/
COPY config/ ./config/
COPY schema/ ./schema/

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV CONFIG_FILE=/usr/src/app/config/config.yml
ENV CELERY_BROKER_URL=${CELERY_BROKER_URL}
ENV CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}
ENV PYTHONPATH /usr/src/app

CMD ["python", "./src/main.py"]
