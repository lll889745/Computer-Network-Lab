import socket
import time
import threading
import json

# 发送数据的 IP 和端口
send_ip = "172.20.10.7"
send_port = 12345

# 创建 UDP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 要发送的数据
message = "hello world"

# 用于记录发送和接收的数据包的数量
sent_packets = 0
received_packets = 0

def send_data():
    global sent_packets
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

def receive_data():
    global received_packets
    while True:
        # 接收回复数据
        response_data, server_addr = client_socket.recvfrom(1024)
        received_packet = json.loads(response_data.decode())
        received_packets += 1
        print("接收到的回复数据：", received_packet)

        # 计算传输时间
        roundtrip_time = time.time() - received_packet['time_sent']
        print("Round-trip time: ", roundtrip_time, "seconds")
        
        # 计算带宽，单位是 bytes/s
        transmit_time = time.time() + 1 - received_packet['time_received']
        bandwidth = len(response_data) / transmit_time
        print("Bandwidth: ", bandwidth, "bytes/s")

        # 计算丢包率
        packet_loss = (sent_packets - received_packets) / sent_packets
        print("Packet loss: ", packet_loss)

# 创建并启动发送和接收线程
send_thread = threading.Thread(target=send_data)
receive_thread = threading.Thread(target=receive_data)

send_thread.start()
receive_thread.start()

# 这里我们让主线程等待发送和接收线程，确保它们都完成后才关闭套接字
send_thread.join()
receive_thread.join()

# 关闭 Socket
client_socket.close()
