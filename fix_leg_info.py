import glob
import re

html_files = glob.glob('katalog_*.html')

for file in html_files:
    if file == 'katalog_baski.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # We want to add missing </div> to the end of <p> tags inside <div class="leg-info">
    # Pattern: <div class="leg-info"><h4>...</h4><p>...</p>
    # If it is followed immediately by \n\s*</div>, we can add the </div> to the end of the line.
    # Actually, let's just make it simple:
    # Replace `<p>Doğal sıcaklı endüstriyel esintilerle buluşturan ikonik tasarım.</p>\n`
    # With    `<p>Doğal sıcaklı endüstriyel esintilerle buluşturan ikonik tasarım.</p></div>\n`
    
    # Let's find any <div class="leg-info">...<p>...</p>\n
    # and replace it with <div class="leg-info">...<p>...</p></div>\n
    # Only if it currently lacks </div> at the end of the line.
    
    def fix_leg_info(match):
        line = match.group(1)
        if not line.endswith('</div>'):
            return line + '</div>\n'
        return match.group(0)
    
    content = re.sub(r'(<div class="leg-info"><h4>.*?</h4><p>.*?</p>)\s*\n', r'\1</div>\n', content)

    # Let's also check if we have enough closing divs for page-content and page.
    # Actually, earlier I added missing tags before OUTRO. But what about the intermediate pages?
    # Each page should end with:
    #             </div>
    #         </div>
    #         </div>
    # (closing leg-grid, page-content, page)
    # If the leg-info was eating one </div>, then leg-grid closed, but page-content and page didn't.
    # Let's just fix the leg-info missing </div> first.
    # Wait, if I add </div> to leg-info, then the 3 </div>s will close leg-item, leg-grid, and page-content!
    # Still missing 1 </div> for page!
    
    # The structure should be:
    # <div class="page">
    #   <div class="page-content ...">
    #     <div class="leg-grid">
    #       <div class="leg-item"> ... </div>
    #       <div class="leg-item"> ... </div>
    #     </div>
    #   </div>
    # </div>
    
    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed missing leg-info tags in {file}")
    else:
        print(f"No match found in {file}")
