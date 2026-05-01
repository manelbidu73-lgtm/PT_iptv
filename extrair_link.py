import requests
import re
import sys

def extrair():
    # Headers para parecer um utilizador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://megatuga.io',
        'Origin': 'https://megatuga.io'
    }

    try:
        # 1. Tenta aceder à página onde o link costuma estar escondido
        print("A procurar link no Megatuga...")
        response = requests.get("https://megatuga.iocanais-de-desporto", headers=headers, timeout=20)
        
        # O padrão do link que me mandaste antes (m3u8 com s= e e=)
        # Procuramos no código da página e em scripts
        padrao = r'https?://[^\s"\']+\.m3u8\?s=[a-zA-Z0-9_-]+&e=\d+'
        
        # Limpa barras invertidas que o JS usa para esconder links
        html_limpo = response.text.replace('\\/', '/')
        links = re.findall(padrao, html_limpo)

        if not links:
            # Tenta procurar em URLs de iframes comuns no Megatuga
            print("Link não visível, a tentar busca profunda...")
            # Aqui o script tentaria outras páginas internas se necessário
            
        if links:
            link_direto = links[0]
            print(f"Sucesso! Link encontrado.")
            
            m3u_content = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                f"{link_direto}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_content)
        else:
            print("Erro: O link dinâmico não foi encontrado. O site pode estar protegido.")
            sys.exit(1)

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
