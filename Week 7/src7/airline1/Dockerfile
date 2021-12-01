#FROM python:3 python:3 is another docker image that already contain information to download python3 and common packages. 
FROM python:3
#This means copy all current file in this directory. 
COPY .  /usr/src/app
#WORKDIR means change working directory like cd in linux
WORKDIR /usr/src/app
#requirements.txt should be a text file containing all the requirements that you need
RUN pip install -r requirements.txt
#Everything else was just setting up the docker image. CMD is when you actually run the command. It is an array where each command is separated by a ,
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
