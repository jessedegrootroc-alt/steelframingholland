/* ============================================================================
   site.js: gedrag dat op elke pagina hoort
   ----------------------------------------------------------------------------
   De header (palet en verbergen bij scrollen), het mobiele paneel en de
   accordeons. Alles in één functie, zodat het bestand opnieuw uitgevoerd kan
   worden na een pagina-overgang.

   De gids laat maar weinig beweging toe (§9.2): hover, menu's en doorlopend
   transport. Er zit hier dus bewust geen enkele scroll-reveal in.
   ========================================================================== */

(() => {
  /* Tijdens een pagina-overgang staan de oude en de nieuwe pagina even samen in
     de DOM. document.getElementById zou dan het element van de oude pagina
     teruggeven, en dan hangt het gedrag aan een pagina die zo verdwijnt.
     Daarom zoeken we alles binnen de container waar dit script zelf in staat. */
  const container = document.currentScript?.closest('[data-barba="container"]') || document;
  const $ = (kiezer, bron = container) => bron.querySelector(kiezer);

  /* De header en het mobiele paneel staan buiten de container: ze blijven staan
     bij een pagina-overgang omdat ze position:fixed zijn en dus buiten
     #smooth-wrapper moeten liggen. Dit script draait wel opnieuw bij elke
     overgang, dus de listeners van de vorige keer moeten er eerst af. Anders
     opent het menu na drie pagina's ook drie keer.

     window en document worden al opgeruimd door page-transitions.js; het gaat
     hier om de listeners die rechtstreeks op die vaste elementen hangen. */
  window.__madegroVast?.abort();
  window.__madegroVast = new AbortController();
  const vast = { signal: window.__madegroVast.signal };
  const $vast = (kiezer) => document.querySelector(kiezer);

  const gsapAanwezig = window.gsap || null;
  const kalm = window.matchMedia('(prefers-reduced-motion: reduce)');
  const smoother = () => window.MADEGRO?.smoother?.instantie || null;

  /* Met ScrollSmoother loopt de inhoud achter op de scrollbalk. Voor de header
     telt wat je ziet en niet waar de scrollbalk staat, anders wisselt hij van
     kleur voordat de hero uit beeld is. Zonder smoother is dit window.scrollY. */
  const zichtbareScroll = () => {
    const s = smoother();
    return (s && gsapAanwezig) ? -gsapAanwezig.getProperty(s.content(), 'y') : window.scrollY;
  };

  /* ---------------------------------------------------------------- header */
  const header = $vast('#siteHeader');
  const lichteZone = $('[data-header-theme="light"]');

  if (header) {
    let vorigeScroll = zichtbareScroll();
    let grens = 0;

    /* De hoogte van de lichte zone opmeten kost een layout-berekening. Die doen
       we bij een resize en niet bij elk beeldje. */
    const meetGrens = () => {
      grens = lichteZone ? lichteZone.offsetTop + lichteZone.offsetHeight - 80 : 0;
    };

    const werkHeaderBij = () => {
      const nu = zichtbareScroll();

      if (lichteZone) {
        const licht = nu < grens;
        header.classList.toggle('header--light', licht);
        header.classList.toggle('header--scrolled', !licht);
      }

      const omlaag = nu > vorigeScroll && nu > 200;
      header.classList.toggle('header--scroll-hidden', omlaag && !document.body.classList.contains('panel-open'));
      vorigeScroll = nu;
    };

    meetGrens();
    werkHeaderBij();
    window.addEventListener('resize', () => { meetGrens(); werkHeaderBij(); });

    if (gsapAanwezig && !kalm.matches) {
      /* Elk beeldje, want na een sprong in de scrollbalk houdt de scroll-
         gebeurtenis op terwijl de inhoud nog aan het inhalen is. */
      gsapAanwezig.ticker.add(werkHeaderBij);
      window.__madegroVast.signal.addEventListener('abort',
        () => gsapAanwezig.ticker.remove(werkHeaderBij));
    } else {
      window.addEventListener('scroll', werkHeaderBij, { passive: true });
    }
  }

  /* -------------------------------------------------------- mobiel paneel */
  const hamburger = $vast('#hamburger');
  const paneel = $vast('#mobilePanel');
  const paneelOverlay = $vast('#panelOverlay');
  const paneelSluit = $vast('#panelSluit');

  if (hamburger && paneel && paneelOverlay) {
    let vorigeFocus = null;

    const zetPaneel = (open) => {
      paneel.classList.toggle('is-open', open);
      paneelOverlay.hidden = !open;
      /* hidden eerst weg, dan pas de klasse: anders is er geen frame om de
         overgang van de dekking in te zetten. */
      requestAnimationFrame(() => paneelOverlay.classList.toggle('is-open', open));
      hamburger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('panel-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
      /* Met ScrollSmoother staat de scroll niet meer op de body, dus overflow
         hidden houdt de pagina achter het paneel niet meer tegen. De smoother
         pauzeren doet dat wel; zonder smoother blijft overflow het werk doen. */
      smoother()?.paused(open);
      if (open) { vorigeFocus = document.activeElement; paneelSluit.focus(); }
      else if (vorigeFocus) { vorigeFocus.focus(); }
    };

    hamburger.addEventListener('click', () => zetPaneel(true), vast);
    paneelSluit.addEventListener('click', () => zetPaneel(false), vast);
    paneelOverlay.addEventListener('click', () => zetPaneel(false), vast);
    paneel.querySelectorAll('[data-panel-sluit]').forEach((a) =>
      a.addEventListener('click', () => zetPaneel(false), vast));

    /* Tab vasthouden binnen het paneel zolang het open staat. */
    paneel.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab' || !paneel.classList.contains('is-open')) return;
      const bereikbaar = [...paneel.querySelectorAll('a[href], button:not([disabled])')]
        .filter((el) => el.offsetParent !== null);
      if (!bereikbaar.length) return;
      const eerste = bereikbaar[0];
      const laatste = bereikbaar[bereikbaar.length - 1];
      if (e.shiftKey && document.activeElement === eerste) { e.preventDefault(); laatste.focus(); }
      else if (!e.shiftKey && document.activeElement === laatste) { e.preventDefault(); eerste.focus(); }
    }, vast);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && paneel.classList.contains('is-open')) zetPaneel(false);
    });
  }

  /* ------------------------------------------------------------ uitklappers
     De menu-items met sublinks. De knop opent het vlak eronder; met de muis
     gaat het ook op hover open, want dat is wat mensen van zo'n balk verwachten.

     Het gesloten vlak krijgt inert: dan staan de links er wel voor een
     zoekmachine maar vang je ze niet met de tab-toets. */
  const triggers = [...document.querySelectorAll('[data-uitklap]')];
  const panelen = new Map(
    [...document.querySelectorAll('[data-uitklap-paneel]')].map((el) => [el.dataset.uitklapPaneel, el]));

  if (triggers.length) {
    const zet = (id, open) => {
      const trigger = triggers.find((t) => t.dataset.uitklap === id);
      const paneel = panelen.get(id);
      if (!trigger || !paneel) return;
      trigger.setAttribute('aria-expanded', String(open));
      paneel.classList.toggle('is-open', open);
      if (open) paneel.removeAttribute('inert');
      else paneel.setAttribute('inert', '');
    };

    const sluitAlles = () => triggers.forEach((t) => zet(t.dataset.uitklap, false));

    /* Bij een pagina-overgang blijft de header staan en draait dit script
       opnieuw; een vlak dat nog openstond gaat hier dicht. */
    sluitAlles();

    triggers.forEach((trigger) => {
      const id = trigger.dataset.uitklap;

      trigger.addEventListener('click', () => {
        const open = trigger.getAttribute('aria-expanded') === 'true';
        sluitAlles();
        zet(id, !open);
      }, vast);

      /* Alleen met een muis; op een aanraakscherm zou hover meteen na de tik
         afgaan en het vlak weer sluiten. */
      trigger.addEventListener('pointerenter', (e) => {
        if (e.pointerType !== 'mouse') return;
        sluitAlles();
        zet(id, true);
      }, vast);

      panelen.get(id)?.addEventListener('pointerleave', (e) => {
        if (e.pointerType === 'mouse') zet(id, false);
      }, vast);
    });

    header?.addEventListener('pointerleave', (e) => {
      if (e.pointerType !== 'mouse') return;
      /* Niet sluiten als de muis het vlak zelf in gaat: dat hangt onder de balk. */
      const naar = e.relatedTarget;
      if (naar && [...panelen.values()].some((p) => p.contains(naar))) return;
      sluitAlles();
    }, vast);

    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape') return;
      const open = triggers.find((t) => t.getAttribute('aria-expanded') === 'true');
      if (!open) return;
      sluitAlles();
      open.focus();
    });

    document.addEventListener('focusin', (e) => {
      if (header?.contains(e.target)) return;
      sluitAlles();
    });

    document.addEventListener('click', (e) => {
      if (header?.contains(e.target)) return;
      sluitAlles();
    });

    /* De balk schuift bij naar beneden scrollen omhoog uit beeld; een open vlak
       zou dan meegaan en half over de pagina hangen. */
    window.addEventListener('scroll', () => {
      if (triggers.some((t) => t.getAttribute('aria-expanded') === 'true')) sluitAlles();
    }, { passive: true });
  }

  /* ------------------------------------------------- uitklappers in het paneel */
  const mobieleTriggers = [...document.querySelectorAll('[data-mobiel-uitklap]')];
  mobieleTriggers.forEach((knop) => {
    const lijst = document.getElementById(knop.getAttribute('aria-controls'));
    if (!lijst) return;
    knop.addEventListener('click', () => {
      const open = knop.getAttribute('aria-expanded') === 'true';
      knop.setAttribute('aria-expanded', String(!open));
      if (open) {
        lijst.style.height = lijst.scrollHeight + 'px';
        requestAnimationFrame(() => { lijst.style.height = '0px'; });
        lijst.addEventListener('transitionend', () => { lijst.hidden = true; }, { once: true });
      } else {
        lijst.hidden = false;
        lijst.style.height = lijst.scrollHeight + 'px';
      }
    }, vast);
  });

  /* -------------------------------------------------------------- logoband
     De logo's staan in data-src. Ze worden pas opgehaald als de band in de
     buurt van het scherm komt, want hij staat altijd onderaan de pagina en de
     dertien logo's samen zijn 118 kB.

     rootMargin 600px: ze zijn binnen voordat je ze ziet. Alle 26 tegelijk, want
     halverwege inladen geeft gaten in de lopende band.

     loading="lazy" doet het hier niet, dat is gemeten: het venster knipt af met
     overflow:hidden en dan blijven de meeste logo's voor de browser buiten
     beeld, ook als je erlangs scrollt. Van de 26 laadden er drie.

     Zonder IntersectionObserver, of zonder JavaScript, staat er een noscript met
     dezelfde reeks en een gewone src; dan is de band er meteen. */
  container.querySelectorAll('[data-logoband]').forEach((band) => {
    const zetAan = () => band.querySelectorAll('img[data-src]').forEach((img) => {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
    });

    if (!('IntersectionObserver' in window)) return zetAan();

    const waarnemer = new IntersectionObserver((invoer) => {
      if (!invoer.some((i) => i.isIntersecting)) return;
      zetAan();
      waarnemer.disconnect();
    }, { rootMargin: '600px 0px' });
    waarnemer.observe(band);
  });

  /* ---------------------------------------------------------------- quotes
     Eén citaat tegelijk in beeld. De rest staat er met hidden bij: zo staan ze
     allemaal in de broncode voor een zoekmachine, en werkt de sectie zonder
     JavaScript als een gewone lijst citaten onder elkaar.

     Dat laatste is de reden dat de knoppen hier pas verschijnen als dit script
     draait: zonder script zou je op pijlen klikken die niets doen. */
  /* ------------------------------------------------------------ herovideo --
     De film hangt niet in de HTML maar wordt hier pas ingehangen. Reden: het is
     anderhalve megabyte, en er zijn drie gevallen waarin je die beter niet
     ophaalt. Zonder JavaScript gebeurt er dus niets en blijft het bij de foto,
     die het eerste beeldje van dezelfde film is.

     Er is geen grens op schermbreedte meer; de film speelt ook op een telefoon.
     Die stond hier eerst wel (768, later 600px), maar breedte zegt niets over
     de verbinding: een telefoon op wifi kan het prima aan, een laptop op een
     hotspot niet. De twee regels over de lijn hieronder maken dat onderscheid
     wel, en die blijven. Het bestand blijft dezelfde 1,5 MB op elk scherm: op
     een staande telefoon wordt van de 16:9-film maar het middelste kwart
     gebruikt, dus een kleinere versie zou daar juist het snelst onscherp worden.

     Pas zichtbaar bij 'playing' en niet bij 'canplay': weigert de browser het
     automatisch afspelen -- dat mag hij -- dan blijft de foto staan in plaats
     van een stilstaand eerste beeldje. */
  container.querySelectorAll('[data-herovideo]').forEach((video) => {
    if (kalm.matches) return;                                   // beweging uit
    if (navigator.connection?.saveData) return;                 // databesparing aan
    if (/^(slow-)?2g$/.test(navigator.connection?.effectiveType || '')) return;  // trage lijn

    const bron = document.createElement('source');
    bron.src = video.dataset.herovideo;
    bron.type = 'video/mp4';
    video.appendChild(bron);
    video.addEventListener('playing', () => video.classList.add('is-zichtbaar'), { once: true });
    video.load();
    video.play().catch(() => {});

    /* Op een telefoon zet de browser de film stil zodra je naar een andere app
       of een ander tabblad gaat, en niet elke browser zet hem weer aan als je
       terugkomt. Dan sta je op een bevroren beeldje. Dus bij terugkomst nog een
       keer play(); weigert de browser dat, dan blijft het stil en is er niets
       kapot. De listener hangt aan het document en gaat mee weg met de rest van
       deze pagina via het signaal. */
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'visible' && video.paused && video.isConnected) {
        video.play().catch(() => {});
      }
    }, { signal: window.__madegroVast?.signal });
  });

  /* Hoe lang een citaat blijft staan, in milliseconden. Het balkje in de
     navigatie loopt op dezelfde waarde, dus dit is de enige plek die je hoeft
     te wijzigen als het sneller of langzamer moet. */
  const QUOTE_DUUR = 2800;

  container.querySelectorAll('[data-quoteslider]').forEach((venster) => {
    const dias = [...venster.querySelectorAll('.quote')];
    if (dias.length < 2) return;

    const sectie = venster.closest('.quotes');
    const teller = sectie?.querySelector('[data-quote-teller]');
    const nav = sectie?.querySelector('.quotes__nav');
    const balkje = sectie?.querySelector('[data-quote-voortgang]');
    const vulling = balkje?.querySelector('span');
    if (nav) nav.hidden = false;

    /* Deze klasse legt de citaten in de stylesheet op elkaar in één rastervak.
       De sectie is dan altijd zo hoog als het langste citaat en de pijlen
       eronder blijven staan waar ze staan; zonder deze klasse verspringen ze,
       want het ene citaat is drie regels en het andere vier. Hij wordt hier
       gezet en niet in de HTML, omdat de opmaak alleen klopt als dit script
       ook echt draait: zonder script staan de citaten onder elkaar. */
    venster.classList.add('quotes__venster--slider');
    let nu = 0;

    const toon = (i) => {
      nu = (i + dias.length) % dias.length;
      dias.forEach((d, n) => { d.hidden = n !== nu; });
      if (teller) teller.textContent = `${nu + 1} / ${dias.length}`;
    };

    toon(0);

    sectie?.querySelectorAll('[data-quote]').forEach((knop) => {
      knop.addEventListener('click', () => {
        stop();                       // wie zelf bladert, bladert verder zelf
        toon(nu + (knop.dataset.quote === 'volgende' ? 1 : -1));
      });
    });

    /* ---------------------------------------------------------- doorlopen --
       De citaten lopen zelf door, met het balkje in de navigatie als aanduiding
       van hoe lang er nog staat.

       Drie keer gaat dat niet aan of gaat het uit:

         1. Bij 'beweging uit' begint het niet. Tekst die zichzelf verwisselt is
            dan ongewenst, en een balkje dat leegloopt zegt niets meer.
         2. Zolang de muis erop staat of er iets in de sectie focus heeft, staat
            het stil. Anders schuift een citaat weg terwijl je het leest, of
            terwijl je met de tab-toets bij de pijlen bent.
         3. Zodra iemand zelf op een pijl klikt, stopt het voorgoed en verdwijnt
            het balkje. Dat is ook wat WCAG 2.2.2 vraagt: er moet een manier
            zijn om bewegende inhoud te stoppen, en de pijlen zijn die manier.

       Bij hervatten beginnen het balkje en de teller samen opnieuw, in plaats
       van verder te lopen waar ze waren. Anders lopen de twee uit elkaar: een
       setTimeout weet niet hoeveel tijd er al verstreken was. */
    let timer = null;
    let gestopt = kalm.matches;

    const balkOpnieuw = () => {
      if (!vulling) return;
      vulling.style.animation = 'none';
      void vulling.offsetWidth;                       // forceert een herstart
      vulling.style.animation = `quote-voortgang ${QUOTE_DUUR}ms linear forwards`;
    };

    const plan = () => {
      timer = setTimeout(() => { toon(nu + 1); start(); }, QUOTE_DUUR);
    };

    const start = () => {
      if (gestopt) return;
      clearTimeout(timer);
      balkOpnieuw();
      plan();
    };

    const pauze = () => {
      clearTimeout(timer);
      timer = null;
      if (vulling) vulling.style.animationPlayState = 'paused';
    };

    function stop() {
      gestopt = true;
      clearTimeout(timer);
      timer = null;
      if (balkje) balkje.hidden = true;
    }

    if (!gestopt) {
      if (balkje) balkje.hidden = false;
      start();

      sectie.addEventListener('mouseenter', pauze);
      sectie.addEventListener('mouseleave', () => { if (!gestopt) start(); });
      sectie.addEventListener('focusin', pauze);
      sectie.addEventListener('focusout', () => { if (!gestopt) start(); });
      // Een tabblad op de achtergrond hoeft niet door te tikken.
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) pauze();
        else if (!gestopt) start();
      });
    }
  });

  /* ------------------------------------------------------------ accordeons */
  container.querySelectorAll('.accordion').forEach((lijst) => {
    lijst.addEventListener('click', (e) => {
      const knop = e.target.closest('.accordion__header');
      if (!knop) return;
      const item = knop.closest('.accordion__item');
      const details = item.querySelector('.accordion__details');
      const open = item.classList.toggle('open');
      knop.setAttribute('aria-expanded', String(open));
      details.style.height = open ? details.scrollHeight + 'px' : '0px';
    });
  });

  /* Bij het verspringen van de kolommen verandert de hoogte van een open
     antwoord; anders wordt de tekst afgekapt. */
  window.addEventListener('resize', () => {
    container.querySelectorAll('.accordion__item.open .accordion__details')
      .forEach((d) => { d.style.height = d.scrollHeight + 'px'; });
  });
})();
