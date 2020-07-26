# The docker file for running Dash

FROM python:3.8

RUN apt-get update -y && apt-get upgrade -y

COPY pip.conf /etc/pip.conf

ADD . /stonksomatic

WORKDIR /stonksomatic

RUN pip install -r requirements.txt

EXPOSE 8050
