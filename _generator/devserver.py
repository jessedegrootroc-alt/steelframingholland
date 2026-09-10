# -*- coding: utf-8 -*-
"""Lokale server die comprimeert en cache-headers stuurt, zoals een echte host.

    python3 _generator/devserver.py 8081
    python3 _generator/devserver.py 8081 --lan     # ook bereikbaar op je telefoon

Waarom dit er is: `python3 -m http.server` comprimeert niet en stuurt geen
cache-headers. Meet je Lighthouse daartegen, dan mis je twee dingen die elke
host wel doet, en kom je ongeveer vijf punten te laag uit. Deze server bootst na
wat Apache, nginx, Netlify en Cloudflare standaard doen, zodat de meting klopt
met wat een bezoeker straks krijgt.

## Byte-ranges, en waarom dat hier niet optioneel is

`SimpleHTTPRequestHandler` negeert de kop `Range` en stuurt altijd het hele
bestand met status 200. Voor html en css maakt dat niets uit, maar **Safari op
iOS speelt een mp4 niet als de server geen 206 met `Content-Range`
teruggeeft.** De herofilm bleef daardoor op een iPhone staan waar hij op
desktop en op Android gewoon liep, en de foto eronder bleef in beeld; aan de
site was niets mis. Deze server stuurt nu 206 en zet `Accept-Ranges: bytes`,
en spreekt HTTP/1.1 in plaats van 1.0, zodat de film ook op een iPhone speelt.

Ook een echte host moet dit doen. Apache, nginx, Netlify en Cloudflare doen het
standaard; zet je de site ergens anders neer, controleer het dan:

    curl -sI -H 'Range: bytes=0-1023' <url>/assets/video/sfh-hero.mp4

Dat moet `HTTP/1.1 206 Partial Content` zijn met een `Content-Range`. Komt er
200 met de volle `Content-Length`, dan speelt de film niet op een iPhone.

## Bereikbaar maken voor een telefoon

Standaard luistert hij op 127.0.0.1, dus alleen op deze computer. Met `--lan`
luistert hij op alle adressen en wordt het adres geprint dat je op je telefoon
kunt openen. Dat zet deze map wel open voor iedereen op hetzelfde netwerk.

Het is een meetgereedschap, geen productieserver: hij comprimeert elk verzoek
opnieuw en heeft geen enkele beveiliging.

Voor de instellingen die de echte host moet krijgen, zie DEPLOY.md.
"""
import gzip
import http.server
import io
import os
import re
import socket
import sys

COMPRIMEREN = ('.html', '.css', '.js', '.json', '.svg', '.xml', '.txt', '.md')
# Al gecomprimeerd; er nog een laag omheen doen kost tijd en levert niets op.
LANG_IN_CACHE = ('.webp', '.avif', '.png', '.jpg', '.jpeg', '.mp4', '.woff2', '.ico')


class Handler(http.server.SimpleHTTPRequestHandler):
    wortel = '.'
    # 1.1 en niet 1.0: een mediaspeler verwacht een verbinding die blijft staan
    # en ranges. Elk antwoord hieronder zet een Content-Length, dus dit kan.
    protocol_version = 'HTTP/1.1'

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=self.wortel, **kw)

    def log_message(self, *a):
        pass                                   # anders loopt de meting vol

    def end_headers(self):
        ext = os.path.splitext(self.path.split('?')[0])[1].lower()
        if ext in LANG_IN_CACHE:
            # Zonder deze kop vraagt Safari geen ranges aan en speelt de mp4 niet.
            self.send_header('Accept-Ranges', 'bytes')
        if '?v=' in self.path:
            # Verandert de inhoud, dan verandert de hash en dus de URL.
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        elif ext in LANG_IN_CACHE:
            self.send_header('Cache-Control', 'public, max-age=2592000')
        elif ext in ('.html', ''):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def stuur_bereik(self, pad, kop):
        """Een stuk van een bestand, als 206 met Content-Range.

           Alleen `bytes=` met één bereik; dat is wat een browser vraagt. Een
           kop die hier niet past valt terug op het hele bestand, want dat mag
           een server altijd doen."""
        grootte = os.path.getsize(pad)
        m = re.fullmatch(r'bytes=(\d*)-(\d*)', kop.strip())
        if not m or not (m.group(1) or m.group(2)):
            return super().send_head()
        if m.group(1):
            start = int(m.group(1))
            eind = int(m.group(2)) if m.group(2) else grootte - 1
        else:
            start, eind = max(0, grootte - int(m.group(2))), grootte - 1
        if start >= grootte:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{grootte}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return io.BytesIO(b'')
        eind = min(eind, grootte - 1)
        with open(pad, 'rb') as f:
            f.seek(start)
            deel = f.read(eind - start + 1)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(pad))
        self.send_header('Content-Range', f'bytes {start}-{eind}/{grootte}')
        self.send_header('Content-Length', str(len(deel)))
        self.end_headers()
        return io.BytesIO(deel)

    def send_head(self):
        pad = self.translate_path(self.path)
        ext = os.path.splitext(pad)[1].lower()
        wil_gzip = 'gzip' in self.headers.get('Accept-Encoding', '')
        if os.path.isdir(pad) or ext not in COMPRIMEREN or not wil_gzip:
            # Gecomprimeerde bestanden krijgen geen bereik: een range over
            # gzip-bytes zegt niets over het bestand. Beeld en film wel.
            bereik = self.headers.get('Range')
            if bereik and os.path.isfile(pad):
                return self.stuur_bereik(pad, bereik)
            return super().send_head()
        try:
            ruw = open(pad, 'rb').read()
        except OSError:
            return super().send_head()
        klein = gzip.compress(ruw, 6)
        self.send_response(200)
        self.send_header('Content-Type', self.guess_type(pad))
        self.send_header('Content-Encoding', 'gzip')
        self.send_header('Content-Length', str(len(klein)))
        self.send_header('Vary', 'Accept-Encoding')
        self.end_headers()
        return io.BytesIO(klein)


def eigen_adres():
    """Het adres van deze computer op het netwerk, voor het testen op een telefoon."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))       # er gaat niets heen, dit kiest de route
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    lan = '--lan' in sys.argv
    poort = int(args[0]) if args else 8081
    Handler.wortel = str(__import__('pathlib').Path(__file__).resolve().parent.parent)
    host = '0.0.0.0' if lan else '127.0.0.1'
    print(f'http://127.0.0.1:{poort}/  (met gzip, cache-headers en byte-ranges)')
    if lan:
        adres = eigen_adres()
        print(f'http://{adres}:{poort}/  <- dit adres op je telefoon, zelfde wifi'
              if adres else 'netwerkadres niet te bepalen')
        print('let op: deze map staat nu open voor iedereen op dit netwerk')
    http.server.ThreadingHTTPServer((host, poort), Handler).serve_forever()


if __name__ == '__main__':
    main()
