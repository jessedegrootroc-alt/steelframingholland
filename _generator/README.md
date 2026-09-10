# _generator

De 51 HTML-pagina's in de hoofdmap worden hier gemaakt en zijn dus
**gegenereerde bestanden**. Pas je een pagina met de hand aan, dan is die
wijziging weg zodra hier iets opnieuw draait.

```
python3 bouw_alles.py
```

Dat schrijft alle pagina's opnieuw. `bouw_alles.py` roept de andere scripts aan:

| bestand | wat het maakt |
|---|---|
| `schil.py` | de gedeelde onderdelen: balk, voettekst, hero's, knoppen, kaarten, beeld |
| `bouw_home.py` | `index.html` |
| `bouw_dienst.py` | de 3 toepassingen en de 4 techniekpagina's |
| `bouw_projecten.py` | `projecten.html` en de 35 projectpagina's |
| `bouw_bedrijf.py` | over ons, werkwijze, partners |
| `bouw_contact.py` | contact, offerte, privacybeleid, cookies |
| `bouw_sitemap.py` | `sitemap.xml` en `robots.txt` |

## Waar de inhoud staat

De site heeft drie contentlagen. Dat onderscheid is niet cosmetisch: het is wat
scheidt wat **waar** is van wat **goed geformuleerd** is.

| bestand | wat erin staat |
|---|---|
| `sfh/` | de contentexport van www.steelframingholland.nl: bronteksten, ongewijzigd |
| `inhoud_sfh.py` | welke pagina's er zijn, welke foto waar hoort, onder welke noemer een project valt |
| `inhoud_copy.py` | de conversielaag: herschreven koppen, leads, CTA's, projectomschrijvingen en SEO |
| `inhoud_dienst_verhaal.py` | de verhaallaag: situaties, processtappen, oplevering, voordelen, vragen |

Bovenaan elk van die bestanden staat wat er wel en niet in mag. De korte versie:

**`sfh/` is de waarheid.** Elk bedrijfsfeit op de site moet hierin terug te
vinden zijn. Deze map is met de hand niet bewerkt behalve op één punt: schrijfwijze
van waarden die de bron zelf geeft (`Mei2011` → `Mei 2011`, `ibiza` → `Ibiza`,
`Zwolle - Nederland` → `Zwolle`). Twee projecten heetten in de bron beide
"Woonhuis"; die hebben hun plaats in de titel gekregen om ze te kunnen
onderscheiden. Elke wijziging staat als commentaar in het script dat de export
maakte.

**`inhoud_copy.py` is de formulering.** Dezelfde feiten, anders gezegd. De
bronsite legt uit wat staalframebouw is; deze laag zegt wat de bezoeker eraan
heeft. Nagerekend: er staat geen dienst, cijfer, certificering of
bedrijfsclaim in die niet uit `sfh/` komt.

**`inhoud_dienst_verhaal.py` is de vakinhoud.** Twee soorten:

- Uit de bron: de vijf processtappen (van `/werkwijze/`), de bewerkingen die op
  een profiel kunnen, en de voordelen (eigen engineers, eigen
  productiefaciliteit, eigen wagenpark, C100 in eigen beheer, stapelen tot zes
  verdiepingen, combineren met warmgewalst staal).
- Algemene vakinhoud: dat koudgevormd staal maatvast is, dat een lichte
  constructie bij optoppen de extra belasting beperkt, en dat naoorlogse
  portiekflats zich daar goed voor lenen. Dat zijn eigenschappen van de
  bouwmethode, geen beweringen over dit bedrijf. Zulke uitleg staat nooit in de
  eerste persoon en nooit als belofte.

Wat er níét in staat: doorlooptijden, tarieven, besparingspercentages,
certificaten, klantnamen buiten de bron, aantallen en garanties.

## Twee bewuste keuzes in de copylaag

- **De H1 van een dienstpagina is de dienstnaam zelf** ("Woningbouw"), niet de
  belofte. Dat houdt de kop gelijk aan het menu en aan waar mensen op zoeken;
  het voordeel staat in de lead eronder en in de eerste H2 ("Voor wie wij
  woningen bouwen"). Alleen de homepage, `projecten.html` en `over-ons.html`
  hebben een H1 die wél een belofte is.
- **Op een projectpagina staat geen verzonnen verhaal.** De bronpagina's hebben
  geen projectomschrijving: onder de titel staan alleen datum, plaats en soms
  een opdrachtgever, en daarna de foto's. De regel per project in `PROJECT_COPY`
  zegt daarom precies twee dingen: wat voor bouwwerk het is, en wat er op de
  foto's te zien is. Geen opgave, geen uitdaging, geen resultaat. Daardoor is de
  fotoreeks op die pagina's het bewijs en niet de illustratie, en staat de
  galerij hoog op de pagina in plaats van onderaan. Zie punt 1 van
  `CONTENT-TODO.md`.

## Wat er uit het template is gehaald

Dit template is voor een ander bedrijf gebouwd. Bij de ombouw is eruit gegaan:

- **De citatenslider.** Daar stonden drie verzonnen referenties in, op naam van
  "Architect", "Aannemer" en "Particuliere opdrachtgever". Steel Framing Holland
  heeft geen referenties op zijn site, dus is de sectie weg. Op de homepage staat
  op die plek nu de werkwijze in vijf stappen, en die staat wél in de bron.
- **De band met klantlogo's.** Daar stonden dertien logo's van opdrachtgevers
  van de vorige eigenaar in (Alstom, Ballast Nedam, Stork en tien andere). Nu
  staan er de zes partners die de bronsite zelf laat zien.
- **Vier pagina's:** het team, historie, registerconstructeur en vacatures. De
  bron levert daarvoor geen enkel feit. Zie `CONTENT-TODO.md` punt 4.
- **De herofilm.** Twee filmbestanden van eerdere eigenaren. Er staat nu een
  foto van eigen werk.
- **`cursus.css`** en de stockfoto's van bouwplaatsen en cursussen: die werden
  door geen enkele pagina meer geladen.

## Beeld

`maak_assets.py` zet de afbeeldingen uit de export om naar responsive WebP. Dat
hoeft alleen als er beeld bijkomt of verandert:

```
python3 maak_assets.py
```

Het leest `beeldplan.json` (welke bron, welke rol, welke alt-tekst) en schrijft
`beeldmaten.json`, dat `schil.py` weer inleest. De bronbestanden staan in
`assets_bron/sfh/`; `beeldplan.json` houdt per beeld de volledige bron-URL bij
in het veld `herkomst`.

Het logo wordt hier niet gemaakt; dat was een eenmalige bewerking. Zie
`assets/logo/HERKOMST.md`.

## Snelheid

De optimalisaties van het template zijn niet aangeraakt en werken nog:
minificeren, de terugvalletter met dezelfde metriek, twee stylesheets in de
pagina in plaats van als los bestand, lage prioriteit voor beeld onder de vouw,
en een versiehash op elke lokale verwijzing.

Wat er bij deze ombouw is veranderd: de herofilm is eruit (dat scheelt een
verzoek en 1,4 MB) en er zijn twee CSS-regels van een pagina-stylesheet naar
`styleguide.css` verhuisd (`.trap`/`.trede` en `.case-bleed`), omdat de
componenten nu ook op pagina's staan die die stylesheet niet laden.

### Meten

```bash
python3 _generator/devserver.py 8081
npx lighthouse http://127.0.0.1:8081/index.html --view
```

Meet tegen `devserver.py` en niet tegen `python3 -m http.server`: die laatste
comprimeert niet en stuurt geen cache-headers, en dan meet je ongeveer vijf
punten te laag. Reken op een spreiding van vijf punten tussen runs; neem de
mediaan van vijf runs.

## Controleren

```bash
python3 _generator/eindcontrole.py
```

Kijkt niet of de site mooi is, maar of er niets kapot of dubbel is: kapotte
links, koppenniveaus, dubbele titles, dubbele labels in de navigatie, lege
alinea's, ontbrekende alt-teksten en resten van het vorige merk. Draai dit na
elke `bouw_alles.py`.

## Versiehash op CSS en JavaScript

Elke lokale stylesheet en elk lokaal script krijgt `?v=<acht tekens>` mee,
berekend uit de sha256 van de inhoud van dat bestand. Verandert het bestand, dan
verandert de hash en haalt de browser hem opnieuw op; verandert het niet, dan
blijft de cache werken. Dat gebeurt in `v()` in `schil.py`.

Let op: de lettertypen krijgen géén hash. Die worden aangeroepen uit
`@font-face` in `styleguide.css`, en dat pad kan het script niet bijwerken. Zou
de `<link rel="preload">` in de kop wél een hash krijgen en de `@font-face`
niet, dan zijn dat twee verschillende URL's en haalt de browser elk font twee
keer op.

## Let op: het uitvoerpad

De bouwscripts schrijven naar de map boven deze (`UIT = ...parent.parent`), dus
naar de hoofdmap van de site. Verplaats je `_generator/`, dan verhuist de
uitvoer mee.
