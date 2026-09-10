# -*- coding: utf-8 -*-
"""Geminificeerde versies van de stylesheets en de scripts wegschrijven.

De bestanden in de wortel zijn de bron: daar staat het commentaar in, en daar
werk je in. Dit script schrijft er `<naam>.min.css` en `<naam>.min.js` naast, en
`schil.py` verwijst naar die als ze bestaan.

Waarom het nodig is: styleguide.css is 116 kB en blokkeert het tekenen van de
pagina. Lighthouse mat daar 1661 ms op een mobiele verbinding. Geminificeerd is
het 61 kB, en dat commentaar hoeft de bezoeker niet te downloaden. De uitleg
blijft in de bron staan, dus er gaat geen documentatie verloren.

Minificeren doet esbuild en niet een eigen zoek-en-vervang: die heeft een echte
CSS- en JS-parser, en een reguliere expressie op CSS gaat vroeg of laat mis op
een string of een url() met een accolade erin.

Staat esbuild niet klaar, dan schrijft dit script niets weg. `schil.py` verwijst
dan naar de gewone bestanden en de site werkt gewoon, alleen wat zwaarder.
"""
import shutil
import subprocess
import pathlib

WORTEL = pathlib.Path(__file__).resolve().parent.parent

# Alles wat in de wortel staat, uit de map gelezen in plaats van hier opgesomd.
# Een handmatige lijst raakte al één bestand kwijt: over-ons.css stond er niet
# in, waardoor `inline()` in schil.py terugviel op het onbewerkte bestand en het
# CSS-commentaar in de HTML van drie pagina's terechtkwam.
#
# cursus.css hoort er strikt niet bij (geen enkele pagina laadt hem meer), maar
# een bestand dat nergens wordt aangeroepen kost ook niets als het toch
# geminificeerd wordt. Dat is een betere ruil dan een lijst die stil verouderd.
def _bestanden(patroon):
    return sorted(p.name for p in WORTEL.glob(patroon)
                  if not p.stem.endswith('.min'))


CSS = None   # wordt in main() uit de map gelezen
JS = None


def _esbuild():
    """Het commando om esbuild te draaien, of None."""
    if shutil.which('esbuild'):
        return ['esbuild']
    if shutil.which('npx'):
        return ['npx', '-y', 'esbuild@0.25']
    return None


def main():
    cmd = _esbuild()
    if not cmd:
        print('minify: esbuild niet gevonden, geen geminificeerde bestanden')
        return []

    gemaakt = []
    for naam in _bestanden('*.css') + _bestanden('*.js'):
        bron = WORTEL / naam
        if not bron.exists():
            continue
        doel = WORTEL / (bron.stem + '.min' + bron.suffix)
        # target=es2020: de bron gebruikt optional chaining, dus lager kan niet
        # zonder te hertalen, en hoger heeft geen zin.
        r = subprocess.run(
            cmd + [str(bron), '--minify', '--target=es2020', f'--outfile={doel}'],
            capture_output=True, text=True)
        if r.returncode != 0:
            print(f'minify: {naam} MISLUKT\n{r.stderr.strip()[:300]}')
            continue
        gemaakt.append(doel.name)
        voor, na = bron.stat().st_size, doel.stat().st_size
        print(f'  {naam:22s} {voor/1024:6.1f} kB -> {na/1024:6.1f} kB '
              f'({100 - na * 100 // voor:.0f}% eraf)')
    print(f'minify: {len(gemaakt)} bestanden')
    return gemaakt


if __name__ == '__main__':
    main()
