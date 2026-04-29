import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Abre o navegador
        browser = await p.chromium.launch(headless=True)
        # O segredo está aqui: simular um computador real
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # O URL exato que tu queres
        target_url = "https://v3.sportssonline.click/channels/pt/sporttv1.php"
        
        # O "Ouvinte" - se o link do vídeo passar pela rede, ele apanha
        page.on("request", lambda request: print(f"🔗 LINK DO VÍDEO DETETADO: {request.url}") if ".m3u8" in request.url else None)

        print(f"A tentar aceder à Sport TV 1...")
        
        try:
            # 1. Vai primeiro à base do site para criar um "cookie" de sessão
            await page.goto("https://v3.sportssonline.click/", wait_until="networkidle")
            
            # 2. Agora sim, vai para o URL da Sport TV 1
            await page.goto(target_url, wait_until="networkidle")
            
            # 3. Espera o vídeo carregar (mesmo com anúncios)
            await asyncio.sleep(20) 
            
            print("Processo terminado. Se o link não apareceu, o site pode ter bloqueado o acesso automático.")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
    
