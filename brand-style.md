# Merklaag: Steel Framing Holland

Dit document beschrijft de merklaag van deze site: welke kleuren en letters er
zijn, waar ze vandaan komen, en welke daarvan je mag aanraken.

De vorige versie van dit bestand was het beslislog van het merk waarvoor dit
template oorspronkelijk is gebouwd. Dat log hoorde bij een ander palet en bij
metingen op andere kleuren; het staat in `_backup-template-duyts.tar.gz` en in
de git-historie. Wat hier staat gaat over de huidige site en de cijfers zijn
opnieuw gemeten.

---

## 1. Waar de kleuren vandaan komen

Uit het logo, en uit niets anders. Het logobestand van de bronsite
(`logo_website_steel_framing_holland.png`, 275×89) heeft 6.723 dekkende pixels,
en die zijn als volgt verdeeld:

| tint | aandeel | hex |
|---|---|---|
| navy | 80,3% | `#0D2646` (waarvan 75,4% exact deze waarde) |
| groen | 14,2% | `#30B36D` |
| lichtgroen | 3,8% | `#BCDA83` |

Navy is dus de merkkleur en groen het accent. Dat is precies de verhouding die
het template als 30/10 gebruikt, dus die vertaling was rechtstreeks.

### Eén aanpassing, en waarom

Het logogroen `#30B36D` haalt op wit **2,69:1**. Voor een link of een label is
4,5:1 nodig en voor een knopvorm 3:1, dus die kleur kan niet als accent op wit.

Daarom is het accent een verdiepte stap van datzelfde groen: **`#1B7A48`**, dat
op wit **5,35:1** haalt. Dezelfde tint, donkerder gezet tot hij leesbaar is.
Het logo zelf blijft onaangeraakt `#30B36D`; die kleur wordt alleen gebruikt
waar contrast geen rol speelt (in het logo, en in de witvariant op de donkere
balk, waar hij 5,64:1 haalt).

---

## 2. De acht tokens

Deze acht bepalen het merk. Verander je hier iets, dan verandert de hele site
mee; alles verderop in `styleguide.css` verwijst hiernaar.

```css
--color-primary:           #0D2646;  /* SFH Navy: merkvlakken (30%) */
--color-secondary:         #BCDA83;  /* SFH Lichtgroen: tekst OP donkere vlakken */
--color-accent:            #1B7A48;  /* SFH Groen verdiept: CTA, links, labels (10%) */
--color-background:        #FFFFFF;  /* de dominante basis (60%) */
--color-background-subtle: #F5F5F5;  /* rustige afwijkende achtergrond */
--color-text:              #383838;  /* koppen en lopende tekst */
--color-text-muted:        #636363;  /* ondersteunende tekst, captions, meta */
--color-border-soft:       #E6E6E6;  /* randen en scheidingen */
```

Plus drie afgeleide stappen, die er zijn omdat een merkvlak een hover en een
ingedrukte staat nodig heeft:

```css
--color-primary-deep:      #0A1E36;  /* haarlijnen, kleine labels, pressed */
--color-primary-deepest:   #081729;  /* donkerste vlak en de sluier over foto's */
--color-accent-strong:     #14603A;  /* accent een stap donkerder: hover en pressed */
```

De historische namen (`--color-geel`, `--color-groen`) staan er nog als alias en
verwijzen naar deze tokens. Ze heten zo omdat het template ooit geel en groen
gebruikte; de namen zijn niet omgezet omdat ze in honderden regels CSS staan en
een halve omzetting erger is dan een rare naam. Ze wijzen naar de juiste kleur.

---

## 3. De 60/30/10-verdeling

- **60% wit.** De basis. De meeste secties staan op wit of op `#F5F5F5`.
- **30% navy.** De merkvlakken: de balk als je gescrold hebt, het CTA-blok, de
  sluier over de hero, het vierde vlak van de vlakkenrij.
- **10% groen.** Knoppen, links, labels en het eerste vlak van de vlakkenrij.

De vlakkenrij op de contactpagina laat de vier rollen naast elkaar zien: groen,
grijs, wit, navy.

---

## 4. Gemeten contrast

Alles hieronder is opnieuw gerekend met de WCAG-formule op de huidige tokens.

| combinatie | ratio | eis |
|---|---|---|
| `--color-text` `#383838` op wit | 11,73:1 | AAA |
| `--color-text` op `#F5F5F5` | 10,76:1 | AAA |
| `--color-text-muted` `#636363` op wit | 6,01:1 | AA |
| `--color-primary` `#0D2646` op wit | 15,19:1 | AAA |
| wit op `--color-primary` | 15,19:1 | AAA |
| `--color-secondary` `#BCDA83` op `--color-primary` | 9,76:1 | AAA |
| `--color-accent` `#1B7A48` op wit | 5,35:1 | AA |
| `--color-accent` op `#F5F5F5` | 4,91:1 | AA |
| wit op `--color-accent` | 5,35:1 | AA |
| `--color-accent-strong` `#14603A` op wit | 7,60:1 | AAA |
| logogroen `#30B36D` op `--color-primary` | 5,64:1 | AA |

Twee dingen om te weten:

- **`--color-secondary` is geen tekstkleur op wit.** `#BCDA83` haalt daar
  1,56:1. Hij is bedoeld voor tekst en details **op** de navy vlakken, en daar
  haalt hij 9,76:1.
- **Het accent haalt AA, niet AAA.** 5,35:1 is genoeg voor lopende tekst en
  ruim genoeg voor labels en knopvormen, maar het is geen AAA. Dat is de prijs
  van een accent dat nog als het logogroen te herkennen is. Wil je AAA, dan moet
  het accent naar `#0F5C36` (8,06:1) en verliest het die herkenbaarheid.

---

## 5. Typografie

Ongewijzigd ten opzichte van het template. Twee families, lokaal in
`assets/fonts/`:

- **Assistant** voor koppen (`--font-heading`).
- **Karla** voor lopende tekst (`--font-regular`, `--font-medium`, `--font-light`).

Bovenaan `styleguide.css` staan twee `@font-face`-blokken die een
**terugvalletter met dezelfde metriek** definiëren: de systeemletter, op maat
gezet met `size-adjust` en overrides voor ascent en descent. Dat is er niet voor
de sier. Zonder die correctie tekent de browser de tekst eerst in de
systeemletter en daarna opnieuw in Assistant of Karla, met andere
regelafmetingen, en registreert Chrome die tweede tekening als de Largest
Contentful Paint: een halve seconde later en drie punten lager.

**De getallen in die blokken horen bij deze twee fontbestanden.** Wordt een font
vervangen, dan moeten ze opnieuw berekend worden.

---

## 6. Het logo

Twee varianten, beide in `assets/logo/`:

- `sfh-logo.webp` — de kleurversie, voor de witte balk.
- `sfh-logo-wit.webp` — voor de navy balk. Hierin zijn de navy delen wit
  gemaakt en is het groen behouden.

Dat laatste is een keuze en geen slordigheid. Een egaal wit silhouet maakt van
het kubusmerk een vlek, omdat de vorm het contrast tussen navy en groen nodig
heeft om te lezen. Met het groen erin blijft de kubus een kubus.

**Het bronbestand is 275×89 pixels en dat is klein.** In de balk staat het logo
op 124×40, dus er is net genoeg voor een 2×-scherm en niets over voor 3×. Een
vectorversie zou dit in één keer oplossen; dat staat in `CONTENT-TODO.md`.

---

## 7. Wat je wel en niet moet aanraken

**Wel:** de acht tokens in `:root` in `styleguide.css`, en de drie afgeleide
stappen. Dat is de merklaag.

**Niet:** de honderden regels eronder die naar die tokens verwijzen. Als het
merk verandert, verandert het daar. Staat er ergens een letterlijke hexwaarde in
plaats van een token, dan is dat een fout; `eindcontrole.py` controleert daarop
onder "oude merkkleur".
