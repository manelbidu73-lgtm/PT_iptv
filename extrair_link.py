import requests
import re

def extrair_link_tvi():
    # URL principal que indicaste
    url = "https://tviplayer.iol.pt/direto"
    
    # Headers para parecer um acesso real de uma pessoa
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://tviplayer.iol.pt/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    
    try:
        print(f"A aceder a: {url}")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Expressão regular para capturar o link .m3u8 com o token wmsAuthSign
        # Esta regex limpa também escapes comuns (como \/) que o site usa no código
        match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', response.text)
        
        if match:
            link_limpo = match.group(0).replace('\\/', '/')
            return link_limpo
            
    except Exception as e:
        print(f"Erro ao processar a página: {e}")
            
    return None

# Processo de gravação
link_final = extrair_link_tvi()

if link_final:
    # Cria o ficheiro com o nome exato tvi.m3u8
    conteudo_m3u8 = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXTINF:-1 tvg-id=\"tvi.pt\" tvg-logo=\"https://m3upt.com\", TVI\n"
        f"{link_final}\n"
    )
    
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(conteudo_m3u8)
    print(f"Sucesso! Link extraído: {link_final}")
else:
    print("Erro: O token não foi encontrado na página da TVI.")
    exit(1)
