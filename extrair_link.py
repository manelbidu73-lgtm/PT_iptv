import time
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair():
    link_m3u8 = None 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("A abrir Megatuga Desporto...")
        driver.get("https://megatuga.io/canais-de-desporto")
        time.sleep(15)

        # 1. Tentar encontrar e clicar no botão Sport TV 1
        print("A procurar botão da Sport TV 1...")
        try:
            # Tenta clicar no elemento que contém o texto
            botao = driver.find_element(By.XPATH, "//a[contains(., 'Sport TV 1')]")
            driver.execute_script("arguments[0].click();", botao)
            print("Clique no canal efetuado.")
            time.sleep(10)
        except:
            print("Aviso: Botão não encontrado ou já clicado.")

        # 2. MÉTODO DO DOWNLOAD HELPER: Monitorizar a rede
        print("A aguardar 40 segundos para capturar o link m3u8...")
        time.sleep(40) 

        for request in driver.requests:
            url = request.url
            # Procura exatamente o padrão do link que mandaste
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        if link_m3u8:
            print(f"SUCESSO! Link capturado.")
            # Criar o M3U com Referer do Megatuga
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                "#EXTVLCOPT:http-referrer=https://megatuga.io\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O link não passou pela rede. O player pode estar bloqueado.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
