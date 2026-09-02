import json
import os
import re
import math
from collections import Counter

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

def dist(p1, p2):
    return math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])

# -------------------------------------------------------------
# 1. CURATE CHARACTERS (LOS 5 KOONIES - PJ's)
# -------------------------------------------------------------
pj_page = pages_by_name.get("Personajes", {})
pj_texts = pj_page.get("texts", [])
pj_images = pj_page.get("images", [])

koonies_roster = [
    {
        "id": "glunt",
        "name": "Glunt",
        "title": "El Gigante de Corazón de Cristal",
        "role": "Guerrero",
        "tag": "Guerrero",
        "stats": {"clase": "Guerrero", "fuerza": "17 (Colosal)", "arma": "Gran Fuerza & Pureza", "origen": "Tierras Bajas de Amatsukuni"},
        "archetype": "Fuerza titánica, inocencia incorruptible y devoción incondicional a los pequeños.",
        "quote": "Padre dijo que me quedara. Glunt se queda. Glunt cuidará de los pequeños hasta que el sol vuelva a salir.",
        "icon": "shield",
        "badge_color": "emerald",
        "accent": "#10b981",
        "primary_image": "images/asset_-929693943.jpg",
        "match_keys": ["Glunt", "Gigante de Corazón", "Glunt:"],
        "curse_status": "Maldición de las Venas Negras (contraída en la Torre de Zenopus, contenida tras las aguas de Kanatsu-mi)."
    },
    {
        "id": "hiroyuki",
        "name": "Hiroyuki Watanabe",
        "title": "El Acero en la Forja",
        "role": "Guerrero",
        "tag": "Guerrero",
        "stats": {"clase": "Guerrero (Kensei)", "fuerza": "15 (Atlético)", "arma": "Espada Larga & Naginata", "origen": "Capital de Amatsukuni"},
        "archetype": "Honor marcial, devoción a Hachiman y escudo inquebrantable de los supervivientes.",
        "quote": "Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.",
        "icon": "swords",
        "badge_color": "amber",
        "accent": "#f59e0b",
        "primary_image": "images/asset_1793380967.jpg",
        "match_keys": ["Hiroyuki", "Hiroyuki Watanabe", "El Acero en la Forja"]
    },
    {
        "id": "sakura",
        "name": "Sakura",
        "title": "La Erudita de lo Arcano",
        "role": "Maga",
        "tag": "Maga",
        "stats": {"clase": "Maga", "magia": "Evocación / Arcano", "arma": "Grimorio de Zarcand", "origen": "Academia Arcana"},
        "archetype": "Mente incisiva, descifradora de secretos antiguos y actual portadora del Ojo de J'karaa.",
        "quote": "El conocimiento no es peligroso; ignorar sus consecuencias sí lo es.",
        "icon": "sparkles",
        "badge_color": "pink",
        "accent": "#ec4899",
        "primary_image": "images/asset_1843595399.jpg",
        "match_keys": ["Sakura", "Maga kunita", "tercer ojo"]
    },
    {
        "id": "ainur",
        "name": "Ainur",
        "title": "El Ojo Atento",
        "role": "Explorador",
        "tag": "Explorador",
        "stats": {"clase": "Explorador / Pícaro", "destreza": "Alta", "arma": "Arco & Daga", "origen": "Fronteras de Amatsukuni"},
        "archetype": "Carisma, sigilo, percepción extrasensorial y rastreador infalible en la niebla.",
        "quote": "La niebla oculta muchas cosas, pero ninguna que no deje rastro.",
        "icon": "eye",
        "badge_color": "indigo",
        "accent": "#6366f1",
        "primary_image": "images/asset_1067045487.jpg",
        "match_keys": ["Ainur", "Ojo de J'karaa", "Airun"]
    },
    {
        "id": "kazgrim",
        "name": "Kazgrim Iwakura (Kaz)",
        "title": "El Guardián de la Llama Perdida",
        "role": "Clérigo",
        "tag": "Clérigo",
        "stats": {"clase": "Clérigo de Kagutsuchi", "fuerza": "13 (+4)", "inteligencia": "10", "origen": "Kizuna-no-Miya (Norte Montañoso)"},
        "archetype": "Cantero enano (38 años) que escucha los kami en la roca y despierta el fuego renaciente.",
        "quote": "El papel arde, pero la verdad es incombustible. Si el fuego lo devoró todo, es porque algo nuevo y más fuerte debe nacer de nuestras cenizas.",
        "icon": "hammer",
        "badge_color": "orange",
        "accent": "#ea580c",
        "primary_image": "images/asset_-1175273093.png",
        "match_keys": ["Kazgrim", "Kaz", "Kazrim", "Iwakura", "Kagutsuchi", "La historia de Kazrim"]
    }
]

for k in koonies_roster:
    matched_texts = []
    for t in pj_texts:
        txt = t["text"]
        if any(key.lower() in txt.lower() for key in k["match_keys"]):
            matched_texts.append(txt)
    k["full_lore"] = "\n\n".join(matched_texts) if matched_texts else f"Miembro fundador de Los Koonies. {k['archetype']}."
    k["gallery"] = [k["primary_image"]]

print(f"Curated {len(koonies_roster)} Koonies player characters (PJs).")

# -------------------------------------------------------------
# 2. CURATE SESSIONS (1 to 16) WITH TEXT CLEANUP (NO DASH LINES / NO OVERFLOW)
# -------------------------------------------------------------
session_covers_unique = {
    1: "images/asset_10816842.png",
    2: "images/asset_238755922.png",
    3: "images/asset_643137533.png",
    4: "images/asset_1325026172.png",
    5: "images/asset_2006248850.png",
    6: "images/asset_1515216225.png",
    7: "images/asset_-199017577.png",
    8: "images/asset_-1336998075.png",
    9: "images/asset_1704990873.png",
    10: "images/asset_2054780468.png",
    11: "images/asset_387950169.png",
    12: "images/asset_1189662238.png",
    13: "images/asset_-1452585810.webp",
    14: "images/asset_2093206144.png",
    15: "images/asset_1370269724.png",
    16: "images/asset_1659737080.png"
}

session_meta_titles = {
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
    page_images = sp.get("images", [])
    
    meta = session_meta_titles.get(s_num, {
        "title": f"Sesión {s_num}",
        "act": "Crónica de Aventuras",
        "in_game": "Fecha desconocida",
        "loc": "Costa de los Naufragios"
    })
    
    cover_img = session_covers_unique.get(s_num, "images/asset_10816842.png")
    
    irl_date = ""
    date_m = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', sp["name"])
    if date_m:
        irl_date = date_m.group(1)
        
    ordered_texts = sorted(texts, key=lambda x: (x["y"], x["x"]))
    blocks = []
    xp_found = ""
    
    used_images_in_session = set([cover_img])
    
    for t in ordered_texts:
        raw_t = t["text"].strip()
        
        # Clean long dashes that cause horizontal overflow
        raw_t = re.sub(r'-{3,}', '---', raw_t)
        # Normalize excessive tabs
        raw_t = re.sub(r'\t+', ' ', raw_t)
        
        if "PX:" in raw_t or "PX " in raw_t or "Experiencia:" in raw_t:
            xp_found = raw_t
            
        valid_imgs = []
        for img in sorted(page_images, key=lambda item: dist(t, item)):
            p = img.get("image_info", {}).get("path")
            if p and p not in used_images_in_session and os.path.exists(os.path.join(ROOT_DIR, p)):
                valid_imgs.append(p)
                used_images_in_session.add(p)
                if len(valid_imgs) >= 1:
                    break
                    
        blocks.append({
            "text": raw_t,
            "images": valid_imgs
        })
        
    all_session_images = list(used_images_in_session)
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
        "xp": xp_found or "250-350 PX",
        "cover_image": cover_img,
        "summary": summary_snippet or "Los Koonies continúan su odisea a través de tierras inhóspitas y misterios arcanos.",
        "blocks": blocks,
        "images": all_session_images,
        "full_text": full_narrative
    })

print(f"Curated {len(curated_sessions)} sessions.")

# -------------------------------------------------------------
# 3. CURATE NPCS (INCLUDING KATSUMI AS PNJ)
# -------------------------------------------------------------
curated_npcs = [
    {
        "name": "Katsumi",
        "nickname": "La Llama Custodia / Líder del Campamento",
        "role": "Clériga de Shien & Líder de Refugiados",
        "location": "Campamento Kunita, Elken",
        "faction": "Refugiados de Amatsukuni / Culto de Shien",
        "attitude": "Devota, protectora y leal aliada",
        "status": "Viva",
        "notes": "Llama Custodia consagrada al servicio de Shien, la Llama Púrpura. Administra el campamento de los 40 supervivientes kunitas extramuros de Elken con su naginata sagrada. Pone sus esperanzas en encontrar a Yoriko Asano.",
        "image": "images/asset_154989466.png"
    },
    {
        "name": "Jelenneth (Jenneleth)",
        "nickname": "La Maga Samaritana",
        "role": "Maga y Sanadora / Aprendiz de Tauster",
        "location": "Milborne & Thurmaster",
        "faction": "Aliada Íntima de Sakura y Los Koonies",
        "attitude": "Muy amigable / 'Hermana de corazón' de Sakura",
        "status": "Viva",
        "notes": "Chica joven con capa azul y bolsa de viaje pesada. Aprendiz del mago Tauster. Examinó el Ojo de J'karaa con gran urgencia y guió al grupo hasta Thurmaster.",
        "image": "images/asset_179927520.png"
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
        "image": "images/asset_1579031251.png"
    },
    {
        "name": "Aleina",
        "nickname": "La Paladín Pinpín",
        "role": "Paladín de Solkarion",
        "location": "Ciudad de Elken",
        "faction": "Orden de Solkarion",
        "attitude": "Legal estricta",
        "status": "Viva",
        "notes": "Caballera devota del Dragón Dorado de Thir. Mantiene vigilancia sobre las actividades en el puerto.",
        "image": "images/asset_-1825000868.png"
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
        "image": "images/asset_966061567.png"
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
        "image": "images/asset_-2115620674.png"
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
        "image": "images/asset_1060867694.png"
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
        "image": "images/asset_-1819219958.png"
    }
]

# -------------------------------------------------------------
# 4. MYSTERIES & ATLAS & TREASURY
# -------------------------------------------------------------
mysteries = [
    {
        "id": "maldicion-glunt",
        "title": "La Maldición de las Venas Negras de Glunt",
        "priority": "Alta",
        "status": "Contenida / Curada en Kanatsu-mi",
        "category": "Salud de los Koonies",
        "image": "images/asset_-929693943.jpg",
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
        "image": "images/asset_1063611285.jpg",
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
        "image": "images/asset_1843595399.jpg",
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
        "image": "images/asset_154989466.png",
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
        "image": "images/asset_387950169.png",
        "description": "Thir fue gobernado por reyes nigromantes hace 300 años. El nigromante Zarcand, los grimorios prohibidos y la máscara demoníaca de la torre de Zenopus indican que viejos poderes intentan volver a la superficie.",
        "clues": [
            "La máscara de bronce en la torre de Zenopus responde a una hora precisa del cuadrante.",
            "Tauster desea comprar el anillo encontrado en la torre del cementerio."
        ]
    }
]

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
        "vessel": {
            "name": "La Galera del Príncipe",
            "desc": "Navío insignia del grupo. Rápido galeón costero artillado y hogar flotante de los Koonies.",
            "image": "images/asset_2006248850.png"
        },
        "magic_items": [
            {"name": "Collar Ojo de J'karaa", "holder": "Sakura (cedido por Ainur)", "desc": "Reliquia arcana con propiedades sensoriales que Tauster y los nigromantes persiguen.", "image": "images/asset_1843595399.jpg"},
            {"name": "Ungüento de Keoghtom", "holder": "Grupo", "desc": "Bálsamo medicinal mágico de gran potencia (4 dosis restantes).", "image": "images/asset_-251637396.jpg"},
            {"name": "Poción de Vida (Life Potion)", "holder": "Grupo", "desc": "Poción legendaria con propiedades de absorción vital temporal.", "image": "images/asset_2054780468.png"},
            {"name": "Grimorio de Zarcand", "holder": "Sakura", "desc": "Libro de conjuros oscuros rescatado del almacén del puerto.", "image": "images/asset_387950169.png"},
            {"name": "Diario y Anillo de Zenopus", "holder": "Grupo", "desc": "Manuscrito con las revelaciones del Kanatsu-mi y el anillo sellador.", "image": "images/asset_1189662238.png"}
        ]
    },
    "atlas": curated_atlas
}

with open(os.path.join(DATA_DIR, "campaign_data.json"), "w", encoding="utf-8") as f:
    json.dump(final_bundle, f, indent=2, ensure_ascii=False)

with open(os.path.join(DATA_DIR, "campaign_data.js"), "w", encoding="utf-8") as f:
    f.write("window.CAMPAIGN_DATA = " + json.dumps(final_bundle, indent=2, ensure_ascii=False) + ";\n")

print(f"Build complete. {len(koonies_roster)} PJs, {len(curated_npcs)} NPCs, {len(curated_sessions)} Sessions.")
