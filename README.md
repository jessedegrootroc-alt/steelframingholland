# Steel Framing Holland: website

Statische site: HTML, CSS en vanilla JavaScript, geen build-stap en geen
npm-afhankelijkheden. Van een CDN komen alleen GSAP (met ScrollTrigger en
ScrollSmoother) en Barba.js; samen doen die de pagina-overgangen en het vloeiende
scrollen. De lettertypen staan lokaal in `assets/fonts/`.

## Lokaal draaien

Open `index.html` in de browser, of draai een server vanuit deze map:

    python3 _generator/devserver.py 5501

Alle links zijn relatief, dus de map kan zonder aanpassing als eigen site
gepubliceerd worden.

## De pagina's zijn gegenereerd

De 51 HTML-bestanden in deze map worden gemaakt door de scripts in
`_generator/`. **Pas je een HTML-bestand met de hand aan, dan is die wijziging
weg zodra de generator opnieuw draait.**

    cd _generator && python3 bouw_alles.py

| bestand | wat het doet |
|---|---|
| `sfh/` | de contentexport van www.steelframingholland.nl: hier staan alle bronteksten |
| `inhoud_sfh.py` | welke pagina's er zijn, welke foto waar hoort, onder welke noemer een project valt |
| `inhoud_copy.py` | de conversielaag: herschreven koppen, leads, CTA's en de SEO-metadata |
| `inhoud_dienst_verhaal.py` | de verhaallaag: situaties, processtappen, oplevering, voordelen en vragen |
| `schil.py` | de gedeelde onderdelen: balk, voettekst, hero's, knoppen, kaarten, beeld |
| `bouw_home.py` | `index.html` |
| `bouw_dienst.py` | de 3 toepassingen en de 4 techniekpagina's |
| `bouw_projecten.py` | het projectenoverzicht en de 35 projectpagina's |
| `bouw_bedrijf.py` | over ons, werkwijze, partners |
| `bouw_contact.py` | contact, offerte, privacybeleid, cookies |
| `bouw_sitemap.py` | `sitemap.xml` en `robots.txt` |
| `maak_assets.py` | zet de beelden uit de export om naar responsive WebP (alleen nodig bij nieuw beeld) |
| `maak_patronen.py` | zet het merkpatroon om naar WebP (alleen nodig bij nieuw patroon) |

De CSS, de JavaScript en alles in `assets/` worden **niet** gegenereerd; die
bewerk je rechtstreeks.

## Waar de tekst vandaan komt

De site heeft drie contentlagen, en dat onderscheid is de kern van hoe hij in
elkaar zit:

1. **`sfh/` is de waarheid.** Dat is de contentexport van
   www.steelframingholland.nl: bronteksten, projectgegevens, contactgegevens en
   partners, ongewijzigd. Elk bedrijfsfeit op de site moet hierin terug te
   vinden zijn.
2. **`inhoud_copy.py` is de formulering.** Dezelfde feiten, maar herschreven:
   korter, met de reden vooraan en de techniek als onderbouwing erachter. De
   bronsite legt uit wat staalframebouw is; deze laag zegt wat de bezoeker
   eraan heeft.
3. **`inhoud_dienst_verhaal.py` is de vakinhoud.** Situaties, processtappen,
   wat je krijgt en de veelgestelde vragen. De vijf processtappen en de
   voordelen komen uit de bron; dat koudgevormd staal maatvast is en dat een
   lichte constructie bij optoppen minder belasting geeft, is algemene
   vakinhoud over de bouwmethode en geen bewering over dit bedrijf.

Bovenaan elk van die bestanden staat precies wat er wel en niet in mag. Wat de
bron niet geeft, staat als `[CONTENT NODIG]` op de pagina of helemaal niet, en
in `CONTENT-TODO.md`.

## Structuur

```
index.html                  Home

woningbouw.html             ┐
renovatie.html              ├ drie toepassingen: waarvoor bouw je
utiliteitsbouw.html         ┘

ontwerpen-tekenen-en-berekenen.html  ┐
lichtgewicht-staalframe.html         ├ vier techniekpagina's: waarmee bouw je
eps-wandsysteem.html                 │
overige-wandsystemen.html            ┘

projecten.html              overzicht met filter op noemer
project-*.html              35 projectpagina's

over-ons.html  werkwijze.html  partners.html
offerte.html   contact.html
privacybeleid.html  cookies.html

brand-style.md              de merklaag: kleuren en typografie
STYLEGUIDE.md               het ontwerpsysteem en waar deze site afwijkt
SECTIONS.md                 het sectieskelet dat de pagina's delen
CONTENT-TODO.md             wat er nog van Steel Framing Holland nodig is
```

## Werken aan deze site

- Een brontekst wijzigen: in `_generator/sfh/`, daarna opnieuw bouwen.
- Een kop, lead of CTA wijzigen: in `_generator/inhoud_copy.py`.
- Een nieuw project of een nieuwe dienst: één regel in `inhoud_sfh.py`.
- Nieuwe kleuren of fonts: alleen de tokens in `styleguide.css`, zie `brand-style.md`.
- Het contactformulier verstuurt nog niets: zet het endpoint in `contactformulier.js`.
- Statistieken laden pas na toestemming en alleen met een meet-ID in `analytics.js`.
- Na een wijziging in een `.css`- of `.js`-bestand moet je opnieuw bouwen, anders
  verwijzen de pagina's naar de oude `.min`-versie.

## Controleren

    python3 _generator/eindcontrole.py

Kijkt niet of de site mooi is, maar of er niets kapot of dubbel is: kapotte
links, koppenniveaus, dubbele titles, lege alinea's, ontbrekende alt-teksten en
resten van het vorige merk. Draai dit na elke `bouw_alles.py`.
