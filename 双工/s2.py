import socket

# 目标 IP 和端口
target_ip = "192.168.1.100"
target_port = 12345

# 创建 UDP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送数据
while True:
    data = 'Hello World!'
    if not data:
        break
    client_socket.sendto(data.encode(), (target_ip, target_port))

    # 接收回复数据
    response_data, server_addr = client_socket.recvfrom(1024)
    print("接收到的回复数据：", response_data.decode())

# 关闭套接字
client_socket.close()