#!/bin/sh 

echo "Static Route Configuration for h6"

# configure ipv4 address
ifconfig h6-eth0 10.0.6.1/24 netmask 255.255.255.0 up

ip route add 10.0.0.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.12.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.13.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.24.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.34.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.21.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.22.0/24 via 10.0.2.2 dev h6-eth0
ip route add 10.0.23.0/24 via 10.0.2.2 dev h6-eth0


# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.h6-eth0.forwarding=1





