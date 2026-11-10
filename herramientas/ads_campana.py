"""Crea la campaña de Búsqueda «Electricista MdP» en 586-442-4444, EN PAUSA.

Todo en un solo GoogleAdsService.Mutate (atómico): presupuesto, campaña, ubicaciones, idioma,
negativas, 2 grupos con palabras clave y anuncio RSA, y recursos (llamada, sitelinks, textos destacados,
fragmentos estructurados).

  uv run --with google-ads python herramientas/ads_campana.py            → solo valida
  uv run --with google-ads python herramientas/ads_campana.py --aplicar  → crea (en pausa)
"""
import os
import sys

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.path.expanduser("~/.google-ads-mcp/credentials.json"))
import google.auth  # noqa: E402
from google.ads.googleads.client import GoogleAdsClient  # noqa: E402

CLIENTE = "5864424444"
APLICAR = "--aplicar" in sys.argv
URL = "https://electricistaurgente.com.ar/"
NOMBRE = "Electricista MdP - Búsqueda"
PRESUPUESTO_DIA = 8_000          # ARS, a confirmar con Lautaro/Dario antes de activar
TOPE_CPC = 3_000                 # ARS (Maximizar clics con tope, como La Plata en Manos Expertas)
UBICACIONES = [9247421, 9255688]  # General Pueyrredón (MdP, Batán, Sierra) y Santa Clara del Mar
ESPANOL = 1003
TELEFONO = "+5492235013375"      # celular: con el 9 (Google lo lee como móvil)

GRUPOS = {
    "Electricista urgente": {
        "claves": [
            "electricista mar del plata", "electricista urgente mar del plata", "electricista urgente",
            "electricista de urgencia", "electricista 24 horas", "electricista 24 hs",
            "electricista a domicilio", "electricista cerca", "electricista domicilio mar del plata",
            "electricista urgencias", "electricista fin de semana", "electricista de guardia",
        ],
        "titulos": [
            "Electricista Urgente en MdP", "Electricista en Mar del Plata", "Atención las 24 Horas",
            "Electricista a Domicilio", "Escribinos por WhatsApp", "Precio Antes de Empezar",
            "Noches, Findes y Feriados", "Vamos a Tu Casa", "¿Te Quedaste Sin Luz?",
            "Salta la Térmica o Disyuntor", "Tableros y Pilares de Luz", "Batán, Sierra y Santa Clara",
            "Mandanos una Foto y Vamos", "Pagá con Mercado Pago", "Respondemos al Toque",
        ],
    },
    "Sin luz y térmica": {
        "claves": [
            "me quede sin luz", "se corto la luz en mi casa", "sin luz en la casa", "salta la termica",
            "salta el disyuntor", "salta la termica y no levanta", "disyuntor salta", "olor a quemado enchufe",
            "enchufe quemado", "cortocircuito en casa", "arreglar tablero electrico", "reparacion pilar de luz",
        ],
        "titulos": [
            "¿Te Quedaste Sin Luz?", "¿Salta la Térmica?", "¿Salta el Disyuntor?", "Olor a Quemado: Llamanos",
            "Electricista Urgente en MdP", "Atención las 24 Horas", "Escribinos por WhatsApp",
            "Precio Antes de Empezar", "Noches, Findes y Feriados", "Vamos a Tu Casa",
            "Electricista en Mar del Plata", "Mandanos una Foto y Vamos", "Encontramos la Falla",
            "Lo Dejamos Funcionando", "Respondemos al Toque",
        ],
    },
}
DESCRIPCIONES = [
    "Electricista urgente en Mar del Plata, las 24 hs. Mandanos un WhatsApp y vamos a tu casa.",
    "Cortes de luz, térmica o disyuntor que salta, olor a quemado. Te pasamos el precio antes.",
    "Te decimos cuándo llegamos y cuánto sale la visita antes de salir. Sin sorpresas.",
    "Tableros, pilares, puesta a tierra y cableado. Efectivo, transferencia o Mercado Pago.",
]
NEGATIVAS = [  # concordancia amplia, a nivel campaña
    "edea", "reclamo", "reclamos", "programado", "programados", "0800", "curso", "cursos", "capacitacion",
    "escuela", "instituto", "carrera", "aprender", "tutorial", "youtube", "video", "pdf", "manual",
    "trabajo", "empleo", "busco", "sueldo", "salario", "cuanto gana", "gratis", "auto", "autos",
    "automotor", "moto", "motos", "camion", "ferreteria", "precio cable", "mercadolibre", "simbolo", "dibujo",
]
SITELINKS = [
    ("Urgencias eléctricas", "Sin luz, térmica, olor a quemado", "Tocá tu problema y escribinos", URL + "#urgencias"),
    ("Servicios", "Tableros, pilares, cableado", "Casas, deptos y comercios", URL + "#servicios"),
    ("Zonas de trabajo", "Todo Mar del Plata", "Batán, Sierra y Santa Clara", URL + "#zonas"),
    ("Preguntas frecuentes", "Precio de la visita y pagos", "Qué hacer mientras llegamos", URL + "#preguntas"),
]
DESTACADOS = ["Atención 24 Horas", "Precio Antes de Empezar", "Noches y Feriados", "Pagás con Mercado Pago", "Respuesta por WhatsApp"]
FRAGMENTO = ("Servicios", ["Cortes de luz", "Térmicas y disyuntores", "Tableros", "Pilar y medidor", "Puesta a tierra", "Cableado"])


def revisar():
    for g in GRUPOS.values():
        assert len(g["titulos"]) <= 15
        for t in g["titulos"]:
            assert len(t) <= 30, t
    for d in DESCRIPCIONES:
        assert len(d) <= 90, (len(d), d)
    for s in SITELINKS:
        assert len(s[0]) <= 25 and len(s[1]) <= 35 and len(s[2]) <= 35, s
    for d in DESTACADOS:
        assert len(d) <= 25, d
    for v in FRAGMENTO[1]:
        assert len(v) <= 25, v


def main():
    revisar()
    cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
    c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
    ga = c.get_service("GoogleAdsService")
    ya = list(ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id FROM campaign WHERE campaign.name = '{NOMBRE}' AND campaign.status != 'REMOVED'"))
    if ya:
        print("La campaña ya existe:", ya[0].campaign.id)
        return

    ops = []
    tmp = iter(range(-1, -1000, -1))

    def op(tipo):
        o = c.get_type("MutateOperation")
        ops.append(o)
        return getattr(o, tipo).create

    presupuesto = f"customers/{CLIENTE}/campaignBudgets/{next(tmp)}"
    b = op("campaign_budget_operation")
    b.resource_name = presupuesto
    b.name = NOMBRE + " - presupuesto"
    b.amount_micros = PRESUPUESTO_DIA * 1_000_000
    b.delivery_method = c.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False

    campana = f"customers/{CLIENTE}/campaigns/{next(tmp)}"
    k = op("campaign_operation")
    k.resource_name = campana
    k.name = NOMBRE
    k.status = c.enums.CampaignStatusEnum.PAUSED
    k.advertising_channel_type = c.enums.AdvertisingChannelTypeEnum.SEARCH
    k.campaign_budget = presupuesto
    k.target_spend.cpc_bid_ceiling_micros = TOPE_CPC * 1_000_000
    k.network_settings.target_google_search = True
    k.network_settings.target_search_network = False
    k.network_settings.target_content_network = False
    k.network_settings.target_partner_search_network = False
    k.geo_target_type_setting.positive_geo_target_type = c.enums.PositiveGeoTargetTypeEnum.PRESENCE
    k.contains_eu_political_advertising = c.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING

    for geo in UBICACIONES:
        cc = op("campaign_criterion_operation")
        cc.campaign = campana
        cc.location.geo_target_constant = f"geoTargetConstants/{geo}"
    cc = op("campaign_criterion_operation")
    cc.campaign = campana
    cc.language.language_constant = f"languageConstants/{ESPANOL}"
    for n in NEGATIVAS:
        cc = op("campaign_criterion_operation")
        cc.campaign = campana
        cc.negative = True
        cc.keyword.text = n
        cc.keyword.match_type = c.enums.KeywordMatchTypeEnum.BROAD

    for nombre, g in GRUPOS.items():
        grupo = f"customers/{CLIENTE}/adGroups/{next(tmp)}"
        a = op("ad_group_operation")
        a.resource_name = grupo
        a.name = nombre
        a.campaign = campana
        a.status = c.enums.AdGroupStatusEnum.ENABLED
        a.type_ = c.enums.AdGroupTypeEnum.SEARCH_STANDARD
        for texto in g["claves"]:
            for tipo in (c.enums.KeywordMatchTypeEnum.PHRASE, c.enums.KeywordMatchTypeEnum.EXACT):
                kw = op("ad_group_criterion_operation")
                kw.ad_group = grupo
                kw.status = c.enums.AdGroupCriterionStatusEnum.ENABLED
                kw.keyword.text = texto
                kw.keyword.match_type = tipo
        ad = op("ad_group_ad_operation")
        ad.ad_group = grupo
        ad.status = c.enums.AdGroupAdStatusEnum.ENABLED
        ad.ad.final_urls.append(URL)
        ad.ad.responsive_search_ad.path1 = "electricista"
        ad.ad.responsive_search_ad.path2 = "mar-del-plata"
        for t in g["titulos"]:
            h = c.get_type("AdTextAsset")
            h.text = t
            ad.ad.responsive_search_ad.headlines.append(h)
        for d in DESCRIPCIONES:
            x = c.get_type("AdTextAsset")
            x.text = d
            ad.ad.responsive_search_ad.descriptions.append(x)

    def recurso(arma, tipo_campo):
        nombre = f"customers/{CLIENTE}/assets/{next(tmp)}"
        a = op("asset_operation")
        a.resource_name = nombre
        arma(a)
        v = op("campaign_asset_operation")
        v.campaign = campana
        v.asset = nombre
        v.field_type = tipo_campo

    def llamada(a):
        a.call_asset.country_code = "AR"
        a.call_asset.phone_number = TELEFONO
    recurso(llamada, c.enums.AssetFieldTypeEnum.CALL)

    for texto, l1, l2, url in SITELINKS:
        def sl(a, texto=texto, l1=l1, l2=l2, url=url):
            a.final_urls.append(url)
            a.sitelink_asset.link_text = texto
            a.sitelink_asset.description1 = l1
            a.sitelink_asset.description2 = l2
        recurso(sl, c.enums.AssetFieldTypeEnum.SITELINK)

    for d in DESTACADOS:
        def co(a, d=d):
            a.callout_asset.callout_text = d
        recurso(co, c.enums.AssetFieldTypeEnum.CALLOUT)

    def fr(a):
        a.structured_snippet_asset.header = FRAGMENTO[0]
        a.structured_snippet_asset.values.extend(FRAGMENTO[1])
    recurso(fr, c.enums.AssetFieldTypeEnum.STRUCTURED_SNIPPET)

    r = ga.mutate(request={"customer_id": CLIENTE, "mutate_operations": ops, "validate_only": not APLICAR})
    print(f"{len(ops)} operaciones", "APLICADAS (campaña en PAUSA)" if APLICAR else "validadas OK")
    if APLICAR:
        for x in r.mutate_operation_responses:
            if x.campaign_result.resource_name:
                print("campaña:", x.campaign_result.resource_name)


if __name__ == "__main__":
    main()
