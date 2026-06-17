import re

with open('logo_full.svg', 'r', encoding='utf-8') as f:
    svg_content = f.read()

# We need to replace the fill="#ffffff" with fill="#282c2e" (black)
# But wait, we should also find the MOBİLYA text and make it grey "#878b8c" if possible.
# Since it's hard to know which paths are MOBİLYA, making everything black "#282c2e" is the best approach.
# Or, if we see the second half of the paths, maybe we can just extract them.

# Actually, the user's uploaded image has #282c2e for SEDİRKON and #878b8c for MOBİLYA.
# Let's just replace ALL #ffffff with #282c2e for now to give them the dark text.
svg_black = svg_content.replace('#ffffff', '#282c2e')
# But wait, there are paths that use #ffffff. Let's just change them to #282c2e.

with open('logo_black.svg', 'w', encoding='utf-8') as f:
    f.write(svg_black)

print("Created logo_black.svg")
