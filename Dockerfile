FROM python:2.7-slim-buster

RUN apt-get update && apt-get install -y \
    gcc \
    git

RUN mkdir /app
WORKDIR /app

# Cache requirements and install them
COPY test_project/requirements.txt .
RUN pip install -r requirements.txt --find-links https://www.djangoplicity.org/repository/packages/

# Create app required directories
RUN mkdir -p tmp

# Final required files
COPY djangoplicity/ djangoplicity/
COPY test_project/ test_project/
COPY .coveragerc .
COPY manage.py .
