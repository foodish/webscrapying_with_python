from urllib.request import urlopen, Request, urlparse, build_opener, ProxyHandler
from urllib.error import HTTPError, URLError


def download1(url):
	return urlopen(url).read()

def download2(url):
	print('downloading:', url)
	try:
		html = urlopen(url).read()
	except (HTTPError, URLError) as e:
		print('downloading error:', e.reason)
		html = None
	return html

def download3(url, num_retries=5):
	print('downloading:', url)
	try:
		html = urlopen(url).read()
	except (HTTPError, URLError) as e:
		print('downloading error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				html = download3(url, num_retries-1)
	return html

def download4(url,user_agent='wswp', num_retries=5):
	print('downloading:', url)
	headers = {'User-agent': user_agent}
	request = Request(url, headers=headers)
	try:
		html = urlopen(request).read()
	except (HTTPError, URLError) as e:
		print('downloading error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				html = download4(url,user_agent, num_retries-1)
	return html

def download5(url,user_agent='wswp',proxy=None, num_retries=5):
	print('downloading:', url)
	headers = {'User-agent': user_agent}
	request = Request(url, headers=headers)
	opener = build_opener()
	if proxy:
		proxy_params = {urlparse(url).scheme: proxy}
	try:
		html = opener.open(request).read()
	except (HTTPError, URLError) as e:
		print('downloading error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				html = download5(url,user_agent,proxy, num_retries-1)
	return html

download = download5

if __name__ == '__main__':
	print(download('http://example.webscraping.com'))