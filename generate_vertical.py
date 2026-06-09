import copy
from bs4 import BeautifulSoup

def process_html():
    with open('katalog_dergi_tr.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Pages are inside .flip-book
    all_pages_raw = soup.select('.flip-book > .page')

    # Filter out dummy/blank pages
    real_pages = []
    for page in all_pages_raw:
        style = page.get('style', '')
        if '#1a1a1a' not in style:
            real_pages.append(page)

    VERTICAL_CSS = """
        /* ===== RESET STYLES ===== */
        * { box-sizing: border-box; }
        body {
            background-color: #1a1a1a;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            font-family: 'Montserrat', sans-serif;
        }

        :root {
            --book-width: 500px;
            --book-height: 707px;
        }

        /* ===== COMMON PAGE OVERRIDES ===== */
        .page {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            transform: none !important;
            margin: 0 !important;
            box-shadow: none !important; 
        }
        .page::before, .page::after {
            box-shadow: none !important;
        }

        /* ===== MÜŞTERİ VERSİYONU ===== */
        .vertical-customer-layout {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            padding: 40px 10px; /* Kenarlardan biraz boşluk */
            gap: 40px;
        }

        .vertical-customer-layout .cover-row {
            display: flex;
            justify-content: center;
            width: 100%;
            max-width: 500px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        .vertical-customer-layout .spread-row {
            display: flex;
            flex-direction: row; /* HER ZAMAN YAN YANA (2'Lİ) */
            justify-content: center;
            width: 100%;
            max-width: 1000px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        .page-wrapper {
            position: relative;
            overflow: hidden;
            background-color: #ffffff;
        }

        /* Kapak tek sayfa */
        .vertical-customer-layout .cover-row .page-wrapper {
            width: 100%;
            aspect-ratio: 500 / 707;
        }

        /* Yan yana iki sayfa */
        .vertical-customer-layout .spread-row .page-wrapper {
            flex: 1 1 50%; /* Kesinlikle %50 genişlik */
            width: 50%;
            max-width: 50%;
            aspect-ratio: 500 / 707;
            height: auto;
        }

        /* MÜŞTERİ PDF ÇIKTISI İÇİN (Yatay A4) */
        @media print {
            html { font-size: 1.4vw !important; }
            body { background-color: #121212; margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            .vertical-customer-layout {
                padding: 0; gap: 0;
                display: block !important;
                background-color: #121212 !important;
            }
            .vertical-customer-layout .cover-row,
            .vertical-customer-layout .spread-row {
                display: flex !important;
                flex-direction: row !important;
                box-shadow: none !important;
                page-break-inside: avoid;
                break-inside: avoid;
                page-break-after: always;
                break-after: page;
                margin: 0 !important;
                width: 100%;
                max-width: none;
                height: auto !important;
            }
            .vertical-customer-layout .cover-row {
                background-color: #121212 !important;
            }
            .vertical-customer-layout .cover-row .page-wrapper {
                margin: 0 auto;
                height: auto !important;
                width: 50% !important;
                aspect-ratio: 500 / 707 !important;
            }
            .vertical-customer-layout .spread-row .page-wrapper {
                flex: 0 0 50% !important;
                width: 50% !important;
                height: auto !important;
                aspect-ratio: 500 / 707 !important;
            }
            .page-wrapper {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            @page {
                size: A4 landscape;
                margin: 0;
            }
        }

        /* ===== BASKI VERSİYONU ===== */
        .vertical-print-layout {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            gap: 20px;
            padding: 20px 10px;
        }

        .vertical-print-layout .page-wrapper {
            width: 100%;
            max-width: 500px;
            aspect-ratio: 500 / 707;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        /* MATBAA PDF ÇIKTISI İÇİN (Dikey A4) */
        @media print {
            .vertical-print-layout {
                padding: 0; gap: 0;
            }
            .vertical-print-layout .page-wrapper {
                box-shadow: none !important;
                margin: 0 !important;
                max-width: none;
                page-break-after: always;
                break-after: page;
            }
        }

        /* Düzeltme: Spread arka planının sola/sağa hizalanması */
        .page-spread-left .page-content::before {
            left: 0 !important;
            right: auto !important;
        }
        .page-spread-right .page-content::before {
            right: 0 !important;
            left: auto !important;
        }
    """

    def create_base_soup():
        base = BeautifulSoup(html, 'html.parser')
        # Remove unwanted elements
        for el in base.select('#loading-overlay, .loading-overlay, .mobile-warning, .controls, #print-container, .catalog-wrapper, script'):
            el.decompose()
        # Add vertical CSS
        style_tag = base.new_tag('style')
        style_tag.string = VERTICAL_CSS
        base.head.append(style_tag)
        return base

    def wrap_page(soup_ref, page_el):
        """Wrap a page in a .page-wrapper div to provide sizing context"""
        wrapper = soup_ref.new_tag('div', attrs={'class': 'page-wrapper'})
        wrapper.append(page_el)
        return wrapper

    # =====================
    # 1. Müşteri Versiyonu
    # =====================
    musteri_soup = create_base_soup()
    container = musteri_soup.new_tag('div', attrs={'class': 'vertical-customer-layout'})

    if real_pages:
        # Kapak
        cover_row = musteri_soup.new_tag('div', attrs={'class': 'cover-row'})
        cover_row.append(wrap_page(musteri_soup, copy.deepcopy(real_pages[0])))
        container.append(cover_row)

        # Diğerleri yan yana
        for i in range(1, len(real_pages), 2):
            spread_row = musteri_soup.new_tag('div', attrs={'class': 'spread-row'})
            spread_row.append(wrap_page(musteri_soup, copy.deepcopy(real_pages[i])))
            if i + 1 < len(real_pages):
                spread_row.append(wrap_page(musteri_soup, copy.deepcopy(real_pages[i + 1])))
            container.append(spread_row)

    musteri_soup.body.append(container)

    with open('katalog_musteri.html', 'w', encoding='utf-8') as f:
        f.write(str(musteri_soup))

    # =====================
    # 2. Baskı Versiyonu
    # =====================
    baski_soup = create_base_soup()
    
    baski_style = baski_soup.new_tag('style')
    baski_style.string = "@media print { @page { size: portrait; } }"
    baski_soup.head.append(baski_style)

    baski_container = baski_soup.new_tag('div', attrs={'class': 'vertical-print-layout'})

    for page in real_pages:
        baski_container.append(wrap_page(baski_soup, copy.deepcopy(page)))

    baski_soup.body.append(baski_container)

    with open('katalog_baski.html', 'w', encoding='utf-8') as f:
        f.write(str(baski_soup))

if __name__ == '__main__':
    process_html()
