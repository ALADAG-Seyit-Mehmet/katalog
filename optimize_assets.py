import os
from PIL import Image
import re

directories = ['.', 'resim', 'yeni_resim']
html_css_files = [f for f in os.listdir('.') if f.endswith(('.html', '.css'))]

# 1. Convert all images to WebP
converted_files = {} # old_name -> new_name
total_saved_bytes = 0

print("Starting image conversion...")
for d in directories:
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            old_path = os.path.join(d, f)
            name, ext = os.path.splitext(f)
            new_f = name + '.webp'
            new_path = os.path.join(d, new_f)
            
            # Skip if already converted
            if os.path.exists(new_path):
                # But still add to mapping so HTML is updated
                converted_files[f] = new_f
                continue
            
            try:
                img = Image.open(old_path)
                
                # Convert RGBA to RGB if saving as webp and image is JPEG originally
                # Actually WebP supports alpha, so RGBA is fine for WebP.
                img.save(new_path, 'webp', quality=80)
                
                old_size = os.path.getsize(old_path)
                new_size = os.path.getsize(new_path)
                total_saved_bytes += (old_size - new_size)
                
                converted_files[f] = new_f
                print(f"Converted {f} -> {new_f} (Saved {(old_size - new_size)/1024:.1f} KB)")
                
                # Optionally delete original
                os.remove(old_path)
            except Exception as e:
                print(f"Failed to convert {f}: {e}")

print(f"\nTotal space saved: {total_saved_bytes/1024/1024:.2f} MB")

# 2. Update HTML and CSS files
print("\nUpdating HTML and CSS files...")
for file in html_css_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace filenames in content
    for old_name, new_name in converted_files.items():
        # Using simple replace. It's safe since these are specific filenames.
        content = content.replace(old_name, new_name)
    
    # 3. Add loading="lazy" decoding="async" to <img> tags (HTML only)
    if file.endswith('.html'):
        # Find all <img> tags
        img_pattern = r'(<img\s+[^>]+>)'
        
        def add_lazy_loading(match):
            img_tag = match.group(1)
            # Add loading="lazy" if not present
            if 'loading=' not in img_tag:
                img_tag = img_tag.replace('<img ', '<img loading="lazy" decoding="async" ')
            return img_tag
            
        content = re.sub(img_pattern, add_lazy_loading, content)
        
    if content != original_content:
        with open(file, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print(f"Updated {file}")

print("\nOptimization complete!")
