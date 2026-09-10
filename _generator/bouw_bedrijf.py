# -*- coding: utf-8 -*-
"""Over ons, werkwijze en partners.

Drie pagina's. Het template had er zes: naast deze drie ook historie, het team,
de registerconstructeur en vacatures.

WAAROM DIE DRIE ZIJN VERVALLEN
  De bronsite van Steel Framing Holland noemt geen oprichtingsjaar en geen
  geschiedenis, geen enkele medewerker of teamgrootte, geen functie of
  registratie van een constructeur, en geen vacatures. Die pagina's zouden dus
  volledig verzonnen moeten worden, en dat mag niet: het zijn precies de
  beweringen over een bedrijf die alleen het bedrijf zelf kan doen.

  Zodra Steel Framing Holland die gegevens aanlevert, zijn de pagina's terug te
  zetten; de bouwfuncties ervoor staan in de git-historie van dit bestand en de
  CSS ervoor is niet aangeraakt. Zie CONTENT-TODO.md.

WAT ERBIJ IS GEKOMEN
  partners.html. De bronsite laat op zijn homepage zes partners zien, met een
  link naar hun site, en noemt op /about-us/ en /eps-wandsysteem/ waarvoor die
  partners er zijn. Dat is echt bewijs van samenwerking en het stond nergens
  uitgewerkt; nu wel.

De teksten komen uit `sfh/`, de formulering uit `inhoud_copy.py`.
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

ICONEN = {
    "vinkje": '<path d="M9.6 16.2 5.4 12l-1.4 1.4 5.6 5.6L20.4 8.2 19 6.8 9.6 16.2Z"/>',
    "schild": '<path d="M12 2 4 5v6.5c0 4.6 3.2 8.4 8 10.5 4.8-2.1 8-5.9 8-10.5V5l-8-3Zm0 2.2 6 2.2v5.1c0 3.5-2.3 6.5-6 8.3-3.7-1.8-6-4.8-6-8.3V6.4l6-2.2Z"/>',
    "lijst": '<path d="M3 5h4v4H3V5Zm6 1h12v2H9V6ZM3 10h4v4H3v-4Zm6 1h12v2H9v-2ZM3 15h4v4H3v-4Zm6 1h12v2H9v-2Z"/>',
    "trap": '<path d="M3 21v-4h5v-4h5V9h5V5h3v18H3Zm2-2h14V7h-1v4h-5v4H8v4H5v0Z"/>',
    "klok": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16Zm-1 3v6l5 3 1-1.7-4-2.3V7h-2Z"/>',
    "mensen": '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm0-6a2 2 0 1 1 0 4 2 2 0 0 1 0-4Zm7 6a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM2 21v-2c0-2.8 3.1-4 7-4s7 1.2 7 4v2H2Zm2-2h10c0-1.2-1.9-2-5-2s-5 .8-5 2Zm14 2v-2c0-1.2-.4-2.2-1.1-3 3 .3 5.1 1.5 5.1 3v2h-4Z"/>',
    "grafiek": '<path d="M3 21V3h2v16h16v2H3Zm4-4V9h3v8H7Zm5 0V5h3v12h-3Zm5 0v-6h3v6h-3Z"/>',
    "document": '<path d="M6 2h8l6 6v14H6V2Zm2 2v16h10V9h-5V4H8Zm7 .4V7h2.6L15 4.4ZM9 12h8v2H9v-2Zm0 4h8v2H9v-2Z"/>',
}


def icoon(naam):
    return (f'<svg class="voordeel__icoon" width="24" height="24" viewBox="0 0 24 24" '
            f'aria-hidden="true">{ICONEN[naam]}</svg>')


def _t(x):
    return D._tekens(x)


def _p(alineas, klasse=''):
    k = f' class="{klasse}"' if klasse else ''
    return "\n".join(f'              <p{k}>{_t(a)}</p>' for a in D.splits_lang(alineas))


def _tekstsectie(nr, ident, kop, alineas, subtitel=None, achtergrond='white'):
    label = (f'            <span class="subtitle" style="margin-bottom:var(--space-500)">{subtitel}</span>\n'
             if subtitel else '')
    kopregel = f'            <h2 class="section-heading">{_t(kop)}</h2>\n' if kop else ''
    return f'''  <section class="content-block" id="s{nr}-{ident}">
    <div class="container">
      <div class="content-block--container background--{achtergrond}">
        <div class="row g-0">
          <div class="col-lg-8 col-12">
{label}{kopregel}            <div class="article-body" style="margin-top:var(--space-500)">
{_p(alineas)}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>'''


def _icoonpanelen(items):
    return "\n".join(f'''        <div>
          <div class="panel panel--{'grey' if i % 2 == 0 else 'wit'}">
            {icoon(ico)}
            <h3 class="voordeel__titel">{_t(titel)}</h3>
            <p class="panel__body">{_t(tekst)}</p>
          </div>
        </div>''' for i, (ico, titel, tekst) in enumerate(items))


def _trap(items):
    return "\n".join(f'''        <li class="trede" style="--trede:{i}">
          <span class="trede__nummer">{i + 1:02d}</span>
          <div class="trede__inhoud">
            <h3 class="trede__titel">{_t(titel)}</h3>
            <p class="trede__tekst">{_t(tekst)}</p>
            {f'<p class="trede__gedrag"><span>Goed om te weten</span> {_t(detail)}</p>' if detail else ''}
          </div>
        </li>''' for i, (titel, tekst, detail) in enumerate(items))


def _seo(bestand):
    return C.seo_titel(bestand), C.SEO[bestand][1]


# --------------------------------------------------------------------- over ons
# De zes stappen die de bronsite drie keer noemt (home, /about-us/,
# /lichtgewicht-staalframe/): ontwerpen, tekenen, berekenen, fabriceren,
# transporteren, monteren. Dat is de kern van waarom deze partij anders is dan
# een leverancier die één schakel doet, dus staat het hier als rij vlakken.
ZES_STAPPEN = [
    ("Ontwerpen", "Een eigen ontwerp- en engineeringafdeling geeft woningen, kantoren "
                  "en bedrijfspanden vorm."),
    ("Tekenen", "Tekenaars zetten het ontwerp met moderne tekensoftware om naar "
                "maakbare staalframe-elementen."),
    ("Berekenen", "Calculators rekenen de constructie door, zodat die aan alle "
                  "geldende normen en eisen voldoet."),
    ("Fabriceren", "In onze eigen productiefaciliteit worden de profielen gebogen, "
                   "gestanst en gesneden. De C100-profielen maken we zelf."),
    ("Transporteren", "Een gespecialiseerd wagenpark brengt het frame naar de "
                      "locatie, geheel of in delen."),
    ("Monteren", "Een vast team monteurs zet het frame op de bouwplaats in elkaar, "
                 "bevestigt het aan de fundering en monteert af."),
]


def over_ons():
    k = C.BEDRIJF['over-ons.html']
    titel, omschrijving = _seo('over-ons.html')
    delen = [
        paginahero('01', 'over-ons', 'Over ons', _t(k['h1']), 'sfh-over-ons'),
        _tekstsectie('02', 'lead', None, k['lead']),
        vlakkenrij('03', 'zes-stappen', 'De zes stappen die wij zelf doen',
                   [(_t(a), _t(b)) for a, b in ZES_STAPPEN[:4]],
                   subtitel='In eigen huis'),
        vlakkenrij('04', 'zes-stappen-2', 'En de laatste twee',
                   [(_t(a), _t(b)) for a, b in ZES_STAPPEN[4:]]),
        # De brontekst van /about-us/, ongewijzigd, als onderbouwing onder de
        # herschreven lead. Zo blijft zichtbaar wat het bedrijf zelf schrijft.
        _tekstsectie('05', 'bron', 'Waar wij in gespecialiseerd zijn',
                     D.OVER_ONS_BRON, achtergrond='grey'),
    ]
    delen.append(f'''  <section class="content-block" id="s06-voordelen">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Wat u daaraan heeft</span>
            <h2 class="section-heading">Waarom dat voor uw project uitmaakt</h2>
          </div>
        </div>
      </div>
      <div class="panel-row panel-row--4">
{_icoonpanelen(V.VOORDELEN_KETEN)}
      </div>
    </div>
  </section>''')
    delen.append(f'''  <section class="content-block" id="s07-verder">
    <div class="container">
      <div class="row g-0">
{beeldkaart("Werkwijze", "De vijf stappen van uw project, van ori&euml;ntatie tot oplevering.",
            'sfh-werkwijze', alt="", kleur="grey", href="werkwijze.html")}
{beeldkaart("Onze partners", "Met wie wij vast samenwerken, en waarvoor.",
            'sfh-partners', alt="", kleur="white", href="partners.html")}
      </div>
    </div>
  </section>''')
    delen.append(logoslider('08'))
    delen.append(ctablok('09', k['slot_kop'],
                         'Vertel kort wat u wilt bouwen. Wij kijken wat er in '
                         'staalframe mogelijk is.'))

    (UIT / 'over-ons.html').write_text(pagina(
        bestand='over-ons.html', titel=titel, omschrijving=omschrijving,
        namespace='over-ons', pagina_css='over-ons.css', css_naam='over-ons',
        inhoud="\n\n".join(delen),
    ), encoding='utf-8')
    return 'over-ons.html'


# -------------------------------------------------------------------- werkwijze
def werkwijze():
    k = C.BEDRIJF['werkwijze.html']
    titel, omschrijving = _seo('werkwijze.html')
    # De opsomming van bewerkingen die op een profiel kunnen, staat als lijst op
    # /werkwijze/ van de bronsite en komt hier ongewijzigd door.
    bewerkingen = "\n".join(f'                <li>{_t(b)}</li>'
                            for b in D.PROFIELBEWERKINGEN)
    delen = [
        paginahero('01', 'werkwijze', 'Over ons', _t(k['h1']), 'sfh-werkwijze'),
        _tekstsectie('02', 'lead', None, k['lead']),
    ]
    delen.append(f'''  <section class="band background--grey" id="s03-stappen">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-12">
          <span class="subtitle" style="margin-bottom:var(--space-500)">Aanpak</span>
          <h2 class="section-heading">Van ori&euml;ntatie tot oplevering</h2>
          <p class="article-body" style="margin-top:var(--space-500)">Vijf stappen. Per
            stap staat wat wij doen en wat wij op dat moment van u nodig hebben.</p>
          <div style="margin-top:var(--space-600)">
            {knop("Bespreek uw project", "offerte.html")}
          </div>
        </div>
        <div class="col-lg-8 col-12">
          <ol class="trap" role="list">
{_trap(V.STAPPEN_STAALFRAME)}
          </ol>
        </div>
      </div>
    </div>
  </section>''')
    delen.append(f'''  <section class="content-block" id="s04-bewerkingen">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row g-0">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Fabricage</span>
            <h2 class="section-heading">Wat er in het profiel zit voordat het de fabriek uit gaat</h2>
            <div class="article-body" style="margin-top:var(--space-500)">
              <p>De fabricage van onze profielen is maatwerk. Wat er op de bouwplaats
                niet meer hoeft te worden gezaagd, geboord of gepast, kost daar ook geen
                tijd. Onder andere kunnen worden aangebracht:</p>
              <ul class="case-lijst" role="list">
{bewerkingen}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>''')
    delen.append(f'''  <section class="content-block" id="s05-oplevering">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Oplevering</span>
            <h2 class="section-heading">Wat u van ons krijgt</h2>
          </div>
        </div>
      </div>
      <div class="panel-row panel-row--4">
{_icoonpanelen(V.OPLEVERING_STAALFRAME)}
      </div>
    </div>
  </section>''')
    # De brontekst van /werkwijze/, ongewijzigd, als onderbouwing.
    delen.append(_tekstsectie('06', 'bron', 'De werkwijze in onze eigen woorden',
                              D.WERKWIJZE_BRON, achtergrond='grey'))
    faq_items = [(vr, [_t(a) for a in D.splits_lang([aw])])
                 for vr, aw in [V.FAQ_EIGEN_ARCHITECT, V.FAQ_MONTAGE, V.FAQ_NORMEN,
                                V.FAQ_VERDIEPINGEN, V.FAQ_OPLEVERING, V.FAQ_BUITENLAND]]
    delen.append(faq_blok('07', faq_items, 'Wat mensen meestal nog vragen'))
    delen.append(logoslider('08'))
    delen.append(ctablok('09', k['slot_kop'],
                         'Stuur ons de tekeningen, of vertel kort wat u wilt bouwen.'))

    (UIT / 'werkwijze.html').write_text(pagina(
        bestand='werkwijze.html', titel=titel, omschrijving=omschrijving,
        namespace='werkwijze', pagina_css='over-ons.css', css_naam='over-ons',
        inhoud="\n\n".join(delen),
        extra_ld=faq_ld(faq_items),
    ), encoding='utf-8')
    return 'werkwijze.html'


# --------------------------------------------------------------------- partners
def partners():
    k = C.BEDRIJF['partners.html']
    titel, omschrijving = _seo('partners.html')
    kaarten = []
    for i, pr in enumerate(D.PARTNERS):
        link = pr.get('url')
        # De naam is een link naar de site van de partner als de bronsite die
        # legt; bij MM Staal staat op de bronsite geen href, dus hier ook niet.
        naamregel = (f'<a href="{link}" rel="noopener external" target="_blank">{_t(pr["naam"])}</a>'
                     if link else _t(pr['naam']))
        # Bij twee van de zes partners zegt de bronsite niet waarvoor ze er
        # zijn. Dan staat er niets in plaats van een markering: een zichtbare
        # [CONTENT NODIG] tussen vier gevulde kaarten leest als een fout, en de
        # naam en de link zijn op zichzelf al waar. Wat er nog bij moet staat in
        # CONTENT-TODO.md.
        body = (f'<p class="panel__body">{_t(pr["rol"])}</p>' if pr.get('rol')
                else (f'<p class="panel__body"><a href="{link}" rel="noopener external" '
                      f'target="_blank">Bekijk hun website</a></p>' if link else ''))
        kaarten.append(f'''        <div>
          <div class="panel panel--{'grey' if i % 2 == 0 else 'wit'}">
            <span class="panel__meta">Partner</span>
            <h3 class="panel__title">{naamregel}</h3>
            {body}
          </div>
        </div>''')
    delen = [
        paginahero('01', 'partners', 'Over ons', _t(k['h1']), 'sfh-partners'),
        _tekstsectie('02', 'lead', None, k['lead']),
    ]
    delen.append(f'''  <section class="content-block" id="s03-partners">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Partners</span>
            <h2 class="section-heading">Met wie wij vast samenwerken</h2>
          </div>
        </div>
      </div>
      <div class="panel-row panel-row--3">
{chr(10).join(kaarten)}
      </div>
    </div>
  </section>''')
    # Urgent Wonen: een samenwerking die de bronsite zelf beschrijft, met de
    # drie partijen erbij. Alleen wat er staat, zonder er een lopend aanbod van
    # te maken; het bericht is van 2018.
    uw = D.URGENT_WONEN
    delen.append(f'''  <section class="content-block" id="s04-urgent-wonen">
    <div class="container">
      <div class="content-block--container background--grey">
        <div class="row g-0">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Samenwerking</span>
            <h2 class="section-heading">{_t(uw['titel'])}</h2>
            <div class="article-body" style="margin-top:var(--space-500)">
              <p>Voor tijdelijke huisvesting werkten wij samen met
                {_t(' en '.join([', '.join(uw['samenwerking'][:-1]), uw['samenwerking'][-1]]))}
                onder de naam Urgent Wonen: woningen die snel en flexibel te
                realiseren zijn, voor mensen die op korte termijn een plek nodig
                hebben.</p>
              <p>Wilt u weten of dit voor uw opgave nog actueel is, dan vraagt u dat
                het beste rechtstreeks aan ons.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>''')
    delen.append(logoslider('05'))
    delen.append(ctablok('06', k['slot_kop'],
                         'Vertel kort wat u wilt bouwen. Wij kijken wat wij en onze '
                         'partners samen voor u kunnen doen.'))

    (UIT / 'partners.html').write_text(pagina(
        bestand='partners.html', titel=titel, omschrijving=omschrijving,
        namespace='partners', pagina_css='over-ons.css', css_naam='over-ons',
        inhoud="\n\n".join(delen),
    ), encoding='utf-8')
    return 'partners.html'


def main():
    gemaakt = [over_ons(), werkwijze(), partners()]
    print(f'{len(gemaakt)} bedrijfspagina\'s geschreven')
    return gemaakt


if __name__ == '__main__':
    main()
