# Electricista Urgente — CONTINUAR

Landing de electricista de urgencia en **Mar del Plata** para Dario.
**No tiene que tener NINGUNA relación con La Perla ni con Manos Expertas** (ni nombre, ni teléfono, ni cuentas, ni textos copiados).

- Dominio: `electricistaurgente.com.ar` (nic.ar, 10/11/2026), DNS en Vercel (ns1/ns2.vercel-dns.com), apex y www andando.
- Repo: `github.com/lautaromendezar-cmd/electricista-urgente` (push a `main` → deploy en Vercel, proyecto `electricista-urgente`).
- Stack: HTML estático, CSS inline en `index.html`, sin build ni `package.json`.
- Teléfono / WhatsApp de Dario: **223 501-3375** (`+5492235013375`, validado como celular). En Ads, con el 15: `223 15-501-3375`.

## Diseño (rediseño «Nocturno», 10/11/2026, casa)

- Fondo tinta azul-noche `#0a0f1a`, texto hueso `#efe9df`, un solo acento ámbar «luz de sodio» `#ffb547`. Verde solo en WhatsApp.
- Una sola familia: **Mona Sans** variable (`fuentes/mona-sans-var.woff2`, recortada a wdth 75–100 y wght 400–850, 63 KB). Títulos con `font-stretch: 86%` y peso 800. **No bajar de ~85 %: a Lautaro las condensadas de afiche le parecen de IA.**
- Entrada «vuelve la luz» en CSS puro (la foto parpadea y prende, los renglones del título suben). Sin JS se ve todo; respaldo de 2,5 s en el `<head>`.
- Portada: la «linterna» (`.portada__haz`) sigue al mouse sobre la foto; en celular queda fija.
- Sin hairlines verticales; WhatsApp con el path oficial de Simple Icons.
- Fotos: `hero-*` es la de Nano Banana (oficina). `enchufe-noche`, `tablero-noche`, `calle-noche` son de **Higgsfield gpt_image_2_6** (10/11, 0,25 créditos c/u), con la portada como referencia de estilo. El enchufe es **argentino (IRAM, patas planas)**: el primero salió Schuko y se descartó. Originales en `fuente-img/` (no se sube).
- Google (generar-google) no anduvo: el proyecto pasó el tope bruto de USD 5 de noviembre. No se tocó el tope.
- Los assets de `img/` y `fuentes/` tienen caché `immutable`: **si cambia una imagen, cambiarle el nombre.**

## Logo (10/11)

- **Elegido por Lautaro (opción B, tras rechazar la «térmica levantada»):** rayo ámbar dentro de un cable que da la vuelta y termina en un enchufe. Nombre en Mona Sans 86 %/800 pasado a trazos, «URGENTE» en ámbar; la versión completa suma «MAR DEL PLATA».
- Referencias que pasó (Pinterest): rayo + enchufe/cable en trazo continuo, signo reconocible al toque. Descartadas: A (cable que dibuja el rayo, floja) y C (sol de MdP con rayo calado).
- Archivos para Dario en `marca/` (no se publica): logo para fondo oscuro, claro y con fondo (SVG + PNG 2400), `icono` cuadrado, `perfil-redes-1080.png` (con aire para el recorte circular de WhatsApp/IG), `simbolo-*` y `logo-web.svg` (sin «MAR DEL PLATA», el que va inline en la cabecera). `favicon.svg` y `apple-touch-icon.png` en la raíz.

## Simplificación (10/11, pedido de Lautaro)

Fuera: punto de «atendemos ahora», checks de la portada, cinta con puntos, rótulos con guion, puntos de servicios, cifras y la pregunta de medios de pago. **No volver a meter puntitos decorativos ni listas de checks: le parecen «IA slop».**

## Páginas de servicio (10/11)

- `/sin-luz`, `/salta-la-termica`, `/pilar-de-luz`, `/tableros-electricos`. **Se generan con `node herramientas/generar-paginas.mjs`** a partir de `index.html` (toma head/estilos, cabecera, pie y scripts): **después de tocar el diseño de la home, volver a correrlo.** Los textos de cada página están en ese archivo. También regenera el `sitemap.xml`.
- Cada una: portada con foto propia, causas (con WhatsApp armado por causa), consejos, pasos, preguntas, «Otros problemas» y cierre. Schema Service + FAQPage + BreadcrumbList.
- La home enlaza desde Servicios (4 títulos con flecha) y desde el pie.
- Ads: cada grupo apunta a su página (`herramientas/ads_paginas_10nov.py`).

## Google Ads — cuenta «Electricista Urgente» 586-442-4444

- Accesible con las credenciales del MCP (`~/.google-ads-mcp/`), facturación aprobada, ARS, autoetiquetado activo.
- Conversiones creadas por API el 10/11 (`herramientas/ads_conversiones.py`): «Clic WhatsApp web» y «Clic llamar web», tag `AW-18567711962`, ya cargadas en `js/medicion.js`. gtag.js se carga con la primera interacción o a los 3,5 s.
- **Campaña «Electricista MdP - Búsqueda» (id 24459234427), creada por API el 10/11 EN PAUSA** (`herramientas/ads_campana.py`, idempotente: si existe no hace nada).
  - **HABILITADA el 10/11 ~21 h** con presupuesto **$6.000/día** (OK de Lautaro). Búsqueda de Google solamente. Maximizar clics con tope CPC $3.000.
  - Ubicación por presencia: General Pueyrredón (MdP, Batán, Sierra) + Santa Clara del Mar. Español.
  - 2 grupos: «Electricista urgente» y «Sin luz y térmica», 12 claves c/u en frase + exacta. 35 negativas (edea, reclamo, programados, curso, trabajo, auto…). **No poner «sin luz» / «corte de luz» como negativas amplias** (en Manos Expertas bloqueaban clientes).
  - RSA de 15 títulos y 4 descripciones por grupo. Sin «matriculado» (falta confirmar). Llamada `+5492235013375`, 4 sitelinks a las anclas, 5 destacados y fragmento de Servicios.
  - 10/11 (`herramientas/ads_ajustes_10nov.py`): fuera el destacado de Mercado Pago y RSA rehechos sin medios de pago. **Revisar ~13-nov: aprobación, términos de búsqueda, clics no válidos.**
- Cuando arranque: medir CPA; si conviene, pasar a Maximizar conversiones con ~15-20 conversiones acumuladas.

## Pendiente

1. **Antispam como La Perla:** registro de gclid/IP en Neon + vigilancia (`api/vigilar.js` de laperladestapaciones, en la PC de casa). Implica sumar `package.json` y una base Neon propia (no la de La Perla). Hacerlo si aparecen clics no válidos.
2. ~~Search Console~~ → **hecho el 10/11**: propiedad de dominio verificada por TXT en Vercel DNS (`vercel dns`), sitemap enviado. **Sin ficha de Google Business por decisión de Lautaro (10/11).**
3. ~~Vercel Analytics~~ → activado por Lautaro el 10/11 y script repuesto en todas las páginas.

## Textos a confirmar con Dario

Criterio tomado de Manos Expertas (10/11): **sin confirmar, no usar** (matriculado, años, garantía, reseñas, medios de pago). «24 hs» se mantiene, como en Manos Expertas.

- ¿Atiende de verdad **24 hs, todos los días**? Está en portada, cabecera, cifras, FAQ y schema.
- Medios de pago: sacados de la web y de los anuncios hasta que los confirme.
- Zonas: 21 barrios en la lista (más «y alrededores»).
- ¿Es **matriculado**? Si lo es, sumarlo (hoy no se menciona).
- ¿Cobra la visita? En el FAQ dice «depende de la zona y del horario».
- No se usó el barrio «La Perla» en la lista de zonas, para no asociar la marca.

## Medición

`js/medicion.js` manda `clic_whatsapp` / `clic_llamar` con el `data-seccion` de cada botón, y la conversión con su etiqueta.
