# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /celery_worker

# Install other necessary packages
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
#COPY requirements_new.txt .

# Install any needed packages specified in requirements.txt
#RUN pip3 install -r requirements_new.txt

# Copy the rest of the source code
COPY celery_worker/ .
COPY config/config.yml ./config/



# Define environment variable
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV CONFIG_FILE=${CONFIG_FILE}
ENV CELERY_BROKER_URL=${CELERY_BROKER_URL}
ENV CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}


# Run celery worker when the container launches
ENTRYPOINT celery -A chatGPTAsk worker -l info -E
