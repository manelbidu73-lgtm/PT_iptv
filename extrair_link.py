import requests

def extrair_definitivo():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Tentativa 1: API Direta da IOL
    try:
        print("Tentando API IOL (cdn.iol.pt)...")
        r = requests.get("https://iol.pt", headers=headers, timeout=10)
        if "wmsAuthSign" in r.text:
            # Limpa o link de aspas ou barras invertidas
            link = r.text.strip().replace('"', '').replace('\\/', '/')
            if link.startswith("http"): 
                return link
    except Exception as e: 
        print(f"Fonte 1 falhou: {e}")

    # Tentativa 2: Backup da M3UPT (URL COMPLETO E CORRETO)
    try:
        print("Tentando Backup M3UPT (://githubusercontent.com)...")
        # Este é o link completo para o ficheiro m3u do projeto M3UPT
        url_backup = "https://://githubusercontent.com/LITUATUI/M3UPT/main/M3U/TVI.m3u"
        r = requests.get(url_backup, timeout=10)
        
        lines = r.text.splitlines()
        for line in lines:
            # Se a linha contiver o token e começar por http, é o nosso link
            if "wmsAuthSign" in line and line.strip().startswith("http"):
                return line.strip()
    except Exception as e: 
        print(f"Fonte 2 falhou: {e}")

    return None

link = extrair_definitivo()

if link:
    print(f"✅ Link encontrado!")
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXTINF:-1 tvg-id=\"TVI\" tvg-logo=\"https://m3upt.com\", TVI\n")
        f.write(f"{link}\n")
else:
    print("❌ Falha crítica: Não foi possível obter o link.")
    exit(1)
