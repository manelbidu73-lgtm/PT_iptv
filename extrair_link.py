import time
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def extrair():
    link_m3u8 = None 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # Define tamanho para o clique ser certeiro
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("A abrir o Megatuga...")
        driver.get("https://megatuga.io")
        time.sleep(20) # Espera o site carregar os anúncios

        # Tenta clicar no centro do ecrã várias vezes para dar Play no vídeo
        print("A tentar dar Play no vídeo (clique forçado)...")
        try:
            actions = ActionChains(driver)
            # Clica no centro (onde costuma estar o player)
            actions.move_by_offset(960, 540).click().perform()
            time.sleep(2)
            actions.click().perform() 
            print("Cliques efetuados.")
        except Exception as e:
            print(f"Aviso ao clicar: {e}")

        print("A aguardar 40 segundos para o link aparecer na rede...")
        time.sleep(40)

        for request in driver.requests:
            url = request.url
            # Procura o padrão de token que o teu DownloadHelper vê
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        if link_m3u8:
            print("SUCESSO! Link pescado.")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O player não disparou o link. Tenta aumentar o tempo ou o site bloqueou o IP.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
