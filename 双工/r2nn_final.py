import socket
import time
import threading
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
sent_packets = 0

def receive_data():
    global received_packets, sent_packets
    while True:
        # 接收数据
        data, addr = server_socket.recvfrom(1024)
        received_packet = json.loads(data.decode())
        received_packets += 1
        print("Received data:", received_packet)
        print("From:", addr)

        # 发送回复数据
        response_packet = {
            'id': sent_packets,
            'time_sent':received_packet['time'],
            'time_received': time.time(),
            'message': 'Received your message!'
        }
        server_socket.sendto(json.dumps(response_packet).encode(), addr)
        sent_packets += 1

# 创建并启动接收线程
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

# 这里我们让主线程等待接收线程，确保它完成后才关闭套接字
receive_thread.join()

# 关闭套接字
server_socket.close()
