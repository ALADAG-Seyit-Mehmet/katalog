import fitz
from PIL import Image
import numpy as np

# 1. Render PDF
doc = fitz.open("Sedirkon Logo.pdf")
page = doc[0]
mat = fitz.Matrix(6, 6) # high resolution
pix = page.get_pixmap(matrix=mat, alpha=False)
pix.save("temp_render.png")

# 2. Open and process with numpy
img = Image.open("temp_render.png").convert("RGBA")
data = np.array(img).astype(float)

height, width = data.shape[:2]

# Crop top logo (Top 30%, Center 60%)
crop = data[int(height*0.05):int(height*0.28), int(width*0.2):int(width*0.8)]

# We want to separate the gold mark from the black text.
# Gold is roughly R=160, G=130, B=50.
# Black is R=G=B < 100.
# White background is R=G=B=255.

# Let's compute distance from white
r, g, b, a = crop[:,:,0], crop[:,:,1], crop[:,:,2], crop[:,:,3]
gray = (r + g + b) / 3.0

# Mask for text: where the pixel is more black than gold
# Gold pixels have high red/green compared to blue.
# Text is neutral (r~g~b).
is_text = (np.abs(r - b) < 30) & (gray < 220)

new_crop = np.zeros_like(crop)
new_crop[:, :, 0] = 255 # initialize to white
new_crop[:, :, 1] = 255
new_crop[:, :, 2] = 255

# Calculate alpha: 255 - gray (so white background becomes 0 alpha)
# This perfectly captures anti-aliasing!
alpha = 255.0 - gray

# For text, we want it to be white on transparent
new_crop[is_text, 0] = 255
new_crop[is_text, 1] = 255
new_crop[is_text, 2] = 255
new_crop[is_text, 3] = alpha[is_text]

# For gold mark, we want original color, but with correct alpha so white bg is gone
is_gold = (~is_text) & (gray < 250)
# Gold is mixed with white bg, so original color * 255 / alpha (un-premultiply)
# But simple approximation: just use original color and alpha based on luminance drop from white
gold_alpha = np.clip((255.0 - gray) * 1.5, 0, 255) # boost alpha slightly so gold is opaque
new_crop[is_gold, 0] = r[is_gold]
new_crop[is_gold, 1] = g[is_gold]
new_crop[is_gold, 2] = b[is_gold]
new_crop[is_gold, 3] = gold_alpha[is_gold]

# For background, alpha is 0
is_bg = gray >= 250
new_crop[is_bg, 3] = 0

# Crop to tight bounding box of non-transparent pixels
final_alpha = new_crop[:, :, 3]
y_indices, x_indices = np.where(final_alpha > 10)
if len(y_indices) > 0:
    y_min, y_max = y_indices.min(), y_indices.max()
    x_min, x_max = x_indices.min(), x_indices.max()
    final_crop = new_crop[y_min:y_max+1, x_min:x_max+1]
else:
    final_crop = new_crop

# Save as WEBP
final_img = Image.fromarray(final_crop.astype(np.uint8), 'RGBA')
final_img.save("sedirkon_logo_header.webp", "webp", quality=100)
print("Saved sedirkon_logo_header.webp!")
