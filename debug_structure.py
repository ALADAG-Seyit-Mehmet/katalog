from bs4 import BeautifulSoup

with open('katalog_dergi_tr.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')

# Check catalog-wrapper children
cw = soup.select_one('.catalog-wrapper')
print('=== catalog-wrapper direct children ===')
for i, child in enumerate(cw.children):
    if hasattr(child, 'get'):
        cls = child.get('class')
        cid = child.get('id')
        print('  child:', child.name, 'class:', cls, 'id:', cid)
    if i > 15:
        print('  ...')
        break

print()
# Check first .page parent chain
first_page = soup.select_one('.page')
print('=== First .page parent chain ===')
el = first_page
for _ in range(5):
    el = el.parent
    if el:
        cls = el.get('class') if hasattr(el, 'get') else None
        cid = el.get('id') if hasattr(el, 'get') else None
        print('  parent:', el.name, 'class:', cls, 'id:', cid)

print()
# All pages
all_pages = soup.select('.page')
print('Total pages:', len(all_pages))
for i, p in enumerate(all_pages[:5]):
    print('  page', i, 'class:', p.get('class'), 'style:', p.get('style', '')[:80])
