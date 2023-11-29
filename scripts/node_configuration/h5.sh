#!/bin/sh 

echo "Static Route Configuration for h5"

# configure ipv4 address
ifconfig h5-eth0 10.0.5.1/24 netmask 255.255.255.0 up

ip route add 10.0.0.0/24  via 10.0.2.2  dev h5-eth0
ip route add 10.0.12.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.13.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.15.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.17.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.19.0/24 via 10.0.2.2  dev h5-eth0

ip route add 10.0.24.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.34.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.24.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.54.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.74.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.94.0/24 via 10.0.2.2  dev h5-eth0


ip route add 10.0.21.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.22.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.23.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.25.0/24 via 10.0.2.2  dev h5-eth0
ip route add 10.0.26.0/24 via 10.0.2.2  dev h5-eth0

# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.h5-eth0.forwarding=1





