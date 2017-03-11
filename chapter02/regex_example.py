import re
from urllib.request import Request
from common import download
from pprint import pprint


url = 'http://example.webscraping.com/view/United-Kingdom-239'
html = download(url).decode('utf-8')
# area = re.findall('<td class="w2p_fw">(.*?)</td>', html)
area = re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html)

# pprint(area)
pprint(area[0])