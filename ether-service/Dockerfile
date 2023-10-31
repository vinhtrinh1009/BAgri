FROM ubuntu:18.04
# Enable unbuffered logging
ENV PYTHONUNBUFFERED=1
# ARG requirements=requirements/production.txt
ARG ssh_prv_key	
# Authorize SSH Host

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y git && \ 
    apt-get install -y curl 

RUN apt-get update --fix-missing && \
    apt-get install -y \
        git \
        openssh-server 
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \ 
    usermod -aG docker root

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl && \ 
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan gitlab.com > /root/.ssh/known_hosts
# Add the keys and set permissions
RUN echo '-----BEGIN OPENSSH PRIVATE KEY----- \nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2g \n-----END OPENSSH PRIVATE KEY-----' > /root/.ssh/id_rsa


RUN  chmod 600 /root/.ssh/id_rsa
RUN git config --global user.email "dangmduc99@gmail.com"
RUN git config --global user.name "Đặng Minh Đức"

WORKDIR /ether-service

COPY . /ether-service
RUN apt-get update  --fix-missing\
    && apt-get install -y software-properties-common \
    && apt-get update  --fix-missing

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD
RUN  add-apt-repository 'deb [arch=amd64] http://repo.sawtooth.me/ubuntu/chime/stable bionic universe' \
 && apt-get update --fix-missing

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

EXPOSE 8080
CMD cd ether-service | cd appservice | python3 main.py