import requests
import re
import os

# URL que queres extrair (o que me deste)
url_alvo = "http://www.sportstvhdonline.com/index.php?canal=sporttv"

# Headers idênticos aos que o Thom usa para enganar o site
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'http://www.sportstvhdonline.com/',
    'Origin': 'http://www.sportstvhdonline.com'
}

def extrair_estilo_thom():
    try:
        # Garante que a pasta m3u8s existe (essencial para não dar erro)
        if not os.path.exists("m3u8s"):
            os.makedirs("m3u8s")

        print(f"A iniciar extração de: {url_alvo}")
        sessao = requests.Session()
        
        # 1. Acede à página principal para capturar cookies de sessão
        res = sessao.get(url_alvo, headers=headers, timeout=20)
        
        # 2. Procura o iFrame do player (técnica comum nestes sites)
        iframe_match = re.search(r'iframe.*?src=["\'](.*?)["\']', res.text)
        
        if iframe_match:
            player_url = iframe_match.group(1)
            if player_url.startswith("//"):
                player_url = "http:" + player_url
            
            print(f"A aceder ao player escondido: {player_url}")
            # Altera o referer para o player aceitar o pedido
            headers['Referer'] = url_alvo
            res_player = sessao.get(player_url, headers=headers, timeout=20)
            
            # 3. Procura o link .m3u8 final dentro do player
            # O Thom usa esta expressão regular para limpar barras invertidas de JS
            links = re.findall(r'["\'](https?://[^\s"\'<> ]+\.m3u8[^\s"\'<> ]*)["\']', res_player.text)
            
            if links:
                link_final = links[0].replace("\\", "")
                
                # 4. Grava o ficheiro na pasta m3u8s (igual ao repositório dele)
                with open("m3u8s/sporttv.m3u8", "w") as f:
                    f.write("#EXTM3U\n")
                    f.write("#EXTINF:-1, SportTV HD\n")
                    f.write(link_final)
                
                print(f"Sucesso! Link pescado: {link_final}")
                return

        print("Não foi possível encontrar o stream. O canal pode estar em pausa.")
        exit(1)

    except Exception as e:
        print(f"Erro no processo: {e}")
        exit(1)

if __name__ == "__main__":
    extrair_estilo_thom()
