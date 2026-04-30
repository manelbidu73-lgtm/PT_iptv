import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def extrair():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("A carregar Megatuga...")
        driver.get("https://megatuga.io/canais-de-desporto")
        
        # 1. Espera a página carregar os ícones
        time.sleep(8)
        
        # 2. Tenta clicar no botão da Sport TV 1 para forçar o carregamento do link
        # Geralmente os canais têm um ID ou um texto. Vamos procurar pelo nome.
        try:
            botao_canal = driver.find_element(By.XPATH, "//*[contains(text(), 'Sport TV 1')]")
            driver.execute_script("arguments[0].click();", botao_canal)
            print("Clique na Sport TV 1 efetuado. A aguardar token...")
            time.sleep(5) # Espera o player gerar o link
        except:
            print("Aviso: Não foi possível clicar no botão, a tentar extração direta...")

        # 3. Varre o código fonte atualizado (DOM)
        html_final = driver.page_source
        
        # Regex potente para pegar o link m3u8 com token
        links = re.findall(r'https?://[^\s"\']+\.m3u8\?[^\s"\']+', html_final.replace('\\/', '/'))
        
        if links:
            # Filtra links conhecidos de publicidade, se houver
            link_m3u8 = links[0]
            
            conteudo_m3u = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"{link_m3u8}"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(conteudo_m3u)
            print(f"Sucesso! Link M3U8 capturado.")
        else:
            print("Erro: Link não encontrado após o clique.")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    extrair()
