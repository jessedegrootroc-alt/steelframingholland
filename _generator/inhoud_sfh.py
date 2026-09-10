# -*- coding: utf-8 -*-
"""De inhoud van de site: alle feiten komen uit de export van de bronsite.

De teksten staan niet in dit bestand maar in `sfh/`, de contentexport van
www.steelframingholland.nl. Hier staat wat er met welke tekst gebeurt: welke
pagina's er zijn, welke dienst waar hangt, welke foto erbij hoort en onder
welke categorie een project valt.

Zo hoeft een tekstwijziging maar op één plek: in de export. En een nieuw
project of een nieuwe dienst is één regel in de tabellen hieronder.

Er wordt niets bijverzonnen. Ontbreekt iets in de bron, dan staat er
NIET_GEVONDEN en dat rendert als een zichtbare markering, zodat het niet per
ongeluk zo live gaat.

WAT DE BRON NIET HEEFT
  De bronsite noemt geen KvK-nummer, geen openingstijden, geen teamgrootte,
  geen oprichtingsjaar, geen certificeringen en geen referenties. Die velden
  staan daarom op NIET_GEVONDEN of zijn helemaal weggelaten; ze zijn niet
  geraden. Zie CONTENT-TODO.md voor wat Steel Framing Holland nog moet
  aanleveren.
"""
import json
import pathlib
import re

DATA = pathlib.Path(__file__).resolve().parent / 'sfh'
NIET_GEVONDEN = '[CONTENT NODIG]'
BRON_MARKER = '[CONTENT NIET GEVONDEN]'      # zo heet het in de export


def _laad(naam):
    return json.loads((DATA / naam).read_text(encoding='utf-8'))


_services = {s['slug']: s for s in _laad('services.json')}
_projecten = _laad('projects.json')
_bedrijf = _laad('company.json')
_contact = _laad('contact.json')


def _schoon(t):
    """Bronmarkering omzetten naar onze eigen markering."""
    if not t or t == BRON_MARKER:
        return NIET_GEVONDEN
    return t


def splits_lang(alineas, maximum=55):
    """Een alinea van meer dan `maximum` woorden opknippen op zinsgrens.

       De woorden veranderen niet; er komt alleen een alineagrens waar toch al
       een punt stond. De bronsite heeft alinea's van tachtig woorden en die
       lezen op een scherm als een muur."""
    uit = []
    for a in alineas:
        if len(a.split()) <= maximum:
            uit.append(a)
            continue
        zinnen = re.split(r'(?<=[.!?])\s+', a.strip())
        blok = []
        for zin in zinnen:
            blok.append(zin)
            if sum(len(z.split()) for z in blok) >= maximum * 0.6:
                uit.append(' '.join(blok))
                blok = []
        if blok:
            if uit and len(' '.join(blok).split()) < 12:
                uit[-1] += ' ' + ' '.join(blok)
            else:
                uit.append(' '.join(blok))
    return uit


def _tekens(t):
    """Losse aanhalings- en deeltekens netjes maken; de tekst zelf blijft."""
    if not t:
        return t
    t = (t.replace('’', '&rsquo;').replace('‘', '&lsquo;')
          .replace('“', '&ldquo;').replace('”', '&rdquo;')
          .replace('–', '&ndash;').replace('—', '&mdash;')
          .replace('é', '&eacute;').replace('ë', '&euml;').replace('ï', '&iuml;')
          .replace('ö', '&ouml;').replace('ü', '&uuml;').replace('è', '&egrave;')
          .replace('á', '&aacute;').replace('í', '&iacute;').replace('ó', '&oacute;')
          .replace('ú', '&uacute;').replace('ç', '&ccedil;').replace('â', '&acirc;')
          .replace('ê', '&ecirc;').replace('î', '&icirc;').replace('û', '&ucirc;')
          .replace('É', '&Eacute;').replace('Ë', '&Euml;').replace('Ï', '&Iuml;')
          .replace('²', '&sup2;').replace('€', '&euro;').replace('…', '&hellip;'))
    return t


# ---------------------------------------------------------------------------
#  Afbreken van lange samenstellingen
# ---------------------------------------------------------------------------
# De vaktermen van dit bedrijf zijn Nederlandse samenstellingen van twintig
# tekens en meer. In een hero van 80px of een kaart van een kwart pagina moeten
# die afbreken. De automatische afbreking van de browser zet de streep op de
# verkeerde plek ("Staalfram-ebouw"), dus geven we hem zelf op met een zacht
# afbreekstreepje: dat is onzichtbaar zolang het woord past.
#
# Alleen voor zichtbare koppen. In een <title>, meta description of schema.org
# hoort geen zacht afbreekstreepje, dus die gebruiken de gewone titel.
AFBREEKPUNTEN = [
    ('Staalframebouw', 'Staalframe&shy;bouw'),
    ('staalframebouw', 'staalframe&shy;bouw'),
    ('Utiliteitsbouw', 'Utiliteits&shy;bouw'),
    ('utiliteitsbouw', 'utiliteits&shy;bouw'),
    ('Woningbouw', 'Woning&shy;bouw'),
    ('woningbouw', 'woning&shy;bouw'),
    ('Wandsystemen', 'Wand&shy;systemen'),
    ('wandsystemen', 'wand&shy;systemen'),
    ('wandsysteem', 'wand&shy;systeem'),
    ('Productiefaciliteit', 'Productie&shy;faciliteit'),
    ('productiefaciliteit', 'productie&shy;faciliteit'),
    ('Brandweerkazerne', 'Brandweer&shy;kazerne'),
    ('Vakantiebungalows', 'Vakantie&shy;bungalows'),
    ('vakantiebungalows', 'vakantie&shy;bungalows'),
    ('Natuurvillapark', 'Natuur&shy;villapark'),
    ('Vakantiehuisjes', 'Vakantie&shy;huisjes'),
    ('Vakantiehuis', 'Vakantie&shy;huis'),
    ('Ziekenhuispersoneel', 'Ziekenhuis&shy;personeel'),
    ('ziekenhuispersoneel', 'ziekenhuis&shy;personeel'),
    ('staalframe-elementen', 'staalframe-&shy;elementen'),
    ('Gevelrenovatie', 'Gevel&shy;renovatie'),
    ('Draagconstructie', 'Draag&shy;constructie'),
    ('draagconstructie', 'draag&shy;constructie'),
    ('Staalconstructie', 'Staal&shy;constructie'),
    ('staalconstructie', 'staal&shy;constructie'),
]


def afbreek(titel):
    """Zachte afbreekstreepjes in een zichtbare kop."""
    if not titel:
        return titel
    uit = titel
    for heel, gebroken in AFBREEKPUNTEN:
        uit = uit.replace(heel, gebroken)
    return uit


# ---------------------------------------------------------------------------
#  Diensten
# ---------------------------------------------------------------------------
# De bronsite deelt het aanbod in twee menugroepen: "Toepassingen" (waarvoor
# bouw je) en "Staalframebouw" (waarmee bouw je). Die tweedeling houden we aan,
# omdat het precies de twee vragen zijn waarmee een bezoeker binnenkomt.
#
# De drie toepassingen zijn de hoofddiensten: daar landt iemand die weet wat hij
# wil bouwen. De vier techniekpagina's staan daaronder en leggen uit waarmee dat
# gebeurt; ze horen bij alle drie de toepassingen en hangen dus niet onder één.
#
# (bestand, slug in de export, titel op de site, beeldsleutel)
HOOFDDIENSTEN = [
    ('woningbouw.html',     'woningbouw',     'Woningbouw',     'sfh-woningbouw'),
    ('renovatie.html',      'renovatie',      'Renovatie',      'sfh-renovatie'),
    ('utiliteitsbouw.html', 'utiliteitsbouw', 'Utiliteitsbouw', 'sfh-utiliteitsbouw'),
]

# (bestand, slug, titel, ouder, beeldsleutel)
# Ouder is None: dit zijn geen onderdelen van één toepassing maar de techniek
# eronder. Ze staan in het menu onder "Staalframebouw".
DIENSTEN = [
    ('ontwerpen-tekenen-en-berekenen.html', 'ontwerpen-tekenen-en-berekenen',
     'Ontwerpen, tekenen en berekenen', None, 'sfh-engineering'),
    ('lichtgewicht-staalframe.html', 'lichtgewicht-staalframe',
     'Lichtgewicht staalframe', None, 'sfh-staalframe'),
    ('eps-wandsysteem.html', 'eps-wandsysteem',
     'EPS wandsysteem', None, 'sfh-eps'),
    ('overige-wandsystemen.html', 'overige-wandsystemen',
     'Overige wandsystemen', None, 'sfh-wandsystemen'),
]

TECHNIEK = DIENSTEN          # sprekender naam voor dezelfde tabel
LOSSE_DIENSTEN = [d for d in DIENSTEN if d[3] is None]


def _blokken(slug):
    """De brontekst van een dienstpagina, klaar om te plaatsen.

       De bronpagina's van deze site zijn kort: twee tot vier alinea's zonder
       tussenkoppen, en op één pagina een opsomming. Er valt hier dus niets te
       sorteren op soort zoals bij een pagina met h3'jes; de eerste alinea is de
       intro en de rest is de uitleg.

       Levert (intro, secties, faq, cta):
         intro   - de eerste alinea van de bronpagina
         secties - de overige alinea's, plus de opsomming als de bron die heeft
         faq     - leeg: de bronsite heeft geen vraag-en-antwoord
         cta     - None: de bronsite heeft geen wervende slotregel
    """
    s = _services[slug]
    alineas = list(s['paragraphs'])
    lijsten = [l for l in s['lists'] if l]
    intro = alineas[:1]
    rest = alineas[1:]
    secties = []
    if rest:
        secties.append({'kop': None, 'alineas': rest, 'lijsten': []})
    if lijsten:
        secties.append({'kop': None, 'alineas': [], 'lijsten': lijsten})
    return intro, secties, [], None


def dienst(bestand):
    """Alle gegevens voor één dienstpagina, klaar voor de bouwer."""
    rij = next((d for d in DIENSTEN if d[0] == bestand), None)
    if rij:
        _, slug, titel, ouder, beeld = rij
    else:
        rij = next(h for h in HOOFDDIENSTEN if h[0] == bestand)
        _, slug, titel, beeld = rij
        ouder = None

    s = _services[slug]
    intro, secties, faq, cta = _blokken(slug)
    return {
        'bestand': bestand,
        'titel': titel,
        'ouder': ouder,
        'is_hoofddienst': bestand in [h[0] for h in HOOFDDIENSTEN],
        'groep': s['group'],
        'beeld': beeld,
        'h1': titel,
        'intro': intro,
        'secties': secties,
        'faq': faq,
        'cta': cta,
        # De bronsite heeft op geen enkele dienstpagina een meta description en
        # gebruikt als title alleen "<Naam> | Steel Framing Holland". Bruikbare
        # metadata schrijven we dus zelf, in inhoud_copy.py.
        'seo_titel': NIET_GEVONDEN,
        'seo_omschrijving': NIET_GEVONDEN,
        'bron': s['sourceUrl'],
    }


def kinderen(hoofddienst_titel):
    """De diensten onder een hoofddienst.

       Deze site heeft die hiërarchie niet: de vier techniekpagina's horen bij
       alle drie de toepassingen. Blijft daarom leeg, waardoor de bouwer de
       sectie "wat valt hieronder" overslaat."""
    return []


# ---------------------------------------------------------------------------
#  Projecten
# ---------------------------------------------------------------------------
# De bronsite heeft 35 portfolio-items. De categorie waaronder ze in WordPress
# hangen (portfolio_category) is op alle items leeg, en de filter op
# /projecten/ deed daardoor niets. Hieronder staat per project onder welke
# noemer het valt.
#
# Dit is een indeling, geen bewering: een brandweerkazerne is utiliteitsbouw en
# een villa is woningbouw. Waar de bron zelf het projectsoort noemt
# ("Prefab gevels") is die gevolgd. Waar het type niet met zekerheid uit de
# bron of het beeld blijkt, staat het project alleen onder de categorie die wel
# vaststaat.
WONINGBOUW, RENOVATIE, UTILITEIT, BUITENLAND = (
    'Woningbouw', 'Renovatie', 'Utiliteitsbouw', 'Buitenland')

CATEGORIE_BIJ_PROJECT = {
    'aanbouw-schuur-texel':               [RENOVATIE],
    'abc-cluster':                        [RENOVATIE],
    'apparterra':                         [RENOVATIE],
    'bonaire-off-grid-woning':            [WONINGBOUW, BUITENLAND],
    'brandweerkazerne-zwolle':            [UTILITEIT],
    'cite-soleil':                        [BUITENLAND],
    'dirkshoeve-vakantiebungalows-fase-1': [WONINGBOUW],
    'dirkshoeve-vakantiebungalows-fase-2': [WONINGBOUW],
    'drijvende-woningen-in-delft':        [WONINGBOUW],
    'gevel-renovatie':                    [RENOVATIE],
    'hotel-de-grote-kerk-in-hoorn':       [RENOVATIE, UTILITEIT],
    'houses-in-bonaire':                  [WONINGBOUW, BUITENLAND],
    'kantershof-optopper':                [RENOVATIE],
    'kantoor-en-werkruimte':              [UTILITEIT],
    'kinderopvang':                       [UTILITEIT],
    'naarden-renovatie':                  [RENOVATIE],
    'natuurvillapark-waalerburght-texel': [WONINGBOUW],
    'school-in-haiti':                    [UTILITEIT, BUITENLAND],
    'steel-framing-holland-irak':         [BUITENLAND],
    'thema-dreven-portiek-flats-utrecht': [RENOVATIE],
    'utrecht-portiek-flats-renovatie':    [RENOVATIE],
    'vakantiehuis-bonaire-crown-west-2':  [WONINGBOUW, BUITENLAND],
    'vakantiehuisjes-panoven':            [WONINGBOUW],
    'veerhuis-building':                  [WONINGBOUW],
    'verblijf-voor-ziekenhuispersoneel':  [UTILITEIT, BUITENLAND],
    'villa-in-bergen':                    [WONINGBOUW],
    'villa-te-schagerbrug':               [WONINGBOUW],
    'villa-te-zoetermeer':                [WONINGBOUW],
    'voortgang-ibiza-woonhuis':           [WONINGBOUW, BUITENLAND],
    'voortgang-villa-noordwijkerhout':    [WONINGBOUW],
    'voortgang-woning-azoren-pico':       [WONINGBOUW, BUITENLAND],
    'woning-nes-aan-de-amstel':           [WONINGBOUW],
    'woningen-lochem':                    [WONINGBOUW],
    'woonhuis':                           [WONINGBOUW],
    'woonhuis-uk':                        [WONINGBOUW, BUITENLAND],
}

# De volgorde op het overzicht en op de homepage. Vooraan staat wat het sterkst
# laat zien wat dit bedrijf kan: afgeronde bouwwerken met bruikbaar beeld.
VOLGORDE = [
    'villa-in-bergen', 'brandweerkazerne-zwolle', 'drijvende-woningen-in-delft',
    'vakantiehuis-bonaire-crown-west-2', 'woning-nes-aan-de-amstel',
    'utrecht-portiek-flats-renovatie', 'kinderopvang', 'kantoor-en-werkruimte',
    'naarden-renovatie', 'voortgang-villa-noordwijkerhout', 'woningen-lochem',
    'veerhuis-building', 'natuurvillapark-waalerburght-texel',
    'dirkshoeve-vakantiebungalows-fase-2', 'dirkshoeve-vakantiebungalows-fase-1',
    'villa-te-zoetermeer', 'villa-te-schagerbrug', 'woonhuis', 'woonhuis-uk',
    'hotel-de-grote-kerk-in-hoorn', 'kantershof-optopper',
    'thema-dreven-portiek-flats-utrecht', 'apparterra', 'abc-cluster',
    'gevel-renovatie', 'aanbouw-schuur-texel', 'vakantiehuisjes-panoven',
    'voortgang-ibiza-woonhuis', 'voortgang-woning-azoren-pico',
    'houses-in-bonaire', 'bonaire-off-grid-woning',
    'steel-framing-holland-irak', 'school-in-haiti',
    'verblijf-voor-ziekenhuispersoneel', 'cite-soleil',
]


def _projecten_opbouwen():
    uit = []
    for p in _projecten:
        slug = p['slug']
        m = p.get('meta', {})
        uit.append({
            'slug': slug,
            'bestand': f'project-{slug}.html',
            'titel': p['title'],
            'plaats': m.get('plaats', ''),
            'datum': m.get('datum', ''),
            'opdrachtgever': m.get('opdrachtgever', ''),
            'soort': m.get('soort', ''),
            'uitvoering': m.get('uitvoering', ''),
            'categorieen': CATEGORIE_BIJ_PROJECT.get(slug, []),
            'beeld': f'sfh-project-{slug}',
            'galerij': [f'sfh-project-{slug}-{i:02d}' for i in range(2, 5)],
            'bron': p['sourceUrl'],
            'bron_alineas': p.get('paragraphs', []),
            'aantal_bronbeelden': len(p.get('images', [])),
        })
    rang = {s: i for i, s in enumerate(VOLGORDE)}
    uit.sort(key=lambda r: (rang.get(r['slug'], 999), r['titel'].lower()))
    return uit


PROJECTEN = _projecten_opbouwen()
CATEGORIEEN = [WONINGBOUW, RENOVATIE, UTILITEIT, BUITENLAND]


def project(slug):
    return next(p for p in PROJECTEN if p['slug'] == slug)


def projecten_in(categorie, maximaal=None):
    lijst = [p for p in PROJECTEN if categorie in p['categorieen']]
    return lijst[:maximaal] if maximaal else lijst


# ---------------------------------------------------------------------------
#  Bedrijf en contact
# ---------------------------------------------------------------------------
NAAM = _bedrijf['name']
NAAM_VOLUIT = _bedrijf['name']
TELEFOON_WEERGAVE = _contact['phone']
TELEFOON_LINK = _contact['phoneLink']
MOBIEL_WEERGAVE = _contact['mobile']
MOBIEL_LINK = _contact['mobileLink']
CONTACTPERSOON = _contact['contactPerson']
EMAIL = _contact['email']
KVK = _schoon(_contact['kvk'])
STRAAT = _contact['address']['street']
POSTCODE_PLAATS = _contact['address']['postalCodeCity']
ADRES = f'{STRAAT}, {POSTCODE_PLAATS}'
WERKPLAATS_INGANG = _contact['workshopEntrance']
COPYRIGHT = f"&copy; {_bedrijf['copyright']}"

# De brontekst van de bronsite, ongewijzigd. De herschreven versie staat in
# inhoud_copy.py; deze blijft de feitenbasis en de herkomst.
HOME_BRON = _bedrijf['homeParagraphs']
OVER_ONS_BRON = _bedrijf['aboutParagraphs']
WERKWIJZE_BRON = _bedrijf['werkwijzeParagraphs']
PROFIELBEWERKINGEN = _bedrijf['werkwijzeProfielbewerkingen']
PARTNERS = _bedrijf['partners']
URGENT_WONEN = _bedrijf['urgentWonen']
NIEUWS = _bedrijf['nieuws']

CONTACT = _contact


def alinea_lijst(tekst):
    """Een tekstblok uit de export opsplitsen in losse alinea's."""
    if not tekst or tekst == BRON_MARKER:
        return [NIET_GEVONDEN]
    if isinstance(tekst, list):
        return list(tekst)
    return [a.strip() for a in tekst.split('\n\n') if a.strip()]
