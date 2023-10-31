FROM python:3.7

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y zip unzip


WORKDIR /back_end

COPY requirements.txt /back_end/
RUN pip3 install -r requirements.txt

COPY . /back_end


EXPOSE 8083

WORKDIR /back_end/back_end

CMD gunicorn -w 1 main:app --bind 0.0.0.0:8080 --worker-class aiohttp.worker.GunicornUVLoopWebWorker --timeout 120 --graceful-timeout 120