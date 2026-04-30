import requests
import re
import sys

def extrair():
    # URL principal onde estão os canais
    url_pai = "https://megatuga.io/canais-de-desporto"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://megatuga.io',
        'Accept-Language': 'pt-PT,pt;q=0.9'
    }

    try:
        session = requests.Session()
        # 1. Aceder à página principal para validar cookies
        main_res = session.get(url_pai, headers=headers, timeout=15)
        
        # 2. Procurar especificamente pela Sport TV 1 no código
        # O site costuma carregar um player externo ou um endpoint de API
        # Vamos buscar qualquer link m3u8 que apareça no código carregado
        html_content = main_res.text
        
        # Regex melhorada para capturar links m3u8 dentro de scripts ou iframes
        padrao_m3u8 = r'(https?://[^\s"\']+\.m3u8\?[^\s"\']+)'
        links = re.findall(padrao_m3u8, html_content)

        if not links:
            # Tentar procurar por ficheiros de configuração do player (ex: player.php ou get_source.php)
            # Se o site usa iframe, precisamos de encontrar o src do iframe primeiro
            if 'sport-tv-1' in html_content.lower():
                print("Canal identificado, a tentar extrair token dinâmico...")
                # Aqui o script tenta "adivinhar" o link baseado na estrutura comum desses sites
                # mas vamos manter a procura por regex que é mais segura.

        if links:
            # Filtramos para garantir que pegamos o da Sport TV (normalmente o primeiro ou com 'live')
            link_final = links[0].replace('\\/', '/')
            
            conteudo_m3u = (
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"SportTV1\" tvg-name=\"SPORT TV 1\" tvg-logo=\"https://wikimedia.org\",SPORT TV 1\n"
                f"{link_final}"
            )
            
            with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                f.write(conteudo_m3u)
            print("Sucesso: sporttv1.m3u atualizado.")
        else:
            print("Erro: O link com token não está visível no HTML inicial.")
            # Se falhar aqui, o site está a esconder o link atrás de um clique (JavaScript)
            sys.exit(1)

    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair()
