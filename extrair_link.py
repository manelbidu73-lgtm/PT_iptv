import time
import sys
import requests
import re
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def buscar_proxy_gratis():
    print("A procurar proxy funcional...")
    try:
        # Vai buscar uma lista de proxies gratuitos
        response = requests.get("https://proxyscrape.com")
        proxies = response.text.splitlines()
        if proxies:
            return proxies[0] # Retorna o primeiro da lista
    except:
        return None
    return None

def extrair():
    proxy = buscar_proxy_gratis()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    proxy_options = {}
    if proxy:
        print(f"A usar proxy: {proxy}")
        proxy_options = {
            'proxy': {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
        seleniumwire_options=proxy_options
    )

    try:
        driver.set_page_load_timeout(60)
        print("A abrir o site Sportssonline...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        
        time.sleep(30) # Tempo para o player carregar via proxy

        link_m3u8 = None
        for request in driver.requests:
            if request.response:
                url = request.url
                if '.m3u8' in url and not any(x in url for x in ['google', 'ads']):
                    link_m3u8 = url
                    break

        if link_m3u8:
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,Sport TV 1\n{link_m3u8}")
            print("SUCESSO!")
        else:
            print("FALHA: Proxy bloqueado ou link não encontrado.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
