#!/bin/sh

echo "Static Route Configuration for R1"

# configure ipv4 address
ifconfig r1-eth0   10.0.21.2/24 netmask 255.255.255.0 up
ifconfig r1-eth3   10.0.22.2/24 netmask 255.255.255.0 up
ifconfig r1-eth4   10.0.23.2/24 netmask 255.255.255.0 up
ifconfig r1-eth6   10.0.26.2/24 netmask 255.255.255.0 up
ifconfig r1-eth8   10.0.25.2/24 netmask 255.255.255.0 up
ifconfig r1-eth10  10.0.29.2/24 netmask 255.255.255.0 up
# v4 path 1
ifconfig r1-eth1  10.0.12.1/24 netmask 255.255.255.0 up
ifconfig r1-eth2  10.0.13.1/24 netmask 255.255.255.0 up
ifconfig r1-eth5  10.0.15.1/24 netmask 255.255.255.0 up
ifconfig r1-eth7  10.0.17.1/24 netmask 255.255.255.0 up
ifconfig r1-eth9  10.0.19.1/24 netmask 255.255.255.0 up

route add -net 10.0.24.0/24 gw 10.0.12.2 dev r1-eth1
route add -net 10.0.34.0/24 gw 10.0.13.2 dev r1-eth2
route add -net 10.0.54.0/24 gw 10.0.15.2 dev r1-eth5
route add -net 10.0.74.0/24 gw 10.0.17.2 dev r1-eth7
route add -net 10.0.94.0/24 gw 10.0.19.2 dev r1-eth9

route add -net 10.0.2.0/24 gw 10.0.12.2 dev r1-eth1
route add -net 10.0.3.0/24 gw 10.0.13.2 dev r1-eth2
route add -net 10.0.4.0/24 gw 10.0.15.2 dev r1-eth5
route add -net 10.0.5.0/24 gw 10.0.17.2 dev r1-eth7
route add -net 10.0.6.0/24 gw 10.0.19.2 dev r1-eth9
#  默认路由到h21


route add -net 8.8.8.0/24 gw 10.0.12.2 dev r1-eth1
route add 192.168.1.131/32 gw 10.0.12.2 dev r1-eth1
route add default gw 10.0.12.2 dev r4-eth1
# Enable ipv4 forwarding
sudo sysctl -w net.ipv4.conf.all.forwarding=1
sudo sysctl -w net.ipv4.conf.lo.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth0.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth1.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth2.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth3.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth4.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth5.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth6.forwarding=1
sudo sysctl -w net.ipv4.conf.r1-eth8.forwarding=11
echo "SRv6 Configuration for R1"


# local tunnel address


# Add through RESTful API
# path 1
# ip route add 192.168.1.207 encap seg6 mode encap segs fc00:2::da,fc00:3::da,fc00:4::da dev r1-eth3
# path 2
# ip route add 192.168.1.207 encap seg6 mode encap segs fc00:2::5a,fc00:3::5a,fc00:4::5a dev r1-eth7
# ip route add 10.0.2.1 encap seg6 mode encap segs fc00:2::cc,fc00:3::cc,fc00:4::cc dev r1-eth3
# path 3
#ip route add 10.0.2.1 encap seg6 mode encap segs fc00:5::cc,fc00:6::cc,fc00:4::cc dev r1-eth7
# ip route add 8.8.8.8 encap seg6 mode encap segs fc00:2::ee,fc00:3::ee,fc00:4::ee dev r1-eth3

















