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

## Google Ads — cuenta «Electricista Urgente» 586-442-4444

- Accesible con las credenciales del MCP (`~/.google-ads-mcp/`), facturación aprobada, ARS, autoetiquetado activo.
- Conversiones creadas por API el 10/11 (`herramientas/ads_conversiones.py`): «Clic WhatsApp web» y «Clic llamar web», tag `AW-18567711962`, ya cargadas en `js/medicion.js`. gtag.js se carga con la primera interacción o a los 3,5 s.
- Campañas: ver abajo.

## Pendiente

1. **Antispam como La Perla:** registro de gclid/IP en Neon + vigilancia (`api/vigilar.js` de laperladestapaciones, en la PC de casa). Implica sumar `package.json` y una base Neon propia (no la de La Perla). Hacerlo si aparecen clics no válidos.
2. **Search Console** + sitemap (el `noindex` ya se sacó el 10/11).
3. **Vercel Analytics:** activarlo en el panel del proyecto (el script ya está).
4. `og.jpg` sigue siendo la del diseño anterior.

## Textos a confirmar con Dario

- ¿Atiende de verdad **24 hs, todos los días**? Está en portada, cabecera, cifras, FAQ y schema.
- Medios de pago: efectivo, transferencia y Mercado Pago.
- Zonas: 21 barrios en la lista (más «y alrededores»).
- ¿Es **matriculado**? Si lo es, sumarlo (hoy no se menciona).
- ¿Cobra la visita? En el FAQ dice «depende de la zona y del horario».
- No se usó el barrio «La Perla» en la lista de zonas, para no asociar la marca.

## Medición

`js/medicion.js` manda `clic_whatsapp` / `clic_llamar` con el `data-seccion` de cada botón, y la conversión con su etiqueta.
