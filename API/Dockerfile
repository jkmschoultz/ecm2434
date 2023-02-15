FROM  python:3.8.13-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /api

RUN pip install django django-cors-headers

# copy from the current directory of the Dockerfile to /api in the image
COPY . . 

EXPOSE 8000