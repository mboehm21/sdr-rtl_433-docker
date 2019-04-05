FROM ubuntu:bionic

MAINTAINER Michael Boehm 

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y \
    git \
    libtool \
    libusb-1.0.0-dev \
    librtlsdr-dev \
    rtl-sdr \
    cmake \
    python3-influxdb \
    && cd / \
    && git clone https://github.com/merbanan/rtl_433.git \
    && cd rtl_433/ \
    && mkdir build \
    && cd build/ \
    && cmake ../ \
    && make \
    && make install \
    && rm -rf /rtl_433 \
    && apt-get purge -y git \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY wrapper.sh /
COPY to_influx.py /

RUN cd / \
    && chmod +x wrapper.sh \
    && chmod +x to_influx.py

WORKDIR /
ENTRYPOINT ./wrapper.sh
