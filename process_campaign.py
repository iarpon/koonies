import json
import os
import re
import math

OUTPUT_DIR = "/Users/ivan/Documents/koonies"
DATA_DIR = os.path.join(OUTPUT_DIR, "data")
WIKI_DIR = os.path.join(OUTPUT_DIR, "wiki")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(WIKI_DIR, exist_ok=True)

with open(os.path.join(OUTPUT_DIR, "extracted_campaign_data.json"), "r", encoding="utf-8") as f:
    raw_data = json.load(f)

pages = raw_data["pages"]
assets = raw_data["assets"]

def dist(item1, item2):
    return math.hypot(item1["x"] - item2["x"], item1["y"] - item2["y"])

def find_nearest_images(item, images, max_dist=1200, limit=3):
    sorted_imgs = sorted(images, key=lambda img: dist(item, img))
    return [img for img in sorted_imgs if dist(item, img) < max_dist][:limit]

# Let's inspect pages
pages_by_name = {p["name"]: p for p in pages}

# 1. PROCESS CHARACTERS (Los Koonies)
pj_page = pages_by_name.get("Personajes", {})
pj_texts = pj_page.get("texts", [])
pj_images = pj_page.get("images", [])

print(f"Personajes texts: {len(pj_texts)}, images: {len(pj_images)}")

# Group character texts by header
characters = []
current_char = None

for t in sorted(pj_texts, key=lambda x: (x["y"], x["x"])):
    text = t["text"].strip()
    # Check if this text looks like a character header (e.g. ### Glunt, ### Hiroyuki, ### Katsumi, ### Sakura, etc.)
    # or starts with a quote or title
    lines = text.split("\n")
    first_line = lines[0].strip()
    
    # Matching headings like: ### Glunt: El Gigante de Corazón de Cristal, ### Hiroyuki Watanabe..., etc.
    header_match = re.match(r'^(?:#+)?\s*(.+?):\s*(.+)', first_line)
    name_quote_match = re.match(r'^"Soy ([^,]+),', first_line)
    
    is_new_char = False
    name = ""
    epithet = ""
    
    if first_line.startswith("### ") or first_line.startswith("## ") or first_line.startswith("# "):
        is_new_char = True
        clean_title = re.sub(r'^#+\s*', '', first_line).strip()
        if ":" in clean_title:
            parts = clean_title.split(":", 1)
            name = parts[0].strip()
            epithet = parts[1].strip()
        else:
            name = clean_title
            epithet = ""
    elif "Soy Katsumi" in text or "Soy Sakura" in text or "Soy Glunt" in text or "Soy Hiroyuki" in text or "Soy Jenneleth" in text or "Soy Ainur" in text:
        # Check if text is monologue
        if not current_char or current_char["name"] not in text:
            is_new_char = True
            for candidate in ["Katsumi", "Sakura", "Glunt", "Hiroyuki Watanabe", "Hiroyuki", "Jenneleth", "Ainur"]:
                if candidate in text:
                    name = candidate
                    break
    
    # Assign nearest images
    nearby_imgs = find_nearest_images(t, pj_images, max_dist=1500, limit=4)
    img_paths = [img["image_info"]["path"] for img in nearby_imgs if img.get("image_info", {}).get("path")]
    
    characters.append({
        "raw_title": first_line,
        "name": name or first_line[:30],
        "epithet": epithet,
        "text": text,
        "pos": {"x": t["x"], "y": t["y"]},
        "images": img_paths
    })

print(f"Found {len(characters)} character blocks.")

# 2. PROCESS SESSIONS (1 to 16)
sessions = []
session_pages = [p for p in pages if re.match(r'^Sesi[oó]n\s+\d+', p["name"], re.IGNORECASE)]

# Sort session pages by session number
def get_session_num(pname):
    m = re.search(r'\d+', pname)
    return int(m.group(0)) if m else 999

session_pages.sort(key=lambda p: get_session_num(p["name"]))

for sp in session_pages:
    s_num = get_session_num(sp["name"])
    pname = sp["name"]
    texts = sp.get("texts", [])
    images = sp.get("images", [])
    
    # Extract IRL Date and In-Game Date if present
    # e.g., "Sesión 15. 02/08/26", "Sesion 1. 15/0/26"
    irl_date = ""
    date_m = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', pname)
    if date_m:
        irl_date = date_m.group(1)
    
    # Merge all texts by y-coordinate
    full_narrative_blocks = []
    in_game_date = ""
    location = ""
    session_title = ""
    xp = ""
    
    for t in sorted(texts, key=lambda x: (x["y"], x["x"])):
        txt = t["text"].strip()
        
        # Check for title
        if not session_title and (txt.startswith("# ") or txt.startswith("## ") or "Sesión" in txt or "Sesion" in txt):
            first_line = txt.split("\n")[0]
            clean = re.sub(r'^[#*_\s]+|[#*_\s]+$', '', first_line)
            session_title = clean
            
        # Check for In-Game date patterns (e.g. "Iryn 15, año 19 CL", "24 de Sulmar del año 18")
        date_game_m = re.search(r'([A-Z][a-z]+ \d{1,2}, año \d{1,2} [A-Z]+|\d{1,2} de [A-Z][a-z]+ del año \d{1,2})', txt)
        if date_game_m and not in_game_date:
            in_game_date = date_game_m.group(1)
            
        # Check for Location (e.g. "*Ciudad de Elken — Costa de los Naufragios*")
        loc_m = re.search(r'\*([^*]+(?:Costa|Isla|Ciudad|Mar|Mansión|Milborne|Thurmaster)[^*]*)\*', txt)
        if loc_m and not location:
            location = loc_m.group(1).strip()
            
        # Check for PX
        xp_m = re.search(r'(?:PX|PX\.|Experiencia)[:\s]*([^\n]+)', txt, re.IGNORECASE)
        if xp_m:
            xp = xp_m.group(0).strip()
            
        # Find images close to this text block
        block_imgs = find_nearest_images(t, images, max_dist=1200, limit=2)
        img_paths = [img["image_info"]["path"] for img in block_imgs if img.get("image_info", {}).get("path")]
        
        full_narrative_blocks.append({
            "text": txt,
            "images": img_paths,
            "pos": {"x": t["x"], "y": t["y"]}
        })
        
    all_img_paths = [img["image_info"]["path"] for img in images if img.get("image_info", {}).get("path")]
    
    sessions.append({
        "number": s_num,
        "raw_name": pname,
        "title": session_title or f"Sesión {s_num}",
        "irl_date": irl_date,
        "in_game_date": in_game_date,
        "location": location,
        "xp": xp,
        "blocks": full_narrative_blocks,
        "images": all_img_paths,
        "full_text": "\n\n".join(b["text"] for b in full_narrative_blocks)
    })

print(f"Processed {len(sessions)} sessions.")

# 3. PROCESS NPCS (PNJ's)
npc_page = pages_by_name.get("PNJ´s", {})
npc_texts = npc_page.get("texts", [])
npc_images = npc_page.get("images", [])

npcs = []
for t in sorted(npc_texts, key=lambda x: (x["y"], x["x"])):
    txt = t["text"].strip()
    if "Nombre:" in txt or "**Nombre:**" in txt:
        # Extract fields
        name_m = re.search(r'Nombre:\s*\**==?([^=\n*]+)==?\**', txt)
        name = name_m.group(1).strip() if name_m else "Desconocido"
        
        nickname_m = re.search(r'Apodo:\s*([^\n]*)', txt)
        nickname = nickname_m.group(1).strip() if nickname_m else ""
        
        race_m = re.search(r'Raza:\s*([^\n]*)', txt)
        race = race_m.group(1).strip() if race_m else ""
        
        age_m = re.search(r'Edad:\s*([^\n]*)', txt)
        age = age_m.group(1).strip() if age_m else ""
        
        role_m = re.search(r'Profesion/Rol:\s*([^\n]*)', txt, re.IGNORECASE)
        role = role_m.group(1).strip() if role_m else ""
        
        attitude_m = re.search(r'Actitud hacia el grupo:\s*([^\n]*)', txt)
        attitude = attitude_m.group(1).strip() if attitude_m else ""
        
        status_m = re.search(r'Estado Actual:\s*\**([^\n*]+)\**', txt)
        status = status_m.group(1).strip() if status_m else "Desconocido"
        
        # Nearest image
        nearby = find_nearest_images(t, npc_images, max_dist=1200, limit=2)
        img_paths = [img["image_info"]["path"] for img in nearby if img.get("image_info", {}).get("path")]
        
        npcs.append({
            "name": name,
            "nickname": nickname,
            "race": race,
            "age": age,
            "role": role,
            "attitude": attitude,
            "status": status,
            "full_card": txt,
            "pos": {"x": t["x"], "y": t["y"]},
            "images": img_paths
        })

print(f"Processed {len(npcs)} NPCs.")

# 4. PROCESS LOOSE ENDS & MYSTERIES (Cabos sueltos)
loose_page = pages_by_name.get("Cabos sueltos", {})
loose_texts = loose_page.get("texts", [])
loose_items = []
for t in loose_texts:
    txt = t["text"].strip()
    # Split bullet points
    lines = txt.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            content = line[2:].strip()
            # Title before dash or bold
            m = re.match(r'^\*\*([^*]+)\*\*\s*[—–-]\s*(.+)', content)
            if m:
                loose_items.append({
                    "title": m.group(1).strip(),
                    "description": m.group(2).strip(),
                    "raw": content,
                    "status": "Abierto"
                })
            else:
                loose_items.append({
                    "title": content[:40],
                    "description": content,
                    "raw": content,
                    "status": "Abierto"
                })

# 5. PROCESS GROUP EQUIPMENT & TREASURY
eq_page = pages_by_name.get("Equipo de Grupo", {})
eq_texts = [t["text"].strip() for t in eq_page.get("texts", [])]
eq_full = "\n\n".join(eq_texts)

# 6. PROCESS MAPS & SKETCHES
maps_page = pages_by_name.get("Mapas", {})
sketch_page = pages_by_name.get("Sketch", {})

maps_list = []
for img in maps_page.get("images", []):
    ainfo = img.get("image_info", {})
    if ainfo.get("path"):
        maps_list.append({
            "path": ainfo.get("path"),
            "name": ainfo.get("name", "Mapa"),
            "category": "Mapa de Región / Localización",
            "pos": {"x": img["x"], "y": img["y"]}
        })

for img in sketch_page.get("images", []):
    ainfo = img.get("image_info", {})
    if ainfo.get("path"):
        maps_list.append({
            "path": ainfo.get("path"),
            "name": ainfo.get("name", "Boceto / Plano Táctico"),
            "category": "Bocetos y Planos",
            "pos": {"x": img["x"], "y": img["y"]}
        })

print(f"Processed {len(maps_list)} maps and sketches.")

# SAVE COMPILED DATA
compiled_data = {
    "characters": characters,
    "sessions": sessions,
    "npcs": npcs,
    "loose_ends": loose_items,
    "group_equipment": eq_full,
    "maps": maps_list
}

with open(os.path.join(DATA_DIR, "campaign_data.json"), "w", encoding="utf-8") as f:
    json.dump(compiled_data, f, indent=2, ensure_ascii=False)

# Also create campaign_data.js for instant browser loading
with open(os.path.join(DATA_DIR, "campaign_data.js"), "w", encoding="utf-8") as f:
    f.write("window.CAMPAIGN_DATA = " + json.dumps(compiled_data, indent=2, ensure_ascii=False) + ";\n")

print("Data processing finished successfully!")
