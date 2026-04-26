import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html') and 'index' not in f]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix 1: Ensure all three closing divs are properly placed at the end of the leg-options-page
    # Wait, my previous fix replaced the end of the first leg options block and the start of the second
    # First, let's remove any invisible headers we added before
    content = re.sub(r'<div class="leg-options-header" style="visibility: hidden;">.*?</div>\s*<div class="leg-grid">', '<div class="leg-grid">', content, flags=re.DOTALL)

    # Next, we must ensure there are exactly three </div> before the second page
    # The pattern is from the end of Model 04 to the start of the next <div class="page">
    pattern_split = r'(<div class="leg-info"><h4>(?:Model|Model) 04</h4>.*?</div>\s*</div>\s*</div>\s*)(</div>\s*)*(<div class="page">)'
    
    def replacer(match):
        # Always insert exactly 3 </div>
        return match.group(1) + '</div>\n        </div>\n        <div class="page">\n'

    content = re.sub(pattern_split, replacer, content, flags=re.DOTALL)

    if content != original_content:
        with open(file, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print(f"Applied structure fixes to {file}")
