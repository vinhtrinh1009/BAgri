FROM python:3.7

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y

WORKDIR /account_service

COPY . /account_service

RUN pip3 install -r requirements.txt

EXPOSE 8080

WORKDIR /account_service/account_service

# CMD gunicorn -w 1 main:app --bind 0.0.0.0:8080 --worker-class aiohttp.worker.GunicornUVLoopWebWorker --timeout 120 --graceful-timeout 120
CMD python3 main.py