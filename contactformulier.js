/* ============================================================================
   contactformulier.js: het contactformulier, één keer
   ----------------------------------------------------------------------------
   Het formulier komt op bijna elke pagina terug. In plaats van dezelfde honderd
   regels HTML dertien keer te herhalen, staat het hier één keer en rendert het
   zich in elke <div data-contactformulier data-onderwerp="…"> op de pagina.

   Voor bezoekers zonder JavaScript staat er in de HTML een <noscript> met het
   e-mailadres en telefoonnummer, zodat de pagina bruikbaar blijft.

   Alles zit in één functie, zodat het bestand ook opnieuw uitgevoerd kan worden
   na een pagina-overgang (zie page-transitions.js).
   ========================================================================== */

(() => {
  /* Tijdens een pagina-overgang staan de oude en de nieuwe pagina even samen in
     de DOM. document.getElementById zou dan het element van de oude pagina
     teruggeven, en dan hangt het gedrag aan een pagina die zo verdwijnt.
     Daarom zoeken we alles binnen de container waar dit script zelf in staat. */
  const container = document.currentScript?.closest('[data-barba="container"]') || document;

  const ONDERWERPEN = [
    ['verbouwing', 'Verbouwing'],
    ['fundering', 'Fundering'],
    ['nieuwbouw', 'Nieuwbouw'],
    ['schaderapportage', 'Schaderapportage of deskundigenadvies'],
    ['offerte', 'Offerteaanvraag'],
    ['overig', 'Overig'],
  ];

  /* TODO-CONTENT: waar moet de inzending naartoe? Zolang dit niet gekoppeld is,
     laat het formulier zien dat het verstuurd is, maar gaat er niets de deur
     uit. Zet hieronder het endpoint of de formulierdienst neer. */
  const ENDPOINT = '';

  /* Het offerteformulier van de bronsite vraagt om bijlagen: vijf velden met
     samen maximaal 20 MB. Die grens staat hier, zodat hij op één plek klopt met
     de tekst die eronder op de pagina staat. */
  const BIJLAGEN = 5;
  const MAX_MB = 20;

  /* Spamcontrole loopt via het onzichtbare honeypotveld onderaan dit formulier.
     De bronsite gebruikt daar Google reCAPTCHA voor; dat is hier bewust niet
     overgenomen, want dat laadt een script van een derde partij en dan hoort er
     ook een vermelding in de privacy- en cookieverklaring bij. */

  async function submitContactForm(payload) {
    // TODO: koppel aan endpoint (eigen backend of formulierdienst)
    if (!ENDPOINT) {
      console.info('Contactformulier nog niet gekoppeld. Inzending:', payload);
      return { ok: true, gekoppeld: false };
    }
    const antwoord = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload),
    });
    return { ok: antwoord.ok, gekoppeld: true };
  }
  window.submitContactForm = submitContactForm;

  const VELDEN = [
    { naam: 'naam',    label: 'Naam',        type: 'text',  autocomplete: 'name',              verplicht: true },
    { naam: 'bedrijf', label: 'Bedrijfsnaam', type: 'text', autocomplete: 'organization',      verplicht: false },
    { naam: 'email',   label: 'E-mailadres', type: 'email', autocomplete: 'email',             verplicht: true },
    { naam: 'telefoon', label: 'Telefoonnummer', type: 'tel', autocomplete: 'tel',             verplicht: false },
  ];

  const fout = {
    naam: 'Vul uw naam in.',
    email: 'Vul een geldig e-mailadres in.',
    telefoon: 'Vul een geldig telefoonnummer in, of laat het veld leeg.',
    bericht: 'Schrijf kort waar het over gaat.',
    bijlagen: `De bestanden zijn samen groter dan ${MAX_MB} MB. Stuur ze per mail of via een verzenddienst.`,
    akkoord: 'U moet akkoord gaan met het privacybeleid.',
  };

  const geldigEmail = (waarde) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(waarde.trim());
  const geldigTelefoon = (waarde) => waarde.trim() === '' || /^[+\d][\d\s().-]{7,}$/.test(waarde.trim());

  const bouw = (houder) => {
    const gekozen = houder.dataset.onderwerp || 'overig';
    const id = 'cf-' + Math.abs(gekozen.split('').reduce((a, c) => a + c.charCodeAt(0), 0)) + '-' + houder.dataset.index;

    const velden = VELDEN.map((v) => `
      <div class="veld">
        <label class="field__label" for="${id}-${v.naam}">${v.label}${v.verplicht ? ' *' : ''}</label>
        <input class="field" id="${id}-${v.naam}" name="${v.naam}" type="${v.type}"
               autocomplete="${v.autocomplete}"${v.verplicht ? ' required' : ''}
               aria-describedby="${id}-${v.naam}-fout">
        <p class="veld__fout" id="${id}-${v.naam}-fout" hidden></p>
      </div>`).join('');

    const projectadres = houder.hasAttribute('data-projectadres') ? `
        <div class="veld">
          <label class="field__label" for="${id}-projectadres">Projectadres (indien van toepassing)</label>
          <input class="field" id="${id}-projectadres" name="projectadres" type="text"
                 autocomplete="street-address">
        </div>` : '';

    /* Bijlagen. type="file" met multiple zou hetzelfde kunnen, maar de bronsite
       heeft vijf losse velden en dat is voor wie een tekening, een berekening en
       een foto los aanlevert overzichtelijker. */
    const bijlagen = houder.hasAttribute('data-bijlagen') ? `
        <fieldset class="veld-groep">
          <legend class="veld-groep__kop">De gezamenlijke grootte van onderstaande bestanden mag niet meer zijn dan ${MAX_MB}MB</legend>
          ${Array.from({ length: BIJLAGEN }, (_, i) => `
          <div class="veld">
            <label class="field__label" for="${id}-bestand-${i}">Bestand</label>
            <input class="field field--bestand" type="file" id="${id}-bestand-${i}" name="bestand${i}">
          </div>`).join('')}
          <p class="veld__fout" id="${id}-bijlagen-fout" hidden></p>
        </fieldset>` : '';

    const opties = ONDERWERPEN.map(([waarde, label]) =>
      `<option value="${waarde}"${waarde === gekozen ? ' selected' : ''}>${label}</option>`).join('');

    houder.innerHTML = `
      <form class="contactformulier" novalidate>
        <div class="veld-rij">
          ${velden}
        </div>

        <div class="veld">
          <label class="field__label" for="${id}-onderwerp">Waar gaat het over?</label>
          <select class="field" id="${id}-onderwerp" name="onderwerp">${opties}</select>
        </div>
        ${projectadres}

        <div class="veld">
          <label class="field__label" for="${id}-bericht">${houder.hasAttribute('data-projectadres') ? 'Vraag of opdrachtomschrijving' : 'Bericht'} *</label>
          <textarea class="field" id="${id}-bericht" name="bericht" rows="6" required
                    aria-describedby="${id}-bericht-fout"></textarea>
          <p class="veld__fout" id="${id}-bericht-fout" hidden></p>
        </div>

        ${bijlagen}

        <div class="veld">
          <label class="akkoord">
            <input type="checkbox" id="${id}-akkoord" name="akkoord" required
                   aria-describedby="${id}-akkoord-fout">
            <span>Ik ga akkoord met het <a href="privacybeleid.html">privacybeleid</a> *</span>
          </label>
          <p class="veld__fout" id="${id}-akkoord-fout" hidden></p>
        </div>

        <!-- Onzichtbaar veld tegen spambots: mensen zien het niet, bots vullen het in. -->
        <input type="text" name="_bericht_extra" tabindex="-1" autocomplete="off"
               aria-hidden="true" class="honeypot">

        <div class="contactformulier__voet">
          <button type="submit" class="button button--primary"><span class="button__inhoud">Versturen<span class="button__spoor" aria-hidden="true"><svg class="arrow--animation is-1" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 4.6 20.6 12l-7.4 7.4-1.4-1.4 5-5H3.4v-2h13.4l-5-5 1.4-1.4Z"/></svg><svg class="arrow--animation is-2" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M13.2 4.6 20.6 12l-7.4 7.4-1.4-1.4 5-5H3.4v-2h13.4l-5-5 1.4-1.4Z"/></svg></span></span></button>
        </div>

        <p class="contactformulier__melding" role="status" aria-live="polite"></p>
      </form>`;

    const form = houder.querySelector('form');
    const melding = houder.querySelector('.contactformulier__melding');

    const toonFout = (veld, tekst) => {
      const doel = form.elements[veld];
      const regel = houder.querySelector(`#${id}-${veld}-fout`);
      if (!doel || !regel) return;
      if (tekst) {
        regel.textContent = tekst;
        regel.hidden = false;
        doel.setAttribute('aria-invalid', 'true');
      } else {
        regel.hidden = true;
        doel.removeAttribute('aria-invalid');
      }
    };

    const controleer = () => {
      const w = (naam) => (form.elements[naam]?.value || '').trim();
      const fouten = [];
      if (!w('naam')) fouten.push(['naam', fout.naam]);
      if (!geldigEmail(w('email'))) fouten.push(['email', fout.email]);
      if (!geldigTelefoon(w('telefoon'))) fouten.push(['telefoon', fout.telefoon]);
      if (w('bericht').length < 5) fouten.push(['bericht', fout.bericht]);
      if (!form.elements.akkoord.checked) fouten.push(['akkoord', fout.akkoord]);

      /* De gezamenlijke grootte van de bijlagen, zoals de bronsite die stelt.
         De regel eronder op de pagina verwijst voor grotere bestanden naar de
         mail; die melding komt hier terug als het te veel wordt. */
      const bestanden = [...form.querySelectorAll('input[type="file"]')]
        .flatMap((v) => [...(v.files || [])]);
      const totaal = bestanden.reduce((som, b) => som + b.size, 0);
      const regelBijlagen = houder.querySelector(`#${id}-bijlagen-fout`);
      if (regelBijlagen) {
        const teGroot = totaal > MAX_MB * 1024 * 1024;
        regelBijlagen.textContent = teGroot ? fout.bijlagen : '';
        regelBijlagen.hidden = !teGroot;
        if (teGroot) fouten.push(['bestand0', fout.bijlagen]);
      }

      ['naam', 'email', 'telefoon', 'bericht', 'akkoord'].forEach((veld) => toonFout(veld, null));
      fouten.forEach(([veld, tekst]) => toonFout(veld, tekst));
      return fouten;
    };

    /* Pas controleren zodra iemand een veld verlaat: tijdens het typen
       foutmeldingen tonen leest als vitten. */
    form.addEventListener('blur', (e) => {
      if (e.target.name && e.target.getAttribute('aria-invalid')) controleer();
    }, true);

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fouten = controleer();

      if (fouten.length) {
        melding.textContent = fouten.length === 1
          ? 'Er staat nog iets open in het formulier.'
          : `Er staan nog ${fouten.length} dingen open in het formulier.`;
        melding.className = 'contactformulier__melding is-fout';
        form.elements[fouten[0][0]].focus();
        return;
      }

      /* Honeypot ingevuld: doen alsof het gelukt is en niets versturen. */
      if (form.elements._bericht_extra.value) {
        melding.textContent = 'Bedankt, uw bericht is verstuurd.';
        melding.className = 'contactformulier__melding is-goed';
        return;
      }

      const knop = form.querySelector('button[type="submit"]');
      knop.disabled = true;
      const oudeTekst = knop.textContent;
      knop.textContent = 'Versturen…';

      try {
        const payload = {
          naam: form.elements.naam.value.trim(),
          projectadres: form.elements.projectadres?.value.trim() || '',
          bedrijf: form.elements.bedrijf.value.trim(),
          email: form.elements.email.value.trim(),
          telefoon: form.elements.telefoon.value.trim(),
          onderwerp: form.elements.onderwerp.value,
          bericht: form.elements.bericht.value.trim(),
        };
        const { ok } = await submitContactForm(payload);
        if (!ok) throw new Error('verzenden mislukt');

        form.reset();
        /* Geen termijn beloven die de bronsite niet noemt. De contactpagina van de
           bronsite zegt "zo spoedig mogelijk"; die formulering staat hier ook. */
        melding.textContent = 'Bedankt, uw bericht is binnen. Wij nemen zo spoedig mogelijk contact met u op.';
        melding.className = 'contactformulier__melding is-goed';
      } catch (err) {
        melding.textContent = 'Het versturen lukte niet. Mail ons op info@madegro.nl of bel 0184 00 00 00.';
        melding.className = 'contactformulier__melding is-fout';
      } finally {
        knop.disabled = false;
        knop.textContent = oudeTekst;
      }
    });
  };

  container.querySelectorAll('[data-contactformulier]').forEach((houder, i) => {
    houder.dataset.index = i;
    bouw(houder);
  });
})();
