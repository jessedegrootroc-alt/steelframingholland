# Uitrollen

De site is platte HTML, CSS en JavaScript. Er is geen server nodig die iets
uitvoert: alle bestanden in de hoofdmap plus `assets/` uploaden is genoeg. Wat
er wél moet, is compressie en cache aanzetten; zonder dat zakt de
Lighthouse-score met ongeveer vijf punten en duurt het eerste beeld op een
telefoon een halve seconde langer.

## Wat de host moet doen

| | Waarom |
|---|---|
| **gzip of brotli** op html, css, js, svg, xml | `styleguide.min.css` gaat van 61 kB naar ruim 10 kB, de HTML van 65 kB naar 11 kB |
| **lange cache op css en js** | Ze worden aangeroepen met `?v=<hash van de inhoud>`, dus een nieuwe versie krijgt automatisch een nieuwe URL |
| **geen cache op html** | Daarin staan die hashes; een oude pagina wijst naar een oude stylesheet |
| **byte-ranges op mp4** | Safari op iOS speelt de herofilm niet zonder; zie hieronder |

Beeld, video en lettertypen niet comprimeren: webp, avif, mp4 en woff2 zijn dat
al, en er nog een laag omheen doen kost tijd en levert niets op.

## Byte-ranges, anders speelt de herofilm niet op een iPhone

Safari op iOS speelt een mp4 alleen als de server een deel van het bestand kan
sturen: status **206** met een `Content-Range`. Komt er 200 met het hele
bestand, dan blijft de film staan en zie je de foto eronder. Op desktop en op
Android valt dat niet op, want die spelen hem wel.

Apache, nginx, Netlify en Cloudflare doen dit standaard. Controleer het na het
uploaden:

```bash
curl -sI -H 'Range: bytes=0-1023' https://<jouw-domein>/assets/video/sfh-hero.mp4
```

Dat moet `206 Partial Content` zijn met `Content-Range: bytes 0-1023/1304051`.
Staat er `200 OK` met de volle lengte, dan speelt de film niet op een iPhone en
moet de host ranges aanzetten.

Twee dingen zetten de film ook uit, en dat is dan geen fout: **Beperk beweging**
in de toegankelijkheidsinstellingen, en de **energiespaarstand** op een iPhone.
In beide gevallen blijft de foto staan, en dat is met opzet zo.

## Apache (de meeste Nederlandse shared hosting)

`.htaccess` staat al in de hoofdmap en regelt dit. Werkt hij niet, dan staat
`AllowOverride` uit; vraag de host om `mod_deflate`, `mod_expires` en
`mod_headers`.

## nginx

```nginx
gzip on;
gzip_types text/html text/css application/javascript application/json image/svg+xml text/xml;
gzip_min_length 512;

location ~* \.(css|js)$        { add_header Cache-Control "public, max-age=31536000, immutable"; }
location ~* \.(webp|avif|png|jpg|mp4)$ { add_header Cache-Control "public, max-age=2592000"; }
location ~* \.woff2$           { add_header Cache-Control "public, max-age=31536000, immutable"; add_header Access-Control-Allow-Origin "*"; }
location ~* \.html$            { add_header Cache-Control "no-cache"; }
```

## Netlify of Cloudflare Pages

Comprimeren doen ze zelf. Voor de cache een bestand `_headers` in de hoofdmap:

```
/*.css
  Cache-Control: public, max-age=31536000, immutable
/*.js
  Cache-Control: public, max-age=31536000, immutable
/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
/assets/*
  Cache-Control: public, max-age=2592000
/*.html
  Cache-Control: no-cache
```

## Voor je uploadt

```bash
python3 _generator/bouw_alles.py
```

Dat minificeert de stylesheets en scripts en schrijft de 51 pagina's opnieuw,
met een verse hash in elke verwijzing. Doe je dat niet na een wijziging in een
`.css`- of `.js`-bestand, dan verwijzen de pagina's naar de oude
`.min`-versie en zie je je wijziging niet.

## Nog te regelen

- `analytics.js`: `META_ID` is leeg, dus er wordt niets gemeten en geen enkel
  script van Google geladen. Vul het meet-id in als dat moet, en bouw opnieuw.
- Het contactformulier verstuurt nog niets: `ENDPOINT` in
  `contactformulier.js` is leeg. Zie `CONTENT-TODO.md`.
- `BASIS` in `_generator/schil.py` staat op
  `https://www.steelframingholland.nl`. Daar komen de canonical-links, de
  sitemap en de deelafbeelding uit. Wijzig dat als de site op een ander domein
  komt te staan.
