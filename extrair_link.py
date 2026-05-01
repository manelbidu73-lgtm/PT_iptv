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
        print("A abrir Megatuga...")
        driver.get("https://megatuga.io")
        time.sleep(20)

        # MÉTODO 1: Procurar todos os links e clicar no que parece ser a Sport TV 1
        print("A varrer a página à procura do canal...")
        clicou = False
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            texto = link.text.lower()
            href = link.get_attribute("href").lower() if link.get_attribute("href") else ""
            
            if ("sport" in texto and "1" in texto) or ("sport-tv-1" in href):
                print(f"Canal encontrado! Texto: {texto} | Link: {href}")
                driver.execute_script("arguments[0].scrollIntoView();", link)
                driver.execute_script("arguments[0].click();", link)
                clicou = True
                break

        if not clicou:
            print("Aviso: Não encontrei o link pelo texto. A tentar clique forçado no topo da lista...")
            driver.execute_script("window.scrollTo(0, 500);")
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(driver).move_by_offset(300, 500).click().perform()

        print("A aguardar 50 segundos para o sinal disparar...")
        time.sleep(50)

        # Capturar o link da rede (m3u8 com s= e e=)
        for request in driver.requests:
            url = request.url
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        if link_m3u8:
            print(f"SUCESSO! Link pescado: {link_m3u8[:60]}...")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O link m3u8 não apareceu na rede. O IP do GitHub pode estar bloqueado.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
