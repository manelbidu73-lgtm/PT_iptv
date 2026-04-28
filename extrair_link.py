import requests
import re

def extrair_da_pagina_direto():
    url_pagina = "https://tviplayer.iol.pt/direto"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url_pagina, headers=headers)
        # O site da TVI guarda o link do stream numa variável JavaScript dentro do HTML
        # Procuramos por algo que comece por https e termine em .m3u8?wmsAuthSign=...
        match = re.search(r'https?://[^\s<>"\']+\.m3u8\?wmsAuthSign=[^\s<>"\']+', response.text)
        
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Erro ao ler a página: {e}")
    return None

link_final = extrair_da_pagina_direto()

if link_final:
    conteudo = f"#EXTM3U\n#EXTINF:-1 tvg-id=\"TVI\", TVI\n{link_final}"
    with open("tvi.m3u8", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("Sucesso: Link extraído da página direto!")
else:
    print("Não foi possível encontrar o link na página.")
