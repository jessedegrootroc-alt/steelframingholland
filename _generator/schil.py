# -*- coding: utf-8 -*-
import hashlib
import pathlib
import re
import inhoud_sfh as D
"""
Gedeelde paginaschil voor de site van Steel Framing Holland.

Dit script schrijft platte HTML-bestanden weg. De site zelf heeft geen
build-stap: wat hier uitkomt is gewone HTML die je met een statische server
serveert. Dit bestand hoort dan ook niet bij de site, het is gereedschap om de
drieënzeventig pagina's identiek te houden terwijl ze gebouwd worden.

De componenten hieronder zijn die van het oorspronkelijke template en zijn niet
van vorm veranderd.

Twee dingen zijn er inhoudelijk uit gehaald:

  - De citatenslider. Het template had daar drie verzonnen referenties in staan.
    Steel Framing Holland heeft geen referenties op zijn site, dus is de sectie
    weg; op de homepage staat op die plek nu de werkwijze in vijf stappen, en
    die staat wél in de bron.
  - De band met klantlogo's. Daar stonden dertien logo's van opdrachtgevers van
    de vorige eigenaar van dit template in. Nu staan er de zes partners die
    Steel Framing Holland zelf op zijn homepage laat zien.
"""

# Het domein waar de site komt te staan. Canonical, sitemap, robots en de
# deelafbeelding verwijzen hierheen.
BASIS = "https://www.steelframingholland.nl"

# Het hoofdmenu. Een item is óf een gewone link, óf een uitklapper met sublinks
# en een kaart ernaast. De drie diensten en de vier cursussen stonden hier
# eerder allemaal los naast elkaar; dat waren zeven items op één balk.
#
# De sublinks komen uit SERVICES en CURSUSSEN verderop in dit bestand, zodat een
# wijziging daar meteen in het menu, de voet en de overzichtspagina's landt.
# Daarom wordt NAV pas onderaan opgebouwd, in bouw_nav().
NAV = []

# De toepassingen en techniekpagina's, in de vorm die de componenten hieronder
# verwachten: (bestand, titel, ondertitel, beeldsleutel). De bronsite heeft geen
# meta descriptions, dus de ondertitel komt uit de herschreven lead in
# inhoud_copy.py, ingekort tot één regel voor de kaart.
def _kort(t, n=95):
    t = (t or '').strip()
    if t.startswith('['):
        return ''
    return t if len(t) <= n else t[:t.rfind(' ', 0, n)] + '&hellip;'


import inhoud_copy as _C


def _ondertitel(bestand, n=95):
    """De regel onder een paginanaam in het menu en op een kaart.

       Komt uit MENU_ONDERTITEL in de copylaag: één korte regel per pagina. Is
       die er niet, dan valt hij terug op de eerste zin van de lead."""
    eigen = _C.menu_ondertitel(bestand)
    if eigen:
        return _kort(eigen, n)
    lead = (_C.dienst(bestand).get('lead') or [''])[0]
    zin = re.split(r'(?<=[.!?])\s', lead.strip())[0] if lead else ''
    return _kort(zin, n)


SERVICES = [(b, t, _ondertitel(b), beeld)
            for b, sl, t, beeld in D.HOOFDDIENSTEN]

# De onderliggende werkzaamheden per hoofddienst.
WERKZAAMHEDEN = {t: [(b, tt, _ondertitel(b), beeld)
                     for b, sl, tt, ouder, beeld in D.kinderen(t)]
                 for _, _, t, _ in D.HOOFDDIENSTEN}

# De losse diensten die niet onder een hoofddienst hangen.
# De vier techniekpagina's. Ze hangen niet onder één toepassing, want ze horen
# bij alle drie; in het menu staan ze onder "Staalframebouw".
LOSSE_DIENSTEN = [(b, tt, _ondertitel(b), beeld)
                  for b, sl, tt, ouder, beeld in D.LOSSE_DIENSTEN]

PROJECTEN = D.PROJECTEN
CATEGORIEEN = D.CATEGORIEEN


def bouw_nav():
    """Het hoofdmenu, met dezelfde indeling als op de bronsite.

       Daar staan Toepassingen en Staalframebouw als uitklapper in de balk, met
       Projecten, Over ons en Contact ernaast. Die indeling is overgenomen,
       omdat het precies de twee vragen zijn waarmee een bezoeker binnenkomt:
       waarvoor bouw je, en waarmee. De vorm van het menu blijft die van dit
       template.

       Nieuws staat er niet in. De bronsite heeft zes nieuwsberichten, maar dit
       template heeft geen nieuwssectie en drie van die zes gaan over een
       project dat al in het portfolio staat. Wat er feitelijk in stond is
       ondergebracht waar het thuishoort: de verhuizing bij de
       contactgegevens, het Mebest-artikel bij het project in Hoorn."""
    NAV.extend([
        {"soort": "link", "href": "index.html", "label": "Home"},
        {
            "soort": "uitklap", "id": "toepassingen", "label": "Toepassingen",
            "links": [(b, t, o) for b, t, o, _ in SERVICES],
            "kaart": {
                "kop": "Weten wat er in staalframe kan?",
                "tekst": "Vertel kort wat u wilt bouwen; we rekenen door wat er constructief mogelijk is en wat het kost.",
                "knop": "Bespreek uw project",
                "href": "offerte.html",
                "foto": "sfh-woningbouw",
            },
        },
        {
            "soort": "uitklap", "id": "staalframebouw", "label": "Staalframebouw",
            "links": [(b, t, o) for b, t, o, _ in LOSSE_DIENSTEN],
            "kaart": {
                "kop": "Zes stappen, één partij",
                "tekst": "Ontwerpen, tekenen, berekenen, fabriceren, transporteren en monteren doen wij met eigen mensen.",
                "knop": "Zo werken we",
                "href": "werkwijze.html",
                "foto": "sfh-engineering",
            },
        },
        {
            "soort": "uitklap", "id": "projecten", "label": "Projecten",
            "links": ([("projecten.html", "Alle projecten",
                        f"{len(PROJECTEN)} projecten in Nederland en daarbuiten")]
                      + [(f"projecten.html#{c.lower()}", c,
                          f"{len(D.projecten_in(c))} projecten") for c in CATEGORIEEN]),
            "kaart": {
                "kop": "Van villa tot optopping",
                "tekst": "Woningen, renovaties en utiliteitsbouw in Nederland, en projecten op Bonaire, in Ha\u00efti, Irak en op Ibiza.",
                "knop": "Bekijk de projecten",
                "href": "projecten.html",
                "foto": "sfh-project-villa-in-bergen",
            },
        },
        {
            "soort": "uitklap", "id": "over-ons", "label": "Over ons",
            "links": [
                ("over-ons.html", "Steel Framing Holland",
                 "Wie wij zijn en wat wij zelf doen"),
                ("werkwijze.html", "Werkwijze",
                 "Van ori\u00ebntatie tot oplevering in vijf stappen"),
                ("partners.html", "Onze partners",
                 "Met wie wij vast samenwerken, en waarvoor"),
            ],
            "kaart": {
                "kop": "Engineering, productie en montage in \u00e9\u00e9n hand",
                "tekst": "Eigen engineers, een eigen productiefaciliteit en een vast team monteurs.",
                "knop": "Over Steel Framing Holland",
                "href": "over-ons.html",
                "foto": "sfh-staalframe",
            },
        },
        # Contact staat hier NIET in. De balk heeft er zelf al een, als
        # highlight-knop rechts, en de mobiele lade als chip in de topbalk.
        # Stond hij hier ook, dan las de navigatie "... Over ons | Contact |
        # Contact": één keer gewoon en één keer uitgelicht.
    ])


# Alle gegevens hieronder komen letterlijk van www.steelframingholland.nl
# (homepage-footer en contactpagina). Er staat niets in dat de bronsite niet
# noemt. Wat de bronsite niet noemt: KvK-nummer, BTW-nummer en openingstijden.
TELEFOON_WEERGAVE = D.TELEFOON_WEERGAVE
TELEFOON_LINK = D.TELEFOON_LINK
EMAIL = D.EMAIL
ADRES = D.ADRES
KVK = D.KVK
MOBIEL_WEERGAVE = D.MOBIEL_WEERGAVE
MOBIEL_LINK = D.MOBIEL_LINK
CONTACTPERSOON = D.CONTACTPERSOON
WERKPLAATS_INGANG = D.WERKPLAATS_INGANG
# De bronsite noemt geen reactietermijn en geen openingstijden, alleen "tijdens
# kantooruren". Die formulering is overgenomen in plaats van een aantal dagen te
# verzinnen.
REACTIETIJD = "zo spoedig mogelijk"




# (naam, groot, groothoogte, klein, kleinhoogte, alt, map, midden)
#
# Middenmaat staat op None voor alle foto's, en dat is een bewuste keuze. Er
# hebben tussenmaten van 800px in gezeten, want op een telefoon van 412 CSS-
# pixels met dpr 1,75 is 721px nodig en dan slaat de browser 640 over en neemt
# 1200. Op papier drie keer zoveel pixels als er te zien is.
#
# In beeld pakte dat verkeerd uit. Een kandidaat die net boven de gevraagde
# breedte ligt wordt door de browser met een goedkoper filter verkleind dan een
# kandidaat die er ruim boven ligt: 800 naar 720 werd zichtbaar zachter dan 1200
# naar 720. Vergeleken op schermafdrukken van voor en na, en nagerekend: de
# scherpte van het gebied zakte met ruim zestig procent. Dat is precies wat we
# niet wilden inleveren, dus de tussenmaten zijn eruit.
#
# Bij de patronen staat wel een tussenmaat, want daar zit geen fijn detail in
# dat zachter kan worden; het zijn vloeiende verlopen.
# De beelden van deze site komen allemaal uit de export van de bronsite en
# staan daarom in beeldplan.json, niet hier. Dit blok bleef leeg over toen de
# foto's van de vorige eigenaar van dit template eruit gingen: dat waren
# stockbeelden van een bouwplaats, een productiehal en cursussen, en die zeggen
# niets over Steel Framing Holland.
FOTOS = {}


# De beelden uit de export van de bronsite. maak_assets.py heeft ze naar WebP omgezet en
# heeft in beeldmaten.json vastgelegd welke breedtes er van elk bestand bestaan
# en hoe groot de grootste is. Dat bestand wordt hier ingelezen, zodat een nieuwe
# foto alleen in beeldplan.json hoeft te staan en niet ook nog hier.
import json as _json
_maten_bestand = pathlib.Path(__file__).resolve().parent / 'beeldmaten.json'
_beeld_maten = (_json.loads(_maten_bestand.read_text(encoding='utf-8'))
                if _maten_bestand.exists() else {})
for _naam, _r in _beeld_maten.items():
    FOTOS[_naam] = (_naam, _r['breed'], _r['hoog'], min(_r['breedtes']), None,
                    _r['alt'], 'foto', None)


# Hoe breed een kaart werkelijk is, voor het sizes-attribuut. Zonder dit haalt
# de browser het grootste bestand op voor een kaart van een kwart pagina breed.
BEELD_MATEN_4 = "(max-width: 767px) 100vw, (max-width: 991px) 50vw, 25vw"
BEELD_MATEN_3 = "(max-width: 991px) 100vw, 33vw"


def foto(sleutel, klasse='', laden='lazy', maten='100vw', alt=None):
    """Eén beeld, in AVIF met WebP als terugval, in meerdere breedtes.

       <picture> met een AVIF-bron en een WebP-<img>. AVIF is bij gelijke
       kwaliteit ruwweg een derde tot de helft kleiner dan WebP; elke browser van
       de laatste jaren kan het lezen, en wie het niet kan krijgt de WebP. De
       browser kiest de breedte zelf, op grond van sizes en de pixeldichtheid.

       De breedtes komen uit MATEN[sleutel] als die er is, anders uit de tuple
       (kleine, middel, grote maat). Bestanden heten <naam>-<breedte>.<ext>.
       width en height zijn die van de grootste maat; ze leggen de verhouding
       vast, zodat er niets verspringt terwijl het beeld nog laadt.

       De alt-tekst beschrijft wat er te zien is; bij puur decoratief beeld geef
       je alt='' mee."""
    naam, gb, gh, kb, kh, standaard_alt, map_, mb = FOTOS[sleutel]
    tekst = standaard_alt if alt is None else alt
    # Een beeld dat lazy geladen wordt, is per definitie niet nodig om de
    # pagina te tekenen, dus krijgt het lage prioriteit. Dat verandert niets aan
    # óf het wordt opgehaald, alleen aan de plek in de rij: de browser gaf de
    # foto's onder de vouw evenveel bandbreedte als de stylesheet en het
    # lettertype, en op een mobiele lijn wachtte de hero-tekst daardoor op
    # ruim twee megabyte aan beeld dat niemand nog zag.
    prioriteit = (' fetchpriority="high" decoding="async"' if laden == 'eager'
                  else ' fetchpriority="low" decoding="async"')
    breedtes = sorted(MATEN.get(sleutel) or ({kb, gb} | ({mb} if mb else set())))
    bron = lambda ext: ', '.join(f'assets/{map_}/{naam}-{b}.{ext} {b}w' for b in breedtes)
    klasse_attr = f' class="{klasse}"' if klasse else ''

    # Vangnet. Een <source> naar een bestand dat er niet is, is erger dan geen
    # <source>: de browser kiest de AVIF-bron op type, en valt bij een 404 NIET
    # terug op de WebP. Je krijgt dan een kapot beeld. Dat is precies wat er
    # gebeurde toen zes foto's wel een WebP hadden en nog geen AVIF. Dus: alleen
    # een AVIF-bron als elk bestand in die srcset ook echt op schijf staat, en
    # anders hard stoppen als ook de WebP ontbreekt, want dan is de build fout.
    wortel = pathlib.Path(__file__).resolve().parent.parent
    ontbreekt = [b for b in breedtes if not (wortel / f'assets/{map_}/{naam}-{b}.webp').exists()]
    if ontbreekt:
        raise FileNotFoundError(f'foto {sleutel!r}: WebP ontbreekt voor breedte(s) {ontbreekt}')
    avif_compleet = all((wortel / f'assets/{map_}/{naam}-{b}.avif').exists() for b in breedtes)
    avif_bron = f'<source type="image/avif" srcset="{bron("avif")}" sizes="{maten}">' if avif_compleet else ''

    return (f'<picture>{avif_bron}'
            f'<img src="assets/{map_}/{naam}-{gb}.webp" srcset="{bron("webp")}" sizes="{maten}" '
            f'width="{gb}" height="{gh}" alt="{tekst}" loading="{laden}"{prioriteit}{klasse_attr}>'
            f'</picture>')


# Per fotosleutel de breedtes die er als bestand van bestaan. Staat een sleutel
# hier niet in, dan gelden de maten uit de FOTOS-tuple. De ladder is afgestemd
# op waar het beeld staat: een band over de volle breedte gaat tot 2400, een
# kaart van een derde pagina hoeft niet verder dan 960.
# De breedteladders komen uit beeldmaten.json, dat maak_assets.py schrijft.
MATEN = {}


for _naam, _r in _beeld_maten.items():
    MATEN[_naam] = _r['breedtes']


PIJL = ('<svg class="arrow--animation is-{n}" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M13.2 4.6 20.6 12l-7.4 7.4-1.4-1.4 5-5H3.4v-2h13.4l-5-5 1.4-1.4Z"/></svg>')


SPOOR = ('<span class="button__spoor" aria-hidden="true">'
         + PIJL.format(n=1).replace('width="16" height="16"', 'width="14" height="14"')
         + PIJL.format(n=2).replace('width="16" height="16"', 'width="14" height="14"')
         + '</span>')


def _inhoud(label):
    return f'<span class="button__inhoud">{label}{SPOOR}</span>'


def knop(label, href, soort='primary', extra=''):
    """De grote CTA-knop met dezelfde pijlwissel als de ronde icoonknop."""
    attr = f' {extra}' if extra else ''
    return f'<a href="{href}" class="button button--{soort}"{attr}>{_inhoud(label)}</a>'


def icoonknop(maat="", soort=""):
    """De ronde icoonknop uit §6.6.2. Decoratief: de hele kaart is de link.

       soort="button--secundair" geeft de diepgroene variant; die is voor de
       cases, die naast diensten en cursussen de tweede keus zijn."""
    klasse = f"button--icon {maat} {soort}".strip()
    return (f'<span class="{klasse}" aria-hidden="true" inert>'
            f'<span class="button--circle"><span class="circle-container">'
            f'{PIJL.format(n=1)}{PIJL.format(n=2)}'
            f'</span></span></span>')


CHEVRON = ('<svg class="submenu--chevron" width="12" height="12" viewBox="0 0 24 24" aria-hidden="true">'
           '<path d="M12 15.4 5.6 9 7 7.6l5 5 5-5L18.4 9 12 15.4Z"/></svg>')


def header(actief):
    """De balk met het logo, het hoofdmenu en de hamburger, plus de uitklappers
       en het mobiele paneel.

       De uitklappers staan buiten .header--container: ze lopen over de volle
       breedte onder de balk door, en dat kan niet binnen een flexrij. De balk
       is position:fixed en dus het ankerpunt voor hun position:absolute."""

    def is_actief(item):
        if item["soort"] == "link":
            return item["href"] == actief
        return any(b == actief for b, _, _ in item["links"])

    def bureau_item(item):
        aan = is_actief(item)
        klasse = "submenu--link is-actief" if aan else "submenu--link"
        if item["soort"] == "link":
            huidig = ' aria-current="page"' if aan else ""
            return f'      <a class="{klasse}" href="{item["href"]}"{huidig}>{item["label"]}</a>'
        return (f'      <button type="button" class="{klasse} submenu--trigger" '
                f'data-uitklap="{item["id"]}" aria-expanded="false" '
                f'aria-controls="uitklap-{item["id"]}">{item["label"]}{CHEVRON}</button>')

    def paneel(item):
        if item["soort"] != "uitklap":
            return ""
        k = item["kaart"]
        links = "\n".join(
            f'          <li><a class="uitklap__link" href="{b}">'
            f'<span class="uitklap__naam">{titel}</span>'
            f'<span class="uitklap__uitleg">{onder}</span></a></li>'
            for b, titel, onder in item["links"])
        return f'''  <div class="uitklap" id="uitklap-{item["id"]}" data-uitklap-paneel="{item["id"]}" inert>
    <div class="uitklap__inner">
      <div class="uitklap__kolom">
        <span class="subtitle">{item["label"]}</span>
        <ul class="uitklap__lijst" role="list">
{links}
        </ul>
      </div>
      <div class="uitklap__kaart">
        {foto(k["foto"], maten="(max-width: 1199px) 0px, 40vw", alt="")}
        <span class="uitklap__sluier" aria-hidden="true"></span>
        <div class="uitklap__kaart-tekst">
          <p class="uitklap__kaart-kop">{k["kop"]}</p>
          <p class="uitklap__kaart-body">{k["tekst"]}</p>
          {knop(k["knop"], k["href"])}
        </div>
      </div>
    </div>
  </div>'''

    def mobiel_item(item, i):
        vertraging = f'style="transition-delay:{i * 60}ms"'
        # Het label staat er twee keer: de tweede schuift bij hover in beeld.
        # Zonder aria-hidden leest een schermlezer "HomeHome", want beide
        # kopieën tellen mee voor de toegankelijke naam van de link.
        rol = (f'<span class="mobile-panel--text-slide"><span class="mobile-panel--text-slide-inner">'
               f'<span>{item["label"]}</span>'
               f'<span aria-hidden="true">{item["label"]}</span></span></span>')
        if item["soort"] == "link":
            return (f'      <li><a class="mobile-panel--nav-link" href="{item["href"]}" '
                    f'data-panel-sluit {vertraging}>{rol}</a></li>')
        sub = "\n".join(
            f'          <li><a class="mobile-panel--sublink" href="{b}" data-panel-sluit>{titel}</a></li>'
            for b, titel, _ in item["links"])
        return f'''      <li>
        <button type="button" class="mobile-panel--nav-link mobile-panel--nav-knop"
                data-mobiel-uitklap="{item["id"]}" aria-expanded="false"
                aria-controls="mobiel-{item["id"]}" {vertraging}>{rol}{CHEVRON}</button>
        <ul class="mobile-panel--sublijst" id="mobiel-{item["id"]}" role="list" hidden>
{sub}
        </ul>
      </li>'''

    links = "\n".join(bureau_item(n) for n in NAV)
    panelen = "\n".join(filter(None, (paneel(n) for n in NAV)))
    paneel_links = "\n".join(mobiel_item(n, i) for i, n in enumerate(NAV))
    # Contact zit niet in NAV, dus de actieve staat van die knop wordt hier
    # gezet in plaats van door bureau_item().
    op_contact = actief == 'contact.html'
    contact_actief = ' is-actief' if op_contact else ''
    contact_huidig = ' aria-current="page"' if op_contact else ''

    return f'''<header class="header header--scrolled" id="siteHeader">
  <div class="header--container">
    <a href="index.html" class="header--logo" aria-label="Steel Framing Holland, naar de homepage">
      <img class="header--logo-kleur" src="assets/logo/sfh-logo.webp" alt="Steel Framing Holland" width="124" height="40">
      <img class="header--logo-wit" src="assets/logo/sfh-logo-wit.webp" alt="" aria-hidden="true" width="124" height="40">
    </a>

    <nav class="submenu" aria-label="Hoofdmenu">
{links}
      <a class="submenu--link highlight{contact_actief}" href="contact.html"{contact_huidig}>Contact</a>
    </nav>

    <button type="button" id="hamburger" class="hamburger" aria-expanded="false" aria-controls="mobilePanel">
      Menu
      <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 5h20v2H2V5Zm0 6h20v2H2v-2Zm0 6h20v2H2v-2Z"/></svg>
    </button>
  </div>

{panelen}
</header>

<div class="mobile-panel--overlay" id="panelOverlay" hidden></div>
<div class="mobile-panel" id="mobilePanel" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="mobile-panel--topbar">
    <a class="mobile-panel--chip" href="contact.html">Contact</a>
    <button type="button" class="mobile-panel--chip is-close" id="panelSluit">
      Sluiten
      <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 6.4 17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19l5.6-5.6 5.6 5.6 1.4-1.4-5.6-5.6L19 6.4Z"/></svg>
    </button>
  </div>
  <nav class="mobile-panel--nav" aria-label="Hoofdmenu">
    <span class="mobile-panel--label">Menu</span>
    <ul class="mobile-panel--list" role="list">
{paneel_links}
    </ul>
  </nav>
  <div class="mobile-panel--cta button__mobile-width">
    {knop("Bespreek uw project", "contact.html")}
  </div>
</div>'''


def footer():
    # De footer van de bronsite heeft een adresblok, een projectenlijstje en de
    # partnerlogo's. Dit template heeft vier kolommen; die worden gevuld met de
    # toepassingen, de techniek en de projectcategorieën, zodat de belangrijkste
    # pagina's van onderaf bereikbaar zijn.
    werkzaamheden = "\n".join(f'            <li><a href="{b}">{t}</a></li>'
                              for b, t, _, _ in SERVICES + LOSSE_DIENSTEN)
    projecten = "\n".join(
        f'            <li><a href="projecten.html#{c.lower()}">{c}</a></li>'
        for c in CATEGORIEEN)
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer--widgets">
      <div class="row footer--gap">
        <div class="col-lg-3 col-md-4 col-12 widget">
          <img src="assets/logo/sfh-logo.webp" alt="Steel Framing Holland" width="124" height="40" style="margin-bottom:var(--space-500)">
          <p class="footer--intro">Staalframebouw voor woningbouw, renovatie en utiliteitsbouw. Ontworpen, gerekend, geproduceerd en gemonteerd met eigen mensen, vanuit Purmerend.</p>
        </div>
        <div class="col-lg-3 col-md-4 col-12 widget">
          <h2 class="footer__kop">Staalframebouw</h2>
          <ul role="list">
{werkzaamheden}
          </ul>
        </div>
        <div class="col-lg-3 col-md-4 col-12 widget">
          <h2 class="footer__kop">Projecten</h2>
          <ul role="list">
{projecten}
            <li><a href="over-ons.html">Over ons</a></li>
            <li><a href="werkwijze.html">Werkwijze</a></li>
            <li><a href="partners.html">Partners</a></li>
          </ul>
        </div>
        <div class="col-lg-3 col-md-4 col-12 widget">
          <h2 class="footer__kop">Contact</h2>
          <ul role="list">
            <li><a href="tel:{TELEFOON_LINK}">{TELEFOON_WEERGAVE}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          </ul>
          <p class="footer--adres">{D.STRAAT}<br>{D.POSTCODE_PLAATS}<br>Werkplaats: {WERKPLAATS_INGANG}</p>
        </div>
      </div>
    </div>
    <div class="footer--line"></div>
    <div class="footer--copyright">
      <span>&copy; {D.NAAM_VOLUIT}</span>
      <a href="privacybeleid.html">Privacybeleid</a>
      <a href="cookies.html">Cookies</a>
    </div>
  </div>
</footer>'''


COOKIEBALK = '''<!-- ================= COOKIEMELDING ================= -->
<aside id="cookiebalk" class="cookiebalk" hidden aria-label="Cookiemelding">
  <h2>Cookie-instellingen</h2>
  <p>Deze site plaatst alleen wat nodig is om hem te laten werken. Zet je analytische cookies aan, dan help je ons te zien wat werkt en wat niet. Lees het <a href="cookies.html">cookiebeleid</a>.</p>

  <div id="cookieKeuzes" class="cookie-keuzes" hidden>
    <div class="cookie-optie">
      <label class="cookie-schakelaar">
        <input type="checkbox" checked disabled aria-label="Functionele cookies, altijd aan">
        <span aria-hidden="true"></span>
      </label>
      <div>
        <span class="cookie-optie-naam">Functioneel</span>
        <p>Nodig om de site te laten werken. Staat altijd aan.</p>
      </div>
    </div>
    <div class="cookie-optie">
      <label class="cookie-schakelaar">
        <input type="checkbox" id="cookieAnalytisch" aria-label="Analytische cookies">
        <span aria-hidden="true"></span>
      </label>
      <div>
        <span class="cookie-optie-naam">Analytisch</span>
        <p>Laat ons zien welke pagina&rsquo;s bezocht worden, zodat we de site kunnen verbeteren.</p>
      </div>
    </div>
    <div class="cookie-optie">
      <label class="cookie-schakelaar">
        <input type="checkbox" id="cookieMarketing" aria-label="Marketingcookies">
        <span aria-hidden="true"></span>
      </label>
      <div>
        <span class="cookie-optie-naam">Marketing</span>
        <p>Voor advertenties en het meten daarvan. Nu niet in gebruik.</p>
      </div>
    </div>
  </div>

  <div class="cookie-knoppen">
    <button type="button" class="cookie-knop" data-cookie="weigeren">Weigeren</button>
    <button type="button" class="cookie-knop" data-cookie="aanpassen">Aanpassen</button>
    <button type="button" class="cookie-knop cookie-knop--donker" data-cookie="toestaan">Toestaan</button>
  </div>
</aside>'''


ORGANISATIE_LD = f'''{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{D.NAAM_VOLUIT}",
  "url": "{BASIS}/",
  "logo": "{BASIS}/assets/logo/sfh-logo.png",
  "email": "{EMAIL}",
  "telephone": "{TELEFOON_LINK}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{D.STRAAT}",
    "postalCode": "{D.POSTCODE_PLAATS.split()[0]} {D.POSTCODE_PLAATS.split()[1]}",
    "addressLocality": "{D.POSTCODE_PLAATS.split(maxsplit=2)[2]}",
    "addressCountry": "NL"
  }},
  "areaServed": "NL",
  "knowsAbout": "Staalframebouw"
}}'''


# ---------------------------------------------------------------------------
#  Versiehash op lokale stylesheets en scripts
# ---------------------------------------------------------------------------
# De site heeft geen build-stap, dus de bestandsnamen liggen vast: styleguide.css
# heet altijd styleguide.css. Een browser die de site eerder bezocht mag dat
# bestand daarom uit zijn cache halen, en blijft dan op de oude versie hangen na
# een update. Dat is geen theoretisch geval: tijdens het bouwen hield de browser
# hier drie keer een oude stylesheet of een oude site.js vast terwijl het bestand
# op schijf al nieuw was.
#
# Elke lokale verwijzing krijgt daarom ?v=<acht tekens uit de sha256 van de
# inhoud> mee. Verandert het bestand, dan verandert de query en haalt de browser
# hem opnieuw op; verandert het niet, dan blijft de cache gewoon werken.
#
# Alleen lokale bestanden. GSAP en Barba komen van jsDelivr en hebben hun
# versienummer al in het pad staan.
_VERSIES = {}


def v(bestand):
    """Verwijzing naar een lokaal bestand: `<naam>?v=<hash van de inhoud>`.

       Staat er een geminificeerde versie naast (`styleguide.min.css`), dan
       verwijst dit naar die, en is de hash die van het geminificeerde bestand:
       dat is immers wat de browser ophaalt. Die bestanden maakt `minify.py`;
       ontbreken ze, dan gaat het gewone bestand mee en werkt de site
       ongewijzigd, alleen wat zwaarder.

       Bestaat het bestand helemaal niet, dan komt de naam onveranderd terug:
       een ontbrekend bestand is een fout die zichtbaar moet blijven in de
       netwerktab, niet iets om hier te maskeren."""
    if bestand not in _VERSIES:
        pad = pathlib.Path(__file__).resolve().parent.parent / bestand
        klein = pad.with_name(f'{pad.stem}.min{pad.suffix}')
        if klein.exists():
            pad, naam = klein, klein.name
        else:
            naam = bestand
        try:
            hash8 = hashlib.sha256(pad.read_bytes()).hexdigest()[:8]
            _VERSIES[bestand] = f'{naam}?v={hash8}'
        except OSError:
            _VERSIES[bestand] = bestand
    return _VERSIES[bestand]


def inline(bestand):
    """De inhoud van een klein stylesheet, om in de pagina te zetten.

       Twee stylesheets zijn zo klein dat het ophalen ervan meer kost dan de
       inhoud: `transitions.css` is 0,5 kB geminificeerd en de pagina-stylesheets
       zijn 0,3 tot 6 kB. Op een mobiele verbinding blokkeerde elk van die twee
       het tekenen 304 ms, en dat is bijna helemaal het heen-en-weer van het
       verzoek. In de pagina gezet is die wachttijd nul.

       styleguide.css blijft wél een los bestand: 59 kB in elke pagina zetten
       maakt de HTML zwaarder dan wat het aan wachttijd scheelt, en dan is het
       bovendien op elke pagina opnieuw ophalen in plaats van één keer uit de
       cache.

       De pagina-overgang kan hiermee om: page-transitions.js kopieert het
       element met data-page-css uit het opgehaalde document en behandelt een
       <style> apart van een <link> ("een <style> geldt meteen")."""
    wortel = pathlib.Path(__file__).resolve().parent.parent
    pad = wortel / bestand
    klein = pad.with_name(f'{pad.stem}.min{pad.suffix}')
    bron = klein if klein.exists() else pad
    try:
        return bron.read_text(encoding='utf-8').strip()
    except OSError:
        return ''


def pagina(bestand, titel, omschrijving, namespace, pagina_css, css_naam,
           inhoud, scripts=(), extra_ld=None, actief=None, body_klasse=""):
    """Zet één complete HTML-pagina in elkaar."""
    ld_blokken = f'<script type="application/ld+json">\n{ORGANISATIE_LD}\n</script>'
    if extra_ld:
        ld_blokken += f'\n<script type="application/ld+json">\n{extra_ld}\n</script>'

    script_regels = "\n".join(f'<script src="{v(s)}"></script>' for s in scripts)
    body_attr = f' class="{body_klasse}"' if body_klasse else ""

    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{titel}</title>
<meta name="description" content="{omschrijving}" />
<link rel="canonical" href="{BASIS}/{bestand}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="author" content="{D.NAAM_VOLUIT}" />
<meta name="theme-color" content="#FFFFFF" />
<meta name="color-scheme" content="light" />

<!-- GSAP en Barba komen van jsDelivr. Het opzetten van die verbinding (dns,
     tcp, tls) kost op een telefoon een paar honderd ms en begint nu al terwijl
     de HTML nog binnenkomt, in plaats van pas onderaan de pagina. -->
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />

<!-- Het lettertype staat in de kop van de pagina en is dus onderdeel van de
     LCP. Zonder preload vindt de browser het pas nadat styleguide.css binnen is
     en ontleed is. crossorigin moet erbij, ook al staat het bestand op dezelfde
     server: een font wordt altijd in CORS-modus opgehaald, en zonder dat woord
     haalt de browser het twee keer op. -->
<link rel="preload" href="assets/fonts/assistant-latin.woff2" as="font" type="font/woff2" crossorigin />
<link rel="preload" href="assets/fonts/karla-latin.woff2" as="font" type="font/woff2" crossorigin />

<link rel="stylesheet" href="{v("styleguide.css")}" />
<style>{inline("transitions.css")}</style>
<!-- De cookiebalk verschijnt pas als cookiebalk.js hem opbouwt, dus zijn stijl
     hoeft de eerste weergave niet op te houden. media="print" laat de browser
     hem buiten het kritieke pad ophalen; onload zet hem daarna alsnog aan. De
     noscript-regel vangt op dat zonder JavaScript ook die onload niet afgaat. -->
<link rel="stylesheet" href="{v("cookiebalk.css")}" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="{v("cookiebalk.css")}" /></noscript>
<style data-page-css="{css_naam}">{inline(pagina_css)}</style>

<link rel="icon" href="assets/favicon/sfh-favicon.ico" sizes="16x16 32x32 48x48" />
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon/sfh-favicon-32.png" />
<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon/sfh-favicon-192.png" />
<link rel="apple-touch-icon" href="assets/favicon/sfh-apple-touch-icon.png" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="{D.NAAM}" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:url" content="{BASIS}/{bestand}" />
<meta property="og:title" content="{titel}" />
<meta property="og:description" content="{omschrijving}" />
<meta property="og:image" content="{BASIS}/assets/social/sfh-deelafbeelding.png" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{D.NAAM}: staalframebouw voor woningbouw, renovatie en utiliteitsbouw" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="{BASIS}/assets/social/sfh-deelafbeelding.png" />
<meta name="twitter:title" content="{titel}" />
<meta name="twitter:description" content="{omschrijving}" />

{ld_blokken}
</head>

<body{body_attr}>
<a class="skip-link" href="#main-content">Naar de inhoud</a>

<!-- De header en het mobiele paneel staan bewust BUITEN #smooth-wrapper.
     ScrollSmoother verschuift de inhoud met een transform, en onder een
     transform hangt position:fixed aan dat element in plaats van aan het
     scherm. Ze blijven daardoor ook staan bij een pagina-overgang; welke
     menulink actief is wordt in page-transitions.js bijgewerkt. -->
{header(actief or bestand)}

<div id="smooth-wrapper">
<div id="smooth-content">

<div data-barba="wrapper">
<div class="app__wrapper" data-barba="container" data-barba-namespace="{namespace}">
<div class="content__wrapper">

<main id="main-content">

{inhoud}

</main>

{footer()}

<script src="{v("site.js")}"></script>
<script src="{v("contactformulier.js")}"></script>
{script_regels}
</div><!-- /.content__wrapper -->
</div><!-- /[data-barba=container] -->
</div><!-- /[data-barba=wrapper] -->

</div><!-- /#smooth-content -->
</div><!-- /#smooth-wrapper -->

{COOKIEBALK}

<!-- ================= PAGINA-OVERGANGEN =================
     Barba wisselt alleen de container hierboven om, GSAP animeert de wissel. -->
<!-- defer: de browser haalt ze op terwijl hij de pagina nog aan het ontleden is
     en voert ze daarna uit, in deze volgorde. Die volgorde is nodig, want
     ScrollTrigger heeft gsap nodig en page-transitions.js heeft Barba nodig. -->
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollSmoother.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@barba/core@2.10.3/dist/barba.umd.js"></script>
<script defer src="{v("cookiebalk.js")}"></script>
<script defer src="{v("analytics.js")}"></script>
<script defer src="{v("smooth-scroll.js")}"></script>
<script defer src="{v("page-transitions.js")}"></script>

</body>
</html>
'''


# ---------------------------------------------------------------------------
#  De band met partners
# ---------------------------------------------------------------------------
# De bronsite laat op zijn homepage onder de kop "Onze partners" zes logo's
# zien, met een link naar de site van die partij. Dat zijn de partners die
# hieronder staan; de rol erachter staat op /about-us/, /eps-wandsysteem/ of
# /werkwijze/ van de bronsite.
#
# Hier stonden dertien logo's van opdrachtgevers van de vorige eigenaar van dit
# template (Alstom, Ballast Nedam, Stork en tien andere). Die zijn eruit: het
# zijn geen opdrachtgevers van Steel Framing Holland en ze hier laten staan zou
# de bezoeker voorliegen. De bestanden staan nog in
# assets/logo/opdrachtgevers/ en kunnen weg.
#
# De logobestanden zijn de logo's van de bronsite zelf, teruggesneden en op één
# hoogte gezet. Zie assets/logo/partners/HERKOMST.md.
LOGOMAP = "assets/logo/partners/"

# (bestand, naam, breedte, hoogte). De maten zijn die van het bestand; de band
# zet ze met CSS op 40px hoog (32px op een telefoon).
OPDRACHTGEVERS = [
    ("veerhuis-bouwsystemen.webp", "Veerhuis Bouwsystemen", 128, 80),
    ("mm-staal.webp", "MM Staal", 61, 80),
    ("finish-profiles.webp", "Finish Profiles", 380, 78),
    ("climate-construction.webp", "Climate Construction", 279, 80),
    ("veerhouse-voda.webp", "Veerhouse Voda", 380, 64),
    ("dutch-health.webp", "Dutch Health", 328, 80),
]


def _logoset(verborgen=False):
    """Eén reeks merken. De band zet er twee achter elkaar en schuift precies de
       helft op, zodat hij naadloos doorloopt; de tweede reeks is aria-hidden,
       dus een schermlezer hoort de namen één keer. Daarom krijgen de logo's in
       die tweede reeks een leeg alt: anders leest hij ze alsnog voor.

       Geen loading="lazy" op deze afbeeldingen. Het venster van de band knipt af
       met overflow: hidden, dus de browser ziet alles rechts van de rand als
       "niet in beeld" en laadt het nooit; de laatste logo's bleven daardoor
       leeg."""
    attr = ' aria-hidden="true"' if verborgen else ''
    regels = []
    for item in OPDRACHTGEVERS:
        if isinstance(item, (tuple, list)):
            bestand, naam = item[0], item[1]
            breedte = item[2] if len(item) > 2 else 190
            hoogte = item[3] if len(item) > 3 else 40
            alt = '' if verborgen else naam
            regels.append(
                f'          <li class="logo-slider__logo">'
                f'<img src="{LOGOMAP}{bestand}" alt="{alt}" '
                f'width="{breedte}" height="{hoogte}" '
                f'fetchpriority="low" decoding="async"></li>')
        else:
            regels.append(
                f'          <li class="logo-slider__logo">'
                f'<span class="logo-slider__woord">{item}</span></li>')
    return f'        <ul class="logo-slider__set"{attr}>\n' + "\n".join(regels) + '\n        </ul>'


def logoslider(nr, kop="Onze partners"):
    """De doorlopende band. Pauzeert bij hover en staat stil bij
       prefers-reduced-motion; dat gedrag zit in de CSS van het template."""
    return (f'  <section class="logo-slider" id="s{nr}-partners" '
            f'aria-label="{kop}" data-logoband>\n'
            '    <div class="logo-slider__venster">\n'
            '      <div class="logo-slider__spoor">\n'
            f'{_logoset()}\n{_logoset(verborgen=True)}\n'
            '      </div>\n'
            '    </div>\n'
            '  </section>')


def ctablok(nr, kop, tekst=None):
    """De afsluitende oproep: één merkvlak over de volle breedte, gecentreerd,
       met een knop naar de contactpagina. Het formulier zelf staat op contact.html
       en op offerte.html; dit is de aanloop erheen.

       De regel eronder kan per pagina worden meegegeven; staat er niets, dan
       valt hij terug op de vaste regel hieronder.

       Er staat één knop en niet twee. Het template had er twee ("Vraag een
       offerte aan" en "Bespreek uw project"), maar die zeggen voor deze
       bezoeker hetzelfde en beide formulieren doen hetzelfde: dan is kiezen
       werk zonder opbrengst. De prijsopgave is de knop, want daar staat het
       formulier met het extra veld projectadres; contact staat in de balk en
       in de voet."""
    regel = tekst or ('Vertel kort wat u wilt bouwen, of stuur de tekeningen mee. '
                      f'Wij nemen {REACTIETIJD} contact met u op.')
    return (f'  <section class="cta-slot" id="s{nr}-contact">\n'
            '    <div class="container">\n'
            '      <div class="cta-slot__hoofd">\n'
            '        <span class="subtitle cta-slot__label">Contact</span>\n'
            f'        <h2 class="cta-slot__kop">{kop}</h2>\n'
            f'        <p class="cta-slot__tekst">{regel}</p>\n'
            '        <div class="cta-slot__actie">\n'
            f'          {knop("Vraag een prijsopgave aan", "offerte.html")}\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n'
            '  </section>')


def paginahero(nr, ident, label, titel, beeld, alt=None, positie=None):
    """De hero met links de kop op grijs en rechts een foto. De <h1> staat in de
       HTML voor het beeld; onder 768px zet de CSS het beeld met order bovenaan,
       zodat de leesvolgorde blijft kloppen."""
    stijl = f' style="object-position:{positie}"' if positie else ""
    beeldtag = foto(beeld, laden="eager", maten="(max-width: 767px) 100vw, 50vw", alt=alt)
    if stijl:
        beeldtag = beeldtag.replace("<img ", f"<img{stijl} ")
    return (f'  <section class="paginahero" id="s{nr}-{ident}">\n'
            '    <div class="paginahero__kop">\n'
            f'      <span class="subtitle">{label}</span>\n'
            f'      <h1 class="paginahero__titel">{titel}</h1>\n'
            '    </div>\n'
            '    <div class="paginahero__beeld">\n'
            f'      {beeldtag}\n'
            '    </div>\n'
            '  </section>')


def patroonhero(nr, ident, label, titel):
    """Dezelfde hero, maar met het merkpatroon in plaats van een foto.

       Eén bestand voor beide breekpunten. Het template had er twee, omdat de
       vorige versie van het patroon een aparte vierkante variant voor de
       telefoon had aangeleverd. Van deze versie is er één liggende compositie
       (1440x940), en die snijdt op beide plekken goed bij: naast de kop op
       ongeveer 1,65:1, en op een telefoon als brede band op 7:3. De diagonalen
       zijn grote vlakken, dus een strook door het midden leest nog steeds als
       het patroon. Nagekeken op beide uitsneden.

       Hoe hoog het vak is, staat in de stylesheet en niet in het bestand: 7:3
       plus de hoogte van de vaste balk, want die ligt eroverheen. Daarom staat
       er `object-fit: cover` op en geen vaste uitsnede in het bestand.

       Het patroon is versiering en zegt niets wat de kop niet al zegt, dus
       alt="" en aria-hidden: een schermlezer slaat het over."""
    return (f'  <section class="paginahero paginahero--patroon" id="s{nr}-{ident}">\n'
            '    <div class="paginahero__kop">\n'
            f'      <span class="subtitle">{label}</span>\n'
            f'      <h1 class="paginahero__titel">{titel}</h1>\n'
            '    </div>\n'
            '    <div class="paginahero__beeld" aria-hidden="true">\n'
            '      <img src="assets/patronen/hero-patroon-v3-1440.webp" '
            'srcset="assets/patronen/hero-patroon-v3-720.webp 720w, '
            'assets/patronen/hero-patroon-v3-1000.webp 1000w, '
            'assets/patronen/hero-patroon-v3-1440.webp 1440w" '
            'sizes="(max-width: 767px) 100vw, 50vw" '
            'width="1440" height="940" alt="" loading="eager" '
            'fetchpriority="high" decoding="async">\n'
            '    </div>\n'
            '  </section>')


KLEURENRIJ = ("geel", "grijs", "wit", "groen")


def vlakkenrij(nr, ident, kop, vlakken, subtitel=None):
    """Kop met daaronder vier gekleurde vlakken over de volle breedte. vlakken is
       een lijst van (kop, tekst); de kleuren lopen vast in dezelfde volgorde,
       zodat de rij op elke pagina hetzelfde ritme heeft."""
    label = f'        <span class="subtitle" style="margin-bottom:var(--space-500)">{subtitel}</span>\n' if subtitel else ""
    items = "\n".join(
        f'      <li class="vlak vlak--{KLEURENRIJ[i % 4]}">\n'
        f'        <h3 class="vlak__kop">{titel}</h3>\n'
        f'        <p class="vlak__tekst">{tekst}</p>\n'
        '      </li>'
        for i, (titel, tekst) in enumerate(vlakken)
    )
    return (f'  <section class="vlakkenband" id="s{nr}-{ident}">\n'
            '    <div class="container">\n'
            '      <div class="vlakkenband__kop">\n'
            f'{label}'
            f'        <h2 class="section-heading">{kop}</h2>\n'
            '      </div>\n'
            '    </div>\n'
            '    <ul class="vlakkenrij">\n'
            f'{items}\n'
            '    </ul>\n'
            '  </section>')


# ---------------------------------------------------------------------------
#  Referenties
# ---------------------------------------------------------------------------
# ===========================================================================
#  HIER STOND DE CITATENSLIDER. Die is eruit.
# ===========================================================================
# Het template had een referentiesectie met drie citaten. Die citaten waren
# verzonnen: ze stonden op naam van "Architect", "Aannemer" en "Particuliere
# opdrachtgever" bij projecten van de vorige eigenaar van dit template.
#
# De bronsite van Steel Framing Holland heeft geen enkele referentie, geen
# review en geen klantcitaat. Een citaat verzinnen is dan het enige wat je kunt
# doen om deze sectie te vullen, en dat is precies wat niet mag.
#
# Op de homepage staat op die plek nu de werkwijze in vijf stappen. Die staat
# wél in de bron, op /werkwijze/, en beantwoordt de vraag die de bezoeker daar
# heeft ("hoe gaat dit lopen?") beter dan een citaat dat had gemoeten.
#
# Komen er echte referenties, dan is het component uit de git-historie van dit
# bestand terug te halen; de CSS ervoor (.quote-*) staat nog in styleguide.css.
# Zie CONTENT-TODO.md.


def beeldkaart(kop, tekst, beeld, alt=None, kleur="grey", href=None):
    """Een kaart met de foto erboven en de tekst eronder, twee per rij. Dit is de
       verticale variant van .cta-blocks-advanced."""
    binnen = (f'      <figure class="cta-blocks-advanced__banner">\n'
              f'        {foto(beeld, maten="(max-width: 991px) 100vw, 50vw", alt=alt)}\n'
              '        <span class="cta-blocks-advanced__backdrop" aria-hidden="true"></span>\n'
              '      </figure>\n'
              f'      <div class="cta-blocks-advanced__body cta-blocks-advanced__body--bg-{kleur}">\n'
              f'        <h3 class="cta-blocks-advanced__title">{kop}</h3>\n'
              '        <div class="cta-blocks-advanced__wrapper">\n'
              f'          <div class="cta-blocks-advanced__content"><p>{tekst}</p></div>\n'
              '        </div>\n'
              '      </div>')
    if href:
        omhulsel = (f'    <a class="cta-blocks-advanced__card cta-blocks-advanced__card--linked hover--icon" '
                    f'href="{href}">\n{binnen}\n    </a>')
    else:
        omhulsel = f'    <div class="cta-blocks-advanced__card">\n{binnen}\n    </div>'
    return f'  <div class="col-lg-6 col-12 kolom--vullend">\n{omhulsel}\n  </div>'

def dienstkaart(i, dienst, intro, kolom="col-lg-4"):
    """Eén dienst als kaart met de foto erboven.

       kolom bepaalt de breedte: col-lg-4 zet er drie op een rij (de
       hoofddiensten), col-lg-3 vier (de losse diensten daaronder)."""
    bestand, titel, sub, beeld = dienst
    return f'''        <div class="{kolom} col-md-6 col-12 kolom--vullend">
          <a class="cta-blocks-advanced__card cta-blocks-advanced__card--linked hover--icon" href="{bestand}"
             aria-label="{titel}: {sub}">
            <figure class="cta-blocks-advanced__banner cta-blocks-advanced__banner--verhouding">
              {foto(beeld, maten=BEELD_MATEN_3, alt="")}
            </figure>
            <div class="cta-blocks-advanced__body cta-blocks-advanced__body--bg-{'grey' if i % 2 == 0 else 'white'}">
              <span class="subtitle">Dienst 0{i + 1}</span>
              <div class="cta-blocks-advanced__wrapper">
                <div>
                  <h3 class="cta-blocks-advanced__title" style="margin-bottom:var(--space-500)">{D.afbreek(titel)}</h3>
                  <div class="cta-blocks-advanced__content"><p>{sub}</p>{f"<p>{intro}</p>" if intro else ""}</div>
                </div>
                {icoonknop("button--icon--56")}
              </div>
            </div>
          </a>
        </div>'''


def contactblok(onderwerp, kop="Neem contact op",
                intro="Vertel kort waar je tegenaan loopt. We reageren binnen "
                      f"{REACTIETIJD}."):
    """Het gedeelde formulier. De HTML wordt door contactformulier.js gerenderd;
       hier staat alleen de haak plus een terugval voor bezoekers zonder JS."""
    return f'''  <section class="band background--grey" id="s{onderwerp["nr"]}-contact">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-12">
          <span class="subtitle">Contact</span>
          <h2 class="section-heading" style="margin:var(--space-500) 0">{kop}</h2>
          <p class="article-body">{intro}</p>
          <p class="article-body" style="margin-top:var(--space-500)">
            Liever bellen? <a href="tel:{TELEFOON_LINK}">{TELEFOON_WEERGAVE}</a>
          </p>
        </div>
        <div class="col-lg-8 col-12">
          <div data-contactformulier data-onderwerp="{onderwerp["waarde"]}"></div>
          <noscript>
            <p class="article-body">Het formulier heeft JavaScript nodig. Mail ons gerust op
              <a href="mailto:{EMAIL}">{EMAIL}</a> of bel {TELEFOON_WEERGAVE}.</p>
          </noscript>
        </div>
      </div>
    </div>
  </section>'''


def faq_blok(nr, items, titel="Veelgestelde vragen"):
    """Drie FAQ-items als accordeon plus de bijbehorende FAQPage-structuurdata."""
    regels = []
    for i, (vraag, antwoorden) in enumerate(items):
        alineas = "".join(f"<p>{a}</p>" for a in antwoorden)
        regels.append(f'''          <div class="accordion__item">
            <button type="button" class="accordion__header" aria-expanded="false" aria-controls="faq-{nr}-{i}">
              <span class="accordion__number">{i + 1:02d}</span>
              <span class="accordion__title">{vraag}</span>
              <span class="accordion__suffix" aria-hidden="true"><span class="accordion__icon"></span></span>
            </button>
            <div class="accordion__details" id="faq-{nr}-{i}">
              <div class="accordion__details-inner article-body">{alineas}</div>
            </div>
          </div>''')
    return f'''  <section class="band background--white" id="s{nr}-faq">
    <div class="container">
      <div class="row">
        <div class="col-md-4 col-12">
          <span class="subtitle">FAQ</span>
          <h2 class="font-size--lg" style="margin-top:var(--space-500)">{titel}</h2>
        </div>
        <div class="col-md-8 col-12">
          <div class="accordion">
{chr(10).join(regels)}
          </div>
        </div>
      </div>
    </div>
  </section>'''


def faq_ld(items):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": _plat(v),
             "acceptedAnswer": {"@type": "Answer", "text": " ".join(_plat(a) for a in ant)}}
            for v, ant in items
        ],
    }, ensure_ascii=False, indent=2)


def _plat(tekst):
    import re, html
    return html.unescape(re.sub(r"<[^>]+>", "", tekst))


# NAV verwijst naar SERVICES, CURSUSSEN en foto(); die staan hierboven, dus de
# lijst wordt hier pas gevuld. header() leest hem daarna.
bouw_nav()
