/* =========================================================
   EL MAÑANERO — panel de administración (vanilla)
   Editor de bloques con drag & drop, subidas y guardado JSON.
   ========================================================= */
(function () {
  'use strict';
  var CSRF = window.CSRF || '';

  function api(path, payload) {
    return fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRF': CSRF },
      body: JSON.stringify(payload)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (!res.ok || data.error) throw new Error(data.error || ('HTTP ' + res.status));
        return data;
      });
    });
  }

  function uploadFile(file) {
    var fd = new FormData();
    fd.append('file', file);
    fd.append('_csrf_dummy', '1');
    return fetch('/admin/api/upload', {
      method: 'POST',
      headers: { 'X-CSRF': CSRF },
      body: fd
    }).then(function (res) {
      return res.json().then(function (data) {
        if (!res.ok || data.error) throw new Error(data.error || ('HTTP ' + res.status));
        return data.files[0];
      });
    });
  }

  /* ---------------- buscador de la lista de noticias ---------------- */
  var qa = document.getElementById('qa-filter');
  var rows = document.getElementById('qa-rows');
  if (qa && rows) {
    qa.addEventListener('input', function () {
      var q = qa.value.toLowerCase();
      rows.querySelectorAll('tr').forEach(function (tr) {
        tr.style.display = (tr.dataset.title || '').indexOf(q) !== -1 ? '' : 'none';
      });
    });
  }

  /* ---------------- eliminar (listas) ---------------- */
  document.querySelectorAll('[data-del]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.dataset.id, kind = btn.dataset.kind;
      if (!id) return;
      if (!confirm('¿Eliminar este elemento? Esta acción no se puede deshacer.')) return;
      api('/admin/api/delete', { id: id, kind: kind }).then(function () {
        var tr = btn.closest('tr');
        if (tr) tr.remove();
        else window.location = kind === 'page' ? '/admin/pages' : '/admin/posts';
      }).catch(function (e) { alert('No se pudo eliminar: ' + e.message); });
    });
  });

  /* ---------------- multimedia ---------------- */
  var drop = document.querySelector('[data-drop]');
  if (drop) {
    var input = drop.querySelector('input[type="file"]');
    var grid = document.querySelector('.media-grid');
    var addCards = function (files) {
      files.forEach(function (f) {
        uploadFile(f).then(function (file) {
          var card = document.createElement('div');
          card.className = 'media-card';
          var media = file.isVideo
            ? '<video src="' + file.url + '" muted controls preload="metadata"></video>'
            : '<img src="' + file.url + '" alt="">';
          card.innerHTML = media +
            '<div class="media-meta"><span>' + file.name.replace(/</g, '&lt;') + '</span>' +
            '<div class="row-actions"><button class="mini" data-copy="' + file.url + '">Copiar enlace</button></div></div>';
          grid.prepend(card);
          bindCopy(card);
        }).catch(function (e) { alert('No se pudo subir: ' + e.message); });
      });
    };
    if (input) input.addEventListener('change', function () { addCards([].slice.call(input.files)); });
    ['dragover', 'dragenter'].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('over'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('over'); });
    });
    drop.addEventListener('drop', function (e) { addCards([].slice.call(e.dataTransfer.files)); });
  }
  function bindCopy(scope) {
    (scope || document).querySelectorAll('[data-copy]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var url = location.origin + btn.dataset.copy;
        (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () {
          var old = btn.textContent;
          btn.textContent = 'Copiado';
          setTimeout(function () { btn.textContent = old; }, 1400);
        }).catch(function () { prompt('Copia este enlace:', url); });
      });
    });
  }
  bindCopy(document);

  /* ---------------- editor de bloques ---------------- */
  var editor = document.querySelector('.editor');
  if (!editor) return;

  var blocksBox = editor.querySelector('[data-blocks]');
  // El botón Guardar y el estado viven en el encabezado de la página, fuera de .editor
  var saveBtn = document.querySelector('[data-save]');
  var saveState = document.querySelector('[data-savestate]');
  var item = window.__ITEM || {};
  var KIND = window.__KIND || 'post';

  var TEMPLATES = {
    h: function () {
      return { t: 'h', text: '' };
    },
    p: function () {
      return { t: 'p', text: '' };
    },
    img: function () {
      return { t: 'img', src: '', alt: '', cap: '' };
    },
    video: function () {
      return { t: 'video', src: '', yt: '', cap: '' };
    },
    q: function () {
      return { t: 'q', text: '', by: 'Equipo El Mañanero' };
    }
  };
  var TYPE_LABEL = { h: 'Subtítulo', p: 'Texto', img: 'Imagen', video: 'Video', q: 'Cita' };
  var ICON_OF = { h: 'heading', p: 'align-left', img: 'image', video: 'video', q: 'quote' };

  function field(f, label, value, tag) {
    var isTa = tag === 'textarea';
    var el = document.createElement(isTa ? 'textarea' : 'input');
    if (!isTa) { el.type = tag || 'text'; } else { el.rows = 4; }
    el.value = value || '';
    el.dataset.f = f;
    el.setAttribute('placeholder', label);
    return el;
  }

  function makeBlock(b) {
    var card = document.createElement('div');
    card.className = 'blk';
    card.dataset.t = b.t;
    card.draggable = false;
    var top = document.createElement('div');
    top.className = 'blk-top';
    top.innerHTML = '<span class="grow" title="Arrastrar para reordenar">' +
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="12" r="1"/><circle cx="9" cy="5" r="1"/><circle cx="9" cy="19" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="5" r="1"/><circle cx="15" cy="19" r="1"/></svg> Mover</span>' +
      (TYPE_LABEL[b.t] || b.t) +
      '<span class="sp">' +
      '<button type="button" class="mini" data-up title="Subir">↑</button>' +
      '<button type="button" class="mini" data-down title="Bajar">↓</button>' +
      '<button type="button" class="mini danger" data-rm title="Eliminar bloque">✕</button></span>';
    card.appendChild(top);

    var body = document.createElement('div');
    var add = function (el) { body.appendChild(el); };

    if (b.t === 'h') {
      var h = field('text', 'Subtítulo', b.text);
      h.style.fontWeight = '800';
      add(h);
    } else if (b.t === 'p') {
      add(field('text', 'Escribe el texto del párrafo…', b.text, 'textarea'));
    } else if (b.t === 'q') {
      add(field('text', 'Texto de la cita', b.text, 'textarea'));
      var by = field('by', '¿Quién lo dijo? (opcional)', b.by);
      by.style.marginTop = '.6rem';
      add(by);
    } else if (b.t === 'img') {
      var src = field('src', 'Pega el enlace de la imagen o súbela desde Multimedia', b.src);
      add(src);
      var up = document.createElement('label');
      up.className = 'mini upl';
      up.innerHTML = 'Subir imagen<input type="file" hidden accept="image/*">';
      add(up);
      up.querySelector('input').addEventListener('change', function () {
        if (!this.files[0]) return;
        up.classList.add('on');
        uploadFile(this.files[0]).then(function (file) {
          src.value = file.url;
          up.classList.remove('on');
          up.classList.add('ok');
        }).catch(function (e) { alert('No se pudo subir: ' + e.message); up.classList.remove('on'); });
      });
      add(field('alt', 'Texto alternativo (descripción para Google y lectores)', b.alt));
      add(field('cap', 'Pie de foto (opcional)', b.cap));
    } else if (b.t === 'video') {
      var yt = field('yt', 'Enlace de YouTube (opcional): https://youtube.com/watch?v=…', b.yt);
      add(yt);
      var vsrc = field('src', '…o video propio subido (opcional)', b.src);
      add(vsrc);
      var vup = document.createElement('label');
      vup.className = 'mini upl';
      vup.innerHTML = 'Subir video<input type="file" hidden accept="video/mp4,video/webm">';
      add(vup);
      vup.querySelector('input').addEventListener('change', function () {
        if (!this.files[0]) return;
        vup.classList.add('on');
        uploadFile(this.files[0]).then(function (file) {
          vsrc.value = file.url;
          vup.classList.remove('on');
        }).catch(function (e) { alert('No se pudo subir: ' + e.message); vup.classList.remove('on'); });
      });
      add(field('cap', 'Pie de video (opcional)', b.cap));
    }
    card.appendChild(body);

    // acciones
    top.querySelector('[data-rm]').addEventListener('click', function () {
      card.remove();
    });
    top.querySelector('[data-up]').addEventListener('click', function () {
      if (card.previousElementSibling) blocksBox.insertBefore(card, card.previousElementSibling);
    });
    top.querySelector('[data-down]').addEventListener('click', function () {
      if (card.nextElementSibling) blocksBox.insertBefore(card.nextElementSibling, card);
    });
    // drag & drop
    var handle = top.querySelector('.grow');
    handle.addEventListener('mousedown', function () { card.draggable = true; });
    handle.addEventListener('mouseup', function () { card.draggable = false; });
    card.addEventListener('dragstart', function (e) {
      card.classList.add('dragging');
      e.dataTransfer.setData('text/plain', '');
    });
    card.addEventListener('dragend', function () { card.classList.remove('dragging'); });
    blocksBox.addEventListener('dragover', function (e) {
      e.preventDefault();
      var dragging = blocksBox.querySelector('.dragging');
      if (!dragging) return;
      var after = [...blocksBox.querySelectorAll('.blk:not(.dragging)')].find(function (el) {
        return e.clientY <= el.getBoundingClientRect().top + el.offsetHeight / 2;
      });
      if (after) blocksBox.insertBefore(dragging, after);
      else blocksBox.appendChild(dragging);
    });
    return card;
  }

  function addBlock(type, data) {
    var b = data || TEMPLATES[type]();
    blocksBox.appendChild(makeBlock(b));
  }

  // render inicial
  (item.blocks && item.blocks.length ? item.blocks : [{ t: 'p', text: '' }])
    .forEach(function (b) { blocksBox.appendChild(makeBlock(b)); });

  editor.querySelectorAll('[data-add]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      addBlock(btn.dataset.add);
      blocksBox.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  /* ---------------- portada: subida ---------------- */
  var coverInput = editor.querySelector('[name="cover"]');
  var coverUp = editor.querySelector('[data-upload]');
  if (coverUp && coverInput) {
    coverUp.addEventListener('change', function () {
      if (!this.files[0]) return;
      uploadFile(this.files[0]).then(function (file) {
        coverInput.value = file.url;
        var prev = editor.querySelector('.cover-preview');
        prev.innerHTML = '<img src="' + file.url + '" alt="">';
      }).catch(function (e) { alert('No se pudo subir: ' + e.message); });
    });
  }

  /* ---------------- guardar ---------------- */
  var slugDirty = false;
  var slugInput = editor.querySelector('[name="slug"]');
  if (slugInput) slugInput.addEventListener('input', function () { slugDirty = true; });

  function collect() {
    var blocks = [];
    blocksBox.querySelectorAll('.blk').forEach(function (card) {
      var b = { t: card.dataset.t || 'p' };
      card.querySelectorAll('[data-f]').forEach(function (input) {
        b[input.dataset.f] = input.value;
      });
      if (b.t === 'img' || b.t === 'video') {
        if (!b.src && !b.yt) return; // bloque vacío
      }
      blocks.push(b);
    });
    var fd = {
      id: (editor.querySelector('[name="id"]') || {}).value || '',
      kind: KIND,
      title: (editor.querySelector('[name="title"]') || {}).value || '',
      slug: (editor.querySelector('[name="slug"]') || {}).value || '',
      status: (editor.querySelector('[name="status"]') || {}).value || 'draft',
      blocks: blocks
    };
    if (KIND === 'post') {
      fd.excerpt = (editor.querySelector('[name="excerpt"]') || {}).value || '';
      fd.cover = (editor.querySelector('[name="cover"]') || {}).value || '';
      fd.tags = (editor.querySelector('[name="tags"]') || {}).value || '';
      fd.category = (editor.querySelector('[name="category"]') || {}).value || 'Noticias';
      fd.author = (editor.querySelector('[name="author"]') || {}).value || 'Redacción El Mañanero';
      fd.featured = !!(editor.querySelector('[name="featured"]') || {}).checked;
      fd.isVideo = !!(editor.querySelector('[name="isVideo"]') || {}).checked;
    } else {
      fd.inNav = !!(editor.querySelector('[name="inNav"]') || {}).checked;
      fd.navOrder = (editor.querySelector('[name="navOrder"]') || {}).value || 99;
    }
    return fd;
  }

  saveBtn.addEventListener('click', function () {
    var data = collect();
    if (!data.title.trim()) { alert('Escribe un título.'); return; }
    saveBtn.disabled = true;
    saveState.textContent = 'Guardando…';
    api('/admin/api/save', data).then(function (res) {
      editor.querySelector('[name="id"]').value = res.id;
      if (!slugDirty && slugInput) slugInput.value = res.slug;
      saveState.textContent = 'Guardado · ' + new Date().toLocaleTimeString();
      var delBtn = document.querySelector('[data-del]');
      if (delBtn) { delBtn.hidden = false; delBtn.dataset.id = res.id; }
    }).catch(function (e) {
      saveState.textContent = '';
      alert('No se pudo guardar: ' + e.message);
    }).finally(function () { saveBtn.disabled = false; });
  });
})();
