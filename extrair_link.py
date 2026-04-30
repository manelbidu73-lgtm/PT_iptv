import time
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # User-Agent de um Chrome real para evitar bloqueios
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    link_m3u8 = None

    try:
        print("A carregar site estilo 'DownloadHelper'...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        time.sleep(15)

        # 1. Tentar remover overlays de publicidade que impedem o clique
        driver.execute_script("""
            var ads = document.querySelectorAll('div[style*="z-index"], iframe[id*="google"], .ads-class');
            for (var i = 0; i < ads.length; i++) { ads[i].remove(); }
        """)

        # 2. Clicar no centro do ecrã para iniciar o vídeo (como o Video DownloadHelper faz)
        try:
            print("A simular clique no player para iniciar o stream...")
            # Clica no body ou num elemento grande para ativar o player
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(5)
        except:
            pass

        # 3. Monitorizar o tráfego de rede (Sniffing)
        print("A escanear tráfego de rede à procura de m3u8...")
        # Espera 30 segundos para o vídeo começar a descarregar chunks
        start_time = time.time()
        while time.time() - start_time < 30:
            for request in driver.requests:
                if request.response:
                    url = request.url
                    # Procura o link que o DownloadHelper encontraria
                    if '.m3u8' in url and "google" not in url and "doubleclick" not in url:
                        # Ignora se for apenas um pedaço (chunk) e tenta pegar a playlist principal
                        if "index" in url or "playlist" in url or "token" in url:
                            link_m3u8 = url
                            break
            if link_m3u8: break
            time.sleep(2)

        if link_m3u8:
            print(f"SUCESSO! Link detetado: {link_m3u8[:70]}...")
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n{link_m3u8}")
        else:
            print("FALHA: O vídeo não iniciou ou o link não passou pela rede.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
