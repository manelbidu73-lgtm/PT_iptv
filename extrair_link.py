import requests
import re
import sys

def extrair():
    # URL da página que contém o player
    url_fonte = "https://v3.sportssonline.click/channels/pt/sporttv1.php"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://sportssonline.click',
        'Origin': 'https://sportssonline.click'
    }

    try:
        session = requests.Session()
        # 1. Aceder à página
        response = session.get(url_fonte, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 2. Procurar o padrão do link que me passaste usando Regex
        # Procura por links que terminam em .m3u8 e têm os parâmetros s= e e=
        padrao = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        links = re.findall(padrao, response.text.replace('\\/', '/'))

        if not links:
            # Se não achou no HTML, pode estar num iframe. Vamos procurar o src do iframe.
            iframes = re.findall(r'iframe.+?src=["\'](.+?)["\']', response.text)
            for iframe_url in iframes:
                if 'http' not in iframe_url: iframe_url = "https:" + iframe_url
                res_if = session.get(iframe_url, headers={'Referer': url_fonte})
                links += re.findall(padrao, res_if.text.replace('\\/', '/'))

        if links:
            link_direto = links[0] # Pega o primeiro link encontrado
            
            # Criar o ficheiro M3U
            conteudo = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"{link_direto}"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"Sucesso! Link capturado: {link_direto[:60]}...")
        else:
            print("Erro: Não foi possível encontrar o link com token s= e e=.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
