FROM ubuntu:18.04
# Enable unbuffered logging
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
#ARG ssh_prv_key
# Authorize SSH Host

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y curl && \
    apt-get install -y openssh-server

RUN apt-get install -y python3-pip

RUN apt-get install -y jq

# RUN apt-get update --fix-missing && \
#     apt-get install -y \
#         git \
#         openssh-server

# RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
#     sh get-docker.sh && \
#     usermod -aG docker root

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN curl -sSL https://bit.ly/2ysbOFE | bash -s -- 2.2.2 1.4.9 -d && \
    cp -r ./fabric-samples/bin/. /usr/local/bin

RUN mkdir -p /root/.ssh && \
   chmod 0700 /root/.ssh && \
   ssh-keyscan gitlab.com > /root/.ssh/known_hosts
# Add the keys and set permissions
RUN echo '-----BEGIN OPENSSH PRIVATE KEY----- \nb3BlbnNzaC1rZXktdjEAAAAABG5vb\n-----END OPENSSH PRIVATE KEY-----' > /root/.ssh/id_rsa

RUN  chmod 600 /root/.ssh/id_rsa
RUN git config --global user.email "haiquan5396@gmail.com"
RUN git config --global user.name "HaiQuan"

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

WORKDIR /fabric_appservice

COPY . /fabric_appservice

EXPOSE 8080
# CMD make dev
