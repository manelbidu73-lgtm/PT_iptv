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
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("A abrir o Megatuga (Canais de Desporto)...")
        driver.get("https://megatuga.io")
        time.sleep(15)

        # MÉTODO DE CLIQUE MELHORADO
        print("A procurar e clicar no canal Sport TV 1...")
        try:
            # Procura qualquer link que contenha 'sport-tv-1' no endereço ou texto
            canais = driver.find_elements(By.XPATH, "//a[contains(@href, 'sport-tv-1') or contains(., 'Sport TV 1')]")
            if canais:
                # Clica no primeiro que encontrar
                driver.execute_script("arguments[0].click();", canais[0])
                print("Clique no canal efetuado com sucesso!")
            else:
                print("Aviso: Botão do canal não encontrado. A tentar clique por coordenadas...")
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(driver)
                actions.move_by_offset(200, 400).click().perform() # Clica onde o 1º canal costuma estar
        except Exception as e:
            print(f"Erro ao tentar clicar: {e}")

        print("A aguardar 45 segundos para o stream disparar na rede...")
        time.sleep(45)

        # Capturar o link da rede
        for request in driver.requests:
            url = request.url
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        if link_m3u8:
            print("SUCESSO! Link capturado.")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io/"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O player não disparou o link. O site pode estar a bloquear o IP do GitHub.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
