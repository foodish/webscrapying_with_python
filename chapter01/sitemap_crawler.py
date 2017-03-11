import re
from common import download


def crawl_sitemap(url):
	sitemap = download(url).decode('utf-8')
	links = re.findall('<loc>(.*?)</loc>', sitemap)
	for link in links:
		html = download(link)

if __name__ == '__main__':
	crawl_sitemap('http://example.webscraping.com/sitemap.xml')