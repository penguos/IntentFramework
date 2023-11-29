#!/bin/sh  

echo "Static Route Configuration for h22"

# configure ipv4 address
ifconfig h22-eth0 10.0.22.1/24 netmask 255.255.255.0 up

# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.h22-eth0.forwarding=1

# route add default gw 10.0.0.2 dev h1-eth0
ip route add 10.0.2.0/24 via 10.0.22.2 dev h22-eth0
ip route add 10.0.3.0/24 via 10.0.22.2 dev h22-eth0
ip route add 10.0.4.0/24 via 10.0.22.2 dev h22-eth0
ip route add 10.0.12.0/24 via 10.0.22.2 dev h22-eth0
ip route add 10.0.13.0/24 via 10.0.22.2 dev h22-eth0
ip route add 10.0.14.0/24 via 10.0.22.2 dev h22-eth0
# route to public dns server
ip route add 62.210.18.40 via 10.0.22.2 dev h22-eth0
ip route add 8.8.8.8 via 10.0.22.2 dev h22-eth0

# To Reach Dell Laptop
ip route add 192.168.1.131 via 10.0.22.2 dev h22-eth0




