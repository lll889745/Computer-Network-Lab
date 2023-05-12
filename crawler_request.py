import requests
from urllib.parse import urlparse, urljoin
import time

proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

headers = {
    'User-Agent': 'CustomCrawler/1.0 (compatible; Chrome/89.0.4389.82; Windows NT 10.0; Win64; x64)'
}

def fetch(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5, allow_redirects=True)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def allowed_to_crawl(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    robots_url = f"http://{host}/robots.txt"
    
    try:
        response = fetch(robots_url)
        if response is None:
            return False

        robots_txt = response.text
        user_agent = headers['User-Agent']
        user_agent_allowed = True

        for line in robots_txt.split("\n"):
            line = line.strip().lower()
            if line.startswith("user-agent:") and user_agent.lower() in line:
                user_agent_allowed = True
            elif line.startswith("disallow:") and user_agent_allowed:
                disallowed_path = line.split("disallow:", 1)[1].strip()
                if parsed_url.path.startswith(disallowed_path):
                    return False

        return True
    except Exception as e:
        print(f"Error checking robots.txt for {url}: {e}")
        return False

def crawl(url):
    if not allowed_to_crawl(url):
        print(f"Not allowed to crawl: {url}")
        return ""

    try:
        response = fetch(url)
        if response is None:
            print(f"Error: Empty response")
            return ""

        content = response.text
        print(content)
        return content
    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
    with open("website.txt", "r") as file:
        for line in file:
            url = line.strip()
            print(f"Crawling: {url}")
            result = crawl(url)
            if result:
                with open("result.txt", "a", encoding="utf-8") as result_file:
                    result_file.write(f"URL: {url}\n")
                    result_file.write(result)
                    result_file.write("\n" + "=" * 80 + "\n\n")
            time.sleep(1)  # 暂停1秒，防止过于频繁的请求

