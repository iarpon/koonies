import json
import os
import re
import math

ROOT_DIR = "/Users/ivan/Documents/koonies"
DATA_DIR = os.path.join(ROOT_DIR, "data")
WIKI_DIR = os.path.join(ROOT_DIR, "wiki")
IMG_DIR = os.path.join(ROOT_DIR, "images")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(WIKI_DIR, "personajes"), exist_ok=True)
os.makedirs(os.path.join(WIKI_DIR, "sesiones"), exist_ok=True)
os.makedirs(os.path.join(WIKI_DIR, "pnjs"), exist_ok=True)
os.makedirs(os.path.join(WIKI_DIR, "lore_y_misterios"), exist_ok=True)
os.makedirs(os.path.join(WIKI_DIR, "mapas"), exist_ok=True)

with open(os.path.join(ROOT_DIR, "extracted_campaign_data.json"), "r", encoding="utf-8") as f:
    raw_data = json.load(f)

pages = raw_data["pages"]
pages_by_name = {p["name"]: p for p in pages}

# Helper: Distance
def dist(p1, p2):
    return math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])

def find_nearest_images(x, y, images, max_dist=1200, limit=2):
    pos = {"x": x, "y": y}
    sorted_imgs = sorted(images, key=lambda img: dist(pos, img))
    return [img["image_info"]["path"] for img in sorted_imgs if dist(pos, img) < max_dist and img.get("image_info", {}).get("path")][:limit]

# -------------------------------------------------------------
# 1. CURATE CHARACTERS (LOS KOONIES - PJ's)
# -------------------------------------------------------------
pj_page = pages_by_name.get("Personajes", {})
pj_texts = pj_page.get("texts", [])
pj_images = pj_page.get("images", [])

koonies_roster = [
    {
        "id": "glunt",
        "name": "Glunt",
        "title": "El Gigante de Corazón de Cristal",
        "role": "Guerrero / Protector",
        "archetype": "Fuerza colosal (Fuerza 17), alma noble, inocente y protectora de los pequeños.",
        "quote": "Padre dijo que me quedara. Glunt se queda. Glunt cuidará de los pequeños hasta que el sol vuelva a salir.",
        "icon": "shield",
        "badge_color": "emerald",
        "accent": "#10b981",
        "primary_image": "images/asset_-929693943.jpg", # Glunt.jpg
        "match_keys": ["Glunt", "Gigante de Corazón", "Glunt:"],
        "curse_status": "Maldición de las Venas Negras (contraída en la Torre de Zenopus, contenida tras las aguas de Kanatsu-mi)."
    },
    {
        "id": "hiroyuki",
        "name": "Hiroyuki Watanabe",
        "title": "El Acero en la Forja",
        "role": "Guerrero Kunita / Kensei Samurai",
        "archetype": "Honor marcial, devoción a Hachiman y escudo inquebrantable de los supervivientes.",
        "quote": "Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.",
        "icon": "swords",
        "badge_color": "amber",
        "accent": "#f59e0b",
        "primary_image": "images/asset_1793380967.jpg", # Hiro.jpg
        "match_keys": ["Hiroyuki", "Hiroyuki Watanabe", "El Acero en la Forja"]
    },
    {
        "id": "katsumi",
        "name": "Katsumi",
        "title": "La Llama Custodia",
        "role": "Clériga de Shien (La Llama Púrpura) / Líder Espiritual",
        "archetype": "Defensora con naginata y guía moral de los 40 refugiados kunitas.",
        "quote": "Soy Katsumi, una Llama Custodia consagrada al servicio de Shien. Mi vida está ligada a la naginata y al deber de proteger a mi pueblo.",
        "icon": "flame",
        "badge_color": "purple",
        "accent": "#a855f7",
        "primary_image": "images/asset_154989466.png",
        "match_keys": ["Katsumi", "Llama Custodia", "Shien"]
    },
    {
        "id": "sakura",
        "name": "Sakura",
        "title": "La Erudita de lo Arcano",
        "role": "Maga Kunita / Investigadora de Grimorios",
        "archetype": "Intelecto analítico, descifradora de secretos antiguos y portadora del Ojo de J'karaa.",
        "quote": "El conocimiento no es peligroso; ignorar sus consecuencias sí lo es.",
        "icon": "sparkles",
        "badge_color": "pink",
        "accent": "#ec4899",
        "primary_image": "images/asset_1843595399.jpg", # Sakura.jpg
        "match_keys": ["Sakura", "Maga kunita", "tercer ojo"]
    },
    {
        "id": "ainur",
        "name": "Ainur",
        "title": "El Ojo Atento",
        "role": "Explorador / Vigilante",
        "archetype": "Carisma, sigilo, percepción aguda y rastreo en las sombras.",
        "quote": "La niebla oculta muchas cosas, pero ninguna que no deje rastro.",
        "icon": "eye",
        "badge_color": "indigo",
        "accent": "#6366f1",
        "primary_image": "images/asset_1067045487.jpg", # Ainur.jpg
        "match_keys": ["Ainur", "Ojo de J'karaa", "Airun"]
    },
    {
        "id": "kazgrim",
        "name": "Kazgrim Iwakura (Kaz)",
        "title": "El Guardián de la Llama Perdida",
        "role": "Cantero Enano / Acólito de Kagutsuchi",
        "archetype": "Joven cantero de piedra volcánica (38 años) que escucha a los kami y despierta el fuego renaciente.",
        "quote": "El papel arde, pero la verdad es incombustible. Si el fuego lo devoró todo, es porque algo nuevo y más fuerte debe nacer de nuestras cenizas.",
        "icon": "hammer",
        "badge_color": "orange",
        "accent": "#ea580c",
        "primary_image": "images/asset_1063611285.jpg", # Kaz.jpg
        "match_keys": ["Kazgrim", "Kaz", "Kazrim", "Iwakura", "Kagutsuchi", "La historia de Kazrim"]
    }
]

# Map texts to characters
for k in koonies_roster:
    matched_texts = []
    matched_images = []
    for t in pj_texts:
        txt = t["text"]
        if any(key.lower() in txt.lower() for key in k["match_keys"]):
            matched_texts.append(txt)
            imgs = find_nearest_images(t["x"], t["y"], pj_images, max_dist=1200, limit=3)
            matched_images.extend(imgs)
    
    k["full_lore"] = "\n\n".join(matched_texts) if matched_texts else f"Miembro fundador de Los Koonies. {k['archetype']}."
    k["gallery"] = list(set([k["primary_image"]] + matched_images))
    k["gallery"] = [img for img in k["gallery"] if os.path.exists(os.path.join(ROOT_DIR, img))]

print(f"Curated {len(koonies_roster)} Koonies player characters.")

# -------------------------------------------------------------
# 2. CURATE SESSIONS (1 to 16)
# -------------------------------------------------------------
session_titles_curated = {
    1: {"title": "La Danza de las Cadenas — El Despertar en la Playa", "act": "Acto I: Naufragio en la Isla de Viladel", "in_game": "15 de Sulmar, Año 18 CL", "loc": "Isla de Viladel — Costa del Naufragio"},
    2: {"title": "Sangre en la Colina — El Barranco de los Trasgos", "act": "Acto I: Naufragio en la Isla de Viladel", "in_game": "20 de Sulmar, Año 18 CL", "loc": "Isla de la Tortuga — Colinas Heladas"},
    3: {"title": "La Visión de Liryel & La Mansión de Viledel", "act": "Acto I: Naufragio en la Isla de Viladel", "in_game": "24 de Sulmar, Año 18 CL", "loc": "Templo de la Diosa — Mansión de Viledel"},
    4: {"title": "Las Catacumbas de Viledel — La Traición de Keestake", "act": "Acto I: Naufragio en la Isla de Viladel", "in_game": "26 de Sulmar, Año 18 CL", "loc": "Catacumbas Subterráneas de Viledel"},
    5: {"title": "Diario de Navegación — El Escape de Korinn en el Rimed Mallow", "act": "Acto II: La Travesía por el Mar de las Nieblas", "in_game": "2 de Iryn, Año 19 CL", "loc": "Mar Abierto — A bordo del Rimed Mallow"},
    6: {"title": "La Llegada a Elken — Refugio en Tierra Extraña", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "12 de Iryn, Año 19 CL", "loc": "Ciudad de Elken — Costa de los Naufragios"},
    7: {"title": "La Noche del Ganso y la Mañana del Mago", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "13 de Iryn, Año 19 CL", "loc": "Taberna del Ganso — Almacenes del Puerto"},
    8: {"title": "Los Koonies y la Niebla que No Perdona", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "13 de Iryn (Noche), Año 19 CL", "loc": "Puertas de Elken — La Torre de la Niebla"},
    9: {"title": "El Dedo de Kaz y el Secreto de la Torre Cerca del Cementerio", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "14 de Iryn, Año 19 CL", "loc": "Torre del Cementerio de Elken"},
    10: {"title": "La Bóveda Prohibida — Pócimas y Manos Esqueléticas", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "14 de Iryn (Tarde), Año 19 CL", "loc": "Criptas y Bóvedas de Zenopus"},
    11: {"title": "La Máscara Habla — Revelaciones de Mandra Voss", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "15 de Iryn, Año 19 CL", "loc": "La Casa de los Tesoros — Sala de la Máscara"},
    12: {"title": "Anamnesis — El Diario Oculto de Zenopus y Kanatsu-mi", "act": "Acto III: La Ciudad Fronteriza de Elken", "in_game": "16 de Iryn, Año 19 CL", "loc": "Estudio Superior de la Torre de Zenopus"},
    13: {"title": "Cadenas, Caminos y el Símbolo de Kagutsuchi", "act": "Acto IV: La Marcha a Milborne y Thurmaster", "in_game": "17-19 de Iryn, Año 19 CL", "loc": "Camino Fluvial de Elken hacia Milborne"},
    14: {"title": "El Monolito del Río y la Senda del Musgo", "act": "Acto IV: La Marcha a Milborne y Thurmaster", "in_game": "20 de Iryn, Año 19 CL", "loc": "Monolito de la Gran Llama — Ribera del Río"},
    15: {"title": "La Caverna de las Columnas Olvidadas", "act": "Acto IV: La Marcha a Milborne y Thurmaster", "in_game": "21 de Iryn, Año 19 CL", "loc": "Cueva Ancestral de Construcción Tosca"},
    16: {"title": "La Hija del Molinero, el Enano que Recordaba y la Fuente de Vida", "act": "Acto IV: La Marcha a Milborne y Thurmaster", "in_game": "22-24 de Iryn, Año 19 CL", "loc": "Milborne, Thurmaster y Kanatsu-mi"}
}

curated_sessions = []
session_pages = [p for p in pages if re.match(r'^Sesi[oó]n\s+\d+', p["name"], re.IGNORECASE)]
def get_session_num(pname):
    m = re.search(r'\d+', pname)
    return int(m.group(0)) if m else 999
session_pages.sort(key=lambda p: get_session_num(p["name"]))

for sp in session_pages:
    s_num = get_session_num(sp["name"])
    texts = sp.get("texts", [])
    images = sp.get("images", [])
    
    meta = session_titles_curated.get(s_num, {
        "title": f"Sesión {s_num}",
        "act": "Crónica de Aventuras",
        "in_game": "Fecha desconocida",
        "loc": "Costa de los Naufragios"
    })
    
    irl_date = ""
    date_m = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', sp["name"])
    if date_m:
        irl_date = date_m.group(1)
        
    ordered_texts = sorted(texts, key=lambda x: (x["y"], x["x"]))
    blocks = []
    xp_found = ""
    
    for t in ordered_texts:
        raw_t = t["text"].strip()
        if "PX:" in raw_t or "PX " in raw_t or "Experiencia:" in raw_t:
            xp_found = raw_t
            
        imgs = find_nearest_images(t["x"], t["y"], images, max_dist=1200, limit=2)
        valid_imgs = [img for img in imgs if os.path.exists(os.path.join(ROOT_DIR, img))]
        blocks.append({
            "text": raw_t,
            "images": valid_imgs
        })
        
    all_imgs = [img["image_info"]["path"] for img in images if img.get("image_info", {}).get("path") and os.path.exists(os.path.join(ROOT_DIR, img["image_info"]["path"]))]
    
    full_narrative = "\n\n".join(b["text"] for b in blocks)
    summary_snippet = ""
    for b in blocks:
        for pgraph in b["text"].split("\n\n"):
            pgraph = pgraph.strip()
            if len(pgraph) > 80 and not pgraph.startswith("#") and not pgraph.startswith("-"):
                summary_snippet = pgraph[:280] + "..."
                break
        if summary_snippet:
            break
            
    curated_sessions.append({
        "number": s_num,
        "title": meta["title"],
        "act": meta["act"],
        "irl_date": irl_date,
        "in_game_date": meta["in_game"],
        "location": meta["loc"],
        "xp": xp_found or "200-350 PX",
        "summary": summary_snippet or "Los Koonies continúan su odisea a través de tierras inhóspitas y misterios arcanos.",
        "blocks": blocks,
        "images": all_imgs,
        "full_text": full_narrative
    })

print(f"Curated {len(curated_sessions)} sessions.")

# -------------------------------------------------------------
# 3. CURATE NPCS (DRAMATIS PERSONAE)
# -------------------------------------------------------------
curated_npcs = [
    {
        "name": "Jelenneth (Jenneleth)",
        "nickname": "La Maga Samaritana",
        "role": "Maga y Sanadora / Aprendiz de Tauster",
        "location": "Milborne & Thurmaster",
        "faction": "Aliada Íntima de Sakura y Los Koonies",
        "attitude": "Muy amigable / 'Hermana de corazón' de Sakura",
        "status": "Viva",
        "notes": "Chica joven con capa azul y bolsa de viaje pesada. Aprendiz del mago Tauster. Examinó el Ojo de J'karaa con gran urgencia y guió al grupo hasta Thurmaster.",
        "image": "images/asset_587532380.png"
    },
    {
        "name": "Tauster",
        "nickname": "El Mago de la Torre de Thurmaster",
        "role": "Mago veterano, erudito y maestro de Jelenneth",
        "location": "Thurmaster",
        "faction": "Independiente / Círculo Arcano",
        "attitude": "Paranoico, brillante y desconfiado",
        "status": "Vivo",
        "notes": "Bajo, panzudo y de mirada inquisitiva. Identificó los objetos mágicos del grupo. Urge al grupo a encontrar una reliquia antes que sus rivales y desea comprar el anillo de la torre de Zenopus.",
        "image": "images/asset_-1273186683.png"
    },
    {
        "name": "El Viejo Oso",
        "nickname": "El Enano de la Ciudadela Perdida",
        "role": "Veterano enano y bebedor en Milborne",
        "location": "Posada de Milborne",
        "faction": "Clanes Enanos de las Montañas",
        "attitude": "Amistoso / Revelador de secretos",
        "status": "Vivo",
        "notes": "Cojea de una pierna rota en su juventud al intentar reconquistar su ciudadela enana. Reveló la existencia de forjas colosales y escrituras que coinciden con los templos kunitas.",
        "image": "images/asset_1063611285.jpg"
    },
    {
        "name": "Mandra Voss",
        "nickname": "La Anticuaria de los Arcanos",
        "role": "Dueña de 'La Casa de los Tesoros'",
        "location": "Ciudad de Elken",
        "faction": "Independiente / Coleccionista Arcana",
        "attitude": "Aliada comercial / Interés en grimorios y reliquias",
        "status": "Desaparecida tras la Sesión XI",
        "notes": "Intercambió saberes mágicos con Sakura por el libro de Zarcand. Al ver el Ojo de J'karaa cerró la tienda precipitadamente y desapareció.",
        "image": "images/asset_-2095511646.png"
    },
    {
        "name": "Elara Frin",
        "nickname": "La Dulce Herbolaria",
        "role": "Boticaria y Maestra de Remedios",
        "location": "Botica de Elara, Elken",
        "faction": "Amiga y Aliada de Los Koonies",
        "attitude": "Muy amigable y cooperativa",
        "status": "Viva",
        "notes": "Siempre huele a tomillo y lleva flores silvestres en el cabello. Provee ungüentos curativos al grupo y rastrea rumores sobre refugiados kunitas.",
        "image": "images/asset_-251637396.jpg"
    },
    {
        "name": "Rurik Feldon",
        "nickname": "El Brazo Firme de Elken",
        "role": "Capitán de la Guardia de la Ciudad",
        "location": "Cuartel del Puerto, Elken",
        "faction": "Guardia de Elken",
        "attitude": "Justo, inteligente e imparcial",
        "status": "Vivo",
        "notes": "Hombre honorable de mediana edad. Respeta a Los Koonies tras sus intervenciones contra el contrabando y matones en el puerto.",
        "image": "images/asset_-1610812971.png"
    },
    {
        "name": "Seraphine Alondar",
        "nickname": "La Voz de Solkarion (La Xenófoba)",
        "role": "Escribana Real, Magistrada y Clériga de Solkarion",
        "location": "Tribunal y Templo de Solkarion, Elken",
        "faction": "Culto de Solkarion / Corona de Thir",
        "attitude": "Hostil / Desconfiada de extranjeros",
        "status": "Viva",
        "notes": "Fanática religiosa que rechaza a los no devotos de Solkarion. Trata a los refugiados kunitas con recelo y burocracia extrema.",
        "image": "images/asset_-1273186683.png"
    },
    {
        "name": "Mirna",
        "nickname": "La Loba de los Mares",
        "role": "Capitana del Rimed Mallow & Miembro del Consejo",
        "location": "Puerto de Elken / Mar Abierto",
        "faction": "Marineros / Consejo de Elken",
        "attitude": "Pragmática y calculadora",
        "status": "Viva",
        "notes": "Veterana capitana que rescató a los Koonies en Korinn. Maneja negocios en las sombras pero mantiene el orden naval.",
        "image": "images/asset_1497705276.png"
    },
    {
        "name": "Kaito",
        "nickname": "El Carpintero Pragmático",
        "role": "Consejero del Campamento Kunita",
        "location": "Campamento Kunita, Elken",
        "faction": "Refugiados de Amatsukuni",
        "attitude": "Favorable y constructivo",
        "status": "Vivo",
        "notes": "Defiende la protección de los niños ante todo. Agradeció enormemente la devolución de bienes recuperados de la cala pirata.",
        "image": "images/asset_1815133749.png"
    },
    {
        "name": "Hanae",
        "nickname": "La Maestra Custodia",
        "role": "Maestra y Cronista Kunita",
        "location": "Campamento Kunita, Elken",
        "faction": "Refugiados de Amatsukuni",
        "attitude": "Favorable pero cautelosa",
        "status": "Viva",
        "notes": "Conserva la memoria histórica de Amatsukuni y el culto a Solkario el Dragón Dorado y los Antiguos Reyes Nigromantes de Thir.",
        "image": "images/asset_587532380.png"
    },
    {
        "name": "Bruiser Holloway",
        "nickname": "El Rostro del Dragón",
        "role": "Ladrón de Caballos y Forajido",
        "location": "Costa de los Naufragios / Prófugo",
        "faction": "Bandidos de Sutter Izen",
        "attitude": "Hostil / Criminal",
        "status": "En busca y captura (1.000 PO)",
        "notes": "Porta un tatuaje de dragón distintivo en el rostro. Se le vincula al contrabando de monturas en la frontera.",
        "image": "images/asset_-2095511646.png"
    },
    {
        "name": "Keestake",
        "nickname": "El Traidor de Viledel",
        "role": "Antiguo Chambelán del Rey de Viladel",
        "location": "Mansión y Catacumbas de Viledel",
        "faction": "Supervivientes Corruptos de Viladel",
        "attitude": "Traidor / Manipulador",
        "status": "Muerto (Sesión III)",
        "notes": "Guió al grupo prometiendo una salida de la isla para luego tenderles una emboscada en las catacumbas.",
        "image": "images/asset_-1610812971.png"
    },
    {
        "name": "Zenopus (Zenotus)",
        "nickname": "El Mago de las Profundidades",
        "role": "Archimago Nigromante / Erudito Olvidado",
        "location": "Torre de Zenopus, Elken (Histórico)",
        "faction": "Círculo Arcano de Thir",
        "attitude": "Misterio Histórico",
        "status": "Desaparecido / Fallecido hace siglos",
        "notes": "Construyó la torre sobre una ruina primordial. Descubrió la maldición de las venas negras y el remedio de Kanatsu-mi en el Río de la Vida.",
        "image": "images/asset_1659737080.png"
    },
    {
        "name": "Zarcand (Z.)",
        "nickname": "El Nigromante del Tercer Ojo",
        "role": "Nigromante de los Callejones",
        "location": "Bajos Fondos de Elken",
        "faction": "Cultos Prohibidos",
        "attitude": "Enemigo Mortal",
        "status": "Malherido / En paradero desconocido",
        "notes": "Sakura le abrió una herida que parece un 'tercer ojo' en la frente durante el enfrentamiento en el almacén.",
        "image": "images/asset_-1273186683.png"
    }
]

for npc in curated_npcs:
    if not os.path.exists(os.path.join(ROOT_DIR, npc["image"])):
        for aid, a in raw_data["assets"].items():
            if a.get("path") and os.path.exists(os.path.join(ROOT_DIR, a["path"])):
                npc["image"] = a["path"]
                break

print(f"Curated {len(curated_npcs)} key NPCs.")

# -------------------------------------------------------------
# 4. CURATE MYSTERIES & LOOSE ENDS (TABLERO DE MISTERIOS)
# -------------------------------------------------------------
mysteries = [
    {
        "id": "maldicion-glunt",
        "title": "La Maldición de las Venas Negras de Glunt",
        "priority": "Alta",
        "status": "Contenida / Curada en Kanatsu-mi",
        "category": "Salud de los Koonies",
        "description": "Las venas negras que ascendían por la pierna de Glunt han remitido tras la expedición a Kanatsu-mi en el sur de Thurmaster (el Río de la Vida). La conexión con Zenopus y el origen de la plaga arcana sigue siendo investigada.",
        "clues": [
            "Descubierto en el compartimento secreto de la torre de Zenopus.",
            "Zenopus sufrió el mismo mal y dejó notas sobre Kanatsu-mi ('El Primer Agua').",
            "Glunt muestra una gran mejoría al regresar a Milborne."
        ]
    },
    {
        "id": "ciudadela-enana-kaz",
        "title": "La Ciudadela Enana Perdida y el Templo de Kaz",
        "priority": "Alta",
        "status": "Nueva Pista Crítica",
        "category": "Destino de Kazrim",
        "description": "El Viejo Oso reveló en Milborne la existencia de una fortaleza enana en las montañas con una forja colosal y escrituras idénticas a los monolitos de Kagutsuchi. Kazrim siente la llamada de los kami para descubrir si este santuario ancestral aguarda ser despertado.",
        "clues": [
            "El Viejo Oso perdió su hogar de niño e intentó reconquistarlo.",
            "Valle oculto accesible desde los niveles subterráneos de la montaña.",
            "Escrituras que coinciden con los símbolos sagrados de Amatsukuni."
        ]
    },
    {
        "id": "colgante-ojo-jkaraa",
        "title": "El Enigma del Ojo de J'karaa & Tauster",
        "priority": "Alta",
        "status": "En Manos de Sakura",
        "category": "Artefactos Arcanos",
        "description": "Ainur cedió el colgante a Sakura tras el análisis urgente de Jelenneth y Tauster. Tauster advierte que fuerzas oscuras buscan este artefacto con desesperación y pide al grupo adelantarse a sus enemigos.",
        "clues": [
            "El nigromante Zarcand intentó robarlo en los almacenes.",
            "Mandra Voss huyó tras reconocer su forma.",
            "Tauster ofreció identificar objetos a cambio de que el grupo ayude a Jelenneth."
        ]
    },
    {
        "id": "refugiados-kunitas",
        "title": "El Futuro y Seguridad del Pueblo de Amatsukuni",
        "priority": "Media",
        "status": "Activo",
        "category": "Pueblo y Política",
        "description": "40 refugiados kunitas sobreviven hacinados en el campamento extramuros de Elken bajo la tutela de Katsumi, Kaito y Hanae. Las autoridades de Thir son xenófobas y los miran con recelo. Se busca un asentamiento permanente seguro.",
        "clues": [
            "La sacerdotisa Yoriko Asano sigue en paradero desconocido.",
            "La devolución del tesoro de la cala pirata consolidó la reputación del grupo.",
            "Hiro desea regresar a Elken para proteger a los niños."
        ]
    },
    {
        "id": "reyes-nigromantes",
        "title": "El Resurgir de los Reyes Nigromantes",
        "priority": "Media",
        "status": "Investigación Abierta",
        "category": "Amenaza Arcana",
        "description": "Thir fue gobernado por reyes nigromantes hace 300 años. El nigromante Zarcand, los grimorios prohibidos y la máscara demoníaca de la torre de Zenopus indican que viejos poderes intentan volver a la superficie.",
        "clues": [
            "La máscara de bronce en la torre de Zenopus responde a una hora precisa del cuadrante.",
            "Tauster desea comprar el anillo encontrado en la torre del cementerio."
        ]
    }
]

# -------------------------------------------------------------
# 5. CURATE MAPS & ATLAS
# -------------------------------------------------------------
atlas_items = []
map_page = pages_by_name.get("Mapas", {})
for idx, img in enumerate(map_page.get("images", [])):
    p = img.get("image_info", {}).get("path")
    if p and os.path.exists(os.path.join(ROOT_DIR, p)):
        atlas_items.append({
            "id": f"map_{idx+1}",
            "title": f"Mapa Cartográfico #{idx+1} — Región y Localizaciones",
            "type": "Cartografía",
            "path": p,
            "description": "Mapa de la Costa de los Naufragios, Ciudad de Elken, calas piratas, Palazio de Kaz y caminos hacia Milborne y Thurmaster."
        })

sketch_page = pages_by_name.get("Sketch", {})
for idx, img in enumerate(sketch_page.get("images", [])):
    p = img.get("image_info", {}).get("path")
    if p and os.path.exists(os.path.join(ROOT_DIR, p)):
        atlas_items.append({
            "id": f"sketch_{idx+1}",
            "title": f"Boceto Táctico #{idx+1} — Planos y Mazmorras",
            "type": "Plano Táctico",
            "path": p,
            "description": "Esquema táctico de combate, distribución de salas subterráneas y notas de exploración."
        })

# -------------------------------------------------------------
# 6. WRITE DATA FILES
# -------------------------------------------------------------
final_bundle = {
    "campaign_name": "Las Crónicas de Los Koonies",
    "subtitle": "Diario de Campaña, Compendio y Crónica de Aventuras",
    "system": "AD&D 2ª Edición / Fantasía Épica",
    "total_sessions": len(curated_sessions),
    "characters": koonies_roster,
    "sessions": curated_sessions,
    "npcs": curated_npcs,
    "mysteries": mysteries,
    "treasury": {
        "gold": 120,
        "silver": 2600,
        "copper": 450,
        "vessel": "La Galera del Príncipe",
        "magic_items": [
            {"name": "Collar Ojo de J'karaa", "holder": "Sakura (cedido por Ainur)", "desc": "Reliquia arcana con propiedades sensoriales y misteriosas que Tauster y nigromantes persiguen."},
            {"name": "Ungüento de Keoghtom", "holder": "Grupo", "desc": "Bálsamo medicinal mágico de gran potencia (4 dosis restantes)."},
            {"name": "Poción de Vida (Life Potion)", "holder": "Grupo", "desc": "Poción legendaria con propiedades de absorción vital temporal."},
            {"name": "Grimorio de Zarcand", "holder": "Sakura", "desc": "Libro de conjuros oscuros rescatado del almacén del puerto."},
            {"name": "Diario y Anillo de Zenopus", "holder": "Grupo", "desc": "Manuscrito con las revelaciones del Kanatsu-mi y el anillo que Tauster desea adquirir."}
        ]
    },
    "atlas": atlas_items
}

with open(os.path.join(DATA_DIR, "campaign_data.json"), "w", encoding="utf-8") as f:
    json.dump(final_bundle, f, indent=2, ensure_ascii=False)

with open(os.path.join(DATA_DIR, "campaign_data.js"), "w", encoding="utf-8") as f:
    f.write("window.CAMPAIGN_DATA = " + json.dumps(final_bundle, indent=2, ensure_ascii=False) + ";\n")

print("Generated data/campaign_data.json and data/campaign_data.js successfully.")

# -------------------------------------------------------------
# 7. GENERATE MARKDOWN WIKI FILES
# -------------------------------------------------------------
with open(os.path.join(WIKI_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(f"""# 🛡️ Las Crónicas de Los Koonies

> **Compendio y Crónica de Campaña**  
> *Sistema:* AD&D 2ª Edición  
> *Estado:* 16 Sesiones jugadas — En marcha hacia las montañas y Thurmaster

---

## 🧭 Índice General

- [[personajes/glunt|👤 Los Koonies (6 Protagonistas)]]
- [[sesiones/sesion-01|📜 Diario de Sesiones (I al XVI)]]
- [[pnjs/jelenneth__jenneleth_|🎭 Dramatis Personae (PNJs y Facciones)]]
- [[lore_y_misterios/cabos-sueltos|🧩 Tablero de Misterios y Cabos Sueltos]]
- [[lore_y_misterios/tesoreria-y-equipo|🎒 Bóveda de Equipo y Tesorería]]
- [[mapas/atlas|🗺️ Atlas Cartográfico y Planos]]

---

## 👥 Los 6 Koonies (Personajes Jugadores)
""")
    for k in koonies_roster:
        f.write(f"- **[[personajes/{k['id']}|{k['name']}]]** — *{k['title']}* ({k['role']})\n")
    f.write("\n## 📜 Sesiones Recientes\n")
    for s in curated_sessions[-5:]:
        f.write(f"- **[[sesiones/sesion-{s['number']:02d}|Sesión {s['number']}: {s['title']}]]** ({s['in_game_date']})\n")

# Characters
for k in koonies_roster:
    with open(os.path.join(WIKI_DIR, "personajes", f"{k['id']}.md"), "w", encoding="utf-8") as f:
        f.write(f"""# {k['name']}
> *"{k['title']}"*

**Rol:** {k['role']}  
**Arquetipo:** {k['archetype']}  
**Cita:** *"{k['quote']}"*

---

## 📜 Historia y Notas
{k['full_lore']}

---
[[README|← Volver al Índice]]
""")

# NPCs
for npc in curated_npcs:
    clean_id = re.sub(r'[^a-zA-Z0-9_-]', '_', npc['name'].lower())
    with open(os.path.join(WIKI_DIR, "pnjs", f"{clean_id}.md"), "w", encoding="utf-8") as f:
        f.write(f"""# {npc['name']}
> *{npc['nickname']}*

- **Rol / Profesión:** {npc['role']}
- **Ubicación:** {npc['location']}
- **Facción:** {npc['faction']}
- **Actitud hacia el Grupo:** {npc['attitude']}
- **Estado Actual:** {npc['status']}

---

## 📝 Notas y Observaciones
{npc['notes']}

---
[[README|← Volver al Índice]]
""")

# Mysteries & Treasury
with open(os.path.join(WIKI_DIR, "lore_y_misterios", "cabos-sueltos.md"), "w", encoding="utf-8") as f:
    f.write("# 🧩 Tablero de Misterios & Cabos Sueltos\n\n")
    for m in mysteries:
        f.write(f"## {m['title']}\n")
        f.write(f"- **Prioridad:** {m['priority']} | **Estado:** {m['status']} | **Categoría:** {m['category']}\n\n")
        f.write(f"{m['description']}\n\n")
        f.write("### Pistas y Hallazgos:\n")
        for clue in m['clues']:
            f.write(f"- {clue}\n")
        f.write("\n---\n\n")

print("Generated Markdown Wiki in /wiki/ successfully.")
