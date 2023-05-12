import socket
import time
import json

# 发送数据的 IP 和端口
send_ip = "172.20.10.7"
send_port = 12345

# 创建 UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 要发送的数据
message = "hello world"

# 用于记录发送数据包的数量
sent_packets = 0

# 发送数据
while True:
    # 为每个数据包分配一个唯一的序列号
    packet = {
        'id': sent_packets,
        'time': time.time(),
        'message': message
    }
    # 发送数据
    client_socket.sendto(json.dumps(packet).encode(), (send_ip, send_port))
    sent_packets += 1
    print("Sent data:", packet)
    time.sleep(1)
