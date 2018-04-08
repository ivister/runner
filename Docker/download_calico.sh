#!/bin/bash
wget https://github.com/projectcalico/calico-containers/releases/download/v0.22.0/calicoctl
chmod +x calicoctl

sudo yum install -y etcd python-etcd
sudo systemctl enable etcd
sudo systemctl start etcd

docker pull calico/node:v0.22.0
docker pull calico/node-libnetwork:v0.9.0

sudo ./calicoctl node --libnetwork
