import os
import re

files = [
    "katalog_dergi_tr.html",
    "katalog_dergi_en.html",
    "katalog_dergi.html"
]

# Regex to match Empty Page 1 and Empty Page 2 and their divs
pattern = re.compile(r'\s*<!-- Empty Page 1 -->\s*<div class="page bleed">\s*<div class="page-content">\s*<div class="pattern-bg"></div>\s*</div>\s*</div>\s*<!-- Empty Page 2 -->\s*<div class="page bleed">\s*<div class="page-content">\s*<div class="pattern-bg"></div>\s*</div>\s*</div>', re.DOTALL)

for filename in files:
    filepath = os.path.join(r"c:\Users\seyit\Desktop\katalog", filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = pattern.sub('', content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {filename}")
