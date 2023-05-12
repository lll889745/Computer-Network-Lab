import socket
import time
import threading
import json

# dy, mxz, zsy 的 IP 和端口
devices = {
    'dy': {
        'ip': '172.20.10.3',
        'port': 12345
    },
    'mxz': {
        'ip': '172.20.10.7',
        'port': 12345
    },
    'zsy': {
        'ip': '172.20.10.10',
        'port': 12345
    }
}

# 创建 UDP Socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定本机 IP 和端口
listen_ip = devices['mxz']['ip']
listen_port = devices['mxz']['port']
socket.bind((listen_ip, listen_port))

# 要发送的数据
message = 'Hello zsy! I am mxz.'

# 用于记录发送和接收的数据包的数量
sent_packets = 0
received_packets = 0

# 当前设备名称
device_name = 'mxz'

def send_data():
    global sent_packets
    while True:
        # 为每个数据包分配一个唯一的序列号
        packet = {
            'id': sent_packets,
            'time_sent': time.time(),
            'message': message,
            'from': device_name
        }
        # 发送数据
        socket.sendto(json.dumps(packet).encode(), (devices['zsy']['ip'], devices['zsy']['port']))
        sent_packets += 1
        print("Sent data:", packet)
        time.sleep(1)

def receive_data():
    global received_packets
    while True:
        response_data, server_addr = socket.recvfrom(1024)
        received_packet = json.loads(response_data.decode())
        if received_packet['from'] == 'zsy':
            # 接收回复数据
            received_packets += 1
            print("Received reply: ", received_packet)

            # 计算传输时间
            roundtrip_time = time.time() - received_packet['time_sent']
            print("Round-trip time: ", roundtrip_time, "seconds")
        
            # 计算带宽，单位是 bytes/s
            transmit_time = time.time() - received_packet['time_received']
            bandwidth = len(response_data) / transmit_time
            print("Bandwidth: ", bandwidth, "bytes/s")

            # 计算丢包率
            packet_loss = (sent_packets - received_packets) / sent_packets
            print("Packet loss: ", packet_loss)
        # 如果接收到的数据包来自 dy，则回复
        elif received_packet['from'] == 'dy':
            reply_packet = {
                'id': sent_packets,
                'time_received': time.time(),
                'time_sent': received_packet['time_sent'],
                'message': 'mxz receive from dy',
                'from': device_name,
            }
            socket.sendto(json.dumps(reply_packet).encode(), (devices['dy']['ip'], devices['dy']['port']))
            #print("回复数据：", reply_packet)
        else:
            print("Illegal sender!")

# 创建并启动发送和接收线程
send_thread = threading.Thread(target=send_data)
receive_thread = threading.Thread(target=receive_data)

send_thread.start()
receive_thread.start()

# 这里我们让主线程等待发送和接收线程，确保它们都完成后才关闭套接字
send_thread.join()
receive_thread.join()

# 关闭 Socket
socket.close()
