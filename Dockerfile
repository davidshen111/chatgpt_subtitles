# pull official base image
FROM python:3.11.3-slim-buster  

# set work directory
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./.env ./*.py /app/

# expose port
EXPOSE 8000

#start the http serrver
CMD ["python", "http_server.py"]