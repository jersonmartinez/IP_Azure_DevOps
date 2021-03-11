import queue
import urllib.request
import re
from urllib.parse import urljoin


def descargar(pagina):
    try:
        peticion = urllib.request.Request(pagina)
        html = urllib.request.urlopen(peticion).read()
        print("[*] Descarga OK >>", pagina)
    except:
        print('[!] Error descargando', pagina)
        return None

    return html


def rastrearEnlaces(pagina):
    buscaEnlaces = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    cola = queue.Queue()
    cola.put(pagina)
    visitados = [pagina]
    print("Buscando enlaces en", pagina)
    while (cola.qsize() > 0):
        html = descargar(cola.get())
        if html == None:
            continue
        enlaces = buscaEnlaces.findall(str(html))
        for enlace in enlaces:
            enlace = urljoin(pagina, str(enlace))
            if(enlace not in visitados):
                cola.put(enlace)
                visitados.append(enlace)


if __name__ == "__main__":
    url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    rastrearEnlaces(url)
