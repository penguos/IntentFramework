#!/bin/sh  

echo "Static Route Configuration for h25"
ifconfig h25-eth0 10.0.26.1/24 netmask 255.255.255.0 up
# configure ipv4 address



# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.h25-eth0.forwarding=1

# route add default gw 10.0.0.2 dev h1-eth0
ip route add 10.0.2.0/24 via 10.0.26.2 dev h25-eth0
ip route add 10.0.3.0/24 via 10.0.26.2 dev h25-eth0
ip route add 10.0.4.0/24 via 10.0.26.2 dev h25-eth0
ip route add 10.0.5.0/24 via 10.0.26.2 dev h25-eth0
ip route add 10.0.6.0/24 via 10.0.26.2 dev h25-eth0

# route to public dns server
ip route add 62.210.18.40 via 10.0.26.2 dev h25-eth0
ip route add 8.8.8.8 via 10.0.26.2 dev h25-eth0

# To Reach Dell Laptop
ip route add 192.168.1.131 via 10.0.26.2 dev h25-eth0

ip -6 addr add 2001:1a::1/64 dev h25-eth0

#default ipv6 gateway is R1 eth0
route add -A inet6 default gw 2001:1a::2 dev h25-eth0

sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.h25-eth0.forwarding=1

sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo sysctl -w net.ipv6.conf.lo.forwarding=1
sudo sysctl -w net.ipv6.conf.h25-eth0.forwarding=1

sudo sysctl -w net.ipv6.conf.lo.seg6_enabled=1
sudo sysctl -w net.ipv6.conf.h25-eth0.seg6_enabled=1





