/* ============================================================================
   smooth-scroll.js: vloeiend scrollen met GSAP ScrollSmoother
   ----------------------------------------------------------------------------
   ScrollSmoother laat de echte scrollbalk van de browser staan en verschuift
   alleen de inhoud ernaartoe. Er komt dus geen namaakscrollbalk in de plaats:
   het muiswiel, de spatiebalk, Page Down, de zoekfunctie van de browser en het
   slepen van de scrollbalk blijven allemaal werken.

   Drie dingen om te weten als je hieraan werkt:

   - Alles wat position:fixed is hoort BUITEN #smooth-wrapper. De inhoud krijgt
     een transform, en een transform maakt een nieuw ankerpunt voor fixed. De
     header, het mobiele paneel en de cookiemelding staan daarom rechtstreeks in
     de body.
   - Bij een pagina-overgang wordt de smoother gesloopt en daarna opnieuw
     opgebouwd; page-transitions.js roept sloop() en maak() aan. De overgang
     zet de containers zelf op position:fixed, en dat werkt niet onder een
     transform.
   - Wie beweging heeft uitgezet (prefers-reduced-motion) krijgt geen smoothing.
     Dan blijft het de gewone scroll van de browser en is #smooth-wrapper een
     doodgewone div.

   Laadt GSAP of een van de twee plug-ins niet, dan gebeurt hier niets en scrolt
   de site precies zoals hij zonder dit bestand zou doen.
   ========================================================================== */

window.MADEGRO = window.MADEGRO || {};

(() => {
  const { gsap, ScrollTrigger, ScrollSmoother } = window;
  if (!gsap || !ScrollTrigger || !ScrollSmoother) return;

  gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

  const kalm = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Staat even op true terwijl we zelf naar een anker springen; zie onFocusIn
     hieronder en de ankerafhandeling onderaan. */
  let eigenSprong = false;

  const api = {
    instantie: null,

    maak() {
      if (this.instantie || kalm.matches) return this.instantie;
      if (!document.getElementById('smooth-wrapper')) return null;

      this.instantie = ScrollSmoother.create({
        wrapper: '#smooth-wrapper',
        content: '#smooth-content',

        /* Tijd in seconden om de echte scrollpositie in te halen. Hoger voelt
           zwever; boven ongeveer 1,5 gaat het los staan van wat je doet. */
        smooth: 1,

        /* Kijkt naar data-speed en data-lag op elementen. Er staat op dit
           moment nergens zo'n attribuut; dit zet alleen de deur open. */
        effects: true,

        /* Op een telefoon voelt smoothing verkeerd: de pagina loopt dan achter
           je vinger aan. 0 is ook de standaard van de plug-in. */
        smoothTouch: 0,

        /* Krijgt een element focus, dan zorgt ScrollSmoother normaal dat het in
           beeld komt. Dat is precies wat je wilt bij tabben, maar niet als we
           zelf al naar dat element aan het springen zijn: bij een sectie die
           hoger is dan het scherm legt ScrollSmoother de onderkant op het
           scherm en overschrijft dat onze eigen positie. */
        onFocusIn: () => (eigenSprong ? false : undefined),
      });

      return this.instantie;
    },

    sloop() {
      if (!this.instantie) return;
      this.instantie.kill();
      this.instantie = null;
    },
  };

  window.MADEGRO.smoother = api;
  api.maak();

  /* --------------------------------------------------------- ankerlinks ----
     Een link naar #iets laat de browser normaal zelf naar het doel springen.
     Dat lukt hier niet: de inhoud zit in een wrapper met position:fixed, en
     daar kan de browser niet naartoe scrollen. De skip-link bovenaan de pagina
     is er ook een, dus dit is geen randgeval.

     MARGE houdt het doel vrij van de vaste header, anders komt de kop waar je
     naartoe springt er precies achter te liggen. */
  const MARGE = 110;

  document.addEventListener('click', (e) => {
    const link = e.target.closest?.('a[href^="#"]');
    if (!link || link.getAttribute('href') === '#') return;

    const id = decodeURIComponent(link.getAttribute('href').slice(1));
    const doel = document.getElementById(id);
    if (!doel || !api.instantie) return;   // zonder smoother doet de browser het zelf

    e.preventDefault();

    /* Normaal verplaatst de browser de focus mee naar het doel. Dat valt met de
       preventDefault hierboven weg, dus doen we het zelf: anders staat een
       toetsenbordgebruiker na de skip-link nog steeds in het menu.

       De focus gaat bewust v&oacute;&oacute;r het scrollen. ScrollSmoother scrolt zelf
       naar een element dat focus krijgt, en dat zou onze eigen sprong
       overschrijven; nu is onze sprong de laatste. */
    eigenSprong = true;
    if (!doel.hasAttribute('tabindex')) doel.setAttribute('tabindex', '-1');
    doel.focus({ preventScroll: true });

    api.instantie.scrollTo(doel, true, `top ${MARGE}px`);
    history.replaceState(history.state, '', `#${id}`);

    /* Twee beeldjes later mag ScrollSmoother weer zelf naar een focus scrollen. */
    requestAnimationFrame(() => requestAnimationFrame(() => { eigenSprong = false; }));
  });

  /* Kom je binnen op een adres met een anker erin, dan is de smoother er nog
     niet op het moment dat de browser springt. Daarom hier nog een keer. */
  if (location.hash && api.instantie) {
    const doel = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (doel) requestAnimationFrame(() => api.instantie.scrollTo(doel, false, `top ${MARGE}px`));
  }

  /* Zet iemand de bewegingsvoorkeur om terwijl de site openstaat, dan volgen we
     dat meteen in plaats van pas bij de volgende paginalading. */
  kalm.addEventListener('change', () => {
    api.sloop();
    api.maak();
    ScrollTrigger.refresh();
  });
})();
