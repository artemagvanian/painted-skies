FROM ubuntu:18.04

# apt dependencies
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y tesseract-ocr tesseract-ocr-rus tesseract-ocr-ukr
RUN apt-get install -y imagemagick
RUN apt-get install -y poppler-utils

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# python dependencies
COPY ./requirements.txt /
RUN pip3 install -r ./requirements.txt

# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/start.sh ./scripts/gunicorn.sh /

WORKDIR /app
