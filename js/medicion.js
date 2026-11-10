// Medición de los clics a WhatsApp y Llamar para Google Ads.
// Cuando exista la cuenta nueva de Ads: completar CUENTA_ADS (AW-XXXXXXXXXX) y las ETIQUETAS
// (Ads → Objetivos → Conversiones → la acción → «Configurar con Google tag» → send_to: AW-.../ETIQUETA).
// Mientras CUENTA_ADS esté vacío, no se carga nada de Google.
(function () {
  var CUENTA_ADS = '';
  var ETIQUETAS = { whatsapp: '', llamar: '' };
  if (!CUENTA_ADS) return;

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', CUENTA_ADS);

  // gtag.js se carga recién con la primera interacción (o a los 3,5 s): no frena la carga.
  var cargado = false;
  function cargar() {
    if (cargado) return;
    cargado = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CUENTA_ADS;
    document.head.appendChild(s);
  }
  ['pointerdown', 'touchstart', 'keydown', 'scroll'].forEach(function (ev) {
    window.addEventListener(ev, cargar, { once: true, passive: true });
  });
  window.addEventListener('load', function () { setTimeout(cargar, 3500); });

  document.addEventListener('click', function (e) {
    var enlace = e.target.closest && e.target.closest('a[href*="wa.me/"], a[href^="tel:"]');
    if (!enlace) return;
    var tipo = enlace.getAttribute('href').indexOf('tel:') === 0 ? 'llamar' : 'whatsapp';
    gtag('event', 'clic_' + tipo, { seccion: enlace.dataset.seccion || 'sin-seccion', pagina: location.pathname, transport_type: 'beacon' });
    if (ETIQUETAS[tipo]) gtag('event', 'conversion', { send_to: CUENTA_ADS + '/' + ETIQUETAS[tipo], transport_type: 'beacon' });
  }, true);
})();
