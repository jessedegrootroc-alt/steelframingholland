#!/usr/bin/env python3
"""Zet het aangeleverde merkpatroon om naar de WebP-bestanden die de site laadt.

    python3 _generator/maak_patronen.py

De bronbestanden staan in `assets/patronen/bron/`. Wat hier gebeurt:

1. **De hero-variant gaat ongewijzigd door.** Dat patroon staat in een eigen vak
   naast de kop; er komt geen tekst over. De kleuren blijven dus precies zoals
   ze zijn aangeleverd.

2. **De CTA-variant wordt omgekleurd.** Daar staat witte tekst middenop, en het
   aangeleverde groen `#00B767` haalt met wit 2,64:1 tegen een eis van 4,5:1.
   Het groen wordt daarom het accent uit de merklaag, `#1B7A48` (5,35:1).

   Waarom omkleuren en niet een waas eroverheen: een waas van 35% navy haalt de
   eis ook, maar duwt het groen naar teal (`#04845b`) en dat valt buiten het
   merk. Omkleuren houdt het een groen, houdt de randen scherp, en gebruikt de
   kleur die in de merklaag al bestaat juist omdat het logogroen op wit te licht
   is. Zie assets/patronen/HERKOMST.md.

3. **Lossless WebP.** Het zijn twee vlakke kleuren met harde diagonalen. Lossy
   op q88 is 10,9 kB en maakt er 4048 kleuren van (franje langs de diagonalen);
   lossless is 8,1 kB en pixelexact. Kleiner én scherper, dus die keuze is geen
   afweging.

De maten hieronder zijn die waar `schil.py` en `styleguide.css` naar verwijzen.
"""
import pathlib
import subprocess
import sys

from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parent
BRON = WORTEL / 'assets' / 'patronen' / 'bron'
UIT = WORTEL / 'assets' / 'patronen'

# De twee kleuren van het aangeleverde patroon, en waar het groen naartoe gaat
# in de variant waar tekst over komt.
NAVY = (0, 40, 72)          # #002848, zoals aangeleverd
GROEN = (0, 183, 103)       # #00B767, zoals aangeleverd
GROEN_LEESBAAR = (27, 122, 72)   # #1B7A48, --color-accent uit de merklaag

# De versie zit in de bestandsnaam, en dat is geen sier.
#
# DEPLOY.md zet een cache van dertig dagen op beeld, en de patroonbestanden
# hadden altijd dezelfde naam. Wie de site eerder bezocht hield daardoor het
# oude patroon, ook nadat het vervangen was. Dat is hier precies gebeurd: bij
# het nakijken van versie 3 stond in de browser nog het paarse patroon van
# versie 2 in het contactvlak, terwijl het nieuwe bestand al op schijf stond.
#
# Verandert het patroon, dan verhoog je VERSIE. Nieuwe naam is een nieuwe URL,
# dus geen enkele cache kan er nog tussen zitten. De stylesheets en scripts
# lossen dit met `?v=<hash>` op (zie v() in schil.py); beeld dat vanuit CSS
# wordt aangeroepen kan dat niet, dus daar doet de naam het werk.
VERSIE = 'v3'

# (bronbestand, naam, breedtes, groen omkleuren)
PLAN = [
    ('Hero.png', f'hero-patroon-{VERSIE}', [720, 1000, 1440], False),
    ('cta.png', f'cta-patroon-{VERSIE}', [1440, 2880], True),
]


def op_de_lijn(im, doelgroen):
    """Elke pixel terugzetten op de lijn tussen navy en `doelgroen`.

       Het patroon is een verloop tussen twee kleuren: elke pixel is navy, groen
       of een tussenstap van de antialiasing op een diagonaal. Per pixel wordt
       bepaald hoe groen hij is (het groene kanaal scheidt het beste: 40 tegen
       183) en daarna opnieuw gemengd tussen navy en het doelgroen. Zo blijven de
       diagonalen even glad als in het origineel.

       Dit gebeurt ná het verkleinen, en dat is niet willekeurig. Lanczos schiet
       op een harde diagonaal door tot voorbij de eindkleur: in de 1440-variant
       leverde dat één pixel van #1f8848 op, lichter dan het groen zelf, en die
       haalde met wit 4,49:1 in plaats van 4,50. Door hier te klemmen op [0,1]
       kan geen pixel lichter worden dan de eindkleur, en is de meting over elke
       pixel exact wat de kleuren beloven."""
    im = im.convert('RGB')
    px = im.load()
    breed, hoog = im.size
    lo, hi = NAVY[1], GROEN[1]
    for y in range(hoog):
        for x in range(breed):
            t = (px[x, y][1] - lo) / (hi - lo)
            t = 0.0 if t < 0 else (1.0 if t > 1 else t)
            px[x, y] = tuple(
                round(NAVY[i] * (1 - t) + doelgroen[i] * t) for i in range(3))
    return im


def webp(im, pad):
    tijdelijk = pad.with_suffix('.tmp.png')
    im.save(tijdelijk)
    r = subprocess.run(['cwebp', '-quiet', '-lossless', '-m', '6',
                        str(tijdelijk), '-o', str(pad)], capture_output=True)
    tijdelijk.unlink()
    if r.returncode != 0:
        sys.exit(f'cwebp faalde op {pad.name}: {r.stderr.decode()[:200]}')
    return pad.stat().st_size


def main():
    if not BRON.exists():
        sys.exit(f'bronmap ontbreekt: {BRON}')
    # De oude bestanden weg, zodat er geen maat blijft liggen die niemand meer
    # aanroept. Dat is één keer gebeurd met hero-patroon-mobiel-*.
    for oud in UIT.glob('*.webp'):
        oud.unlink()
    totaal = 0
    for bestand, naam, breedtes, om in PLAN:
        bron = BRON / bestand
        if not bron.exists():
            sys.exit(f'bron ontbreekt: {bron}')
        origineel = Image.open(bron).convert('RGB')
        doel = GROEN_LEESBAAR if om else GROEN
        print(f'{bestand}  {origineel.size[0]}x{origineel.size[1]}'
              f'{"  (groen -> #1B7A48)" if om else "  (kleuren ongewijzigd)"}')
        for b in breedtes:
            h = round(origineel.size[1] * b / origineel.size[0])
            pad = UIT / f'{naam}-{b}.webp'
            verkleind = origineel.resize((b, h), Image.LANCZOS)
            n = webp(op_de_lijn(verkleind, doel), pad)
            totaal += n
            print(f'   {pad.name:28} {b}x{h}  {n / 1024:6.1f} kB')
    print(f'\n{totaal / 1024:.1f} kB aan patronen')


if __name__ == '__main__':
    main()
