import requests
import re
import sys

def extrair():
    # URL direta do canal
    url_fonte = "https://v3.sportssonline.click/channels/pt/sporttv1.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://sportssonline.click',
        'Origin': 'https://sportssonline.click'
    }

    try:
        session = requests.Session()
        response = session.get(url_fonte, headers=headers, timeout=15)
        
        # Procura o link m3u8 no código da página
        # O padrao procura o link que me enviaste antes (com s= e e=)
        padrao = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        links = re.findall(padrao, response.text.replace('\\/', '/'))

        if links:
            link_direto = links[0] # Pega o primeiro link encontrado
            
            # FORMATO ESPECIAL PARA EVITAR ERRO 403 NO PLAYER
            # O link termina com |User-Agent... para a App de IPTV se disfarçar
            m3u_content = (
                "#EXTM3U\n"
                f"#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n"
                f"#EXTVLCOPT:http-referrer=https://sportssonline.click\n"
                f"{link_direto}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://sportssonline.click"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print(f"Sucesso! Link capturado e formatado.")
        else:
            print("Erro: Nao foi possivel encontrar o link m3u8 no site.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()

