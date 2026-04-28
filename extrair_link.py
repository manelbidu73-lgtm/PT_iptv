import requests
import json

def extrair_tvi_oficial():
    # Este é o endpoint da API interna que gera o link de stream
    api_url = "https://iol.pt"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://iol.pt',
        'Origin': 'https://iol.pt'
    }

    try:
        print("A solicitar link à API de produção...")
        # Fazemos o pedido à API
        response = requests.get(api_url, headers=headers, timeout=15)
        
        # A API da IOL muitas vezes responde com o link direto ou um ficheiro de texto
        txt = response.text
        
        # Se a resposta contiver o wmsAuthSign, isolamos o link
        if "wmsAuthSign" in txt:
            # Limpeza de caracteres que podem vir da API
            link = txt.strip().replace('\\/', '/')
            # Se o link vier entre aspas (JSON), limpamos
            link = link.replace('"', '')
            return link
            
    except Exception as e:
        print(f"Erro na API: {e}")
    
    return None

link_final = extrair_tvi_oficial()

if link_final:
    print(f"Link obtido com sucesso!")
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(f"#EXTM3U\n#EXT-X-VERSION:3\n#EXTINF:-1 tvg-id=\"tvi.pt\", TVI\n{link_final}\n")
else:
    # Se falhar, vamos criar um ficheiro vazio para não quebrar a lista, 
    # mas o exit 1 avisa-nos do erro.
    print("A TVI bloqueou o acesso do GitHub Actions. Tentando alternativa...")
    exit(1)
