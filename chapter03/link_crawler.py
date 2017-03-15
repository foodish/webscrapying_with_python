import re
from downloader import Downloader
from urllib.parse import urldefrag, urljoin
from urllib.request import urlparse
from urllib import robotparser


def link_crawler(seed_url, link_regex=None, delay=1, max_depth=-1,max_urls=-1, user_agent='wswp', proxies=None,
                 num_retries=1, scrap_callback=None, cache=None):
    crawl_queue = [seed_url]
    seen = {seed_url: 0}
    num_urls = 0
    rp = get_robots(seed_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        if rp.can_fetch(user_agent, url):
            html = D(url)
            links = []
            if scrap_callback:
                links.extend(scrap_callback(url, html) or [])

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


def normalize(seed_url, link):
    link, _ = urldefrag(link)
    return urljoin(seed_url, link)


def same_domain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc


def get_robots(url):
    rp = robotparser.RobotFileParser()
    rp.set_url(urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html.decode('utf-8'))


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1,
                 user_agent='GoodCrawler')


