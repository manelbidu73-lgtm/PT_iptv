import requests

def extrair_definitivo():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Tentativa 1: API IOL (Original)
    try:
        print("Tentando API IOL...")
        r = requests.get("https://iol.pt", headers=headers, timeout=10)
        if "wmsAuthSign" in r.text:
            link = r.text.strip().replace('"', '').replace('\\/', '/')
            if link.startswith("http"): return link
    except: pass

    # Tentativa 2: Backup Direto da M3UPT (LITUATUI)
    # Vamos descarregar o ficheiro que ele já validou
    try:
        print("Tentando Backup M3UPT...")
        r = requests.get("https://githubusercontent.com", timeout=10)
        lines = r.text.splitlines()
        for line in lines:
            if "wmsAuthSign" in line and line.startswith("http"):
                return line.strip()
    except: pass

    return None

link = extrair_definitivo()

if link:
    print(f"✅ Link encontrado!")
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        # Formato exato para listas IPTV
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXTINF:-1 tvg-id=\"TVI\" tvg-logo=\"https://m3upt.com\", TVI\n")
        f.write(f"{link}\n")
else:
    print("❌ Falha crítica: Nenhuma fonte disponível.")
    exit(1)
