import itertools
from common import download

def iteration():
	max_errors = 5
	num_errors = 0
	for page in itertools.count(1):
		# url = 'http://example.webscraping.com/view/-%d' % page
		url = 'http://example.webscraping.com/view/-{}'.format(page)
		html = download(url)
		if html is None:
			num_errors += 1
			if num_errors == max_errors:
				break
		else:
			num_errors = 0

if __name__ == '__main__':
	iteration()