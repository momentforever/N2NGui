import socket

# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
# 目标主机和端口
target_host = 'localhost'
target_port = 5645

# 要发送的数据
data = b'\n'

# 发送数据包
sock.sendto(data, (target_host, target_port))

# 循环接收数据
num_packets = 5  # 要接收的数据包数量
for _ in range(num_packets):
    data, addr = sock.recvfrom(1024)
    print("Received data:", data.decode())
    print("Sender address:", addr)


# 关闭套接字
sock.close()