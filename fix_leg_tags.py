import glob
import re

html_files = glob.glob('katalog_*.html')

for file in html_files:
    if file == 'katalog_baski.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Let's check if the file has unclosed leg-options-page before OUTRO
    # If there's a leg-grid div before OUTRO, it might be missing closing tags for page-content and page
    if "leg-grid" in content:
        # Check if OUTRO is preceded by just </div>
        # Actually, let's just make sure there are enough closing divs.
        # We can look for the specific block in katalog_dergi.html:
        """
                <div class="leg-item tall-model">
                    <div class="leg-img-wrapper"><img loading="lazy" decoding="async" src="yeni_resim/ayak8.webp" alt="Model 08 - Sedir Kol Arkası"></div>
                    <div class="leg-info"><h4>Model 08 (Kol Arkası)</h4><p>Sedir iskeletine estetik ve ergonomik bir dokunuş katan özel kol arkası tasarımı.</p></div>
                </div>
            </div>
        <!-- ============================== OUTRO ============================== -->
        """
        pattern = r'(<div class="leg-info"><h4>Model 08 \(Kol Arkası\)</h4><p>Sedir iskeletine estetik ve ergonomik bir dokunuş katan özel kol arkası tasarımı\.</p></div>\s*</div>\s*</div>)(\s*<!-- ============================== OUTRO ============================== -->)'
        
        # Add </div>\n        </div>
        content = re.sub(pattern, r'\1\n        </div>\n        </div>\2', content)

    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed missing tags in {file}")
    else:
        print(f"No match found in {file}")
