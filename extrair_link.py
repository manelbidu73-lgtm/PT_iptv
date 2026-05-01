import time
import sys
import re
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extrair():
    link_m3u8 = None 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("A abrir o site...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        time.sleep(30)

        # 1. Capturar o link da rede
        for request in driver.requests:
            if request.response:
                url = request.url
                if '.m3u8?s=' in url and '&e=' in url:
                    link_m3u8 = url
                    break

        # 2. Criar o ficheiro se encontrar o link
        if link_m3u8:
            print(f"Sucesso! Link capturado.")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n"
                "#EXTVLCOPT:http-referrer=https://sportssonline.click\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://sportssonline.click"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: Link nao encontrado.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro critico: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
