import socket
import time

# 发送数据的 IP 和端口
send_ip = "192.168.0.100"
send_port = 12345

# 创建 UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 要发送的数据
message = "hello world"

# 发送数据
while True:
    client_socket.sendto(message.encode(), (send_ip, send_port))
    print("Sent data:", message)
    time.sleep(1)

# 关闭 Socket
client_socket.close()
