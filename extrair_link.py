import requests
import re
import os
import sys

# URL Alvo
url_alvo = "https://iol.pt" 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://iol.pt',
    'Accept-Language': 'pt-PT,pt;q=0.9'
}

def limpar_link(link):
    """Limpa apenas barras invertidas de JSON, mantendo os tokens (?wmsAuthSign=)"""
    return link.replace("\\/", "/").replace('\\"', '').replace('"', '').replace("'", "")

def extrair_universal():
    try:
        if not os.path.exists("m3u8s"):
            os.makedirs("m3u8s")

        print(f"--- A iniciar pesca profunda em: {url_alvo} ---")
        sessao = requests.Session()
        sessao.headers.update(headers)
        
        res = sessao.get(url_alvo, timeout=20)
        
        # ALTERAÇÃO AQUI: Expressão ajustada para capturar o link COM o token wmsAuthSign
        links = re.findall(r'https?://[^\s"\'<> ]+?\.m3u8\?[^\s"\'<> ]+', res.text)
        
        if not links:
            print("Link com token não encontrado. A vasculhar iFrames...")
            iframes = re.findall(r'iframe.*?src=["\'](.*?)["\']', res.text)
            for f_url in iframes:
                if f_url.startswith("//"): f_url = "https:" + f_url
                try:
                    res_f = sessao.get(f_url, timeout=15)
                    # Procura também nos iframes links que contenham o sinal "?"
                    links += re.findall(r'https?://[^\s"\'<> ]+?\.m3u8\?[^\s"\'<> ]+', res_f.text)
                except:
                    continue

        if links:
            # Pegamos o primeiro link e limpamos as barras do JSON
            link_final = limpar_link(links[0])
            
            nome = "tvi.m3u8" if "tvi" in url_alvo.lower() else "canal_auto.m3u8"

            with open(f"m3u8s/{nome}", "w") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, TVI Direto\n")
                # Adicionamos os headers ao link para garantir que o player é aceite
                f.write(f"{link_final}|User-Agent={headers['User-Agent']}&Referer={headers['Referer']}")
            
            print(f"✅ SUCESSO! Link pescado com token: {link_final}")
        else:
            print("❌ ERRO: Não foi possível encontrar o link com token de segurança.")
            sys.exit(1)

    except Exception as e:
        print(f"⚠️ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair_universal()
    
