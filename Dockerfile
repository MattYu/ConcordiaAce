# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG C.UTF-8
ENV PORT=8000
ENV DEBIAN_FRONTEND=noninteractive

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

EXPOSE 8000

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder:Ace. Please enter the Python path to wsgi file.
CMD gunicorn ace.wsgi:application --bind 0.0.0.0:$PORT
