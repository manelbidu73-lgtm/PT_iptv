import requests
import re
import os
import sys

# URL Alvo: Podes trocar para o que quiseres (TVI, SportTV, etc.)
url_alvo = "https://tviplayer.iol.pt/direto" 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://tviplayer.iol.pt/',
    'Accept-Language': 'pt-PT,pt;q=0.9'
}

def limpar_link(link):
    """Limpa barras invertidas e aspas de links extraídos de scripts"""
    return link.replace("\\/", "/").replace("\\", "").replace('"', '').replace("'", "")

def extrair_universal():
    try:
        # Garante que a pasta m3u8s existe (essencial para o GitHub)
        if not os.path.exists("m3u8s"):
            os.makedirs("m3u8s")

        print(f"--- A iniciar pesca profunda em: {url_alvo} ---")
        sessao = requests.Session()
        sessao.headers.update(headers)
        
        # 1. Tenta ler a página principal
        res = sessao.get(url_alvo, timeout=20)
        
        # 2. Procura links .m3u8 (com ou sem tokens) no código-fonte
        # Esta expressão regular é a mais potente para links dinâmicos
        links = re.findall(r'https?://[^\s"\'<> ]+\.m3u8(?:\?[^\s"\'<> ]+)?', res.text)
        
        # 3. Se não encontrar, procura por iFrames (técnica para sites de desporto)
        if not links:
            print("Link direto não encontrado. A vasculhar iFrames...")
            iframes = re.findall(r'iframe.*?src=["\'](.*?)["\']', res.text)
            for f_url in iframes:
                if f_url.startswith("//"): f_url = "https:" + f_url
                if not f_url.startswith("http"): f_url = "https://iol.pt" + f_url
                
                try:
                    print(f"A analisar janela escondida: {f_url}")
                    res_f = sessao.get(f_url, timeout=15)
                    links += re.findall(r'https?://[^\s"\'<> ]+\.m3u8(?:\?[^\s"\'<> ]+)?', res_f.text)
                except:
                    continue

        # 4. Se ainda assim não encontrar, tenta procurar variáveis de vídeo (source)
        if not links:
            links = re.findall(r'source:\s*["\'](http[^\s"\']+)["\']', res.text)

        if links:
            # Filtra links duplicados e limpa o primeiro encontrado
            link_final = limpar_link(links[0])
            
            # Define o nome do ficheiro conforme o canal
            nome = "tvi.m3u8" if "tvi" in url_alvo else "canal_auto.m3u8"

            with open(f"m3u8s/{nome}", "w") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, Canal Automático\n")
                f.write(link_final)
            
            print(f"✅ SUCESSO! Link pescado: {link_final}")
        else:
            print("❌ ERRO: Não foi possível encontrar nenhum stream.")
            sys.exit(1)

    except Exception as e:
        print(f"⚠️ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extrair_universal()
