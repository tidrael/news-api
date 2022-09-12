# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
WORKDIR /app
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Install google chrome and chromedriver
RUN apt-get -y update
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Port
EXPOSE 8000

# Command
CMD exec uvicorn app:app