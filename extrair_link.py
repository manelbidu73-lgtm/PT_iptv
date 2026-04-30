import requests
import re
import sys

def extrair():
    url_fonte = "https://v3.sportssonline.click/channels/pt/sporttv1.php"
    
    # Simula um iPhone para o site entregar o link mais facilmente
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
        'Referer': 'https://sportssonline.click',
        'Accept': '*/*'
    }

    try:
        session = requests.Session()
        response = session.get(url_fonte, headers=headers, timeout=20)
        
        # Procura o padrão s= e e= que nos deste
        # Aumentamos a flexibilidade da procura (Regex)
        padrao = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        
        # Limpamos o código de barras invertidas antes de procurar
        html_limpo = response.text.replace('\\/', '/')
        links = re.findall(padrao, html_limpo)

        # Se não encontrar no HTML principal, procura dentro de scripts
        if not links:
            print("Tentando busca profunda em scripts...")
            scripts = re.findall(r'<script src=["\'](.+?)["\']', response.text)
            for s_url in scripts:
                if 'http' not in s_url: s_url = "https://sportssonline.click" + s_url
                try:
                    s_res = session.get(s_url, headers=headers, timeout=10)
                    links += re.findall(padrao, s_res.text.replace('\\/', '/'))
                except: continue

        if links:
            link_direto = links[0]
            m3u_content = (
                "#EXTM3U\n"
                f"#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X)\n"
                f"#EXTVLCOPT:http-referrer=https://sportssonline.click\n"
                f"{link_direto}|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X)&Referer=https://sportssonline.click"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print(f"Sucesso! Link capturado.")
        else:
            print("Erro: O link ainda nao esta visivel. O site pode ter bloqueado o acesso.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
