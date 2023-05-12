import socket
import ssl
import re
from urllib.parse import urlparse
from io import BytesIO


def http_get(url):
    url_parsed = urlparse(url)
    host, path = url_parsed.hostname, url_parsed.path
    is_https = url_parsed.scheme == 'https'

    if not path:
        path = '/'

    # 创建一个socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if is_https:
        # 使用ssl库包装socket
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=host)

    # 连接目标主机和端口
    s.connect((host, 443 if is_https else 80))

    # 构建一个HTTP GET请求
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    s.sendall(request.encode())

    response = b''
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data

    s.close()

    # 从响应头部获取字符编码
    content_type_pattern = re.compile(rb"Content-Type: .+?charset=(.+?)\r\n")
    charset_match = content_type_pattern.search(response)
    charset = 'utf-8'
    if charset_match:
        charset = charset_match.group(1).decode()

    # 使用找到的字符编码解码响应
    response_decoded = response.decode(charset, errors='ignore')

    return response_decoded


def main():
    with open('website.txt', 'r') as f:
        urls = f.read().splitlines()

    with open('result.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            try:
                response = http_get(url)
                f.write(f"URL: {url}\n")
                f.write(f"Response:\n{response}\n")
                f.write("=============================================================\n")
            except Exception as e:
                print(f"Error fetching {url}: {e}")


if __name__ == "__main__":
    main()
