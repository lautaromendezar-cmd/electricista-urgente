"""11-nov-2026: coherencia anuncios ↔ web antes de mandarle el link a Dario.

1. RSA: fuera «cuánto sale la visita» (no se sabe si se cobra) y «Batán» (las zonas son las de La Perla).
2. Sitelink «Tableros eléctricos»: decía «Cambio y armado / puesta a tierra» → revisión y reparación.
3. Ubicaciones: suma Miramar y el partido de Villa Gesell (Villa Gesell, Mar de las Pampas, Mar Azul), como La Perla.

  uv run --with google-ads python herramientas/ads_coherencia_11nov.py            → solo valida
  uv run --with google-ads python herramientas/ads_coherencia_11nov.py --aplicar
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
REEMPLAZOS = {
    "Te decimos cuándo llegamos y cuánto sale la visita antes de salir. Sin sorpresas.":
        "Te decimos cuándo llegamos y te pasamos el precio antes de empezar. Sin sorpresas.",
    "Batán, Sierra y Santa Clara": "De Mar del Plata a Mar Azul",
}
PROHIBIDO = ["visita", "batán", "batan", "pilar", "puesta a tierra", "comercio", "armado"]
SITELINK_TABLEROS = ("Tableros eléctricos", "Revisión y reparación", "Térmicas y disyuntores", D + "/tableros-electricos")
UBICACIONES_NUEVAS = [9255017, 9243464]  # Miramar (Bs. As.), Villa Gesell Partido


def malo(t):
    return any(p in t.lower() for p in PROHIBIDO)


def main():
    for v in REEMPLAZOS.values():
        assert len(v) <= 90
    assert len(REEMPLAZOS["Batán, Sierra y Santa Clara"]) <= 30
    cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
    c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
    ga = c.get_service("GoogleAdsService")
    campana = f"customers/{CLIENTE}/campaigns/{CAMPANA}"
    ops = []

    def op(tipo):
        o = c.get_type("MutateOperation")
        ops.append(o)
        return getattr(o, tipo)

    q = f"""SELECT campaign.id, ad_group.name, ad_group.resource_name, ad_group_ad.resource_name, ad_group_ad.ad.final_urls,
            ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2
            FROM ad_group_ad WHERE campaign.id = {CAMPANA} AND ad_group_ad.status != 'REMOVED' AND ad_group.status != 'REMOVED'"""
    for f in ga.search(customer_id=CLIENTE, query=q):
        rsa = f.ad_group_ad.ad.responsive_search_ad
        tit = [REEMPLAZOS.get(h.text, h.text) for h in rsa.headlines]
        des = [REEMPLAZOS.get(d.text, d.text) for d in rsa.descriptions]
        if tit == [h.text for h in rsa.headlines] and des == [d.text for d in rsa.descriptions]:
            continue
        assert not [t for t in tit + des if malo(t)], (f.ad_group.name, [t for t in tit + des if malo(t)])
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
        print("RSA corregido:", f.ad_group.name)

    tmp = iter(range(-1, -100, -1))
    for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, campaign_asset.resource_name, asset.sitelink_asset.link_text, asset.sitelink_asset.description1, asset.sitelink_asset.description2 FROM campaign_asset WHERE campaign.id = {CAMPANA} AND campaign_asset.field_type = 'SITELINK' AND campaign_asset.status != 'REMOVED'"):
        sl = f.asset.sitelink_asset
        if malo(sl.link_text + " " + sl.description1 + " " + sl.description2):
            op("campaign_asset_operation").remove = f.campaign_asset.resource_name
            rn = f"customers/{CLIENTE}/assets/{next(tmp)}"
            a = op("asset_operation").create
            a.resource_name = rn
            a.final_urls.append(SITELINK_TABLEROS[3])
            a.sitelink_asset.link_text, a.sitelink_asset.description1, a.sitelink_asset.description2 = SITELINK_TABLEROS[:3]
            v = op("campaign_asset_operation").create
            v.campaign, v.asset, v.field_type = campana, rn, c.enums.AssetFieldTypeEnum.SITELINK
            print("sitelink corregido:", sl.link_text, "/", sl.description1, "/", sl.description2)

    ya = {f.campaign_criterion.location.geo_target_constant for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = {CAMPANA} AND campaign_criterion.type = 'LOCATION'")}
    for g in UBICACIONES_NUEVAS:
        if f"geoTargetConstants/{g}" in ya:
            continue
        cc = op("campaign_criterion_operation").create
        cc.campaign = campana
        cc.location.geo_target_constant = f"geoTargetConstants/{g}"
        print("ubicación sumada:", g)

    ga.mutate(request={"customer_id": CLIENTE, "mutate_operations": ops, "validate_only": not APLICAR})
    print(len(ops), "operaciones", "APLICADAS" if APLICAR else "validadas OK")


if __name__ == "__main__":
    main()
