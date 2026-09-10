> **Let op:** dit document beschreef het sectieskelet van de vorige site
> (cases, cursussen, drie diensten). De componenten en de sectievolgorde zijn
> nog steeds die van dit template en dus nog geldig, maar de paginanamen in de
> voorbeelden bestaan niet meer. De actuele indeling per paginatype staat in de
> docstrings van de bouwscripts in `_generator/`. Ook de kleuren en de
> contrastgetallen in dit document zijn die van vóór de merkwissel; de
> actuele meting staat in `brand-style.md` onder Accessibility.

# SECTIONS.md: het sectieskelet

De site heeft geen build-stap, dus er zijn geen includes of partials. Pagina's van
hetzelfde type delen hun structuur doordat ze **exact dezelfde sectie-ids, klassen
en volgorde** gebruiken. Dit bestand beschrijft dat skelet één keer.

Pas je een sectie aan, pas hem dan op alle pagina's van dat type aan.

---

## Wat elke pagina heeft

```html
<body>
  <a class="skip-link" href="#main-content">Naar de inhoud</a>

  <!-- alles met position:fixed staat BUITEN #smooth-wrapper -->
  <header class="header" id="siteHeader">…</header>
  <div class="mobile-panel--overlay" id="panelOverlay" hidden></div>
  <div class="mobile-panel" id="mobilePanel">…</div>

  <div id="smooth-wrapper">
    <div id="smooth-content">
      <div data-barba="wrapper">
        <div class="app__wrapper" data-barba="container" data-barba-namespace="…">
          <div class="content__wrapper">
            <main id="main-content">…secties…</main>
            <footer class="footer">…</footer>
            <script src="site.js"></script>
            <script src="contactformulier.js"></script>
          </div>
        </div>
      </div>
    </div>
  </div>

  <aside id="cookiebalk">…</aside>
  <!-- gsap, ScrollTrigger, ScrollSmoother, barba, cookiebalk.js,
       analytics.js, smooth-scroll.js, page-transitions.js -->
</body>
```

Regels die daarbij horen:

- **Het hoofdmenu heeft twee uitklappers: Diensten en Cursussen.** Een menu-item
  is in `NAV` (in het bouwscript) &oacute;f een gewone link &oacute;f een uitklapper met
  sublinks en een kaart. De sublinks komen uit `SERVICES` en `CURSUSSEN`, zodat
  een wijziging daar meteen in het menu, de voet en de overzichtspagina's landt.

  De uitklapvlakken staan in de HTML buiten `.header--container`: ze lopen over
  de volle breedte onder de balk door en dat kan niet binnen een flexrij. De
  balk is `position: fixed` en dus hun ankerpunt.

  Een gesloten vlak heeft `inert`: de links staan er wel voor een zoekmachine,
  maar je vangt ze niet met de tab-toets. Het vlak opent op klik en, met een
  muis, ook op hover; het sluit op Escape (focus terug naar de knop), bij een
  klik of focus buiten de balk, en bij scrollen, want de balk schuift dan namelijk
  omhoog uit beeld.

  Onder 1200px is de balk zelf al weg. Dezelfde items zijn daar accordeons in
  het mobiele paneel.

- **Alles wat `position: fixed` is hoort buiten `#smooth-wrapper`.** ScrollSmoother
  verschuift `#smooth-content` met een transform, en onder een transform hangt
  `fixed` aan dat element in plaats van aan het scherm. Dat geldt voor de header,
  het mobiele paneel met zijn overlay en de cookiemelding. Voeg je iets vasts toe,
  zet het daar dan bij.
- **De header en het paneel staan buiten de barba-container** en blijven dus staan
  bij een pagina-overgang. Welke menulink de huidige pagina is wordt daarom in
  `page-transitions.js` overgezet, en `site.js` haalt zijn oude listeners eraf via
  `window.__madegroVast`, anders opent het menu na drie pagina's ook drie keer.
- **Header, footer en paneel zijn per pagina echte HTML.** Ze moeten vindbaar zijn
  voor zoekmachines en werken zonder JavaScript. Ze staan dus twintig keer in de
  broncode; dat is bewust.
- **De scripts in de container** worden bij een pagina-overgang opnieuw uitgevoerd.
  Ze zoeken hun elementen binnen `document.currentScript.closest('[data-barba="container"]')`,
  want tijdens een overgang staan de oude en de nieuwe pagina even samen in de DOM.
  Uitzondering: wat op de vaste onderdelen slaat wordt op `document` gezocht, want
  die staan buiten de container.
- **Het contactformulier is het enige stuk HTML dat door JavaScript gemaakt wordt.**
  Het staat één keer in `contactformulier.js` en rendert in elke
  `<div data-contactformulier data-onderwerp="…">`. Daaronder staat een `<noscript>`
  met e-mailadres en telefoonnummer.
- **Sectie-ids zijn genummerd** (`s01-introductie`, `s02-…`). De nummering is de
  volgorde op de pagina en tegelijk de prioriteit uit de projectbrief.

---

## Rangorde in de knoppen

Er zijn twee niveaus:

| Niveau | Kleur | Waarvoor |
|---|---|---|
| primair | geel | diensten, cursussen en alles wat naar contact leidt |
| secundair | diepgroen (`button--secundair`) | alles wat naar een case leidt |

Diensten en cursussen zijn waar iemand voor komt; de cases zijn de onderbouwing
daarbij. Dat geldt voor de grote knop (`knop(..., "secundair")`), voor de ronde
icoonknop op een caserij (`icoonknop(maat, "button--secundair")`) en voor de
actieve filterpil op `cases.html`.

Het contactblok onder aan een casepagina blijft geel: dat is de conversie, niet
een verwijzing naar nog een case.

## De quotes

Op de homepage (`s08-testimonials`) en op de vier cursuspagina's
(`s10-ervaringen`) staat &eacute;&eacute;n citaat per keer groot uitgelicht: beeld links,
citaat rechts, een kort streepje boven de naam, en eronder twee pijlen met een
teller. Onder 768px komt het beeld boven de tekst.

Het beeld is liggend (16:10) en beslaat een derde van de rij. Het stond eerst
staand op 3:4 over bijna de helft: op de breedste maat, waar de container ophoudt
bij 1800px, was het 683 bij 911, en daarmee werd het beeld het onderwerp van
de sectie in plaats van wat er staat. Nu is het 547 bij 342, ruim zestig procent
lager. Het past ook beter bij de bronfoto's: die zijn allemaal liggend (3,3:1
tot 3:2), dus een staande uitsnede gooide er het meeste van weg.

Onder de naam staat `.quote__logo`: het logo van de opdrachtgever, op 32px hoog
met een breedtebegrenzing, net als in de logoband. De vijfde waarde in de
testimonial-lijst is de sleutel: staat hij in `OPDRACHTGEVERS` dan komt het echte
logo, staat hij in `PLAATSHOUDER_LOGOS` dan komt een voorlopig woordmerk (40px,
want die tekening heeft lucht onderin), en bij `None` een geel invulveld. Nu
staan er overal voorlopige woordmerken, want de citaten zijn verzonnen;
zie CONTENT-TODO.md.

De pijlen eronder zijn `.button--grijs`, niet geel: het is bediening en geen
actie.

Twee dingen om de hoogte stil te houden, want de citaten zijn niet even lang:

- **De marge tussen twee citaten** staat op
  `.quote:not([hidden]) + .quote:not([hidden])`. Met alleen `.quote + .quote`
  kreeg het tweede en derde citaat de marge ook als de slider draaide, want het
  citaat ervoor staat er dan nog wel, maar op `display: none`, en zag je
  64px witruimte verschijnen zodra je doorklikte.
- **Het beeld is zo hoog als het citaat ernaast.** Het staat absoluut in een vak
  dat met de rij meestrekt, dus de onderkant van de foto ligt gelijk met de
  onderkant van de naam. Onder 768px staat het beeld boven de tekst en heeft het
  geen buur meer om zich naar te richten; daar geldt weer 16:10 en gaat
  `align-items` terug naar `start`: bij `stretch` rekent `aspect-ratio` de
  breedte terug uit de rijhoogte en loopt de foto het scherm uit.
- **De wissel is een overvloeiing** van 350ms: het oude citaat in 150ms weg, het
  nieuwe daarna in 200ms erbij. Niet allebei tegelijk half doorzichtig, want dan
  liggen er twee foto's over elkaar.
- **De citaten liggen op elkaar** in &eacute;&eacute;n rastervak zodra de slider draait
  (`.quotes__venster--slider`, gezet door `site.js`). De rij is daardoor altijd
  zo hoog als het langste citaat en de pijlen eronder blijven staan; zonder dit
  sprong de nav 73px op en neer. De verborgen citaten staan op
  `visibility: hidden`, niet op `display: none`: dat haalt ze uit de tabvolgorde
  en uit wat een schermlezer voorleest, maar ze tellen wel mee voor de hoogte.
  Zonder JavaScript staat de klasse er niet en staan de citaten onder elkaar.

Er stonden hier eerder drie kleine kaarten naast elkaar.

De 16:10 komt uit de referentie, waar het beeld 637 bij 390 staat (1,63:1) en
bijna de helft van de kaarthoogte beslaat. Bij de dienstkaarten is dat hier ook
48%; bij de cursuskaarten 41%, want die staan met vier op een rij en zijn dus
smaller.

Twee dingen om te weten als je eraan werkt:

- **De pijlen staan `hidden` in de HTML** en worden door `site.js` zichtbaar
  gemaakt. Zonder JavaScript staan alle citaten onder elkaar; dan zou je op
  knoppen klikken die niets doen.
- **De foto naast een citaat is een werkplek en geen portret.** Dat is een
  bewuste keuze: van deze mensen hebben we geen foto, en een willekeurig gezicht
  naast een naam zetten maakt er een bestaand persoon van die dit nooit gezegd
  heeft. Komen er echte portretten met toestemming, dan kan de fotosleutel in de
  lijst gewoon vervangen worden.

## Kaarten met een foto erboven

De drie dienstkaarten (homepage `s04-diensten`) en de vier cursuskaarten
(homepage `s07-cursusaanbod` en `cursusaanbod.html` `s02-cursussen`) dragen een
foto boven de tekst. Twee verschillende componenten, dezelfde opbouw:

| | Dienstkaart | Cursuskaart |
|---|---|---|
| Component | `.cta-blocks-advanced__card` | `.panel` |
| Beeld | `.cta-blocks-advanced__banner--verhouding` | `.panel--beeld` + `.panel__beeld` |
| Per rij | drie | vier |
| Verhouding | 16:10 | 16:10 |
| Op 1440px | 480 bij 300 | 360 bij 225 |

Twee dingen om te weten als je eraan werkt:

- **De inzet is kleiner dan de paginainzet.** In een rij van vier is de kaart
  360px breed op 1440; met de 48px van `--inset-x` links en rechts bleef er 264px
  voor de tekst over, en "Veiligheidsbewustzijn" is op 30px al 283px breed. Dat
  liep dus over de rand. In `.panel-row--4` is de inzet daarom 32px, en de titel
  krijgt `hyphens: auto`, want net boven de 992px is de kaart maar 248px breed en
  past ook 296px niet. Met `lang="nl"` op de pagina breekt de browser op de
  juiste plek. De rijen met twee of drie kaarten houden de paginainzet.
- **Het beeld loopt tot de rand van de kaart.** Bij `.panel` zit de inzet in de
  padding van de kaart zelf, dus het beeld heeft een negatieve marge van precies
  `--inset-x` en de kaart geen padding aan de bovenkant. Die regels staan in
  `styleguide.css` bewust n&aacute; de media-queries van `.panel`: ze hebben dezelfde
  soortelijkheid en moeten de padding op smalle schermen ook kunnen overschrijven.
- **De alt is leeg.** De foto zegt niets wat de link niet al zegt; met een
  beschrijving erin hoort een schermlezer eerst een productiehal voordat hij bij
  de cursusnaam is.

De beeldsleutel staat als laatste veld in `SERVICES` en `CURSUSSEN` in
`schil.py`, en `cursuskaart()` en `dienstkaart()` daar bouwen de kaart. De
cursuskaart komt op twee pagina's voor; daarom staat hij in de schil en niet in
een van de bouwbestanden.

## De voet

Vier kolommen: logo met intro, Diensten, Cursussen, Contact. Ze staan alle vier
op `col-lg-3 col-md-4 col-12`, wat neerkomt op:

| Breedte | Wat je ziet |
|---|---|
| vanaf 992px | vier naast elkaar |
| 768&ndash;991px | drie naast elkaar, de vierde eronder |
| onder 768px | onder elkaar |

De kolommen zaten eerder op `col-lg-3 / col-lg-2 / col-lg-3 / col-lg-3` (samen
elf van de twaalf, dus een gat aan de rechterkant) en op tablet op
`col-md-6 / 4 / 4 / 4`, wat een rij van anderhalf gaf. Nu tellen ze op elke
stap precies op.

## De zijinzet

Elke sectie zet zijn tekst op `var(--inset-x)` van de schermrand: 48px, 16px
onder 992px. Dat is de enige horizontale maat op de pagina, en hij hoort overal
gelijk te zijn, ook in componenten die hun eigen padding meebrengen.

Ga je een component toevoegen met eigen padding, gebruik dan `var(--inset-x)`
voor de horizontale kant en niet `--space-panel` of een los getal. Twee plekken
gingen daar eerder de mist in: de horizontale kaart van `.cta-blocks-advanced`
zette links 48px op elk formaat (dus 32px te veel onder 992px) en had rechts een
hardgecodeerde 121px uit de referentie. Beide staan nu op tokens.

Nalopen doe je zo: meet in de browser de `left` van het eerste tekstelement van
elke sectie en kijk of er &eacute;&eacute;n waarde uit komt. De logoband en het slotblok
vallen daarbuiten: die lopen bewust door tot de rand of staan gecentreerd.

## De staart van elke pagina

Elke pagina met een FAQ eindigt in dezelfde volgorde: **eerst de FAQ, dan het
slotblok** (logoband plus CTA). Het slotblok is &eacute;&eacute;n aanroep maar twee secties,
dus het nummer erna springt met twee.

Een sectie met partnerkaarten heet `samenwerking` en niet `partners`; die naam
is van de logoband.

## Twee componenten die contact en over-ons delen

Beide pagina's beginnen met dezelfde hero en hebben allebei een rij van vier
gekleurde vlakken. Die twee staan daarom in `styleguide.css` en niet in een
paginastijl:

| Component | Wat het is |
|---|---|
| `.paginahero` | Twee helften over de volle breedte: links een grijs vlak met de `<h1>` onderin, rechts een foto. Onder 768px staat de foto als band van 220px bovenaan; de `<h1>` blijft in de HTML v&oacute;&oacute;r het beeld en verhuist met `order`. |
| `.vlakkenrij` | Vier vlakken in geel, grijs, wit en diepgroen, tekst onderin, tot de schermrand. Twee kolommen onder 992px, &eacute;&eacute;n onder 576px. De rij zit buiten `.container`; de kop erboven houdt wel de pagina-inzet aan. |

In de bouwscripts zijn dat `paginahero()` en `vlakkenrij()` in `schil.py`; de
kleuren van de vlakken lopen vast in dezelfde volgorde, zodat het ritme op elke
pagina hetzelfde is.

## De scrollstand bij een pagina-overgang

Drie dingen moeten hier samenwerken, en ze deden dat geen van drieën vanzelf.

1. **ScrollSmoother onthoudt zijn eigen stand over `kill()` en `create()` heen**,
   en `ScrollTrigger.refresh()` zet die met opzet terug om een sprong te
   voorkomen. Bij een pagina-overgang is dat precies verkeerd: je klikt
   halverwege pagina A door en komt halverwege pagina B uit, met een scrollbalk
   die bovenaan staat. Daarom zet `after` de stand er als laatste nog een keer
   in, na de refresh.
2. **De browser bewaart zelf ook een stand per stap in de geschiedenis.** Die
   zette hij terug op een pagina die er nog niet stond, waarna wij het nog eens
   deden. `history.scrollRestoration` staat daarom op `manual`; het geheugen in
   `page-transitions.js` doet het werk.
3. **De stand wordt opgemeten vóór `sloop()`, en bij de smoother zelf.** Na een
   `kill()` geeft `window.scrollY` een oude waarde terug, en dan onthoud je de
   verkeerde stand voor de verkeerde pagina. Dat was te zien bij de vooruitknop.

Nagemeten: klikken vanaf een gescrolde pagina komt op nul uit, de terugknop komt
terug op de onthouden stand, en de vooruitknop op nul als die pagina daar stond.

## Servicepagina's: `veilig-gedrag`, `ehs-rie`, `safety-checks`

De kop is `.paginahero paginahero--hoog`. Die modifier zet de kop op 640px, de
hoogte die de cursuskop vanaf 1440px aanneemt; de twee staan naast elkaar in het
menu en horen dus even hoog te zijn. Tussen 768 en 1200px is de cursuskop 50 tot
90px hoger, want daar breekt zijn introtekst over meer regels. Dat is niet te
volgen met een vaste maat: die reeks loopt eerst op en dan weer terug. Onder
768px geldt de modifier niet, want daar stapelt de hero.


Deze drie zijn één template. Alleen de teksten, de iconen en het stappenplan
verschillen. Gedeelde opmaak staat in `service.css`.

| id | Component | Opmerking |
|---|---|---|
| `s01-introductie` | `.service-hero` op plum, `data-header-theme="light"` | h1 + twee alinea's + knop |
| `s02-wanneer-geschikt` | `.content-block` + `.panel-row--3` | drie herkenningskaarten |
| `s03-hoe-werken-wij` | `.band.background--grey` + `<ol class="trap">` | de treden; vijf bij Veilig gedrag, drie bij de andere twee |
| `s04-voordelen` | `.content-block` + `.panel-row--4` | icoon + titel + omschrijving |
| `s05-partners` | `.content-block` + `.panel-row--3` | naam, subtitel, tekst, link naar de corporate site |
| `s06-projecten` | `.cases-grid` | rijen wisselen grijs en wit af |
| `s07-contact` | `.band.background--grey` + `[data-contactformulier]` | onderwerp voorgeselecteerd op de dienst |
| `s08-faq` | `.band.background--white` + `.accordion` | drie items, met `FAQPage`-structuurdata |

## Cursuspagina's: vier stuks

Eén template, gedeelde opmaak in `cursus.css`.

De volgorde volgt wat iemand die de cursus overweegt achter elkaar wil weten:
wat is het, wat kost het en hoe lang duurt het, is het voor mij, wat lever ik
ermee op, hoe ziet het eruit, wat neem ik mee, waarom hier, wat zeggen anderen,
en dan pas het formulier.

| id | Component | Rol in de flow |
|---|---|---|
| `s01-introductie` | `.service-hero` met &eacute;&eacute;n alinea, de twee knoppen en daaronder `.hero--bewijs` | wat is dit, en hoeveel mensen gingen je voor |
| `s02-statement` | `.content-text-side-cta` + knop naar het infopack | de tweede alinea van de inleiding, losgetrokken |
| `s03-in-het-kort` | `.kerncijfers` | tijdsbeslag, doorlooptijd, groep, tarief |
| `s04-voor-wie` | `.cta-blocks-advanced__card--horizontal` | beeld naast tekst |
| `s05-resultaat` | `.band.background--grey` + `.check-lijst--twee` | wat je ermee kunt |
| `s06-inhoud` | `.content-text-side-visual` | hoe de cursus eruitziet |
| `s07-programma` | `<ol class="trap">` met tijdsbeslag per stap | de opbouw |
| `s08-certificaat` | `.band.background--groen.certificaat` + knop naar het vervolg | certificaat en vervolgstap samen |
| `s09-waarom` | `.panel-row--4`, vier USP's | vertrouwen |
| `s10-ervaringen` | `.panel-row--3` | vertrouwen |
| `s11-infopack` | `[data-contactformulier]` | de conversie |
| `s12-faq` | `.accordion`, drie items | |
| `s13-partners` + `s14-contact` | het slotblok | |

Twee blokken van dezelfde soort staan nergens achter elkaar; de vorm wisselt van
tekstband naar cijferrij naar beeld-naast-tekst naar lijst naar beeld-met-uitloop
naar trap naar kaarten. De knop naar het infopack komt drie keer terug: in de
hero, bij het statement en als de sectie zelf.

De inleiding stond eerder als twee alinea's in de hero. Die staan nu uit elkaar:
de eerste in de hero, de tweede als statement. De leerresultaten stonden als
lijstje onder de opzet-tekst en hebben nu een eigen sectie met twee kolommen;
dat is waarvoor iemand de cursus boekt. Het certificaat en het &ldquo;en daarna&rdquo;-blok
zijn samengevoegd: allebei gaan ze over wat er na de laatste dag overblijft.

## Cases

Het overzicht en de detailpagina's delen `cases.css`. De gegevens van alle zes
de cases staan op één plek (`CASES` in het bouwscript), en voeden ook de
projectrijen op de homepage en op de servicepagina's. Wijzig een case daar, niet
in de losse HTML.

**`cases.html`**, overzicht met filters:

| id | Component |
|---|---|
| `s01-introductie` | `.band` met kicker, titel, intro |
| `s02-cases` | twee filtergroepen (`.filter-groep` met `.filter-pil`), een telling in `aria-live`, het kaartraster en een lege-staat |
| `s03-contact` | het gedeelde contactblok |
| `s04-faq` | `.accordion`, drie items |

De filters staan in `cases.js`: binnen een groep geldt er één tegelijk, de
eerste pil zet de groep weer open. De kaarten staan gewoon in de HTML en worden
alleen verborgen, dus zonder JavaScript zie je alle zes de cases.

**`case-[slug].html`**: twaalf blokken, &eacute;&eacute;n template. De opzet volgt
het ritme van de referentiecase: alles op wit, secties gestapeld in plaats van in
twee kolommen, en beeld over de volle breedte als adempauze tussen de tekst. De
schaalsprong doet het werk: een grote kop boven een smalle kolom kleine tekst.

| id | Component |
|---|---|
| `s01-introductie` | `.service-hero` met foto, sluier en de twee knoppen |
| `s02-kerncijfers` | `.kerncijfers`, vier getallen met label en eenheid |
| `s03-inleiding` | `.case-lead`, de situatie in leadformaat |
| `s04-over` | `.case-blok`, wie de opdrachtgever is |
| geen | `.case-bleed`, beeld over de volle breedte |
| `s05-uitdaging` | `.case-blok` met `.case-lijst` |
| `s06-citaat` | `.case-citaat` op wit |
| `s07-aanpak` | `.case-blok` met `.case-lijst` |
| geen | `.case-bleed`, beeld over de volle breedte |
| `s08-resultaat` | `.case-blok`, wat het opleverde |
| `s09-verwant` | twee andere cases als `.cases-grid__row` |
| `s11-contact` | het gedeelde contactblok, onderwerp voorgeselecteerd op de dienst |

`.case-bleed` staat b&eacute;wust buiten `.container`, want alleen zo loopt het beeld
door de zijinzet heen. De bandhoogte is begrensd op 460px omdat het opvulbeeld
maar 1024px breed is; hoger zou dat te ver oprekken.

## Het slotblok: logoband en CTA

Zeventien pagina's eindigen met dezelfde twee secties, uit &eacute;&eacute;n functie in het
bouwscript. `contact.html`, `privacybeleid.html` en `cookies.html` niet: daar is
een verwijzing naar de contactpagina zinloos.

| Component | Wat |
|---|---|
| `.logo-slider` | doorlopende logoband; de reeks staat er twee keer in en de animatie schuift precies de helft op, dus de lus is naadloos. Het tweede exemplaar is `aria-hidden`, zodat een schermlezer de namen &eacute;&eacute;n keer hoort. Pauzeert bij hover en focus, en staat stil bij `prefers-reduced-motion`. |
| `.cta-slot` | &eacute;&eacute;n groen vlak over de volle breedte met de kop, de tekst en de knop naar `contact.html`, alles gecentreerd. De kop is afgetopt op 20ch en de tekst op 46ch, zodat de regels op een breed scherm niet uitrekken. |

Het slotblok is &eacute;&eacute;n aanroep maar twee secties, dus ook twee nummers:
`slotblok("11")` levert `s11-partners` en `s12-contact`. Eerder kregen ze allebei
hetzelfde nummer.

Er stond eerder een contactkaart met Martins portret en gegevens naast het
groene vlak; die is eruit gehaald omdat dezelfde gegevens een klik verderop
staan, op de pagina waar de knop naartoe wijst.

Het contactformulier stond hier eerder in en staat nu alleen nog op
`contact.html`, plus als infopack-formulier op de vier cursuspagina's.

## Overige pagina's

- **`index.html`**: twaalf secties:
  `s01-introductie` (hero met foto) · `s02-wat-we-doen` (statement op grijs) ·
  `s03-hoe-we-werken` (tekst met uitlopend beeld) · `s04-diensten` ·
  `s05-projecten` · `s06-usps` · `s07-cursusaanbod` · `s08-testimonials` ·
  `s09-faq` · `s10-martin` · `s11-partners` · `s12-contact`.
  De brief noemt er acht; `s02` en `s03` zijn erbij gekomen omdat de hero
  alleen een belofte doet en de bezoeker daarna wil weten wát MADEGRO doet.
  `s10-martin` staat er na de FAQ bij: de medewerkersband
  (`.streamer--employee`, dezelfde als op `over-ons.html`) met een korte
  introductie van Martin. Die sectie gebruikt de modifier
  `.streamer--employee--portret`, want bij een staand portret snijdt de
  16/9-band op mobiel door het gezicht; met de modifier wordt dat 4/3.
  Het component staat sinds deze wijziging in `styleguide.css` en niet meer in
  `over-ons.css`: twee pagina&rsquo;s gebruiken het nu.
- **`cursusaanbod.html`**: intro, grid van vier, contact, FAQ.
- **`over-ons.html`**: negen secties, in de opzet van de referentiepagina:

| Sectie | Vorm |
|---|---|
| `s01-verhaal` | `.paginahero`: kop op grijs links, foto rechts |
| `s02-statement` | `.content-text-side-cta`: &eacute;&eacute;n alinea in de grote lichte snede |
| `s03-waarden` | `.vlakkenrij`: vier gekleurde vlakken met de waarden |
| `s04-werkwijze` | `.cta-blocks-advanced` in de verticale variant: foto boven, tekst eronder, twee per rij. De kleuren lopen als een schaakbord (grijs, wit, wit, grijs); groen zou botsen met de band eronder |
| `s05-martin` | `.streamer--employee--portret` |
| `s06-samenwerking` | `.panel-row--3` met de partners |
| `s07-faq` | het gedeelde FAQ-blok |
| `s08-partners` + `s09-contact` | het slotblok |
- **`contact.html`**: drie secties:

| Sectie | Vorm |
|---|---|
| `s01-contact` | `.paginahero`: twee helften over de volle breedte. Links het grijze vlak met de h1 onderin, rechts een foto. Onder 768px staat de foto als band van 220px bovenaan en de kop eronder; de `<h1>` blijft in de HTML v&oacute;&oacute;r het beeld staan en wordt met `order` verplaatst. |
| `s02-formulier` | `.band` met de aanloop links (`col-lg-4`) en het formulier rechts (`col-lg-8`, zelf afgetopt op 720px zodat de velden scanbaar blijven). |
| `s03-gegevens` | `.vlakkenrij`: vier vlakken over de volle breedte met de tekst onderin, in geel, grijs, wit en diepgroen. Twee kolommen onder 992px, &eacute;&eacute;n onder 576px. |

  De vier vlakken zijn **geen vestigingen**: MADEGRO heeft &eacute;&eacute;n locatie. Ze
  dragen de vier manieren om contact te leggen: telefoon, e-mail, adres en de
  bedrijfsgegevens. De `<dl class="contactgegevens">` die daar eerder voor was,
  is vervallen.
- **`privacybeleid.html` / `cookies.html`**: `.tekstband` met één leeskolom, `tekstpagina.css`.

---

## Componenten die je hergebruikt

Uit `styleguide.css` (op elke pagina beschikbaar):

`.button`, `.button--icon` (met `.hover--icon` op de ouder), `.panel` / `.panel-row`,
`.cases-grid__row`, `.accordion__item`, `.contactformulier`, `.field`,
`.marquee-streamer`, `.streamer--employee`, `.subtitle`, `.section-heading`,
`.band`, `.content-block--container`, `.background--white|grey|plum|volt`.

Verzin geen nieuwe varianten zonder ze hier bij te schrijven.


## Hero op de homepage

Drie lagen over elkaar in `.hero--beeld`:

1. een foto (`logistiek`, met srcset); dit is het LCP-element en staat op
   `eager` met `fetchpriority="high"`;
2. de film erover, op `opacity: 0` tot hij speelt;
3. de sluier.

`site.js` hangt de bron van de film er pas in, en alleen als
`prefers-reduced-motion` uit staat, de bezoeker geen databesparing aan heeft en
de lijn geen 2G is. Valt een van die drie weg, dan blijft het bij de foto, en
dat is het eerste beeldje van dezelfde film. Zonder JavaScript gebeurt er niets
en is de uitkomst hetzelfde.

Op schermbreedte wordt niet meer gekeken; de film speelt ook op een telefoon.
Die grens stond er eerst wel (768, later 600px), maar breedte zegt niets over de
verbinding, en daar gaat het om. Het is op elk scherm hetzelfde bestand van
1,5 MB: op een staande telefoon wordt van de 16:9-film maar het middelste kwart
gebruikt, dus een kleinere versie zou daar juist als eerste onscherp worden.

De film komt pas in beeld bij `playing` en niet bij `canplay`: weigert de
browser het automatisch afspelen, en dat mag hij, dan zie je de foto in plaats
van een stilstaand eerste beeldje.

Ga je op een telefoon naar een andere app of een ander tabblad, dan zet de
browser de film stil, en niet elke browser zet hem weer aan als je terugkomt.
Daarom doet `site.js` bij `visibilitychange` nog een keer `play()` als de film
stilstaat. Weigert de browser dat, dan blijft het stil en is er niets kapot.

De hero vult het scherm: `min-height: 100svh`, niet `height`. Zo groeit hij mee
als de tekst niet past, en dat gebeurt: op 375 bij 667 is de hero 751px hoog,
want de kop, twee alinea's en twee knoppen passen niet in 667. `svh` en niet
`vh`, anders steekt hij op een telefoon onder de browserbalken uit.

Over de film ligt alleen nog een zwarte aanloop van 30% naar 70%. De groene
gradient uit Figma is er op verzoek af; de film houdt zijn eigen kleuren. De
zwarte laag kan er niet ook af: op de beeldjes met de verlichte loods staat wit
op wit en haalt de kop 1,00:1. Zie `index.css` en CONTENT-TODO.md.


## Paginahero met het merkpatroon

`.paginahero--patroon` is dezelfde gesplitste hero als met een foto, maar met
het patroon ernaast. Staat op `contact.html`, `cases.html` en
`cursusaanbod.html`.

Twee bestanden, want de compositie verschilt en niet alleen de uitsnede:

| | bestand | zichtbaar onder de balk |
|---|---|---|
| vanaf 768px | `hero-patroon-*.webp` (1,53:1) | 1,65:1 op 1440px |
| tot 767px | `hero-patroon-mobiel-*.webp` (1:1) | 7:3, op elke breedte |

De 7:3 komt uit de referentie: daar is de band op een telefoon 2,3:1.

**Let op de balkhoogte.** De balk staat vast over de bovenkant van de pagina en
dus over de bovenkant van het patroon: op 375px lag de helft eronder, op 900px
een derde. Het vak is daarom een `--balk-hoogte` hoger dan de verhouding vraagt,
zodat er ond&eacute;r de balk staat wat er hoort te staan. Op een telefoon met
`padding-bottom` op het verhoudingsvak, daarboven met een hogere `min-height` op
`.paginahero__kop` (waar de titel onderaan uitlijnt, dus die zakt mee).

`--balk-hoogte` is gemeten en niet berekend: 77px tot 768, 109px tot 1199,
daarboven 116px. De balk krijgt zijn hoogte van zijn inhoud, en die wisselt van
hamburger naar menu-items.

`<picture>` kiest op dezelfde grens waar de layout zelf omslaat. Op een telefoon
staat de afbeelding in de stroom (`position: static`) in plaats van absoluut:
in een kolom is flex-basis de hoogte, en een vak waarvan de inhoud absoluut
staat heeft geen hoogte, dus dan wordt de band nul hoog.

De drie **dienstpagina's** gebruiken dezelfde layout maar met een foto van de
dienst, niet met het patroon. Dat is dezelfde foto als op de dienstkaart op de
homepage, zodat je na een klik ziet waar je vandaan komt: `overleg` bij Veilig
gedrag, `lassen` bij EHS RIE, `haven` bij Safety Checks. Hun introtekst is
daarbij uit de hero gehaald en staat nu als `s02-statement` eronder, zoals op
over-ons.


## De sluier over een fotohero

Drie pagina's-soorten hebben een fotohero met witte tekst eroverheen: de vier
cursuspagina's (`cursus.css`), het case-overzicht en de zes casepagina's
(`cases.css`). Het kaartje in het uitklapmenu draagt dezelfde sluier. Sinds
2 september 2026 dragen die alle vier deze twee lagen:

| laag | wat | waarom |
|---|---|---|
| 1 | `#017E84`, 20% boven naar 80% onder | de gradient uit Figma |
| 2 | zwart, 50% boven naar 75% onder | draagt de witte tekst |

Laag 2 verschilt van de homepage (daar 0% naar 60%), en dat is geen slordigheid:
op de homepage staat de tekst onderin, hier al op een derde van de hoogte, waar
de gradient nog licht is. Met alleen de gradient haalt het label daar 1,76:1.

Doorgerekend over de zes herofoto's, op de lichtste vijf procent van elk
tekstvak: cursuspagina 5,37 tot 5,98:1, casepagina 5,49 tot 5,97:1. Eis is
4,5:1, en 3:1 voor de kop.

Let op: hier stond tot 2 september het oude groen `rgba(6, 68, 44, ...)`. Dat
kwam niet mee met de kleurwissel naar het petrol uit het logo, omdat het als
rgba-waarde geschreven stond en niet als token of hex.


## Het statement met een knop ernaast

`content-text-side-cta` met een `.statement__actie` als tweede kolom: een alinea
in de grote lichte snede, de knop ernaast. Staat op de vier cursuspagina's, de
drie dienstpagina's en (zonder knop) op over-ons.

De rij staat op `gx-0`, want de tekst hoort op de paginainzet te beginnen en
niet op de inzet plus een goot. Daardoor raakten de twee kolommen elkaar: de
knop begon precies waar de tekst ophield. De ruimte zit nu op de actiekolom
zelf, 64px ernaast en 48px eronder als hij stapelt.

Let op de kiezer: `.row.gx-0 > *` zet `padding-inline` op nul en dat zijn twee
klassen, dus de inspringing staat op `.row.gx-0 > .statement__actie`. Met alleen
`.statement__actie` verliest die regel.

De regel stond eerst in `cursus.css`. Sinds de dienstpagina's dit blok ook
gebruiken staat hij in `styleguide.css`; die pagina's laden `cursus.css` niet,
dus daar stond de knop bovenin de kolom in plaats van op de onderregel.
