import itertools
from common import download


def iteration():
	for page in itertools.count(1):
		# url = 'http://example.webscraping.com/view/-%d' % page
		url = 'http://example.webscraping.com/view/-{}'.format(page)
		html = download(url)
		if html is None:
				break
		else:
			pass

if __name__ == '__main__':
	iteration()



