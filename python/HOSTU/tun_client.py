#!/usr/bin/python3
import select
import fcntl
import struct
import os
import time
from scapy.all import *

tunnelremoteprealip = "10.0.2.8"
tunnelremoteprealport = 9090
tunnellocalip = "192.168.30.99"
tunnelremoteip = "192.168.53.100"
tunnelsubnetmask = "24"
tunneltargetsubnet = "192.168.60.0"
tunneltargetsubnetmask = "24"


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
print("setup the ip and bring the interface up")
print("ip addr add {}/{} dev {}".format(tunnellocalip,tunnelsubnetmask,ifname))
print("ip link set dev {} up".format(ifname))
os.system("ip addr add {}/{} dev {}".format(tunnellocalip,tunnelsubnetmask,ifname))
os.system("ip link set dev {} up".format(ifname))

#setup the ip route to target subnet
print("Setup the ip route to target subnet by command")
print("ip route add {}/{} dev {} via {}".format(tunneltargetsubnet,tunneltargetsubnetmask,ifname,tunnelremoteip))
os.system("ip route add {}/{} dev {} via {}".format(tunneltargetsubnet,tunneltargetsubnetmask,ifname,tunnelremoteip))

#Create UDP socket
sockTX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Create UDP socket for receive
IP_A = "0.0.0.0"
PORT = 9090
sockRx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockRx.bind((IP_A, PORT))

while True:

	# this will block until at least one interface is ready
	ready, _, _ = select.select([sockRx, tun], [], [])
	for fd in ready:
		if fd is sockRx:
			# Get a packet from the udp tunnel
			data, (ip, port) = sockRx.recvfrom(2048)
			print("From sock {}:{} --> {}:{}".format(ip, port, IP_A, PORT))
			pkt = IP(data)
			print(" Inside: {} --> {}".format(pkt.src, pkt.dst))
			# Extract the Inside Packet
			# pass the extracted packet to tun interface
			print("pass the extracted packet to tun interface")
			os.write(tun, bytes(pkt))
		
		if fd is tun:
			# Get a packet from the tun interface
			packet = os.read(tun, 2048)
			pkt = IP(packet)
			print("From tun ==>: {} --> {}".format(pkt.src, pkt.dst))
			# Extract the Inside Packet
			# pass the extracted packet to tunnel
			print("pass the extracted packet to udp tunnel")
			sockTX.sendto(packet, (tunnelremoteprealip, tunnelremoteprealport))

