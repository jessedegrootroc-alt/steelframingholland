# Herkomst van de herofilm

`sfh-hero.mp4` is de film achter de kop op de homepage. Aangeleverd door Jesse
op 10 september 2026 als
`Steel_framing_video_generation_i…_20260910121732.mp4`.

Het origineel staat in `_generator/assets_bron/sfh/sfh-hero-video-origineel.mp4`
en gaat niet mee met de site.

## Wat er met het bestand is gedaan

| | origineel | wat er staat |
|---|---|---|
| grootte | 6,5 MB | **1,24 MB** |
| beeld | 1280×720, h264, 24 fps, 10,0 s | ongewijzigd |
| geluid | AAC-spoor | **eruit** |
| helderheid | zoals aangeleverd | **teruggebracht** (zie hieronder) |
| start | gewone mp4 | **faststart**: de index staat vooraan, dus hij begint te spelen voordat het hele bestand binnen is |

Het geluidsspoor is eruit omdat de film gedempt en in een lus staat: geluid is
daar alleen gewicht. De naam is veranderd omdat de originele bestandsnaam een
weglatingsteken (`…`) bevat, en dat is een niet-ASCII teken in een URL.

De commando's:

```bash
ffmpeg -i sfh-hero-video-origineel.mp4 -an \
  -vf "colorlevels=romax=0.52:gomax=0.52:bomax=0.52,eq=contrast=1.08" \
  -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -movflags +faststart \
  sfh-hero.mp4

# het eerste beeldje als terugvalfoto
ffmpeg -i sfh-hero.mp4 -vf "select=eq(n\,0)" -vsync 0 -q:v 1 sfh-hero-still.jpg
```

CRF 26 is gekozen na vergelijking met CRF 24 en 28: het gemiddelde verschil met
het origineel is 1,5 op 255 en op een uitsnede van 100% is het niet te zien,
terwijl het bestand van 6,5 MB naar 1,24 MB gaat. Donkerder beeld comprimeert
beter, dus de gradatie hieronder maakt het bestand nog kleiner.

## Waarom de film donkerder is gemaakt

Over deze film staat witte tekst: de kop, het label, de introtekst, de knoppen
en de navigatie. Ongegradeerd haalde die tekst de contrasteis niet, ook niet met
de sluier die er al lag. Gemeten over dertig beeldjes:

| tekstvlak | eis | ongegradeerd | na gradatie |
|---|---|---|---|
| navigatie (14px) | 4,5:1 | 2,53:1 | **5,3:1** |
| label (11px) | 4,5:1 | 1,88:1 | **5,1:1** |
| titel (72px) | 3,0:1 | 2,19:1 | **5,2:1** |
| introtekst (16px) | 4,5:1 | 3,05:1 | **5,9:1** |
| knoppen (11px) | 4,5:1 | 3,32:1 | **5,7:1** |

Dat is opgelost in de film en niet in de sluier, en dat is een bewuste ruil. Een
sluier haalt contrast **weg** uit het beeld: alles gaat naar zwart toe, de lucht
gaat banden vertonen en de film wordt een grijs vlak met een hint van beweging.
Een gradatie houdt het contrast binnen het beeld intact en maakt het alleen
donkerder.

Daardoor kon de sluier in `index.css` van drie stops (68% boven, 36% midden, 70%
onder) terug naar één vlakke laag van **25%**. Dat is wat je ziet: boven in de
hero is de film ruim twee keer zo goed zichtbaar als eerst, terwijl de tekst er
nog steeds ruim boven de eis op staat.

## Opnieuw meten

Komt er een andere film, dan moet deze meting opnieuw:

```bash
python3 _generator/meet_hero_contrast.py assets/video/sfh-hero.mp4
```

Dat script haalt dertig beeldjes uit de film, bepaalt per beeldje welk deel bij
`object-fit: cover` echt in beeld komt (op desktop én op een staande telefoon),
legt de sluier uit `index.css` eroverheen en rekent per tekstvlak het contrast
van witte tekst uit. Het neemt het 98e percentiel van de helderheid, niet het
gemiddelde: één lichte plek achter de kop is al genoeg om hem onleesbaar te
maken.

Blijkt een nieuwe film ongegradeerd donker genoeg, dan is de gradatie niet
nodig; laat `colorlevels` dan weg.

## Wat er nog beter kan

Deze film is machinaal gegenereerd. Voor een bedrijf dat vijfendertig echte
projecten heeft staan, is eigen opnamemateriaal sterker: de eigen
productiefaciliteit, het wagenpark en een montageploeg aan het werk. Dat is
precies het verhaal dat de homepage vertelt en waar nu geen beeld van is. Zie
`CONTENT-TODO.md`.
