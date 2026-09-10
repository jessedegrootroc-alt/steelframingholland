# -*- coding: utf-8 -*-
"""Herschreven copy: dezelfde feiten als de bronsite, anders geformuleerd.

De bronteksten in `sfh/` blijven staan zoals ze zijn; dat is de feitenbasis en
de herkomst. Dit bestand zet daar de webcopy tegenover: korter, actiever, met
de reden vooraan en de techniek als onderbouwing erachter.

REGEL BIJ ELKE REGEL HIERONDER
  Elk bedrijfsfeit moet in de bron staan. Geen nieuwe diensten, mogelijkheden,
  certificaten, cijfers, doorlooptijden, garanties of opdrachtgevers.

  Waar hieronder algemene vakinhoud staat over hoe staalframebouw werkt (dat
  koudgevormde profielen dimensioneel stabiel zijn, dat een lichte constructie
  de extra belasting bij optoppen beperkt, dat naoorlogse portiekflats zich
  goed lenen voor optoppen), is dat eigenschap van de bouwmethode en niet een
  bewering over dít bedrijf. Bron: Bouwen met Staal over staalframebouw en de
  gangbare vakliteratuur over optoppen. Zulke uitleg staat nooit in de eerste
  persoon en nooit als belofte.

WAT HIER IS VERANDERD TEN OPZICHTE VAN DE BRON
  - Openingszinnen. De bron begint met de bouwmethode ("Staalframebouw wint
    wereldwijd snel aan populariteit"). Dat is waar, maar het is geen antwoord
    op de vraag van de bezoeker. De openingen hier beginnen bij wat hij eraan
    heeft.
  - Koppen. Kale zelfstandige naamwoorden ("Woningbouw", "Renovatie") blijven
    de H1, omdat dat het woord is waarop mensen zoeken en waarmee het in het
    menu staat. Het voordeel staat direct daaronder en in de eerste H2.
  - Wij-vorm. "Wij beschikken over een eigen productiefaciliteit" is geworden
    wat dat voor de opdrachtgever betekent.
  - Lege formuleringen eruit. De bron gebruikt "totaaloplossing",
    "zorgeloos", "ongekende mogelijkheden" en "vlekkeloos". Het feit
    eronder staat er ook: engineering, fabricage en montage in eigen huis.
    Dat feit is gebleven, de kwalificatie niet.
  - Lengte. Alinea's van tachtig woorden zijn er twee of drie geworden.

WAT DE BRON NIET GEEFT EN HIER DUS NIET STAAT
  Geen oprichtingsjaar, teamgrootte, aantal projecten per jaar, levertijden,
  prijzen, besparingspercentages, certificeringen of klantcitaten. Dat zijn
  uitspraken over dít bedrijf en die kan alleen Steel Framing Holland doen.
  Zie CONTENT-TODO.md.
"""

# ---------------------------------------------------------------------------
#  Homepage
# ---------------------------------------------------------------------------
# De bron had als hero-kop "Vooruit met staalframebouw". Als merkregel kan die,
# als H1 niet: je leest er niet in wat het bedrijf doet, voor wie, of wat je
# eraan hebt. De H1 hieronder noemt de bouwmethode en de drie markten die de
# bronsite zelf als menu-indeling gebruikt, zodat de bezoeker in één regel ziet
# of hij op de goede site is.
#
# De propositie in de lead is de enige die deze bronsite feitelijk onderbouwt en
# die concurrenten in staalframebouw meestal niet hebben: engineering,
# productie, transport én montage met eigen mensen. Dat staat drie keer in de
# bron (home, over ons, utiliteitsbouw).
HOME = {
    'eyebrow': 'Specialist in staalframebouw',
    'h1': 'Staalframebouw voor woningbouw, renovatie en utiliteitsbouw',
    'lead': [
        'Wij ontwerpen, rekenen, produceren, transporteren en monteren het stalen '
        'frame met eigen mensen. Eén partij van de eerste berekening tot het frame '
        'dat overeind staat, dus geen naden tussen leveranciers en een korte '
        'doorlooptijd.',
    ],
    'cta_primair': ('Bespreek uw project', 'offerte.html'),
    'cta_secundair': ('Bekijk projecten', 'projecten.html'),

    # Sectie direct onder de partnerband: waar je terecht kunt en waarom.
    'statement_kop': 'Waarom opdrachtgevers voor een stalen frame kiezen',
    'statement': [
        'Een stalen frame is licht en sterk. Dat levert grote overspanningen op, dus '
        'weinig dragende binnenwanden en een indeling die u later opnieuw kunt maken. '
        'Bij een bestaand gebouw betekent hetzelfde lage gewicht dat de extra '
        'belasting beperkt blijft.',
        'De elementen worden op maat gemaakt in de fabriek en op de bouwplaats in '
        'elkaar gezet. Daardoor staat het casco er snel, is de overlast voor '
        'omwonenden korter, en ligt de prijs doorgaans onder die van traditioneel '
        'bouwen.',
        'Wij werken voor particuliere opdrachtgevers, projectontwikkelaars, '
        'aannemers, woningcorporaties, VvE&rsquo;s, vastgoedeigenaren en overheden. '
        'Voor de één maken we één villa, voor de ander seriematige woningbouw of een '
        'optopping van tientallen woningen.',
    ],
    'statement_cta': ('Zo werken we', 'werkwijze.html'),

    # De vijf stappen zelf staan in inhoud_dienst_verhaal.py, want ze staan ook
    # op elke dienstpagina en op werkwijze.html. Hier alleen de kop eromheen.
    'werkwijze_kop': 'Hoe uw project bij ons loopt',
    'werkwijze_lead': 'Vijf stappen, van het inventariseren van de mogelijkheden tot '
                      'de oplevering die we samen met u nalopen. Uw projectleider is '
                      'in alle vijf uw aanspreekpunt.',
    'werkwijze_cta': ('Bekijk de werkwijze', 'werkwijze.html'),

    'werkzaamheden_kop': 'Waarvoor wij staalframes maken',
    'werkzaamheden_lead': 'Drie richtingen, met daaronder de vraag waarmee '
                          'opdrachtgevers meestal binnenkomen.',
    'losse_kop': 'De techniek erachter',
    'losse_lead': 'Wat het frame is, hoe het wordt gerekend en getekend, en waarmee '
                  'de wanden en gevels worden gesloten.',

    'projecten_kop': 'Wat er inmiddels staat',
    'projecten_cta': ('Alle projecten', 'projecten.html'),

    'over_kop': 'Engineering, productie en montage in één hand',
    'over': [
        'Onze engineers rekenen en tekenen het frame. In onze eigen '
        'productiefaciliteit worden de profielen gebogen, gestanst en gesneden, en '
        'een vast team monteurs zet ze op de bouwplaats in elkaar. De C100-profielen '
        'maken we zelf; grotere C-profielen komen van onze partners.',
        'Dat u met één partij te maken heeft, scheelt u de afstemming tussen '
        'tekenaar, leverancier en montageploeg. Loopt er iets anders dan gedacht, dan '
        'zit degene die het frame heeft gerekend in hetzelfde bedrijf als degene die '
        'het monteert.',
    ],
    'over_cta': ('Over Steel Framing Holland', 'over-ons.html'),

    'slot_kop': 'Leg uw project bij ons neer',
    'slot': 'Stuur ons de tekeningen of vertel kort wat u wilt bouwen. Wij kijken wat '
            'in staalframe mogelijk is en wat het gaat kosten.',
}


# ---------------------------------------------------------------------------
#  Diensten
# ---------------------------------------------------------------------------
# Per dienst:
#   lead        de eerste alinea's op de pagina: waarom dit relevant is
#   wanneer_kop de eerste H2, die iets zegt in plaats van "Wanneer is dit iets voor u?"
#   uitleg_kop  de kop boven de technische uitleg uit de bron
#   uitleg      de brontekst herschreven; de bron schuift dan naar het uitlegblok
#   lijst_kop   de kop boven een opsomming uit de bron
#   cta         (label, bestand) voor de knop in het statement
DIENST = {
    # ------------------------------------------------------- toepassingen
    'woningbouw.html': {
        'lead': [
            'Een stalen frame laat zich indelen zoals u wilt. Grote overspanningen '
            'betekenen weinig dragende binnenwanden, en dus een woning die u over tien '
            'jaar opnieuw kunt indelen zonder aan de constructie te komen.',
            'Wij hebben woningen in staalframebouw gerealiseerd in eigen beheer en met '
            'andere partijen, van vrijstaande villa tot seriematige woningbouw.',
        ],
        'wanneer_kop': 'Voor wie wij woningen bouwen',
        'uitleg_kop': 'Hoe een woning in staalframe wordt opgebouwd',
        'uitleg': [
            'De woning bestaat uit een stalen frame waarin geprefabriceerde vloeren, '
            'wanden en gevels worden bevestigd. Wat waar komt, en hoe de woning wordt '
            'ingedeeld, volgt uit de wensen van de bewoner.',
            'U kunt daarbij werken met een vast team waarin architect, constructeur en '
            'adviseur zitten, naast onze eigen fabricage-unit en onze eigen monteurs. '
            'Dat geleide traject van eerste contact tot oplevering verkort de bouwtijd '
            'en levert een gegarandeerde kostprijs op.',
            'Voor een particuliere woningbezitter, een projectontwikkelaar en een '
            'overheid pakt dat hetzelfde uit: één aanspreekpunt, en vooraf duidelijk '
            'wat het gaat kosten.',
        ],
        'cta': ('Bespreek uw woningbouwplan', 'offerte.html'),
    },
    'renovatie.html': {
        'lead': [
            'Een extra verdieping op een bestaand gebouw, een gevel die eraf moet, een '
            'vleugel die erbij komt. Omdat een staalframe licht is, blijft de extra '
            'belasting op het bestaande gebouw en de fundering beperkt.',
            'Het frame gaat snel in elkaar. Dat scheelt bouwtijd en het houdt de '
            'overlast voor bewoners en omwonenden kort, wat in een binnenstedelijke '
            'omgeving vaak zwaarder weegt dan de bouwkosten zelf.',
        ],
        'wanneer_kop': 'Waarvoor eigenaren en corporaties ons vragen',
        'uitleg_kop': 'Optoppen en het vervangen van gebouwdelen',
        'uitleg': [
            'De renovatiemogelijkheden van staalframebouw zie je vooral terug in '
            'binnenstedelijk gebied. VvE&rsquo;s, woningbouwverenigingen en '
            'vastgoedmaatschappijen zetten het regelmatig in bij het optoppen van hun '
            'bezit: één of meer extra verdiepingen boven op een bestaand gebouw.',
            'Naoorlogse portiek- en galerijflats lenen zich daar goed voor. Ze zijn '
            'onderling gelijk van maat en hebben meestal een plat dak, dus een '
            'oplossing die op het eerste blok werkt, werkt ook op het volgende.',
            'Ook het vervangen of uitbreiden van gebouwdelen gaat efficiënt met een '
            'staalframe. Denk aan een gevel die wordt vervangen door prefab '
            'gevelelementen, of een aanbouw waarvoor de bestaande constructie niet '
            'zwaarder mag worden belast.',
        ],
        'cta': ('Bespreek uw renovatieproject', 'offerte.html'),
    },
    'utiliteitsbouw.html': {
        'lead': [
            'Bedrijfsunits, kantoren, hallen en scholen bouwen met een staalframe gaat '
            'sneller en flexibeler dan conventioneel, en doorgaans goedkoper. De lichte '
            'constructie volgt het ontwerp in plaats van het te beperken.',
            'Bij een utiliteitsproject zit de winst meestal niet in de laagste prijs per '
            'element maar in een uitvoering die niet stilstaat. Daarom doen wij de '
            'engineering, de fabricage en de montage met eigen mensen.',
        ],
        'wanneer_kop': 'Waar staalframebouw in de utiliteit uitkomt',
        'uitleg_kop': 'Wat er constructief mogelijk is',
        'uitleg': [
            'De lichte constructie kan volledig naar de hand van het ontwerp worden '
            'gezet en sluit aan bij de huidige normen voor energie en duurzaamheid.',
            'Het lichtgewicht stalen frame is stevig genoeg om tot zes verdiepingen door '
            'te stapelen, zonder hulpconstructie. Wilt u hoger, of vraagt een creatief '
            'ontwerp meer stevigheid op één punt, dan combineren we het frame met '
            'warmgewalst staal. De bouwmethode bepaalt dus niet waar uw ontwerp ophoudt.',
            'Utiliteitsprojecten zijn vaak omvangrijk en afhankelijk van een strikte '
            'doorloop: schuift de staallevering, dan schuift alles erachter mee. Met '
            'engineering-, fabricage- en montageteams in eigen gelederen houden we de '
            'uitvoering en de kosten in de hand.',
        ],
        'cta': ('Leg uw utiliteitsproject voor', 'offerte.html'),
    },

    # ------------------------------------------------------------ techniek
    'ontwerpen-tekenen-en-berekenen.html': {
        'lead': [
            'Voordat er één profiel wordt gebogen, moet vaststaan dat het gebouw doet '
            'wat het moet doen en dat de constructie het houdt. Wij maken het ontwerp, '
            'de tekeningen en de berekeningen, en zorgen dat het geheel aan de geldende '
            'normen en eisen voldoet.',
            'Heeft u al een architect? Dan werken wij onze tekeningen en berekeningen '
            'uit in het verlengde van dat ontwerp.',
        ],
        'wanneer_kop': 'Wanneer u hiermee begint',
        'uitleg_kop': 'Van ruimtelijk ontwerp naar maakbare elementen',
        'uitleg': [
            'Iedere staalconstructie begint bij een ruimtelijk-functioneel ontwerp, en '
            'staal geeft daarin veel vrijheid. Met een eigen ontwerp- en '
            'engineeringafdeling geven wij woningen, kantoren en bedrijfspanden vorm en '
            'houden we tegelijk de functionaliteit in het oog.',
            'Onze tekenaars en calculators zetten dat ontwerp met moderne reken- en '
            'tekensoftware om naar de fabricage van de staalframe-elementen. Wat de '
            'fabriek maakt, is dus wat de engineer heeft gerekend, en niet een '
            'interpretatie daarvan.',
            'Levert u een eigen ontwerp aan, dan werken wij in het verlengde daarvan. '
            'Waar nodig overleggen we met de architect, zodat de constructie zijn visie '
            'volgt in plaats van hem te corrigeren.',
        ],
        'cta': ('Laat uw ontwerp doorrekenen', 'offerte.html'),
    },
    'lichtgewicht-staalframe.html': {
        'lead': [
            'Het frame is opgebouwd uit lichtgewicht, koudgevormde staalprofielen. Die '
            'zijn op de millimeter te maken, in vrijwel elke vorm en maat, en ze staan '
            'snel overeind.',
            'De profielen komen uit onze eigen productiefaciliteit. Daardoor bepalen wij '
            'zelf wanneer uw serie op de machine ligt, en hoeft u niet te wachten op de '
            'planning van een leverancier.',
        ],
        'wanneer_kop': 'Wat lichtgewicht staal oplevert',
        'uitleg_kop': 'Van profiel tot gemonteerd casco',
        'uitleg': [
            'Onze productiefaciliteit buigt, stanst en snijdt de frames non-stop. Op maat '
            'fabriceren gaat daardoor snel, ook als er halverwege iets wijzigt.',
            'Hoe het frame bij u aankomt, kiest u zelf. Als bouwpakket op locatie, met '
            'onze montage erbij, of volledig voorgemonteerd in onze werkplaats. In dat '
            'laatste geval vervoeren we de constructie geheel of in delen met ons eigen '
            'gespecialiseerde wagenpark, takelen hem ter plaatse omhoog, bevestigen hem '
            'aan de fundering en monteren af. Dat is de snelste route.',
            'Staal is bovendien maatvast: het krimpt niet, zet niet uit en vervormt niet '
            'door vocht. Dat is een eigenschap van het materiaal, en het is de reden dat '
            'stucwerk niet scheurt en vloeren niet gaan werken.',
            'Het frame is pas af als de wanden en gevels dicht zijn. Dat kan met ons EPS '
            'wandsysteem of met een van de andere wandsystemen.',
        ],
        'cta': ('Vraag een prijsopgave aan', 'offerte.html'),
    },
    'eps-wandsysteem.html': {
        'lead': [
            'Als het frame en de verdiepingsvloeren staan, moeten de wanden erin. Met '
            'EPS-elementen gaat dat snel: ze zijn licht, ze isoleren, en de leidingen '
            'kunt u erin wegwerken.',
            'Aan de buitenkant is er weinig van te zien. De gevel wordt afgewerkt met '
            'pleisterwerk, kunststof, hout of steenstrips, dus de woning ziet uit zoals '
            'u hem heeft ontworpen.',
        ],
        'wanneer_kop': 'Wanneer EPS de logische keuze is',
        'uitleg_kop': 'Wat het EPS wandsysteem doet',
        'uitleg': [
            'EPS-elementen isoleren tegen geluid en warmte, zijn brandveilig, sterk, '
            'licht te verwerken en breed toepasbaar. Ze zijn onschadelijk en '
            'milieuvriendelijk, en van de wandsystemen die wij leveren zijn ze de '
            'voordeligste.',
            'Bevestigen gaat eenvoudig en snel, juist door dat geringe gewicht: geen '
            'kraan nodig voor een binnenwand. Alle bekabeling en leidingwerk werkt u weg '
            'in de EPS, dus er hoeft niet achteraf gesleuteld te worden.',
            'Binnenmuur en buitengevel zijn op verschillende manieren af te werken, met '
            'bijvoorbeeld pleisterwerk, kunststof, hout of steenstrip. Uiterlijk en '
            'comfort van een staalframe met EPS kunnen concurreren met conventionele '
            'bouw; het verschil zit in de bouwtijd en de prijs.',
            'Voor EPS werken we nauw samen met Veerhuis, die op wereldwijde schaal '
            'specialist is in EPS-bouwwerken. Samen bouwen we hiermee villa&rsquo;s, '
            'kantoren, bedrijfsgebouwen, scholen en ziekenhuizen.',
        ],
        'cta': ('Vraag naar de mogelijkheden', 'offerte.html'),
    },
    'overige-wandsystemen.html': {
        'lead': [
            'EPS is niet altijd het antwoord. Vraagt uw project andere bouwfysische '
            'prestaties, een hogere statische belasting of een specifieke afwerking, dan '
            'zijn er genoeg alternatieven.',
            'Welk systeem het wordt, hangt af van isolatienormen, '
            '(brand)veiligheidsnormen, esthetische eisen en uw eigen wensen. Wij zetten '
            'de voor- en nadelen voor u op een rij voordat u kiest.',
        ],
        'wanneer_kop': 'Wanneer u naar een ander wandsysteem kijkt',
        'uitleg_kop': 'Welke wandsystemen mogelijk zijn',
        'uitleg': [
            'Aan de binnenzijde van de stalen constructie zijn diverse '
            'bekledingsmaterialen mogelijk, die op elke denkbare manier kunnen worden '
            'nabehandeld. Houten, gipsen, kunststof en aluminium beplating zijn '
            'denkbaar, al dan niet opgevuld met isolatiemateriaal.',
            'Ook kant-en-klare prefab wandelementen monteren wij in de constructie. Voor '
            'de buitengevel zijn er eveneens talloze bekledingsmogelijkheden.',
            'Op basis van uw gegevens praten we u bij over wat de verschillen in de '
            'praktijk betekenen, en komen we met een advies dat op uw project is '
            'toegesneden.',
        ],
        'cta': ('Vraag advies over uw wandsysteem', 'offerte.html'),
    },
}


# ---------------------------------------------------------------------------
#  Projecten
# ---------------------------------------------------------------------------
# WAT HIER WEL EN NIET IN STAAT
#   De bronsite geeft per project alleen een titel, een datum, een plaats en
#   soms een opdrachtgever, een projectsoort en een uitvoerende partij. Er staat
#   geen projectomschrijving, geen opgave, geen uitdaging en geen resultaat.
#
#   De regels hieronder zeggen daarom precies twee dingen: wat voor bouwwerk het
#   is, en wat op de projectfoto's te zien is. Dat eerste volgt uit de titel en
#   de bronvelden, dat tweede uit de foto's zelf. Er staat geen opgave, geen
#   probleem, geen doorlooptijd en geen resultaat bij die de bron niet geeft;
#   dat zou een verzonnen case study zijn.
#
#   Zodra Steel Framing Holland per project vertelt wat de opgave was en welke
#   rol zij hadden, kan elke regel hieronder een volwaardige case study worden.
#   Dat staat als eerste punt in CONTENT-TODO.md.
PROJECT_COPY = {
    'villa-in-bergen': 'Vrijstaande villa van twee lagen met een plat dak, grote '
        'glasvlakken over de volle breedte en een uitkragende bovenverdieping, gebouwd '
        'in een bosrijke omgeving.',
    'brandweerkazerne-zwolle': 'Brandweerkazerne met een wit, geleed volume waarin de '
        'verdiepingen ten opzichte van elkaar verspringen. Op de bouwfoto&rsquo;s is de '
        'stalen draagconstructie achter de gevel te zien.',
    'drijvende-woningen-in-delft': 'Drijvende woningen met een houten gevelbekleding en '
        'donkere luiken. Het lage eigen gewicht van een staalframe telt bij een '
        'drijvende fundering direct mee.',
    'vakantiehuis-bonaire-crown-west-2': 'Vakantiewoning voor opdrachtgever Corzilius, '
        'met een open woonkeuken over de volle diepte en een terras met zwembad. De '
        'luchtfoto&rsquo;s laten de indeling van het perceel zien.',
    'woning-nes-aan-de-amstel': 'Woning voor opdrachtgever Sherton, met een wit '
        'gepleisterde gevel en een donker mansardedak. Tijdens de bouw is de kapconstructie '
        'in delen aangevoerd over het water.',
    'utrecht-portiek-flats-renovatie': 'Renovatie van portiekflats, sinds 2018 in '
        'uitvoering. Op de foto&rsquo;s zijn de bestaande galerijflat en de nieuwe '
        'geveldelen te zien.',
    'kinderopvang': 'Kinderopvang in Almere. De foto&rsquo;s laten de montage van het '
        'stalen frame op de bouwplaats zien, van losse profielen tot het complete casco '
        'met dakvlak.',
    'kantoor-en-werkruimte': 'Kantoor met werkruimte, waarbij het lichte bovenvolume '
        'over de bedrijfsruimte is gelegd. De luchtfoto toont het pand in zijn omgeving.',
    'naarden-renovatie': 'Renovatie van een appartementengebouw, met een nieuwe gevel '
        'met balkons en een lichte bekleding over de volle hoogte.',
    'voortgang-villa-noordwijkerhout': 'Villa in aanbouw op het terrein Sancta Maria, met '
        'ver uitkragende betonvloeren en een gevel die daar tussen wordt gezet.',
    'woningen-lochem': 'Seriematige woningbouw in Lochem. Op de foto&rsquo;s staan de '
        'stalen frames van meerdere woningen naast elkaar op de bouwplaats.',
    'veerhuis-building': 'Woonhuis in Wervershoof met een lichte gevel en een topgevel '
        'met hoge ramen. Tijdens de bouw is de rode staalconstructie zichtbaar.',
    'natuurvillapark-waalerburght-texel': 'Villapark op Texel. De luchtfoto laat de '
        'vrijstaande woningen zien, gegroepeerd rond een waterpartij.',
    'dirkshoeve-vakantiebungalows-fase-2': 'Tweede fase vakantiebungalows in Dirkshorn: '
        'vrijstaande bungalows met een zadeldak en een donkere gevelbekleding.',
    'dirkshoeve-vakantiebungalows-fase-1': 'Eerste fase vakantiebungalows in Dirkshorn, '
        'met dezelfde opzet van vrijstaande bungalows op eigen kavel.',
    'villa-te-zoetermeer': 'Villa in Zoetermeer. De bouwfoto&rsquo;s laten de combinatie '
        'zien waarmee hier is gewerkt: een stalen frame waarin de EPS-wandelementen '
        'worden gezet.',
    'villa-te-schagerbrug': 'Villa in Schagerbrug, waarbij op het stalen frame een '
        'houten kapconstructie is geplaatst.',
    'woonhuis': 'Woonhuis in Voorthuizen. Op de foto&rsquo;s zijn het stalen frame en de '
        'EPS-wanden te zien voordat de gevel werd afgewerkt.',
    'woonhuis-uk': 'Woonhuis in het Verenigd Koninkrijk. De foto&rsquo;s tonen het '
        'complete stalen frame met kap, opgebouwd op de bouwplaats.',
    'hotel-de-grote-kerk-in-hoorn': 'Herbestemming van de Grote Kerk in Hoorn tot hotel. '
        'Binnen het bestaande kerkgebouw is een vrijstaande constructie opgebouwd. '
        'Vakblad Mebest schreef over dit project.',
    'kantershof-optopper': 'Optopping in Amsterdam: op het bestaande dak is een stalen '
        'frame voor een extra verdieping gemonteerd.',
    'thema-dreven-portiek-flats-utrecht': 'Portiekflats in Utrecht, waarbij de entrees en '
        'de gevel zijn vernieuwd.',
    'apparterra': 'Prefab gevels in Heemskerk voor opdrachtgever Van Rhijn Bouw BV, '
        'uitgevoerd door Thermogreen. Op de foto&rsquo;s hangt een compleet gevelelement '
        'met raam aan de kraan.',
    'abc-cluster': 'Prefab gevels in Amersfoort voor opdrachtgever Dura Vermeer, '
        'uitgevoerd door Thermogreen. Het bovenvolume met steenstripgevel is op de '
        'bestaande constructie geplaatst.',
    'gevel-renovatie': 'Gevelrenovatie in Amsterdam voor opdrachtgever Van der Leij '
        'Bouwprojecten BV, met een licht gepleisterde afwerking.',
    'aanbouw-schuur-texel': 'Aanbouw bij een schuur op Texel. De foto&rsquo;s laten de '
        'nieuwe vloerplaat en de aansluiting op het bestaande gebouw zien.',
    'vakantiehuisjes-panoven': 'Vakantiehuisjes in Zevenaar, opgebouwd met EPS-wanden met '
        'rondbogen boven de raamopeningen.',
    'voortgang-ibiza-woonhuis': 'Woonhuis in aanbouw op Ibiza, met een stalen frame en '
        'EPS-wanden op een hellend terrein.',
    'voortgang-woning-azoren-pico': 'Woning in aanbouw op Pico, Azoren, met stalen frame '
        'en EPS-wandelementen.',
    'houses-in-bonaire': 'Woonhuizen op Bonaire: gelijkvormige woningen van één laag met '
        'een licht hellend dak, in serie gebouwd.',
    'bonaire-off-grid-woning': 'Off-grid woning op Bonaire, één laag met een plat dak, '
        'gebouwd op een kavel zonder netaansluiting.',
    'steel-framing-holland-irak': 'Bouwproject in Irak. Op de foto&rsquo;s is te zien hoe '
        'het team de stalen frames en de EPS-wanden ter plaatse opbouwt.',
    'school-in-haiti': 'School in Haïti: een langgerekt gebouw van één laag met een '
        'doorgaand dakvlak, opgebouwd uit een stalen frame.',
    'verblijf-voor-ziekenhuispersoneel': 'Verblijf voor ziekenhuispersoneel in Haïti, '
        'waarbij het stalen frame op een betonnen onderbouw is geplaatst.',
    'cite-soleil': 'Bouwproject in Cité Soleil, Haïti. Op de foto&rsquo;s staat een '
        'gebouw van één laag met een overdekte veranda.',
}

PROJECT = {
    'lead_kop': None,
    'project_kop': 'Wat hier is gebouwd',
    'werk_kop': 'Waar dit project onder valt',
    'werk_lead': 'Per noemer leest u hoe wij dat soort werk aanpakken.',
    'gegevens_kop': 'Projectgegevens',
    'slot_kop': 'Een vergelijkbaar project?',
    'slot': 'Vertel kort wat u wilt bouwen. Wij kijken of we hetzelfde voor u kunnen doen.',
    'cta': ('Bespreek uw project', 'contact.html'),
}

PROJECTEN_OVERZICHT = {
    'h1': 'Wat er inmiddels staat',
    'kop': 'Van vrijstaande villa tot optopping van een flat',
    'lead': 'Woningen, renovaties en utiliteitsbouw in Nederland, en projecten op '
            'Bonaire, in Haïti, Irak, het Verenigd Koninkrijk, op Ibiza en op de '
            'Azoren. Een project staat soms onder meer dan één noemer.',
    'slot_kop': 'Een vergelijkbaar project?',
}


# ---------------------------------------------------------------------------
#  Over ons, werkwijze en partners
# ---------------------------------------------------------------------------
BEDRIJF = {
    'over-ons.html': {
        'h1': 'Specialisten in staal en staalframebouw',
        'lead': [
            'Steel Framing Holland ontwerpt, tekent, berekent, fabriceert, transporteert '
            'en monteert staalframes voor woningen en andere bouwwerken. Die zes stappen '
            'doen wij zelf, met eigen engineers, een eigen productiefaciliteit en een '
            'vast team monteurs.',
            'Daardoor houden wij grip op de kwaliteit en blijft de doorlooptijd kort. En '
            'als er tijdens de bouw iets anders blijkt te zijn dan op de tekening, dan '
            'zitten de mensen die het hebben gerekend en de mensen die het monteren in '
            'hetzelfde bedrijf.',
        ],
        'slot_kop': 'Kennismaken?',
    },
    'werkwijze.html': {
        'h1': 'Constructieve werkwijze',
        'lead': [
            'Van eerste gesprek tot oplevering doorloopt elk project bij ons dezelfde '
            'route. Hieronder staat welke stappen dat zijn, wat u per stap van ons krijgt '
            'en wat wij op dat moment van u nodig hebben.',
        ],
        'slot_kop': 'Uw project langs deze route',
    },
    'partners.html': {
        'h1': 'Onze partners',
        'lead': [
            'Een deel van het werk doen wij niet alleen. Onze partners leveren materialen '
            'en profielen, en brengen specialisme mee waardoor we samen een compleet '
            'pakket kunnen aanbieden.',
            'Hieronder staat met wie wij vast werken, en waarvoor.',
        ],
        'slot_kop': 'Overleg over uw project',
    },
}


# ---------------------------------------------------------------------------
#  Contact en offerte
# ---------------------------------------------------------------------------
CONTACT = {
    'h1': 'Contact',
    'lead': [
        'Weet u al wat u wilt bouwen? Stuur dan de tekeningen mee, dan kunnen wij '
        'gericht antwoorden wat er in staalframe mogelijk is en wat het kost.',
        'Weet u dat nog niet precies? Bel of mail ons dan gerust. Dan kijken we eerst '
        'samen waar uw project om vraagt.',
    ],
    'formulier_kop': 'Stuur ons een bericht',
    'formulier_lead': 'Vertel kort waar het over gaat. Wij nemen zo spoedig mogelijk '
                      'contact met u op.',
}

OFFERTE = {
    'h1': 'Prijsopgave aanvragen',
    'lead': [
        'Vraag hieronder vrijblijvend een prijsopgave aan. Hoe concreter u het project '
        'beschrijft, hoe beter wij kunnen aangeven wat er mogelijk is en wat het gaat '
        'kosten.',
    ],
    'formulier_kop': 'Vertel ons over uw project',
    'formulier_lead': 'Na ontvangst nemen wij contact met u op, of komen we direct met '
                      'een opgave als we genoeg weten.',
}


def dienst(bestand):
    """De herschreven copy voor een dienstpagina, of een leeg blok."""
    return DIENST.get(bestand, {})


def project_lead(slug):
    """De omschrijving bij een project, of niets als die er niet is."""
    return PROJECT_COPY.get(slug)


# ---------------------------------------------------------------------------
#  SEO: titel en omschrijving per pagina
# ---------------------------------------------------------------------------
# De bronsite heeft op geen enkele pagina een meta description, en als title
# staat er overal "<Paginanaam> |  Steel Framing Holland" (met dubbele spatie).
# Die zijn dus niet over te nemen; hieronder staan ze per pagina.
#
# Regels die hier zijn aangehouden:
#   - Titel plus " | Steel Framing Holland" onder de 65 tekens, met het
#     zoekwoord vooraan. Langer dan dat kapt Google af.
#   - Omschrijving tussen 120 en 158 tekens, met een reden om te klikken en
#     niet alleen een opsomming van zoekwoorden.
#   - Geen enkel getal, tarief of levertijd, want die staan niet in de bron.
SEO = {
    'index.html': (
        'Staalframebouw uit eigen productie',
        'Wij ontwerpen, rekenen, produceren en monteren staalframes met eigen '
        'mensen. Eén partij van de eerste berekening tot het gemonteerde frame. '
        'Bespreek uw project.'),
    'woningbouw.html': (
        'Woningbouw in staalframe',
        'Grote overspanningen, dus een vrije indeling. Van vrijstaande villa tot '
        'seriematige woningbouw, met een geleid traject en een gegarandeerde '
        'kostprijs.'),
    'renovatie.html': (
        'Renovatie en optoppen met staalframebouw',
        'Een extra verdieping of een nieuwe gevel zonder het bestaande gebouw zwaar '
        'te belasten. Snel gemonteerd, dus korte overlast voor bewoners en '
        'omwonenden.'),
    'utiliteitsbouw.html': (
        'Utiliteitsbouw in staalframe',
        'Bedrijfsunits, kantoren, hallen en scholen in staalframebouw. Engineering, '
        'fabricage en montage in eigen hand, zodat de planning en de kosten in de '
        'hand blijven.'),
    'ontwerpen-tekenen-en-berekenen.html': (
        'Ontwerpen, tekenen en berekenen',
        'Eigen ontwerp- en engineeringafdeling voor woningen, kantoren en '
        'bedrijfspanden. Ook met uw eigen architect: wij werken uit in het verlengde '
        'van dat ontwerp.'),
    'lichtgewicht-staalframe.html': (
        'Lichtgewicht staalframe',
        'Koudgevormde staalprofielen uit onze eigen productiefaciliteit. Als '
        'bouwpakket, gemonteerd op de bouwplaats of voorgemonteerd in de werkplaats '
        'aangevoerd.'),
    'eps-wandsysteem.html': (
        'EPS wandsysteem',
        'EPS-wanden isoleren tegen geluid en warmte, zijn brandveilig en snel te '
        'bevestigen. Leidingen werkt u erin weg; de gevel wordt afgewerkt zoals u '
        'wilt.'),
    'overige-wandsystemen.html': (
        'Wandsystemen voor staalframebouw',
        'Houten, gipsen, kunststof en aluminium beplating, of kant-en-klare prefab '
        'wandelementen. Wij zetten de voor- en nadelen op een rij voordat u kiest.'),
    'projecten.html': (
        'Projecten in staalframebouw',
        'Woningen, renovaties en utiliteitsbouw in Nederland, en projecten op '
        'Bonaire, in Haïti, Irak, het Verenigd Koninkrijk, op Ibiza en op de Azoren.'),
    'over-ons.html': (
        'Over ons: specialist in staalframebouw',
        'Ontwerpen, tekenen, berekenen, fabriceren, transporteren en monteren doen '
        'wij zelf, met eigen engineers, een eigen productiefaciliteit en een vast '
        'team monteurs.'),
    'werkwijze.html': (
        'Werkwijze: van oriëntatie tot oplevering',
        'Vijf stappen, van het inventariseren van de mogelijkheden tot de oplevering '
        'die we samen met u nalopen. Per stap weet u wie wat doet.'),
    'partners.html': (
        'Onze partners',
        'Veerhuis Bouwsystemen, MM Staal, Finish Profiles en onze andere partners '
        'leveren materialen en specialisme, zodat we samen een compleet pakket '
        'kunnen aanbieden.'),
    'contact.html': (
        'Contact',
        'Netwerk 150 in Purmerend, met een eigen ingang voor de werkplaats op '
        'Component 148. Bel, mail of stuur uw tekeningen mee.'),
    'offerte.html': (
        'Prijsopgave aanvragen',
        'Vraag vrijblijvend een prijsopgave aan. Hoe concreter u het project '
        'beschrijft, hoe beter wij kunnen aangeven wat er mogelijk is en wat het '
        'gaat kosten.'),
}


def seo(bestand, standaard_titel='', standaard_omschrijving=''):
    """(titel, omschrijving) voor een pagina, of de meegegeven terugval."""
    return SEO.get(bestand, (standaard_titel, standaard_omschrijving))


def project_seo(titel, plaats, categorieen):
    """Titel en omschrijving voor een projectpagina.

       Opgebouwd uit de projectgegevens die de bron wél geeft, want een eigen
       regel per project zou 35 keer hetzelfde zeggen met andere woorden."""
    # De merknaam niet twee keer: één project heet zelf "Steel Framing
    # Holland in Irak".
    t = titel if 'Steel Framing Holland' in titel else f'{titel} | Steel Framing Holland'
    soort = (categorieen[0].lower() if categorieen else 'staalframebouw')
    # De plaats niet noemen als die al in de titel staat: "villa Noordwijkerhout
    # in Noordwijkerhout" leest als een fout.
    waar = f' in {plaats}' if plaats and plaats.lower() not in titel.lower() else ''
    o = f'{titel}{waar}: {soort} in staalframebouw.'
    staart = (' Bekijk de foto&rsquo;s van dit project en wat wij voor een '
              'vergelijkbare opgave kunnen doen.')
    # Google kapt rond de 160 tekens af; bij een lange projecttitel valt de
    # tweede zin er daarom af in plaats van halverwege te stoppen.
    if len(o) + len(staart) <= 158:
        o += staart
    else:
        o += ' Bekijk de foto&rsquo;s van dit project.'
    return t, o


def seo_titel(bestand):
    """De <title> voor een pagina: de SEO-titel plus de bedrijfsnaam, en die
       naam maar één keer."""
    t = SEO[bestand][0]
    return t if 'Steel Framing Holland' in t else f'{t} | Steel Framing Holland'

# ---------------------------------------------------------------------------
#  Ondertitels in het menu en op de kaarten
# ---------------------------------------------------------------------------
# Eén regel per pagina, en met opzet kort: in het uitklapmenu staat hij op één
# of twee regels naast de naam, en op een kaart onder de titel. Een afgekapte
# eerste zin uit de lead deed het daar niet, want die brak middenin een
# opsomming af ("een gevel die eraf moet, een vleugel die erbij…").
MENU_ONDERTITEL = {
    'woningbouw.html': 'Van vrijstaande villa tot seriematige woningbouw',
    'renovatie.html': 'Optoppen, gevels vervangen en uitbreiden',
    'utiliteitsbouw.html': 'Bedrijfsunits, kantoren, hallen en scholen',
    'ontwerpen-tekenen-en-berekenen.html': 'Ook in het verlengde van uw eigen ontwerp',
    'lichtgewicht-staalframe.html': 'Koudgevormde profielen uit eigen productie',
    'eps-wandsysteem.html': 'Isolerend, brandveilig en voordelig',
    'overige-wandsystemen.html': 'Hout, gips, kunststof, aluminium of prefab',
}


def menu_ondertitel(bestand):
    """De regel onder een paginanaam in het menu en op een kaart."""
    return MENU_ONDERTITEL.get(bestand, '')
