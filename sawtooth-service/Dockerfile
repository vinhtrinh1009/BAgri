FROM ubuntu:20.04
# Enable unbuffered logging
ENV PYTHONUNBUFFERED=1
#ARG requirements=requirements/production.txt
ARG ssh_prv_key	
# Authorize SSH Host
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        wget
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y curl && \ 
    apt-get install -y openssh-server

# RUN apt-get update --fix-missing && \
#     apt-get install -y openssh-server

# RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
#     sh get-docker.sh && \
#     usermod -aG docker root

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.16.2/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan gitlab.com > /root/.ssh/known_hosts
# Add the keys and set permissions
RUN echo '-----BEGIN OPENSSH PRIVATE KEY----- \nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn \nNhAAAAAwEAAQAAAQEA28Zqj17FgCg64KsLt0Iy3X/sHKzSdpv2FhOMRC5S8DD8FKOHLnCI \nXwhz1Hk2uompoG4LzG7QO7huroMtJMMYgdv+TTG78Fddv+VHA5SVIpaPW905gcpz/dBcDI \nFqPagFOOjO197/PPOiQzrULQ9lWiAO6C+/nWuFRjWJpLpeRH6LloUrxQ6ycqOGADJlxTyz \n3SeHierGtnenltmNwAS6aQg2a3HMTTR/I3NXaT1niqp+u8D8FkXMpb054j+Cqy25JQv/xY \ngcSAn2uLv37nb3Ge0SBLD29I2F/gOwXsjDRu+mOjrJ2xbKhqsTvWYcYGFUKxCGwuwN0Dcp \n4Cng9r6OGQAAA9gp12CTKddgkwAAAAdzc2gtcnNhAAABAQDbxmqPXsWAKDrgqwu3QjLdf+ \nwcrNJ2m/YWE4xELlLwMPwUo4cucIhfCHPUeTa6iamgbgvMbtA7uG6ugy0kwxiB2/5NMbvw \nV12/5UcDlJUilo9b3TmBynP90FwMgWo9qAU46M7X3v8886JDOtQtD2VaIA7oL7+da4VGNY \nmkul5EfouWhSvFDrJyo4YAMmXFPLPdJ4eJ6sa2d6eW2Y3ABLppCDZrccxNNH8jc1dpPWeK \nqn67wPwWRcylvTniP4KrLbklC//FiBxICfa4u/fudvcZ7RIEsPb0jYX+A7BeyMNG76Y6Os \nnbFsqGqxO9ZhxgYVQrEIbC7A3QNyngKeD2vo4ZAAAAAwEAAQAAAQEArzDhrNvtMBXhqUpw \nEmuQxIS+oLUbKDV2225Ft+v9bT5/E6yvi9Nkweyo+MyPVe966koO2a3UDGcew7oJeG6U0J \n+ffcWRfSsHrnqEO1Rr9aBzMtWMi+vovoEjf0yCdhfD4fOjPu2iJOJJjLIOhMTrFAbOG0RE \nyKX3HVp8GHX/wzRqv0CM7wJnjWZ9UkO/3Ye7aMc8SXmT/jkeAIP8d7WOSjdqxsWolxEpGh \nn/9FSsI+4wquF9EEWWP02t4LOltHc8C/iHSMvHHUoBMUHtjkIwYOu6thyiYXj0U++vsO8e \nU17hnXJxEm9aPyXJpZy9E1ChvxqGt2tkE72zJ3gAfbo6oQAAAIEArP3zWnDmNXPFDoAcIg \nLQ1rohio2lvFp6rxVgaR/tM0N4wm5eXJ+oafBjILBUxAGkCY028p/Hc42fokuDyHf0JKbz \nJnN01w09xCj1Zf3avNdNkACr7+rcawXD+OxaYgLZ9uIb3ElD5nlvKlN34u8jI/i+cm64xl \nmPJZGWLSpXgewAAACBAO91ekK4TfgNR2xlT9xDcLTvZ1NrAv/3xLeIuMf6f/Ud8wpHQfoq \nf33sxyPBXUDa+REqqBF+AyteVjRoGve07jB1lYL97hBrVx++peaSICvwKEAzeHY++Oyg2b \nuiLPtLXCWE8DyYPs0nhTPMb0uYfh9Ypte0OOWu7JvaJxiU58Y9AAAAgQDq9Nr8Gq7CzkY9 \nw+yhjSDVovMrxuguR2G4MaKsht+aJIJa/K29yT02PPWO/sYg3KB/4PYQ4Hovzcmv/rKKeK \njPESbfF54zw8Kx1iHfnLrYH7QA8GZCVAx4cwdhqrBsvL0t/W7IKHfm4IFR2x3oE5GaEBYY \ninrsd/ViOBiFQnRBDQAAACByb290QGFwcHNlcnZpY2UtN2Y1NTRjOTRjNC10djc1cQE= \n-----END OPENSSH PRIVATE KEY-----' > /root/.ssh/id_rsa

RUN  chmod 600 /root/.ssh/id_rsa
RUN git config --global user.email "haiquan@gmail.com"
RUN git config --global user.name "HaiQuan"

RUN apt-get update  --fix-missing\
    && apt-get install -y software-properties-common \
    && apt-get update  --fix-missing

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD
RUN add-apt-repository 'deb http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe' \
 && apt-get update --fix-missing


# RUN apt-get install -y --allow-unauthenticated -q \
#     sawtooth \
#     python3-sawtooth-cli \
#     python3-sawtooth-sdk \
#     python3-sawtooth-rest-api

# RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update --fix-missing && apt-get install -y python3.7 python3.7-dev
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && update-alternatives --config python3
COPY requirements.txt ./

RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

WORKDIR /sawtooth-service

COPY . /sawtooth-service

EXPOSE 8080
# CMD cd appservice | python3 main.py