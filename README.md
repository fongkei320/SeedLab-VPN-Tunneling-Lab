# VPN Tunneling Lab

## Introduction

According to this Lab Manual, the objective of the lab is to implement
the VPN tunnel.

## Topology

The following is the network diagram of the lab

![](./media/image1.png)

## Background Information

And the following is the ip address table

| HOST       | IP address     | Subnet mask   |
|------------|----------------|---------------|
| HOST U     | 10.0.2.7       | 255.255.255.0 |
| VPN Server | 10.0.2.8       | 255.255.255.0 |
|            | 192.168.60.1   | 255.255.255.0 |
| HOST V     | 192.168.60.101 | 255.255.255.0 |

## Task 1

3 VMs is setup and in the following confguration

| VM Name                           | vVPU assigned | RAM assigned | HDD assigned | Number of vNIC | Vnet assigned        |
|-----------------------------------|---------------|--------------|--------------|----------------|----------------------|
| VPN Server SEEDUbuntu-16.04-32bit | 2             | 4GB          | 20GB         | 2              | 1x NAT, 1x Host only |
| Host U SEEDUbuntu-16.04-32bit     | 2             | 4GB          | 20GB         | 1              | NAT                  |
| Host V SEEDUbuntu-16.04-32bit     | 2             | 2GB          | 20GB         | 1              | Host only            |

### Appliance Network Configuration

HOST U

<img src="./media/image3.png"
style="width:6.46203in;height:4.83314in" />

HOST V

<img src="./media/image4.png" style="width:6.5in;height:5.77708in" />

VPN Server NIC1

<img src="./media/image5.png"
style="width:6.31319in;height:4.79747in" />

VPN Server NIC 2

<img src="./media/image6.png"
style="width:6.26582in;height:4.59851in" />

### Connectivity Check: 

- Connectivity between Host V and VPN Server

<img src="./media/image7.jpeg" style="width:6.5in;height:5.69861in" />

<img src="./media/image8.jpeg" style="width:6.5in;height:5.69861in" />

- Connectivity between VPN Server and Host U  
<img src="./media/image9.jpeg"
style="width:4.43671in;height:3.3481in" />

<img src="./media/image10.jpeg"
style="width:4.49306in;height:3.51899in" />

## Task 2

### Task 2a

- HOSTU

Missing scapy package for python2 Require excute the command  
pip3 install scapy

Screenshot of base code

<img src="./media/image11.png" style="width:6.5in;height:4.62986in" />

Screenshot of excution

<img src="./media/image12.png" style="width:6.5in;height:2.50278in" />

Excute sudo ./tun.py

<img src="./media/image13.png" style="width:6.5in;height:0.70278in" />

Tun0 address

<img src="./media/image14.png" style="width:6.5in;height:3.48403in" />

### Task 2b

After excution of the following command

// Assign IP address to the interface

> $ sudo ip addr add 192.168.53.99/24 dev tun0

// Bring up the interface

> $ sudo ip link set dev tun0 up

<img src="./media/image15.png" style="width:6.5in;height:4.62986in" />

Screenshot for base modified according from the lab manual

<img src="./media/image16.png" style="width:6.5in;height:4.62986in" />

### Task 2c

Screenshot for base modified according from the lab manual

<img src="./media/image17.png" style="width:6.5in;height:5.12014in" />

Screenshot for excution screen

<img src="./media/image18.png" style="width:6.5in;height:2.33889in" />

IP address

<img src="./media/image19.png" style="width:6.5in;height:5.12014in" />

Screenshot of ping to a host at 192.168.60.1, 192.168.53.100,
192,168,53.99

<img src="./media/image20.png" style="width:6.5in;height:5.12014in" />

- On Host U, ping a host in the 192.168.53.0/24 network. What are
printed out by the tun.py program? What has happened? Why?

This is because the another end of the tunnel is not setup yet, the
packet found a route for 192.168.53.0/24 via tun0, so the packet pass
top this interface and the application able to get the packet. For
192.168.53.99, the ping command success, because it is the address of
local adapter, so the icmp message goes into loopback interface. The
application has the following printout

<img src="./media/image21.png" style="width:6.5in;height:2.33889in" />

- On Host U, ping a host in the internal network 192.168.60.0/24, Does
tun.py print out anything? Why?

Because which command ping excute to ip address 192.168.60.1, the os
lookup the routing table and found the packet should pass via the
physical interface ens33, so the packet did not pass through tun0
interface and the application can not catpure the packet.

### Task 2d

- Screenshot of the code

<img src="./media/image22.png" style="width:6.24028in;height:9in" />

- Test ping from 192.168.53.99 to 192.168.53.100

<img src="./media/image23.png"
style="width:6.49931in;height:1.82278in" />

- Tun.py output

<img src="./media/image24.png"
style="width:6.23968in;height:5.68987in" />

When arbitrary data placed on the interface, there is no response from
the tun.py and the packet is discarded

## Task 3

Need to install scapy module to VPN Server, run the following command to installl the scapy module

> sudo pip3 install scapy

code screenshot at HOSTU

<img src="./media/image25.png" style="width:6.5in;height:7.24722in" />

Code screenshot at VPN Server

<img src="./media/image26.png" style="width:6.5in;height:4.14306in" />

- Observation

Screenshoot of running the tun_client.py

<img src="./media/image27.png"
style="width:6.23767in;height:0.82278in" />

Screenshoot of running the tun_client.py

<img src="./media/image28.png" style="width:6.5in;height:4.14306in" />

Test with ping to 192.168.53.100

<img src="./media/image29.png"
style="width:6.49925in;height:1.55063in" />

Run the tun server.py program on VPN Server, and then run tun client.py
on Host U

There is output for packet send to the 192.168.53.100. But ping test
fail. The reason behind is that there is only one way traffic from HOST
U to VPN Server the tunnel works in one way and no ip address assigned
as 192.168.53.100 at VPN Server, and you can observe the ping packet is
encalpulated inside udp packet.

The command is

>$ sudo ip route add 192.168.60.0/24 dev tun0 via 192.168.53.99 

Screenshot at VPNServer tun_server.py output

<img src="./media/image30.png" style="width:6.5in;height:4.14306in" />

Screen shot of tun_client.py output

<img src="./media/image31.png"
style="width:6.49954in;height:0.82911in" />

## Task 4

Run command and update the sysctl.conf for permanent configuration
> sudo sysctl net.ipv4.ip_forward=1 

<img src="./media/image32.png" style="width:6.5in;height:4.13889in" />

VPN Server code listing

<img src="./media/image33.png"
style="width:6.31646in;height:8.25771in" />

Packet capture by the following command

<img src="./media/image34.png" style="width:6.5in;height:1.16837in" />

packet captured at HOSTV

<img src="./media/image35.png" style="width:6.5in;height:3.14931in" />

## Task 5

Code Listing for HOST U

<img src="./media/image36.png" style="width:4.8481in;height:8.958in" />

Code listing for VPN Server

<img src="./media/image37.png"
style="width:5.41772in;height:8.54654in" />

Screenshot for ping and traceroute succes

<img src="./media/image38.png" style="width:6.5in;height:2.66667in" />

Packet capture of testing

<img src="./media/image39.png" style="width:6.5in;height:4.73194in" />

Screenshot for telnet test success

<img src="./media/image40.png" style="width:6.5in;height:4.30208in" />

Packet capture at HOST V of the telnet test

<img src="./media/image41.png" style="width:6.5in;height:4.73194in" />

Description

In ping test, the icmp packet at Host U is target to 192.168.60.101, by
the static route setup, the packet will route to interface tun0 and next
hop address is 192.168.59.100. the packet will delivery to tun 0 and
capture by the application tun_client.py. Then tun_client.py encapulate
the icmp packet with a udp packet and deliver to 10.0.2.8 with
destination port 9090. As the application tun_server.py is started and
the udp socket is listensing at port 9090. The UDP packet to
10.0.2.8:9090 will capturedby the tun_server.py and the application will
decapulate the UDP packet and extract its payload to become the IP
packet. After that the application will pass the packet to tun0 right
away. By the IP forward function is enabled at VPNserver’s kernel. The
decapulated packet will forward to 192.168.60.101 according to the
destination address at ip header.

Vice versa, the HOST V server receive the ICMP request and response with
ICMP reply to VPN server. According to the routing table at VPNServer,
the VPN Server receive a icmp reply packet with src ip 192.168.60.101
and destnation 192.168.53.99. the VPN server will forward this packet to
tun0 interface and capture by tun_server.py application. The application
will encapsulate the packet with a UDP packet with destination ip
10.0.2.7 and destination port 9090 Via ens33 interface at VPN server. At
next step, the ens33 interface at Host U will receive the UDP packet and
the application has a udp socket that is listensing at 9090 port. The
application will receive the packet and decapsulate to the icmp reply
packet. Finally, it pass back to tun0 interface and OS will pass to ping
application with success result.

![](./media/image42.png)

## Task 6 Tunnel-Breaking Experiment

There are 3 possibilites of tunnel breakiing; Firstly, the tunnel breaks
at client side. Secondly, the tunnel breaks at server side. Finally, the
tunnel breaks because the network connectivity to VPNServer lost.

### Case 1, tunnel breaks at HostU side

Procedures for this test

1.  Setup the tunnel by starts tun_client.py at HOST U and tun_server.py
    at VPNServer

2.  At HOST U start telnet connection to HOST V (192.168.60.101).

3.  Test telnet connection by login the session to HOSTV, you will see
    you can type character to the telnet session

4.  Kill tun_client.py, and test will type a few character, observe what
    is happening.

5.  Start the tun_client.py again and observe what is happening

### Case 2, tunnel breaks at VPNServer side

Procedures for this test

1.  Setup the tunnel by starts tun_client.py at HOST U and tun_server.py
    at VPNServer

2.  At HOST U start telnet connection to HOST V (192.168.60.101).

3.  Test telnet connection by login the session to HOSTV, you will see
    you can type character to the telnet session

4.  Kill tun_server.py, and test will type a few character, observe what
    is happening.

5.  Start the tun\_ server.py again and observe what is happening

### Case 3, tunnel breaks because the network connectivity to VPNServer lost

1.  Setup the tunnel by starts tun_client.py at HOST U and tun_server.py
    at VPNServer

2.  At HOST U start telnet connection to HOST V (192.168.60.101).

3.  Test telnet connection by login the session to HOSTV, you will see
    you can type character to the telnet session

4.  Diconeect the host U ens33 connection by config at VM Host, which
    simulate a network cable unplug event, type a few character and
    observe what is happening.

5.  Start the tun\_ server.py again and observe what is happening

### Results of the tests

All 3 tests has the same result, the connection can resume if the
disconnection time is not too long. The charater typed after tunnel
breaks can resume and send to the telent session. And telnet session is
resumed without issue.

From my understanding telnet use TCP as protocol, the packet send
without ack from remote end will resend within certain time windows.
That makes the connection persistent and recoverable even the UDP tunnel
breaks. However, the disconnect time beyond the Retransmission timeout
RTO. In RFC 1122, the recommendation is at least 100 seconds for the
timeout, which corresponds to a value of at least 8, ubuntu default at
15. Another recommendation is at least 3 retransmissions, which is the
default at ubuntu.

<img src="./media/image43.png" style="width:6.5in;height:4.62986in" />

## Task 7

<img src="./media/image44.png" style="width:6.5in;height:4.14306in" />

## Task 8

Requrie ro remove the default route at HOST U

sudo ip route del 0.0.0.0/0

initial routing table at HOSTU

<img src="./media/image45.png" style="width:6.5in;height:4.62986in" />

Initial Routing table at VPN Server

<img src="./media/image46.png" style="width:6.5in;height:4.62986in" />

initial routing table at HOSTV

<img src="./media/image47.png" style="width:6.5in;height:4.14306in" />

HOST U tun_client.py code listing

<img src="./media/image48.png"
style="width:5.17226in;height:9.55696in" />

The telnet from HostU to HostV is failed; the packet is dropped at the
HOSTV side

![](./media/image49.png)

VPN Server and HOSTU has traffic the tunnel is operational

Packet capture at ens33 interface at vpnserver

<img src="./media/image50.png" style="width:6.5in;height:4.13194in" />

The tun_server.py can decapulate the tunnel packet back into telnet
packet and forward to 192.168.60.0/24 subnet.

Packet capture at tun0 interface at vpnserver

<img src="./media/image51.png" style="width:6.5in;height:4.13194in" />

Packet capture at ens34 interface at vpnserver

<img src="./media/image52.png" style="width:6.5in;height:5.11806in" />

This is because the ip packet source address is 192.168.30.99, which is
the tun0 ipaddress at HOST U. To solve this issue, simply add the
default route or static route to host V for 192.168.30.0/24 at interface
ens33 via 192.168.60.1, the problem will solve. The following is the
command for the route add.

At host V

sudo ip route del 192.168.30.0/24 dev ens33 via 192.168.60.1

At VPN Server

sudo ip route add 192.168.30.0/24 dev tun0

this is because there is no route for 192.168.30.0/24 in VPNserver and
HOSTV, that means they do not know how to put the packet to correct
device and subnet.

## Task9

Code listing of HOSTU

<img src="./media/image53.png"
style="width:5.40506in;height:7.38559in" />

Ping result and program output

<img src="./media/image54.png" style="width:6.5in;height:4.63403in" />

<img src="./media/image55.png" style="width:6.5in;height:1.63924in" />

Packet capture

<img src="./media/image56.png" style="width:6.5in;height:4.13194in" />

Observation

The ping operation is failed, but the application has an extra output of
other subnet’s packet

After adding more code to the HOST U, the following is the code listing
and output

<img src="./media/image57.png" style="width:6.5in;height:2.13924in" />

Tap_client.py output

<img src="./media/image58.png" style="width:6.5in;height:5.44792in" />

<img src="./media/image59.png"
style="width:5.46891in;height:9.45381in" />

#  References

Braden, R. (1989, October). *RFC 1122 - Requirements for internet
hosts - Communication layers*. IETF
Tools. <https://tools.ietf.org/html/rfc1122>

Du, W. (2020). *VPN tunneling lab*. SEED
Project. <https://seedsecuritylabs.org/Labs_16.04/Networking/VPN_Tunnel/>
