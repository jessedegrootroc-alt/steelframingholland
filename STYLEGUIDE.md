# STYLEGUIDE.md: MADEGRO

Het ontwerpsysteem van deze site is overgenomen uit een referentie-implementatie
die tot 4 september 2026 naast deze map stond en toen is verwijderd. De volledige
specificatie van dat systeem staat nu hier, in `STYLEGUIDE-SPECIFICATIE.md`; de
paragraafnummers (§) in de commentaren van `styleguide.css` verwijzen daarnaar.
Dit bestand beschrijft wat je moet weten om hier te werken, en waar MADEGRO
afwijkt.

## Het systeem in het kort

- **Palet: de huisstijlkleuren van MADEGRO.**

  | Token | Waarde | Waarvoor |
  |---|---|---|
  | `--color-groen` | `#017E84` | het merkgroen uit het logo: gekleurde vlakken, hero, knopvullingen, grote koppen |
  | `--color-groen-diep` | `#01575B` | haarlijnen, kleine labels, en de hover op een groen vlak |
  | `--color-groen-diepst` | `#014144` | **alle lopende tekst en kleine koppen**, de sluier over foto's, en het ingedrukte groen |
  | `--color-geel` | `#FFFC58` | de CTA-kleur: knoppen, accenten, markeringen |
  | `--color-geel-hover` | `#F2EE3E` | hover op een gele knop |
  | `--color-background` | `#FFFFFF` | het paginavlak |
  | `--color-grey` | `#F1F1F1` | de tweede achtergrond, voor afwisselende banden en panelen |

  Verzin geen nieuwe kleuren; gebruik deze tokens.

- **Twee tinten groen, en waarom.** Het merkgroen `#017E84` haalt op wit 4.86:1
  en op het grijs `#F1F1F1` nog maar 4.09:1. Voor tekst onder 24px is 4.5:1 de
  eis, dus daar staat het diepere `#014144` (10,1 tot 11,4:1). Vanaf 24px geldt
  3:1 en mag het merkgroen wél: dat zijn `.section-heading`,
  `.cases-grid__heading`, `.font-size--xl`, `.cta-blocks-advanced__title`,
  `.usp__getal` en `.streamer--employee-name`. Zet je een nieuwe kop in het
  merkgroen, controleer dan eerst of hij minstens 24px is.

- **Geel is voor actie, niet voor vlakken.** De gele knop met bijna-zwarte tekst
  haalt 19:1. Wit op geel is 1.09:1 en mag dus nooit; in een groene band is de
  regel die links wit maakt daarom uitgezonderd voor `.button`.
- **Vierkante hoeken.** `border-radius: 0` op alles, behalve ronde icoonknoppen
  (`100px`) en de markeer-chip in een kop (`12px`).
- **Geen schaduwen op layout.** Hoogteverschil maak je met een andere
  achtergrondkleur, niet met een schaduw. Alleen zwevende lagen (de cookiemelding)
  hebben er een.
- **Koppen zijn licht (300), labels zijn medium (500).** Hoe kleiner de tekst, hoe
  zwaarder. Dat is de typografische handtekening.
- **Uppercase labels krijgen `letter-spacing: 2.2px`.** Altijd. Lopende tekst is
  nooit uppercase.
- **Secties zijn volle kleurbanden**, geen zwevende kaarten. Het ritme komt uit de
  padding van de band: 96px verticaal en 48px horizontaal op desktop, 32/16px op
  mobiel. Nooit marges tussen secties.
- **Twee banden op elkaar halveren hun padding** (48 + 48 = 96px), zodat elke
  overgang dezelfde lucht heeft. De eerste en de laatste band van een pagina
  houden hun volle 96px. Dat is §4.6 van de gids: twee keer 96px zou 192px lucht
  geven, en dat leest als een gat. De regel staat in `styleguide.css` onder
  &ldquo;Ritme tussen banden&rdquo; en werkt met `:has(+ section)`, dus je hoeft er in de
  HTML niets voor te doen.
- **Kolommen die onder elkaar vallen** krijgen 48px tussenruimte via `row-gap` op
  `.row`. Bij `.row.g-0` is die nul, want daar horen de panelen elkaar te raken.
- **Eén zijinzet voor de hele pagina: `--inset-x`.** 48px, en 16px vanaf 991px
  naar beneden, hetzelfde schakelpunt als de caserijen (§6.9) en de
  kaartlichamen (§6.8), zodat op een tablet alles op dezelfde rand staat.
  De componenten uit de gids schakelen elk op hun eigen breekpunt (§6.8 op 991px,
  §6.9 op 991px, `content-block--container` pas op 576px), waardoor er op een
  tablet 16, 32, 40 en 48px naast elkaar stonden. Alles wat de linkerrand van de
  pagina raakt gebruikt nu die ene variabele: banden, panelen, caserijen,
  kaartlichamen, treden, de hero en het tekstblok met uitlopend beeld. Zet je een
  nieuw component neer, gebruik dan `var(--inset-x)` en geen eigen waarde.
- **Links uitlijnen.** Gecentreerde tekst gebruiken we niet.
- **Beweging is beperkt** tot hover, menu's en doorlopend transport. Geen
  scroll-reveals, geen parallax, geen tellers behalve de USP-cijfers op de
  homepage (die respecteren `prefers-reduced-motion`).

## Waar MADEGRO afwijkt van de referentie

| Onderwerp | Referentie | Hier | Waarom |
|---|---|---|---|
| Kleuren | plum en lime uit de referentie | het groen, geel, wit en grijs van MADEGRO | dit zijn de huisstijlkleuren van de opdrachtgever |
| Lettertype | Inter Tight via Google Fonts CDN | Inter Tight lokaal in `assets/fonts/` | de projectbrief eist lokaal gehoste fonts met `font-display: swap` |
| Pagina-overgang | 300 ms Barba + GSAP | identiek overgenomen | geen |
| Formulier | geen | `contactformulier.js` | de referentie had er geen; velden zijn afgeleid van de veldbeschrijving in de gids (52px hoog, geen radius, uppercase label) |
| Trap / treden | bestaat niet | `.trap` en `.trede` | nodig voor de Veiligheidsladder en de stappenplannen; opgebouwd uit bestaande tokens |
| Panelen van 3 en 4 kolommen | alleen een paar van twee | `.panel-row--3` en `--4` | zelfde `.row.g-0`-idioom, meer kolommen |
| Veldkleur | veld is wit | wit, maar grijs op een witte band | zonder randen (DR-3) is het vlak het veld; wit op wit zou onzichtbaar zijn |
| Pijl in de grote knop | alleen een kleurwissel op hover | daarbij dezelfde pijlwissel als de ronde icoonknop, in `.button__spoor` | de pijl volgt `currentColor`, dus hij klopt ook als een knop op hover van kleur wisselt. Een opengeklapt vlak zoals bij de ronde knop is geprobeerd en weer verworpen: te zwaar op een brede knop |
| Lopende tekst in de lichte snede | 16px met 135% interlinie | 18px met 1,45 | de lichte 300 oogt dunner dan een normale 400; op 16px las dat krap. Tekst in de normale snede zet zijn eigen maat en blijft op 16px |
| Slotblok | contactformulier onder aan elke pagina | logoband plus een CTA naar `contact.html` | het formulier hoort op &eacute;&eacute;n plek te staan; onderaan volstaat de verwijzing, met de logoband als sociale onderbouwing ervoor |
| Logoband | logo's op hoogte uitgelijnd | idem, met een max-width erbij | de dertien logo's lopen van 160 tot 478px breed op gelijke hoogte; zonder begrenzing krijgen de lange woordmerken het dubbele gewicht van de compacte. Met `max-width` plus `object-fit: contain` worden de brede iets lager en houden de compacte de volle hoogte |
| Kaarten met beeld | tekstkaarten | een foto van 16:10 boven de tekst op de dienst- en cursuskaarten | de kaarten stonden als tekstblokken naast elkaar en waren op afstand niet uit elkaar te houden. Het beeld loopt tot de rand van de kaart; bij `.panel` gaat dat met een negatieve marge van precies de inzet, want daar zit die in de padding van de kaart zelf. In een rij van vier is de inzet 32px in plaats van de 48 van de pagina: bij 360px kaartbreedte bleef er anders te weinig over en liep een woord als "Veiligheidsbewustzijn" over de rand |
| Ronde knop, derde keus | geel of diepgroen | grijs (`.button--grijs`) | de pijlen onder de citaten zijn bediening, geen actie: je bladert ermee, je gaat er niet mee naar een volgende stap. Geel trok ze naar het niveau van een hoofdknop. De vulling is `--color-grey-diep`, een stap donkerder dan de knop zelf, anders is er niets te zien als de cirkel opengaat |
| Getuigenissen | drie kaarten naast elkaar | &eacute;&eacute;n citaat per keer, groot, met een liggend beeld (16:10) op een derde van de rij, het logo van de opdrachtgever onder de naam en pijlen eronder | overgenomen uit de referentie. De pijlen zijn de bestaande ronde icoonknop; die naar links is gespiegeld zodat de hover-animatie dezelfde kant op blijft werken |
| Rangorde in de CTA's | &eacute;&eacute;n accent (geel) voor alles | geel voor diensten, cursussen en contact; diepgroen (`--secundair`) voor alles wat naar een case leidt | de cases zijn onderbouwing en niet waar iemand voor komt. Wit op `#014144` haalt 11,4:1, de hover op `#017E84` 4,9:1, allebei boven AA |
| Contactpagina | gegevens links, formulier rechts, in &eacute;&eacute;n band | hero met een halve foto, daarna het formulier, daaronder vier vlakken over de volle breedte | overgenomen uit de referentiepagina. De vier vlakken staan daar voor vestigingen; MADEGRO heeft er &eacute;&eacute;n, dus ze dragen hier telefoon, e-mail, adres en bedrijfsgegevens |
| Over ons | verhaal, band, werkwijze, partners | hero, statement, vier waardevlakken, werkwijze als beeldraster, band, partners | overgenomen uit de referentiepagina, met dezelfde `.paginahero` en `.vlakkenrij` als de contactpagina |
| Cursuspagina | acht secties, veel tekst achter elkaar | veertien secties met wisselende vorm, kerncijfers boven aan | layout overgenomen van de BESS-pagina van de referentie; kleuren, typografie, knoppen en componenten zijn ongewijzigd |
| Hoofdmenu | zeven losse links op één balk | Home, Diensten &#9662;, Cursussen &#9662;, Cases, Over ons, Contact | de uitklapper is overgenomen uit de referentie: links de sublinks met een ondertitel, rechts een kaart met een foto en een knop naar de contactpagina. De token `--z-header-dropdown` stond al in het systeem |
| Menu-items | 11px in kapitalen, met letterafstand | 14px zonder kapitalen | de items zijn woorden om te lezen, geen labels; het mobiele paneel schreef ze al zo. Zonder kapitalen is 11px te klein, en de extra letterafstand kan eraf: die is er voor kapitalen. De overige labels op de site (subtitels, knoppen, voetkoppen) blijven wel in kapitalen |
| Logo | placeholderwoordmerk in de sitekleuren | het echte logo van Martin, petrol met uitgespaarde letters | de kleuren van de site (groen/geel) en van het logo (petrol/bleekgeel) lopen uiteen; dat is een openstaande beslissing, zie CONTENT-TODO.md. op een donkere ondergrond wisselt de balk naar de witte variant `madegro-logo-wit.svg`; dat gaat met twee `<img>`'s in hetzelfde rastervak die van opacity wisselen, niet met een filter: `brightness(0) invert(1)` zou van een uitgespaard logo een massief wit blok maken |
| Scrollen | de gewone scroll van de browser | GSAP ScrollSmoother, `smooth: 1` | de gids laat weinig beweging toe (&sect;9.2), maar dit voegt geen beweging toe: het vertraagt alleen de bestaande. ScrollSmoother gebruikt de echte scrollbalk, dus muiswiel, spatiebalk, Page Down, zoeken in de pagina en het slepen van de balk blijven werken. Uit bij `prefers-reduced-motion` en uit op aanraakschermen, waar de pagina anders achter je vinger aan loopt |

Nieuwe afwijkingen markeer je in de CSS met een comment dat begint met
`INFERRED:` en de reden erbij, zodat het later te herzien is.

## Praktisch

- Tokens en componenten: `styleguide.css`. Paginaspecifieke opmaak: `index.css`,
  `service.css`, `cursus.css`, `contact.css`, `over-ons.css`, `tekstpagina.css`.
- Elke paginastijl is in de `<head>` gemarkeerd met `data-page-css="naam"`. Het
  overgangsscript wisselt die mee; zonder die markering blijft een stijl hangen op
  een pagina waar hij niet hoort.
- De sectiestructuur staat in `SECTIONS.md`.

- **Kleuren staan als token, niet als rgba.** Bij de wissel naar het petrol uit
  het logo bleven vier plekken achter waar het oude groen als `rgba(...)` in een
  verloop stond: de sluier op de cursus- en casepagina's, het kaartje in het
  uitklapmenu en `--overlay-card-backdrop`. Die zijn los nagelopen. Schrijf een
  kleur dus als token, en als dat niet kan (in een verloop met dekking) zet er
  dan bij welk token het is.

- **Een gekleurd vlak draagt het merkgroen, tekst draagt de donkerste toon.**
  `.vlak--groen` staat op `#017E84`, want dat vlak staat in een rij naast geel,
  grijs en wit en is dus een merkvlak. `--color-groen-diepst` (`#014144`) blijft
  voor lopende tekst, koppen en de knop naar een case. Wit op `#017E84` haalt
  4,86:1: genoeg voor 16px, maar er zit geen rek in. Wordt de tekst in zo'n vlak
  kleiner, dan moet het vlak donkerder.
- **Foto met witte tekst erover: altijd twee lagen.** De gradient uit Figma
  (`#017E84`, 20% naar 80%) plus zwart van 50% naar 75%. Staat zo op de
  cursuspagina's, de casepagina's en het kaartje in het uitklapmenu. Alleen de
  homepagehero wijkt af (zwart van 0% naar 60%), omdat de tekst daar onderin
  staat in plaats van op een derde van de hoogte.

- **Het contactvlak wijkt bewust af van de contrasteis.** Het merkpatroon staat
  daar op volle sterkte, zonder waas ertussen, op verzoek. De tekst staat
  gecentreerd en de gele stralen lopen er precies doorheen: het label haalt
  1,76:1 waar 4,5 nodig is, de kop 2,03:1 waar 3 nodig is en de introtekst
  3,15:1 waar 4,5 nodig is. De regel om de waas terug te zetten staat in
  `styleguide.css` bij `.cta-slot__hoofd`. Wie dit zonder waas wil oplossen,
  moet de tekst uit het midden halen naar de donkere hoek linksonder.
