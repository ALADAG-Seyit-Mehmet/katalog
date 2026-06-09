import asyncio
from playwright.async_api import async_playwright
import os
import fitz

async def main():
    html_path = f"file:///{os.path.abspath('katalog_musteri.html').replace(chr(92), '/')}"
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
        
        print("Generating High Quality Landscape PDF...")
        yatay_pdf = "katalog_yatay.pdf"
        # We explicitly set landscape=True
        await page.pdf(path=yatay_pdf, print_background=True, landscape=True, format="A4")
        print(f"Saved: {yatay_pdf} (Size: {os.path.getsize(yatay_pdf)/1024/1024:.2f} MB)")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
