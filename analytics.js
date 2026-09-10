/* ---- Google Analytics, achter toestemming ----

   VUL HIER DE MEETCODE IN. Je vindt hem in Google Analytics onder
   Beheer > Gegevensstromen > je website. Hij begint met G- en ziet eruit als
   G-ABC1234XYZ. Zolang dit leeg is, gebeurt er niets: er wordt geen script
   geladen en er komt geen cookie op de site.

   TODO-CONTENT: meet-ID aanleveren door Martin (of laten staan als er geen
   statistieken gemeten worden).                                              */
const META_ID = '';

/* Analytics laadt pas nadat de bezoeker analytische cookies heeft aangezet in
   de cookiemelding. Dat is niet alleen netjes, het is ook wat het privacy-
   beleid belooft. */
(() => {
  if (!META_ID) return;

  let geladen = false;

  const laad = () => {
    if (geladen) return;
    geladen = true;

    /* Stond de uitschakelvlag nog aan van een eerdere weigering, dan moet die
       eerst uit; anders laadt gtag wel maar stuurt hij niets door. */
    window['ga-disable-' + META_ID] = false;

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', META_ID, { anonymize_ip: true });

    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(META_ID);
    document.head.appendChild(script);
  };

  const zetUit = () => {
    /* Officiële uitschakelvlag van Google: hiermee stuurt gtag niets meer. */
    window['ga-disable-' + META_ID] = true;
    /* En de cookies die al stonden opruimen, zodat 'weigeren' ook echt
       betekent dat er niets van je achterblijft. */
    document.cookie.split(';').forEach(c => {
      const naam = c.split('=')[0].trim();
      if (naam === '_ga' || naam.startsWith('_ga_') || naam === '_gid') {
        const domein = location.hostname.replace(/^www\./, '');
        document.cookie = naam + '=; Max-Age=0; path=/';
        document.cookie = naam + '=; Max-Age=0; path=/; domain=.' + domein;
      }
    });
  };

  const verwerk = (keuze) => (keuze && keuze.analytisch) ? laad() : zetUit();

  /* De cookiemelding zet de keuze klaar en meldt elke wijziging. Allebei
     afhandelen, want welke van de twee eerst is hangt af van de laadvolgorde. */
  verwerk(window.madegroToestemming);
  document.addEventListener('madegro:toestemming', (e) => verwerk(e.detail));
})();
