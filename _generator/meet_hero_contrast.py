# -*- coding: utf-8 -*-
"""Meet het contrast van de herotekst op de film, met de sluier eroverheen.

Waarom dit nodig is: de sluier in index.css is doorgerekend op de vórige film.
Een andere film heeft andere lichte beeldjes, dus de meting moet opnieuw.

Werkwijze: per beeldje wordt het deel van de film bepaald dat bij
`object-fit: cover` echt in beeld komt, de sluier eroverheen gelegd, en per
tekstvlak de helderheid van de lichtste pixels genomen. Daar wordt het contrast
van witte tekst tegen berekend.
"""
import re, subprocess, sys, os, pathlib, tempfile
from PIL import Image

WORTEL = pathlib.Path(__file__).resolve().parent.parent
VIDEO = sys.argv[1] if len(sys.argv) > 1 else str(WORTEL / 'assets/video/sfh-hero.mp4')
# De beeldjes zijn wegwerpmateriaal en horen niet in het project.
FRAMES = os.path.join(tempfile.gettempdir(), 'sfh-meetframes')

def lees_sluier():
    """De stops van .hero--sluier uit index.css lezen.

       Niet overtypen: een meting die op andere waarden is gedaan dan er in de
       CSS staan, is erger dan geen meting. Dat is hier één keer gebeurd."""
    css = (WORTEL / 'index.css').read_text(encoding='utf-8')
    m = re.search(r'\.hero--sluier\s*\{(.*?)\}', css, re.S)
    if not m:
        raise SystemExit('.hero--sluier niet gevonden in index.css')
    blok = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
    stops = []
    for a, pos in re.findall(r'rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*([\d.]+)\s*\)\s*([\d.]+)?%?', blok):
        stops.append((None if pos in ('', None) else float(pos) / 100, float(a)))
    if not stops:
        raise SystemExit('geen zwarte stops gevonden in .hero--sluier')
    # stops zonder eigen positie verdelen over 0..1, zoals CSS dat doet
    n = len(stops)
    uit = []
    for i, (pos, a) in enumerate(stops):
        uit.append(((i / (n - 1) if n > 1 else 0.0) if pos is None else pos, a))
    return sorted(uit)


SLUIER = None            # wordt in main gevuld uit index.css

# De tekstvlakken, als fractie van de hero (uit de browser gemeten op 1440x900).
VLAKKEN = {
    'navigatie (14px, eis 4,5)': (0.4948, 0.0356, 0.9667, 0.0933),
    'label     (11px, eis 4,5)': (0.0333, 0.4309, 0.6583, 0.4446),
    'titel     (72px, eis 3,0)': (0.0333, 0.4713, 0.6583, 0.7352),
    'intro     (16px, eis 4,5)': (0.0333, 0.7619, 0.4944, 0.8489),
    'knop      (11px, eis 4,5)': (0.0333, 0.9022, 0.3216, 0.9556),
}

SCHERMEN = [('desktop 1440x900', 1440, 900), ('telefoon 375x812', 375, 812)]


def alfa(fy):
    """De dekking van de sluier op hoogte fy (0..1), lineair tussen de stops."""
    for (p0, a0), (p1, a1) in zip(SLUIER, SLUIER[1:]):
        if p0 <= fy <= p1:
            t = 0 if p1 == p0 else (fy - p0) / (p1 - p0)
            return a0 + t * (a1 - a0)
    return SLUIER[-1][1]


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(r, g, b):
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_wit(L):
    return (1.0 + 0.05) / (L + 0.05)


def haal_frames(n=30):
    os.makedirs(FRAMES, exist_ok=True)
    for f in os.listdir(FRAMES):
        os.remove(os.path.join(FRAMES, f))
    # 30 beeldjes verdeeld over de hele film
    # dertig beeldjes over de hele film, ongeacht de lengte
    duur = float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', VIDEO], capture_output=True, text=True).stdout.strip())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO,
                    '-vf', f'fps={n}/{duur:.3f}', '-vsync', '0', '-q:v', '2',
                    os.path.join(FRAMES, 'f%03d.jpg')], check=True)
    return sorted(os.path.join(FRAMES, f) for f in os.listdir(FRAMES))


def zichtbaar(im, bw, bh):
    """Het deel van het beeld dat bij object-fit: cover in een bak bw x bh valt."""
    w, h = im.size
    s = max(bw / w, bh / h)
    zw, zh = bw / s, bh / s                       # in bronpixels
    l, t = (w - zw) / 2, (h - zh) / 2
    return im.crop((round(l), round(t), round(l + zw), round(t + zh)))


def meet(frames, bw, bh, percentiel=0.98):
    slechtst = {k: (99.0, None) for k in VLAKKEN}
    for pad in frames:
        im = Image.open(pad).convert('RGB')
        deel = zichtbaar(im, bw, bh)
        dw, dh = deel.size
        for naam, (x0, y0, x1, y1) in VLAKKEN.items():
            vak = deel.crop((round(x0 * dw), round(y0 * dh),
                             max(round(x1 * dw), round(x0 * dw) + 1),
                             max(round(y1 * dh), round(y0 * dh) + 1)))
            vak = vak.resize((max(1, vak.size[0] // 4), max(1, vak.size[1] // 4)))
            fy = (y0 + y1) / 2
            a = alfa(fy)
            waarden = sorted(lum(*p) * (1 - a) for p in vak.getdata())
            L = waarden[min(len(waarden) - 1, int(len(waarden) * percentiel))]
            c = contrast_wit(L)
            if c < slechtst[naam][0]:
                slechtst[naam] = (c, os.path.basename(pad))
    return slechtst


if __name__ == '__main__':
    SLUIER = lees_sluier()
    print('sluier uit index.css: ' + ', '.join(f'{a*100:.0f}% op {p*100:.0f}%' for p, a in SLUIER))
    frames = haal_frames()
    print(f'{len(frames)} beeldjes gemeten uit {os.path.basename(VIDEO)}\n')
    for label, bw, bh in SCHERMEN:
        print(f'--- {label} ---')
        r = meet(frames, bw, bh)
        for naam, (c, waar) in r.items():
            eis = 3.0 if 'titel' in naam else 4.5
            vlag = 'OK  ' if c >= eis else 'FOUT'
            print(f'  {vlag} {naam}  {c:5.2f}:1   (slechtste beeldje: {waar})')
        print()
