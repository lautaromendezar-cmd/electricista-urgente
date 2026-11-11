// Genera las páginas de servicio (sin-luz.html, salta-la-termica.html, pilar-de-luz.html, tableros-electricos.html)
// a partir de index.html: toma de ahí el <head> (estilos), la cabecera, el pie, la barra del celular y los scripts,
// así un cambio de diseño en la home se aplica a todas con solo volver a correr esto.
//
//   node herramientas/generar-paginas.mjs
//
// Sin dependencias ni package.json (un package.json en la raíz rompe el deploy estático de Vercel).
// Criterio de textos (como Manos Expertas): nada sin confirmar con Dario — ni matriculado, ni precios, ni garantías,
// ni medios de pago.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOMINIO = 'https://electricistaurgente.com.ar';
const TEL = '5492235013375';
const TEL_VER = '223 501-3375';

const FOTOS = {
  calle: { src: 'calle-noche', alt: 'Calle de un barrio de Mar del Plata de noche, con las casas sin luz', pos: '50% 50%' },
  tablero: { src: 'tablero-noche', alt: 'Electricista a domicilio midiendo un tablero eléctrico con un multímetro', pos: '50% 40%' },
  pilar: { src: 'pilar-noche', alt: 'Pilar de luz con el medidor de EDEA iluminado con una linterna', pos: '30% 50%' },
  enchufe: { src: 'enchufe-noche', alt: 'Enchufe quemado con hollín en la pared, iluminado con una linterna', pos: '50% 50%' },
};

const PAGINAS = [
  {
    slug: 'sin-luz',
    corto: 'Sin luz en casa',
    titulo: 'Sin luz en casa en Mar del Plata · Electricista urgente 24 hs',
    descripcion: '¿Te quedaste sin luz y los vecinos tienen? Electricista urgente en Mar del Plata: encontramos la falla y te devolvemos la luz. Escribinos por WhatsApp.',
    servicio: 'Reparación de cortes de luz y fallas eléctricas',
    clave: 'Sin luz en casa: electricista de urgencia en Mar del Plata',
    tema: 'cortes de luz',
    pasosTitulo: 'Cómo te devolvemos <em>la luz.</em>',
    grande: ['¿Sin luz', 'en casa?', '<em>Vamos.</em>'],
    bajada: 'Si los vecinos tienen luz y vos no, la falla está en tu instalación. Mandanos una foto del tablero y vamos.',
    wa: 'Hola! Me quedé sin luz en casa',
    foto: 'calle',
    causasTitulo: 'Por qué se corta la luz <em>en tu casa.</em>',
    causas: [
      ['Saltó la térmica o el disyuntor', 'Mirá el tablero: si alguna llave está abajo, ahí está la pista.', 'Hola! Me quedé sin luz y saltó la térmica o el disyuntor'],
      ['Un cortocircuito', 'Un cable pelado, un enchufe quemado o un artefacto en corto hacen saltar todo.', 'Hola! Creo que tengo un cortocircuito'],
      ['Una falla en el pilar o la entrada', 'Si el tablero está bien y no hay luz, el problema puede estar antes: en el pilar o en la acometida.', 'Hola! Me quedé sin luz y el tablero parece estar bien'],
      ['Un corte de EDEA', 'Si tus vecinos tampoco tienen luz, es un corte general: ahí hay que reclamarle a EDEA.', 'Hola! No sé si el corte de luz es mío o de EDEA'],
    ],
    consejosTitulo: 'Qué hacer mientras <em>llega el electricista.</em>',
    consejos: [
      'Fijate si tus vecinos tienen luz.',
      'Mirá el tablero: si una térmica o el disyuntor están abajo, <strong>probá subirlos una sola vez.</strong>',
      'Si vuelven a saltar, dejalos abajo y desenchufá todo.',
      'Si hay olor a quemado o chispas, <strong>bajá la general y no toques nada.</strong>',
    ],
    fotoConsejos: 'enchufe',
    pasos: [
      ['Buscamos la falla', 'Medimos circuito por circuito hasta encontrar dónde está el problema.'],
      ['Te pasamos el precio', 'Antes de arreglar nada, te decimos qué es y cuánto sale.'],
      ['Reparamos', 'Cambiamos lo que esté dañado: cables, tomas o protecciones.'],
      ['Volvés a tener luz', 'Probamos toda la casa antes de irnos.'],
    ],
    faq: [
      ['¿Cómo sé si el corte es mío o de EDEA?', 'Si tus vecinos tienen luz y vos no, la falla está en tu instalación. Si toda la cuadra está sin luz, es un corte de EDEA.'],
      ['¿Pueden venir de noche?', 'Sí. Atendemos las 24 horas, también fines de semana y feriados.'],
      ['¿Qué hago si hay olor a quemado?', 'Bajá la térmica general, no toques el enchufe ni el artefacto y llamanos. Si hay fuego, llamá primero al 100.'],
    ],
  },
  {
    slug: 'salta-la-termica',
    corto: 'Salta la térmica',
    titulo: 'Salta la térmica o el disyuntor en Mar del Plata · Electricista 24 hs',
    descripcion: '¿Salta la térmica o el disyuntor y no levanta? Electricista en Mar del Plata: encontramos la fuga o el corto y lo dejamos funcionando. Escribinos.',
    servicio: 'Reparación de térmicas y disyuntores que saltan',
    clave: 'Salta la térmica o el disyuntor: electricista en Mar del Plata',
    tema: 'térmicas y disyuntores',
    pasosTitulo: 'Cómo encontramos <em>la falla.</em>',
    grande: ['¿Salta', 'la térmica?', '<em>Vamos.</em>'],
    bajada: 'Si la subís y vuelve a saltar, hay una falla. No la fuerces: mandanos una foto del tablero.',
    wa: 'Hola! Me salta la térmica o el disyuntor y no levanta',
    foto: 'tablero',
    causasTitulo: 'Térmica o disyuntor: <em>no es lo mismo.</em>',
    causas: [
      ['Salta la térmica', 'Protege los cables. Salta por sobrecarga, con muchos artefactos juntos, o por un cortocircuito.', 'Hola! Me salta la térmica'],
      ['Salta el disyuntor', 'Protege a las personas. Salta cuando hay una fuga de corriente: humedad, un cable dañado o un artefacto con falla.', 'Hola! Me salta el disyuntor'],
      ['Salta cuando enchufás algo', 'Casi siempre es ese artefacto. Desenchufalo y probá de nuevo.', 'Hola! Me salta la térmica cuando enchufo algo'],
      ['Salta cuando llueve', 'Entra humedad en alguna caja, en el pilar o en una instalación exterior.', 'Hola! Me salta el disyuntor cuando llueve'],
    ],
    consejosTitulo: 'Qué podés probar <em>antes de llamar.</em>',
    consejos: [
      'Desenchufá todo y subí la llave una vez.',
      'Si se mantiene, enchufá los artefactos de a uno: <strong>el que la hace saltar es el culpable.</strong>',
      'Si salta aun con todo desenchufado, la falla está en la instalación. Dejala abajo.',
      '<strong>Nunca la puentees</strong> ni la ates para que «aguante».',
    ],
    fotoConsejos: 'enchufe',
    pasos: [
      ['Revisamos el tablero', 'Vemos qué protección salta y por qué.'],
      ['Medimos la instalación', 'Buscamos la fuga o el corto, circuito por circuito.'],
      ['Te pasamos el precio', 'Antes de arreglar nada, te decimos qué es y cuánto sale.'],
      ['Lo dejamos protegido', 'Reparamos la falla y, si hace falta, cambiamos la protección por una adecuada.'],
    ],
    faq: [
      ['¿Puedo poner una térmica o un disyuntor más grande para que no salte?', 'No. Si salta, está avisando de una falla. Cambiarlo por uno más grande o puentearlo deja la casa sin protección.'],
      ['¿Por qué salta el disyuntor cuando llueve?', 'Porque entra humedad en alguna caja o instalación exterior y se produce una fuga a tierra. Hay que encontrarla y sellarla.'],
      ['¿Atienden de noche y feriados?', 'Sí. Atendemos las 24 horas, todos los días.'],
    ],
  },
  {
    slug: 'pilar-de-luz',
    corto: 'Pilar de luz',
    titulo: 'Pilar de luz en Mar del Plata · Pilar y medidor para EDEA',
    descripcion: 'Armamos y reparamos pilares de luz en Mar del Plata: caja de medidor, tablero de entrada y puesta a tierra, listos para EDEA. Pedí presupuesto por WhatsApp.',
    servicio: 'Armado y reparación de pilares de luz',
    clave: 'Pilar de luz en Mar del Plata, listo para EDEA',
    tema: 'pilares de luz',
    pasosTitulo: 'Cómo armamos <em>el pilar de luz.</em>',
    grande: ['Pilar de luz', 'listo para', '<em>EDEA.</em>'],
    bajada: 'Armamos el pilar nuevo o reparamos el que tenés. Mandanos una foto y te pasamos presupuesto.',
    wa: 'Hola! Quiero consultar por un pilar de luz',
    foto: 'pilar',
    causasTitulo: 'Cuándo hace falta <em>un pilar de luz.</em>',
    causas: [
      ['Conexión nueva', 'Casa a estrenar, obra o terreno que necesita el medidor de EDEA.', 'Hola! Necesito un pilar de luz para una conexión nueva'],
      ['Pilar dañado', 'Pilar roto, caja quebrada, tapa que no cierra o cables a la vista.', 'Hola! Tengo el pilar de luz dañado'],
      ['EDEA pidió cambios', 'Si te pidieron adecuar el pilar antes de conectar o de cambiar el medidor.', 'Hola! EDEA me pidió cambios en el pilar'],
      ['Más consumo', 'Si vas a sumar aires o artefactos grandes y la entrada te queda chica.', 'Hola! Voy a sumar consumo y quiero revisar el pilar'],
    ],
    consejosTitulo: 'Si el pilar <em>está dañado.</em>',
    consejos: [
      'No toques cables sueltos ni la caja del medidor.',
      'Si hay chispas o cables a la vista, <strong>mantené lejos a los chicos y a las mascotas.</strong>',
      'Sacale una foto de cerca y otra de lejos, y mandánoslas.',
      'Si hay riesgo en la vereda, avisale también a EDEA.',
    ],
    fotoConsejos: 'calle',
    pasos: [
      ['Vemos el pilar', 'Con tus fotos o en el lugar, vemos qué hace falta.'],
      ['Te pasamos el presupuesto', 'Materiales y mano de obra, antes de empezar.'],
      ['Armamos o reparamos', 'Caja de medidor, tablero de entrada, cañería y puesta a tierra.'],
      ['Queda listo para conectar', 'Para que EDEA pueda instalar o reconectar el medidor.'],
    ],
    faq: [
      ['¿Cuánto sale un pilar de luz?', 'Depende de si es nuevo o una reparación, y de los materiales. Mandanos fotos y te pasamos el presupuesto antes de empezar.'],
      ['¿Qué lleva un pilar de luz?', 'La caja para el medidor, un tablero con protecciones, la cañería de la acometida y la puesta a tierra con jabalina.'],
      ['¿Trabajan en Batán y Sierra de los Padres?', 'Sí, en todo Mar del Plata y alrededores.'],
    ],
  },
  {
    slug: 'tableros-electricos',
    corto: 'Tableros eléctricos',
    titulo: 'Tableros eléctricos en Mar del Plata · Cambio y armado',
    descripcion: 'Cambio y armado de tableros eléctricos en Mar del Plata: térmicas, disyuntor y puesta a tierra. Presupuesto por WhatsApp antes de empezar.',
    servicio: 'Cambio y armado de tableros eléctricos',
    clave: 'Tableros eléctricos en Mar del Plata: cambio y armado',
    tema: 'tableros eléctricos',
    pasosTitulo: 'Cómo cambiamos <em>el tablero eléctrico.</em>',
    grande: ['Tablero', 'nuevo,', '<em>seguro.</em>'],
    bajada: 'Cambiamos tableros viejos por tableros con térmicas, disyuntor y puesta a tierra. Presupuesto antes de empezar.',
    wa: 'Hola! Quiero un presupuesto para cambiar el tablero eléctrico',
    foto: 'hero',
    causasTitulo: 'Cuándo conviene <em>cambiar el tablero.</em>',
    causas: [
      ['No tiene disyuntor', 'Sin disyuntor, una fuga de corriente puede electrocutar a alguien sin que nada corte.', 'Hola! Mi tablero no tiene disyuntor'],
      ['Tiene fusibles o tapones', 'Las instalaciones viejas con fusibles no protegen como corresponde.', 'Hola! Mi tablero todavía tiene fusibles'],
      ['Se calienta o huele a quemado', 'Una térmica caliente o con marcas negras es una falla en curso.', 'Hola! El tablero se calienta o huele a quemado'],
      ['Vas a sumar consumo', 'Aires, horno eléctrico o termotanque necesitan circuitos y protecciones propias.', 'Hola! Voy a sumar aires o artefactos y quiero revisar el tablero'],
    ],
    consejosTitulo: 'Señales de que <em>hay que cambiar el tablero.</em>',
    consejos: [
      '<strong>Térmicas calientes</strong> al tacto o con olor a quemado.',
      'Marcas negras o plástico derretido en el tablero.',
      'Luces que bajan cuando arranca un artefacto.',
      'La térmica o el disyuntor saltan seguido sin causa clara.',
    ],
    fotoConsejos: 'tablero',
    pasos: [
      ['Revisamos la instalación', 'Vemos el tablero, los circuitos y la puesta a tierra.'],
      ['Te pasamos el presupuesto', 'Materiales y mano de obra, antes de empezar.'],
      ['Armamos el tablero nuevo', 'Con térmicas por circuito, disyuntor y puesta a tierra.'],
      ['Probamos cada circuito', 'Verificamos que todo corte y funcione antes de irnos.'],
    ],
    faq: [
      ['¿Qué es la puesta a tierra y por qué importa?', 'Es la conexión de la instalación a una jabalina enterrada. Sin ella, el disyuntor no puede proteger bien ante una fuga.'],
      ['¿Hacen presupuesto?', 'Sí. Mandanos fotos del tablero por WhatsApp y te pasamos un presupuesto antes de empezar.'],
      ['¿Trabajan en comercios?', 'Sí, en casas, departamentos y comercios.'],
    ],
  },
];

const esc = s => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
const sinHtml = s => s.replace(/<[^>]+>/g, '');
const wa = (texto) => `https://wa.me/${TEL}?text=${encodeURIComponent(texto)}`;

function imagen(clave, sizes, extra = '') {
  if (clave === 'hero') return `<img src="/img/hero-1920.webp" srcset="/img/hero-1100.webp 1100w, /img/hero-1920.webp 1920w" sizes="${sizes}" alt="Electricista de urgencia revisando un tablero eléctrico de noche en Mar del Plata" width="1920" height="1072"${extra}>`;
  const f = FOTOS[clave];
  return `<img src="/img/${f.src}-900.webp" srcset="/img/${f.src}-700.webp 700w, /img/${f.src}-900.webp 900w" sizes="${sizes}" alt="${esc(f.alt)}" width="900" height="1125"${extra}>`;
}

function principal(p) {
  const otros = PAGINAS.filter(x => x.slug !== p.slug);
  const fotoPortada = p.foto === 'hero'
    ? `<picture><source media="(max-width: 860px)" srcset="/img/hero-movil-800.webp">${imagen('hero', '50vw', ' fetchpriority="high"')}</picture>`
    : imagen(p.foto, '(max-width: 860px) 100vw, 50vw', ` fetchpriority="high" style="object-position:${FOTOS[p.foto].pos}"`);
  return `
  <main>
    <section class="portada" id="inicio" data-portada>
      <div class="portada__foto">
        ${fotoPortada}
        <div class="portada__haz" aria-hidden="true"></div>
      </div>
      <div class="portada__texto">
        <p class="miga"><a href="/">Inicio</a> / ${esc(p.corto)}</p>
        <h1 class="portada__clave">${esc(p.clave)}</h1>
        <p class="portada__grande display">
${p.grande.map(l => `          <span class="renglon"><span>${l}</span></span>`).join('\n')}
        </p>
        <p class="portada__bajada">${esc(p.bajada)}</p>
        <div class="portada__acciones">
          <a class="boton boton--wa" href="${wa(p.wa)}" data-seccion="${p.slug}-portada">
            <svg class="ico ico-marca"><use href="#i-wa"/></svg>Escribir por WhatsApp
          </a>
          <a class="boton boton--luz" href="tel:+${TEL}" data-seccion="${p.slug}-portada">
            <svg class="ico ico-trazo"><use href="#i-tel"/></svg>Llamar ${TEL_VER}
          </a>
        </div>
      </div>
    </section>

    <section class="seccion grano" id="causas">
      <div class="envoltura">
        <div class="encabezado" data-revelar>
          <h2>${p.causasTitulo}</h2>
          <p class="bajada">Tocá la que se parece a lo tuyo: el WhatsApp sale armado.</p>
        </div>
        <ul class="indice" data-revelar>
${p.causas.map(([t, d, m]) => `          <li><a href="${wa(m || `Hola! ${t}`)}" data-seccion="${p.slug}-causa">
            <span class="indice__num" aria-hidden="true"></span>
            <h3>${esc(t)}</h3>
            <p>${esc(d)}</p>
            <span class="indice__ir">WhatsApp<svg class="ico ico-trazo"><use href="#i-flecha"/></svg></span>
          </a></li>`).join('\n')}
        </ul>
      </div>
    </section>

    <section class="seccion mientras grano" aria-labelledby="consejos-titulo">
      <div class="envoltura mientras__grilla">
        <div class="mientras__foto" data-revelar="foto">
          ${imagen(p.fotoConsejos, '(max-width: 860px) 100vw, 40vw', ' loading="lazy"')}
        </div>
        <div data-revelar>
          <h2 id="consejos-titulo">${p.consejosTitulo}</h2>
          <ol class="consejos">
${p.consejos.map(c => `            <li><span>${c}</span></li>`).join('\n')}
          </ol>
          <a class="boton boton--luz" href="tel:+${TEL}" data-seccion="${p.slug}-consejos">
            <svg class="ico ico-trazo"><use href="#i-tel"/></svg>Llamar ahora
          </a>
        </div>
      </div>
    </section>

    <section class="seccion grano">
      <div class="envoltura">
        <h2 data-revelar>${p.pasosTitulo}</h2>
        <ol class="pasos" data-revelar>
${p.pasos.map(([t, d]) => `          <li><h3>${esc(t)}</h3><p>${esc(d)}</p></li>`).join('\n')}
        </ol>
      </div>
    </section>

    <section class="seccion grano" id="preguntas">
      <div class="envoltura preguntas">
        <div data-revelar>
          <h2>Preguntas frecuentes sobre <em>${esc(p.tema)}.</em></h2>
        </div>
        <div class="faq" data-revelar>
${p.faq.map(([q, a], i) => `          <details${i === 0 ? ' open' : ''}><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('\n')}
        </div>
      </div>
    </section>

    <section class="seccion grano mientras">
      <div class="envoltura">
        <h2 data-revelar>Otros servicios de electricista <em>en Mar del Plata.</em></h2>
        <ul class="otros" data-revelar>
${otros.map(o => `          <li><a href="/${o.slug}"><strong>${esc(o.corto)}</strong><span>Ver más<svg class="ico ico-trazo"><use href="#i-flecha"/></svg></span></a></li>`).join('\n')}
          <li><a href="/"><strong>Todos los servicios</strong><span>Inicio<svg class="ico ico-trazo"><use href="#i-flecha"/></svg></span></a></li>
        </ul>
      </div>
    </section>

    <section class="cierre">
      <div class="envoltura" data-revelar>
        <h2 class="cierre__titulo">¿Necesitás un electricista <em>ahora?</em></h2>
        <a class="cierre__tel" href="tel:+${TEL}" data-seccion="${p.slug}-cierre" aria-label="Llamar al ${TEL_VER}">${TEL_VER}</a>
        <div class="cierre__pie">
          <p>Electricista urgente en Mar del Plata, las 24 horas. Escribinos y vamos.</p>
          <div class="cierre__acciones">
            <a class="boton boton--wa" href="${wa(p.wa)}" data-seccion="${p.slug}-cierre">
              <svg class="ico ico-marca"><use href="#i-wa"/></svg>Escribir por WhatsApp
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>
`;
}

function esquemas(p) {
  const url = `${DOMINIO}/${p.slug}`;
  const servicio = {
    '@context': 'https://schema.org', '@type': 'Service', name: p.servicio, serviceType: p.servicio, url,
    areaServed: { '@type': 'City', name: 'Mar del Plata' },
    provider: { '@type': 'Electrician', name: 'Electricista Urgente', url: DOMINIO + '/', telephone: '+' + TEL },
  };
  const faq = {
    '@context': 'https://schema.org', '@type': 'FAQPage',
    mainEntity: p.faq.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })),
  };
  const miga = {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Inicio', item: DOMINIO + '/' },
      { '@type': 'ListItem', position: 2, name: p.corto, item: url },
    ],
  };
  return [servicio, faq, miga].map(o => `  <script type="application/ld+json">\n  ${JSON.stringify(o)}\n  </script>`).join('\n');
}

const base = fs.readFileSync(path.join(RAIZ, 'index.html'), 'utf8');
const finHead = base.indexOf('</head>'), iniMain = base.indexOf('<main>'), finMain = base.indexOf('</main>') + '</main>'.length;
if (finHead < 0 || iniMain < 0 || finMain < 7) throw new Error('index.html no tiene la estructura esperada');

for (const p of PAGINAS) {
  const url = `${DOMINIO}/${p.slug}`;
  let head = base.slice(0, finHead);
  const cambiar = (re, nuevo) => { if (!re.test(head)) throw new Error(`${p.slug}: no encontré ${re}`); head = head.replace(re, nuevo); };
  cambiar(/<title>.*?<\/title>/, `<title>${esc(p.titulo)}</title>`);
  cambiar(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${esc(p.descripcion)}">`);
  cambiar(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${url}">`);
  cambiar(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${esc(sinHtml(p.titulo.split(' · ')[0]))}">`);
  cambiar(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${esc(p.descripcion)}">`);
  cambiar(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${url}">`);
  // Esquemas de la home → los de la página
  head = head.replace(/\s*<script type="application\/ld\+json">[\s\S]*?<\/script>/g, '');
  head = head.replace('\n  <style>', `\n${esquemas(p)}\n\n  <style>`);
  // Precarga de la foto de portada
  head = head.replace(/\s*<link rel="preload" as="image"[^>]*>/g, '');
  const pre = p.foto === 'hero'
    ? `<link rel="preload" as="image" href="/img/hero-movil-800.webp" media="(max-width: 860px)">\n  <link rel="preload" as="image" href="/img/hero-1920.webp" media="(min-width: 861px)">`
    : `<link rel="preload" as="image" href="/img/${FOTOS[p.foto].src}-900.webp">`;
  head = head.replace(/(<link rel="preload" href="\/fuentes\/[^>]*>)/, `$1\n  ${pre}`);

  // Cabecera: las anclas del menú apuntan a la home
  const cabecera = base.slice(finHead, iniMain).replace(/href="#(urgencias|servicios|zonas|preguntas)"/g, 'href="/#$1"');
  const cola = base.slice(finMain);
  const html = head + cabecera + principal(p).trimStart().replace(/^<main>/, '<main>') + cola;
  fs.writeFileSync(path.join(RAIZ, p.slug + '.html'), html);
  console.log('ok', p.slug + '.html', html.length);
}

// sitemap
const hoy = new Date().toISOString().slice(0, 10);
const urls = ['/', ...PAGINAS.map(p => '/' + p.slug)];
fs.writeFileSync(path.join(RAIZ, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>\n    <loc>${DOMINIO}${u}</loc>\n    <lastmod>${hoy}</lastmod>\n  </url>`).join('\n')}
</urlset>
`);
console.log('sitemap:', urls.length, 'URLs');
