content = open('katalog_dergi_en.html', encoding='utf-8').read()

front_target = """                    <div class="cover-inner">
                        <span class="eyebrow">SINCE 1986</span>
                        <div class="logo-crop front-logo">
                            <img src="sedirkon_logo_header.webp" alt="Sedirkon Logo">
                        </div>"""

front_replace = """                    <div class="logo-crop top-logo">
                        <img src="sedirkon_logo_header.webp" alt="Sedirkon Logo">
                    </div>
                    <div class="cover-inner">
                        <span class="eyebrow">SINCE 1986</span>
                        <h1>SEDİRKON</h1>"""

back_target = """                    <div class="back-cover-inner">
                        <div class="logo-area">
                            <div class="logo-crop back-logo">
                                <img src="sedirkon_logo_header.webp" alt="Sedirkon Logo">
                            </div>"""

back_replace = """                    <div class="logo-crop top-logo">
                        <img src="sedirkon_logo_header.webp" alt="Sedirkon Logo">
                    </div>
                    <div class="back-cover-inner">
                        <div class="logo-area">
                            <h2>SEDİRKON</h2>"""

content = content.replace(front_target, front_replace)
content = content.replace(back_target, back_replace)

open('katalog_dergi_en.html', 'w', encoding='utf-8').write(content)
print("done")
