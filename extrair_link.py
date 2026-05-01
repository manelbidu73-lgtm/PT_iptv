import time
import sys
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
        print("A abrir o Megatuga (Canais de Desporto)...")
        driver.get("https://megatuga.io")
        
        # Esperamos 45 segundos para o site carregar o player e os tokens
        print("A aguardar 45 segundos para capturar tráfego de rede...")
        time.sleep(45)

        # Analisa todos os pedidos de rede (como o DownloadHelper faz)
        for request in driver.requests:
            url = request.url
            # Procura o padrão s= e e= que me mandaste
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        if link_m3u8:
            print(f"SUCESSO! Link encontrado.")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O link não passou pela rede. O player pode exigir um clique.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro crítico: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
