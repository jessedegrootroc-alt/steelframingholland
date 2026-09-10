# assets/patronen: het merkpatroon

Aangeleverd door Jesse, **versie 3 op 10 september 2026**. De PNG's staan
onveranderd in `bron/`; de vorige twee versies liggen ernaast in `bron/v2/` en
`bron/v1/`.

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
telefoon. Versie 3 heeft één liggende compositie, en die snijdt op beide plekken
goed bij: naast de kop op ongeveer 1,65:1, en op een telefoon als brede band op
7:3. De diagonalen zijn grote vlakken, dus een strook door het midden leest nog
steeds als het patroon. Beide uitsneden zijn nagekeken voordat het aparte
bestand eruit ging.

Hoe groot het vak is bepaalt de stylesheet, niet het bestand. Reden: de vaste
balk ligt over de bovenkant van de pagina, en die is een vast aantal pixels hoog
terwijl het vak meeschaalt met de breedte. Op een telefoon is het vak daarom 7:3
**plus** de hoogte van de balk; onder de balk staat dan precies 7:3 aan patroon.

## Het contactvlak krijgt een omgekleurde variant

Op het contactvlak staat witte tekst middenop het patroon. Wit op het
aangeleverde groen `#00B767` haalt **2,64:1**, tegen een eis van 4,5:1 voor
tekst en 3:1 voor de kop. Onleesbaar, en dat is met een schermafdruk ook gewoon
te zien.

In de CTA-variant is dat groen daarom `#1B7A48` geworden, een dieper groen.
Gemeten over elke pixel van beide bitmaps: **5,35:1**, en geen enkele pixel
onder 4,5.

**Dit is de enige plek op de site waar dat diepere groen nog staat.** Overal
elders is het accent `#00B767`, precies zoals aangeleverd; daar staat navy tekst
op in plaats van wit (5,76:1), en zo kon de kleur letterlijk worden overgenomen.
Op dit patroon kan die truc niet: het is tweekleurig en de tekst loopt over
beide kleuren. Navy haalt op het groen 5,76:1, maar op het navy in datzelfde
patroon 1,01:1.

Wil je hier ook het volle `#00B767`, dan moet de tekst op een massief vlak
middenin komen te staan met het patroon eromheen. Zet dan `GROEN_LEESBAAR`
gelijk aan `GROEN` in `maak_patronen.py` en pas `.cta-slot__hoofd` aan.

De hero-variant is **niet** omgekleurd en houdt het felle groen. Daar staat geen
tekst over: de kop zit in het grijze vak ernaast.

### Waarom omkleuren en geen waas

Een waas van 35% navy over het felle groen haalt de eis ook (4,70:1). Maar die
duwt het groen naar `#04845b`, en dat is teal en geen merkkleur. Omkleuren houdt
het een groen, houdt de randen scherp en voegt geen laag toe.

Wil je toch de waas, dan staat het codevoorbeeld in `styleguide.css` bij
`.cta-slot__hoofd`.

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
