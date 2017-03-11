import re
from common import download



def link_crawler(seed_url, link_regex):
	crawl_queue = [seed_url]
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url).decode('utf-8')
		for link in get_links(html):
			if re.match(link_regex, link):
				crawl_queue.append(link)

def get_links(html):
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html)

if __name__ == '__main__':
	link_crawler('http://example.webscraping.com', '/(index|view)')