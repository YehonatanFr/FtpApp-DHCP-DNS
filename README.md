# FtpApp-DHCP-DNS
A Final project in Network course.      
**The project were written by:** 
- [Yehonatan Friedman](https://github.com/YehonatanFr)
- [Hagay Knorovich](https://github.com/hagayknoro)

# About the ptoject    
In this Project we implements FTP(File Transfer Protocol) with TCP, based on client-server model with multiple serveres.     
When a client connect to the internet he doesnt have IP address, so he send a discovery packet which tell us "hey i'm new",     
the DHCP server gut the packet and send hin an IP address.     
Afterwards, the client ask what the IP address of the FTP server, so the DNS server giv him the IP address of the FTP server,      
and then the client connect with the server and he choose an action from the action list.        
## Protocols we used       
In the project we used several protocols, here is a brief explanation.      
### DHCP (Dynamic Host Configuration Protocol)     
DHCP is a network protocol used to automatically assign IP addresses and other network configuration settings to devices on a network.     
When a device connects to a network, it sends a broadcast message requesting network configuration information,       
and a DHCP server responds with the necessary information, such as an IP address, subnet mask, default gateway, and DNS servers.      
This process is known as DHCP lease.      

DHCP operates on the client-server model,     
where the DHCP server is responsible for assigning and managing IP addresses,      
and the client device receives the address and other settings.      
DHCP is used in many networks, including home, business, and enterprise networks,       
to simplify network management and reduce the chances of IP address conflicts.  
[Move to top](#FtpApp-DHCP-DNS)      

### DNS (Domain Name System)      
DNS is a protocol used to translate human-readable domain names.     
When a user types a domain name into a web browser or other network application,       
the application sends a DNS query to a DNS server, requesting the IP address of the domain name.    

The DNS server then searches its database for the IP address associated with the domain name and returns it to the requesting application.      
DNS operates on a hierarchical, distributed database system,        
where different levels of DNS servers are responsible for different parts of the domain name system.  
[Move to top](#FtpApp-DHCP-DNS)      

### TCP (Transmission Control Protocol)      
TCP is a reliable, connection-oriented protocol used to transmit data over a network.        
TCP breaks down data into packets and sends them over the network,       
ensuring that they are delivered in the correct order and without errors.       
It also includes features such as flow control and congestion control to ensure efficient use of network resources.    

TCP uses a three-way handshake process to establish a connection between two devices,      
where the devices exchange control messages to establish and confirm the connection.         
Once the connection is established, data can be transmitted in both directions.        
TCP is widely used for applications such as web browsing, email, and file transfers.      
[Move to top](#FtpApp-DHCP-DNS)       

## What is FTP?      
FTP (File Transfer Protocol) is a protocol used to transfer files between computers on a network.      
In our project the computer is both the client and the server.      
The client initiates a connection to the server and then requests to transfer one or more files.      
We implemented FTP to support several operations.     
For example download a file from the server, upload a file from the server, remove a file from the server, etc.      

Usually, FTP uses two separate channels to transfer files: a command channel and a data channel.     
The command channel is used for sending commands between the client and server,       
such as requesting a file transfer or listing the contents of a directory.       
In our case we used one channel that transmits both commands and the data.       
[Move to top](#FtpApp-DHCP-DNS)       

# How to run the project? 
## Before the run
First, we need to create two folders where the code files will be stored.     
one for the client named "ftp_client_files", and one for the server named "ftp_server_files".      
Then, we need to choose the files we want to download or upload.      

After completing these steps, we need to pay attention to an important detail.      
In the code for the client, DHCP, and DNS server, we used a variable called `device`.       
We did this because each computer has a different device name.        
To find the name of the device, we need to run the command `ifconfig` and then locate our device's name.
   

## Start to run      
First, to run the the project we need to used four trminals in the same time.       
And we need to run thr commands with administrator permissions, meaning with `sudo` command.  

![Screenshot from 2023-03-23 12-21-29](https://user-images.githubusercontent.com/118724971/227174652-df7bc621-af28-41a0-9e0f-b5ca9aa8bf79.png)

After we run all the following commands, we can see the server cummunicate between them, the DHCP server give an IP address for the client,     
then the DNS server give the IP of the FTP server to the client, and then the client cummunicate with the server and ask what he wants to do?     


![Screenshot from 2023-03-23 12-27-40](https://user-images.githubusercontent.com/118724971/227175684-f92c29bd-783d-4769-b58e-f0e5ae4c367e.png)


Then the client choose whatever he wants to do.     

[Move to top](#FtpApp-DHCP-DNS) 

# Summary
For summary, The project was definitely not a simple and very challenging project.        
We learned a lot about how to communicate based on TCP,       
how much TCP enables reliable communication, what protocols it uses to be reliable, etc.         
In addition, we learned about how to build packets using the scapy library,        
about the roles of the DHCP and DNS servers.


Hope you enjoyed :wink:






