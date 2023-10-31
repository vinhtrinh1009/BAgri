FROM python:3.7

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y zip unzip

WORKDIR /v_storage

COPY . /v_storage

RUN pip3 install -r requirements.txt

EXPOSE 8080

WORKDIR /v_storage/v_storage

CMD python3 main.py