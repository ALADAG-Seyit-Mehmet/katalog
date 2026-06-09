import os
import re

files = [
    "katalog_dergi_tr.html",
    "katalog_dergi_en.html",
    "katalog_dergi.html"
]

pattern = re.compile(r'(\s*<!-- ============================== LEG OPTIONS ============================== -->.*?(?=<!-- ============================== OUTRO ============================== -->))', re.DOTALL)

for filename in files:
    filepath = os.path.join(r"c:\Users\seyit\Desktop\katalog", filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = pattern.sub(r'\n        ', content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {filename}")
