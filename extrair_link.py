import time
import sys
import re
import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options  # ESTA LINHA CORRIGE O ERRO
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extrair():
    link_m3u8 = None 
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Roda em segundo plano
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

        # Configuração de Proxy para tentar IP de Portugal ou Europa
    # Nota: Proxies grátis falham muito. Se der erro, corre o workflow outra vez.
    proxy_options = {
        'proxy': {
            'http': 'http://188.93.228.41:80', # Exemplo de IP europeu, podes trocar se falhar
            'https': 'https://188.93.228.41:80',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    try:
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        time.sleep(30)

        for request in driver.requests:
            if request.response:
                url = request.url
                if '.m3u8?s=' in url and '&e=' in url:
                    link_m3u8 = url
                    break

        # 2. Só tenta gravar o ficheiro se o link foi realmente encontrado
        if link_m3u8:
            print(f"Sucesso! Link capturado.")
            m3u_content = f"#EXTM3U\n#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://sportssonline.click"
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: O link nao foi detetado na rede.")
            sys.exit(1) # Força o erro para tu saberes que falhou a captura

    finally:
        driver.quit()




    extrair()
