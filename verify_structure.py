from bs4 import BeautifulSoup

with open('katalog_musteri.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
layout = soup.select_one('.vertical-customer-layout')

if layout:
    children = [c for c in layout.children if hasattr(c, 'get')]
    print('Layout children count:', len(children))
    for i, c in enumerate(children[:6]):
        pages_in_row = c.select('.page')
        cls = c.get('class')
        print('  Row', i, 'class:', cls, 'pages:', len(pages_in_row))
    if len(children) > 6:
        print('  ...')
        for i, c in enumerate(children[-2:]):
            pages_in_row = c.select('.page')
            cls = c.get('class')
            print('  Row', len(children)-2+i, 'class:', cls, 'pages:', len(pages_in_row))
else:
    print('Layout NOT FOUND!')

# Also check total pages in musteri
all_pages = soup.select('.page')
print()
print('Total pages in musteri:', len(all_pages))

# Check baski too
with open('katalog_baski.html', 'r', encoding='utf-8') as f:
    html2 = f.read()
soup2 = BeautifulSoup(html2, 'html.parser')
layout2 = soup2.select_one('.vertical-print-layout')
if layout2:
    pages2 = layout2.select('.page')
    print('Total pages in baski:', len(pages2))
else:
    print('Baski layout NOT FOUND!')
