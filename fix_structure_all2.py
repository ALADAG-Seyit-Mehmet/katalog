import os
import re
import io

suna_kose_en = """        <!-- ============================== SERIES 11: SUNA KÖŞE ============================== -->
        <div class="page bleed page-spread-left">
            <div class="page-content" style="background-image: url('yeni_resim/sunaköşe1.webp');"></div>
        </div>
        <div class="page bleed page-spread-right">
            <div class="page-content" style="background-image: url('yeni_resim/sunaköşe1.webp');">
                <div class="hero-text-overlay bottom-right">
                    <h3>Suna Corner</h3>
                </div>
            </div>
        </div>
        <div class="page">
            <div class="page-content">
                <div class="content-inner info-layout">
                    <span class="series-badge">SERIES 11</span>
                    <h2 class="series-title">Suna Corner</h2>
                    <p class="series-desc">A corner set comfort that makes you feel like on clouds with its organic curves and extra wide seating area. An elegant sanctuary for large families with the soft texture of Troya fabric.</p>
                    <ul class="series-specs">
                        <li><span>Fabric:</span> TROYA</li>
                        <li><span>Concept:</span> Organic Luxury</li>
                    </ul>
                    <div class="technical-specs">
                        <div class="spec-row"><span class="spec-label">Corner</span><span class="spec-value">W: 320x320 | D: 110 | H: 83 cm</span></div>
                        <div class="spec-row"><span class="spec-label">Armchair</span><span class="spec-value">W: 79 | D: 92 | H: 83 cm</span></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="page bleed">
            <div class="page-content">
                <div class="multi-image-layout">
                    <figure><img loading="lazy" decoding="async" src="yeni_resim/sunaköşe2.webp" alt="Suna Corner Detail"></figure>
                    <figure><img loading="lazy" decoding="async" src="yeni_resim/sunaköşe3.webp" alt="Suna Corner Armchair"></figure>
                </div>
            </div>
        </div>
"""

with io.open('katalog_dikey_tr.html', 'r', encoding='utf-8') as f:
    text_tr = f.read()

start_idx_tr = text_tr.find('<!-- ============================== SERIES 11: SUNA KÖŞE ============================== -->')
end_idx_tr = text_tr.find('<!-- ============================== LEG OPTIONS ============================== -->')
suna_kose_tr = text_tr[start_idx_tr:end_idx_tr]

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

for f in html_files:
    with io.open(f, 'r', encoding='utf-8') as file:
        content = file.read()

    is_en = '_en' in f
    
    # 1. ADD TO TOC IF MISSING
    if 'Suna Köşe' not in content and 'SUNA KÖŞE' not in content and 'Suna Corner' not in content:
        toc_add = '<div class="toc-item"><span class="toc-num">11</span><span class="toc-title">Suna Corner</span></div>' if is_en else '<div class="toc-item"><span class="toc-num">11</span><span class="toc-title">Suna Köşe Serisi</span></div>'
        if '10</span>' in content:
            # Find the end of Series 10 TOC item
            s10_idx = content.find('<span class="toc-num">10</span>')
            s10_end = content.find('</div>', s10_idx) + 6
            content = content[:s10_end] + '\n                            ' + toc_add + content[s10_end:]
        
    # 2. INJECT SUNA KÖŞE CONTENT IF MISSING
    if 'SERIES 11: SUNA KÖŞE' not in content:
        insert_text = suna_kose_en if is_en else suna_kose_tr
        legs_idx = content.find('<!-- ============================== LEG OPTIONS ============================== -->')
        if legs_idx != -1:
            content = content[:legs_idx] + insert_text + '        ' + content[legs_idx:]

    # 3. FIX LEGS LAYOUT
    # We want to replace the second leg options page with one that has a hidden header
    # We'll use regex to match the start of the second page.
    # Second page starts after the first `</div>\n        </div>\n        <div class="page">\n            <div class="page-content leg-options-page">\n            <div class="leg-grid">`
    # Let's rebuild the Leg Options section completely to be perfectly 4 per page and identically formatted.
    
    start_legs = content.find('<!-- ============================== LEG OPTIONS ============================== -->')
    end_legs = content.find('<!-- ============================== OUTRO ============================== -->')
    
    if start_legs != -1 and end_legs != -1:
        legs_content = content[start_legs:end_legs]
        # Extract all leg items
        leg_items = re.findall(r'(<div class="leg-item">.*?</div>\s*</div>)', legs_content, re.DOTALL)
        
        if len(leg_items) == 8:
            header_title = "Leg Options" if is_en else "Ayak Seçenekleri"
            header_desc = "Exclusive leg alternatives designed to personalize our collection." if is_en else "Koleksiyonumuzu kişiselleştirmeniz için tasarlanmış özel ayak alternatifleri."
            
            new_legs_content = f"""<!-- ============================== LEG OPTIONS ============================== -->
        <div class="page">
            <div class="page-content leg-options-page">
            <div class="leg-options-header">
                <h2>{header_title}</h2>
                <p>{header_desc}</p>
            </div>
            <div class="leg-grid">
                {leg_items[0]}
                {leg_items[1]}
                {leg_items[2]}
                {leg_items[3]}
            </div>
        </div>
        </div>
        <div class="page">
            <div class="page-content leg-options-page">
            <div class="leg-options-header" style="opacity: 0; pointer-events: none; user-select: none;">
                <h2>{header_title}</h2>
                <p>{header_desc}</p>
            </div>
            <div class="leg-grid">
                {leg_items[4]}
                {leg_items[5]}
                {leg_items[6]}
                {leg_items[7]}
            </div>
        </div>
        </div>

        """
            content = content[:start_legs] + new_legs_content + content[end_legs:]

    with io.open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Processed {f}")
