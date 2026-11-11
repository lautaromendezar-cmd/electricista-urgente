"""Ajustes del 10-nov-2026 en 586-442-4444, con OK de Lautaro:
1. Presupuesto a $6.000/día.
2. Sin medios de pago (no confirmados, criterio de Manos Expertas): saca el destacado «Pagás con Mercado Pago»
   y reemplaza los anuncios RSA por versiones sin «Mercado Pago» (el texto de un RSA no se edita: se crea otro y se borra el viejo).
3. Habilita la campaña.

  uv run --with google-ads python herramientas/ads_ajustes_10nov.py            → solo valida
  uv run --with google-ads python herramientas/ads_ajustes_10nov.py --aplicar
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
PRESUPUESTO_DIA = 6_000
URL = "https://electricistaurgente.com.ar/"
QUITAR = ["Pagá con Mercado Pago"]
NUEVOS_TITULOS = {"Pagá con Mercado Pago": "Te Pasamos el Precio Antes"}
DESCRIPCIONES = [
    "Electricista urgente en Mar del Plata, las 24 hs. Mandanos un WhatsApp y vamos a tu casa.",
    "Cortes de luz, térmica o disyuntor que salta, olor a quemado. Te pasamos el precio antes.",
    "Te decimos cuándo llegamos y cuánto sale la visita antes de salir. Sin sorpresas.",
    "Tableros, pilares, puesta a tierra y cableado. Casas, departamentos y comercios.",
]

cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
ga = c.get_service("GoogleAdsService")
v = not APLICAR
for d in DESCRIPCIONES:
    assert len(d) <= 90, d
for t in NUEVOS_TITULOS.values():
    assert len(t) <= 30, t

# 1) Presupuesto
f = next(iter(ga.search(customer_id=CLIENTE, query=f"SELECT campaign.campaign_budget FROM campaign WHERE campaign.id = {CAMPANA}")))
op = c.get_type("CampaignBudgetOperation")
op.update.resource_name = f.campaign.campaign_budget
op.update.amount_micros = PRESUPUESTO_DIA * 1_000_000
op.update_mask.CopyFrom(protobuf_helpers.field_mask(None, op.update._pb))
c.get_service("CampaignBudgetService").mutate_campaign_budgets(request={"customer_id": CLIENTE, "operations": [op], "validate_only": v})
print("presupuesto:", PRESUPUESTO_DIA)

# 2a) Destacado de Mercado Pago fuera de la campaña
ops = []
for f in ga.search(customer_id=CLIENTE, query=f"SELECT campaign.id, campaign_asset.resource_name, asset.callout_asset.callout_text FROM campaign_asset WHERE campaign.id = {CAMPANA} AND campaign_asset.field_type = 'CALLOUT' AND campaign_asset.status != 'REMOVED'"):
    if "Mercado Pago" in f.asset.callout_asset.callout_text:
        o = c.get_type("CampaignAssetOperation")
        o.remove = f.campaign_asset.resource_name
        ops.append(o)
if ops:
    c.get_service("CampaignAssetService").mutate_campaign_assets(request={"customer_id": CLIENTE, "operations": ops, "validate_only": v})
print("destacados quitados:", len(ops))

# 2b) RSA nuevos sin medios de pago, viejos borrados
q = f"""SELECT campaign.id, ad_group_ad.resource_name, ad_group.resource_name, ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions FROM ad_group_ad
        WHERE campaign.id = {CAMPANA} AND ad_group_ad.status != 'REMOVED'"""
crear, borrar = [], []
for f in ga.search(customer_id=CLIENTE, query=q):
    rsa = f.ad_group_ad.ad.responsive_search_ad
    textos = [h.text for h in rsa.headlines] + [d.text for d in rsa.descriptions]
    if not any("Mercado Pago" in t for t in textos):
        continue
    o = c.get_type("AdGroupAdOperation")
    a = o.create
    a.ad_group = f.ad_group.resource_name
    a.status = c.enums.AdGroupAdStatusEnum.ENABLED
    a.ad.final_urls.append(URL)
    a.ad.responsive_search_ad.path1 = "electricista"
    a.ad.responsive_search_ad.path2 = "mar-del-plata"
    for h in rsa.headlines:
        x = c.get_type("AdTextAsset")
        x.text = NUEVOS_TITULOS.get(h.text, h.text)
        a.ad.responsive_search_ad.headlines.append(x)
    for d in DESCRIPCIONES:
        x = c.get_type("AdTextAsset")
        x.text = d
        a.ad.responsive_search_ad.descriptions.append(x)
    crear.append(o)
    b = c.get_type("AdGroupAdOperation")
    b.remove = f.ad_group_ad.resource_name
    borrar.append(b)
if crear:
    c.get_service("AdGroupAdService").mutate_ad_group_ads(request={"customer_id": CLIENTE, "operations": crear + borrar, "validate_only": v})
print("anuncios reemplazados:", len(crear))

# 3) Habilitar
op = c.get_type("CampaignOperation")
op.update.resource_name = f"customers/{CLIENTE}/campaigns/{CAMPANA}"
op.update.status = c.enums.CampaignStatusEnum.ENABLED
op.update_mask.CopyFrom(protobuf_helpers.field_mask(None, op.update._pb))
c.get_service("CampaignService").mutate_campaigns(request={"customer_id": CLIENTE, "operations": [op], "validate_only": v})
print("campaña:", "HABILITADA" if APLICAR else "validada")
