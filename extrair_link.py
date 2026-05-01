import sys
import os
from seleniumbase import SB

def extrair():
    link_m3u8 = None
    # Adicionamos wire=True para o SeleniumBase ativar o monitor de rede
    with SB(uc=True, xvfb=True, wire=True) as sb:
        try:
            print("A abrir Megatuga...")
            sb.open("https://megatuga.io/canais-de-desporto")
            sb.sleep(15)

            print("A procurar e clicar na Sport TV 1...")
            # Tenta clicar no link que contém o texto Sport TV 1
            if sb.is_element_visible('a:contains("Sport TV 1")'):
                sb.click('a:contains("Sport TV 1")')
                print("Clique efetuado.")
            else:
                print("Aviso: Botão não visível, a tentar captura direta...")

            print("A aguardar 45 segundos para o stream disparar...")
            sb.sleep(45)

            # Agora o 'requests' já vai existir porque usamos wire=True
            print("A analisar pedidos de rede...")
            for request in sb.driver.requests:
                url = request.url
                if '.m3u8?s=' in url and '&e=' in url:
                    link_m3u8 = url
                    break

            if link_m3u8:
                print(f"SUCESSO! Link: {link_m3u8[:50]}...")
                m3u_content = (
                    "#EXTM3U\n"
                    "#EXTINF:-1 tvg-id=\"SportTV1\",SPORT TV 1\n"
                    f"{link_m3u8}|User-Agent=Mozilla/5.0&Referer=https://megatuga.io"
                )
                with open("sporttv1.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u_content)
            else:
                print("ERRO: O link m3u8 não apareceu na rede.")
                sys.exit(1)

        except Exception as e:
            print(f"Erro Crítico: {e}")
            sys.exit(1)

if __name__ == "__main__":
    extrair()
