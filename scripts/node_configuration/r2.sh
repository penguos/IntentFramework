#!/bin/sh

echo "Static Route Configuration for R2"

# configure ipv4 address
ifconfig r2-eth0 10.0.12.2/24 netmask 255.255.255.0 up
ifconfig r2-eth1 10.0.24.1/24 netmask 255.255.255.0 up


# configure static route
route add -net 10.0.2.0/24  gw 10.0.24.2 dev r2-eth1
route add -net 10.0.3.0/24  gw 10.0.24.2 dev r2-eth1
route add -net 10.0.4.0/24  gw 10.0.24.2 dev r2-eth1
route add -net 10.0.5.0/24  gw 10.0.24.2 dev r2-eth1
route add -net 10.0.6.0/24  gw 10.0.24.2 dev r2-eth1

route add -net 10.0.21.0/24 gw 10.0.12.1 dev r2-eth0
route add -net 10.0.22.0/24 gw 10.0.12.1 dev r2-eth0
route add -net 10.0.23.0/24 gw 10.0.12.1 dev r2-eth0
route add -net 10.0.25.0/24 gw 10.0.12.1 dev r2-eth0
route add -net 10.0.26.0/24 gw 10.0.12.1 dev r2-eth0
route add -net 10.0.29.0/24 gw 10.0.12.1 dev r2-eth0

route add -net 8.8.8.0/24 gw 10.0.24.2 dev r2-eth1
route add 192.168.1.131/32 gw 10.0.24.2 dev r2-eth1

# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.r2-eth0.forwarding=1
sudo sysctl -w net.ipv4.conf.r2-eth1.forwarding=1

