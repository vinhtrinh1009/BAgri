FROM python:3.7

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y zip unzip

WORKDIR /core_service

COPY . /core_service

RUN pip3 install -r requirements.txt

EXPOSE 8080

WORKDIR /core_service/core_service

# CMD gunicorn -w 1 main:app --bind 0.0.0.0:8080 --worker-class aiohttp.worker.GunicornUVLoopWebWorker --timeout 120 --graceful-timeout 120
CMD python3 main.py