import json, os

with open("/Users/ivan/Documents/koonies/extracted_campaign_data.json", "r") as f:
    data = json.load(f)

assets = data["assets"]
for aid, a in list(assets.items())[:30]:
    p = a.get("path")
    n = a.get("name")
    sz = a.get("size", 0)
    print(f"{p} ({n}) - {sz} bytes")
