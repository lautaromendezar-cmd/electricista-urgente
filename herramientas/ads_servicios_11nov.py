"""11-nov-2026 (OK de Lautaro): servicios alineados con Manos Expertas (sin pilares, puesta a tierra, aires, comercios).

1. Borra el grupo «Pilar de luz».
2. «Tableros»: fuera claves de puesta a tierra / cambio de tablero / instalar disyuntor; entran revisión y reparación;
   RSA nuevo de revisión y reparación.
3. Cualquier otro RSA de la campaña con textos prohibidos se reemplaza por uno igual con los textos corregidos.
4. Sitelink «Pilar de luz» → «Zonas de trabajo» (/#zonas). Fragmento estructurado con los servicios de Manos Expertas.

  uv run --with google-ads python herramientas/ads_servicios_11nov.py            → solo valida
  uv run --with google-ads python herramientas/ads_servicios_11nov.py --aplicar
"""
import os
import sys

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.path.expanduser("~/.google-ads-mcp/credentials.json"))
import google.auth  # noqa: E402
from google.ads.googleads.client import GoogleAdsClient  # noqa: E402

CLIENTE = "5864424444"
CAMPANA = 24459234427
APLICAR = "--aplicar" in sys.argv
D = "https://electricistaurgente.com.ar"
PROHIBIDO = ["pilar", "puesta a tierra", "jabalina", "comercio", "fusible", "aires", "edea", "cableado"]

SACAR_CLAVES = {"puesta a tierra", "jabalina puesta a tierra", "cambiar tablero electrico", "cambio de tablero electrico", "instalar disyuntor"}
SUMAR_CLAVES = ["reparacion tablero electrico", "revision tablero electrico", "tablero electrico en falla"]

TABLEROS_TITULOS = ["Reparación de Tableros MdP", "Tablero Eléctrico en Falla", "Revisión de Tableros",
                    "Térmicas y Disyuntores", "Salta la Térmica: Vamos", "Tablero que Huele a Quemado",
                    "Electricista a Domicilio", "Atención las 24 Horas", "Escribinos por WhatsApp",
                    "Precio Antes de Empezar", "Electricista en Mar del Plata", "Mandanos una Foto del Tablero",
                    "Respondemos al Toque", "Encontramos la Falla", "Media Casa Sin Luz: Vamos"]
TABLEROS_DESC = ["Revisamos y reparamos tableros, térmicas y disyuntores en Mar del Plata, las 24 hs.",
                 "Mandanos fotos del tablero por WhatsApp y te decimos cómo seguimos. Sin vueltas.",
                 "Tablero que se calienta, térmicas que saltan o media casa sin luz: buscamos la falla.",
                 "Te decimos cuándo llegamos y cuánto sale la visita antes de salir. Sin sorpresas."]
REEMPLAZOS = {
    "Tableros y Pilares de Luz": "Tableros, Térmicas y Disyuntor",
    "Tableros, pilares, puesta a tierra y cableado. Casas, departamentos y comercios.":
        "Cortocircuitos, olor a quemado y fases caídas. También instalaciones e iluminación.",
    "Fugas a Tierra y Cortos": "Fugas y Cortocircuitos",
}
SITELINK_NUEVO = ("Zonas de trabajo", "Todo Mar del Plata", "Preguntanos por tu barrio", D + "/#zonas")
FRAGMENTO = ["Cortes de luz", "Térmicas y disyuntores", "Tableros", "Cortocircuitos", "Instalaciones", "Iluminación"]


def malo(t):
    return any(p in t.lower() for p in PROHIBIDO)


def main():
    for t in TABLEROS_TITULOS + list(REEMPLAZOS.values())[::2] + [REEMPLAZOS["Fugas a Tierra y Cortos"]]:
        assert len(t) <= 30, t
    for d in TABLEROS_DESC + [REEMPLAZOS["Tableros, pilares, puesta a tierra y cableado. Casas, departamentos y comercios."]]:
        assert len(d) <= 90, (len(d), d)
    cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
    c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
    ga = c.get_service("GoogleAdsService")
    campana = f"customers/{CLIENTE}/campaigns/{CAMPANA}"
    grupos = {f.ad_group.name: f.ad_group.resource_name for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, ad_group.name, ad_group.resource_name FROM ad_group WHERE campaign.id = {CAMPANA} AND ad_group.status != 'REMOVED'")}
    print("grupos:", list(grupos))
    ops = []

    def op(tipo):
        o = c.get_type("MutateOperation")
        ops.append(o)
        return getattr(o, tipo)

    tmp = iter(range(-1, -1000, -1))

    # 1) Grupo Pilar de luz fuera
    if "Pilar de luz" in grupos:
        op("ad_group_operation").remove = grupos["Pilar de luz"]

    # 2) Tableros: claves
    tab = grupos["Tableros"]
    ya = set()
    for f in ga.search(customer_id=CLIENTE, query=f"SELECT ad_group.id, ad_group_criterion.resource_name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group.resource_name = '{tab}' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED' AND ad_group_criterion.negative = FALSE"):
        t = f.ad_group_criterion.keyword.text
        ya.add(t)
        if t in SACAR_CLAVES:
            op("ad_group_criterion_operation").remove = f.ad_group_criterion.resource_name
    for k in SUMAR_CLAVES:
        if k in ya:
            continue
        for mt in (c.enums.KeywordMatchTypeEnum.PHRASE, c.enums.KeywordMatchTypeEnum.EXACT):
            kw = op("ad_group_criterion_operation").create
            kw.ad_group = tab
            kw.status = c.enums.AdGroupCriterionStatusEnum.ENABLED
            kw.keyword.text = k
            kw.keyword.match_type = mt

    # 3) RSA: Tableros nuevo; los demás con textos corregidos
    q = f"""SELECT campaign.id, ad_group.name, ad_group.resource_name, ad_group_ad.resource_name, ad_group_ad.ad.final_urls,
            ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2
            FROM ad_group_ad WHERE campaign.id = {CAMPANA} AND ad_group_ad.status != 'REMOVED' AND ad_group.status != 'REMOVED'"""
    for f in ga.search(customer_id=CLIENTE, query=q):
        if f.ad_group.name == "Pilar de luz":
            continue
        rsa = f.ad_group_ad.ad.responsive_search_ad
        tit = [h.text for h in rsa.headlines]
        des = [d.text for d in rsa.descriptions]
        if f.ad_group.name == "Tableros":
            tit, des = TABLEROS_TITULOS, TABLEROS_DESC
        elif not any(malo(t) for t in tit + des):
            continue
        else:
            tit = [REEMPLAZOS.get(t, t) for t in tit]
            des = [REEMPLAZOS.get(d, d) for d in des]
        sobran = [t for t in tit + des if malo(t)]
        assert not sobran, (f.ad_group.name, sobran)
        a = op("ad_group_ad_operation").create
        a.ad_group = f.ad_group.resource_name
        a.status = c.enums.AdGroupAdStatusEnum.ENABLED
        a.ad.final_urls.extend(list(f.ad_group_ad.ad.final_urls))
        a.ad.responsive_search_ad.path1 = rsa.path1
        a.ad.responsive_search_ad.path2 = rsa.path2
        for t in tit:
            h = c.get_type("AdTextAsset"); h.text = t
            a.ad.responsive_search_ad.headlines.append(h)
        for d in des:
            h = c.get_type("AdTextAsset"); h.text = d
            a.ad.responsive_search_ad.descriptions.append(h)
        op("ad_group_ad_operation").remove = f.ad_group_ad.resource_name
        print("RSA reemplazado en", f.ad_group.name)

    # 4) Sitelink del pilar y fragmento estructurado
    for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, campaign_asset.resource_name, campaign_asset.field_type, asset.final_urls, asset.structured_snippet_asset.values, asset.callout_asset.callout_text FROM campaign_asset WHERE campaign.id = {CAMPANA} AND campaign_asset.status != 'REMOVED'"):
        ft = f.campaign_asset.field_type.name
        if ft == "SITELINK" and any("pilar" in u for u in f.asset.final_urls):
            op("campaign_asset_operation").remove = f.campaign_asset.resource_name
            rn = f"customers/{CLIENTE}/assets/{next(tmp)}"
            a = op("asset_operation").create
            a.resource_name = rn
            a.final_urls.append(SITELINK_NUEVO[3])
            a.sitelink_asset.link_text, a.sitelink_asset.description1, a.sitelink_asset.description2 = SITELINK_NUEVO[:3]
            v = op("campaign_asset_operation").create
            v.campaign, v.asset, v.field_type = campana, rn, c.enums.AssetFieldTypeEnum.SITELINK
            print("sitelink del pilar reemplazado")
        if ft == "STRUCTURED_SNIPPET" and any(malo(x) for x in f.asset.structured_snippet_asset.values):
            op("campaign_asset_operation").remove = f.campaign_asset.resource_name
            rn = f"customers/{CLIENTE}/assets/{next(tmp)}"
            a = op("asset_operation").create
            a.resource_name = rn
            a.structured_snippet_asset.header = "Servicios"
            a.structured_snippet_asset.values.extend(FRAGMENTO)
            v = op("campaign_asset_operation").create
            v.campaign, v.asset, v.field_type = campana, rn, c.enums.AssetFieldTypeEnum.STRUCTURED_SNIPPET
            print("fragmento reemplazado")
        if ft == "CALLOUT" and malo(f.asset.callout_asset.callout_text):
            op("campaign_asset_operation").remove = f.campaign_asset.resource_name
            print("destacado quitado:", f.asset.callout_asset.callout_text)

    ga.mutate(request={"customer_id": CLIENTE, "mutate_operations": ops, "validate_only": not APLICAR})
    print(len(ops), "operaciones", "APLICADAS" if APLICAR else "validadas OK")


if __name__ == "__main__":
    main()
