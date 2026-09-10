# assets/patronen: het merkpatroon

Aangeleverd door Jesse, versie 2 op 2 september 2026. De PNG's staan onveranderd
in `bron/`; de eerste versie ligt ernaast in `bron/v1/`.

| bron | maat | waarvoor |
|---|---|---|
| `CTA.SECTION.BACKGROUND.png` | 2880 x 760 (3,79:1) | achtergrond van het contactvlak |
| `HERO.SECTION.png` | 1440 x 940 (1,53:1) | hero vanaf 768px |
| `HERO.SECTION2.png` | 1440 x 1440 (1:1) | hero tot 767px, cover snijdt bij |

Omgezet naar WebP met `cwebp -q 88 -m 6`. Het zijn vlakke verlopen, dus dat
comprimeert extreem goed: samen 125 kB tegen 3,0 MB als PNG.

## De uitsnede staat in de stylesheet, niet in het bestand

Beide herobestanden worden onveranderd geexporteerd; hoe groot het vak is
bepaalt de stylesheet. Reden: de vaste balk ligt over de bovenkant van de
pagina, en die is een vast aantal pixels hoog terwijl het vak meeschaalt met de
breedte. Een vaste uitsnede in het bestand kan dat niet opvangen.

Op een telefoon is het vak daarom 7:3 (de verhouding uit de referentie, gemeten
over vier schermafdrukken: 2,27, 2,29, 2,29 en 2,42) **plus** de hoogte van de
balk. Onder de balk staat dan precies 7:3 aan patroon. Het bronbestand is
vierkant zodat `cover` verticaal wat over heeft.

Vanaf 768px is de hero een balkhoogte hoger dan hij was, zodat er onder de balk
net zoveel patroon staat als bedoeld: 1,65:1 op 1440px.

## Waarom het patroon in het contactvlak op 30% staat

De tekst staat gecentreerd midden op dat vlak, en daar lopen de gele stralen
doorheen. Wit op de felste pixel van het patroon haalt 1,17:1, tegen een eis van
4,5:1. Er ligt daarom een waas van het diepe petrol overheen.

Doorgerekend over elke pixel van het patroon, dus bij welke uitsnede dan ook, is
36% de bovengrens waarbij wit overal nog 4,5:1 haalt. Op 30% is dat 5,26:1.

Op volle sterkte kan het patroon dus alleen waar geen tekst overheen staat.
