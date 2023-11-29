#!/bin/sh

echo "Static Route Configuration for R4"

# configure ipv4 address
ifconfig r4-eth1 10.0.2.2/24   netmask 255.255.255.0 up
ifconfig r4-eth3 10.0.3.2/24   netmask 255.255.255.0 up
ifconfig r4-eth4 10.0.4.2/24   netmask 255.255.255.0 up
ifconfig r4-eth6 10.0.5.2/24   netmask 255.255.255.0 up
ifconfig r4-eth8 10.0.6.2/24   netmask 255.255.255.0 up

# path 1
ifconfig r4-eth0 10.0.24.2/24 netmask 255.255.255.0 up
# path2
ifconfig r4-eth2 10.0.34.2/24 netmask 255.255.255.0 up
# path3
ifconfig r4-eth8 10.0.54.2/24  netmask 255.255.255.0 up
# path4
ifconfig r4-eth10 10.0.74.2/24  netmask 255.255.255.0 up
# path5
ifconfig r4-eth12 10.0.94.2/24  netmask 255.255.255.0 up

# configure static route
# path 1
route add -net 10.0.13.0/24 gw 10.0.34.1 dev r4-eth0
route add -net 10.0.12.0/24 gw 10.0.24.1 dev r4-eth0
# configure route to r2
route add -net 10.0.0.0/24 gw 10.0.24.1 dev r4-eth0

# To R2
route add -net 10.0.21.0/24 gw 10.0.24.1 dev r4-eth0
route add -net 10.0.22.0/24 gw 10.0.34.1 dev r4-eth2
route add -net 10.0.23.0/24 gw 10.0.54.1 dev r4-eth8
route add -net 10.0.25.0/24 gw 10.0.74.1 dev r4-eth10
route add -net 10.0.26.0/24 gw 10.0.94.1 dev r4-eth12
route add -net 10.0.29.0/24 gw 10.0.24.1 dev r4-eth0

ifconfig r4-eth1 10.0.2.2/24 netmask 255.255.255.0 up
route add default gw 10.0.2.1 dev r4-eth1
# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth0.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth1.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth2.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth3.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth4.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth8.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth9.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth10.forwarding=1
sudo sysctl -w net.ipv4.conf.r4-eth12.forwarding=1