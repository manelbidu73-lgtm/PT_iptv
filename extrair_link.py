import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0...")
        page = await context.new_page()
        
        target_url = "https://sportssonline.click"
        found_link = None

        # Captura o link e guarda na variável
        def capture_request(request):
            nonlocal found_link
            if ".m3u8" in request.url and "chunk" not in request.url:
                found_link = request.url

        page.on("request", capture_request)

        await page.goto("https://sportssonline.click", wait_until="networkidle")
        await page.goto(target_url, wait_until="networkidle")
        await asyncio.sleep(15)

        if found_link:
            with open("sporttv1.m3u8", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,Sport TV 1\n{found_link}")
            print(f"✅ Link guardado com sucesso!")
        else:
            print("❌ Link não encontrado.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
    
