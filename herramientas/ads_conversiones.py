"""Crea «Clic WhatsApp web» y «Clic llamar web» en 586-442-4444 e imprime las etiquetas send_to.
uv run --with google-ads python herramientas/ads_conversiones.py [--aplicar]
"""
import os, sys, re
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.path.expanduser("~/.google-ads-mcp/credentials.json"))
import google.auth
from google.ads.googleads.client import GoogleAdsClient

CLIENTE = "5864424444"
APLICAR = "--aplicar" in sys.argv
NOMBRES = ["Clic WhatsApp web", "Clic llamar web"]
cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
ga = c.get_service("GoogleAdsService")

def existentes():
    q = "SELECT conversion_action.name, conversion_action.tag_snippets FROM conversion_action WHERE conversion_action.status != 'REMOVED'"
    return {f.conversion_action.name: f.conversion_action for f in ga.search(customer_id=CLIENTE, query=q)}

faltan = [n for n in NOMBRES if n not in existentes()]
ops = []
for n in faltan:
    op = c.get_type("ConversionActionOperation"); ca = op.create
    ca.name = n
    ca.type_ = c.enums.ConversionActionTypeEnum.WEBPAGE
    ca.category = c.enums.ConversionActionCategoryEnum.CONTACT
    ca.status = c.enums.ConversionActionStatusEnum.ENABLED
    ca.counting_type = c.enums.ConversionActionCountingTypeEnum.ONE_PER_CLICK
    ca.click_through_lookback_window_days = 30
    ca.value_settings.default_value = 1
    ca.value_settings.always_use_default_value = True
    ops.append(op)
if ops:
    r = c.get_service("ConversionActionService").mutate_conversion_actions(
        request={"customer_id": CLIENTE, "operations": ops, "validate_only": not APLICAR})
    print("creadas" if APLICAR else "validadas", faltan)
for n, ca in existentes().items():
    for s in ca.tag_snippets:
        m = re.search(r"send_to': '([^']+)'", s.event_snippet)
        if m: print(n, "->", m.group(1)); break
