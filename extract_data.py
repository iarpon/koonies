import json
import os
import re
import base64

TLDR_PATH = "/Users/ivan/Desktop/Los Koonies.tldr"
OUTPUT_DIR = "/Users/ivan/Documents/koonies"
IMG_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

with open(TLDR_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

records = data.get("records", [])

def get_text_from_node(node):
    if not isinstance(node, dict):
        return ""
    ntype = node.get("type")
    if ntype == "text":
        t = node.get("text", "")
        marks = node.get("marks", [])
        for m in marks:
            mt = m.get("type")
            if mt == "bold":
                t = f"**{t}**"
            elif mt == "italic":
                t = f"*{t}*"
            elif mt == "link":
                href = m.get("attrs", {}).get("href", "#")
                t = f"[{t}]({href})"
            elif mt == "highlight":
                t = f"=={t}=="
        return t
    content = node.get("content", [])
    inner = "".join(get_text_from_node(c) for c in content)
    if ntype == "paragraph":
        return inner + "\n\n"
    elif ntype == "heading":
        level = node.get("attrs", {}).get("level", 2)
        h_prefix = "#" * level
        return f"\n{h_prefix} {inner.strip()}\n\n"
    elif ntype == "bulletList":
        return inner + "\n"
    elif ntype == "listItem":
        return f"- {inner.strip()}\n"
    elif ntype == "doc":
        return inner
    return inner

pages = {r["id"]: r for r in records if r.get("typeName") == "page"}
shapes = [r for r in records if r.get("typeName") == "shape"]
assets = {r["id"]: r for r in records if r.get("typeName") == "asset"}

# Export assets to disk
asset_file_map = {}
print(f"Exporting {len(assets)} assets to {IMG_DIR}...")
for aid, asset in assets.items():
    props = asset.get("props", {})
    src = props.get("src", "")
    mime = props.get("mimeType", "image/png")
    name = props.get("name", "asset")
    clean_aid = re.sub(r'[^a-zA-Z0-9_-]', '_', aid)
    
    ext = ".png"
    if "jpeg" in mime or "jpg" in mime:
        ext = ".jpg"
    elif "svg" in mime:
        ext = ".svg"
    elif "webp" in mime:
        ext = ".webp"
    
    filename = f"{clean_aid}{ext}"
    filepath = os.path.join(IMG_DIR, filename)
    
    if src.startswith("data:"):
        # decode base64
        try:
            _, b64data = src.split(",", 1)
            raw = base64.b64decode(b64data)
            with open(filepath, "wb") as img_f:
                img_f.write(raw)
            asset_file_map[aid] = {
                "filename": filename,
                "path": f"images/{filename}",
                "name": name,
                "mimeType": mime,
                "size": len(raw),
                "w": props.get("w"),
                "h": props.get("h")
            }
        except Exception as e:
            print(f"Error decoding asset {aid}: {e}")
    else:
        asset_file_map[aid] = {
            "filename": "",
            "path": src,
            "name": name,
            "mimeType": mime,
            "w": props.get("w"),
            "h": props.get("h")
        }

print(f"Extracted {len(asset_file_map)} assets successfully.")

# Map shapes to pages
shape_map = {s["id"]: s for s in shapes}
def get_page_id(shape):
    cur = shape
    while cur:
        pid = cur.get("parentId", "")
        if pid.startswith("page:"):
            return pid
        cur = shape_map.get(pid)
    return "page:unknown"

# Group page contents
page_data_list = []
for pid, page in sorted(pages.items(), key=lambda x: x[1].get("index", "")):
    pname = page.get("name", "Sin título")
    pshapes = [s for s in shapes if get_page_id(s) == pid]
    
    texts = []
    images = []
    
    for s in pshapes:
        stype = s.get("type")
        props = s.get("props", {})
        
        if stype == "image":
            aid = props.get("assetId")
            ainfo = asset_file_map.get(aid, {})
            images.append({
                "shape_id": s.get("id"),
                "asset_id": aid,
                "image_info": ainfo,
                "x": s.get("x", 0),
                "y": s.get("y", 0),
                "w": props.get("w", 0),
                "h": props.get("h", 0)
            })
        elif "richText" in props:
            rt = props.get("richText")
            parsed = get_text_from_node(rt).strip()
            if parsed:
                texts.append({
                    "shape_id": s.get("id"),
                    "text": parsed,
                    "x": s.get("x", 0),
                    "y": s.get("y", 0),
                    "w": props.get("w", 0),
                    "color": props.get("color", "black"),
                    "size": props.get("size", "m")
                })
        elif stype == "geo" and props.get("text"):
            t = props.get("text").strip()
            if t:
                texts.append({
                    "shape_id": s.get("id"),
                    "text": t,
                    "x": s.get("x", 0),
                    "y": s.get("y", 0),
                    "w": props.get("w", 0),
                    "color": props.get("color", "black"),
                    "size": props.get("size", "m")
                })
        elif stype == "note" and props.get("text"):
            t = props.get("text").strip()
            if t:
                texts.append({
                    "shape_id": s.get("id"),
                    "text": t,
                    "x": s.get("x", 0),
                    "y": s.get("y", 0),
                    "w": props.get("w", 0),
                    "color": props.get("color", "yellow"),
                    "size": props.get("size", "m")
                })

    # Sort texts and images by position (y, x)
    texts.sort(key=lambda item: (item["y"], item["x"]))
    images.sort(key=lambda item: (item["y"], item["x"]))
    
    page_data_list.append({
        "id": pid,
        "name": pname,
        "index": page.get("index", ""),
        "total_shapes": len(pshapes),
        "texts": texts,
        "images": images
    })

# Save clean JSON
with open(os.path.join(OUTPUT_DIR, "extracted_campaign_data.json"), "w", encoding="utf-8") as f:
    json.dump({"pages": page_data_list, "assets": asset_file_map}, f, indent=2, ensure_ascii=False)

print(f"Extraction complete! Saved extracted_campaign_data.json with {len(page_data_list)} pages.")
