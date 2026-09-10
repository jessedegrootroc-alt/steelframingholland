# -*- coding: utf-8 -*-
"""Meet het contrast van de herotekst op de film, met de sluier eroverheen.

    python3 _generator/meet_hero_contrast.py [film]

Waarom dit nodig is: de sluier in `index.css` is doorgerekend op deze film en
op deze tekstposities. Een andere film heeft andere lichte beeldjes, en een
andere kop of introtekst staat op een andere plek. Verandert een van de drie,
dan moet deze meting opnieuw.

Twee dingen zijn hier eerder misgegaan, en daarom werken ze nu zo:

1. **De sluier wordt uit `index.css` gelezen, niet overgetypt.** Een meting op
   andere waarden dan er in de CSS staan is erger dan geen meting.

2. **De zones zijn de LETTERS, niet de elementvakken.** Het label is een
   block-span die de hele kolom breed is, maar de tekst "Specialist in
   staalframebouw" vult op 1440 maar 16,5% van de breedte. Op het elementvak
   gemeten leek het label het midden van het beeld te claimen, en daardoor leek
   een sluier die alleen tekst dekt onmogelijk. De zones hieronder zijn met
   `Range.getClientRects()` in de browser gemeten.

De sluier is niet vlak meer, dus de dekking hangt van x én y af. Per pixel
wordt de dekking van elke gradientlaag uitgerekend en samengesteld: twee lagen
zwart met dekking a1 en a2 geven samen 1 - (1-a1)(1-a2), precies zoals de
browser ze over elkaar zet.

Genomen wordt het 98e percentiel van de helderheid per zone, niet het
gemiddelde: één lichte plek achter de kop is al genoeg om hem onleesbaar te
maken.
"""
import math
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

WORTEL = pathlib.Path(__file__).resolve().parent.parent
VIDEO = sys.argv[1] if len(sys.argv) > 1 else str(WORTEL / 'assets/video/sfh-hero.mp4')
# De beeldjes zijn wegwerpmateriaal en horen niet in het project.
FRAMES = os.path.join(tempfile.gettempdir(), 'sfh-meetframes')
BEELDJES = 30

# ---------------------------------------------------------------------------
#  De tekstzones, per schermmaat, als fractie van de hero
# ---------------------------------------------------------------------------
# De hero is even hoog als het venster, dus de tekst staat op elke maat op een
# andere hoogte: op 375 begint het label op 30% en op 768 op 63%. Daarom alle
# vier de maten waarop deze site wordt nagekeken.
#
# De knoppen staan er niet in: die hebben een eigen navy vlak en liggen dus
# niet op de film.
#
# eis 4,5 voor gewone tekst; 3,0 voor grote tekst (de titel) en voor vormen
# (het logo, de menuknop).
ZONES = {
    'telefoon 375x812': (375, 812, {
        'logo   (vorm, eis 3,0)': ((0.0427, 0.0265, 0.3228, 0.0683), 3.0),
        'label  (11px, eis 4,5)': ((0.0427, 0.2952, 0.6768, 0.3119), 4.5),
        'titel  (36px, eis 3,0)': ((0.0427, 0.3363, 0.8222, 0.5411), 3.0),
        'intro  (15px, eis 4,5)': ((0.0427, 0.5689, 0.9134, 0.7554), 4.5),
    }),
    'tablet 768x1024': (768, 1024, {
        'logo   (vorm, eis 3,0)': ((0.0208, 0.0210, 0.1576, 0.0542), 3.0),
        'menu   (vorm, eis 3,0)': ((0.8840, 0.0312, 0.9323, 0.0439), 3.0),
        'label  (11px, eis 4,5)': ((0.0208, 0.6319, 0.3305, 0.6451), 4.5),
        'titel  (56px, eis 3,0)': ((0.0208, 0.6634, 0.9548, 0.7715), 3.0),
        'intro  (16px, eis 4,5)': ((0.0208, 0.7932, 0.8848, 0.8647), 4.5),
    }),
    'laptop 1024x768': (1024, 768, {
        'logo   (vorm, eis 3,0)': ((0.0469, 0.0449, 0.1676, 0.0970), 3.0),
        'menu   (vorm, eis 3,0)': ((0.8818, 0.0624, 0.9180, 0.0794), 3.0),
        'label  (11px, eis 4,5)': ((0.0469, 0.4501, 0.2791, 0.4677), 4.5),
        'titel  (64px, eis 3,0)': ((0.0469, 0.4798, 0.6640, 0.7599), 3.0),
        'intro  (16px, eis 4,5)': ((0.0469, 0.7763, 0.6948, 0.8716), 4.5),
    }),
    'desktop 1440x900': (1440, 900, {
        'logo   (vorm, eis 3,0)': ((0.0333, 0.0544, 0.1200, 0.0733), 3.0),
        'nav    (14px, eis 4,5)': ((0.5063, 0.0544, 0.9556, 0.0733), 4.5),
        'label  (11px, eis 4,5)': ((0.0333, 0.4298, 0.1985, 0.4448), 4.5),
        'titel  (72px, eis 3,0)': ((0.0333, 0.4629, 0.5476, 0.7434), 3.0),
        'intro  (16px, eis 4,5)': ((0.0333, 0.7647, 0.4941, 0.8460), 4.5),
    }),
}


# ---------------------------------------------------------------------------
#  De sluier uit index.css
# ---------------------------------------------------------------------------
def lees_sluier():
    """De gradientlagen van .hero--sluier uit index.css lezen.

       -> [(hoek_in_graden, [(positie, dekking), ...]), ...], bovenste laag
       eerst. De volgorde doet voor het resultaat niet uit: zwart over zwart
       is commutatief."""
    css = (WORTEL / 'index.css').read_text(encoding='utf-8')
    m = re.search(r'\.hero--sluier\s*\{(.*?)\n\}', css, re.S)
    if not m:
        raise SystemExit('.hero--sluier niet gevonden in index.css')
    blok = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
    lagen = []
    for stuk in re.findall(r'linear-gradient\(([^()]*(?:\([^()]*\)[^()]*)*)\)', blok):
        delen = [d.strip() for d in stuk.split(',')]
        # De browser hergroepeert rgba(...) niet, maar split() wel: plakken.
        samen, buffer = [], ''
        for d in delen:
            buffer = f'{buffer}, {d}' if buffer else d
            if buffer.count('(') == buffer.count(')'):
                samen.append(buffer)
                buffer = ''
        hoek = 180.0                       # CSS-standaard: naar onderen
        if samen and 'rgba' not in samen[0]:
            kop = samen.pop(0)
            g = re.search(r'(-?[\d.]+)deg', kop)
            if g:
                hoek = float(g.group(1))
            elif 'to bottom' in kop:
                hoek = 180.0
            elif 'to top' in kop:
                hoek = 0.0
            else:
                raise SystemExit(f'onbekende gradientrichting: {kop!r}')
        stops = []
        for s in samen:
            a = re.search(r'rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*([\d.]+)\s*\)', s)
            if not a:
                raise SystemExit(f'alleen zwarte stops worden gemeten, niet {s!r}')
            p = re.search(r'([\d.]+)%', s)
            stops.append((None if not p else float(p.group(1)) / 100, float(a.group(1))))
        # stops zonder eigen positie verdelen over 0..1, zoals CSS dat doet
        n = len(stops)
        uit = [((i / (n - 1) if n > 1 else 0.0) if p is None else p, a)
               for i, (p, a) in enumerate(stops)]
        lagen.append((hoek, sorted(uit)))
    if not lagen:
        raise SystemExit('geen linear-gradient gevonden in .hero--sluier')
    return lagen


def dekking(lagen, fx, fy, bw, bh):
    """De dekking van de hele sluier op (fx, fy), als array.

       De positie langs een CSS-gradientlijn: 0deg wijst naar boven en 90deg
       naar rechts, en de lijn is |b*sin| + |h*cos| lang. Bij 0deg ligt 0% dus
       onderaan, precies zoals de browser het tekent."""
    open_deel = np.ones_like(np.asarray(fx, dtype=float))
    for hoek, stops in lagen:
        r = math.radians(hoek)
        L = abs(bw * math.sin(r)) + abs(bh * math.cos(r))
        p = ((np.asarray(fx) * bw - bw / 2) * math.sin(r) +
             (np.asarray(fy) * bh - bh / 2) * -math.cos(r)) / L + 0.5
        a = np.interp(p, [q for q, _ in stops], [v for _, v in stops])
        open_deel = open_deel * (1 - a)
    return 1 - open_deel


# ---------------------------------------------------------------------------
#  Helderheid en contrast (WCAG)
# ---------------------------------------------------------------------------
_c = np.arange(256) / 255
_LIN = np.where(_c <= 0.03928, _c / 12.92, ((_c + 0.055) / 1.055) ** 2.4)


def lum(arr):
    """Relatieve luminantie van een RGB-array."""
    a = _LIN[arr]
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def contrast_wit(L):
    return 1.05 / (L + 0.05)


# ---------------------------------------------------------------------------
#  De film
# ---------------------------------------------------------------------------
def haal_frames(n=BEELDJES):
    os.makedirs(FRAMES, exist_ok=True)
    for f in os.listdir(FRAMES):
        os.remove(os.path.join(FRAMES, f))
    duur = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', VIDEO], capture_output=True, text=True).stdout.strip()
    if not duur:
        raise SystemExit(f'kan de duur van {VIDEO} niet lezen; bestaat het bestand?')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO,
                    '-vf', f'fps={n}/{float(duur):.3f}', '-vsync', '0', '-q:v', '2',
                    os.path.join(FRAMES, 'f%03d.jpg')], check=True)
    return sorted(os.path.join(FRAMES, f) for f in os.listdir(FRAMES))


def zichtbaar(im, bw, bh):
    """Het deel van het beeld dat bij object-fit: cover in een bak bw x bh valt."""
    w, h = im.size
    s = max(bw / w, bh / h)
    zw, zh = bw / s, bh / s                       # in bronpixels
    l, t = (w - zw) / 2, (h - zh) / 2
    return im.crop((round(l), round(t), round(l + zw), round(t + zh)))


def meet(lagen, paden):
    """-> {(schermnaam, zonenaam): (contrast, eis, beeldje)}"""
    uit = {}
    for schermnaam, (bw, bh, zones) in ZONES.items():
        for naam, (_, eis) in zones.items():
            uit[(schermnaam, naam)] = (99.0, eis, None)
        for pad in paden:
            im = Image.open(pad).convert('RGB')
            deel = zichtbaar(im, bw, bh)
            dw, dh = deel.size
            for naam, ((x0, y0, x1, y1), eis) in zones.items():
                vak = deel.crop((round(x0 * dw), round(y0 * dh),
                                 max(round(x1 * dw), round(x0 * dw) + 1),
                                 max(round(y1 * dh), round(y0 * dh) + 1)))
                k = max(1, min(vak.size) // 12)
                vak = vak.resize((max(1, vak.size[0] // k), max(1, vak.size[1] // k)))
                vw, vh = vak.size
                gx, gy = np.meshgrid(x0 + (x1 - x0) * (np.arange(vw) + .5) / vw,
                                     y0 + (y1 - y0) * (np.arange(vh) + .5) / vh)
                a = dekking(lagen, gx.ravel(), gy.ravel(), bw, bh)
                eff = lum(np.asarray(vak)).ravel() * (1 - a)
                c = contrast_wit(np.percentile(eff, 98))
                if c < uit[(schermnaam, naam)][0]:
                    uit[(schermnaam, naam)] = (c, eis, os.path.basename(pad))
    return uit


def gemiddelde_helderheid(lagen, bw, bh, n=48):
    """Hoeveel van de film er gemiddeld overblijft: 1 is een sluier van niets."""
    gx, gy = np.meshgrid((np.arange(n) + .5) / n, (np.arange(n) + .5) / n)
    return float((1 - dekking(lagen, gx.ravel(), gy.ravel(), bw, bh)).mean())


def main():
    lagen = lees_sluier()
    print(f'film   {os.path.relpath(VIDEO, WORTEL)}')
    print(f'sluier {len(lagen)} laag/lagen uit index.css:')
    for hoek, stops in lagen:
        print(f'   {hoek:g}deg  ' + '  '.join(f'{a * 100:.0f}% op {p * 100:.0f}%'
                                              for p, a in stops))
    paden = haal_frames()
    print(f'{len(paden)} beeldjes, 98e percentiel per zone\n')
    r = meet(lagen, paden)
    fout = False
    for schermnaam, (bw, bh, _) in ZONES.items():
        h = gemiddelde_helderheid(lagen, bw, bh)
        print(f'{schermnaam}   sluier laat gemiddeld {h * 100:.0f}% van de film door')
        for (s, naam), (c, eis, beeldje) in sorted(r.items()):
            if s != schermnaam:
                continue
            ok = c >= eis
            fout = fout or not ok
            print(f'   {naam:24} {c:5.2f}:1  {"OK" if ok else "TE DONKER"}'
                  f'   krapste beeldje {beeldje}')
        print()
    if fout:
        sys.exit('MINSTENS EEN ZONE HAALT DE EIS NIET')
    print('alle zones halen de eis')


if __name__ == '__main__':
    main()
