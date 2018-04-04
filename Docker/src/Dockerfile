FROM centos:latest
MAINTAINER Andrey Alexeev <salexs95@yandex.ru>

#ENV http_proxy=192.168.152.1:80
#ENV https_proxy=192.168.152.1:80

#RUN dhclient
RUN yum update -y

RUN yum install -y openssh

RUN yum install -y libibverbs && \
    yum install -y mvapih2-2.2

RUN sed -ri 's/#   StrictHostKeyChecking ask/StrictHostKeyCheking no/g' /etc/ssh/ssh_config
