FROM ubuntu:18.04

# apt dependencies
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y tesseract-ocr tesseract-ocr-rus tesseract-ocr-ukr
RUN apt-get install -y imagemagick
RUN apt-get install -y poppler-utils
RUN apt-get install -y git

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# python dependencies
RUN pip3 install pipenv

COPY ./Pipfile ./Pipfile.lock /

RUN pipenv install --system --deploy

# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/start.sh ./scripts/gunicorn.sh /

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

WORKDIR /app
