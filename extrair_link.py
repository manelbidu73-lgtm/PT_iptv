import requests
import re
import sys

def extrair():
    # URL que indicaste
    url_canal = "https://v3.sportssonline.click/channels/pt/sporttv1.php"
    
    # Headers para parecer um navegador real e evitar o erro 403
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://sportssonline.click/',
        'Origin': 'https://sportssonline.click'
    }

    try:
        session = requests.Session()
        # 1. Carrega a página do player
        response = session.get(url_canal, headers=headers, timeout=20)
        
        # O padrão do teu link (m3u8 com s= e e=)
        padrao_m3u8 = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        
        # Limpa barras invertidas que o JavaScript usa para esconder o link
        html_limpo = response.text.replace('\\/', '/')
        links = re.findall(padrao_m3u8, html_limpo)

        # 2. Se não estiver no HTML, o link está num script externo (estratégia DownloadHelper)
        if not links:
            scripts = re.findall(r'src=["\'](.+?\.js.*?)["\']', response.text)
            for js_url in scripts:
                if js_url.startswith('//'): js_url = 'https:' + js_url
                elif js_url.startswith('/'): js_url = "https://v3.sportssonline.click" + js_url
                try:
                    js_res = session.get(js_url, headers=headers, timeout=10)
                    links += re.findall(padrao_m3u8, js_res.text.replace('\\/', '/'))
                    if links: break
                except: continue

        if links:
            link_direto = links[0]
            # Adiciona o "disfarce" no link para o teu player IPTV não dar 403
            # O "|" (pipe) é o padrão usado para passar Referer em listas M3U
            m3u_final = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"{link_direto}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_final)
            print("Sucesso! Link capturado e guardado.")
        else:
            print("Erro: O link dinâmico não foi encontrado. O IP do GitHub pode estar bloqueado.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
