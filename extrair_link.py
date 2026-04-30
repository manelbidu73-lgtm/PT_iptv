import time
import sys
from seleniumwire import webdriver # Usamos selenium-wire em vez de selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    link_m3u8 = None

    try:
        print("A abrir Megatuga e a monitorizar rede...")
        driver.get("https://megatuga.io")
        time.sleep(15) # Tempo para carregar scripts iniciais

        # Procura e clica na Sport TV 1
        try:
            canais = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sport TV 1')]")
            if canais:
                driver.execute_script("arguments.click();", canais[0])
                print("Clique na Sport TV 1 efetuado. A capturar pedidos de rede...")
                time.sleep(15) # Tempo para o player disparar o link m3u8
        except Exception as e:
            print(f"Erro ao clicar: {e}")

        # Analisa todos os pedidos de rede efetuados pelo browser
        for request in driver.requests:
            if request.response:
                url = request.url
                # Filtra links m3u8 que geralmente contêm tokens
                if '.m3u8' in url and ('token=' in url or 'hls' in url or 'key=' in url):
                    link_m3u8 = url
                    break

        if link_m3u8:
            # Limpa o link de possíveis caracteres indesejados
            link_m3u8 = link_m3u8.split('"')[0].split("'")[0]
            
            conteudo = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"{link_m3u8}"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"SUCESSO! Link capturado via Network: {link_m3u8[:60]}...")
        else:
            print("ERRO: O link m3u8 não passou pela rede do browser.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
