/* El Mañanero Deportes — interacciones del sitio público (vanilla) */
(function () {
  'use strict';
  var toggle = document.getElementById('navToggle');
  var drawer = document.getElementById('drawer');
  if (toggle && drawer) {
    var panel = drawer.querySelector('.drawer-panel');
    var set = function (open) {
      if (open) {
        drawer.removeAttribute('hidden');
        // doble frame para que el navegador pinte el estado inicial y luego transite
        requestAnimationFrame(function () {
          requestAnimationFrame(function () { drawer.classList.add('open'); });
        });
        toggle.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
      } else {
        drawer.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        // retirar del arbol cuando termina la animacion (con respaldo por tiempo)
        var done = function () { drawer.setAttribute('hidden', ''); };
        var t = setTimeout(done, 420);
        if (panel) {
          panel.addEventListener('transitionend', function h(e) {
            if (e.target === panel) {
              clearTimeout(t);
              panel.removeEventListener('transitionend', h);
              done();
            }
          });
        }
      }
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
