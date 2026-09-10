/* ---- Cookiemelding ----
   De keuze wordt opgeslagen in localStorage, niet in een cookie: daarvoor is
   geen toestemming nodig, want het is puur de vastlegging van je eigen keuze.

   Er staan op dit moment nog geen analytische of marketingscripts op de site.
   Deze balk legt de toestemming alvast vast en stelt die beschikbaar, zodat
   zo'n script later alleen hoeft te laden als de bezoeker ja heeft gezegd:

     window.madegroToestemming            -> { analytisch, marketing }
     window.madegroCookies.open()         -> balk opnieuw tonen
     document.addEventListener('madegro:toestemming', e => e.detail)
*/
(() => {
  const SLEUTEL = 'madegro-cookies-v1';
  const balk = document.getElementById('cookiebalk');
  if (!balk) return;

  const keuzes = balk.querySelector('#cookieKeuzes');
  const schakelaars = {
    analytisch: balk.querySelector('#cookieAnalytisch'),
    marketing:  balk.querySelector('#cookieMarketing'),
  };

  const lees = () => {
    try { return JSON.parse(localStorage.getItem(SLEUTEL)); } catch (e) { return null; }
  };
  const schrijf = (waarde) => {
    try { localStorage.setItem(SLEUTEL, JSON.stringify(waarde)); } catch (e) { /* privémodus */ }
  };

  const toepassen = (keuze) => {
    window.madegroToestemming = keuze;
    document.dispatchEvent(new CustomEvent('madegro:toestemming', { detail: keuze }));
  };

  const sluit = (keuze) => {
    schrijf({ ...keuze, moment: new Date().toISOString() });
    toepassen(keuze);
    balk.classList.remove('is-open');
    balk.hidden = true;
  };

  const toon = () => {
    const opgeslagen = lees();
    schakelaars.analytisch.checked = !!(opgeslagen && opgeslagen.analytisch);
    schakelaars.marketing.checked = !!(opgeslagen && opgeslagen.marketing);
    keuzes.hidden = true;
    balk.hidden = false;
    balk.classList.add('is-open');
  };

  balk.querySelector('[data-cookie="weigeren"]').addEventListener('click', () =>
    sluit({ analytisch: false, marketing: false }));

  balk.querySelector('[data-cookie="toestaan"]').addEventListener('click', () =>
    sluit({ analytisch: true, marketing: true }));

  /* 'Aanpassen' klapt de keuzes uit; daarna slaat dezelfde knop ze op. */
  const aanpassen = balk.querySelector('[data-cookie="aanpassen"]');
  aanpassen.addEventListener('click', () => {
    if (keuzes.hidden) {
      keuzes.hidden = false;
      aanpassen.textContent = 'Opslaan';
      schakelaars.analytisch.focus();
      return;
    }
    sluit({ analytisch: schakelaars.analytisch.checked, marketing: schakelaars.marketing.checked });
  });

  /* Vanaf de cookiepagina kun je je keuze herzien. Via de klik op document,
     omdat de pagina-inhoud bij een overgang vervangen wordt: een knop die
     later in beeld komt werkt zo nog steeds. */
  document.addEventListener('click', (e) => {
    if (!e.target.closest('[data-cookie-instellingen]')) return;
    aanpassen.textContent = 'Opslaan';
    toon();
    keuzes.hidden = false;
  });

  window.madegroCookies = { open: toon, keuze: () => lees() };

  const bestaand = lees();
  if (bestaand) {
    toepassen({ analytisch: !!bestaand.analytisch, marketing: !!bestaand.marketing });
  } else {
    toon();
  }
})();
