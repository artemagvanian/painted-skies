FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1

# Copy contents of this directory to code
RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN apt-get update

# Install python-connected dependencies
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install -r backend/requirements.txt

# Install node-connected dependencies
RUN apt-get -y install nodejs npm
RUN npm install -g npm
RUN cd frontend/ && npm install
RUN cd frontend/ && npm run build

# Install ImageMagick for TextCleaner script
RUN apt-get -y install imagemagick


# Install Tesseract for image recognition
RUN apt-get -y install tesseract-ocr tesseract-ocr-rus tesseract-ocr-ukr
