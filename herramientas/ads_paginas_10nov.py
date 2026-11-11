"""10-nov-2026 (OK de Lautaro): cada grupo de anuncios apunta a su página de servicio.

1. «Sin luz y térmica» → se renombra «Sin luz», pierde las claves de térmica/disyuntor/pilar/tablero y su RSA va a /sin-luz.
2. Grupos nuevos «Térmica y disyuntor» (/salta-la-termica), «Pilar de luz» (/pilar-de-luz) y «Tableros» (/tableros-electricos),
   con claves en frase + exacta y un RSA cada uno.
3. Sitelinks: los 4 de anclas (#urgencias…) se reemplazan por los de las páginas.
4. Negativas de búsquedas informativas (qué es, cómo hacer, diagrama…).

  uv run --with google-ads python herramientas/ads_paginas_10nov.py            → solo valida
  uv run --with google-ads python herramientas/ads_paginas_10nov.py --aplicar
"""
import os
import sys

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.path.expanduser("~/.google-ads-mcp/credentials.json"))
import google.auth  # noqa: E402
from google.ads.googleads.client import GoogleAdsClient  # noqa: E402
from google.api_core import protobuf_helpers  # noqa: E402

CLIENTE = "5864424444"
CAMPANA = 24459234427
APLICAR = "--aplicar" in sys.argv
D = "https://electricistaurgente.com.ar"
GRUPO_VIEJO = "Sin luz y térmica"

MOVER = {"salta la termica", "salta el disyuntor", "salta la termica y no levanta", "disyuntor salta",
         "arreglar tablero electrico", "reparacion pilar de luz"}

NUEVOS = {
    "Térmica y disyuntor": {
        "url": D + "/salta-la-termica", "p1": "termica", "p2": "disyuntor",
        "claves": ["salta la termica", "salta el disyuntor", "salta la termica y no levanta", "disyuntor salta",
                   "termica que salta", "se baja la termica", "disyuntor no levanta", "salta el disyuntor cuando llueve",
                   "se corta la luz y salta la termica"],
        "titulos": ["¿Salta la Térmica?", "¿Salta el Disyuntor?", "Salta y No Levanta: Vamos", "Encontramos la Falla",
                    "Electricista Urgente en MdP", "Atención las 24 Horas", "Escribinos por WhatsApp",
                    "Precio Antes de Empezar", "Noches, Findes y Feriados", "Fugas a Tierra y Cortos",
                    "No la Puentees: Llamanos", "Electricista en Mar del Plata", "Mandanos una Foto y Vamos",
                    "Respondemos al Toque", "Lo Dejamos Protegido"],
        "desc": ["¿Salta la térmica o el disyuntor y no levanta? Encontramos la fuga o el corto.",
                 "Electricista urgente en Mar del Plata, las 24 hs. Mandanos un WhatsApp y vamos a tu casa.",
                 "Te decimos cuándo llegamos y cuánto sale la visita antes de salir. Sin sorpresas.",
                 "No la fuerces ni la puentees: si vuelve a saltar, hay una falla. Escribinos y vamos."],
    },
    "Pilar de luz": {
        "url": D + "/pilar-de-luz", "p1": "pilar-de-luz", "p2": "mar-del-plata",
        "claves": ["pilar de luz", "pilar de luz mar del plata", "armado de pilar de luz", "reparacion pilar de luz",
                   "pilar de luz edea", "pilar para medidor de luz", "caja de medidor de luz", "hacer pilar de luz"],
        "titulos": ["Pilar de Luz en Mar del Plata", "Pilar Listo para EDEA", "Armado de Pilar de Luz",
                    "Reparación de Pilar de Luz", "Caja de Medidor y Tablero", "Puesta a Tierra con Jabalina",
                    "Presupuesto por WhatsApp", "Mandanos una Foto del Pilar", "Electricista en Mar del Plata",
                    "Conexión Nueva o Reparación", "Precio Antes de Empezar", "Batán, Sierra y Santa Clara",
                    "Respondemos al Toque", "Pilar Dañado: Lo Reparamos", "Para Casa, Obra o Terreno"],
        "desc": ["Armamos y reparamos pilares de luz en Mar del Plata: caja de medidor, tablero y jabalina.",
                 "Pilar nuevo o reparación, listo para que EDEA conecte el medidor. Pedí presupuesto.",
                 "Mandanos fotos del pilar por WhatsApp y te pasamos el presupuesto antes de empezar.",
                 "Conexión nueva, pilar roto o cambios que pidió EDEA. Trabajamos en todo Mar del Plata."],
    },
    "Tableros": {
        "url": D + "/tableros-electricos", "p1": "tableros", "p2": "mar-del-plata",
        "claves": ["tablero electrico", "cambiar tablero electrico", "arreglar tablero electrico",
                   "tablero electrico mar del plata", "cambio de tablero electrico", "puesta a tierra",
                   "jabalina puesta a tierra", "instalar disyuntor"],
        "titulos": ["Tableros Eléctricos en MdP", "Cambio de Tablero Eléctrico", "Tablero con Disyuntor",
                    "Puesta a Tierra con Jabalina", "Térmicas por Circuito", "Chau Fusibles Viejos",
                    "Presupuesto por WhatsApp", "Precio Antes de Empezar", "Electricista en Mar del Plata",
                    "Casas, Deptos y Comercios", "Tu Casa Más Segura", "Mandanos una Foto del Tablero",
                    "Respondemos al Toque", "Instalación de Disyuntor", "Circuitos para Aires"],
        "desc": ["Cambiamos tableros viejos por tableros con térmicas, disyuntor y puesta a tierra.",
                 "Mandanos fotos del tablero por WhatsApp y te pasamos el presupuesto antes de empezar.",
                 "Tablero que se calienta, sin disyuntor o con fusibles: lo cambiamos y queda seguro.",
                 "Electricista en Mar del Plata para casas, departamentos y comercios. Escribinos."],
    },
}
SITELINKS = [
    ("Sin luz en casa", "Encontramos la falla", "Y te devolvemos la luz", D + "/sin-luz"),
    ("Salta la térmica", "Térmica o disyuntor que salta", "Fugas a tierra y cortos", D + "/salta-la-termica"),
    ("Pilar de luz", "Pilar listo para EDEA", "Armado y reparación", D + "/pilar-de-luz"),
    ("Tableros eléctricos", "Cambio y armado de tableros", "Disyuntor y puesta a tierra", D + "/tableros-electricos"),
]
NEGATIVAS_FRASE = ["que es", "como se hace", "como hacer", "como armar", "como conectar", "diagrama", "esquema",
                   "norma", "reglamento", "medidas"]


def revisar():
    for g in NUEVOS.values():
        assert len(g["titulos"]) == 15 and len(g["desc"]) == 4
        for t in g["titulos"]:
            assert len(t) <= 30, t
        for d in g["desc"]:
            assert len(d) <= 90, (len(d), d)
        assert len(g["p1"]) <= 15 and len(g["p2"]) <= 15
    for s in SITELINKS:
        assert len(s[0]) <= 25 and len(s[1]) <= 35 and len(s[2]) <= 35, s


def main():
    revisar()
    cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
    c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
    ga = c.get_service("GoogleAdsService")
    v = not APLICAR
    campana = f"customers/{CLIENTE}/campaigns/{CAMPANA}"
    grupos = {f.ad_group.name: f.ad_group.resource_name for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, ad_group.name, ad_group.resource_name FROM ad_group WHERE campaign.id = {CAMPANA} AND ad_group.status != 'REMOVED'")}
    print("grupos:", list(grupos))
    ops = []

    def op(tipo):
        o = c.get_type("MutateOperation")
        ops.append(o)
        return o, getattr(o, tipo)

    tmp = iter(range(-1, -1000, -1))

    # 1) Grupo viejo → «Sin luz»
    viejo = grupos.get(GRUPO_VIEJO) or grupos.get("Sin luz")
    if GRUPO_VIEJO in grupos:
        o, x = op("ad_group_operation")
        x.update.resource_name = viejo
        x.update.name = "Sin luz"
        x.update_mask.CopyFrom(protobuf_helpers.field_mask(None, x.update._pb))
    for f in ga.search(customer_id=CLIENTE, query=f"SELECT ad_group.id, ad_group_criterion.resource_name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group.resource_name = '{viejo}' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED' AND ad_group_criterion.negative = FALSE"):
        if f.ad_group_criterion.keyword.text in MOVER:
            o, x = op("ad_group_criterion_operation")
            x.remove = f.ad_group_criterion.resource_name
    for f in ga.search(customer_id=CLIENTE, query=f"SELECT ad_group.id, ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.resource_name = '{viejo}' AND ad_group_ad.status != 'REMOVED'"):
        o, x = op("ad_operation")
        x.update.resource_name = f"customers/{CLIENTE}/ads/{f.ad_group_ad.ad.id}"
        x.update.final_urls.append(D + "/sin-luz")
        x.update_mask.CopyFrom(protobuf_helpers.field_mask(None, x.update._pb))

    # 2) Grupos nuevos
    for nombre, g in NUEVOS.items():
        if nombre in grupos:
            print("ya existe:", nombre)
            continue
        rn = f"customers/{CLIENTE}/adGroups/{next(tmp)}"
        o, x = op("ad_group_operation")
        a = x.create
        a.resource_name = rn
        a.name = nombre
        a.campaign = campana
        a.status = c.enums.AdGroupStatusEnum.ENABLED
        a.type_ = c.enums.AdGroupTypeEnum.SEARCH_STANDARD
        for k in g["claves"]:
            for t in (c.enums.KeywordMatchTypeEnum.PHRASE, c.enums.KeywordMatchTypeEnum.EXACT):
                o, x = op("ad_group_criterion_operation")
                kw = x.create
                kw.ad_group = rn
                kw.status = c.enums.AdGroupCriterionStatusEnum.ENABLED
                kw.keyword.text = k
                kw.keyword.match_type = t
        o, x = op("ad_group_ad_operation")
        ad = x.create
        ad.ad_group = rn
        ad.status = c.enums.AdGroupAdStatusEnum.ENABLED
        ad.ad.final_urls.append(g["url"])
        ad.ad.responsive_search_ad.path1 = g["p1"]
        ad.ad.responsive_search_ad.path2 = g["p2"]
        for t in g["titulos"]:
            h = c.get_type("AdTextAsset")
            h.text = t
            ad.ad.responsive_search_ad.headlines.append(h)
        for d in g["desc"]:
            h = c.get_type("AdTextAsset")
            h.text = d
            ad.ad.responsive_search_ad.descriptions.append(h)

    # 3) Sitelinks: fuera los de anclas, adentro los de páginas
    actuales = list(ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, campaign_asset.resource_name, asset.final_urls FROM campaign_asset WHERE campaign.id = {CAMPANA} AND campaign_asset.field_type = 'SITELINK' AND campaign_asset.status != 'REMOVED'"))
    urls_actuales = {u for f in actuales for u in f.asset.final_urls}
    if not any(s[3] in urls_actuales for s in SITELINKS):
        for f in actuales:
            if any("#" in u for u in f.asset.final_urls):
                o, x = op("campaign_asset_operation")
                x.remove = f.campaign_asset.resource_name
        for texto, l1, l2, url in SITELINKS:
            rn = f"customers/{CLIENTE}/assets/{next(tmp)}"
            o, x = op("asset_operation")
            a = x.create
            a.resource_name = rn
            a.final_urls.append(url)
            a.sitelink_asset.link_text = texto
            a.sitelink_asset.description1 = l1
            a.sitelink_asset.description2 = l2
            o, x = op("campaign_asset_operation")
            x.create.campaign = campana
            x.create.asset = rn
            x.create.field_type = c.enums.AssetFieldTypeEnum.SITELINK

    # 4) Negativas de frase a nivel campaña
    ya = {f.campaign_criterion.keyword.text for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.id = {CAMPANA} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")}
    for n in NEGATIVAS_FRASE:
        if n in ya:
            continue
        o, x = op("campaign_criterion_operation")
        x.create.campaign = campana
        x.create.negative = True
        x.create.keyword.text = n
        x.create.keyword.match_type = c.enums.KeywordMatchTypeEnum.PHRASE

    ga.mutate(request={"customer_id": CLIENTE, "mutate_operations": ops, "validate_only": v})
    print(len(ops), "operaciones", "APLICADAS" if APLICAR else "validadas OK")


if __name__ == "__main__":
    main()
