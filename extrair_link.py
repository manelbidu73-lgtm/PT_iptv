import time
import sys
import re
import undetected_chromedriver as uc
from seleniumwire import webdriver # Usamos selenium-wire para capturar a rede

def extrair():
    # Opções para parecer um browser real
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Inicia o browser indetetável com suporte a monitorização de rede
    driver = uc.Chrome(options=options, seleniumwire_options={})
    
    try:
        print("A abrir Megatuga com bypass de deteção...")
        driver.get("https://megatuga.io/canais-de-desporto")
        time.sleep(20)

        # Tentar clicar no canal pelo texto ou pela posição
        print("A tentar ativar o player...")
        try:
            # Tenta clicar no primeiro elemento que pareça a Sport TV 1
            elementos = driver.find_elements("xpath", "//a[contains(., 'Sport TV 1')]")
            if elementos:
                driver.execute_script("arguments[0].click();", elementos[0])
                print("Clique efetuado!")
            else:
                # Se não achar o botão, clica no centro do ecrã onde o player costuma estar
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(driver)
                actions.move_by_offset(500, 500).click().perform()
                print("Clique forçado no centro do ecrã.")
        except:
            pass

        print("A aguardar 40 segundos para o link aparecer na rede...")
        time.sleep(40)

        link_m3u8 = None
        for request in driver.requests:
            url = request.url
            if '.m3u8?s=' in url and '&e=' in url:
                link_m3u8 = url
                break

        if link_m3u8:
            print("SUCESSO!")
            m3u_content = f"#EXTM3U\n#EXTINF:-1,Sport TV 1\n{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O link não foi disparado. O site bloqueou o IP do GitHub.")
            sys.exit(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
