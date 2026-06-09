import asyncio
from playwright.async_api import async_playwright
import os
import fitz

async def main():
    html_path = f"file:///{os.path.abspath('katalog_dergi.html').replace(chr(92), '/')}"
    print(f"Loading {html_path}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use print styles
        page = await browser.new_page()
        await page.emulate_media(media="print")
        
        await page.goto(html_path, wait_until="networkidle")
        
        print("Scrolling down to trigger lazy loading...")
        # Scroll to bottom
        await page.evaluate("""
            async () => {
                await new Promise((resolve, reject) => {
                    var totalHeight = 0;
                    var distance = 500;
                    var timer = setInterval(() => {
                        var scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;

                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100);
                });
            }
        """)
        
        # Wait a bit more for images to settle
        await page.wait_for_timeout(5000)
        
        print("Generating High Quality (Print) PDF...")
        baski_pdf = "katalog_dergi_baski.pdf"
        # Since it's a catalog, it might be landscape A4 or portrait A4.
        # We don't specify format so it uses the @page CSS format if provided, or default A4.
        await page.pdf(path=baski_pdf, print_background=True, format="A4")
        print(f"Saved: {baski_pdf} (Size: {os.path.getsize(baski_pdf)/1024/1024:.2f} MB)")
        
        await browser.close()
        
        # Now use PyMuPDF to compress it for "müşteriye göndermelik"
        print("Compressing PDF for customer version...")
        musteri_pdf = "katalog_dergi_musteri.pdf"
        
        doc = fitz.open(baski_pdf)
        
        # To heavily compress images, we can iterate over pages and reduce image quality, 
        # but PyMuPDF's save with deflate and garbage collection often reduces the size.
        doc.save(musteri_pdf, garbage=4, deflate=True, deflate_images=True, deflate_fonts=True)
        print(f"Saved: {musteri_pdf} (Size: {os.path.getsize(musteri_pdf)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    asyncio.run(main())
