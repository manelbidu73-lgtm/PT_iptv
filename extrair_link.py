import time
import sys
import re
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extrair():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    link_m3u8 = None

    try:
        print("A aceder ao site Sportssonline...")
        driver.get("https://sportssonline.click")
        
        # Espera para carregar frames e scripts
        time.sleep(20) 

        # ESTRATÉGIA 1: Procurar nos pedidos de rede (Sniffer)
        print("Analisando tráfego de rede...")
        for request in driver.requests:
            if request.response:
                url = request.url
                if '.m3u8' in url and "google" not in url and "doubleclick" not in url:
                    link_m3u8 = url
                    break

        # ESTRATÉGIA 2: Se não achou na rede, varrer o HTML de todos os IFRAMES
        if not link_m3u8:
            print("Link não achado na rede. Varrendo IFRAMEs...")
            iframes = driver.find_elements("tag name", "iframe")
            for f in iframes:
                try:
                    driver.switch_to.frame(f)
                    html = driver.page_source
                    found = re.findall(r'https?://[^\s"\']+\.m3u8\?[^\s"\']+', html.replace('\\/', '/'))
                    if found:
                        link_m3u8 = found[0]
                        driver.switch_to.default_content()
                        break
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()
                    continue

        if link_m3u8:
            # Limpeza de caracteres de escape comuns em JS
            link_m3u8 = link_m3u8.replace('\\/', '/').replace('"', '').replace("'", "")
            
            print(f"SUCESSO! Link: {link_m3u8[:60]}...")
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n{link_m3u8}")
        else:
            print("FALHA: O link não foi encontrado nem na rede nem nos frames.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
