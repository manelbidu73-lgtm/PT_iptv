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
        print("A abrir o Megatuga...")
        driver.get("https://megatuga.io/canais-de-desporto") 
        time.sleep(15) # Aumentei um pouco para garantir o carregamento

        # Procura o botão da Sport TV 1 e clica nele
        try:
            print("A selecionar Sport TV 1...")
            # XPATH melhorado para encontrar o link exato
            botao = driver.find_element("xpath", "//a[contains(., 'Sport TV 1')]")
            driver.execute_script("arguments[0].click();", botao)
            print("Clique efetuado!")
        except Exception as e:
            print(f"Aviso: Nao foi possivel clicar. Erro: {e}")

        print("A aguardar 40 segundos para o player disparar o link na rede...")
        time.sleep(40) 

        # 1. Capturar o link da rede (procuramos m3u8 genérico já que o site mudou)
        for request in driver.requests:
            if request.response:
                url = request.url
                # No Megatuga o padrão pode ser diferente, vamos procurar apenas .m3u8
                if '.m3u8' in url and 'ads' not in url:
                    link_m3u8 = url
                    break

        # 2. Criar o ficheiro se encontrar o link
        if link_m3u8:
            print(f"Sucesso! Link capturado.")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                "#EXTVLCOPT:http-referrer=https://megatuga.io/\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io/"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: Link nao encontrado na rede.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro critico: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
