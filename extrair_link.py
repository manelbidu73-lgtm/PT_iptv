import time
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extrair():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Roda em segundo plano
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # User-agent real para não ser bloqueado
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    link_m3u8 = None

    try:
        print("A abrir o site...")
        driver.get("https://v3.sportssonline.click/channels/pt/sporttv1.php")
        
        # 1. Esperar que os canais apareçam e clicar na Sport TV 1
        wait = WebDriverWait(driver, 20)
        print("A procurar o botão da Sport TV 1...")
        
        # Procura o link ou botão que contém 'sport-tv-1'
        botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'sport-tv-1')] | //*[contains(text(), 'Sport TV 1')]")))
        driver.execute_script("arguments[0].click();", botao)
        
        print("Clique no canal efetuado. A aguardar o player carregar...")
        time.sleep(10) # Espera a página do player abrir

        # 2. Tentar clicar no botão de PLAY (se houver um overlay/frame)
        # Muitos sites de IPTV usam um botão de play central
        try:
            # Tenta clicar no centro do ecrã onde costuma estar o Play
            play_button = driver.find_elements(By.XPATH, "//button | //div[contains(@class, 'play')]")
            for b in play_button:
                if b.is_displayed():
                    driver.execute_script("arguments[0].click();", b)
                    print("Clique no botão de Play efetuado!")
        except:
            pass

        print("A monitorizar pedidos de rede por 20 segundos...")
        time.sleep(20) # Tempo para o vídeo começar e o link m3u8 aparecer na rede

        # 3. O 'Sniffer' analisa todos os pedidos feitos pelo browser
        for request in driver.requests:
            if request.response:
                url = request.url
                # Procura links m3u8 que não sejam publicidade (geralmente têm tokens)
                if '.m3u8' in url and ('token' in url or 'hls' in url or 'm3u8' in url):
                    if "ads" not in url and "google" not in url:
                        link_m3u8 = url
                        break

        if link_m3u8:
            print(f"Link capturado: {link_m3u8[:70]}...")
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n{link_m3u8}")
        else:
            print("Não foi possível capturar o link m3u8. O vídeo pode não ter arrancado.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
