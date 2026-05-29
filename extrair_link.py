import asyncio
import random
from playwright.async_api import async_playwright

async def extrair_com_sessao_nativa():
    async with async_playwright() as p:
        
        # Lança o Chromium aplicando argumentos nativos para ocultar a automação
        browser = await p.chromium.launch(
            headless=True, 
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--disable-dev-shm-usage"
            ]
        )
        
        # Criamos o contexto emulando perfeitamente um navegador Chrome real em Windows
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="pt-PT",
            timezone_id="Europe/Lisbon",
            extra_http_headers={
                "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"'
            }
        )
        
        page = await context.new_page()
        
        # Injeta um script nativo na página para apagar o rasto do 'navigator.webdriver'
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        link_final_stream = None

        # Escuta ativa da rede
        async def capturar_link(request):
            nonlocal link_final_stream
            url = request.url
            if ".m3u8" in url or "token=" in url.lower():
                if "playlist.m3u" not in url:
                    print(f"[SUCESSO] Link IPTV Detetado: {url}")
                    link_final_stream = url

        page.on("request", capturar_link)

        try:
            # PASSO 1: Validar cookies no site pai
            print("1. A aceder ao dzeko11.de...")
            await page.goto("https://dzeko11.de", wait_until="commit", timeout=60000)
            
            tempo_espera = random.randint(10, 15)
            print(f"A aguardar {tempo_espera} segundos para estabilização de sessão...")
            await page.wait_for_timeout(tempo_espera * 1000)

            # PASSO 2: Ir direto ao segundo site com Referer injetado
            # SUBSTITUA ABAIXO PELA URL DO SEGUNDO SITE QUE DETECTOU
            url_segundo_site = "https://main.wwin.cloud/player/60"
            
            print(f"2. A saltar diretamente para o segundo site com o Referer...")
            await page.goto(
                url_segundo_site, 
                referer="https://dzeko11.de", 
                wait_until="load", 
                timeout=60000
            )

            # PASSO 3: Aguardar o player disparar o link m3u8
            print("3. A aguardar que o stream dispare o token na rede...")
            await page.wait_for_timeout(15000)

            if link_final_stream:
                 link_com_headers = f"{link_final_stream}|http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36&http-referer=https://main.wwin.cloud/&http-origin=https://main.wwin.cloud"
        
        conteudo_m3u = f"""#EXTM3U
#EXTINF:-1, SPORT TV 2
{link_com_headers}
"""
            with open("sporttv2.m3u", "w", encoding="utf-8") as f:
                    f.write(conteudo_m3u)
                print("Ficheiro playlist.m3u atualizado com sucesso!")
            else:
                print("[AVISO] O segundo site abriu com sucesso, mas nenhum .m3u8 foi disparado.")

        except Exception as e:
            print(f"[ERRO] O processo falhou: {e}")
            await page.screenshot(path="screenshot_bloqueio.png")
        finally:
            await browser.close()

asyncio.run(extrair_com_sessao_nativa())
