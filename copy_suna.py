import io

with io.open('katalog_dergi.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find Suna Köşe section wrapper
start_idx = text.find('<!-- ============================== SERIES 11: SUNA KÖŞE ============================== -->')
end_idx = text.find('<!-- Empty Page 1 -->')

if start_idx != -1 and end_idx != -1:
    suna_kose = text[start_idx:end_idx]
    
    # Do this for both dikey and baski
    files = ['katalog_dikey.html', 'katalog_baski.html']
    for file in files:
        with io.open(file, 'r', encoding='utf-8') as f:
            d_text = f.read()
        
        # Add to TOC if needed
        toc_add = '<div class="toc-item"><span class="toc-num">11</span><span class="toc-title">SUNA KÖŞE Serisi / Series</span></div>\n                    </div>'
        if 'SUNA KÖŞE' not in d_text:
            d_text = d_text.replace('</div>\n                    </div>\n                    <p class="intro-text">', toc_add + '\n                    <p class="intro-text">')
        
            res = d_text.replace('<!-- Empty Page 1 -->', suna_kose + '<!-- Empty Page 1 -->')
            with io.open(file, 'w', encoding='utf-8') as f:
                f.write(res)
            print(f'Added Suna Köşe to {file}')
        else:
            print(f'Already in {file}')
else:
    print('Suna Kose section not found in katalog_dergi.html')
