# assets/patronen: het merkpatroon

Aangeleverd door Jesse. De PNG's staan onveranderd in `bron/`; oudere versies
liggen ernaast in `bron/v3/`, `bron/v2/` en `bron/v1/`.

- `Hero.png` is versie 3, 10 september 2026.
- `cta.png` is versie 4, 10 september 2026: hetzelfde patroon met een **leeg
  midden**. De vorige staat in `bron/v3/cta.png`.

De omgezette bestanden heten `-v5-`. Die teller loopt op de omzetting en niet
op de bron: v4 was v3 zonder het omgekleurde groen, v5 is de nieuwe CTA-bron met
het lege midden. De versie zit in de naam omdat DEPLOY.md dertig dagen cache op
beeld zet; zie onderaan.

| bron | maat | waarvoor |
|---|---|---|
| `cta.png` | 2880 × 760 (3,79:1) | achtergrond van het contactvlak |
| `Hero.png` | 1440 × 940 (1,53:1) | de hero, op beide breekpunten |

De twee kleuren van het aangeleverde patroon: navy `#002848` en groen `#00B767`.

Omzetten gebeurt met:

```bash
python3 _generator/maak_patronen.py
```

## Eén bestand voor de hero, geen aparte mobiele variant

Versie 2 had drie bronbestanden, waaronder een vierkante speciaal voor de
telefoon. Versie 3 van de bron heeft één liggende compositie, en die snijdt op beide plekken
goed bij: naast de kop op ongeveer 1,65:1, en op een telefoon als brede band op
7:3. De diagonalen zijn grote vlakken, dus een strook door het midden leest nog
steeds als het patroon. Beide uitsneden zijn nagekeken voordat het aparte
bestand eruit ging.

Hoe groot het vak is bepaalt de stylesheet, niet het bestand. Reden: de vaste
balk ligt over de bovenkant van de pagina, en die is een vast aantal pixels hoog
terwijl het vak meeschaalt met de breedte. Op een telefoon is het vak daarom 7:3
**plus** de hoogte van de balk; onder de balk staat dan precies 7:3 aan patroon.

## Beide varianten houden de aangeleverde kleuren

Navy `#002848` met groen `#00B767`, in de hero én op het contactvlak.

Dat was tot 10 september 2026 anders, en het is nuttig om te weten waarom het
veranderd is. Op het contactvlak staat witte tekst middenop het patroon, en wit
op `#00B767` haalt **2,64:1** tegen een eis van 4,5:1 voor tekst en 3:1 voor de
kop. Er zijn drie oplossingen geprobeerd, in deze volgorde:

1. **Het groen omkleuren** naar `#1B7A48`, een dieper groen dat over elke pixel
   gemeten 5,35:1 haalde. Het werkte, maar het kostte de merkkleur: het blok
   las als dof groen met een donkere waas erover, terwijl die waas de bitmap
   zelf was. Dat was ook de klacht erover, "haal hier de zwarte filter weg", en
   er lag geen filter.
2. **De tekst op een massief navy vlak** middenin, met het patroon eromheen.
   Leesbaar (wit op `#081729` is 18,03:1), maar het legde een zichtbaar blok
   over het patroon.
3. **Het middelste groene vlak uit het patroon halen.** Dat is wat er nu staat.

## Het CTA-patroon heeft een leeg midden

De tekst staat gecentreerd, dus het midden moet navy zijn. De aangeleverde
`cta.png` is daarop gemaakt: waar versie 3 drie groene vormen had, heeft deze
alleen het parallellogram linksonder en de kubus rechts, met navy ertussen.
`maak_patronen.py` zet hem verder ongewijzigd om.

Gemeten over de echte pixels, op 375, 768, 1024 en 1440 px breed en op 1x en
2x, met de uitsnede die `background-size: cover` maakt: **elk tekstvak staat
voor 100% op navy, 15,03:1**. De krapste vrije ruimte tussen de tekst en het
groen is 92 px, bij de alinea op 1440.

### Op een telefoon is dit blok egaal navy

Het contactvlak is op 375 px ongeveer 375 x 450, dus 0,83:1, en het patroon is
3,79:1. `cover` snijdt daar zo hard uit het midden dat er van de groene vormen
niets in beeld komt. Dat is geen fout maar het gevolg van een leeg midden: waar
de tekst op navy moet staan, staat op een smal blok alleen nog navy.

Wil je daar toch patroon zien, dan is er een aparte uitsnede voor die maat
nodig die zelf ook een leeg midden heeft, zoals de hero-variant die in versie 2
had. Een andere `background-size` lost het niet op: bij een volledige breedte
valt de tekst over het parallellogram en over de kubus, en dan staat wit weer
op groen.

### Waarom geen waas over het patroon

Een waas van 35% navy over het felle groen haalt de eis ook (4,70:1). Maar die
duwt het groen naar `#04845b`, en dat is teal en geen merkkleur. Bovendien is
een waas precies wat het omgekleurde groen leek te zijn, en dat was de klacht.
Het codevoorbeeld staat nog in `styleguide.css` bij `.cta-slot__hoofd`.

## Lossless WebP, en waarom dat hier kleiner is

Het zijn twee vlakke kleuren met harde diagonalen. Gemeten op de 1440-variant:

| | grootte | unieke kleuren |
|---|---|---|
| PNG (bron) | 21,6 kB | 285 |
| lossy `-q 88` | 10,9 kB | **4048** |
| lossless | 8,1 kB | 285 |

Lossy is groter én maakt er vierduizend kleuren van: dat is franje langs de
diagonalen. Lossless is kleiner en pixelexact, dus die keuze is geen afweging.
Alle vijf de bestanden samen zijn 28 kB.

## Klemmen na het verkleinen

`maak_patronen.py` verkleint eerst en zet daarna elke pixel terug op de lijn
tussen de twee kleuren. Dat is nodig omdat Lanczos op een harde diagonaal
doorschiet tot voorbij de eindkleur: in de eerste poging leverde dat in de
1440-variant één pixel `#1f8848` op, lichter dan het groen zelf, die met wit
4,49:1 haalde in plaats van 4,50. Door te klemmen kan geen pixel lichter worden
dan de eindkleur en klopt de meting over elke pixel met wat de kleuren beloven.
