"""Lectura rápida de la cuenta de Ads 586-442-4444 (Electricista Urgente).
uv run --with google-ads python herramientas/ads_leer.py
"""
import os
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", os.path.expanduser("~/.google-ads-mcp/credentials.json"))
import google.auth
from google.ads.googleads.client import GoogleAdsClient

CLIENTE = "5864424444"
cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/adwords"])
c = GoogleAdsClient(credentials=cred, use_proto_plus=True)
print("accesibles:", c.get_service("CustomerService").list_accessible_customers().resource_names)
ga = c.get_service("GoogleAdsService")
for q in [
    "SELECT customer.descriptive_name, customer.currency_code, customer.time_zone, customer.auto_tagging_enabled, customer.status FROM customer",
    "SELECT conversion_action.name, conversion_action.status, conversion_action.type FROM conversion_action",
    "SELECT campaign.name, campaign.status FROM campaign",
    "SELECT billing_setup.status, billing_setup.payments_account_info.payments_account_name FROM billing_setup",
]:
    try:
        for f in ga.search(customer_id=CLIENTE, query=q):
            print(q.split()[1].split('.')[0], f)
    except Exception as e:
        print("ERROR", q[:50], str(e)[:400])
