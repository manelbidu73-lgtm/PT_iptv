import requests
import re
import json

def extrair_tvi():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://tviplayer.iol.pt/',
        'Origin': 'https://tviplayer.iol.pt'
    }

    # Método 1: API de Playlist Direta (Mais fiável para bots)
    try:
        print("Tentando Método 1: API de Playlist...")
        api_url = "https://iol.pt"
        res = requests.get(api_url, headers=headers, timeout=10)
        # Procura o link m3u8 com o token wmsAuthSign
        match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', res.text)
        if match:
            return match.group(0).replace('\\/', '/')
    except Exception as e:
        print(f"Erro no Método 1: {e}")

    # Método 2: Scraping da Página de Direto
    try:
        print("Tentando Método 2: Página de Direto...")
        pg_url = "https://tviplayer.iol.pt/direto"
        res = requests.get(pg_url, headers=headers, timeout=10)
        # Procura no código fonte da página
        match = re.search(r'videoUrl["\']\s*:\s*["\']([^"\']+\.m3u8\?wmsAuthSign=[^"\']+)["\']', res.text)
        if not match:
            match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', res.text)
        
        if match:
            return match.group(1 if len(match.groups()) > 0 else 0).replace('\\/', '/')
    except Exception as e:
        print(f"Erro no Método 2: {e}")

    return None

link = extrair_tvi()

if link:
    print(f"Link capturado: {link}")
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"tvi.pt\", TVI\n{link}\n")
else:
    print("Falha total: O token não foi encontrado em nenhuma fonte.")
    exit(1)
