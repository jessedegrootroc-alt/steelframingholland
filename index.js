/* ============================================================================
   index.js: alleen wat de homepage extra doet
   Het gedeelde gedrag (header, paneel, accordeons) staat in site.js.
   ========================================================================== */

(() => {
  /* Tijdens een pagina-overgang staan de oude en de nieuwe pagina even samen in
     de DOM. document.getElementById zou dan het element van de oude pagina
     teruggeven, en dan hangt het gedrag aan een pagina die zo verdwijnt.
     Daarom zoeken we alles binnen de container waar dit script zelf in staat. */
  const container = document.currentScript?.closest('[data-barba="container"]') || document;

  /* De getallen bij de USP's tellen op zodra ze in beeld komen. De gids staat
     geen scroll-reveals toe (§9.3); dit is geen reveal maar een teller op een
     element dat al zichtbaar is, en hij slaat zichzelf over bij 'reduce'.
     Zolang de cijfers nog placeholders zijn ([X]) gebeurt er niets. */
  const kalm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const getallen = [...container.querySelectorAll('[data-telop]')]
    .filter((el) => /^\d+$/.test(el.dataset.telop.trim()));

  if (!getallen.length || kalm || !('IntersectionObserver' in window)) return;

  const telOp = (el) => {
    const doel = parseInt(el.dataset.telop, 10);
    const duur = 900;
    const start = performance.now();
    const stap = (nu) => {
      const deel = Math.min((nu - start) / duur, 1);
      /* uitdempen, zodat het einde rustig aanvoelt */
      el.textContent = Math.round(doel * (1 - Math.pow(1 - deel, 3)));
      if (deel < 1) requestAnimationFrame(stap);
    };
    requestAnimationFrame(stap);
  };

  const wacht = new IntersectionObserver((items) => {
    items.forEach((item) => {
      if (!item.isIntersecting) return;
      wacht.unobserve(item.target);
      telOp(item.target);
    });
  }, { threshold: 0.6 });

  getallen.forEach((el) => { el.textContent = '0'; wacht.observe(el); });
})();
