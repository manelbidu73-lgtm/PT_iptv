import requests
import re
import os

# URL da página
url_pagina = "http://sportstvhdonline.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'http://sportstvhdonline.com'
}

try:
    if not os.path.exists("canais"):
        os.makedirs("canais")

    response = requests.get(url_pagina, headers=headers, timeout=15)
    # Procura o link que termina em .m3u8
    busca = re.search(r'(https?://[^\s"\'<> ]+\.m3u8[^\s"\'<> ]*)', response.text)
    
    if busca:
        link_final = busca.group(1)
        with open("canais/sporttv.m3u8", "w") as f:
            f.write("#EXTM3U\n")
            f.write("#EXTINF:-1, SportTV Online\n")
            f.write(link_final)
        print("Sucesso!")
    else:
        print("Link não encontrado.")
except Exception as e:
    print(f"Erro: {e}")
