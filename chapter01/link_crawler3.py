import re
from urllib.parse import urljoin, urldefrag
from common import download
from urllib.request import Request, build_opener, urlparse, ProxyHandler
from urllib.error import HTTPError, URLError
from urllib import robotparser
import time
from datetime import datetime
from collections import deque
from queue import Queue


class Throttle():

	def __init__(self, delay):
		self.delay = delay
		self.domains = {}

	def wait(self,url):
		domain = urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.now()

def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1):
	crawl_queue = deque([seed_url])
	seen = {seed_url: 0}
	num_urls = 0
	rp = get_robots(seed_url)
	throttle = Throttle(delay)
	headers = headers or {}
	if user_agent:
		headers['User-agent'] = user_agent

	while crawl_queue:
		url = crawl_queue.pop()
		if rp.can_fetch(user_agent, url):
			throttle.wait(url)
			html = download(url, headers, proxy=proxy, num_retries=num_retries).decode('utf-8')
			links = []

			depth = seen[url]
			if depth != max_depth:
				if link_regex:
					links.extend(link for link in get_links(html) if re.match(link_regex, link))

				for link in links:
					link = normalize(seed_url, link)
					if link not in seen:
						seen[link] = depth + 1
						if same_domain(seed_url, link):
							crawl_queue.append(link)

			num_urls += 1
			if num_urls == max_urls:
				break
		else:
			print('Blocked by robots.txt:', url)

def get_links(html):
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html)

def download(url,headers,proxy=None, num_retries=5,data=None):
	print('downloading:', url)
	request = Request(url, data=data, headers=headers)
	opener = build_opener()
	if proxy:
		proxy_params = {urlparse(url).scheme: proxy}
		opener.add_handler(ProxyHandler(proxy_params))
	try:
		response = opener.open(request)
		html = response.read()
		code = response.code
	except (HTTPError, URLError) as e:
		print('downloading error:', e.reason)
		html = ''
		if hasattr(e, 'code'):
			code = e.code
			if num_retries > 0 and 500 <= e.code < 600:
				return download(url,headers,proxy, num_retries-1, data)
		else:
			code = None
	return html

def normalize(seed_url, link):
	link,_ = urldefrag(link)
	return urljoin(seed_url, link)

def same_domain(url1, url2):
	return urlparse(url1).netloc == urlparse(url2).netloc

def get_robots(url):
	rp = robotparser.RobotFileParser()
	rp.set_url(urljoin(url, '/robots.txt'))
	rp.read()
	return rp

if __name__ == '__main__':
	link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=5, user_agent='BadCrawler')
	link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=5,max_depth=-1, user_agent='GoodCrawler')