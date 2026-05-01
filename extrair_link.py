import requests
import re
import sys

def extrair():
    url_principal = "https://megatuga.io/canais-de-desporto"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://megatuga.io/'
    }

    try:
        session = requests.Session()
        print(f"1. A aceder à página principal...")
        res = session.get(url_principal, headers=headers, timeout=20)
        
        # O link m3u8 com s= e e=
        padrao_m3u8 = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        
        # Tenta procurar logo na página principal
        links = re.findall(padrao_m3u8, res.text.replace('\\/', '/'))

        if not links:
            print("2. Link não encontrado na principal. A procurar iframes...")
            # Procura por endereços de iframes (src="...")
            iframes = re.findall(r'iframe.+?src=["\'](.+?)["\']', res.text)
            
            for url_if in iframes:
                if 'ads' in url_if or 'facebook' in url_if: continue
                if url_if.startswith('//'): url_if = 'https:' + url_if
                
                print(f"3. A verificar iframe: {url_if[:50]}...")
                try:
                    res_if = session.get(url_if, headers={'Referer': url_principal}, timeout=10)
                    links = re.findall(padrao_m3u8, res_if.text.replace('\\/', '/'))
                    if links: break
                except: continue

        if links:
            link_direto = links[0]
            print("SUCESSO! Link encontrado.")
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_direto}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io/"
            )
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("ERRO: O link m3u8 está muito bem escondido ou requer JavaScript.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
