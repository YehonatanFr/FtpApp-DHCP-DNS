from scapy.all import *
from scapy.layers.dns import DNS, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether


#get the machine MAC
DNS_MAC = uuid.getnode()
DNS_MAC = ':'.join(['{:02x}'.format((DNS_MAC >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])

# define DNS server IP address
dns_ip = "192.168.1.2"

# define DNS server port
dns_port = 53

# difine goodel DNS server ip address
google_dns_ip = "8.8.8.8"

# difine the domain name for ip mapping
dns_rec = {"yhonatan&hagayFTP.org": "127.0.0.1"}

device = "enp0s3"

# the handeling DNS query func
def query_dns_handler(packet):
    client_ip = packet[IP].src
    client_port = packet[UDP].sport
    query = packet[DNS].qd
    qname = query.qname.decode()
    qname = qname[:-1]
    # check if the query is in the local DNS rec
    if qname in dns_rec:
        # make a response packet
        ip = dns_rec[qname]
        response  = Ether(src=DNS_MAC, dst="ff:ff:ff:ff:ff:ff") / \
                IP(src=dns_ip, dst=client_ip) / \
                UDP(sport=dns_port, dport=client_port) / \
                DNS(id=packet[DNS].id, qd=query, an=DNSRR(rrname=qname, rdata=ip))
        

        # send the respons
        time.sleep(2)
        sendp(response, iface=device)
        print('a domain ip sent')
    else:
        # get the ip from google dns server
        response = sr1(IP(dst=google_dns_ip) / UDP(dport=53) / packet[DNS], verbose=0)

        # make my oun response packet ote of the google response
        ip = response[DNS].an
        response_packet  = Ether(src=DNS_MAC, dst="ff:ff:ff:ff:ff:ff") / \
                IP(src=dns_ip, dst=client_ip) / \
                UDP(sport=dns_port, dport=client_port) / \
                DNS(id=packet[DNS].id, qd=query, an=DNSRR(rrname=qname, rdata=ip))       
        

        # send the response
        send(response_packet, verbose=0)
        print('a domain ip sent requested from googel')


# start opertion of the dns srever
print("The DNS server is up and his ip is:", dns_ip)
sniff(filter=f"udp port {dns_port} and dst {dns_ip}", prn=query_dns_handler)

