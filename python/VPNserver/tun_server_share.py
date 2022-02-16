#!/usr/bin/python3
import select
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

#setup the ip and bring the interface up
print("setup the ip to 192.168.53.100 and bring the interface up")
os.system("ip addr add {}/{} dev {}".format("192.168.53.100","24",ifname))
os.system("ip link set dev {} up".format(ifname))

#Create UDP socket
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Create UDP socket for receive
IP_A = "0.0.0.0"
PORT = 9090
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind((IP_A, PORT))

while True:

	# this will block until at least one interface is ready
	ready, _, _ = select.select([sock1, tun], [], [])
	for fd in ready:
		if fd is sock1:
			data, (ip, port) = sock1.recvfrom(2048)
			print("{}:{} --> {}:{}".format(ip, port, IP_A, PORT))
			pkt = IP(data)
			print("From sock Inside: {} --> {}".format(pkt.src, pkt.dst))
			os.write(tun, bytes(pkt))
		
		if fd is tun:
			packet = os.read(tun, 2048)
			pkt = IP(packet)
			print("From tun ==>: {} --> {}".format(pkt.src, pkt.dst))
			sock2.sendto(packet, ("10.0.2.7", 9090))

