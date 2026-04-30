import re
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    link_m3u8 = None

    try:
        print("A carregar Megatuga...")
        driver.get("https://megatuga.io/canais-de-desporto")
        time.sleep(10)

        # Tenta clicar no canal Sport TV 1
        try:
            canais = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sport TV 1')]")
            if canais:
                driver.execute_script("arguments[0].click();", canais[0])
                print("Clique efetuado. A aguardar carregamento do player...")
                time.sleep(10)
        except Exception as e:
            print(f"Não foi possível clicar: {e}")

        # Procura em todos os frames da página
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Encontrados {len(iframes)} iframes. A analisar...")

        # Procura o link no HTML principal
        html_source = driver.page_source
        links = re.findall(r'https?://[^\s"\']+\.m3u8\?[^\s"\']+', html_source.replace('\\/', '/'))
        
        # Se não achou no principal, entra em cada iframe
        if not links:
            for index, iframe in enumerate(iframes):
                try:
                    driver.switch_to.frame(iframe)
                    links += re.findall(r'https?://[^\s"\']+\.m3u8\?[^\s"\']+', driver.page_source.replace('\\/', '/'))
                    driver.switch_to.default_content()
                except:
                    continue

        if links:
            link_m3u8 = links[0]
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n{link_m3u8}")
            print(f"Sucesso! Link guardado: {link_m3u8[:50]}...")
        else:
            print("Link não encontrado em nenhum frame.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
