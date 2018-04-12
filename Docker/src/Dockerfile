FROM centos:latest
MAINTAINER Andrey Alexeev <salexs95@yandex.ru>

RUN yum update -y

RUN yum install -y openssh-server initscripts openssh  openssh-clients

RUN sed -ri 's/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config && \
    sed -ri 's/#   Port 22/Port 2222/g' /etc/ssh/ssh_config

RUN echo "+:ivan:ALL" >> /etc/security/access.conf

RUN yum install -y yum-utils
RUN yum groupinstall -y "Infiniband Support" && \
    yum groupinstall -y "Development Tools"

RUN curl -o hwloc.tar.gz https://www.open-mpi.org/software/hwloc/v2.0/downloads/hwloc-2.0.1.tar.gz && \
    tar -xvzf hwloc.tar.gz && \
    cd hwloc-2.0.1 && \
    ./configure && \
    make && \
    make install

RUN yum install -y libibverbs && \
   yum install -y mvapich2-2.2.x86_64 mvapich2-2.2-devel.x86_64

RUN echo "soft memlock unlimited" >> /etc/security/limits.conf && \
    echo "hard memlock unlimited" >> /etc/security/limits.conf

RUN useradd -d /home/ivan -g 100 -u 1001 ivan

RUN mkdir /ssh && \
    touch /ssh/sshd_log
ADD sshd_config /ssh
RUN ssh-keygen -t rsa -b 4096 -f /ssh/ssh_host_rsa_key && \
    chown 1001:100 --recursive /ssh

EXPOSE 2222 

VOLUME /home:/home

CMD ["/usr/sbin/sshd", "-D", "-f", "/ssh/sshd_config", "-E", "/ssh/sshd_log"]
