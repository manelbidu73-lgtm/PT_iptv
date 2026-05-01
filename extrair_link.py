import requests
import re
import sys

def extrair():
    # URL exatamente como indicaste
    url_fonte = "https://megatuga.io/canais-de-desporto"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://megatuga.io/',
        'Origin': 'https://megatuga.io'
    }

    try:
        print(f"A aceder a: {url_fonte}")
        session = requests.Session()
        # Faz a requisição à página
        response = session.get(url_fonte, headers=headers, timeout=20)
        
        # Procura o padrão do link .m3u8 que o teu Video DownloadHelper apanha
        padrao = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        
        # Limpa o HTML (remove as barras invertidas do JavaScript)
        html_limpo = response.text.replace('\\/', '/')
        links = re.findall(padrao, html_limpo)

        if links:
            link_direto = links[0] # Paga o primeiro link encontrado
            print("Sucesso! Link m3u8 encontrado.")
            
            # Cria o conteúdo do ficheiro M3U
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_direto}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io/"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: O link com token s= e e= não está no código desta página.")
            print("Dica: O Megatuga pode estar a carregar o player dentro de um iframe separado.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro ao ligar ao site: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
