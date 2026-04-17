import io

with io.open('katalog_dergi.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make bilingual labels
content = content.replace('Kumaş:', 'Kumaş / Fabric:')
content = content.replace('Konsept:', 'Konsept / Concept:')
content = content.replace('<span class="spec-label">Kanepe</span>', '<span class="spec-label">Kanepe / Sofa</span>')
content = content.replace('<span class="spec-label">Berjer</span>', '<span class="spec-label">Berjer / Armchair</span>')
content = content.replace('G: ', 'G/W: ')
content = content.replace('D: ', 'D/D: ')
content = content.replace('Y: ', 'Y/H: ')
content = content.replace('<strong>İletişim</strong>', '<strong>İletişim / Contact</strong>')

# Cover and other text 
content = content.replace('<p class="subtitle">PREMİUM MOBİLYA KOLEKSİYONU</p>', '<p class="subtitle">PREMİUM MOBİLYA KOLEKSİYONU</p>\n                        <p class="subtitle-en">PREMIUM FURNITURE COLLECTION</p>')
content = content.replace('<div class="cover-bottom">\n                            Doğadan İlham Aldı. İnsan İçin Tasarlandı.', '<div class="cover-bottom">\n                            Doğadan İlham Aldı. İnsan İçin Tasarlandı.\n                            <div class="cover-bottom-en">Inspired by Nature. Designed for Mankind.</div>')
content = content.replace('<span class="qr-label">Konum İçin Okutun</span>', '<span class="qr-label">Konum İçin Okutun</span>\n                                <span style="font-size: 0.7em; color: #888; margin-top: 2px;">Scan for Location</span>')

# Fix translations specific to split_lang concepts
content = content.replace('Soft Kadife', 'Soft Kadife / Soft Velvet')
content = content.replace('Şehirli Modern', 'Şehirli Modern / Urban Modern')
content = content.replace('Organik Lüks', 'Organik Lüks / Organic Luxury')
content = content.replace('İPEK', 'İPEK / SILK')

# Serisi / Series replacements
for i in range(1, 11):
    content = content.replace(f'SERİ 0{i}', f'SERİ / SERIES 0{i}')
content = content.replace('SERİ 10', 'SERİ / SERIES 10')
content = content.replace('SERİ 11', 'SERİ / SERIES 11') # Just in case

content = content.replace('Serisi</span>', 'Serisi / Series</span>')

with io.open('katalog_dergi.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
