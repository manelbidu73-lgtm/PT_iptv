import time
import sys
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def extrair():
    options = uc.ChromeOptions()
    # NÃO usar o modo headless tradicional, pois é facilmente detetado
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Inicia o browser "indetetável"
    driver = uc.Chrome(options=options)
    
    try:
        print("A aceder ao player direto...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        
        # Espera longa para o bypass da Cloudflare e carregamento do player
        time.sleep(25)

        # 1. Tenta clicar no centro do ecrã para ativar o stream
        try:
            driver.find_element(By.TAG_NAME, "body").click()
            print("Clique de ativação efetuado.")
            time.sleep(10)
        except:
            pass

        # 2. Varre o código de todos os frames à procura do m3u8
        html_total = driver.page_source
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                html_total += driver.page_source
                driver.switch_to.default_content()
            except:
                continue

        # Regex para capturar o link com o token
        # Procura por padrões comuns como playlist.m3u8?token= ou similar
        links = re.findall(r'https?://[^\s"\']+\.m3u8\?[^\s"\']+', html_total.replace('\\/', '/'))

        if links:
            # Filtra para evitar links de publicidade
            link_final = [l for l in links if "google" not in l and "ads" not in l]
            
            conteudo = f"#EXTM3U\n#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n{link_final}"
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"SUCESSO! Link extraído.")
        else:
            print("ERRO: Link não encontrado. O site pode estar a bloquear o IP do GitHub.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
