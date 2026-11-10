# Electricista Urgente — CONTINUAR

Landing de electricista de urgencia en **Mar del Plata** para Dario.
**No tiene que tener NINGUNA relación con La Perla ni con Manos Expertas** (ni nombre, ni teléfono, ni cuentas, ni textos copiados).

- Dominio: `electricistaurgente.com.ar` (registrado en nic.ar el 10/11/2026).
- Repo: `github.com/lautaromendezar-cmd/electricista-urgente` (push a `main` → deploy en Vercel).
- Stack: HTML estático, CSS inline en `index.html`, sin build ni `package.json`. Fuente Hanken Grotesk local (`/fuentes`).
- Fotos generadas con Google Nano Banana 2.1 (10/11). Los PNG originales están en `fuente-img/` (en .gitignore, solo en la PC de la oficina). Las versiones WebP están en `img/`.

## Pendiente para salir en vivo

1. **Teléfono real.** Hoy figura `5492230000000` / `223 000-0000` como placeholder. Cuando Dario lo pase, reemplazar en todo el sitio:
   ```bash
   sed -i 's/5492230000000/549223XXXXXXX/g; s/223 000-0000/223 XXX-XXXX/g' index.html
   ```
   (el número también aparece en el schema `telephone`, que lo cubre el primer reemplazo.)
2. **Sacar el `noindex`** de `index.html` (está marcado con un TODO) apenas esté el teléfono real.
3. **DNS:** en nic.ar delegar el dominio a `ns1.vercel-dns.com` y `ns2.vercel-dns.com`. El dominio ya está agregado en el proyecto de Vercel.
4. **Mecanismo antispam como el de La Perla:** el contexto está en la PC de casa. En el código publicado de laperladestapaciones / laperlacerrajeria no se ve: allá solo hay un 403 a `.php` (firewall de Vercel, `X-Vercel-Mitigated: deny`) y `Disallow: /api/` en robots. Agregarlo desde casa.
5. **Google Ads:** cuenta NUEVA, con mail propio, fuera del administrador de las otras. Después completar `CUENTA_ADS` y `ETIQUETAS` en `js/medicion.js`. Mientras esté vacío, no se carga nada de Google.
6. **Vercel Analytics:** activarlo en el panel del proyecto (el script `/_vercel/insights/script.js` ya está puesto).
7. Search Console + sitemap, cuando el sitio esté indexable.

## Textos a confirmar con Dario

- ¿Atiende de verdad **24 hs, todos los días**? Está en el hero, la cabecera, los datos, el FAQ y el schema (`openingHoursSpecification`).
- Medios de pago: efectivo, transferencia y Mercado Pago.
- Zonas: la lista de barrios, más Batán, Sierra de los Padres y Santa Clara del Mar.
- ¿Es **matriculado**? Si lo es, conviene sumarlo como argumento (hoy no se menciona).
- ¿Cobra la visita? En el FAQ dice «depende de la zona y del horario, te lo decimos antes de salir».
- ¿Trabaja en comercios? En Servicios dice «casas, departamentos y comercios».
- No se usó el barrio «La Perla» en la lista de zonas, para no asociar la marca.

## Medición

`js/medicion.js` manda `clic_whatsapp` / `clic_llamar` con el `data-seccion` de cada botón, y la conversión si hay etiqueta. Mismo esquema que La Perla, pero con otra cuenta.
