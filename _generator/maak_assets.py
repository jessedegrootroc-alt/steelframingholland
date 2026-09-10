#!/usr/bin/env python3
"""Zet de afbeeldingen uit de export van de bronsite om naar de assets van deze site.

De template vraagt per beeld meerdere breedtes in WebP (zie foto() in
schil.py). cwebp maakt ze; welke ladder een beeld krijgt hangt af van waar het
staat.

De bronbestanden staan in `assets_bron/sfh/`. Dat zijn de originelen van
www.steelframingholland.nl: per beeldsleutel één bestand, met dezelfde naam als
de sleutel. Welke dat zijn en waar ze vandaan komen staat in `beeldplan.json`,
onder `herkomst`.

Het logo wordt hier niet gemaakt. Dat is een eenmalige bewerking geweest van
het logobestand van de bronsite (de navy delen wit, het groen behouden, zodat
het merk ook op een donkere balk leesbaar blijft); het resultaat staat in
assets/logo/. Zie assets/logo/HERKOMST.md.

Draaien:  python3 maak_assets.py
"""
import json, pathlib, subprocess, sys
from PIL import Image

HIER   = pathlib.Path(__file__).resolve().parent
WORTEL = HIER.parent
FOTO   = WORTEL / 'assets' / 'foto'

LADDERS = {
    'hero':    [640, 1200, 1800, 2400],
    'kaart':   [480, 800, 1200, 1800],
    'inhoud':  [480, 800, 1200],
}


def webp(bron, naam, breedtes, kwaliteit=82):
    """Schrijft <naam>-<breedte>.webp voor elke breedte die het origineel haalt."""
    FOTO.mkdir(parents=True, exist_ok=True)
    im = Image.open(bron)
    bb, bh = im.size
    gedaan = []
    kandidaten = [b for b in breedtes if b <= bb] or [bb]
    if bb not in kandidaten and bb < max(breedtes):
        kandidaten.append(bb)                 # de eigen breedte als grootste trap
    for b in sorted(set(kandidaten)):
        uit = FOTO / f'{naam}-{b}.webp'
        r = subprocess.run(['cwebp', '-quiet', '-q', str(kwaliteit), '-m', '6',
                            '-resize', str(b), '0', str(bron), '-o', str(uit)],
                           capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f'cwebp faalde op {bron}: {r.stderr.decode()[:200]}')
        gedaan.append(b)
    grootste = max(gedaan)
    hoogte = round(bh * grootste / bb)
    return gedaan, grootste, hoogte


def main():
    plan = json.loads((HIER / 'beeldplan.json').read_text(encoding='utf-8'))
    uit = {}
    for naam, regel in plan.items():
        bron = HIER / regel['bron'].lstrip('/')
        if not bron.exists():
            raise SystemExit(f'{naam}: bron ontbreekt: {regel["bron"]}')
        breedtes, gb, gh = webp(bron, naam, LADDERS[regel['rol']])
        uit[naam] = {'breedtes': breedtes, 'breed': gb, 'hoog': gh,
                     'alt': regel['alt'], 'bron': regel['bron'],
                     'herkomst': regel.get('herkomst', '')}
        print(f'  {naam:44s} {breedtes} -> {gb}x{gh}')
    (HIER / 'beeldmaten.json').write_text(
        json.dumps(uit, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n{len(uit)} beelden omgezet, maten in beeldmaten.json')


if __name__ == '__main__':
    main()
