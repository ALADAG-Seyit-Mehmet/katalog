import re

with open('katalog_dikey_tr.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(len(re.findall(r'<div class="page">', content)))
print(len(re.findall(r'<div class="page page-spread-left">', content)))
print(len(re.findall(r'<div class="page page-spread-right">', content)))
print(len(re.findall(r'<div class="page page-cover">', content)))
