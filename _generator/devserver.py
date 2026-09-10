# -*- coding: utf-8 -*-
"""Lokale server die comprimeert en cache-headers stuurt, zoals een echte host.

    python3 _generator/devserver.py 8081

Waarom dit er is: `python3 -m http.server` comprimeert niet en stuurt geen
cache-headers. Meet je Lighthouse daartegen, dan mis je twee dingen die elke
host wel doet, en kom je ongeveer vijf punten te laag uit. Deze server bootst na
wat Apache, nginx, Netlify en Cloudflare standaard doen, zodat de meting klopt
met wat een bezoeker straks krijgt.

Het is een meetgereedschap, geen productieserver: hij comprimeert elk verzoek
opnieuw en heeft geen enkele beveiliging.

Voor de instellingen die de echte host moet krijgen, zie DEPLOY.md.
"""
import gzip
import http.server
import io
import os
import sys

COMPRIMEREN = ('.html', '.css', '.js', '.json', '.svg', '.xml', '.txt', '.md')
# Al gecomprimeerd; er nog een laag omheen doen kost tijd en levert niets op.
LANG_IN_CACHE = ('.webp', '.avif', '.png', '.jpg', '.jpeg', '.mp4', '.woff2', '.ico')


class Handler(http.server.SimpleHTTPRequestHandler):
    wortel = '.'

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=self.wortel, **kw)

    def log_message(self, *a):
        pass                                   # anders loopt de meting vol

    def end_headers(self):
        ext = os.path.splitext(self.path.split('?')[0])[1].lower()
        if '?v=' in self.path:
            # Verandert de inhoud, dan verandert de hash en dus de URL.
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        elif ext in LANG_IN_CACHE:
            self.send_header('Cache-Control', 'public, max-age=2592000')
        elif ext in ('.html', ''):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_head(self):
        pad = self.translate_path(self.path)
        ext = os.path.splitext(pad)[1].lower()
        wil_gzip = 'gzip' in self.headers.get('Accept-Encoding', '')
        if os.path.isdir(pad) or ext not in COMPRIMEREN or not wil_gzip:
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


def main():
    poort = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    Handler.wortel = str(__import__('pathlib').Path(__file__).resolve().parent.parent)
    print(f'http://127.0.0.1:{poort}/  (met gzip en cache-headers)')
    http.server.ThreadingHTTPServer(('127.0.0.1', poort), Handler).serve_forever()


if __name__ == '__main__':
    main()
