/* Puente entre FoMT_Suite.html y cada herramienta.
   La suite abre la ROM una sola vez y la envía a la herramienta activa con postMessage
   (funciona también abriendo los archivos con doble clic, sin servidor).
   Si la herramienta se abre sola, el puente no hace nada y sigue funcionando por su cuenta.

   Uso en una herramienta:
     FomtHub.onRom(function (bytes, name) { ...cargar la ROM... });
     FomtHub.publish(bytesNuevos, nombre);   // tras inyectar: la suite la usa como ROM de trabajo */
(function () {
  'use strict';
  var inSuite = window.parent && window.parent !== window, handler = null, pending = null;

  window.addEventListener('message', function (e) {
    var d = e.data;
    if (!d || d.type !== 'fomt-rom' || !d.bytes) return;
    var bytes = d.bytes instanceof Uint8Array ? d.bytes : new Uint8Array(d.bytes);
    if (handler) handler(bytes, d.name || 'rom.gba'); else pending = { bytes: bytes, name: d.name };
  });

  window.FomtHub = {
    inSuite: inSuite,
    onRom: function (fn) {
      handler = fn;
      if (pending) { var p = pending; pending = null; fn(p.bytes, p.name || 'rom.gba'); }
      if (inSuite) window.parent.postMessage({ type: 'fomt-ready' }, '*');
    },
    publish: function (bytes, name) {
      if (!inSuite) return;
      var copy = new Uint8Array(bytes);
      window.parent.postMessage({ type: 'fomt-rom-out', name: name, bytes: copy }, '*');
    }
  };
})();
