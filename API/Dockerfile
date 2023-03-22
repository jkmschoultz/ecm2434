FROM  python:3.8.13-bullseye

ENV PYTHONUNBUFFERED=1

# Set the working directory to /API
WORKDIR /api

# Install dependencies
RUN pip install django django-cors-headers djangorestframework-simplejwt Pillow

# copy from the current directory of the Dockerfile to /API in the image
COPY . . 

EXPOSE 8000