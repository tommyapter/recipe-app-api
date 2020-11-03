FROM python:3.7-alpine
MAINTAINER Tommy Apter

ENV PYTHONUNBUFFERED 1
  #runs python on unbuffered more which is recommended for docker containers
  #The reason for this is that it doesn't allow Python to buffer the outputs. It just prints them directly. And this avoids some complications and things like that with the Docker image when you're running your python application.

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
  # What this does is it says copy from the directory adjacent to the Docker file, copy the requirements file that we're going to create here and copy it on the Docker image to /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./app /app
# make a directory within our Docker image that we can use to store our application source code.

RUN adduser -D user
USER user
# create a user that is going to run our application using docker.
# Hyphen D says create a user that is going to be used for running applications only. Not for basically having a home directory and that someone will log in to it's going to be used simply to run our processes from our project.
# The reason why we do this is for security purposes.
  # If you don't do this then the image will run our application using the root account which is not recommended
    # because that means if somebody compromises our application they then have root access to the whole image
    # and they can go do other than vicious things.
  # Whereas if you create a separate user just for our application then this kind of limits the scope thatan attacker would have in our documentation.
