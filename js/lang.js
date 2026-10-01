/* Language switcher: opens and closes the menu. The links themselves are plain <a> tags, so it works without JavaScript for crawlers. */
(function () {
  'use strict';
  var boxes = document.querySelectorAll('[data-lang]');
  if (!boxes.length) return;
  function close(box) { box.classList.remove('is-open'); var b = box.querySelector('.lang__btn'); if (b) b.setAttribute('aria-expanded', 'false'); }
  boxes.forEach(function (box) {
    var btn = box.querySelector('.lang__btn');
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !box.classList.contains('is-open');
      boxes.forEach(close);
      if (open) { box.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    });
    box.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(box); btn.focus(); } });
  });
  document.addEventListener('click', function (e) { boxes.forEach(function (box) { if (!box.contains(e.target)) close(box); }); });
  // remember an explicit choice so the site could offer it later; nothing redirects automatically
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-lang] a[hreflang], .lang-mobile a[hreflang]');
    if (a) { try { localStorage.setItem('vs-lang', a.getAttribute('hreflang')); } catch (x) { /* storage unavailable */ } }
  });
})();
