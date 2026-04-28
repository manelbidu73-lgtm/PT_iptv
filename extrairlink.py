import requests
import re
import os

url_pagina = "http://sportstvhdonline.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'http://sportstvhdonline.com'
}

def extrair():
    try:
        if not os.path.exists("canais"):
            os.makedirs("canais")

        print(f"A analisar: {url_pagina}")
        sessao = requests.Session()
        res = sessao.get(url_pagina, headers=headers, timeout=20)
        
        # 1. Tentar encontrar links .m3u8 no código principal
        links = re.findall(r'(https?://[^\s"\'<> ]+\.m3u8[^\s"\'<> ]*)', res.text)
        
        # 2. Se não encontrar, procurar por iFrames
        if not links:
            iframes = re.findall(r'iframe.*?src=["\'](.*?)["\']', res.text)
            for frame_url in iframes:
                if "http" not in frame_url:
                    if frame_url.startswith("//"):
                        frame_url = "http:" + frame_url
                    else:
                        frame_url = "http://sportstvhdonline.com" + frame_url
                
                print(f"A analisar iFrame: {frame_url}")
                try:
                    res_f = sessao.get(frame_url, headers=headers, timeout=15)
                    links += re.findall(r'(https?://[^\s"\'<> ]+\.m3u8[^\s"\'<> ]*)', res_f.text)
                except:
                    continue

        if links:
            # CORREÇÃO: Pegar o primeiro item da lista e limpar barras
            link_final = links[0].replace("\\", "")
            
            with open("canais/sporttv.m3u8", "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXTINF:-1, SportTV HD\n")
                f.write(link_final)
            print(f"Sucesso! Link encontrado e guardado.")
        else:
            print("Não foi possível encontrar o stream.")
            exit(1)

    except Exception as e:
        print(f"Erro: {e}")
        exit(1)

if __name__ == "__main__":
    extrair()
