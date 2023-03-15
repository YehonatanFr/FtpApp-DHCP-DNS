from scapy.all import *
import random

from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

# Define the DHCP server MAC address and IP address
SERVER_MAC = uuid.getnode()
SERVER_MAC = ':'.join(['{:02x}'.format((SERVER_MAC >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
SERVER_IP = "192.168.1.1"

device = "enp0s3"

# Define the DHCP options
dhcp_options = [("subnet_mask", "255.255.255.0"),
                ("router", SERVER_IP),
                ("domain_name_server", "192.168.1.2"),
                ("lease_time", 86400)]

taken_ips = []


def get_free_ip():
    rand_ip = random.randint(10, 99)
    while rand_ip in taken_ips:
        rand_ip = random.randint(10, 99)
    taken_ips.append(taken_ips)
    return f"192.168.1.{rand_ip}"


#  the handeling DHCP func
def dhcp_handler(pkt):
    offered_ip = get_free_ip()
    
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:
        # A discover packet has received, sending an offer packet

        
        dhcp_offer = Ether(src=SERVER_MAC, dst=pkt[Ether].src) / \
            IP(src=SERVER_IP, dst="255.255.255.255") / \
            UDP(sport=67, dport=68) / \
            BOOTP(op="BOOTREPLY", yiaddr=offered_ip, siaddr=SERVER_IP, chaddr=pkt[Ether].src) / \
            DHCP(options=[("message-type", "offer"),
                           ("server_id", SERVER_IP),
                           ("lease_time", dhcp_options[3][1]),
                           ("subnet_mask", dhcp_options[0][1]),
                           ("router", dhcp_options[1][1]),
                           ("domain_name_server", dhcp_options[2][1]),
                          "end"])

        time.sleep(1)
        sendp(dhcp_offer, iface=device)
        time.sleep(1)
        print('an offer packet sent')



    # Waiting for a request packet and then sending  an ACK packet
    if  pkt[DHCP].options[0][1] == 3:
        offered_ip = pkt[BOOTP].yiaddr
        dhcp_ack = Ether(src=SERVER_MAC, dst=pkt[0][Ether].src) / \
                    IP(src=SERVER_IP, dst="255.255.255.255") / \
                    UDP(sport=67, dport=68) / \
                    BOOTP(yiaddr=offered_ip, siaddr=SERVER_IP, chaddr=pkt[0][Ether].src,
                            xid=pkt[0][BOOTP].xid, op =5 ) / \
                    DHCP(options=[("message-type", 5 ),
                                    ("server_id", SERVER_IP),
                                    ("lease_time", dhcp_options[3][1]),
                                    ("subnet_mask", dhcp_options[0][1]),
                                    ("router", dhcp_options[1][1]),
                                    ("domain_name_server", dhcp_options[2][1]),
                                    "end"])
        time.sleep(2)
        sendp(dhcp_ack, iface=device)
        time.sleep(1)
        print('an ACK pacet sent')


print('the dhcp server is up')
# Start the DHCP server
while True:
    sniff(filter="udp and (port 67 or 68)", prn=dhcp_handler)
