import os
import re

files_to_fix = ['katalog_dikey.html', 'katalog_baski.html']

for file in files_to_fix:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the entire LEG OPTIONS block
    # It starts with <!-- ============================== LEG OPTIONS ============================== -->
    # and ends right before the NEXT <!-- ============================== OUTRO ============================== -->
    # We want to remove the SECOND occurrence of this block, including the OUTRO comment if there's a duplicate.
    
    # Actually, the simplest way is to find all LEG OPTIONS blocks.
    # The block is exactly the same both times.
    
    pattern = r'<!-- ============================== LEG OPTIONS ============================== -->.*?<!-- ============================== OUTRO ============================== -->\n*'
    
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if len(matches) > 1:
        # Keep the FIRST match, remove all subsequent matches by replacing them with just the OUTRO comment
        # Because my original script replaced OUTRO with LEG OPTIONS + OUTRO.
        # So to undo it, we replace LEG OPTIONS + OUTRO with just OUTRO.
        
        # Start from the end so we don't mess up indices
        for match in reversed(matches[1:]):
            content = content[:match.start()] + '<!-- ============================== OUTRO ============================== -->\n' + content[match.end():]
            
        with open(file, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print(f"Fixed {file}")
