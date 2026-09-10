# -*- coding: utf-8 -*-
"""De homepage.

De bronsite heeft op zijn homepage een slider met drie regels, drie alinea's
over staalframebouw, een nieuwsblok, drie projecten en een partnerband. Wat
ontbreekt is een reden om verder te klikken: er staat wat staalframebouw is,
maar niet wat de bezoeker eraan heeft of wat hij nu moet doen.

Deze homepage volgt daarom een conversieflow:

  01 hero            wat doen zij, voor wie, en wat is mijn volgende stap (met film)
  02 partnerband     met wie werken zij (de zes partners van de bronsite)
  03 statement       waarom een stalen frame, en voor wie zij werken
  04 werkwijze       hoe gaat dit lopen: de vijf stappen uit de bron
  05 toepassingen    waarvoor bouwen zij, en de techniek erachter
  06 projecten       bewijs dat zij dit soort werk doen
  07 over ons        waarom deze partij: de keten in eigen hand
  08 slot            CTA

Op de plek van 04 stond in het template een citatenslider met drie verzonnen
referenties. Steel Framing Holland heeft geen referenties op zijn site, dus is
die eruit; de werkwijze staat wél in de bron en beantwoordt op deze plek de
vraag die de bezoeker heeft.

De feiten komen uit `sfh/`, de formulering uit `inhoud_copy.py`.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schil import *          # noqa: F401,F403
from schil import _plat
import inhoud_sfh as D
import inhoud_copy as C
import inhoud_dienst_verhaal as V

UIT = pathlib.Path(__file__).resolve().parent.parent

def _p(alineas):
    return "\n".join(f'          <p>{D._tekens(a)}</p>' for a in alineas)


# De drie categorieën waaruit de homepage één project laat zien, in deze
# volgorde: dezelfde drie als de toepassingen in het menu, zodat een bezoeker
# van elk van de drie richtingen één voorbeeld ziet.
UITGELICHT = ('Woningbouw', 'Renovatie', 'Utiliteitsbouw')


def _projectrijen(maximaal=3):
    rijen = []
    # Eén project per categorie, maar wel drie verschillende. Een project kan
    # onder meer dan één categorie vallen: Artis valt onder alle drie en staat
    # vooraan in de lijst, dus `projecten_in(cat, 1)` gaf hem drie keer terug en
    # stond hij drie keer op de homepage. Daarom per categorie doorzoeken tot er
    # een project is dat er nog niet bij staat.
    gekozen = []
    gebruikt = set()
    for cat in UITGELICHT:
        for kandidaat in D.projecten_in(cat):
            if kandidaat['bestand'] in gebruikt:
                continue
            gekozen.append((cat, kandidaat))
            gebruikt.add(kandidaat['bestand'])
            break
    gekozen = gekozen[:maximaal]
    # De categorie die erbij staat is die waarvoor het project gekozen is, en
    # niet zijn eerste categorie: een project dat hier de Verbouwing vult moet
    # niet "Nieuwbouw" als label krijgen.
    for i, (cat, p) in enumerate(gekozen):
        meta = "".join(f'<span class="cases-grid__meta-item">{m}</span>'
                       for m in [cat] + ([p['plaats']] if p['plaats'] else []))
        rijen.append(f'''      <a class="cases-grid__row {'cases-grid__row--grey' if i % 2 == 0 else 'cases-grid__row--white'} hover--icon"
         href="{p['bestand']}" aria-label="{_plat(p['titel'])}">
        <div class="cases-grid__body">
          <div class="cases-grid__meta">{meta}</div>
          <h3 class="cases-grid__title">{D._tekens(p['titel'])}</h3>
          <div class="cases-grid__wrapper">
            <p class="cases-grid__text">{D._tekens(C.project_lead(p['slug']) or '')}</p>
            {icoonknop("button--icon--54", "button--secundair")}
          </div>
        </div>
        <figure class="cases-grid__image">
          {foto(p['beeld'], maten="(max-width: 991px) 100vw, 50vw")}
        </figure>
      </a>''')
    return "\n".join(rijen)


def _stappen():
    """De vijf stappen uit inhoud_dienst_verhaal, in het trap-component van het
       template. Alleen de titel en de eerste zin: de volledige uitleg staat op
       werkwijze.html en hoeft hier niet twee keer."""
    regels = []
    for i, (titel, tekst, _detail) in enumerate(V.STAPPEN_STAALFRAME):
        eerste = re.split(r'(?<=[.!?])\s', tekst.strip())[0]
        regels.append(f'''        <li class="trede" style="--trede:{i}">
          <span class="trede__nummer">{i + 1:02d}</span>
          <div class="trede__inhoud">
            <h3 class="trede__titel">{D._tekens(titel)}</h3>
            <p class="trede__tekst">{D._tekens(eerste)}</p>
          </div>
        </li>''')
    return "\n".join(regels)


# Alle diensten op de homepage: de drie hoofddiensten als brede kaart, en de
# vier losse diensten daaronder in een rij van vier. De werkzaamheden die onder
# een hoofddienst hangen staan op die hoofddienstpagina zelf.
hoofddiensten = "\n".join(dienstkaart(i, d, '') for i, d in enumerate(SERVICES))
losse_diensten = "\n".join(dienstkaart(i, d, '', kolom="col-lg-6")
                           for i, d in enumerate(LOSSE_DIENSTEN))

inhoud = f'''  <!-- ================= 01 INTRODUCTIE =================
       De film ligt over het stilstaande beeld heen en komt pas in beeld als hij
       speelt. site.js hangt de bron er pas in als beweging aan staat en de lijn
       het aankan; zonder JavaScript, met prefers-reduced-motion of op een trage
       verbinding blijft het bij de foto hieronder, en dat is het eerste beeldje
       van dezelfde film. Het audiospoor is eruit gehaald: de film staat muted
       en loopt rond, dus geluid is alleen gewicht.

       De film is teruggebracht in helderheid voordat hij hier kwam te staan;
       zonder dat haalde de witte kop erover 2,19:1 waar 3:1 nodig is. Waarom
       dat in de film zit en niet in de sluier: zie de meting bij .hero--sluier
       in index.css. -->
  <section class="hero" id="s01-introductie" data-header-theme="light">
    <div class="hero--beeld" aria-hidden="true">
      {foto("sfh-hero", laden="eager", maten="100vw", alt="")}
      <video class="hero--video" data-herovideo="assets/video/sfh-hero.mp4"
             width="1280" height="720" muted loop playsinline preload="none"></video>
      <span class="hero--sluier"></span>
    </div>
    <div class="container hero--container">
      <div class="hero--content">
        <span class="subtitle" style="color:var(--color-white)">{C.HOME['eyebrow']}</span>
        <h1 class="hero--title">{D.afbreek(C.HOME['h1'])}</h1>
        <div class="hero--intro article-body">
{_p(C.HOME['lead'])}
        </div>
        <div class="hero--actions">
          {knop(*C.HOME['cta_primair'])}
          {knop(*C.HOME['cta_secundair'], "secondary")}
        </div>
      </div>
    </div>
  </section>

{logoslider("02")}

  <!-- ================= 03 WAAROM EEN STALEN FRAME ================= -->
  <section class="content-text-side-cta" id="s03-wat-we-doen">
    <div class="container">
      <div class="content-text-side-cta--container background--grey">
        <div class="row gx-0">
          <div class="col-lg-8 col-12">
            <h2 class="section-heading" style="margin-bottom:var(--space-500)">{C.HOME['statement_kop']}</h2>
            <div class="content-text-side-cta--body article-body">
{_p(C.HOME['statement'])}
            </div>
          </div>
          <div class="col-lg-4 col-12 statement__actie">
            {knop(*C.HOME['statement_cta'])}
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ================= 04 WERKWIJZE =================
       De vijf stappen staan op /werkwijze/ van de bronsite. Hier staan ze kort,
       met een knop naar de volledige uitleg. -->
  <section class="band background--grey" id="s04-werkwijze">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-12">
          <span class="subtitle" style="margin-bottom:var(--space-500)">Werkwijze</span>
          <h2 class="section-heading">{C.HOME['werkwijze_kop']}</h2>
          <p class="article-body" style="margin-top:var(--space-500)">{C.HOME['werkwijze_lead']}</p>
          <div style="margin-top:var(--space-600)">
            {knop(*C.HOME['werkwijze_cta'], "secundair")}
          </div>
        </div>
        <div class="col-lg-8 col-12">
          <ol class="trap" role="list">
{_stappen()}
          </ol>
        </div>
      </div>
    </div>
  </section>

  <section class="content-block" id="s05-werkzaamheden">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row g-0">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Werkzaamheden</span>
            <h2 class="section-heading">{C.HOME['werkzaamheden_kop']}</h2>
            <p class="article-body" style="margin-top:var(--space-500); max-width:var(--content-max-half)">
              {C.HOME['werkzaamheden_lead']}
            </p>
          </div>
        </div>
      </div>
      <div class="row g-0">
{hoofddiensten}
      </div>
      <div class="content-block--container background--white"
           style="padding-top:var(--space-700); padding-bottom:var(--space-600)">
        <div class="row g-0">
          <div class="col-md-8 col-12">
            <h3 class="font-size--md">{C.HOME['losse_kop']}</h3>
            <p class="article-body" style="margin-top:var(--space-400); max-width:var(--content-max-half)">
              {C.HOME['losse_lead']}
            </p>
          </div>
        </div>
      </div>
      <div class="row g-0">
{losse_diensten}
      </div>
    </div>
  </section>

  <!-- ================= 05 PROJECTEN ================= -->
  <section class="cases-grid" id="s06-projecten">
    <div class="container">
      <div class="cases-grid__header">
        <h2 class="cases-grid__heading">{C.HOME['projecten_kop']}</h2>
        {knop(*C.HOME['projecten_cta'], "secundair")}
      </div>
      <div class="cases-grid__list">
{_projectrijen()}
      </div>
    </div>
  </section>

  <!-- ================= 07 OVER ONS =================
       Het beeld staat op zijn eigen verhouding over de inhoudsbreedte, niet in
       een vak met een vaste hoogte, zodat er niemand wordt afgesneden. Er is
       geen teamfoto van dit bedrijf; wat er staat is een foto van eigen
       monteurs aan het werk, en dat is precies waar de tekst over gaat.

       Het beeld wordt gesneden en niet op zijn eigen verhouding gezet. De
       template gebruikte .beeldband omdat daar een groepsfoto stond waarop
       niemand mocht afvallen; deze foto is 4:3 en zou over de volle
       inhoudsbreedte 990px hoog worden. -->
  <section class="content-block" id="s07-over-ons">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row g-0">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Over ons</span>
            <h2 class="section-heading">{C.HOME['over_kop']}</h2>
            <div class="article-body" style="margin-top:var(--space-500); max-width:var(--content-max-half)">
{_p(C.HOME['over'])}
            </div>
            <div style="margin-top:var(--space-600)">
              {knop(*C.HOME['over_cta'], "secundair")}
            </div>
          </div>
        </div>
      </div>
      <figure class="case-bleed" style="margin-top:var(--space-700)">
        {foto("sfh-over-ons", maten="(max-width: 1352px) calc(100vw - 32px), 1320px")}
      </figure>
    </div>
  </section>

{ctablok("08", C.HOME['slot_kop'], C.HOME['slot'])}
'''

(UIT / 'index.html').write_text(pagina(
    bestand='index.html',
    titel=C.seo_titel('index.html'),
    omschrijving=C.SEO['index.html'][1],
    namespace='home',
    pagina_css='index.css',
    css_naam='index',
    inhoud=inhoud,
    scripts=('index.js',),
    extra_ld=json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": D.NAAM,
        "url": BASIS + "/",
        "inLanguage": "nl-NL",
    }, ensure_ascii=False, indent=2),
), encoding='utf-8')
print('index.html geschreven')
