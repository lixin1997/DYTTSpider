import requests

"""
针对免费动态IP代理的测试
"""
proxy = {
    'http': '106.75.164.15:3128'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
}

ip = requests.get('http://httpbin.org/ip', headers=headers, proxies=proxy)
print(ip.text)
