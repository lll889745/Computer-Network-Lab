import requests
from urllib.parse import urlparse, urljoin
import time

TIMEOUT = 5  # 设置超时时间为5秒

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

headers = {
    'User-Agent': 'CustomCrawler/1.0 (compatible; Chrome/89.0.4389.82; Windows NT 10.0; Win64; x64)'
}

def allowed_to_crawl(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    robots_url = f"{parsed_url.scheme}://{host}/robots.txt"

    try:
        response = requests.get(robots_url, headers=headers, proxies=proxies, timeout=TIMEOUT)
        if response.status_code in (301, 302):
            robots_url = urljoin(robots_url, response.headers.get('Location'))
            response = requests.get(robots_url, headers=headers, proxies=proxies, timeout=TIMEOUT)

        robots_txt = response.text
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")
        return False

    user_agent_allowed = True
    for line in robots_txt.split("\n"):
        line = line.strip().lower()
        if line.startswith("user-agent:") and headers['User-Agent'].lower() in line:
            user_agent_allowed = True
        elif line.startswith("disallow:") and user_agent_allowed:
            disallowed_path = line.split("disallow:", 1)[1].strip()
            if urlparse(url).path.startswith(disallowed_path):
                return False

    return True

def crawl(url):
    if not allowed_to_crawl(url):
        print(f"Not allowed to crawl: {url}")
        return None

    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, proxies=proxies, timeout=TIMEOUT)
        response_time = time.time() - start_time
        response_code = response.status_code
        response_headers = response.headers
        response_method = response.request.method

        result = {
            'url': url,
            'response_time': response_time,
            'response_code': response_code,
            'response_headers': response_headers,
            'response_method': response_method
        }

        return result

    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return None

if __name__ == "__main__":
    with open("website.txt", "r") as file:
        with open("result.txt", "a", encoding="utf-8") as result_file:
            for line in file:
                url = line.strip()
                print(f"Crawling: {url}")
                result = crawl(url)
                if result:
                    result_file.write(f"URL: {url}\n")
                    result_file.write(f"Response Time: {result['response_time']:.2f} seconds\n")
                    result_file.write(f"Response Code: {result['response_code']}\n")
                    result_file.write(f"Response Method: {result['response_method']}\n")
                    result_file.write("Response Headers:\n")
                    for header, value in result['response_headers'].items():
                        result_file.write(f"{header}: {value}\n")
                    result_file.write("\n" + "=" * 80 + "\n\n")
                time.sleep(1)  # 暂停1秒，防止过于频繁的请求

