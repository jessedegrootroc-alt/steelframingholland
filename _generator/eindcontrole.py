# -*- coding: utf-8 -*-
"""Controleert de gegenereerde pagina's op fouten die je met het oog mist.

    python3 _generator/eindcontrole.py

Draai dit na `bouw_alles.py`. Het kijkt niet of de site mooi is; het kijkt of er
niets kapot of dubbel is. Wat het nagaat:

  - kapotte interne links
  - precies één <h1> per pagina, en geen sprong in de koppenniveaus
  - unieke <title> en meta-omschrijving, en geen lege
  - resten van de vorige merken: bedrijfsnaam, contactgegevens, merkkleuren
    (als hex, als rgb-getallen ongeacht schrijfwijze, én in de pixels van de
    verzonden beelden), dienstnamen (dit template is twee keer omgebouwd)
  - lege alinea's en afbeeldingen zonder alt
  - dubbele labels in de navigatie
  - hoeveel [CONTENT NODIG]-markeringen er staan (die horen er te zijn)
"""
import collections
import pathlib
import re
import sys

WORTEL = pathlib.Path(__file__).resolve().parent.parent
PAGINAS = sorted(WORTEL.glob('*.html'))

# Dingen die er niet meer in mogen staan.
#
# Dit template is twee keer omgebouwd. Elke ronde laat resten achter die je met
# het oog mist omdat ze op één pagina staan of in een attribuut; daarom staat
# per vorige eigenaar waar je op moet letten. De regels van een oudere ronde
# blijven staan: ze kosten niets en vangen een terugval uit een backup.
VERBODEN = [
    # generiek
    (r'(?i)lorem ipsum', 'lorem'),
    (r'TODO-CONTENT', 'todo'),
    # vorige eigenaar: Duyts Bouwconstructies (Amsterdam)
    (r'(?i)duyts', 'oude bedrijfsnaam'),
    (r'020[\s-]?684[\s-]?7475|\+3120684', 'oud telefoonnummer'),
    (r'(?i)slingelandtstraat|1051\s?CH', 'oud adres'),
    (r'33228370', 'oud KvK-nummer'),
    (r'(?i)#463878|#C7D8E0|#143369|#3A2E63|#2A2147', 'oude merkkleur'),
    (r'(?i)registerconstructeur|funderingsherstel|muurdoorbraak',
     'oude dienstnaam'),
    # eigenaar daarvoor
    (r'(?i)madegro', 'madegro'),
    (r'0182[\s-]?\d{6}', 'ouder telefoonnummer'),
    (r'(?i)gouda|moordrecht', 'ouder adres'),
    (r'#017E84|#0d7377|rgba\(1,\s*126,\s*132', 'oudere merkkleur'),
]


# De oude merktinten als rgb-getallen. Een reguliere expressie op de
# hexvorm mist `rgba(70, 56, 120, .2)`, en een expressie op één rgba-schrijfwijze
# mist `rgba(70,56,120,.2)` zonder spaties. Die twee zijn hier allebei
# voorgekomen: de sluier in het uitklapmenu stond twee kleurwissels achter en
# is er twee keer mee doorgeglipt. Daarom worden de getallen zelf vergeleken.
OUDE_TINTEN = {
    (70, 56, 120):   '#463878 (oude primary)',
    (42, 33, 71):    '#2A2147 (oude deepest)',
    (58, 46, 99):    '#3A2E63 (oude deep)',
    (20, 51, 105):   '#143369 (oude accent)',
    (199, 216, 224): '#C7D8E0 (oude secondary)',
    (13, 34, 71):    '#0D2247 (oude accent-strong)',
}


def oude_tint_als_rgb(inhoud):
    """Elke rgb()/rgba() in `inhoud` die een oude merktint is."""
    uit = []
    for m in re.finditer(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', inhoud):
        trio = tuple(int(x) for x in m.groups())
        if trio in OUDE_TINTEN:
            uit.append(f'{m.group(0)}) = {OUDE_TINTEN[trio]}')
    return uit


# De tinten van dít merk. Nodig omdat sommige oude en nieuwe tinten dicht bij
# elkaar liggen: de oude #0D2247 zit op vier waarden van de huidige navy
# #0D2646. Een pixel wordt daarom toegewezen aan de referentiekleur waar hij het
# dichtst bij ligt, en telt alleen als dat een oude tint is.
HUIDIGE_TINTEN = {
    (13, 38, 70):    '#0D2646 navy',
    (188, 218, 131): '#BCDA83 lichtgroen',
    (27, 122, 72):   '#1B7A48 accent',
    (10, 30, 54):    '#0A1E36 navy diep',
    (8, 23, 41):     '#081729 navy diepst',
    (20, 96, 58):    '#14603A accent donker',
    (0, 40, 72):     '#002848 patroon-navy',
    (0, 183, 103):   '#00B767 patroon-groen',
    (48, 179, 109):  '#30B36D logogroen',
    (255, 255, 255): 'wit',
    (0, 0, 0):       'zwart',
}


def merkkleur_in_beeld(drempel=10.0, marge=8, max_kleuren=400):
    """De verzonden beelden aftasten op de merktinten van een vorige eigenaar.

       Waarom dit er is: de patroonbitmaps in assets/patronen/ waren bij de
       ombouw naar dit merk niet opnieuw gemaakt. Ze bestonden voor 46% uit
       #463878, de indigo van de vorige eigenaar, en stonden zo op het
       contactvlak en in de patroonhero van vier pagina's. Alle tekstcontroles
       hierboven gaven groen licht, want in de HTML en de CSS stond niets
       verkeerd: de kleur zat in de pixels. De opdrachtgever zag het zelf.

       Deze controle kijkt naar wat die fout kenmerkte, en niet naar losse
       pixels:

         `max_kleuren`  alleen vlak beeld. Een patroon, logo of icoon heeft
                        tientallen kleuren, een foto tienduizenden. Zonder deze
                        grens meldt de controle bleekblauwe luchten als
                        #C7D8E0 en donkere schaduwen als #0D2247, en dan is
                        hij niets waard.
         `drempel`      minstens tien procent van het beeld. Een achtergebleven
                        merkvlak is groot; antialiasing langs een rand is dat
                        niet.
         nearest        een kleur telt alleen als hij dichter bij een OUDE tint
                        ligt dan bij een huidige. De oude #0D2247 zit op vier
                        waarden van de huidige navy #0D2646, dus zonder dit
                        meldt elk navy vlak zich.

       Vraagt PIL, en die is er niet altijd; dan levert het None en slaat de
       controle zichzelf over.
    """
    try:
        from PIL import Image
    except ImportError:
        return None

    referenties = ([(t, naam, True) for t, naam in OUDE_TINTEN.items()]
                   + [(t, naam, False) for t, naam in HUIDIGE_TINTEN.items()])

    def is_oud(kleur):
        if not any(all(abs(kleur[i] - t[i]) <= marge for i in range(3))
                   for t in OUDE_TINTEN):
            return None
        beste, beste_afstand, oud = None, None, False
        for tint, naam, van_vroeger in referenties:
            d = sum((kleur[i] - tint[i]) ** 2 for i in range(3))
            if beste_afstand is None or d < beste_afstand:
                beste_afstand, beste, oud = d, naam, van_vroeger
        return beste if oud else None

    treffers = []
    for pad in sorted(WORTEL.glob('assets/**/*')):
        if pad.suffix.lower() not in ('.webp', '.png', '.jpg', '.jpeg'):
            continue
        if 'bron' in pad.parts or 'origineel' in pad.parts:
            continue          # archief, gaat niet mee met de site
        try:
            im = Image.open(pad).convert('RGB')
        except Exception:
            continue
        im.thumbnail((160, 160))
        tel = collections.Counter(im.getdata())
        if len(tel) > max_kleuren:
            continue          # foto, geen vlak beeld
        aantal = sum(tel.values())
        per_tint = collections.Counter()
        for kleur, n in tel.items():
            naam = is_oud(kleur)
            if naam:
                per_tint[naam] += n
        for naam, n in per_tint.items():
            deel = n / aantal * 100
            if deel >= drempel:
                treffers.append(f'{pad.relative_to(WORTEL)}: {deel:.0f}% {naam}')
    return treffers


def tekst(el):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', el)).strip()


def main():
    print(f'EINDCONTROLE ({len(PAGINAS)} pagina\'s)\n')
    fouten = []
    bestanden = {p.name for p in PAGINAS}
    titels, omschrijvingen = collections.defaultdict(list), collections.defaultdict(list)
    markeringen = 0

    kapot, geen_h1, sprongen, leeg_alinea, geen_alt, dubbel_nav = [], [], [], [], [], []

    for p in PAGINAS:
        h = p.read_text(encoding='utf-8')

        # interne links
        for m in re.finditer(r'href="(?!https?:|mailto:|tel:|#)([^"#?]+)', h):
            doel = m.group(1)
            if doel.endswith('.html') and doel not in bestanden:
                kapot.append(f'{p.name} -> {doel}')

        # koppen
        h1 = re.findall(r'<h1\b', h)
        if len(h1) != 1:
            geen_h1.append(f'{p.name} ({len(h1)})')
        niveaus = [int(m.group(1)) for m in re.finditer(r'<h([1-6])\b', h)]
        vorig = 0
        for n in niveaus:
            if vorig and n > vorig + 1:
                sprongen.append(f'{p.name}: h{vorig} -> h{n}')
            vorig = n

        # title en omschrijving
        t = re.search(r'<title>(.*?)</title>', h, re.S)
        d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
        titels[tekst(t.group(1)) if t else ''].append(p.name)
        omschrijvingen[tekst(d.group(1)) if d else ''].append(p.name)

        # Lege alinea's. Een live region mag wél leeg zijn: die wordt door
        # JavaScript gevuld, en hij moet al in de DOM staan voordat er iets in
        # komt, anders kondigt een schermlezer de wijziging niet aan. Zo werkt
        # de tellerregel op projecten.html.
        for m in re.finditer(r'<p((?:[^>"]|"[^"]*")*)>\s*</p>', h):
            attr = m.group(1)
            if 'aria-live' in attr or 'role="status"' in attr:
                continue
            leeg_alinea.append(p.name)
        for m in re.finditer(r'<img\b((?:[^>"]|"[^"]*")*)>', h):
            if 'alt=' not in m.group(1):
                geen_alt.append(p.name)

        # dubbele labels in de balk
        nav = re.search(r'<nav class="submenu".*?</nav>', h, re.S)
        if nav:
            labels = [tekst(x.group(2)) for x in
                      re.finditer(r'<(a|button)[^>]*>(.*?)</\1>', nav.group(), re.S)]
            labels = [l for l in labels if l]
            for label, aantal in collections.Counter(labels).items():
                if aantal > 1:
                    dubbel_nav.append(f'{p.name}: "{label}" {aantal}x')

        markeringen += len(re.findall(r'\[CONTENT NODIG\]', h))

    def regel(naam, lijst, toon=3):
        vlag = 'FOUT' if lijst else 'ok  '
        extra = f'  {lijst[:toon]}' if lijst else ''
        print(f'  {vlag} {naam:34s} {len(lijst)}{extra}')
        if lijst:
            fouten.append(naam)

    regel('kapotte interne links', kapot)
    regel('pagina\'s zonder precies 1 h1', geen_h1)
    regel('sprongen in koppenniveaus', sprongen)
    regel('lege alinea\'s', leeg_alinea)
    regel('afbeeldingen zonder alt', sorted(set(geen_alt)))
    regel('dubbele labels in de navigatie', dubbel_nav)

    for veld, kaart in (('title', titels), ('omschrijving', omschrijvingen)):
        dubbel = {k: v for k, v in kaart.items() if k and len(v) > 1}
        leeg = kaart.get('', [])
        regel(f'dubbele {veld}', [f'{k[:30]}: {v}' for k, v in dubbel.items()], 1)
        regel(f'lege {veld}', leeg)

    for patroon, label in VERBODEN:
        treffers = [p.name for p in PAGINAS
                    if re.search(patroon, p.read_text(encoding='utf-8'))]
        regel(label, treffers)

    # De oude merktinten als rgb-getallen, in de pagina's én in de bron-CSS. De
    # pagina's dragen de pagina-stylesheets in een <style> mee, dus daar komt
    # zo'n waarde ook in terecht; styleguide.css wordt als los bestand geladen
    # en moet daarom apart nagekeken worden.
    rgb_treffers = []
    for p in PAGINAS:
        for vondst in oude_tint_als_rgb(p.read_text(encoding='utf-8')):
            rgb_treffers.append(f'{p.name}: {vondst}')
    for c in sorted(WORTEL.glob('*.css')):
        if c.name.endswith('.min.css'):
            continue
        inhoud = re.sub(r'/\*.*?\*/', '', c.read_text(encoding='utf-8'), flags=re.S)
        for vondst in oude_tint_als_rgb(inhoud):
            rgb_treffers.append(f'{c.name}: {vondst}')
    regel('oude merkkleur als rgb()', rgb_treffers, 2)

    beeld = merkkleur_in_beeld()
    if beeld is None:
        print('  n.v.t. oude merkkleur in beeld            (PIL niet aanwezig)')
    else:
        regel('oude merkkleur in beeld', beeld, 2)

    print(f'\n  [CONTENT NODIG]-markeringen: {markeringen} (bewust: ontbrekende brondata)')
    print('\nRESULTAAT: ' + ('ALLES OK' if not fouten else 'AANDACHT: ' + ', '.join(fouten)))
    return 1 if fouten else 0


if __name__ == '__main__':
    sys.exit(main())
