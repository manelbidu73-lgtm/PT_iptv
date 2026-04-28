import requests
import re

def get_token():
    url = "https://tviplayer.iol.pt/direto"
    h = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=h, timeout=10)
        # Esta linha procura o link com o token wmsAuthSign
        match = re.search(r'(https://[^\s"\']+\.m3u8\?wmsAuthSign=[^\s"\']+)', r.text)
        return match.group(1) if match else None
    except: return None

link = get_token()
if link:
    with open("tvi.m3u8", "w") as f:
        f.write(f"#EXTM3U\n#EXTINF:-1, TVI\n{link}")
        
