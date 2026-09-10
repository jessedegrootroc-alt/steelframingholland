# -*- coding: utf-8 -*-
"""De dienstpagina's: drie toepassingen en vier techniekpagina's.

Eén skelet voor alle zeven, met de secties die het template daarvoor heeft. De
volgorde volgt wat een bezoeker nodig heeft:

  01 hero               waar ben ik
  02 statement          waar gaat dit over, met de eerste CTA
  03 wanneer            herken ik mijn situatie hierin
  04 uitleg             hoe zit het technisch in elkaar   <- tekst van de bronsite
  05 aanpak             hoe verloopt het traject
  06 oplevering         wat heb ik aan het eind in handen
  07 voordelen          waarom bij ons
  08 projectbewijs      (alleen op een toepassing) wat er in deze categorie staat
  09 vragen             wat mensen meestal nog willen weten
  10 slot               CTA

Sectie 08 is projectbewijs en niet "wat valt hieronder". Deze site heeft geen
diensten onder een dienst: de vier techniekpagina's horen bij alle drie de
toepassingen en hangen dus niet onder één ervan. Op een toepassingspagina is de
vraag die overblijft "kunnen zij mijn soort project aan?", en daar is een rij
echte projecten uit die categorie het antwoord op.

De technische uitleg komt uit `sfh/services.json`. De rest van de tekst staat in
`inhoud_dienst_verhaal.py`; bovenin dat bestand staat wat daarvan uit de bron
komt en wat algemene vakinhoud is.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schil import *          # noqa: F401,F403
from schil import _plat
import inhoud_sfh as D
import inhoud_dienst_verhaal as V
import inhoud_copy as C

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


# ------------------------------------------------------------------ onderdelen
def _situatiekaarten(items):
    return "\n".join(f'''        <div>
          <div class="panel panel--{'grey' if i % 2 == 0 else 'wit'}">
            <span class="panel__meta">Situatie {i + 1:02d}</span>
            <h3 class="panel__title">{_t(titel)}</h3>
            <p class="panel__body">{_t(tekst)}</p>
          </div>
        </div>''' for i, (titel, tekst) in enumerate(items))


def _trap(items):
    return "\n".join(f'''        <li class="trede" style="--trede:{i}">
          <span class="trede__nummer">{i + 1:02d}</span>
          <div class="trede__inhoud">
            <h3 class="trede__titel">{_t(titel)}</h3>
            <p class="trede__tekst">{_t(tekst)}</p>
            {f'<p class="trede__gedrag"><span>Goed om te weten</span> {_t(detail)}</p>' if detail else ''}
          </div>
        </li>''' for i, (titel, tekst, detail) in enumerate(items))


def _icoonpanelen(items):
    return "\n".join(f'''        <div>
          <div class="panel panel--{'grey' if i % 2 == 0 else 'wit'}">
            {icoon(ico)}
            <h3 class="voordeel__titel">{_t(titel)}</h3>
            <p class="panel__body">{_t(tekst)}</p>
          </div>
        </div>''' for i, (ico, titel, tekst) in enumerate(items))


def _lijst(items):
    """Een opsomming uit de bron. Items met een eigen kopje worden panelen."""
    met_kop = [i for i in items if ':' in i[:60]]
    if len(met_kop) == len(items) and 2 <= len(items) <= 6:
        panelen = []
        for i, item in enumerate(items):
            kop, _, rest = item.partition(':')
            panelen.append(f'''        <div>
          <div class="panel panel--{'grey' if i % 2 == 0 else 'wit'}">
            <h3 class="panel__title">{_t(kop.strip())}</h3>
            <p class="panel__body">{_t(rest.strip())}</p>
          </div>
        </div>''')
        kolommen = 3 if len(items) % 3 == 0 or len(items) > 4 else len(items)
        return f'      <div class="panel-row panel-row--{kolommen}">\n' + "\n".join(panelen) + '\n      </div>'
    punten = "\n".join(f'                <li>{_t(i)}</li>' for i in items)
    return '              <ul class="case-lijst" role="list">\n' + punten + '\n              </ul>'


def _uitleg(nr, secties, kop=None, lijst_kop=None):
    """De technische uitleg: kopjes met alinea's en lijsten.

       kop is de H2 boven het blok. Die komt uit de copylaag en zegt waar het
       blok over gaat; zonder kop staat er het neutrale label van het template."""
    blokken, panelen_buiten = [], []
    for sec in secties:
        if not sec['alineas'] and not sec['lijsten']:
            continue
        # let op: niet 'kop' noemen, dat is de parameter van deze functie
        sec_kop = (f'            <h3 class="font-size--md" style="margin-bottom:var(--space-400)">{_t(sec["kop"])}</h3>\n'
                   if sec['kop'] else '')
        tekst = "\n".join(f'              <p>{_t(a)}</p>' for a in D.splits_lang(sec['alineas']))
        binnen, buiten = [], []
        for l in sec['lijsten']:
            (buiten if 'panel-row' in _lijst(l) else binnen).append(_lijst(l))
        blokken.append(sec_kop + '            <div class="article-body">\n' + tekst
                       + ("\n" + "\n".join(binnen) if binnen else '') + '\n            </div>')
        panelen_buiten += buiten
    if not blokken:
        return ''
    return f'''  <section class="content-block" id="s{nr}-uitleg">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Hoe het werkt</span>
{f'            <h2 class="section-heading" style="margin-bottom:var(--space-500)">{_t(kop)}</h2>' + chr(10) if kop else ''}{chr(10).join(blokken)}
          </div>
        </div>
      </div>
{f'      <div class="content-block--container background--white" style="padding-top:var(--space-600)"><div class="row g-0"><div class="col-md-8 col-12"><h3 class="font-size--md">{_t(lijst_kop)}</h3></div></div></div>' + chr(10) if lijst_kop and panelen_buiten else ''}{chr(10).join(panelen_buiten)}
    </div>
  </section>'''


# ------------------------------------------------------------------- de pagina
def dienstpagina(bestand):
    d = D.dienst(bestand)
    v = V.verhaal(bestand, d['groep'])
    nr = [1]

    def volgend():
        nr[0] += 1
        return f'{nr[0]:02d}'

    # Het label boven de H1 is de menugroep waar de pagina in staat, zodat de
    # bezoeker ziet waar hij zit: "Toepassingen" bij woningbouw, renovatie en
    # utiliteitsbouw, "Staalframebouw" bij de vier techniekpagina's.
    label = 'Toepassingen' if d['groep'] == 'toepassing' else 'Staalframebouw'
    delen = [paginahero('01', 'introductie', label, D.afbreek(_t(d['titel'])), d['beeld'])]

    # 02 statement
    # De lead bovenaan komt uit de copylaag, de uitleg eronder ook.
    #
    # Alle zeven pagina's hebben in inhoud_copy.py een `uitleg` die de héle
    # bronpagina herschrijft, niet alleen de openingszin. De bronalinea's worden
    # daarom niet ook nog eens onder die uitleg gezet: dan staat hetzelfde er
    # twee keer, één keer actief en één keer in de lijdende vorm, en eindigt het
    # blok met de wervende slotregel van de bronsite ("tegen een scherpe
    # projectprijs") midden in de body.
    #
    # De brontekst blijft staan waar hij thuishoort: in `sfh/services.json`. Dat
    # is de feitenbasis, niet de webcopy.
    #
    # Heeft een pagina géén eigen uitleg, dan valt hij terug op de brontekst:
    # de eerste twee alinea's als statement, de rest in het uitlegblok.
    herschreven = C.dienst(bestand)
    alle_intro = d['intro'] or [d['seo_omschrijving']]
    eigen_uitleg = herschreven.get('uitleg')
    if herschreven.get('lead'):
        intro = herschreven['lead']
        rest_intro = eigen_uitleg or alle_intro
    else:
        intro = alle_intro[:2]
        rest_intro = alle_intro[2:]
    delen.append(f'''  <section class="content-text-side-cta" id="s{volgend()}-statement">
    <div class="container">
      <div class="content-text-side-cta--container">
        <div class="row gx-0">
          <div class="col-lg-8 col-12">
            <div class="content-text-side-cta--body article-body">
{chr(10).join(f"              <p>{_t(a)}</p>" for a in intro)}
            </div>
          </div>
          <div class="col-lg-4 col-12 statement__actie">
            {knop(*(herschreven.get('cta') or ("Vraag een offerte aan", "offerte.html")))}
          </div>
        </div>
      </div>
    </div>
  </section>''')

    # 03 wanneer is dit iets voor u
    if v.get('situaties'):
        delen.append(f'''  <section class="content-block" id="s{volgend()}-wanneer">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Herkenbaar?</span>
            <h2 class="section-heading">{_t(herschreven.get('wanneer_kop') or v['wanneer_kop'])}</h2>
            <p class="article-body" style="margin-top:var(--space-500); max-width:var(--content-max-half)">{_t(v['wanneer_intro'])}</p>
          </div>
        </div>
      </div>
      <div class="panel-row panel-row--3">
{_situatiekaarten(v['situaties'])}
      </div>
    </div>
  </section>''')

    # 04 de technische uitleg van de bronsite
    # De bronsecties alleen als deze pagina geen eigen uitleg heeft. De
    # opsommingen uit de bron blijven wel altijd staan: die zijn feitelijk en
    # niet te herschrijven zonder ze te verarmen.
    secties = [s for s in d['secties'] if s['lijsten']] if eigen_uitleg else d['secties']
    if rest_intro:
        secties = [{'kop': None, 'alineas': rest_intro, 'lijsten': []}] + secties
    uitleg = _uitleg(volgend(), secties, herschreven.get('uitleg_kop'), herschreven.get('lijst_kop'))
    if uitleg:
        delen.append(uitleg)
    else:
        nr[0] -= 1

    # 05 aanpak
    delen.append(f'''  <section class="band background--grey" id="s{volgend()}-aanpak">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-12">
          <span class="subtitle" style="margin-bottom:var(--space-500)">Aanpak</span>
          <h2 class="section-heading">{_t(v['stappen_kop'])}</h2>
          <p class="article-body" style="margin-top:var(--space-500)">{_t(v['stappen_intro'])}</p>
          <div style="margin-top:var(--space-600)">
            {knop("Onze werkwijze", "werkwijze.html", "secundair")}
          </div>
        </div>
        <div class="col-lg-8 col-12">
          <ol class="trap" role="list">
{_trap(v['stappen'])}
          </ol>
        </div>
      </div>
    </div>
  </section>''')

    # 06 wat u van ons krijgt
    delen.append(f'''  <section class="content-block" id="s{volgend()}-oplevering">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Oplevering</span>
            <h2 class="section-heading">{_t(v['oplevering_kop'])}</h2>
          </div>
        </div>
      </div>
      <div class="panel-row panel-row--4">
{_icoonpanelen(v['oplevering'])}
      </div>
    </div>
  </section>''')

    # 07 voordelen
    delen.append(f'''  <section class="content-block" id="s{volgend()}-voordelen">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Waarom wij</span>
            <h2 class="section-heading">{_t(v['voordelen_kop'])}</h2>
          </div>
        </div>
      </div>
      <div class="panel-row panel-row--4">
{_icoonpanelen(v['voordelen'])}
      </div>
    </div>
  </section>''')

    # 08 projectbewijs: de projecten in deze categorie
    #
    # Alleen op een toepassingspagina, want alleen daar is er een categorie om
    # op te filteren. De naam van de toepassing is ook de naam van de
    # projectcategorie ("Woningbouw", "Renovatie", "Utiliteitsbouw"), dus de
    # koppeling is de titel zelf.
    if d['is_hoofddienst']:
        bewijs = D.projecten_in(d['titel'], 4)
        if bewijs:
            kaarten = "\n".join(
                beeldkaart(_t(pr['titel']),
                           _t(', '.join(x for x in (pr['plaats'], pr['datum']) if x))
                           or 'Zie het project',
                           pr['beeld'], href=pr['bestand'])
                for pr in bewijs[:2])
            rest = bewijs[2:4]
            rij2 = "\n".join(
                beeldkaart(_t(pr['titel']),
                           _t(', '.join(x for x in (pr['plaats'], pr['datum']) if x))
                           or 'Zie het project',
                           pr['beeld'], kleur='white', href=pr['bestand'])
                for pr in rest)
            delen.append(f'''  <section class="content-block" id="s{volgend()}-projectbewijs">
    <div class="container">
      <div class="content-block--container background--white" style="padding-bottom:var(--space-700)">
        <div class="row">
          <div class="col-md-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Projectbewijs</span>
            <h2 class="section-heading">Wat wij in {D.afbreek(_t(d["titel"].lower()))} hebben gebouwd</h2>
            <p class="article-body" style="margin-top:var(--space-500); max-width:var(--content-max-half)">
              Onder deze noemer staan {len(D.projecten_in(d['titel']))} projecten. Hieronder een paar; de rest staat op het projectenoverzicht.
            </p>
          </div>
        </div>
      </div>
      <div class="row g-0">
{kaarten}
{rij2}
      </div>
      <div class="content-block--container background--white" style="padding-top:var(--space-600)">
        {knop("Alle projecten", "projecten.html", "secundair")}
      </div>
    </div>
  </section>''')

    # 09 vragen: die van de bronsite eerst, dan de rest
    faq_items = [(vr, [_t(a) for a in D.splits_lang(aw)]) for vr, aw in d['faq']]
    for vr, aw in v.get('faq', []):
        if not any(vr == bestaande for bestaande, _ in faq_items):
            faq_items.append((vr, [_t(a) for a in D.splits_lang([aw])]))
    faq_ld_blok = None
    if faq_items:
        delen.append(faq_blok(volgend(), faq_items, 'Wat mensen meestal nog vragen'))
        faq_ld_blok = faq_ld(faq_items)

    # 10 slot
    delen.append(logoslider(volgend()))
    delen.append(ctablok(volgend(), 'Overleg over uw project',
                         _t(d['cta']) if d['cta'] else None))

    # De bronsite heeft geen meta descriptions en als title overal alleen
    # "<Paginanaam> |  Steel Framing Holland". Titel en omschrijving komen dus
    # uit de copylaag; de terugval is de eerste zin van de lead.
    seo_titel, seo_omschrijving = C.seo(
        bestand, f"{d['titel']} | {D.NAAM}", _t(intro[0])[:155])
    titel = C.seo_titel(bestand) if bestand in C.SEO else f"{d['titel']} | {D.NAAM}"
    omschrijving = seo_omschrijving

    extra = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": d['titel'],
        "name": d['titel'],
        "description": _plat(seo_omschrijving),
        "areaServed": "NL",
        "provider": {"@type": "Organization", "name": D.NAAM_VOLUIT},
    }, ensure_ascii=False, indent=2)
    if faq_ld_blok:
        extra += "\n</script>\n<script type=\"application/ld+json\">\n" + faq_ld_blok

    (UIT / bestand).write_text(pagina(
        bestand=bestand, titel=titel, omschrijving=omschrijving,
        namespace='dienst', pagina_css='service.css', css_naam='service',
        inhoud="\n\n".join(delen), extra_ld=extra,
    ), encoding='utf-8')
    return bestand


def main():
    gemaakt = [dienstpagina(b) for b, _, _, _ in D.HOOFDDIENSTEN]
    gemaakt += [dienstpagina(b) for b, _, _, _, _ in D.DIENSTEN]
    print(f"{len(gemaakt)} dienstpagina's geschreven")
    return gemaakt


if __name__ == '__main__':
    main()
