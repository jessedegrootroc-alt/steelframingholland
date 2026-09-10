# -*- coding: utf-8 -*-
"""De verhaallaag onder de dienstpagina's.

De bronsite legt per pagina goed uit *wat* iets technisch is, maar niet wat een
opdrachtgever ermee moet: wanneer je hiervoor aanklopt, hoe het traject loopt,
wat je aan het eind in handen hebt en wat er van jou wordt verwacht. Dat deel
staat hier, in de secties die het template daarvoor heeft.

WAT HIER UIT DE BRON KOMT
  - De vijf processtappen. De pagina /werkwijze/ van de bronsite beschrijft die
    stappen zelf: oriëntatiefase, plan van aanpak door de ontwerp-, teken- en
    berekendivisie, fabricage op maat, aansturing door de projectleider vanuit
    het draaiboek, en een oplevering waarbij het werk wordt nagelopen.
  - De bewerkingen die op een profiel kunnen: die staan als opsomming op
    dezelfde pagina en komen ongewijzigd door de generator heen.
  - De voordelen. Eigen engineers, eigen productiefaciliteit, eigen wagenpark,
    vast team monteurs, C100 in eigen beheer, grotere C-profielen via partners,
    stapelen tot zes verdiepingen zonder hulpconstructie, combineren met
    warmgewalst staal: alles uit /about-us/, /werkwijze/, /utiliteitsbouw/ en
    /lichtgewicht-staalframe/.
  - De landen bij "werken jullie ook buiten Nederland": die volgen uit het
    portfolio zelf (Bonaire, Haïti, Irak, Verenigd Koninkrijk, Ibiza, Azoren).

WAT HIER ALGEMENE VAKINHOUD IS
  Dat koudgevormd staal maatvast is en dus niet werkt door vocht, dat een
  lichte constructie bij optoppen de extra belasting op gebouw en fundering
  beperkt, en dat naoorlogse portiekflats zich daar goed voor lenen omdat ze
  onderling gelijk van maat zijn en een plat dak hebben. Dat zijn eigenschappen
  van de bouwmethode, niet van dit bedrijf. Bron: Bouwen met Staal over
  staalframebouw en de gangbare vakliteratuur over optoppen.

WAT HIER BEWUST NIET STAAT
  Geen doorlooptijden, tarieven, besparingspercentages, certificaten,
  klantnamen, aantallen of garanties. Dat zijn uitspraken over dít bedrijf en
  die kan alleen Steel Framing Holland doen. Waar zo'n getal het verhaal zou
  helpen, staat een formulering die klopt zonder te beloven.

Een pagina zonder eigen regel hieronder valt terug op de groep waar hij bij
hoort (GROEP_STANDAARD). Zo blijft een nieuwe pagina één regel werk.
"""

# ---------------------------------------------------------------------------
#  De processtappen: de werkwijze van de bronsite, in vijf stappen
# ---------------------------------------------------------------------------
STAPPEN_STAALFRAME = [
    ("Oriëntatie op de mogelijkheden",
     "We gaan eerst in op wat u wilt bouwen. Aan de hand van uw visie, wensen en "
     "de wettelijke eisen en normen brengen we in kaart welke constructie&shy;"
     "mogelijkheden er zijn.",
     "Heeft u al tekeningen of een architect, dan starten we daar; anders beginnen we bij het idee."),
    ("Ontwerp, tekening en berekening",
     "Is de best passende oplossing gekozen, dan maakt onze ontwerp-, teken- en "
     "berekendivisie het plan van aanpak. Daarin staat hoe het frame eruitziet en "
     "waarom het zo is gerekend.",
     "Wij zorgen dat de uiteindelijke constructie aan alle geldende normen en eisen voldoet."),
    ("Fabricage op maat",
     "De profielen worden in onze eigen productiefaciliteit gebogen, gestanst en "
     "gesneden. De C100-profielen maken we zelf; grotere C-profielen komen van onze "
     "partners.",
     "De bewerkingen op het profiel zitten er al in, dus op de bouwplaats hoeft er niets bij."),
    ("Transport en montage",
     "Het frame gaat als bouwpakket naar de locatie, of we monteren het voor in onze "
     "werkplaats en vervoeren het met ons eigen wagenpark. Ter plaatse takelen we het "
     "omhoog, bevestigen het aan de fundering en monteren af.",
     "Vanuit het draaiboek stuurt onze projectleider de fabricage en de montage aan."),
    ("Oplevering",
     "Bij de oplevering lopen we het geleverde werk met u na en stellen we in overleg "
     "vast of alle afspraken zijn nagekomen.",
     "Tijdens het hele traject is de projectleider uw aanspreekpunt en houdt hij de planning bij."),
]


# ---------------------------------------------------------------------------
#  Wat u van ons krijgt
# ---------------------------------------------------------------------------
OPLEVERING_STAALFRAME = [
    ("document", "Ontwerp, tekeningen en berekeningen",
     "De constructieve uitwerking van uw project, opgezet zodat de uiteindelijke "
     "constructie aan de geldende normen en eisen voldoet."),
    ("lijst", "Profielen met de bewerkingen erin",
     "Uitsparingen, gaten voor kabels en leidingen, bevestigingsgaten en "
     "eindafwerkingen zitten al in het profiel, met de specificaties erop geprint."),
    ("trap", "Het frame zoals u het wilt hebben",
     "Als bouwpakket op locatie, door ons gemonteerd op de bouwplaats, of "
     "voorgemonteerd in onze werkplaats en in delen aangevoerd."),
    ("vinkje", "Een oplevering die u samen met ons nagaat",
     "We lopen het geleverde werk met u na en stellen in overleg vast of alle "
     "afspraken zijn nagekomen."),
]


# ---------------------------------------------------------------------------
#  Waarom Steel Framing Holland
# ---------------------------------------------------------------------------
VOORDELEN_KETEN = [
    ("mensen", "Zes stappen, één partij",
     "Ontwerpen, tekenen, berekenen, fabriceren, transporteren en monteren doen wij "
     "zelf. U hoeft niet te schakelen tussen een tekenbureau, een staalleverancier en "
     "een montageploeg."),
    ("grafiek", "Eigen productie, eigen planning",
     "Onze productiefaciliteit buigt, stanst en snijdt de frames non-stop, en de "
     "C100-profielen maken we in eigen beheer. Wij bepalen dus zelf wanneer uw serie "
     "op de machine ligt."),
    ("schild", "Het systeem begrenst uw ontwerp niet",
     "Een lichtgewicht frame stapelt tot zes verdiepingen zonder hulpconstructie. "
     "Vraagt uw ontwerp meer, dan combineren we het met warmgewalst staal."),
    ("klok", "Eén aanspreekpunt tijdens de uitvoering",
     "Onze projectleider stuurt fabricage, assemblage en montage aan, houdt de "
     "planning bij en onderhoudt het contact met u."),
]


# ---------------------------------------------------------------------------
#  Veelgestelde vragen
# ---------------------------------------------------------------------------
FAQ_EIGEN_ARCHITECT = (
    "Kan ik met mijn eigen architect of ontwerp bij u terecht?",
    "Ja. Levert u een eigen ontwerp aan, dan werken wij onze tekeningen en "
    "berekeningen uit in het verlengde daarvan. Waar nodig treden we in overleg met "
    "de architect, zodat de constructie zijn ontwerp volgt.")

FAQ_VERDIEPINGEN = (
    "Tot hoeveel verdiepingen kan een lichtgewicht staalframe?",
    "Het lichtgewicht stalen frame is stevig genoeg om tot zes verdiepingen door te "
    "stapelen, zonder hulpconstructie. Wilt u hoger bouwen, of vraagt een creatief "
    "ontwerp op een bepaald punt meer stevigheid, dan combineren we het frame met "
    "warmgewalst staal.")

FAQ_MONTAGE = (
    "Wordt het frame op de bouwplaats of in de werkplaats gemonteerd?",
    "Dat kiest u. De staalconstructie kan als bouwpakket op de locatie worden "
    "afgeleverd, en doorgaans verzorgen wij dan ook ter plaatse de montage. Moet het "
    "sneller, dan monteren we het frame voor in onze werkplaats en vervoeren we het "
    "geheel of in delen met ons gespecialiseerde wagenpark. Ter plaatse takelen we de "
    "constructie omhoog, bevestigen hem aan de fundering en monteren af.")

FAQ_NORMEN = (
    "Voldoet de constructie aan de geldende normen?",
    "Ja. Onze tekenaars en calculators werken met moderne reken- en tekensoftware, en "
    "wij zorgen ervoor dat de uiteindelijke constructie voldoet aan alle geldende "
    "normen en eisen.")

FAQ_MAATVAST = (
    "Gaat een stalen frame niet werken, zoals hout?",
    "Nee. Koudgevormd staal is maatvast: het krimpt niet, zet niet uit en vervormt "
    "niet door vocht. Dat is een eigenschap van het materiaal en het is de reden dat "
    "stucwerk op een staalframe niet scheurt en vloeren niet gaan doorzakken.")

FAQ_GEVELAFWERKING = (
    "Ziet een staalframewoning eruit als een systeemwoning?",
    "Van buiten is er niets van het frame te zien. Binnenmuur en buitengevel worden "
    "afgewerkt met bijvoorbeeld pleisterwerk, kunststof, hout of steenstrip, dus het "
    "gebouw ziet uit zoals het is ontworpen.")

FAQ_LEIDINGEN = (
    "Waar gaan de leidingen en de bekabeling?",
    "Alle benodigde bekabeling en leidingwerk kan in de wanden worden weggewerkt. Bij "
    "het EPS wandsysteem gaat dat eenvoudig; ook in de profielen zelf zitten al ronde, "
    "rechthoekige of vierkante gaten voor kabels en leidingen.")

FAQ_BUITENLAND = (
    "Werkt u ook buiten Nederland?",
    "Ja. Naast projecten door heel Nederland hebben wij gebouwd op Bonaire, in Haïti, "
    "in Irak, in het Verenigd Koninkrijk, op Ibiza en op de Azoren. Voor een locatie "
    "op afstand is voormontage in onze werkplaats vaak de praktische route.")

FAQ_OPLEVERING = (
    "Hoe weet ik of alles is gedaan wat is afgesproken?",
    "Bij de oplevering lopen we het geleverde werk samen met u na. In overleg stellen "
    "we vast of alle afspraken zijn nagekomen.")

FAQ_OPTOPPEN_BELASTING = (
    "Kan het bestaande gebouw een extra verdieping dragen?",
    "Dat moet per gebouw worden berekend, en dat is precies wat wij in de "
    "oriëntatiefase doen. Het voordeel van een staalframe is dat het licht is: de "
    "extra belasting op de bestaande constructie en de fundering blijft daardoor "
    "beperkt, waardoor er in veel gevallen minder aan het bestaande gebouw hoeft te "
    "worden versterkt dan bij een zwaardere bouwmethode.")


# ---------------------------------------------------------------------------
#  Per groep: waar een pagina niets eigens heeft, geldt dit
# ---------------------------------------------------------------------------
GROEP_STANDAARD = {
    'toepassing': {
        'wanneer_kop': 'Wanneer is dit iets voor uw project?',
        'wanneer_intro': 'Deze drie situaties komen het meest voor.',
        'stappen_kop': 'Van oriëntatie tot oplevering',
        'stappen_intro': 'Elk project doorloopt bij ons dezelfde vijf stappen. Per stap '
                         'weet u wie wat doet en wanneer wij iets van u nodig hebben.',
        'stappen': STAPPEN_STAALFRAME,
        'voordelen_kop': 'Wat u eraan heeft dat wij het zelf doen',
        'voordelen': VOORDELEN_KETEN,
        'oplevering_kop': 'Wat u van ons krijgt',
        'oplevering': OPLEVERING_STAALFRAME,
        'faq': [FAQ_EIGEN_ARCHITECT, FAQ_VERDIEPINGEN, FAQ_MONTAGE,
                FAQ_GEVELAFWERKING, FAQ_MAATVAST, FAQ_OPLEVERING],
    },
    'techniek': {
        'wanneer_kop': 'Wanneer is dit iets voor u?',
        'wanneer_intro': 'Deze drie situaties komen het meest voor.',
        'stappen_kop': 'Van oriëntatie tot oplevering',
        'stappen_intro': 'Elk project doorloopt bij ons dezelfde vijf stappen. Per stap '
                         'weet u wie wat doet en wanneer wij iets van u nodig hebben.',
        'stappen': STAPPEN_STAALFRAME,
        'voordelen_kop': 'Wat u eraan heeft dat wij het zelf doen',
        'voordelen': VOORDELEN_KETEN,
        'oplevering_kop': 'Wat u van ons krijgt',
        'oplevering': OPLEVERING_STAALFRAME,
        'faq': [FAQ_VERDIEPINGEN, FAQ_MONTAGE, FAQ_NORMEN, FAQ_MAATVAST,
                FAQ_LEIDINGEN, FAQ_BUITENLAND],
    },
}


# ---------------------------------------------------------------------------
#  Per pagina: de situaties, en waar nodig eigen vragen of voordelen
# ---------------------------------------------------------------------------
PER_DIENST = {
    # ----------------------------------------------------------- toepassingen
    'woningbouw.html': {
        'wanneer_intro': 'Wij bouwen woningen voor particuliere opdrachtgevers, voor '
                         'ontwikkelaars en voor overheden. De vraag verschilt per type '
                         'opdrachtgever; het frame eronder niet.',
        'situaties': [
            ("U laat een eigen woning bouwen",
             "Een vrijstaande woning of villa, ontworpen zoals u hem wilt. Grote "
             "overspanningen geven een vrije indeling, en u kunt werken met een vast "
             "team waarin architect, constructeur en adviseur zitten."),
            ("U ontwikkelt seriematige woningbouw",
             "Zodra dezelfde woning meerdere keren terugkomt, gaat het om herhaling in "
             "de fabriek. De profielen liggen op maat klaar, dus de montage op de "
             "bouwplaats is elke keer hetzelfde werk."),
            ("U bouwt als corporatie of overheid",
             "Een geleid traject van eerste contact tot oplevering, met een "
             "gegarandeerde kostprijs. Dat maakt de aanbesteding en de "
             "begrotingsverantwoording eenvoudiger."),
        ],
        'faq': [
            ("Kan ik de woning later opnieuw indelen?",
             "Ja, en dat is een van de redenen om voor een stalen draagconstructie te "
             "kiezen. Doordat het frame grote overspanningen maakt, zijn er weinig "
             "dragende binnenwanden. Een andere indeling raakt dan de constructie niet."),
            ("Wat betekent een gegarandeerde kostprijs?",
             "Het geleide proces van contact tot oplevering, waarbij ontwerp, "
             "fabricage en montage in één hand zitten, maakt dat de kostprijs vooraf "
             "vaststaat. Wat die prijs voor uw woning is, hangt af van het ontwerp; dat "
             "rekenen we in de oriëntatiefase uit."),
            FAQ_EIGEN_ARCHITECT, FAQ_GEVELAFWERKING, FAQ_MAATVAST, FAQ_LEIDINGEN,
            FAQ_MONTAGE, FAQ_OPLEVERING,
        ],
    },
    'renovatie.html': {
        'wanneer_intro': 'Bij een bestaand gebouw is de vraag niet wat mooi is, maar wat '
                         'het gebouw aankan. Deze drie opgaven komen het meest voor.',
        'situaties': [
            ("U wilt optoppen",
             "Eén of meer extra verdiepingen boven op een bestaand gebouw. VvE&rsquo;s, "
             "woningbouwverenigingen en vastgoedmaatschappijen zetten staalframebouw "
             "hier regelmatig voor in, juist omdat het licht is."),
            ("De gevel moet eraf",
             "Een bestaande gevel vervangen door prefab gevelelementen. Die worden op "
             "maat gemaakt en in delen aangevoerd, dus de bewoners kijken niet weken "
             "tegen een open gebouw aan."),
            ("Er komt een gebouwdeel bij",
             "Een aanbouw, een vleugel of een herbestemming waarbij de bestaande "
             "constructie niet zwaarder mag worden belast."),
        ],
        'voordelen_kop': 'Wat een licht frame bij renovatie oplevert',
        'voordelen': [
            ("schild", "Minder belasting op wat er al staat",
             "Een lichte constructie houdt de extra belasting op het bestaande gebouw "
             "en de fundering beperkt. Er hoeft daardoor in veel gevallen minder te "
             "worden versterkt dan bij een zwaardere bouwmethode."),
            ("klok", "Kort op de bouwplaats",
             "De elementen worden in de fabriek op maat gemaakt en gaan snel in elkaar. "
             "Dat scheelt bouwtijd en houdt de overlast voor bewoners en omwonenden kort."),
            ("mensen", "Zes stappen, één partij",
             "Ontwerpen, tekenen, berekenen, fabriceren, transporteren en monteren doen "
             "wij zelf, met eigen engineers, eigen productie en een vast team monteurs."),
            ("trap", "Herhaalbaar over meerdere blokken",
             "Werkt een oplossing op het eerste gebouw, dan is die op een volgend blok "
             "van dezelfde opzet opnieuw in te zetten."),
        ],
        'faq': [
            FAQ_OPTOPPEN_BELASTING,
            ("Kunnen bewoners in het gebouw blijven tijdens de bouw?",
             "Dat hangt van het project af en bepaalt u samen met uw aannemer en "
             "bewoners. Wat staalframebouw hieraan bijdraagt, is dat de elementen in de "
             "fabriek worden gemaakt en op de bouwplaats alleen nog in elkaar gaan. De "
             "periode waarin er echt aan het gebouw wordt gewerkt, is daardoor korter."),
            FAQ_VERDIEPINGEN, FAQ_GEVELAFWERKING, FAQ_MONTAGE, FAQ_OPLEVERING,
        ],
    },
    'utiliteitsbouw.html': {
        'wanneer_intro': 'In de utiliteit gaat het bijna altijd om een gebouw dat op een '
                         'datum in gebruik moet zijn. Deze drie opgaven komen het meest voor.',
        'situaties': [
            ("U bouwt bedrijfsruimte of kantoor",
             "Bedrijfsunits, kantoren en hallen. Sneller en flexibeler dan conventioneel "
             "bouwen, en doorgaans goedkoper, met een constructie die aansluit bij de "
             "huidige normen voor energie en duurzaamheid."),
            ("U bouwt een school of maatschappelijk gebouw",
             "Een gebouw dat vaak binnen een schooljaar of een boekjaar klaar moet zijn, "
             "waarbij de opleverdatum harder is dan het budget."),
            ("Het ontwerp vraagt meer dan een standaardsysteem",
             "Grote overspanningen, verspringende volumes of meer dan zes lagen. Daar "
             "combineren we het lichtgewicht frame met warmgewalst staal."),
        ],
        'faq': [
            ("Wat gebeurt er als de staallevering uitloopt?",
             "Dat risico beperken we door de profielen zelf te produceren: onze eigen "
             "productiefaciliteit bepaalt wanneer uw serie op de machine ligt. Grotere "
             "C-profielen komen van onze partners. Omdat de fabricage en de montage "
             "vanuit hetzelfde draaiboek worden aangestuurd, ziet onze projectleider een "
             "verschuiving in de planning meteen."),
            FAQ_VERDIEPINGEN, FAQ_NORMEN, FAQ_EIGEN_ARCHITECT, FAQ_MONTAGE,
            FAQ_MAATVAST, FAQ_OPLEVERING,
        ],
    },

    # --------------------------------------------------------------- techniek
    'ontwerpen-tekenen-en-berekenen.html': {
        'wanneer_kop': 'Wanneer u hiermee begint',
        'wanneer_intro': 'Hoe vroeger de constructie op tafel ligt, hoe meer keuze er is. '
                         'Deze drie startpunten zien we het meest.',
        'situaties': [
            ("U heeft een idee, nog geen ontwerp",
             "Dan beginnen we bij het ruimtelijk-functionele ontwerp. Onze eigen "
             "ontwerp- en engineeringafdeling geeft het gebouw vorm en houdt tegelijk "
             "de functionaliteit in het oog."),
            ("U heeft een architect en een ontwerp",
             "Dan werken wij de tekeningen en berekeningen uit in het verlengde van dat "
             "ontwerp, en overleggen waar nodig met de architect."),
            ("U wilt weten of het in staalframe kan",
             "Een ontwerp dat voor een andere bouwmethode is gemaakt, is vaak wel in "
             "staalframe uit te voeren. Wij rekenen door wat dat betekent voor de "
             "constructie."),
        ],
        'oplevering_kop': 'Wat u van deze fase in handen krijgt',
        'oplevering': [
            ("document", "Het ruimtelijk-functionele ontwerp",
             "Als u er nog geen heeft: een ontwerp waarin het gebouw esthetisch vorm "
             "krijgt en de functionaliteit is bewaakt."),
            ("lijst", "Tekeningen en berekeningen",
             "Uitgewerkt met moderne reken- en tekensoftware, en zo dat de "
             "uiteindelijke constructie aan alle geldende normen en eisen voldoet."),
            ("grafiek", "Een naar fabricage vertaald ontwerp",
             "De tekeningen gaan direct door naar de fabricage van de "
             "staalframe-elementen, dus wat de fabriek maakt is wat er is gerekend."),
            ("mensen", "Afstemming met uw architect",
             "Waar nodig treden we in overleg met de architect, zodat de constructie "
             "zijn ontwerp volgt in plaats van het te corrigeren."),
        ],
        'faq': [FAQ_EIGEN_ARCHITECT, FAQ_NORMEN, FAQ_VERDIEPINGEN, FAQ_MAATVAST,
                FAQ_BUITENLAND, FAQ_OPLEVERING],
    },
    'lichtgewicht-staalframe.html': {
        'wanneer_kop': 'Wat lichtgewicht staal oplevert',
        'wanneer_intro': 'De eigenschappen van koudgevormd staal pakken in deze drie '
                         'situaties het gunstigst uit.',
        'situaties': [
            ("Het casco moet er snel staan",
             "De profielen worden op maat gefabriceerd en gaan op de bouwplaats in "
             "elkaar. Wilt u het nog sneller, dan monteren we het frame voor in onze "
             "werkplaats en takelen het ter plaatse omhoog."),
            ("De locatie is lastig of ligt ver weg",
             "Een voorgemonteerd frame gaat geheel of in delen mee met ons "
             "gespecialiseerde wagenpark. Op locatie is er dan minder werk en minder "
             "materieel nodig."),
            ("Het ontwerp vraagt vrije indeling",
             "Er is veel flexibiliteit mogelijk in vorm en afmeting, en grote "
             "overspanningen betekenen weinig dragende binnenwanden."),
        ],
        'faq': [FAQ_VERDIEPINGEN, FAQ_MONTAGE, FAQ_MAATVAST, FAQ_LEIDINGEN,
                FAQ_GEVELAFWERKING, FAQ_BUITENLAND],
    },
    'eps-wandsysteem.html': {
        'wanneer_kop': 'Wanneer EPS de logische keuze is',
        'wanneer_intro': 'Van de wandsystemen die wij leveren is EPS de voordeligste. In '
                         'deze drie situaties valt de keuze meestal die kant op.',
        'situaties': [
            ("Het budget is bepalend",
             "EPS is prijsvriendelijk, en het lage gewicht maakt het bevestigen "
             "eenvoudig en snel. Dat scheelt niet alleen materiaal maar ook uren op de "
             "bouwplaats."),
            ("De leidingen moeten weggewerkt",
             "Alle bekabeling en leidingwerk kan eenvoudig in de EPS-wanden worden "
             "weggewerkt, dus er hoeft niet achteraf te worden gesleuteld."),
            ("Er zijn eisen aan isolatie en brandveiligheid",
             "EPS-wanden isoleren tegen geluid en warmte, zijn energiebesparend, "
             "brandveilig, sterk en onschadelijk."),
        ],
        'oplevering_kop': 'Wat het EPS wandsysteem u geeft',
        'oplevering': [
            ("schild", "Een wand die isoleert en brandveilig is",
             "Geluids- en warmte-isolerend, energiebesparend, brandveilig, sterk, "
             "onschadelijk en milieuvriendelijk."),
            ("klok", "Snel te bevestigen",
             "Door het geringe gewicht gaat het bevestigen aan het frame eenvoudig en "
             "snel, zonder zwaar materieel voor een binnenwand."),
            ("lijst", "Leidingwerk uit het zicht",
             "Alle benodigde bekabeling en leidingwerk werkt u weg in de EPS-wanden."),
            ("vinkje", "De afwerking die u wilt",
             "Binnenmuur en buitengevel zijn af te werken met bijvoorbeeld pleisterwerk, "
             "kunststof, hout of steenstrip."),
        ],
        'faq': [
            ("Wat is EPS eigenlijk?",
             "EPS staat voor geëxpandeerd polystyreen, in de bouw beter bekend als "
             "piepschuim. Voor een wandsysteem wordt het geleverd als element dat aan "
             "het stalen frame wordt bevestigd en daarna wordt afgewerkt."),
            ("Met wie werkt u samen voor EPS?",
             "Met Veerhuis, die op wereldwijde schaal specialist is in "
             "EPS-bouwwerken. Samen maken wij hiermee villa&rsquo;s, kantoren, "
             "bedrijfsgebouwen, scholen en ziekenhuizen mogelijk."),
            FAQ_GEVELAFWERKING, FAQ_LEIDINGEN, FAQ_MAATVAST, FAQ_MONTAGE,
        ],
    },
    'overige-wandsystemen.html': {
        'wanneer_kop': 'Wanneer u naar een ander wandsysteem kijkt',
        'wanneer_intro': 'EPS past niet op elk project. Deze drie redenen brengen '
                         'opdrachtgevers bij een ander systeem.',
        'situaties': [
            ("Er zijn hogere bouwfysische eisen",
             "Vraagt uw project andere bouwfysische prestaties of hogere statische "
             "belastingen, dan bepalen die de keuze van het bekledingsmateriaal."),
            ("De uitstraling is bepalend",
             "Esthetische eisen wegen soms zwaarder dan de prijs per vierkante meter. "
             "Voor de binnenzijde en de buitengevel zijn er talloze "
             "bekledingsmogelijkheden."),
            ("U wilt prefab wandelementen",
             "Kant-en-klare prefab wandelementen monteren wij in de constructie, zodat "
             "er op de bouwplaats minder hoeft te gebeuren."),
        ],
        'oplevering_kop': 'Wat u van ons krijgt',
        'oplevering': [
            ("document", "Een advies op uw project",
             "Op basis van uw gegevens praten we u bij over de voor- en nadelen van de "
             "verschillende materialen, en komen we met een op maat gesneden advies."),
            ("lijst", "De keuze uit de materialen",
             "Houten, gipsen, kunststof en aluminium beplating, al dan niet opgevuld met "
             "isolatiemateriaal."),
            ("trap", "Prefab wandelementen, gemonteerd",
             "Kant-en-klare wandelementen die wij in de constructie voor u monteren."),
            ("vinkje", "Een gevel naar keuze",
             "Voor de buitengevel zijn eveneens talloze bekledingsmogelijkheden."),
        ],
        'faq': [
            ("Waarop baseert u het advies over het wandsysteem?",
             "Op isolatienormen, (brand)veiligheidsnormen, esthetische normen en uw "
             "eigen eisen en wensen. Die vier bepalen samen welk materiaal aan de "
             "binnenzijde en aan de gevel het meest logisch is."),
            ("Kan de bekleding later worden nabehandeld?",
             "Ja. De bekledingsmaterialen aan de binnenzijde van de stalen constructie "
             "kunnen op elke denkbare wijze worden nabehandeld."),
            FAQ_GEVELAFWERKING, FAQ_MAATVAST, FAQ_MONTAGE, FAQ_NORMEN,
        ],
    },
}


def verhaal(bestand, groep):
    """De verhaalvelden voor één dienstpagina: eigen invulling waar die er is,
       anders die van de groep."""
    basis = dict(GROEP_STANDAARD.get(groep, GROEP_STANDAARD['techniek']))
    basis.update(PER_DIENST.get(bestand, {}))
    return basis
