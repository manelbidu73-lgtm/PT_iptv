import time
import sys
import re
import requests # Garante que tens este import
from seleniumwire import webdriver

def extrair():
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

    # Inicia o browser com monitorização de rede
        # Adicionamos seleniumwire_options=proxy_options
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options,
        seleniumwire_options=proxy_options
    )

    try:
        print("A abrir o site e a monitorizar a rede (Igual ao DownloadHelper)...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        
        # Espera 30 segundos para o player carregar e o link aparecer na rede
        time.sleep(30)

        # Analisa todos os pedidos de rede que o browser fez
        for request in driver.requests:
            if request.response:
                url = request.url
                # Procura o link com o padrão que me mandaste (s= e e=)
                if '.m3u8?s=' in url and '&e=' in url:
                    link_m3u8 = url
                    break

        if link_m3u8:
            print(f"Sucesso! Link capturado da rede.")
            # O "|" ajuda o teu player a passar as proteções 403
            m3u_content = (
                "#EXTM3U\n"
                f"#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://sportssonline.click"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: O link não passou pela rede. O vídeo pode não ter iniciado.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
