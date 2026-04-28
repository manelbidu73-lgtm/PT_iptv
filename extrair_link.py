import requests
import re
import os

# Configurações de headers para evitar deteção de bot
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://iol.pt',
    'Origin': 'https://iol.pt'
}

class StreamExtractor:
    def __init__(self):
        self.results = {}

    def extract_tvi(self):
        """Extrai o token dinâmico da TVI Direto."""
        url_web = "https://iol.ptdireto/TVI"
        try:
            response = requests.get(url_web, headers=HEADERS, timeout=15)
            # Procura por URLs .m3u8 dentro do código fonte ou scripts carregados
            match = re.search(r'https?://[^\s"\']+\.m3u8\?[^\s"\']+', response.text)
            if match:
                self.results['TVI'] = match.group(0)
                print("[+] TVI link extraído com sucesso.")
            else:
                print("[-] TVI: Link m3u8 não encontrado.")
        except Exception as e:
            print(f"[-] Erro na TVI: {e}")

    def save_m3u(self, filename="playlist.m3u"):
        """Gera o ficheiro final com os links atualizados."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for name, url in self.results.items():
                f.write(f"#EXTINF:-1,{name}\n{url}\n")
        print(f"[!] Ficheiro {filename} guardado.")

if __name__ == "__main__":
    extractor = StreamExtractor()
    extractor.extract_tvi()
    # Podes adicionar extractor.extract_rtp(), etc.
    extractor.save_m3u()
    
