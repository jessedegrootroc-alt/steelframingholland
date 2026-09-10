/* ============================================================================
   cases.js: de filters op het cases-overzicht
   ----------------------------------------------------------------------------
   Een groep pillen per filterdimensie. Binnen een groep geldt er één tegelijk,
   en de eerste pil ('alle') zet de groep weer open. De kaarten staan gewoon in
   de HTML en worden alleen verborgen, zodat de pagina zonder JavaScript alle
   projecten laat zien.

   Welke dimensies er zijn staat niet meer in dit bestand: ze komen uit de
   data-filter-attributen van de pillen zelf. Nu is dat er één (categorie), maar
   twee of drie werkt net zo goed. Een kaart mag per dimensie meerdere waarden
   hebben, gescheiden door een spatie: een project dat zowel onder verbouwing
   als onder funderingsherstel valt, blijft bij beide filters staan.

   Alles in één functie, zodat het bestand opnieuw uitgevoerd kan worden na een
   pagina-overgang.
   ========================================================================== */

(() => {
  /* Tijdens een overgang staan twee pagina's in de DOM; zoek binnen de eigen. */
  const container = document.currentScript?.closest('[data-barba="container"]') || document;

  const raster = container.querySelector('#caseRaster');
  if (!raster) return;

  const pillen = [...container.querySelectorAll('.filter-pil')];
  const kaarten = [...raster.querySelectorAll('.case-kaart')];
  const telling = container.querySelector('.cases-overzicht__telling');
  const leeg = container.querySelector('.cases-overzicht__leeg');

  /* De dimensies komen uit de pillen; elke groep begint op 'alles'. */
  const groepen = [...new Set(pillen.map((p) => p.dataset.filter))];
  const keuze = Object.fromEntries(groepen.map((g) => [g, 'alles']));

  const werkBij = () => {
    let zichtbaar = 0;
    kaarten.forEach((kaart) => {
      const past = groepen.every((groep) => {
        if (keuze[groep] === 'alles') return true;
        const waarden = (kaart.dataset[groep] || '').split(/\s+/);
        return waarden.includes(keuze[groep]);
      });
      kaart.hidden = !past;
      if (past) zichtbaar++;
    });

    /* De achtergrond van een kaart wisselt om en om. Omdat er kaarten
       wegvallen, moet die wisseling opnieuw geteld worden over wat er
       overblijft; anders staan er twee grijze naast elkaar. */
    let n = 0;
    kaarten.forEach((kaart) => {
      if (kaart.hidden) return;
      kaart.classList.toggle('is-even', n % 2 === 1);
      n++;
    });

    if (telling) {
      telling.textContent = zichtbaar === kaarten.length
        ? `${kaarten.length} projecten`
        : `${zichtbaar} van ${kaarten.length} projecten`;
    }
    if (leeg) leeg.hidden = zichtbaar > 0;
  };

  pillen.forEach((pil) => {
    pil.addEventListener('click', () => {
      const groep = pil.dataset.filter;
      keuze[groep] = pil.dataset.waarde;
      pillen.filter((p) => p.dataset.filter === groep).forEach((p) => {
        const aan = p === pil;
        p.classList.toggle('is-actief', aan);
        p.setAttribute('aria-pressed', String(aan));
      });
      werkBij();
    });
  });

  werkBij();
})();
