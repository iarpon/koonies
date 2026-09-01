import re

with open("/Users/ivan/Documents/koonies/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update stats counter from 29 to 5
html = re.sub(r'<p class="text-2xl font-bold font-cinzel text-slate-100">29</p>', '<p class="text-2xl font-bold font-cinzel text-slate-100">5</p>', html)

# Update atlas filter buttons
html = html.replace(
    '<button onclick="filterAtlas(\'Plano Táctico\')" class="atlas-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-medium bg-slate-900/80 text-slate-300 hover:bg-slate-800" data-type="Plano Táctico">Bocetos y Mazmorras</button>',
    '<button onclick="filterAtlas(\'Plano de Ciudad\')" class="atlas-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-medium bg-slate-900/80 text-slate-300 hover:bg-slate-800" data-type="Plano de Ciudad">Planos de Ciudad</button>'
)

# Update atlas subtitle
html = html.replace("29 mapas de navegación", "5 cartas de navegación y planos principales de Elken")

with open("/Users/ivan/Documents/koonies/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html patched with 5 maps count.")
