import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    has_suna_kose = 'Suna Köşe' in content or 'SUNA KÖŞE' in content
    legs = len(re.findall(r'<div class="leg-item">', content))
    leg_pages = len(re.findall(r'<div class="page-content leg-options-page">', content))
    
    print(f'{f}: Suna Kose={has_suna_kose}, Legs={legs}, Leg Pages={leg_pages}')
