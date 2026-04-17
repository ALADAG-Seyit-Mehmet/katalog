import sys
files = ['katalog_dergi.html', 'katalog_dikey.html', 'katalog_baski.html']
for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    c = text.count('<div class="page"') + text.count('<div class="page ')
    print(f"{fn} pages: {c}")
