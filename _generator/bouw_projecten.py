# -*- coding: utf-8 -*-
"""Het projectenoverzicht met filters, en een pagina per project.

De bronsite heeft 35 portfolio-items. De WordPress-categorie waaronder ze
hangen (portfolio_category) is op alle items leeg, waardoor de filter op
/projecten/ niets deed. Dit overzicht neemt die taak over met de indeling uit
`inhoud_sfh.py`, met het filtercomponent dat al in het template zat.

WAT ER PER PROJECT UIT DE BRON KOMT
  De titel, de datum, de plaats en soms een opdrachtgever, een projectsoort
  ("Prefab gevels") en een uitvoerende partij ("Thermogreen"). En de foto's:
  gemiddeld twaalf per project, tot achtendertig toe.

WAT ER NIET UIT DE BRON KOMT, EN HIER DUS NIET STAAT
  Een projectomschrijving. De bronpagina's hebben er geen: onder de titel staan
  alleen die gegevens en daarna de fotoreeks. Er is dus geen opgave, geen
  uitdaging, geen aanpak en geen resultaat om te plaatsen.

  Dat is bewust niet opgevuld. Een "uitdaging" en een "resultaat" bedenken bij
  een echt project van een echte opdrachtgever is precies wat een case study
  waardeloos maakt. Wat er per project wél staat, in `PROJECT_COPY` in
  inhoud_copy.py, is tweeledig: wat voor bouwwerk het is (dat volgt uit de
  titel en de bronvelden) en wat er op de foto's te zien is.

  Daardoor is de fotoreeks hier het bewijs en niet de illustratie: de galerij
  staat hoog op de pagina in plaats van onderaan.

  Zodra Steel Framing Holland per project vertelt wat de opgave was en welke
  rol zij hadden, kan elke projectpagina een volwaardige case study worden. Dat
  staat als eerste punt in CONTENT-TODO.md.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schil import *          # noqa: F401,F403
from schil import _plat
import inhoud_sfh as D
import inhoud_copy as C

UIT = pathlib.Path(__file__).resolve().parent.parent

VINKJE = ('<svg class="filter-pil__vink" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">'
          '<path d="M9.6 16.2 5.4 12l-1.4 1.4 5.6 5.6L20.4 8.2 19 6.8 9.6 16.2Z"/></svg>')

# Onder welke noemer een project valt, en waar de bezoeker leest hoe wij dat
# soort werk aanpakken. Dit is de doorstap van bewijs naar aanbod: iemand die
# op een villa is beland, moet bij "woningbouw" uitkomen.
#
# Bij het vorige template werd dit lijstje afgeleid uit de projecttekst ("staat
# er 'kelder' in, dan komt er een regel over de kelderconstructie bij"). Dat kan
# hier niet: deze bronpagina's hebben geen tekst. De categorie-indeling uit
# inhoud_sfh.py is nu de bron.
WERK_BIJ_CATEGORIE = {
    'Woningbouw': (
        'Woningbouw',
        'Van vrijstaande villa tot seriematige woningbouw: het frame, de vloeren en '
        'de gevels.', 'woningbouw.html'),
    'Renovatie': (
        'Renovatie',
        'Optoppen, gevels vervangen en gebouwdelen uitbreiden met een constructie die '
        'het bestaande gebouw licht belast.', 'renovatie.html'),
    'Utiliteitsbouw': (
        'Utiliteitsbouw',
        'Bedrijfsunits, kantoren, hallen en scholen, tot zes verdiepingen zonder '
        'hulpconstructie.', 'utiliteitsbouw.html'),
    'Buitenland': (
        'Werk buiten Nederland',
        'Voormontage in onze werkplaats en transport met eigen wagenpark, zodat er op '
        'locatie minder werk en minder materieel nodig is.',
        'lichtgewicht-staalframe.html'),
}

# Deze staat onder elk project: elk project hier is staalframebouw.
WERK_ALTIJD = (
    'Lichtgewicht staalframe',
    'Koudgevormde staalprofielen uit onze eigen productiefaciliteit, op maat '
    'gefabriceerd.', 'lichtgewicht-staalframe.html')

# Welke toepassingspagina en welk beeld bij een categorie horen, voor de
# doorstapkaarten onderaan een projectpagina.
DIENST_BIJ_CATEGORIE = {
    'Woningbouw': ('woningbouw.html', 'Woningbouw', 'sfh-woningbouw'),
    'Renovatie': ('renovatie.html', 'Renovatie', 'sfh-renovatie'),
    'Utiliteitsbouw': ('utiliteitsbouw.html', 'Utiliteitsbouw', 'sfh-utiliteitsbouw'),
}


def sleutelvorm(t):
    return "".join(c if c.isalnum() else '-' for c in t.lower()).strip('-')


def _lead(p):
    """De omschrijving bij een project, of leeg als die er niet is."""
    return C.project_lead(p['slug']) or ''


def _werkzaamheden(p):
    """Onder welke noemers dit project valt, met de doorstap per noemer."""
    uit = [WERK_BIJ_CATEGORIE[c] for c in p['categorieen'] if c in WERK_BIJ_CATEGORIE]
    uit.append(WERK_ALTIJD)
    return uit


# ---------------------------------------------------------------- overzicht
def _filtergroep(label, naam, waarden, alles):
    pillen = [f'''          <button type="button" class="filter-pil is-actief" data-filter="{naam}" data-waarde="alles" aria-pressed="true">
            {VINKJE}<span>{alles}</span>
          </button>''']
    for w in waarden:
        pillen.append(f'''          <button type="button" class="filter-pil" data-filter="{naam}" data-waarde="{sleutelvorm(w)}" aria-pressed="false">
            {VINKJE}<span>{w}</span>
          </button>''')
    return f'''        <div class="filter-groep" role="group" aria-label="{label}">
{chr(10).join(pillen)}
        </div>'''


def _kaart(p):
    cats = " ".join(sleutelvorm(c) for c in p['categorieen'])
    labels = "".join(f'<span class="case-kaart__label">{c}</span>' for c in p['categorieen'])
    plaats = f'<span class="case-kaart__label">{p["plaats"]}</span>' if p['plaats'] else ''
    jaar = f'<span class="case-kaart__label">{p["datum"]}</span>' if p['datum'] else ''
    return f'''        <article class="case-kaart" data-categorie="{cats}">
          <a class="case-kaart__link hover--icon" href="{p['bestand']}">
            <figure class="case-kaart__beeld">
              {foto(p['beeld'], maten="(max-width: 767px) 100vw, (max-width: 1199px) 50vw, 33vw", alt="")}
            </figure>
            <div class="case-kaart__inhoud">
              <div class="case-kaart__meta">{labels}{plaats}{jaar}</div>
              <h2 class="case-kaart__titel">{D.afbreek(D._tekens(p['titel']))}</h2>
              <p class="case-kaart__tekst">{D._tekens(_lead(p))}</p>
              <div class="case-kaart__voet">
                <span class="case-kaart__lees">Bekijk het project</span>
                {icoonknop("", "button--secundair")}
              </div>
            </div>
          </a>
        </article>'''


def overzicht():
    per_cat = " &middot; ".join(f'{len(D.projecten_in(c))}&times; {c.lower()}'
                                for c in D.CATEGORIEEN)
    inhoud = f'''{patroonhero("01", "projecten", "Projecten", C.PROJECTEN_OVERZICHT['h1'])}

  <section class="band background--white" id="s02-introductie">
    <div class="container">
      <div class="row g-0">
        <div class="col-lg-8 col-12">
          <h2 class="section-heading" style="margin:0 0 var(--space-500)">{C.PROJECTEN_OVERZICHT['kop']}</h2>
          <p class="case-lead">{C.PROJECTEN_OVERZICHT['lead']}</p>
          <p class="article-body" style="margin-top:var(--space-500)">
            {len(D.PROJECTEN)} projecten: {per_cat}.
          </p>
        </div>
      </div>
    </div>
  </section>

  <section class="cases-overzicht" id="s03-projecten">
    <div class="container">
      <div class="cases-overzicht__filters">
{_filtergroep("Filter projecten op categorie", "categorie", D.CATEGORIEEN, "Alle projecten")}
      </div>

      <p class="cases-overzicht__telling" role="status" aria-live="polite"></p>

      <div class="cases-overzicht__raster" id="caseRaster">
{chr(10).join(_kaart(p) for p in D.PROJECTEN)}
      </div>

      <p class="cases-overzicht__leeg" hidden>Geen projecten in deze categorie. Zet het filter terug op &lsquo;alle projecten&rsquo;.</p>
    </div>
  </section>

{logoslider("04")}

{ctablok("05", C.PROJECTEN_OVERZICHT['slot_kop'], C.PROJECT['slot'])}
'''
    (UIT / 'projecten.html').write_text(pagina(
        bestand='projecten.html',
        titel=C.seo_titel('projecten.html'),
        omschrijving=C.SEO['projecten.html'][1],
        namespace='projecten', pagina_css='cases.css', css_naam='cases',
        inhoud=inhoud, scripts=['cases.js'],
    ), encoding='utf-8')
    return 'projecten.html'


# ---------------------------------------------------------------- detailpagina
def _blok(nr, ident, kop, alineas, achtergrond='white', extra=''):
    body = "\n".join(f'          <p>{a}</p>' for a in alineas)
    return f'''  <section class="band background--{achtergrond}" id="s{nr}-{ident}">
    <div class="container">
      <div class="case-blok__inner">
        <h2 class="case-blok__kop">{kop}</h2>
        <div class="case-blok__body">
{body}
        </div>
{extra}
      </div>
    </div>
  </section>'''


def detail(p):
    eerste = next((c for c in p['categorieen'] if c in DIENST_BIJ_CATEGORIE), None)
    werk = _werkzaamheden(p)
    nr = [1]

    def volgend():
        nr[0] += 1
        return f'{nr[0]:02d}'

    delen = [paginahero('01', 'project', " &middot; ".join(p['categorieen']),
                        D.afbreek(D._tekens(p['titel'])), p['beeld'])]

    # 02 de lead: de regel van de bronsite, groot gezet
    delen.append(f'''  <section class="band background--white" id="s{volgend()}-lead">
    <div class="container">
      <div class="case-blok__inner">
        <p class="case-lead">{D._tekens(_lead(p))}</p>
      </div>
    </div>
  </section>''')

    # 03 de fotoreeks. Dit is wat de bron van dit project wél heeft, en het is
    # het bewijs dat het gebouwd is; daarom staat het hoog op de pagina en niet
    # onderaan als illustratie.
    galerij = [g for g in p['galerij'] if g in FOTOS]
    if galerij:
        beelden = "\n".join(
            f'''          <li>
            <figure>{foto(g, maten="(max-width: 576px) 100vw, (max-width: 991px) 50vw, 33vw")}</figure>
          </li>''' for g in galerij)
        delen.append(f'''  <section class="band background--grey" id="s{volgend()}-galerij">
    <div class="container">
      <div class="case-blok__inner">
        <h2 class="case-blok__kop">{C.PROJECT['project_kop']}</h2>
        <ul class="case-galerij" role="list">
{beelden}
        </ul>
      </div>
    </div>
  </section>''')

    # 04 wat er is gedaan, afgeleid uit de projecttekst
    if werk:
        punten = "\n".join(
            f'          <li><strong>{t}</strong><br>{tl} '
            f'<a href="{b}">Meer over {t.lower()}</a></li>' for t, tl, b in werk)
        delen.append(f'''  <section class="band background--white" id="s{volgend()}-werkzaamheden">
    <div class="container">
      <div class="case-blok__inner">
        <h2 class="case-blok__kop">{C.PROJECT['werk_kop']}</h2>
        <div class="case-blok__body">
          <p>{C.PROJECT['werk_lead']}</p>
        </div>
        <ul class="case-lijst">
{punten}
        </ul>
      </div>
    </div>
  </section>''')

    # 06 projectgegevens. Alleen de velden die de bron geeft; wat er niet staat
    # wordt niet als leeg veld getoond maar als regel eronder benoemd, zodat de
    # lijst niet half uit markeringen bestaat.
    regels = [('Noemer', ' &middot; '.join(p['categorieen']) or None),
              ('Plaats', p['plaats'] or None),
              ('Datum', p['datum'] or None),
              ('Opdrachtgever', p['opdrachtgever'] or None),
              ('Soort project', p['soort'] or None),
              ('Uitvoering', p['uitvoering'] or None)]
    gegevens = "\n".join(f'          <li><strong>{k}</strong><br>{D._tekens(v)}</li>'
                          for k, v in regels if v)
    leeg = [k.lower() for k, v in regels if not v and k in ('Opdrachtgever', 'Datum')]
    ontbreekt_blok = ''
    if leeg:
        woorden = ' en '.join(leeg)
        ontbreekt_blok = (
            '\n        <div class="case-blok__body" style="margin-top:var(--space-500)">'
            f'\n          <p>De {woorden} van dit project staat niet op de bronpagina en is '
            'daarom niet vermeld.</p>\n        </div>')
    delen.append(f'''  <section class="band background--grey" id="s{volgend()}-gegevens">
    <div class="container">
      <div class="case-blok__inner">
        <h2 class="case-blok__kop">{C.PROJECT['gegevens_kop']}</h2>
        <ul class="case-lijst">
{gegevens}
        </ul>{ontbreekt_blok}
      </div>
    </div>
  </section>''')

    # 07 verwante projecten
    if eerste:
        anderen = [q for q in D.projecten_in(eerste) if q['slug'] != p['slug']][:2]
        if anderen:
            rijen = []
            for i, q in enumerate(anderen):
                rijen.append(f'''      <a class="cases-grid__row {'cases-grid__row--grey' if i % 2 == 0 else 'cases-grid__row--white'} hover--icon"
         href="{q['bestand']}" aria-label="{_plat(q['titel'])}">
        <div class="cases-grid__body">
          <div class="cases-grid__meta"><span class="cases-grid__meta-item">{eerste}</span></div>
          <h3 class="cases-grid__title">{D.afbreek(D._tekens(q['titel']))}</h3>
          <div class="cases-grid__wrapper">
            <p class="cases-grid__text">{D._tekens(_lead(q))}</p>
            {icoonknop("button--icon--54", "button--secundair")}
          </div>
        </div>
        <figure class="cases-grid__image">
          {foto(q['beeld'], maten="(max-width: 991px) 100vw, 50vw")}
        </figure>
      </a>''')
            delen.append(f'''  <section class="cases-grid" id="s{volgend()}-verwant">
    <div class="container">
      <div class="cases-grid__header">
        <h2 class="cases-grid__heading">Meer {eerste.lower()}</h2>
        {knop("Alle projecten", "projecten.html", "secundair")}
      </div>
      <div class="cases-grid__list">
{chr(10).join(rijen)}
      </div>
    </div>
  </section>''')

    # 08 doorstap naar de dienst en de offerte
    if eerste:
        bestand, titel, beeld = DIENST_BIJ_CATEGORIE[eerste]
        delen.append(f'''  <section class="content-block" id="s{volgend()}-dienst">
    <div class="container">
      <div class="row g-0">
{beeldkaart(titel, "Wat wij bij dit soort werk doen, van eerste berekening tot gemonteerd frame.",
            beeld, alt="", kleur="grey", href=bestand)}
{beeldkaart("Prijsopgave aanvragen",
            "Vertel kort wat u wilt bouwen; wij kijken wat er in staalframe mogelijk is.",
            'sfh-offerte', alt="", kleur="white", href="offerte.html")}
      </div>
    </div>
  </section>''')

    delen.append(logoslider(volgend()))
    delen.append(ctablok(volgend(), C.PROJECT['slot_kop'], C.PROJECT['slot']))

    # De bronsite heeft per project geen meta description; titel en
    # omschrijving worden opgebouwd uit de projectgegevens die er wél staan.
    titel, omschrijving = C.project_seo(p['titel'], p['plaats'], p['categorieen'])
    (UIT / p['bestand']).write_text(pagina(
        bestand=p['bestand'], titel=titel, omschrijving=omschrijving,
        namespace='project', pagina_css='cases.css', css_naam='cases',
        inhoud="\n\n".join(delen),
        extra_ld=json.dumps({
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": p['titel'],
            "description": _plat(_lead(p)),
            "creator": {"@type": "Organization", "name": D.NAAM_VOLUIT},
        }, ensure_ascii=False, indent=2),
    ), encoding='utf-8')
    return p['bestand']


def main():
    gemaakt = [overzicht()] + [detail(p) for p in D.PROJECTEN]
    print(f"projecten: overzicht + {len(gemaakt) - 1} detailpagina's")
    return gemaakt


if __name__ == '__main__':
    main()
