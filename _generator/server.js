const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');

const ROOT = "/Users/jessevialuxury.nl/Library/CloudStorage/OneDrive-Advalley(2)/Documenten/Code/SERVICE.BASED.LANDINGSPAGE";
const PORT = 5500;

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.pdf': 'application/pdf',
};

// Tekstbestanden gaan gecomprimeerd over de lijn. Zonder dit is styleguide.css
// 96 kB en index.html 61 kB; met brotli is dat 20 en 10 kB. Afbeeldingen, video
// en woff2 zitten al in een gecomprimeerd formaat en gaan er ongemoeid doorheen:
// die nog eens door gzip halen kost tijd en levert niets op.
const COMPRIMEERBAAR = new Set([
  'text/html; charset=utf-8', 'text/css; charset=utf-8', 'text/javascript; charset=utf-8',
  'application/json; charset=utf-8', 'image/svg+xml', 'application/xml; charset=utf-8',
  'text/plain; charset=utf-8',
]);

// Hoe lang de browser een bestand mag bewaren. De namen van de afbeeldingen en
// van de video dragen hun maat in zich (logistiek-1200.webp); komt er een andere
// versie, dan komt er een andere naam, dus die mogen lang blijven staan.
// HTML, CSS en JS worden nog bewerkt en moeten elke keer opnieuw gecontroleerd
// worden, anders zie je je eigen wijziging niet.
//
// LET OP: dit is de ontwikkelserver. Voor productie horen CSS en JS ook lang
// gecachet te worden, maar dan met een versie in de bestandsnaam of in de query.
// Zie LEVERING.md voor de headers die daar horen te staan.
function cache(type) {
  if (type.startsWith('image/') || type.startsWith('video/') || type.startsWith('font/')) {
    // Geen immutable hier. De namen dragen hun maat (logistiek-1200.webp), maar
    // tijdens het bouwen wordt een bestand weleens vervangen zonder dat de naam
    // verandert, en dan zit je er met immutable een jaar aan vast. In productie
    // hoort hier wel immutable te staan; zie LEVERING.md.
    return 'public, max-age=86400';
  }
  return 'no-cache';
}

http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.normalize(path.join(ROOT, rel));
  if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(file, (err, data) => {
    if (err) {
      res.writeHead(404, {'Content-Type': 'text/html; charset=utf-8'});
      return res.end('<h1>404</h1><p>' + rel + '</p>');
    }
    const type = TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream';
    // Zwakke etag (W/): hij staat voor de inhoud van het bestand, niet voor de
    // vorm waarin het over de lijn gaat. Hetzelfde bestand kan er brotli, gzip
    // of onverpakt uitgaan; dat zijn andere bytes met dezelfde inhoud.
    const etag = 'W/"' + crypto.createHash('sha1').update(data).digest('base64').slice(0, 20) + '"';
    const kop = {'Content-Type': type, 'Cache-Control': cache(type), 'ETag': etag};
    if (req.headers['if-none-match'] === etag) { res.writeHead(304, kop); return res.end(); }

    // Een video wordt niet in één keer opgehaald. De browser vraagt om stukken
    // (Range: bytes=0-1, dan verder) en verwacht daar 206 op met precies dat
    // stuk. Safari en iOS spelen niets af als de server dat negeert en gewoon
    // 200 met het hele bestand terugstuurt; Chrome is er soepeler in. Vandaar
    // dit blok. Accept-Ranges vertelt de browser vooraf dat het kan.
    if (type.startsWith('video/') || type.startsWith('audio/')) {
      kop['Accept-Ranges'] = 'bytes';
      const bereik = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '');
      if (bereik) {
        const eind = bereik[2] ? Math.min(parseInt(bereik[2], 10), data.length - 1) : data.length - 1;
        const begin = bereik[1] ? parseInt(bereik[1], 10) : data.length - eind - 1;
        if (begin > eind || begin >= data.length) {
          res.writeHead(416, {'Content-Range': `bytes */${data.length}`});
          return res.end();
        }
        kop['Content-Range'] = `bytes ${begin}-${eind}/${data.length}`;
        kop['Content-Length'] = eind - begin + 1;
        res.writeHead(206, kop);
        return res.end(data.subarray(begin, eind + 1));
      }
    }

    const mag = (req.headers['accept-encoding'] || '');
    if (COMPRIMEERBAAR.has(type) && data.length > 512) {
      if (/\bbr\b/.test(mag)) {
        kop['Content-Encoding'] = 'br';
        kop['Vary'] = 'Accept-Encoding';
        return zlib.brotliCompress(data, {
          params: {[zlib.constants.BROTLI_PARAM_QUALITY]: 5},
        }, (e, uit) => { res.writeHead(200, kop); res.end(e ? data : uit); });
      }
      if (/\bgzip\b/.test(mag)) {
        kop['Content-Encoding'] = 'gzip';
        kop['Vary'] = 'Accept-Encoding';
        return zlib.gzip(data, {level: 6}, (e, uit) => {
          res.writeHead(200, kop); res.end(e ? data : uit);
        });
      }
    }
    res.writeHead(200, kop);
    res.end(data);
  });
}).listen(PORT, () => console.log('Serving ' + ROOT + ' on http://localhost:' + PORT));
