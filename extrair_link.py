import requests
import re
import time

def extrair_blindado():
    # 1. Configuração de "Disfarce" (Smart TV / Android TV)
    # Este User-Agent e Referer fazem o servidor da TVI pensar que é uma App Oficial
    headers = {
        'User-Agent': 'TVIPlayer/3.0.4 (Linux; Android 10; BRAVIA 4K VH2) AppleWebkit/537.36',
        'Referer': 'https://iol.pt',
        'Origin': 'https://iol.pt',
        'Accept': '*/*',
        'X-Requested-With': 'com.iol.tviplayer'
    }

    # 2. Ordem de busca (Do mais direto para o backup)
    fontes = [
        "https://iol.pt",      # API Direta
        "https://iol.ptdireto",           # Página Web
        "https://m3upt.com",                # Proxy M3UPT
        "https://githubusercontent.com" # Backup Final
    ]

    for url in fontes:
        try:
            print(f"A testar fonte: {url}")
            # Timeout curto para não prender a Action se o IP do GitHub estiver bloqueado
            response = requests.get(url, headers=headers, timeout=8)
            
            if response.status_code == 200:
                # Regex potente: procura URLs m3u8 que contenham o token wmsAuthSign
                # Funciona mesmo se o link estiver escondido em JavaScript ou JSON
                match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', response.text)
                
                if match:
                    link = match.group(0).replace('\\/', '/') # Limpa barras de JSON
                    print(f"✅ Token capturado via: {url}")
                    return link
        except Exception as e:
            print(f"⚠️ Falha na fonte {url}: {e}")
            continue # Tenta a próxima fonte
            
    return None

# Início do processo
print("🚀 A iniciar extração blindada da TVI...")
link_final = extrair_blindado()

if link_final:
    # Gerar o ficheiro m3u8 com tags de alta compatibilidade
    conteudo_final = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,RESOLUTION=1280x720\n"
        f"{link_final}\n"
    )
    
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(conteudo_final)
    print("💎 Ficheiro tvi.m3u8 atualizado e pronto!")
else:
    print("❌ Erro: A TVI bloqueou todas as rotas. Verifique se o site está online.")
    exit(1)
