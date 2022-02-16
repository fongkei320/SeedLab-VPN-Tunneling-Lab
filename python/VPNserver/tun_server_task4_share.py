#!/usr/bin/python3
import fcntl
import struct
import os
import time
from scapy.all import *

tunnelremoteprealip = "10.0.2.7"
tunnelremoteprealport = 9090
tunnellocalip = "192.168.53.100"
tunnelremoteip = "192.168.53.99"
tunnelsubnetmask = "24"


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

os.system("ip addr add {}/{} dev {}".format(tunnellocalip,tunnelsubnetmask,ifname))
os.system("ip link set dev {} up".format(ifname))

IP_A = "0.0.0.0"
PORT = 9090
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

while True:
	data, (ip, port) = sock.recvfrom(2048)
	print("{}:{} --> {}:{}".format(ip, port, IP_A, PORT))
	pkt = IP(data)
	print(" Inside: {} --> {}".format(pkt.src, pkt.dst))
	os.write(tun, bytes(pkt))
