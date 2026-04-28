import requests
import re

def extrair_link_tvi():
    # URL da página oficial de direto
    url_pagina = "https://iol.pt"
    
    # Headers para simular um navegador real e evitar bloqueios
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://iol.pt'
    }
    
    try:
        # 1. Aceder à página para capturar o link do manifesto que contém o token
        response = requests.get(url_pagina, headers=headers, timeout=15)
        
        # 2. Expressão regular para encontrar o link .m3u8 com o wmsAuthSign
        # Este padrão procura o URL que a TVI usa no seu player dinâmico
        match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', response.text)
        
        if match:
            return match.group(0)
            
        # 3. Caso falhe, tenta a API direta como plano B
        api_fallback = requests.get("https://iol.pt", headers=headers, timeout=10)
        match_fallback = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', api_fallback.text)
        
        if match_fallback:
            return match_fallback.group(0)
            
    except Exception as e:
        print(f"Erro durante a extração: {e}")
    
    return None

# Execução do processo
link_encontrado = extrair_link_tvi()

if link_encontrado:
    # Criar o conteúdo do ficheiro final com o nome exato tvi.m3u8
    # Adicionamos tags básicas de IPTV para melhor compatibilidade
    conteudo_m3u = (
        "#EXTM3U\n"
        "#EXTINF:-1 tvg-id=\"tvi.pt\" tvg-logo=\"https://m3upt.com\" group-title=\"Canais Portugueses\", TVI\n"
        f"{link_encontrado}\n"
    )
    
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(conteudo_m3u)
    
    print("Sucesso: Ficheiro tvi.m3u8 gerado com o novo token!")
else:
    print("Erro: Não foi possível capturar o token da TVI.")
    exit(1) # Força a GitHub Action a mostrar erro se falhar
