from common import download
from lxml import html


url = 'http://example.webscraping.com/view/United-Kingdom-239'
html = download(url).decode('utf-8')
tree = html.fromstring(html)
td = tree.cssselect('tr#places_neighbours__row > td.w2p_fw')[0]
area = td.text_content()

print(area)