#!/bin/bash
yum install -y etcd

chmod +x calicoctl
mv calicoctl /bin/

systemctl enable etcd
systemctl start etcd

# Copy conf files
cp etcd.conf /etc/etcd/
cp daemon.json /etc/docker/

systemctl restart etcd
systemctl restart docker

docker pull calico/node:v0.22.0
docker pull calico/node-libnetwork:v0.9.0

calicoctl node --libnetwork
