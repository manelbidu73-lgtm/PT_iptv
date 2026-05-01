import time
import sys
import re
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extrair():
    print("A iniciar o processo...") # Isto TEM de aparecer no log
    link_m3u8 = None 
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("A abrir o site Sportssonline...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        
        print("A aguardar 30 segundos para capturar rede...")
        time.sleep(30)

        # Contador para sabermos quantos pedidos o sniffer viu
        pedidos_vistos = 0
        for request in driver.requests:
            pedidos_vistos += 1
            url = request.url
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        print(f"Analisados {pedidos_vistos} pedidos de rede.")

        if link_m3u8:
            print(f"SUCESSO: Link encontrado!")
         # Formato otimizado para VLC e outras Apps
m3u_content = (
    "#EXTM3U\n"
    f"#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
    f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n"
    f"#EXTVLCOPT:http-referrer=https://sportssonline.click\n"
    f"{link_m3u8}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://sportssonline.click"
)
      else:
            print("AVISO: O link nao foi encontrado na rede desta vez.")
            # Se não encontrar, forçamos o erro para o círculo ficar vermelho e sabermos
            sys.exit(1)

    except Exception as e:
        print(f"ERRO CRITICO: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
