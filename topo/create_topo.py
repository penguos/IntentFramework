import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from config.config_parser import app_config
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink, Intf
from mininet.nodelib import NAT

def topology():
    monitor = 'Yes'

    # 1） create Mininet object*/
    net = Mininet(controller=RemoteController, switch=OVSSwitch, autoSetMacs=True, autoStaticArp=False)

    # SDN controller
    controller_ip = app_config.get("General","controller_ip")

    # 2）add controller address and port
    c0 = net.addController('c0', controller=RemoteController, ip=controller_ip, port=6633,)

    # 3） add SDN switch for control and monitor purpose
    s11 = net.addSwitch('s11', protocols=["OpenFlow13"])
    s22 = net.addSwitch('s22', protocols=["OpenFlow13"])


    # 4) add hosts and routers

    h21 =  net.addHost('h21', ip='10.0.21.1/24')
    h22 =  net.addHost('h22', ip='10.0.22.1/24')
    h23 =  net.addHost('h23', ip='10.0.23.1/24')
    h24 =  net.addHost('h24', ip='10.0.26.1/24')
    h25 =  net.addHost('h25', ip='10.0.25.1/24')
    h2 = net.addHost('h2', cls=NAT, inNamespace=False)
    #h2 = net.addHost('h2', ip='10.0.2.1/24')
    h3 = net.addHost('h3', ip='10.0.3.1/24')
    h4 = net.addHost('h4', ip='10.0.4.1/24')
    h5 = net.addHost('h5', ip='10.0.5.1/24')
    h6 = net.addHost('h6', ip='10.0.6.1/24')



    # 5) add paths
    # Path 1: IPv4/SRv6 Router
    r1 = net.addHost('r1')

    r2 = net.addHost('r2')
    r3 = net.addHost('r3')
    r4 = net.addHost('r4')
    r5 = net.addHost('r5')
    r7 = net.addHost('r7')
    r9 = net.addHost('r9')

    # 6) add Link Host Links
    net.addLink(node1=h21, node2=s11, port1=0,  port2=11)
    net.addLink(node1=h22, node2=s11, port1=0,  port2=12)
    net.addLink(node1=h23, node2=s11, port1=0,  port2=13)
    net.addLink(node1=h24, node2=s11, port1=0,  port2=14)
    net.addLink(node1=h25, node2=s11, port1=0,  port2=15)


    # Ingress and Egress node
    net.addLink(node1=s11, node2=r1, port1=2, port2=0)
    net.addLink(node1=s11, node2=r1, port1=3, port2=3)
    net.addLink(node1=s11, node2=r1, port1=4, port2=4)
    net.addLink(node1=s11, node2=r1, port1=5, port2=6)
    net.addLink(node1=s11, node2=r1, port1=6, port2=8)
    #7 from s11 to 10 from r1 is for intf interface
    net.addLink(node1=s11, node2=r1, port1=7, port2=10)

    #net.addLink(node1=h2, node2=s11, port1=0,  port2=2)
    net.addLink(node1=s22, node2=h2, port1=2, port2=0)
    net.addLink(node1=s22, node2=h3, port1=3, port2=0)
    net.addLink(node1=s22, node2=h4, port1=4, port2=0)
    net.addLink(node1=s22, node2=h5, port1=5, port2=0)
    net.addLink(node1=s22, node2=h6, port1=9, port2=0)

    net.addLink(node1=r4, node2=s22, port1=1, port2=7)
    net.addLink(node1=r4, node2=s22, port1=3, port2=1)
    net.addLink(node1=r4, node2=s22, port1=4, port2=6)
    net.addLink(node1=r4, node2=s22, port1=6, port2=8)
    net.addLink(node1=r4, node2=s22, port1=9, port2=10)

    # Path 1
    # ipv4 route sw1- r1-r2-r3 -sw2
    net.addLink(node1=r1, node2=r2,  port1=1, port2=0, cls=TCLink,
                bw=app_config.getint("Path","v4_path_1_bw"), delay=app_config.get("Path","v4_path_1_delay"), jitter=app_config.get("Path","v4_path_1_jitter"), use_tbf=True)
    net.addLink(node1=r2, node2=r4,  port1=1, port2=0, cls=TCLink, use_tbf=True)

    # Path 2
    # ipv4 route
    net.addLink(node1=r1, node2=r3, port1=2,  port2 =0, cls=TCLink,
                bw=app_config.getint("Path", "v4_path_2_bw"), delay=app_config.get("Path", "v4_path_2_delay"),
                jitter=app_config.get("Path", "v4_path_2_jitter"), use_tbf=True)
    net.addLink(node1=r3, node2=r4, port1=1,  port2 =2, cls=TCLink, use_tbf=True)

    # Path 3
    # ipv4 route
    net.addLink(node1=r1, node2=r5, port1=5, port2=0, cls=TCLink,
                bw=app_config.getint("Path", "v4_path_3_bw"), delay=app_config.get("Path", "v4_path_3_delay"),
                jitter=app_config.get("Path", "v4_path_3_jitter"), use_tbf=True)
    net.addLink(node1=r5, node2=r4, port1=1, port2=8, cls=TCLink, use_tbf=True)

    # Path 4
    # ipv4 route
    net.addLink(node1=r1, node2=r7, port1=7, port2=0, cls=TCLink,
                bw=app_config.getint("Path", "v4_path_4_bw"), delay=app_config.get("Path", "v4_path_4_delay"),
                jitter=app_config.get("Path", "v4_path_4_jitter"), use_tbf=True)
    net.addLink(node1=r7, node2=r4, port1=1, port2=10, cls=TCLink, use_tbf=True)

    # Path 5
    # ipv4 route
    net.addLink(node1=r1, node2=r9, port1=9, port2=0, cls=TCLink,
                bw=app_config.getint("Path", "v4_path_5_bw"), delay=app_config.get("Path", "v4_path_5_delay"),
                jitter=app_config.get("Path", "v4_path_5_jitter"), use_tbf=True)
    net.addLink(node1=r9, node2=r4, port1=1, port2=12, cls=TCLink, use_tbf=True)

    r1.setMAC(mac='2e:1f:31:9c:61:ad', intf='r1-eth1')
    r1.setMAC(mac='2a:5c:db:4a:fe:bc', intf='r1-eth2')


    # 7) Add physical link with usb ethernet interface to external PC
    switch = s11
    # UBS 3.0 to Ethernet on X1 5th
    intfName = app_config.get("General", "intfName")
    _intf = Intf(intfName, node=switch, port=16)

    net.build()
    c0.start()

    # Connect SDN sw and controller
    s11.start([c0])
    s22.start([c0])


    print("*** Running CLI")

    CLI(net)

    print("*** Stopping network")

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
