import socket
import os
import time
from datetime import datetime

server_ip = '127.0.0.1'
server_port = 30367

max_packet_size = 9216

ftp_dir = 'ftp_server_files/'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_ip, server_port))

server_socket.listen(1)

print('Waiting for a connection...')

client_socket, client_address = server_socket.accept()

# Function to check if a file exists in the FTP server
def file_exists(file_name):
    if os.path.isfile(ftp_dir + file_name):
        return True
    else:
        return False
    
# Function to save the files in the folder
def ListFolder(ftp_dir):
    items = os.listdir(ftp_dir)
    return items

# Remove file in the server
def remove(ftp_dir):
    filelist = ListFolder(ftp_dir)
    filelist_bytes = bytes(str(filelist), encoding='utf-8')
    client_socket.send(filelist_bytes)
    print('Server wait for file name')
    request_packet = client_socket.recv(max_packet_size)
    file_name = request_packet.decode()
    filepath = os.path.join(ftp_dir , file_name)
    if os.path.exists(filepath):
        os.remove(filepath)
        msg = 'File has been removed'
        client_socket.send(msg.encode())




# Print the files sorted by name
def SendFileListByName():
    file_list = []
    for file_name in os.listdir(ftp_dir):
        if os.path.isfile(os.path.join(ftp_dir, file_name)):
            file_date = os.path.getmtime(ftp_dir + file_name)
            date_modified = datetime.fromtimestamp(file_date)
            formatted_date = date_modified.strftime("%Y:%m:%d")
            file_size = os.path.getsize(os.path.join(ftp_dir, file_name))
            file_list.append((file_name, file_size, formatted_date))
    sorted_file_list = sorted(file_list, key=lambda x: x[0])
    file_list_str = "\n".join([f"\033[1mfile name:\033[0m{file[0]}  \033[1mSize:\033[0m{file[1]/1000}KB  \033[1mDate:\033[0m{file[2]}" for file in sorted_file_list])

    chunks = [file_list_str[i:i+max_packet_size] for i in range(0, len(file_list_str), max_packet_size)]
    for chunk in chunks:
        if chunk is not None:
            client_socket.send(chunk.encode())

    client_socket.send(b"END_OF_LIST")

# Print the files sorted by size
def SendFileListBySize():
    file_list = []
    for file_name in os.listdir(ftp_dir):
        if os.path.isfile(os.path.join(ftp_dir, file_name)):
            file_date = os.path.getmtime(ftp_dir + file_name)
            date_modified = datetime.fromtimestamp(file_date)
            formatted_date = date_modified.strftime("%Y:%m:%d")
            file_size = os.path.getsize(os.path.join(ftp_dir, file_name))
            file_list.append((file_name, file_size, formatted_date))
    sorted_file_list = sorted(file_list, key=lambda x: x[1])
    file_list_str = "\n".join([f"\033[1mfile name:\033[0m{file[0]}  \033[1mSize:\033[0m{file[1]/1000}KB  \033[1mDate:\033[0m{file[2]}" for file in sorted_file_list])

    chunks = [file_list_str[i:i+max_packet_size] for i in range(0, len(file_list_str), max_packet_size)]
    for chunk in chunks:
        if chunk is not None:
            client_socket.send(chunk.encode())
    
    client_socket.send(b"END_OF_LIST")



# Print the files sorted by date
def SendFileListByDate():
    file_list = []
    for file_name in os.listdir(ftp_dir):
        if os.path.isfile(os.path.join(ftp_dir, file_name)):
            file_date = os.path.getmtime(ftp_dir + file_name)
            date_modified = datetime.fromtimestamp(file_date)
            formatted_date = date_modified.strftime("%Y:%m:%d")
            file_size = os.path.getsize(os.path.join(ftp_dir, file_name))
            file_list.append((file_name, file_size, formatted_date))
    sorted_file_list = sorted(file_list, key=lambda x: x[2])
    file_list_str = "\n".join([f"\033[1mfile name:\033[0m{file[0]}  \033[1mSize:\033[0m{file[1]/1000}KB  \033[1mDate:\033[0m{file[2]}" for file in sorted_file_list])

    chunks = [file_list_str[i:i+max_packet_size] for i in range(0, len(file_list_str), max_packet_size)]
    for chunk in chunks:
        if chunk is not None:
            client_socket.send(chunk.encode())

    client_socket.send(b"END_OF_LIST")

# Send file list by filter by user's choice
def SendFileList():
    choice_packet = client_socket.recv(max_packet_size)
    choice = choice_packet.decode()
    if(choice == 'Name'):
        print('Server send list of files orderd by name..')
        SendFileListByName()
    if(choice == 'Date'):
        print('Server send list of files orderd by date..')
        SendFileListByDate()
    elif(choice == 'Size'):
        print('Server send list of files orderd by size..')
        SendFileListBySize()
    else:
        print("Something is wrong..")
        return

# Function to send a file to a client using TCP
# def send_file(file_name):
#     if file_exists(file_name):
#         file_size = os.path.getsize(ftp_dir + file_name)
#         client_socket.send(str(file_size).encode())
#         time.sleep(1)
#         msg = client_socket.recv(max_packet_size)
#         ack_msg = msg.decode()
#         if( ack_msg == 'ack'):
#             f = open(ftp_dir + file_name, "rb")
#             file_data = f.read()
#             client_socket.sendall(file_data)
#             f.close() 
#     else:
#         error_msg = 'File does not exist!'
#         client_socket.send(error_msg.encode())

def send_file(file_name):
    if file_exists(file_name):
        file_size = os.path.getsize(ftp_dir + file_name)
        client_socket.send(str(file_size).encode())
        time.sleep(1)
        msg = client_socket.recv(max_packet_size)
        ack_msg = msg.decode()

        if( ack_msg == 'ack'):
            f = open(ftp_dir + file_name, "rb")
            file_data = f.read()
            data_part1 = file_data[:len(file_data)//2]
            data_part2 = file_data[len(file_data)//2:]

            # Sending the first half
            client_socket.send(data_part1)
            
            time.sleep(1)
            msg_first_half = 'Send the first half succefuly'
            client_socket.send(msg_first_half.encode())

            time.sleep(2)
            # Receive answer from the client
            msg_data = client_socket.recv(max_packet_size)
            msg_client = msg_data.decode()
            
            if(msg_client != 'Y'):
                return
            
            # Sending the second half
            client_socket.send(data_part2)

            f.close() 

    else:
        error_msg = 'File does not exist!'
        client_socket.send(error_msg.encode())

# Function to receive a file from the client
def receive_file(file_name):
    time.sleep(1)
    data = client_socket.recv(max_packet_size)
    file_size = float(data)
    msg = 'ack'
    client_socket.send(msg.encode())
    print('Start to upload.. ')
    with open(ftp_dir + file_name, 'wb') as f:
        packets_received = 0
        while packets_received < file_size:
            packet_data = client_socket.recv(max_packet_size)
            f.write(packet_data)
            packets_received += len(packet_data)
    print('Finish download\tFile received successfully!')

# Download function - download a file from the server
def download():
        filelist = ListFolder(ftp_dir)
        filelist_bytes = bytes(str(filelist), encoding='utf-8')
        client_socket.send(filelist_bytes)
        print('Server wait for file name')
        request_packet = client_socket.recv(max_packet_size)
        file_name = request_packet.decode()
        print("The file name want to download: ", file_name)
        send_file(file_name)
        print('Done download')

# Upload function - upload a file to the server
def upload():
        print('Server wait for file name')
        request_packet = client_socket.recv(max_packet_size)
        file_name = request_packet.decode()
        time.sleep(1)
        receive_file(file_name)
        print('Done Upload')


# The main loop
while True:

    print('Server wait for client decesion')
    client_socket.settimeout(60)
    choice_packet = client_socket.recv(max_packet_size)
    action = choice_packet.decode()

    if(action == 'A'):
        download()
    elif (action == 'B'):
       upload()
    elif (action == 'C'):
        SendFileList()
    elif (action == 'D'):
        remove(ftp_dir)
    elif (action == 'E'):
        print('Close the program')
        break

server_socket.close()
client_socket.close()