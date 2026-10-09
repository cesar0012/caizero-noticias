/* El Mañanero Deportes — interacciones del sitio público (vanilla) */
(function () {
  'use strict';
  var toggle = document.getElementById('navToggle');
  var drawer = document.getElementById('drawer');
  if (toggle && drawer) {
    var set = function (open) {
      if (open) drawer.removeAttribute('hidden');
      else drawer.setAttribute('hidden', '');
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', function () { set(drawer.hasAttribute('hidden')); });
    drawer.querySelectorAll('[data-close]').forEach(function (el) {
      el.addEventListener('click', function () { set(false); });
    });
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { set(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') set(false);
    });
  }
})();
