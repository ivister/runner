FROM centos:latest
MAINTAINER Andrey Alexeev <salexs95@yandex.ru>

RUN yum update -y

RUN yum install -y openssh-server initscripts openssh  openssh-clients && \
    sed -ri 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config

RUN yum install -y yum-utils

RUN yum groupinstall -y "Infiniband Support" && \
    yum groupinstall -y "Development Tools"

RUN yum install -y libibverbs && \
   yum install -y mvapich2-2.2.x86_64 mvapich2-2.2-devel.x86_64

EXPOSE 22

VOLUME /home:/home

RUN ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key

RUN useradd -d /home/ivan -g 100 -u 1001 ivan
CMD ["/usr/sbin/sshd", "-D"]

