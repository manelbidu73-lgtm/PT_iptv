import asyncio
import random
from playwright_extra import async_playwright
from playwright_extra_plugin_stealth import stealth_sync

async def extrair_com_stealth_e_sessao():
    # Iniciamos o Playwright com suporte a plugins de ocultação
    async with async_playwright() as p:
        
        # Ativa o modo furtivo para mascarar assinaturas de automação (evita o bloqueio do Cloudflare)
        p.selectors.set_test_id_attribute("data-testid")
        
        browser = await p.chromium.launch(
            headless=False, # Mude para True se for rodar no servidor do GitHub Actions
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
        
        # Aplica o pacote stealth especificamente nesta página para passar nos testes antibot
        # (Remove flags como navigator.webdriver = true, altera canvas, WebGL, etc.)
        # Nota: O pacote stealth_sync aplica-se de forma transparente
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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
            # COLOQUE A URL DO SEGUNDO SITE AQUI
            url_segundo_site = "https://url-do-segundo-site-aqui.com"
            
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
                with open("playlist.m3u", "w", encoding="utf-8") as f:
                    f.write(conteudo_m3u)
                print("Ficheiro playlist.m3u atualizado com sucesso!")
            else:
                print("[AVISO] O segundo site abriu com sucesso, mas nenhum .m3u8 foi disparado. O jogo pode não ter começado.")

        except Exception as e:
            print(f"[ERRO] O Cloudflare ou o redirecionamento falhou: {e}")
            await page.screenshot(path="screenshot_bloqueio.png")
        finally:
            await browser.close()

asyncio.run(extrair_com_stealth_e_sessao())
