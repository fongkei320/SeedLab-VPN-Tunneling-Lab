#!/usr/bin/python3
import fcntl
import struct
import os
import time
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000
# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tun%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

while True:
# Get a packet from the tun interface
	packet = os.read(tun, 2048)
	if True:
		ip = IP(packet)
		print(ip.summary())
		#Send out a spoof packet using the tun interface
		if(ip.haslayer(ICMP)):
			print("this is ICMP packet")
			icmppayload = ip.getlayer(ICMP)
			print(icmppayload.display())
			if(icmppayload.type == 8):
				print("this is ICMP request, send icmp reply")
				newip = IP(src=ip.dst, dst=ip.src)
				newpayload = icmppayload
				#change the icmp type to 0 (imcp reply) and update the checksum
				newpayload.type = 0
				newpayload.chksum -= 8
				print(newpayload.display())
				newpkt = newip/newpayload/icmppayload.load
				os.write(tun, bytes(newpkt))
				print("write some arbitrary data (Hellow world to interface")
				print(bytes("Hello World", encoding="ascii"))
				os.write(tun, bytes("Hello World", encoding="ascii"))

		
