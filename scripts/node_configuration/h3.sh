#!/bin/sh

echo "Static Route Configuration for h3"

# configure ipv4 address
ifconfig h3-eth0 10.0.3.1/24 netmask 255.255.255.0 up

ip route add 10.0.0.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.12.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.13.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.24.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.34.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.21.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.22.0/24 via 10.0.3.2 dev h3-eth0
ip route add 10.0.23.0/24 via 10.0.3.2 dev h3-eth0
# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.h3-eth0.forwarding=1





