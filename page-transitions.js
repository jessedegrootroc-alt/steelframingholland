/* ---- Pagina-overgangen met Barba.js en GSAP ----

   In plaats van de hele pagina te herladen, wisselt Barba alleen het blok met
   data-barba="container" om. Daardoor kunnen de oude en de nieuwe pagina even
   naast elkaar bestaan en kun je ze samen animeren.

   De overgang hieronder heet 'default-transition' en draait in sync-modus: de
   huidige pagina schaalt terug en vervaagt, terwijl de nieuwe pagina er vanaf
   de onderkant overheen schuift met een clip-path.

   Wat dit bestand verder regelt, omdat de site uit losse HTML-pagina's bestaat:
   - de paginastijlen in de <head> (gemarkeerd met data-page-css) wisselen mee;
   - de scripts van de nieuwe pagina worden opnieuw uitgevoerd;
   - titel, omschrijving, canonical en de klassen op <body> lopen mee;
   - de scrollpositie gaat naar boven, of naar het anker uit de link.

   Laadt Barba of GSAP niet, dan gebeurt hier niets en navigeert de site
   gewoon op de normale manier.                                              */

(() => {
  const { barba, gsap } = window;
  if (!barba || !gsap) return;

  /* Alle tijden en afstanden op één plek, zodat je de overgang hier bijstelt.

     DUUR is de hele overgang van begin tot eind. De stappen eronder lopen over
     elkaar heen en worden uitgedrukt als deel van die duur; verhoog of verlaag
     DUUR en de verhouding blijft kloppen. */
  const DUUR         = 0.3;   // totale duur van de overgang, in seconden
  const SCHAAL_UIT   = 0.9;   // hoever de huidige pagina terugschaalt
  const SCHAAL_IN    = 0.82;  // waar de nieuwe pagina vandaan komt
  const DOOFT_TOT    = 0.45;  // hoe ver de huidige pagina wegvalt
  const PARALLAX     = 0.05;  // deel van de schermhoogte dat de oude inhoud meeschuift
  const DUUR_KALM    = 0.2;   // overvloeier voor wie beweging heeft uitgezet

  const barbaWrapper = document.querySelector('[data-barba="wrapper"]');
  const schermHoogte = () => window.innerHeight || document.documentElement.clientHeight || 800;
  const kalm = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ================= Paginastijlen wisselen =================
     De <head> blijft staan bij een overgang, dus de stijlen die bij één
     pagina horen moeten we zelf meenemen. Ze zijn gemarkeerd met
     data-page-css="naam". Wat de nieuwe pagina nodig heeft zetten we erbij;
     wat alleen bij de oude hoorde ruimen we op zodra de overgang klaar is. */
  const wisselPaginaStijlen = (nieuweDocument) => {
    const huidig  = [...document.head.querySelectorAll('[data-page-css]')];
    const gewenst = [...nieuweDocument.head.querySelectorAll('[data-page-css]')];
    const namen   = gewenst.map((el) => el.dataset.pageCss);

    const wachten = gewenst
      .filter((el) => !huidig.some((h) => h.dataset.pageCss === el.dataset.pageCss))
      .map((el) => new Promise((klaar) => {
        const kopie = document.importNode(el, true);
        /* Een <link> moet eerst geladen zijn, anders zie je de nieuwe pagina
           een moment zonder opmaak. Een <style> geldt meteen. */
        if (kopie.tagName === 'LINK') {
          kopie.addEventListener('load', klaar, { once: true });
          kopie.addEventListener('error', klaar, { once: true });
          document.head.appendChild(kopie);
        } else {
          document.head.appendChild(kopie);
          klaar();
        }
      }));

    return {
      geladen: Promise.all(wachten),
      opruimen: () => huidig
        .filter((el) => !namen.includes(el.dataset.pageCss))
        .forEach((el) => el.remove()),
    };
  };

  /* ================= Kop van het document bijwerken =================
     Barba zet de titel al goed; de rest doen we hier, zodat een gedeelde link
     of de terugknop dezelfde gegevens houdt als bij een normale paginalading. */
  const werkKopBij = (nieuweDocument) => {
    document.body.className = nieuweDocument.body.className;

    /* De header staat buiten de container omdat hij position:fixed is en dus
       buiten #smooth-wrapper moet liggen. Hij wisselt daardoor niet mee, dus
       zetten we zelf over welke menulink de huidige pagina is. */
    const bronLinks = [...nieuweDocument.querySelectorAll('#siteHeader .submenu--link')];
    const doelLinks = [...document.querySelectorAll('#siteHeader .submenu--link')];
    if (bronLinks.length === doelLinks.length) {
      doelLinks.forEach((link, i) => {
        link.className = bronLinks[i].className;
        if (bronLinks[i].hasAttribute('aria-current')) link.setAttribute('aria-current', 'page');
        else link.removeAttribute('aria-current');
      });
    }

    [
      ['meta[name="description"]', 'content'],
      ['meta[name="robots"]', 'content'],
      ['meta[property="og:title"]', 'content'],
      ['meta[property="og:description"]', 'content'],
      ['meta[property="og:url"]', 'content'],
      ['link[rel="canonical"]', 'href'],
    ].forEach(([kiezer, eigenschap]) => {
      const bron = nieuweDocument.querySelector(kiezer);
      const doel = document.querySelector(kiezer);
      if (bron && doel) doel.setAttribute(eigenschap, bron.getAttribute(eigenschap));
    });
  };

  /* ================= Scripts van de nieuwe pagina =================
     Een script dat met de container meekomt draait niet vanzelf: de browser
     voert alleen scripts uit die als echt script-element in de pagina worden
     gezet. Dat doen we hier alsnog.

     Twee dingen vangen we daarbij op:
     - de code komt in een eigen functie te staan, zodat een const op het
       hoogste niveau niet botst met dezelfde const van de vorige keer;
     - listeners op window en document krijgen stilletjes een signal mee, zodat
       ze verdwijnen zodra je de pagina weer verlaat en er niets opstapelt. */
  let paginaAfbreker = null;

  const voerPaginaScriptsUit = (container) => {
    if (paginaAfbreker) paginaAfbreker.abort();
    paginaAfbreker = new AbortController();
    const signal = paginaAfbreker.signal;

    const origineelWindow = window.addEventListener;
    const origineelDocument = document.addEventListener;
    const metSignaal = (doel, origineel) => function (soort, functie, opties) {
      const uitgebreid = (opties && typeof opties === 'object')
        ? { ...opties, signal: opties.signal || signal }
        : { capture: !!opties, signal };
      return origineel.call(doel, soort, functie, uitgebreid);
    };

    window.addEventListener = metSignaal(window, origineelWindow);
    document.addEventListener = metSignaal(document, origineelDocument);

    try {
      container.querySelectorAll('script').forEach((oud) => {
        const nieuw = document.createElement('script');
        [...oud.attributes].forEach((attr) => nieuw.setAttribute(attr.name, attr.value));
        if (!oud.src) nieuw.textContent = `(function () {\n${oud.textContent}\n})();`;
        oud.replaceWith(nieuw);
      });
    } finally {
      window.addEventListener = origineelWindow;
      document.addEventListener = origineelDocument;
    }
  };

  /* ================= Scrollpositie =================
     Zonder herlading blijft de browser staan waar hij stond, dus dat regelen
     we zelf:
     - kwam je hier via de terugknop, dan ga je terug naar waar je was;
     - wees de link naar een anker (./#diensten), dan springen we daarheen;
     - anders begin je gewoon bovenaan.

     Barba houdt de hash niet vast in data.next.url, dus die halen we uit de
     link waarop geklikt is. */
  /* De browser bewaart zelf ook een scrollpositie per stap in de geschiedenis en
     zet die terug bij de terug- en vooruitknop. Bij een gewone site is dat
     precies goed, hier niet: Barba wisselt alleen de inhoud om, dus de browser
     zet zijn positie terug op een pagina die nog niet staat, en daarna zetten
     wij hem nog een keer. Die twee liepen door elkaar heen. Zichtbaar bij de
     vooruitknop: die kwam uit op de stand van de vórige pagina.

     Met 'manual' laat de browser het aan ons over. Het geheugen hieronder doet
     het werk, en dat weet wel welke stand bij welke pagina hoort. */
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  const scrollGeheugen = new Map();

  const haalHash = (aanleiding) => {
    if (!aanleiding || typeof aanleiding === 'string') return '';
    try {
      return new URL(aanleiding.href, location.href).hash;
    } catch (e) {
      return '';
    }
  };

  const zetScroll = (data) => {
    const viaGeschiedenis = typeof data.trigger === 'string';
    const onthouden = scrollGeheugen.get(data.next.url.path);

    if (viaGeschiedenis && typeof onthouden === 'number') {
      window.scrollTo(0, onthouden);
      return;
    }

    const hash = haalHash(data.trigger);
    const anker = hash ? document.getElementById(hash.slice(1)) : null;
    if (anker) {
      anker.scrollIntoView({ behavior: 'instant', block: 'start' });
      /* De hash weer in de adresbalk zetten, zodat een verversing of een
         gedeelde link op dezelfde plek uitkomt. */
      history.replaceState(history.state, '', location.pathname + hash);
      return;
    }

    window.scrollTo(0, 0);
  };

  barba.init({
    /* Eén overgang tegelijk; een tweede klik wordt genegeerd. */
    preventRunning: true,

    /* Wat Barba met rust laat: ankers op dezelfde pagina, mailto, downloads,
       links naar een ander tabblad en alles buiten deze site. */
    prevent: ({ el }) => {
      const href = el.getAttribute('href') || '';
      if (!href || href.startsWith('#')) return true;
      if (/^(mailto:|tel:|javascript:)/i.test(href)) return true;
      if (el.hasAttribute('download') || el.target === '_blank') return true;
      try {
        return new URL(el.href, location.href).origin !== location.origin;
      } catch (e) {
        return true;
      }
    },

    transitions: [
      {
        name: 'default-transition',
        sync: true,

        /* ---- Beginstand ----
           De nieuwe pagina ligt klaar bovenop de oude: verkleind en volledig
           weggeknipt met een clip-path. De oude pagina zetten we vast op de
           plek waar je nu kijkt, zodat hij niet naar boven springt zodra hij
           uit de flow gehaald wordt. */
        before: async (data) => {
          barbaWrapper.classList.add('is__transitioning');

          /* De overgang zet beide containers op position:fixed. Onder de
             transform van ScrollSmoother zou fixed aan de inhoud hangen in
             plaats van aan het scherm, dus de smoother gaat er even af. In
             'after' wordt hij opnieuw opgebouwd. De scrollbalk zelf is de
             echte van de browser, dus window.scrollY klopt hierna gewoon. */
          /* Eerst opmeten waar we staan, daarna pas slopen. De smoother weet dat
             zelf het beste: hij houdt zijn eigen stand bij en die overleeft een
             kill(), terwijl window.scrollY daarna een oude waarde kan geven.
             Dat was te zien bij de vooruitknop, die op de stand van de vorige
             pagina uitkwam. */
          const smoother = window.MADEGRO?.smoother?.instantie;
          const scroll = smoother ? Math.round(smoother.scrollTop()) : window.scrollY;
          scrollGeheugen.set(data.current.url.path, scroll);

          window.MADEGRO?.smoother?.sloop();
          window.scrollTo(0, scroll);

          /* Barba geeft de opgehaalde pagina als tekst mee; hieruit halen we
             de stijlen en de gegevens uit de <head>. */
          data.nieuweDocument = new DOMParser().parseFromString(data.next.html, 'text/html');

          const stijlen = wisselPaginaStijlen(data.nieuweDocument);
          data.opruimenStijlen = stijlen.opruimen;

          gsap.set(data.current.container, {
            position: 'fixed',
            top: -scroll,
            left: 0,
            right: 0,
            zIndex: 2,
            /* Terugschalen rondom het midden van wat je ziet, niet rondom het
               midden van de hele lange pagina. */
            transformOrigin: `50% ${scroll + schermHoogte() / 2}px`,
            willChange: 'transform, opacity',
          });

          gsap.set(data.next.container, {
            position: 'fixed',
            inset: 0,
            overflow: 'hidden',
            scale: kalm.matches ? 1 : SCHAAL_IN,
            opacity: kalm.matches ? 0 : 1,
            clipPath: kalm.matches ? 'inset(0% 0 0 0)' : 'inset(100% 0 0 0)',
            zIndex: 3,
            willChange: 'transform, clip-path',
          });

          /* De nieuwe pagina bouwt zichzelf deels met JavaScript op (marquee,
             reviews, faq). Die scripts draaien voordat de pagina in beeld
             komt, anders zie je lege blokken tijdens de overgang. */
          voerPaginaScriptsUit(data.next.container);

          await stijlen.geladen;
        },

        /* ---- De overgang zelf ---- */
        enter: (data) => {
          if (kalm.matches) {
            return gsap.to(data.next.container, {
              opacity: 1,
              duration: DUUR_KALM,
              ease: 'none',
            });
          }

          const inhoudHuidig = data.current.container.querySelector('.content__wrapper');

          /* Bij deze snelheid kunnen de drie stappen niet netjes achter elkaar:
             dan is elk stukje zo kort dat je geen beweging meer ziet, alleen
             een sprong. Ze overlappen daarom, met een vaste plek op de tijdlijn
             in plaats van 'volgt op de vorige'. */
          const tl = gsap.timeline({
            defaults: { duration: DUUR * 0.65, ease: 'power3.inOut' },
            onComplete: () => tl.kill(),
          });

          /* De pagina die je verlaat: terugschalen, wegvallen en iets omhoog. */
          tl.to(data.current.container, {
            scale: SCHAAL_UIT,
          }, 0);

          tl.to(data.current.container, {
            opacity: DOOFT_TOT,
            duration: DUUR * 0.7,
            ease: 'power3',
          }, DUUR * 0.2);

          /* Parallax in pixels, niet in procenten: de pagina's hier zijn
             duizenden pixels hoog, en een percentage daarvan zou de halve
             pagina omhoog schuiven. */
          tl.to(inhoudHuidig, {
            y: -Math.round(schermHoogte() * PARALLAX),
            duration: DUUR * 0.7,
            ease: 'power3',
          }, DUUR * 0.2);

          /* De nieuwe pagina schuift van onder naar boven open en zet zich op
             volle grootte. Allebei eindigen ze precies op DUUR. */
          tl.to(data.next.container, {
            clipPath: 'inset(0% 0 0 0)',
            duration: DUUR * 0.8,
            ease: 'power2.out',
          }, DUUR * 0.2);

          tl.to(data.next.container, {
            scale: 1,
            duration: DUUR * 0.7,
            ease: 'power2.out',
          }, DUUR * 0.3);

          return tl.then();
        },

        /* ---- Opruimen ----
           Alle inline stijlen van GSAP eraf, anders staat de nieuwe pagina
           vast op fixed en werkt scrollen niet meer. */
        after: (data) => {
          werkKopBij(data.nieuweDocument);

          gsap.set(data.next.container, { clearProps: 'all' });
          if (data.opruimenStijlen) data.opruimenStijlen();

          zetScroll(data);
          barbaWrapper.classList.remove('is__transitioning');

          /* Waar de nieuwe pagina hoort te staan. zetScroll heeft dat net op de
             echte scrollbalk gezet; met de smoother gesloopt is dat de enige
             plek waar het staat. */
          const doelScroll = window.scrollY;

          /* Pas opbouwen als de nieuwe pagina op zijn plek staat en de
             scrollpositie klopt: de smoother meet bij het aanmaken de hoogte
             van de inhoud op. */
          const sm = window.MADEGRO?.smoother?.maak();
          window.ScrollTrigger?.refresh();

          /* En dan de stand er nog een keer in zetten. ScrollSmoother bewaart
             zijn eigen scrollpositie over sloop() en maak() heen, en
             ScrollTrigger.refresh() zet die met opzet terug om een sprong te
             voorkomen. Bij een pagina-overgang is dat precies verkeerd: je klikt
             halverwege pagina A door en komt dan halverwege pagina B uit, met een
             scrollbalk die bovenaan staat. Zonder deze twee regels landde je
             2200px diep in de nieuwe pagina. */
          /* De stand gaat er als laatste in, na de refresh. Andersom werkt niet:
             refresh() zet de onthouden stand terug en gooit hem er dan weer
             overheen. Dat was te zien bij de vooruitknop, die op nul hoorde uit
             te komen en op 1500 bleef staan. */
          if (sm) sm.scrollTop(doelScroll);
          window.scrollTo(0, doelScroll);
        },
      },
    ],
  });
})();
