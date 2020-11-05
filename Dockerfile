FROM python:3.7-alpine
MAINTAINER Tommy Apter

ENV PYTHONUNBUFFERED 1
  #runs python on unbuffered more which is recommended for docker containers
  #The reason for this is that it doesn't allow Python to buffer the outputs. It just prints them directly. And this avoids some complications and things like that with the Docker image when you're running your python application.

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# RUN apk add zlib-dev jpeg-dev gcc musl-dev
# https://www.reddit.com/r/docker/comments/bv31s2/has_anyone_managed_to_get_pip_pillow_installed/
RUN pip install -r /requirements.txt
# What this does is it says copy from the directory adjacent to the Docker file, copy the requirements file that we're going to create here and copy it on the Docker image to /requirements.txt
RUN apk del .tmp-build-deps
# https://www.udemy.com/course/django-python-advanced/learn/lecture/12712601#questions


RUN mkdir /app
WORKDIR /app
COPY ./app /app
# make a directory within our Docker image that we can use to store our application source code.

RUN mkdir -p /vol/web/media
# I like to store any files that may need to be shared with other containers in a subdirectory called vol which is short for volume this way we know where all of the volume mappings need to be in our container if we need to share this data with other containers in our service for example if you had an engine X or a web server that needed to serve these media files you know that you would need to map this volume and share it with the web server container.
# and the media directory is typically used for any media files that are uploaded by the user so that's where we're going to store our recipe pictures
RUN mkdir -p /vol/web/static
# in Django you typically have two files that hold static data one is the static and that is typically used for things like JavaScript CSS files or any static files that you may want to serve which are not typically changing during the execution of the application
# in case you don't know this - p here that we add to the mkdir means make all of the sub directories including the directory that we need so if the vol directory doesn't exist it will create vol web and media if you don't include this then it will say something like the volume directory doesn't exist then it'll give an error
RUN adduser -D user
RUN chown -R user:user /vol/
# sets the ownership of all the directories within the volume directory to our custom user
# the R here means recursive so instead of just setting the vol permissions it will set any subdirectories in the vol folder
RUN chmod -R 755 /vol/web
#  add the permissions. The line above means is that the user can do everything so the owner can do everything with the directory and the rest can read and execute from the directory
USER user
# create a user that is going to run our application using docker.
# Hyphen D says create a user that is going to be used for running applications only. Not for basically having a home directory and that someone will log in to it's going to be used simply to run our processes from our project.
# The reason why we do this is for security purposes.
  # If you don't do this then the image will run our application using the root account which is not recommended
    # because that means if somebody compromises our application they then have root access to the whole image
    # and they can go do other than vicious things.
  # Whereas if you create a separate user just for our application then this kind of limits the scope thatan attacker would have in our documentation.
