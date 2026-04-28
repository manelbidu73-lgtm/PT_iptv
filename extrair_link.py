import requests
import re

def obter_token():
    # Headers para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://iol.pt'
    }

    # Tentativa 1: API Direta da IOL
    try:
        print("A testar Fonte 1 (API)...")
        r = requests.get("https://iol.pt", headers=headers, timeout=10)
        m = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', r.text)
        if m: return m.group(0).replace('\\/', '/')
    except: print("Fonte 1 falhou.")

    # Tentativa 2: Página de Direto
    try:
        print("A testar Fonte 2 (Página)...")
        r = requests.get("https://iol.ptdireto", headers=headers, timeout=10)
        m = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', r.text)
        if m: return m.group(0).replace('\\/', '/')
    except: print("Fonte 2 falhou.")

    # Tentativa 3: Backup da Comunidade (M3UPT)
    try:
        print("A testar Fonte 3 (Backup M3UPT)...")
        r = requests.get("https://githubusercontent.com", timeout=10)
        m = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', r.text)
        if m: return m.group(0).replace('\\/', '/')
    except: print("Fonte 3 falhou.")

    return None

link = obter_token()

if link:
    print(f"✅ Sucesso: {link}")
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1 tvg-id=\"tvi.pt\", TVI\n{link}\n")
else:
    print("❌ Erro: Não foi possível obter o token em nenhuma fonte.")
    exit(1)
