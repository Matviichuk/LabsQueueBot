# Version 0.0.1
# Choice base image
FROM python:3.8

MAINTAINER Oleksandr Matviichuk <Sasha.Matviich@gmail.com>
# Setup software
#RUN ["apt-get", "install", "git"]
#RUN ["pip", "install", "--upgrade pip"]

# Clone code
WORKDIR /app
#RUN git clone https://github.com/Matviichuk/LabsQueueBot.git origin
COPY . origin

# Setup environment
WORKDIR /app/origin/
RUN ["pip", "install", "-r", "requirements.txt"]

# Run App
WORKDIR /app/origin/Sources
CMD ["python", "main.py"]
