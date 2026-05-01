import sys
from seleniumbase import SB

def extrair():
    link_m3u8 = None
    # Usamos o contexto SB (SeleniumBase) com modo UC (Undetected) e XVFB
    with SB(uc=True, xvfb=True) as sb:
        try:
            print("A abrir Megatuga com proteção avançada...")
            sb.open("https://megatuga.io/canais-de-desporto")
            sb.sleep(20)

            print("A tentar ativar o player da Sport TV 1...")
            # Clica no canal usando um seletor seguro
            sb.click_if_visible('a:contains("Sport TV 1")')
            sb.sleep(45) # Tempo para o stream carregar

            # Captura os links da rede
            print("A analisar pedidos de rede...")
            for request in sb.driver.requests:
                url = request.url
                if '.m3u8?s=' in url and '&e=' in url:
                    link_m3u8 = url
                    break

            if link_m3u8:
                print("SUCESSO!")
                m3u_content = f"#EXTM3U\n#EXTINF:-1,Sport TV 1\n{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
                with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u_content)
            else:
                print("ERRO: Link não detetado.")
                sys.exit(1)

        except Exception as e:
            print(f"Erro: {e}")
            sys.exit(1)

if __name__ == "__main__":
    extrair()
