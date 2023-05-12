# 双工接收端
import socket

# 创建 UDP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 监听的 IP 和端口
#listen_ip = "172.20.10.3"
listen_ip = "0.0.0.0"
listen_port = 12345

# 绑定 IP 和端口
server_socket.bind((listen_ip, listen_port))

# 接收数据
data, addr = server_socket.recvfrom(1024)
received_data, addr = data, addr

print("Received data:", received_data.decode())
print("From:", addr)
    
# 发送回复数据
response_data = 'Received your message!'
server_socket.sendto(response_data.encode(), addr)

# 关闭套接字
server_socket.close()