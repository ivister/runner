FROM centos:latest
MAINTAINER Andrey Alexeev <salexs95@yandex.ru>

#ENV http_proxy=192.168.152.1:80
#ENV https_proxy=192.168.152.1:80

#RUN dhclient
RUN yum update -y

RUN yum install -y openssh-server initscripts openssh  openssh-clients && \
    sed -ri 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config

RUN yum install -y yum-utils

RUN yum groupinstall -y "Infiniband Support" && \
    yum groupinstall -y "Development Tools"

# RUN yum install -y libibverbs && \
#    yum install -y mvapih2-2.2
EXPOSE 22
#RUN systemctl enable sshd
#ENTRYPOINT ["/usr/sbin/init"]
RUN ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key
CMD ["/usr/sbin/sshd", "-D"]
