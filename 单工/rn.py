import socket
import time
import json

# 创建 UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 监听的 IP 和端口
listen_ip = "0.0.0.0"
listen_port = 12345

# 绑定 IP 和端口
server_socket.bind((listen_ip, listen_port))

# 用于记录接收和发送的数据包的数量
received_packets = 0

while True:
    # 接收数据
    data, addr = server_socket.recvfrom(1024)
    received_packet = json.loads(data.decode())
    received_packets += 1
    transmit_time = time.time() - received_packet['time']
    packet_loss = (received_packet['id'] + 1 - received_packets) / (received_packet['id'] + 1)
    bandwidth = len(data) / transmit_time
    print("Received data:", received_packet)
    print("From:", addr)
    print("Packet loss: ", packet_loss)
    print("Bandwidth: ", bandwidth, "bytes/s")
