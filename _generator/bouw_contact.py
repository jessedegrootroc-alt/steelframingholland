# -*- coding: utf-8 -*-
"""Contact, prijsopgave, privacybeleid en cookies.

De bronsite heeft één formulier (Contact Form 7) met vier velden: naam, e-mail,
onderwerp en bericht. Een offertepagina heeft de bronsite niet. Die is hier wel
gemaakt, want een bezoeker met een concreet bouwplan heeft een andere vraag dan
iemand die zich oriënteert, en het formuliercomponent van dit template kan het
onderscheid maken: op de opgavepagina staat het extra veld projectadres.

Let op: het formulier verstuurt nog niets. ENDPOINT in contactformulier.js is
leeg. Dat gold al voor het template en is met deze ombouw niet veranderd; het
staat in CONTENT-TODO.md.

Privacybeleid en cookies horen bij de cookiemelding van het template, die naar
beide pagina's linkt. De bronsite heeft geen van beide, en ook geen AVG-passage
bij zijn formulier. Wat hier staat is dus wat er functioneel gebeurt met een
aanvraag, plus een markering. Er is geen beleid verzonnen; een verzonnen
privacyverklaring is juridisch onjuiste tekst.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from schil import *          # noqa: F401,F403
import inhoud_sfh as D
import inhoud_copy as C

UIT = pathlib.Path(__file__).resolve().parent.parent

# De bronsite heeft geen AVG-passage bij zijn formulier. Deze regel zegt alleen
# wat er functioneel met een aanvraag gebeurt en verwijst voor de rest door; er
# staat geen bewaartermijn, geen grondslag en geen verwerker in, want die zijn
# niet bekend.
AVG = ('Wij gebruiken wat u hier invult om uw aanvraag te behandelen en er contact '
       'met u over op te nemen. Hoe wij verder met persoonsgegevens omgaan, staat in '
       'ons <a href="privacybeleid.html">privacybeleid</a>.')


def _p(alineas):
    return "\n".join(f'              <p>{D._tekens(a)}</p>' for a in alineas)


# ---------------------------------------------------------------------- contact
def contact():
    c = D.CONTACT
    # De gegevens staan onder het formulier in de vlakkenrij van het template:
    # vier vlakken in navy, grijs, wit en indigo, tekst onderin, tot de
    # schermrand. De kleuren lopen vast in die volgorde, dus adres, telefoon,
    # e-mail en KvK krijgen op elke pagina hetzelfde vlak.
    #
    # Het vierde vlak was KvK. Dat nummer staat niet op de bronsite, en een
    # gekleurd vlak met een markering erin leest als een fout. In plaats
    # daarvan staat er de aparte ingang van de werkplaats: dat is een feit dat
    # de bronsite wél geeft (in het bericht over de verhuizing) en het is
    # precies wat een vrachtwagenchauffeur moet weten.
    #
    # De openingstijden staan er niet bij. De bronsite zegt alleen "tijdens
    # kantooruren". Zodra de tijden bekend zijn horen ze in het telefoonvlak,
    # onder het nummer. Zie CONTENT-TODO.md.
    gegevens = [
        ('Adres', f'{D.STRAAT}<br>{D.POSTCODE_PLAATS}'),
        # Het mobiele nummer op een eigen regel, met de naam erboven: staat
        # "de heer Melman: +31 (0)6 22 376 826" op één regel, dan breekt hij in
        # dit smalle vlak middenin het nummer af.
        ('Telefoon', f'<a href="tel:{D.TELEFOON_LINK}">{D.TELEFOON_WEERGAVE}</a><br>'
                     f'{D.CONTACTPERSOON}<br>'
                     f'<a href="tel:{D.MOBIEL_LINK}">{D.MOBIEL_WEERGAVE}</a>'),
        ('E-mail', f'<a href="mailto:{D.EMAIL}">{D.EMAIL}</a>'),
        ('Werkplaats', f'Eigen ingang op<br>{D.WERKPLAATS_INGANG}'),
    ]

    inhoud = f'''{patroonhero("01", "contact", "Contact", C.CONTACT['h1'])}

  <section class="content-block" id="s02-introductie">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row g-0">
          <div class="col-lg-8 col-12">
            <div class="article-body">
{_p(C.CONTACT['lead'])}
            </div>
            <div style="margin-top:var(--space-600)">
              {knop("Vraag een prijsopgave aan", "offerte.html")}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

{contactblok({"nr": "03", "waarde": "overig"}, kop=C.CONTACT['formulier_kop'],
             intro=C.CONTACT['formulier_lead'])}

  <figure class="case-bleed" id="s04-pand">
    {foto("sfh-pand", maten="100vw")}
  </figure>

{vlakkenrij("05", "gegevens", D.NAAM, gegevens, subtitel="Gegevens")}

  <section class="content-block" id="s06-privacy">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Uw gegevens</span>
            <div class="article-body" style="margin-top:var(--space-500)">
{_p([AVG])}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    (UIT / 'contact.html').write_text(pagina(
        bestand='contact.html',
        titel=C.seo_titel('contact.html'),
        omschrijving=C.SEO['contact.html'][1],
        namespace='contact', pagina_css='contact.css', css_naam='contact',
        inhoud=inhoud,
        extra_ld=json.dumps({
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": "Contact",
            "url": BASIS + "/contact.html",
        }, ensure_ascii=False, indent=2),
    ), encoding='utf-8')
    return 'contact.html'


# ---------------------------------------------------------------------- offerte
def offerte():
    # De bronsite heeft geen offertepagina en dus ook geen bronformulier. Wat
    # een bezoeker moet aanleveren staat hieronder; het is geen bronfeit maar
    # een praktische vraag die uit de werkwijze volgt (in de oriëntatiefase
    # wordt op basis van tekeningen en eisen bepaald wat mogelijk is).
    #
    # De grens van 20 MB staat in contactformulier.js (MAX_MB) en wordt daar ook
    # gecontroleerd. Hij staat hier in woorden zodat iemand het weet vóórdat hij
    # vijf bestanden heeft uitgekozen.
    upload = ('Tekeningen kunt u meesturen: vijf bestanden van samen maximaal '
              '20 MB. Is het meer, mail ze dan naar '
              f'<a href="mailto:{D.EMAIL}">{D.EMAIL}</a> met uw naam erbij, dan '
              'leggen wij ze bij uw aanvraag.')

    inhoud = f'''{paginahero("01", "offerte", "Prijsopgave", C.OFFERTE['h1'], "sfh-offerte")}

  <section class="content-text-side-cta" id="s02-introductie">
    <div class="container">
      <div class="content-text-side-cta--container background--grey">
        <div class="row gx-0">
          <div class="col-lg-8 col-12">
            <div class="content-text-side-cta--body article-body">
{_p(C.OFFERTE['lead'])}
              <p>Liever bellen? Dat kan ook: <a href="tel:{D.TELEFOON_LINK}">{D.TELEFOON_WEERGAVE}</a>.</p>
            </div>
          </div>
          <div class="col-lg-4 col-12 statement__actie">
            {knop("Onze werkwijze", "werkwijze.html", "secundair")}
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="band background--grey" id="s03-formulier">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-12">
          <span class="subtitle">Prijsopgave</span>
          <h2 class="section-heading" style="margin:var(--space-500) 0">{C.OFFERTE['formulier_kop']}</h2>
          <p class="article-body">{C.OFFERTE['formulier_lead']}</p>
          <p class="article-body" style="margin-top:var(--space-500)">
            Liever bellen? <a href="tel:{D.TELEFOON_LINK}">{D.TELEFOON_WEERGAVE}</a>
          </p>
        </div>
        <div class="col-lg-8 col-12">
          <!-- data-projectadres zet het extra veld aan dat de bronsite hier ook
               vraagt. Bestanden kunnen niet via dit formulier mee: de bron
               verwijst daarvoor naar de mail, en die regel staat eronder. -->
          <div data-contactformulier data-onderwerp="offerte" data-projectadres data-bijlagen></div>
          <noscript>
            <p class="article-body">Het formulier heeft JavaScript nodig. Mail uw aanvraag gerust naar
              <a href="mailto:{D.EMAIL}">{D.EMAIL}</a> of bel {D.TELEFOON_WEERGAVE}.</p>
          </noscript>
          <p class="article-body" style="margin-top:var(--space-600)">{upload}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="content-block" id="s04-aanleveren">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Wat wij nodig hebben</span>
            <h2 class="section-heading">Hoe u een opgave het snelst krijgt</h2>
            <div class="article-body" style="margin-top:var(--space-500)">
              <p>In de ori&euml;ntatiefase bepalen we op grond van uw visie, wensen en
                de geldende eisen en normen welke constructie past. Hoe meer daarvan
                al bekend is, hoe concreter onze opgave kan zijn.</p>
              <ul class="case-lijst" role="list">
                <li>Wat u wilt bouwen, en waar</li>
                <li>Tekeningen of een ontwerp, als u die heeft &mdash; u kunt ze hieronder meesturen</li>
                <li>Of u met een eigen architect werkt</li>
                <li>Of het om nieuwbouw, renovatie of utiliteitsbouw gaat</li>
                <li>Wanneer het gebouw in gebruik moet zijn</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="content-block" id="s05-privacy">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row">
          <div class="col-lg-8 col-12">
            <span class="subtitle" style="margin-bottom:var(--space-500)">Uw gegevens</span>
            <div class="article-body" style="margin-top:var(--space-500)">
{_p([AVG])}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    (UIT / 'offerte.html').write_text(pagina(
        bestand='offerte.html',
        titel=C.seo_titel('offerte.html'),
        omschrijving=C.SEO['offerte.html'][1],
        namespace='offerte', pagina_css='contact.css', css_naam='contact',
        inhoud=inhoud,
    ), encoding='utf-8')
    return 'offerte.html'


# ------------------------------------------------------------- tekstpagina's
def _tekstpagina(bestand, titel, omschrijving, kop, blokken):
    secties = []
    for i, (subkop, alineas) in enumerate(blokken, start=2):
        kopregel = f'            <h2 class="font-size--md" style="margin-bottom:var(--space-400)">{subkop}</h2>\n' if subkop else ''
        secties.append(f'''  <section class="content-block" id="s{i:02d}-blok">
    <div class="container">
      <div class="content-block--container background--white">
        <div class="row">
          <div class="col-lg-8 col-12">
{kopregel}            <div class="article-body">
{_p(alineas)}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>''')
    inhoud = patroonhero('01', 'kop', titel, kop) + "\n\n" + "\n\n".join(secties)
    (UIT / bestand).write_text(pagina(
        bestand=bestand, titel=f'{titel} | {D.NAAM}', omschrijving=omschrijving,
        namespace='tekst', pagina_css='tekstpagina.css', css_naam='tekstpagina',
        inhoud=inhoud,
    ), encoding='utf-8')
    return bestand


def privacybeleid():
    # De bronsite heeft geen privacyverklaring. Wat er wel staat is de AVG-alinea
    # bij de formulieren; die is hier overgenomen. De rest is een markering,
    # want een privacyverklaring verzinnen zou juridisch onjuiste tekst opleveren.
    return _tekstpagina(
        'privacybeleid.html', 'Privacybeleid',
        f'Hoe {D.NAAM} met uw persoonsgegevens omgaat.',
        'Privacybeleid',
        [(None, [AVG]),
         ('Nog aan te leveren',
          [f'{D.NIET_GEVONDEN} De bronsite heeft geen privacyverklaring en ook geen '
           f'AVG-passage bij het formulier. Een volledige verklaring moet door '
           f'{D.NAAM} worden aangeleverd: welke gegevens worden vastgelegd, op welke '
           'grondslag, hoe lang ze worden bewaard, met wie ze worden gedeeld, en hoe '
           'iemand zijn gegevens kan opvragen of laten verwijderen.']),
         ('Contact over uw gegevens',
          [f'Vragen over uw gegevens? Bel {D.TELEFOON_WEERGAVE} of mail naar {D.EMAIL}.'])])


def cookies():
    return _tekstpagina(
        'cookies.html', 'Cookies',
        'Welke cookies deze website plaatst en waarvoor.',
        'Cookies',
        [(None, ['Deze website plaatst alleen cookies die nodig zijn om de site te laten '
                 'werken. Analytische cookies staan uit tot u ze zelf aanzet via de '
                 'cookiemelding; daarin kunt u uw keuze ook weer wijzigen.']),
         ('Nog aan te leveren',
          [f'{D.NIET_GEVONDEN} De bronsite heeft geen cookieverklaring. Zodra bekend is '
           'welk statistiekpakket wordt gebruikt en welke cookies dat plaatst, hoort '
           'die opsomming hier: naam, doel en bewaartermijn per cookie.']),
         ('Contact over cookies',
          [f'Vragen hierover? Bel {D.TELEFOON_WEERGAVE} of mail naar {D.EMAIL}.'])])


def main():
    gemaakt = [contact(), offerte(), privacybeleid(), cookies()]
    print(f'{len(gemaakt)} contact- en tekstpagina\'s geschreven')
    return gemaakt


if __name__ == '__main__':
    main()
