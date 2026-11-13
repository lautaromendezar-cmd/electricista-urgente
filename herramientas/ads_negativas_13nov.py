"""13/11: negativas en FRASE para búsquedas de cortes de la distribuidora (no buscan electricista).

Apareció «zonas sin luz hoy mar del plata» en el grupo Sin luz. No se usa «sin luz» / «corte de luz»
amplias (en Manos Expertas bloqueaban clientes) ni «hoy» suelta («electricista hoy» es buena).

  uv run --with google-ads python herramientas/ads_negativas_13nov.py            → solo valida
  uv run --with google-ads python herramientas/ads_negativas_13nov.py --aplicar  → aplica
"""
import os
import sys

os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.path.expanduser("~/.google-ads-mcp/credentials.json"))
import google.auth  # noqa: E402
from google.ads.googleads.client import GoogleAdsClient  # noqa: E402

CLIENTE = "5864424444"
CAMPANA = "24459234427"
APLICAR = "--aplicar" in sys.argv
NEGATIVAS_FRASE = ["zonas sin luz", "barrios sin luz", "corte de luz hoy", "cortes de luz hoy"]


def main():
    cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
    c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
    ga = c.get_service("GoogleAdsService")
    q = (f"SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion "
         f"WHERE campaign.id = {CAMPANA} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'")
    ya = {(r.campaign_criterion.keyword.text, r.campaign_criterion.keyword.match_type.name) for r in ga.search(customer_id=CLIENTE, query=q)}
    nuevas = [n for n in NEGATIVAS_FRASE if (n, "PHRASE") not in ya]
    if not nuevas:
        print("Ya estaban todas.")
        return
    svc = c.get_service("CampaignCriterionService")
    ops = []
    for n in nuevas:
        o = c.get_type("CampaignCriterionOperation")
        cc = o.create
        cc.campaign = f"customers/{CLIENTE}/campaigns/{CAMPANA}"
        cc.negative = True
        cc.keyword.text = n
        cc.keyword.match_type = c.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(o)
    svc.mutate_campaign_criteria(request={"customer_id": CLIENTE, "operations": ops, "validate_only": not APLICAR})
    print(len(ops), "negativas", "APLICADAS" if APLICAR else "validadas OK", nuevas)


if __name__ == "__main__":
    main()
