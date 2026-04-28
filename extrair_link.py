import requests
import re
import os
import sys

url_alvo = "https://iol.pt" 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://tviplayer.iol.pt/',
    'Accept-Language': 'pt-PT,pt;q=0.9'
}

def limpar_link(link):
    """Limpa barras invertidas sem destruir o token (?wmsAuthSign)"""
    return link.replace("\\/", "/").replace('\\"', '').replace('"', '').replace("'", "")

def extrair_universal():
    try:
        if not os.path.exists("m3u8s"):
            os.makedirs("m3u8s")

        print(f"--- A iniciar pesca profunda em: {url_alvo} ---")
        sessao = requests.Session()
        sessao.headers.update(headers)
        
        res = sessao.get(url_alvo, timeout=20)
        
        # AJUSTE: Procura especificamente o campo videoUrl que já contém o token
        links = re.findall(r'"videoUrl"\s*:\s*"(https?://[^"]+)"', res.text)
        
        if not links:
            # Segunda tentativa: procurar qualquer link m3u8 que tenha o ponto de interrogação do token
            links = re.findall(r'https?://[^\s"\'<> ]+\.m3u8\?[^\s"\'<> ]+', res.text)

        if links:
            link_final = limpar_link(links[0])
            
            nome = "tvi.m3u8" # Forçamos o nome correto

            with open(f"m3u8s/{nome}", "w") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, TVI Direto\n")
                # IMPORTANTE: O player precisa do User-Agent para aceitar o token
                f.write(f"{link_final}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}")
            
            print(f"✅ SUCESSO! Link capturado com token.")
        else:
            print("❌ ERRO: Não encontrei o link com a assinatura wmsAuthSign.")
            sys.exit(1)

    except Exception as e:
        print(f"⚠️ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair_universal()
            
