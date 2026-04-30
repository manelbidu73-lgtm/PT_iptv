import time
import sys
import re
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def extrair():
    options = uc.ChromeOptions()
    options.add_argument("--headless") # Roda sem abrir janela no GitHub
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Inicia o navegador indetetável
    driver = uc.Chrome(options=options)
    
    try:
        print("A abrir o site Sportssonline...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        
        # Espera 25 segundos para o site carregar tudo (como o DownloadHelper faz)
        time.sleep(25)
        
        # Captura todo o código gerado após o JavaScript correr
        html_final = driver.page_source
        
        # O padrão exato do link que me enviaste
        padrao = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        links = re.findall(padrao, html_final.replace('\\/', '/'))

        if links:
            link_direto = links[0]
            print(f"Sucesso! Link capturado.")
            
            m3u_content = (
                "#EXTM3U\n"
                f"#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n"
                f"#EXTVLCOPT:http-referrer=https://sportssonline.click\n"
                f"{link_direto}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)&Referer=https://sportssonline.click"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: O link com s= e e= não apareceu mesmo com o navegador aberto.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
