#FROM python:latest
FROM python:3.10.9

RUN apt-get update && apt-get -y install vim

RUN mkdir /automation

COPY ./woocommercetest /automation/woocommercetest

COPY ./setup.py /automation

WORKDIR /automation

RUN python3 setup.py install


