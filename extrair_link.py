import asyncio
import random
from playwright.async_api import async_playwright
# Importa o módulo correto de camuflagem para Python
from playwright_stealth import stealth_async

async def extrair_com_stealth_e_sessao():
    async with async_playwright() as p:
        
        # Inicia o navegador (Mantenha headless=True para o GitHub Actions)
        browser = await p.chromium.launch(
            headless=True, 
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars"
            ]
        )
        
        # Cria um contexto imitando um computador real (Windows/Chrome)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="pt-PT",
            timezone_id="Europe/Lisbon"
        )
        
        page = await context.new_page()
        
        # APLICA O STEALTH: Esta linha ativa a camuflagem antibot na página criada
        await stealth_async(page)

        link_final_stream = None

        # Escuta o tráfego oculto da rede procurando o ficheiro .m3u8 final
        async def capturar_link(request):
            nonlocal link_final_stream
            url = request.url
            if ".m3u8" in url or "token=" in url.lower():
                if "playlist.m3u" not in url:
                    print(f"[SUCESSO] Link IPTV Detetado: {url}")
                    link_final_stream = url

        page.on("request", capturar_link)

        try:
            # PASSO 1: Entrar no Dzeko11.de para validar o Cloudflare e guardar os Cookies
            print("1. A aceder ao dzeko11.de com proteção Stealth...")
            await page.goto("https://dzeko11.de", wait_until="commit", timeout=60000)
            
            # Aguarda um tempo humano aleatório enquanto o Cloudflare resolve o desafio invisível
            tempo_espera = random.randint(10, 15)
            print(f"A aguardar {tempo_espera} segundos para o Cloudflare validar a sessão...")
            await page.wait_for_timeout(tempo_espera * 1000)

            # PASSO 2: Ir direto ao segundo site simulando que veio do primeiro (sem cliques)
            # SUBSTITUA PELA URL DO SEGUNDO SITE QUE DETECTOU
            url_segundo_site = "https://main.wwin.cloud/player/60"
            
            print(f"2. A saltar diretamente para o segundo site com o Referer injetado...")
            await page.goto(
                url_segundo_site, 
                referer="https://dzeko11.de", # Engana o servidor provando a origem legítima
                wait_until="load", 
                timeout=60000
            )

            # PASSO 3: Dar tempo para o player do segundo site começar a carregar o vídeo
            print("3. A aguardar que o stream dispare o token na rede...")
            await page.wait_for_timeout(15000)

            if link_final_stream:
                # Gera a playlist final formatada
                conteudo_m3u = (
                    f"#EXTM3U\n"
                    f"#EXTINF:-1, Stream Dzeko11\n"
                    f"#EXTVLCOPT:http-referrer=https://dzeko11.de\n"
                    f"{link_final_stream}\n"
                )
                with open("sporttv2.m3u", "w", encoding="utf-8") as f:
                    f.write(conteudo_m3u)
                print("Ficheiro playlist.m3u atualizado com sucesso!")
            else:
                print("[AVISO] O segundo site abriu com sucesso, mas nenhum .m3u8 foi disparado.")

        except Exception as e:
            print(f"[ERRO] O Cloudflare ou o redirecionamento falhou: {e}")
            await page.screenshot(path="screenshot_bloqueio.png")
        finally:
            await browser.close()

asyncio.run(extrair_com_stealth_e_sessao())
