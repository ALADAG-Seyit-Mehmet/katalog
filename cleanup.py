import io
with io.open('katalog_dergi.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'(<p class="subtitle-en">PREMIUM FURNITURE COLLECTION</p>\s*)+', '<p class="subtitle-en">PREMIUM FURNITURE COLLECTION</p>\n                        ', text)
text = re.sub(r'(<div class="cover-bottom-en">Inspired by Nature\. Designed for Mankind\.</div>\s*)+', '<div class="cover-bottom-en">Inspired by Nature. Designed for Mankind.</div>\n                            ', text)
text = re.sub(r'(<span style="font-size: 0\.7em; color: #888; margin-top: 2px;">Scan for Location</span>\s*)+', '<span style="font-size: 0.7em; color: #888; margin-top: 2px;">Scan for Location</span>\n                                ', text)

with io.open('katalog_dergi.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done cleanup")
