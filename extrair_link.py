import requests
import re

def extrair_blindado():
    # Headers de Smart TV para evitar bloqueios
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://iol.pt'
    }

    # URLs COMPLETOS (Corrigidos para evitar NameResolutionError)
    fontes = [
        "https://iol.pt",
        "https://iol.ptdireto",
        "https://githubusercontent.com" # Backup real
    ]

    for url in fontes:
        try:
            print(f"A testar fonte: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Procura o link .m3u8 com o token wmsAuthSign
                match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', response.text)
                
                if match:
                    link = match.group(0).replace('\\/', '/')
                    print(f"✅ Sucesso via: {url}")
                    return link
        except Exception as e:
            print(f"⚠️ Erro na fonte {url}: {e}")
            
    return None

print("🚀 A iniciar extração final...")
link_final = extrair_blindado()

if link_final:
    conteudo = f"#EXTM3U\n#EXT-X-VERSION:3\n#EXTINF:-1 tvg-id=\"tvi.pt\", TVI\n{link_final}\n"
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("💎 Ficheiro tvi.m3u8 atualizado!")
else:
    print("❌ Falha: Nenhuma fonte respondeu com um token válido.")
    exit(1)
