#!/usr/bin/env python3
"""Zet het aangeleverde merkpatroon om naar de WebP-bestanden die de site laadt.

    python3 _generator/maak_patronen.py

De bronbestanden staan in `assets/patronen/bron/`. Wat hier gebeurt:

1. **Beide varianten gaan ongewijzigd door.** De kleuren blijven precies zoals
   ze zijn aangeleverd: navy `#002848` met `#00B767`.

   Dat was niet altijd zo. De CTA-variant werd hier omgekleurd naar `#1B7A48`,
   een dieper groen, omdat er witte tekst middenop staat en wit op `#00B767`
   maar 2,64:1 haalt tegen een eis van 4,5:1. Het gevolg was een dof groen dat
   niet als de merkkleur las: het leek alsof er een donkere waas over het blok
   lag, terwijl het de bitmap zelf was.

   Dat is nu opgelost in de vórm en niet in de kleur, en niet hier maar in het
   patroon zelf. De aangeleverde `cta.png` heeft een **leeg midden**: alleen
   het parallellogram linksonder en de kubus rechts, met navy ertussen. Daar
   staat de tekst, en wit haalt op dat navy 15,03:1.

   Wil je hier terug naar een omgekleurd patroon, zet dan een doelgroen in
   PLAN en gebruik `op_de_lijn()`; die functie staat er nog en werkt.

2. **Lossless WebP.** Het zijn twee vlakke kleuren met harde diagonalen. Lossy
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

# De twee kleuren van het aangeleverde patroon. Beide varianten houden ze.
NAVY = (0, 40, 72)          # #002848, zoals aangeleverd
GROEN = (0, 183, 103)       # #00B767, zoals aangeleverd

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
VERSIE = 'v5'

# (bronbestand, naam, breedtes)
PLAN = [
    ('Hero.png', f'hero-patroon-{VERSIE}', [720, 1000, 1440]),
    ('cta.png', f'cta-patroon-{VERSIE}', [1440, 2880]),
]


def op_de_lijn(im, doelgroen):
    """Elke pixel terugzetten op de lijn tussen navy en `doelgroen`.

       Beide varianten gebruiken hier GROEN, dus dit verandert de kleuren niet;
       het haalt de franje weg die het verkleinen erin legt. Zie hieronder.

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
    for bestand, naam, breedtes in PLAN:
        bron = BRON / bestand
        if not bron.exists():
            sys.exit(f'bron ontbreekt: {bron}')
        origineel = Image.open(bron).convert('RGB')
        print(f'{bestand}  {origineel.size[0]}x{origineel.size[1]}'
              f'  (kleuren ongewijzigd)')
        for b in breedtes:
            h = round(origineel.size[1] * b / origineel.size[0])
            pad = UIT / f'{naam}-{b}.webp'
            verkleind = origineel.resize((b, h), Image.LANCZOS)
            n = webp(op_de_lijn(verkleind, GROEN), pad)
            totaal += n
            print(f'   {pad.name:28} {b}x{h}  {n / 1024:6.1f} kB')
    print(f'\n{totaal / 1024:.1f} kB aan patronen')


if __name__ == '__main__':
    main()
