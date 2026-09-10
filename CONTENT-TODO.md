# Wat er nog van Steel Framing Holland nodig is

De site staat en is volledig. Alles hieronder is content die **niet op
www.steelframingholland.nl staat** en daarom niet is overgenomen. Er is niets
van geraden: waar een feit ontbreekt staat er niets, of `[CONTENT NODIG]` als
het veld anders leeg zou opvallen.

De lijst staat op volgorde van hoeveel het oplevert.

---

## 1. Projectverhalen — het grootste gat

**Wat er nu staat.** Per project: de titel, de plaats, de datum, soms een
opdrachtgever, en de fotoreeks. Plus één regel die zegt wat voor bouwwerk het
is en wat er op de foto's te zien is.

**Wat er niet staat.** Geen opgave, geen uitdaging, geen aanpak en geen
resultaat. De bronpagina's hebben die niet: onder de titel staan alleen die
gegevens en daarna de foto's.

Dat is bewust niet opgevuld. Een "uitdaging" en een "resultaat" bedenken bij een
echt project van een echte opdrachtgever is precies wat een case study
waardeloos maakt, en het is niet te verdedigen tegenover die opdrachtgever.

**Wat er nodig is.** Per project vier of vijf regels:

| vraag | voorbeeld van wat er nodig is |
|---|---|
| Wat moest er gebeuren? | "Twee verdiepingen op een portiekflat uit 1962, met de bewoners erin." |
| Wat maakte het lastig? | "De fundering kon geen zwaardere opbouw dragen." |
| Wat hebben jullie gedaan? | "Frame in de werkplaats voorgemonteerd en in delen aangevoerd." |
| Wat is het resultaat? | "Achttien woningen erbij, in elf weken." |
| Welke rol hadden jullie? | engineering / fabricage / montage / alle drie |

Begin bij de tien projecten die vooraan staan op `projecten.html`; die worden
het meest bekeken. De teksten komen in `PROJECT_COPY` in
`_generator/inhoud_copy.py`.

**Wat het oplevert.** Een projectpagina wordt nu bekeken en weer verlaten. Met
deze vijf regels wordt het bewijs: een bezoeker met een vergelijkbare opgave
herkent zichzelf en belt.

---

## 2. Referenties

**Wat er nu staat.** Niets. Het template had een citatenslider; die is
weggehaald omdat de drie citaten die erin stonden verzonnen waren.

**Wat er nodig is.** Drie tot vijf uitspraken van opdrachtgevers, met naam en
functie of bedrijf, en toestemming om ze te gebruiken. Één alinea per stuk is
genoeg.

De bron noemt vijf opdrachtgevers bij naam, dus daar is een begin: Dura Vermeer
(ABC Cluster, Amersfoort), Van Rhijn Bouw (Apparterra, Heemskerk), Van der Leij
Bouwprojecten (gevelrenovatie Amsterdam), Sherton (Nes aan de Amstel) en
Corzilius (Bonaire).

Het component staat nog in de git-historie van `_generator/schil.py` en de CSS
ervoor (`.quote-*`) staat nog in `styleguide.css`, dus terugzetten is een klein
klusje.

---

## 3. Bedrijfsgegevens die nu ontbreken

| wat | waar het hoort | waarom het nodig is |
|---|---|---|
| **KvK-nummer** | voettekst, contactpagina, JSON-LD | hoort bij een zakelijke site en telt mee voor vertrouwen |
| **BTW-nummer** | voettekst | idem |
| **Openingstijden** | contactpagina, telefoonvlak | de bron zegt alleen "tijdens kantooruren" |
| **Oprichtingsjaar** | over ons, JSON-LD `foundingDate` | "sinds jaartal" is het goedkoopste vertrouwenssignaal dat er is |
| **Aantal medewerkers** | over ons | maakt "eigen engineers en een vast team monteurs" concreet |
| **Certificeringen en keurmerken** | over ons, dienstpagina's | in de bouw wordt hierop geselecteerd |

Deze staan in `_generator/sfh/contact.json` op `[CONTENT NIET GEVONDEN]`.

---

## 4. Pagina's die zijn vervallen

Het template had vier pagina's die hier niet konden bestaan, omdat de bronsite
er geen enkel feit voor levert:

- **Het team.** De bron noemt geen medewerker, geen functie en geen aantal.
- **Historie.** Geen oprichtingsjaar en geen geschiedenis.
- **Registerconstructeur.** Geen constructeur en geen registratie genoemd.
- **Vacatures.** Geen vacatures.

De bouwfuncties ervoor staan in de git-historie van `_generator/bouw_bedrijf.py`
en de CSS is niet aangeraakt, dus terugzetten kan zodra de content er is.

**Het team is hiervan de interessantste.** Deze site verkoopt "zes stappen, één
partij, eigen mensen". Gezichten bij die mensen maken dat verhaal af. Nodig:
vier tot acht namen met functie en een foto, en één regel over wat die persoon
doet.

---

## 5. Beeldmateriaal

Wat er is, is bruikbaar: 138 beelden, allemaal echt eigen werk. Maar:

**Het logo is te klein.** Het bestand op de bronsite is 275×89 pixels. In de
balk staat het op 124×40, dus er is net genoeg voor een 2×-scherm en niets over
voor 3×. **Een vectorversie (SVG of EPS) lost dit in één keer op** en is
waarschijnlijk het snelste punt op deze hele lijst.

**Drie partnerlogo's zijn opgeschaald** en daardoor iets zachter dan de andere
drie: Climate Construction (1,5×), Veerhouse Voda (1,8×) en Dutch Health (1,6×).
Vraag die partners om een logo op een transparante achtergrond. Van Finish
Profiles heeft de bronsite een logo met een grijze achtergrond en een
blokjespatroon; een variant zonder achtergrond staat mooier in de band.

**Vier projecten hebben alleen klein of staand beeld:**

| project | wat er is |
|---|---|
| Cité Soleil | 640×480, vijf foto's |
| Gevel renovatie | 640×478 |
| Hotel de Grote kerk in Hoorn | alleen staand, 3024×4032 |
| Bonaire off grid woning | 960×720 |

**Wat er verder zou helpen:** foto's van de productiefaciliteit en van het
wagenpark. De site vertelt drie keer dat die er zijn — dat is de kernpropositie
— maar er is geen enkele foto van. Nu staat er op de werkwijzepagina en bij
"over ons" een foto van monteurs op de bouwplaats, en dat is een omweg.

**De herofilm is machinaal gegenereerd.** Hij staat er sinds 10 september 2026
en doet zijn werk: transport, frames op de bouwplaats, montage, afgebouwd huis.
Precies het verhaal dat de kop ernaast vertelt. Maar voor een bedrijf met
vijfendertig echte projecten is eigen opnamemateriaal sterker, en het zou
tegelijk het gat hierboven dichten: één dag filmen in de productiefaciliteit en
op een montage levert zowel de film als de ontbrekende foto's. Zie
`assets/video/HERKOMST.md` voor wat er technisch met de film is gedaan en hoe je
een nieuwe doormeet.

Van twee projecten stonden de themavelden op de bronsite nog op de
standaardtekst (`voortgang-woning-azoren-pico` had `Date: YOUR_TEXT`,
`thema-dreven-portiek-flats-utrecht` en `voortgang-woning-azoren-pico` hadden
"This is the default portfolio custom title" als H1). Die zijn hier niet
overgenomen; de plaats is uit de titel gehaald. Datum en opdrachtgever van die
twee zijn dus nog onbekend.

---

## 6. Het contactformulier verstuurt nog niets

`ENDPOINT` in `contactformulier.js` is leeg. Zolang dat zo is doet het formulier
niets: iemand vult het in, klikt op versturen en er gebeurt niets.

Dit gold al voor het template en is met deze ombouw niet veranderd, maar het is
het enige punt op deze lijst dat **een bezoeker die wil kopen tegenhoudt.**
Zet er een endpoint in (een eigen mailscript, Formspree, of wat de host biedt).

---

## 7. Privacybeleid en cookieverklaring

De bronsite heeft geen van beide, en ook geen AVG-passage bij het formulier.

`privacybeleid.html` en `cookies.html` bestaan wel, want de cookiemelding linkt
ernaar, maar ze staan half leeg met een markering erin. Wat erin moet:

- welke gegevens het formulier vastlegt, en op welke grondslag;
- hoe lang ze worden bewaard en met wie ze worden gedeeld;
- hoe iemand zijn gegevens kan opvragen of laten verwijderen;
- welke cookies de site plaatst: naam, doel en bewaartermijn per cookie.

Dat laatste kan pas als bekend is welk statistiekpakket wordt gebruikt.
`META_ID` in `analytics.js` is nu leeg, dus er wordt niets gemeten en er wordt
geen enkel script van Google geladen.

Een verzonnen privacyverklaring is juridisch onjuiste tekst, dus die staat er
niet.

---

## 8. Twee partners zonder omschrijving

De bronsite laat zes partners zien maar zegt bij twee niet waarvoor ze er zijn:
**Veerhouse Voda** en **Dutch Health**. Op `partners.html` staat bij die twee
alleen de naam met een link naar hun site.

Eén regel per partner is genoeg: wat leveren ze, of waarin werken jullie samen.
Ze staan in `_generator/sfh/company.json` onder `partners`.

---

## 9. Is Urgent Wonen nog actueel?

Op `partners.html` staat een blok over Urgent Wonen, de samenwerking met Van der
Leij Bouwbedrijven en Veerhuis Bouwsystemen voor tijdelijke huisvesting. Het
nieuwsbericht waar dat op is gebaseerd is van oktober 2018.

Als het nog loopt, verdient het meer dan een blok op de partnerpagina: het is
een compleet propositieverhaal met een eigen doelgroep. Als het niet meer loopt,
kan het blok eruit.

---

## 10. Domein en canonical

`BASIS` in `_generator/schil.py` staat op `https://www.steelframingholland.nl`.
Daar komen de canonical-links, de sitemap en de deelafbeelding uit. Komt de site
op een ander domein, dan moet die regel mee.

---

## Wat er bewust níét op deze lijst staat

Doorlooptijden, prijzen, besparingspercentages en garanties. Die zouden de
teksten sterker maken ("in elf weken", "30% goedkoper"), maar het zijn
uitspraken die alleen Steel Framing Holland kan doen en die hard moeten zijn.
Levert u ze aan, dan kunnen ze erin — maar dan als cijfer dat klopt, niet als
sfeerbeeld.
