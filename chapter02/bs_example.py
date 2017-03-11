from common import download
from bs4 import BeautifulSoup


url = 'http://example.webscraping.com/view/United-Kingdom-239'
html = download(url).decode('utf-8')
soup = BeautifulSoup(html,'lxml')
tr = soup.find(attrs={'id': 'places_area__row'})  # locate the area row
# 'class' is a special python attribute so instead 'class_' is used
td = tr.find(attrs={'class': 'w2p_fw'})  # locate the area tag
area = td.text  # extract the area contents from this tag

print(area)
