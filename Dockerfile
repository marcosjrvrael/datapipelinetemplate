######### BASE Image #########
FROM ubuntu:20.04 as base

ARG DEBIAN_FRONTEND=noninteractive

LABEL MAINTAINER="Marcos Oliveira Jr"

RUN apt update && apt install default-jdk python3.9 python3.9-dev \
  python3.9-venv python3-pip python3-wheel build-essential -y

COPY pyproject.toml poetry.lock ./

RUN pip3 install --no-cache-dir --upgrade pip wheel setuptools poetry \
  && poetry config virtualenvs.create false \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* /tmp/* /var/tmp/*

######### Final Image #########
FROM base AS final

COPY . /source/

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN update-alternatives --set python /usr/bin/python3.9

WORKDIR /source

RUN python -m pip install -r requirements.txt
