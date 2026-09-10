# Herkomst van de foto's

Alle foto's in deze map komen van **www.steelframingholland.nl** en zijn
eigendom van Steel Framing Holland. Ze zijn opgehaald van de mediabibliotheek
van die site (`/wp-content/uploads/`), in de hoogste resolutie die daar staat:
waar WordPress een verkleinde variant serveerde (`-1024x768` en dergelijke) is
het origineel zonder maatsuffix opgehaald.

De bestanden hier zijn de WebP-versies die `_generator/maak_assets.py` daarvan
maakt, in de breedtes die `foto()` in `_generator/schil.py` opvraagt. De
originelen staan in `_generator/assets_bron/sfh/`.

## Welke foto waar vandaan komt

`_generator/beeldplan.json` legt per beeldsleutel vast welk bronbestand het is,
met de volledige bron-URL in het veld `herkomst` en de oorspronkelijke
pixelmaat in `bronmaat`. `_generator/beeldmaten.json` houdt daarnaast bij welke
breedtes er van elk beeld bestaan.

## Waar op gelet is bij de keuze

- Per project is één beeld de hero en zijn er tot drie galerijbeelden. Geen
  beeld wordt op twee plaatsen als hero gebruikt.
- De hero's van de zeven dienstpagina's komen uit een ánder project dan het
  project waarvan dat beeld de hero is, zodat een bezoeker niet twee keer
  dezelfde foto ziet.
- Waar mogelijk is een liggend beeld gekozen: de hero's snijden op
  `object-fit: cover` en een staand beeld verliest daar te veel.

## Wat de bron niet heeft

Van vier projecten zijn alleen kleine of staande beelden beschikbaar
(Cité Soleil 640×480, Gevel renovatie 640×478, Hotel de Grote kerk in Hoorn
alleen staand 3024×4032, Bonaire off grid woning 960×720). Die zijn niet
opgeschaald; de ladder in `maak_assets.py` stopt bij de eigen breedte van het
origineel. Zie CONTENT-TODO.md.
