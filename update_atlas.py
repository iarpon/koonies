import json
import os

with open("/Users/ivan/Documents/koonies/data/campaign_data.json", "r") as f:
    data = json.load(f)

# The 5 curated maps: 1, 2, 3, 4, 7 from Mapas page
curated_atlas = [
    {
        "id": "map_1",
        "title": "Mapa I — Costa de los Naufragios y Región Costera",
        "type": "Cartografía",
        "path": "images/asset_1603148333.jpg",
        "description": "Carta de navegación y mapa general de la Costa de los Naufragios, islas y rutas marítimas."
    },
    {
        "id": "map_2",
        "title": "Mapa II — Plano General de la Ciudad de Elken",
        "type": "Plano de Ciudad",
        "path": "images/asset_1515216225.png",
        "description": "Distribución urbana de Elken: puerto, dársena, campamento kunita extramuros y accesos."
    },
    {
        "id": "map_3",
        "title": "Mapa III — Mapa de Elken para Jugadores",
        "type": "Plano de Ciudad",
        "path": "images/asset_1261867066.png",
        "description": "Mapa detallado con la Taberna del Ganso, Cuartel, Botica de Elara, Templo de Solkarion, Torre de Zenopus y Casa de los Tesoros."
    },
    {
        "id": "map_4",
        "title": "Mapa IV — Plano Costero, Calas y Accesos",
        "type": "Cartografía",
        "path": "images/asset_-583554640.png",
        "description": "Cartografía táctica de las calas piratas, accesos subterráneos a la torre y costas escarpadas."
    },
    {
        "id": "map_7",
        "title": "Mapa V — Rutas Hacia Milborne, Thurmaster y Kanatsu-mi",
        "type": "Cartografía",
        "path": "images/asset_2125889959.png",
        "description": "Carta terrestre del camino fluvial, monolitos sagrados de la Gran Llama y rutas hacia el Río de la Vida."
    }
]

data["atlas"] = curated_atlas

with open("/Users/ivan/Documents/koonies/data/campaign_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open("/Users/ivan/Documents/koonies/data/campaign_data.js", "w", encoding="utf-8") as f:
    f.write("window.CAMPAIGN_DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n")

print(f"Atlas updated. Kept strictly {len(curated_atlas)} maps.")
