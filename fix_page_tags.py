import glob
import re

html_files = glob.glob('katalog_*.html')

for file in html_files:
    if file == 'katalog_baski.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Model 04 block ending:
    # </div>\s*</div>\s*</div>\s*<div class="page">\s*<div class="page-content leg-options-page">\s*<div class="leg-options-header" style="opacity: 0; pointer-events: none; user-select: none;">\s*<h2>Ayak Seçenekleri</h2>
    # We want to add one more </div> before <div class="page">
    
    # Instead of specific strings, let's just find:
    #             </div>
    #         </div>
    #         </div>
    #         <div class="page">
    #             <div class="page-content leg-options-page">
    # And replace with 4 </div>s.
    
    pattern = r'(</div>\s*</div>\s*</div>)(\s*<div class="page">\s*<div class="page-content leg-options-page">)'
    content = re.sub(pattern, r'\1\n        </div>\2', content)

    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed missing page closing tags in {file}")
    else:
        print(f"No match found in {file}")
