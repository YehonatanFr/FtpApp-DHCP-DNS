import socket
import os
from telnetlib import IP
import time
from datetime import datetime
import ast
from datetime import datetime
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNSQR, DNS
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

device = "enp0s3"
#get the machine MAC
CLIENT_MAC = uuid.getnode()
CLIENT_MAC = ':'.join(['{:02x}'.format((CLIENT_MAC >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])

cliient_ip = None

# UDP server IP and port number
ftp_server_domain_name = "yhonatan&hagayFTP.org"
ftp_server_ip = None
dns_ip = "192.168.1.2"
server_port = 30367
dns_port = 53

ftp_server_ip = '127.0.0.1'
CLIENT_PORT = 20647

max_packet_size = 9216

ftp_dir = 'ftp_client_files/'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_dhcp_packet(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        # DHCP Offer packet received, send DHCP Request packet to accept the offered lease
        transaction_id = packet[BOOTP].xid
        server_ip = packet[IP].src
        dhcp_offer_ip = packet[BOOTP].yiaddr

        # Construct DHCP Request packet
        dhcp_request = Ether(src=CLIENT_MAC, dst="ff:ff:ff:ff:ff:ff") / \
            IP(src="0.0.0.0", dst=server_ip) / \
            UDP(sport=68, dport=67) / \
            BOOTP(op=1, chaddr=CLIENT_MAC, xid=transaction_id,yiaddr=dhcp_offer_ip) / \
            DHCP(options=[("message-type", "request"),
                           ("server_id", server_ip),
                           ("requested_addr", dhcp_offer_ip),
                           "end"])

        
        # Send DHCP Request packet
        time.sleep(1)
        sendp(dhcp_request, iface=device)
        time.sleep(1)
        return dhcp_offer_ip
        
    
def handle_dhcp_ack_packet(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 5:
        dhcp_offer_ip = packet[BOOTP].yiaddr
        CLIENT_IP = dhcp_offer_ip
        print('ACK hes arieved')
        return dhcp_offer_ip
        


def get_client_ip():
    # Define the DHCP options
    dhcp_options = [("message-type", "discover"), "end"]

    # Construct and send DHCP Discover packet to initiate DHCP negotiation
    dhcp_discover = Ether(src=CLIENT_MAC, dst="ff:ff:ff:ff:ff:ff") / \
        IP(src="0.0.0.0", dst="255.255.255.255") / \
        UDP(sport=68, dport=67) / \
        BOOTP(op=1, chaddr=CLIENT_MAC, xid=random.randint(1, 1000000000)) / \
        DHCP(options=dhcp_options)

    time.sleep(1)
    sendp(dhcp_discover, iface=device)
    
    print("Sent DHCP Discover")


    # Wait for DHCP Offer packet from server
    prn = sniff(iface=device, filter="udp and (port 67 or 68)", timeout=10, count =1)[0]
    ip = handle_dhcp_packet(prn)
    
        # Wait for DHCP Offer packet from server
    
    prnt = sniff(iface=device, filter="udp and (port 67 or 68)", timeout=10, count =1)[0]
    time.sleep(1)
    ip = handle_dhcp_ack_packet(prnt)
    
    return str(ip) 


def anss_dns_handler(packet):
    # Extract IP address from DNS response
    found_ip = packet[DNS].an.rdata
    ftp_server_ip = found_ip
    print(ftp_server_ip)
    return ftp_server_ip


def get_ftp_server_ip():
    print('trying to get ftp ip adress')
    # Create DNS query packet
    query = Ether(src=CLIENT_MAC, dst="ff:ff:ff:ff:ff:ff") / \
    IP(src=cliient_ip, dst=dns_ip) / \
    UDP(sport=CLIENT_PORT, dport=dns_port) / \
    DNS(rd=1, qd=DNSQR(qname=ftp_server_domain_name))

    time.sleep(1)
    sendp(query, iface=device)
    
    prnt = sniff(iface=device, filter=f"udp port {CLIENT_PORT} and dst {cliient_ip}", timeout=10, count =1)[0]
    ip = anss_dns_handler(prnt)
    
    return str(ip)

# Function to check if a file exists
def file_exists(file_name):
    if os.path.isfile(ftp_dir + file_name):
        return True
    else:
        return False
    
# Function to print the files in the folder
def ListFolder(ftp_dir):
    items = os.listdir(ftp_dir)
    for item in items:
        print(item)

# Remove file in the server
def remove(client_socket):
    print("\nThe files you can remove:")
    request_packet = client_socket.recv(max_packet_size)
    filelist = ast.literal_eval(request_packet.decode())
    for file in filelist:
        print(file)
    file_name = input('\nEnter the file name: ')
    client_socket.send(file_name.encode())
    msg_packet = client_socket.recv(max_packet_size)
    msgfromclient = msg_packet.decode()
    print(msgfromclient)
    print()

# Receive file list
def receivelist(client_socket):
    file_list_bytes = b""
    while True:
        chunk = client_socket.recv(max_packet_size)
        if not chunk:
            break
        if b"END_OF_LIST" in chunk:
            chunk = chunk.replace(b"END_OF_LIST", b"")
            file_list_bytes += chunk
            break
        file_list_bytes += chunk

    file_list_str = file_list_bytes.decode()

    print("\nFile list:")
    print(file_list_str)

# Function to receive a file from the server using TCP
# def receive_file(file_name):
#     time.sleep(1)
#     data = client_socket.recv(max_packet_size)
#     file_size = float(data)
#     msg = 'ack'
#     client_socket.send(msg.encode())
#     print('ack sent from client')
#     print(f"The size of the file for download is: {file_size/1000} KB")
#     print('Start to download.. ')
#     with open(ftp_dir + file_name, 'wb') as f:
#         packets_received = 0
#         while packets_received < file_size:
#             packet_data = client_socket.recv(max_packet_size)
#             f.write(packet_data)
#             packets_received += len(packet_data)
#     print('Finish download File received successfully!\n')

def receive_file(file_name):

    filepath = os.path.join(ftp_dir , file_name)
    time.sleep(1)
    data = client_socket.recv(max_packet_size)
    file_size = float(data)
    msg = 'ack'
    client_socket.send(msg.encode())
    print('ack sent from client')

    print(f"The size of the file for download is: {file_size/1000} KB")
    print('Start to download.. ')
    f = open(filepath ,"wb")

    file_half_size = int(file_size/2)

    # Receive first half
    packets_received_first_half = 0
    while packets_received_first_half < file_half_size:
        packet_data = client_socket.recv(max_packet_size)
        f.write(packet_data)
        packets_received_first_half += len(packet_data)

    time.sleep(1)
    msg_data = client_socket.recv(max_packet_size)
    msg_first_half = msg_data.decode()

    time.sleep(1)
    print("Msg from the server: ", msg_first_half)
    action = input("\nDo you want to contiue the download? [Y/n]")
    client_socket.send(action.encode())

    if(action != 'Y'):
        os.remove(filepath)
        return

    # Receive second half
    packets_received_second_half = 0
    while packets_received_second_half < file_size/2:
        packet_data = client_socket.recv(max_packet_size)
        f.write(packet_data)
        packets_received_second_half += len(packet_data)

    f.close


# Function to send a file to a client using TCP
def send_file(file_name):
    print('Send the file size')
    file_size = os.path.getsize(ftp_dir + file_name)
    client_socket.send(str(file_size).encode())
    time.sleep(1)
    msg = client_socket.recv(max_packet_size)
    ack_msg = msg.decode()
    print('Ack messege has arrived ', ack_msg) 
    f = open(ftp_dir + file_name, "rb")
    file_data = f.read()
    client_socket.sendall(file_data)
    f.close()

# Download function to download a file from the server
def download():
        request_packet = client_socket.recv(max_packet_size)
        filelist = ast.literal_eval(request_packet.decode())
        print("\nThe files you can Download:")
        for file in filelist:
            print(file)
        file_name = input('\nEnter the file name: ')
        client_socket.send(file_name.encode())
        receive_file(file_name)
        print('Finish download\n')

# Upload function to uplad file to the server folder
def upload(ftp_dir):
        print("\nHere are the files in the folder which you can upload to server:")
        ListFolder(ftp_dir)
        file_name = input('\nEnter the file name: ')
        print('Send the file name')
        client_socket.send(file_name.encode())
        print('Upload started')
        time.sleep(2)
        send_file(file_name)
        print('Finish upload File received successfully!\n')

cliient_ip = get_client_ip()
print(f"the client ip is now: {cliient_ip}")

ftp_server_ip = get_ftp_server_ip()
print(f"the descoverd FTP ip is: {ftp_server_ip}")

client_socket.connect((ftp_server_ip, server_port))
# The main loop
while True:

    # Receive the action fron the input and then send it to the server
    print("Please choose an action:")
    print("A. Download a file")
    print("B. Upload a file")
    print("C. Show files in the folder")
    print("D. Delete a file")
    print("E. Close the program")

    # Get the user's choice
    action = input("\nEnter your choice (A, B, C, D, or E): ")
    
    if action not in ['A', 'B', 'C', 'D', 'E']:
        print("\nSomethine is wrong please type again")
        action = input("Enter your choice (A, B, C, D, or E): ")
    client_socket.send(action.encode())

    client_socket.settimeout(10)
    if(action == 'A'):
        download()
    elif ( action == 'B'):
        upload(ftp_dir)
    elif ( action == 'C'):
        print("\nPlease choose way of print list:")
        print("Name - sorted by name")
        print("Date -  sorted by last added")
        print("Size - sorted by size")
        choice = input("Enter your choice: ")
        client_socket.send(choice.encode())
        receivelist(client_socket)
    elif ( action == 'D'):
        remove(client_socket)
    elif ( action == 'E'):
        print('Close the program')
        break
            
client_socket.close()