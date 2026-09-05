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
        "stats": {
            "clase": "Guerrero 1 (Fighter)",
            "raza": "Humano",
            "alineamiento": "Neutral",
            "fue": "18 (+1 atq / +3 daño)",
            "des": "14",
            "con": "18 (+4 PG/dado)",
            "int": "7",
            "sab": "13",
            "car": "11",
            "ca": "7",
            "pg": "14",
            "thac0": "20 (19 con Fue)"
        },
        "archetype": "Fuerza titánica, inocencia incorruptible y devoción incondicional a los pequeños.",
        "quote": "Padre dijo que me quedara. Glunt se queda. Glunt cuidará de los pequeños hasta que el sol vuelva a salir.",
        "icon": "shield",
        "badge_color": "emerald",
        "accent": "#10b981",
        "primary_image": "images/asset_-929693943.jpg",
        "match_keys": [
            "Glunt",
            "Gigante de Corazón",
            "Glunt:"
        ],
        "curse_status": "Maldición de las Venas Negras (contraída en la Torre de Zenopus, contenida tras las aguas de Kanatsu-mi).",
        "full_lore": "### Glunt: El Gigante de Corazón de Cristal\n\n\n\nEl destino de Glunt estuvo marcado por el peso de su propia existencia desde el primer aliento. Nacido con un tamaño que la naturaleza no pudo sostener, su llegada al mundo supuso la partida de su madre. Aquellos minutos de silencio antes de su primera bocanada de aire dejaron una huella eterna en su mente, otorgándole una sencillez de espíritu que el mundo a menudo confunde con debilidad, pero que en realidad es **pureza absoluta**.\n\n\n\nHijo de un humilde labrador, Glunt creció entre surcos y arados, siendo el motor que aligeraba la vejez de su padre. Su viaje a la capital para el **Festival de Invierno** debía ser un premio, una maravilla de luces y alegría; en cambio, se convirtió en el inicio de su exilio. Con la misma entrega con la que araba la tierra, ayudó a cargar los grandes galeones, usando su inmensa fuerza (**Fuerza 17**) para salvar lo que pudiera del desastre.\n\nCuando el mundo se rompía en pedazos, su padre le dio una última instrucción: *\"Quédate en el barco\"*. \n\nY Glunt, fiel como una montaña, obedeció. No entiende de eclipses púrpura, ni de la no muerte que Ainur presintió; solo entiende que debe proteger a los que le rodean mientras espera volver a ver a su padre. En la oscuridad de la bodega de los piratas, Glunt es el único que mantiene una paz inquebrantable, convencido de que, si sigue siendo \"bueno\" y protege a sus amigos, cumplirá su palabra.\n\n\n\n*\"Padre dijo que me quedara. Glunt se queda. Glunt cuidará de los pequeños hasta que el sol vuelva a salir.\"*\n\n### Hiroyuki Watanabe: El Acero en la Forja\n\n\n\nHiroyuki no nació con un linaje de sangre noble, pero su espíritu siempre ha vibrado con la disciplina de los **Escudos de la Justicia**.\n\n\n\nDe constitución atlética y una fuerza que rivaliza con la de los veteranos, Hiroyuki recorría las calles de la capital con un solo propósito: conseguir los fondos necesarios para ser aceptado formalmente en la casta de los samurai.\n\n\n\nPara él, el honor no era un regalo de nacimiento, sino un trofeo que debía ser comprado con sudor y mérito.\n\n\n\nEn la ciudad de Amatsukuni, mientras otros celebraban o rezaban, él trabajaba y entrenaba, preparándose para el día en que pudiera portar la *naginata* o la espada larga bajo el estandarte de **Hachiman**, el Guardián Marcial. Sin embargo, la noche del eclipse púrpura no trajo su iniciación, sino el fin de su mundo.\n\n\n\nCapturado por los piratas de Lyndoria tras la caída de los galeones, Hiroyuki se encuentra ahora despojado de sus ahorros y de su futuro planeado. Pero en la oscuridad de la bodega, rodeado por el carisma de **Ainur**, la bondad de **Glunt**, la sabiduría de **Kazgrim** y la severidad de **Sumiko**, Hiroyuki comprende una verdad fundamental: el verdadero samurai no es aquel que paga por su entrada al dojo, sino aquel que protege a los suyos cuando todo lo demás se ha perdido. \n\n\n\n*\"Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.\"*\n\n# **La historia de Kazrim:**\n\nBackground del personaje\n\nNombre\n\nKazgrim Iwakura\n\n(pero todavía muchos lo llaman simplemente Kaz)\n\n\n\n\n# **Origen**\n\nKazgrim nació hace apenas 38 años, lo que para un enano sigue siendo casi un adolescente.\n\nCreció en un pequeño barrio de artesanos de piedra y metal en las cercanías de Kizuna-no-Miya, en el norte montañoso de Amatsukuni.\n\nSu clan no es famoso ni noble.\n\nSon canteros y constructores de templos, especialistas en trabajar la piedra volcánica de las montañas.\n\nDesde pequeño, Kazgrim creció escuchando dos cosas constantemente:\n\n- El sonido de los martillos sobre la piedra.\n- Las historias de los kami que habitan en las montañas y herramientas.\n\nEn Amatsukuni, incluso los objetos pueden albergar espíritus, y eso marcó profundamente su forma de ver el mundo. \n\n\n\n\n# **Infancia**\n\nKazgrim nunca fue el más fuerte del clan.\n\nMientras otros jóvenes competían en fuerza o en combate, él era conocido por:\n\n- hacer demasiadas preguntas\n- quedarse observando los rituales del templo\n- hablar con los ancianos y monjes\n\n\n\nSu abuelo solía decir:\n\n“La piedra escucha antes de romperse. Aprende a escuchar.”\n\nKazgrim se tomó esa frase demasiado en serio.\n\n\n\n\n# **El suceso que cambió su vida**\n\nCuando tenía 31 años, ocurrió algo extraño.\n\nDurante la reconstrucción de un pequeño santuario dedicado a Kagutsuchi, el dios del fuego, Kazgrim escuchó algo mientras trabajaba en la base del altar.\n\nNo fue una voz clara.\n\nMás bien una sensación, como si el calor de la piedra quisiera decirle algo.\n\nEsa misma noche soñó con un yunque ardiendo bajo una montaña.\n\nA la mañana siguiente, el anciano sacerdote del santuario le dijo algo inquietante:\n\n“A veces los kami hablan primero a quienes aún no saben escucharlos.”\n\nDesde entonces, Kazgrim comenzó a pasar cada vez más tiempo en templos y santuarios.\n\n\n\n\n# **Situación actual**\n\nKazgrim aún no es clérigo.\n\nEn realidad es poco más que un acólito curioso que ayuda con tareas simples:\n\n- limpiar altares\n- transportar ofrendas\n- mantener el fuego de los braseros\n- ayudar durante los festivales matsuri\n\nPero algo dentro de él está despertando.\n\nNo tiene formación completa.\n\nNo conoce aún los conjuros sagrados.\n\nSin embargo, cuando reza…\n\nlas velas a veces arden más intensamente de lo normal.\n\n\n\n\n# **Personalidad**\n\nKazgrim es:\n\n- curioso\n- sincero\n- un poco ingenuo\n- extremadamente respetuoso con las tradiciones\n\nTiene una fe instintiva, no dogmática.\n\nEn Amatsukuni es común venerar distintos kami según el momento de la vida, y Kazgrim todavía está intentando descubrir qué espíritu guía realmente su destino. \n\n\n\n\n# **Motivación para la aventura**\n\nKazgrim ha salido al mundo por tres razones:\n\n- Comprender la voz de los kami que cree haber escuchado.\n- Descubrir qué dios lo ha marcado realmente.\n- Demostrar a su clan que no hace falta ser el más fuerte para proteger a los demás.\n\n\n\n# **El guardian de la Llama perdida**\n\nEn los templos de Amatsukuni, el nombre de Kazgrim era sinónimo de devoción silenciosa y s\n\nabiduría profunda. Como enano de los templos, su vida estaba dedicada al estudio de los ciclos \n\ny a la protección de las reliquias sagradas. Se le confió la tarea más alta de su orden: \n\ncustodiar las escrituras de **==Kagutsuchi, el Fuego Renaciente==**, el dios que enseña que \n\nla destrucción es solo el preludio de la purificación.z\n\n\n\nSin embargo, la ingenuidad de su buen corazón no fue rival para la crueldad del acero pirata. \n\nEn la noche del naufragio, Kazgrim vio con horror cómo las llamas naturales de su dios eran \n\nsuperadas por el fuego de la traición. No pudo proteger los textos; las palabras sagradas se \n\nhundieron en el abismo junto con el orgullo de su pueblo.\n\nAhora, encadenado en la bodega, Kazgrim ya no es solo un bibliotecario de lo divino. \n\nEs un sabio que debe aprender que la verdadera escritura de Kagutsuchi no está en el \n\npapel, sino en la voluntad de renacer de las cenizas. Aunque se siente perdido, su sola \n\npresencia es un faro de calma para Glunt y una brújula moral para Ainur. Kazgrim busca \n\nsu camino, sin saber que el destino ya lo ha marcado para reescribir la historia de su pueblo \n\ncon sus propios actos.\n\n\n\n*\"El papel arde, pero la verdad es incombustible. Si el fuego lo devoró todo, es porque algo *\n\n*nuevo y más fuerte debe nacer de nuestras cenizas.\"*",
        "gallery": [
            "images/asset_-929693943.jpg"
        ],
        "saves": {
            "paralisis_veneno_muerte": 14,
            "varas_bastones_varitas": 16,
            "petrificacion_polimorfia": 15,
            "armas_aliento": 17,
            "conjuros": 17
        }
    },
    {
        "id": "hiroyuki",
        "name": "Hiroyuki Watanabe",
        "title": "El Acero en la Forja",
        "role": "Guerrero",
        "tag": "Guerrero",
        "stats": {
            "clase": "Guerrero 1 (Kensei)",
            "raza": "Humano",
            "alineamiento": "Neutral",
            "fue": "18 (+1 atq / +3 daño)",
            "des": "18 (+2 atq / -4 a CA)",
            "con": "12",
            "int": "16",
            "sab": "8",
            "car": "11",
            "ca": "6",
            "pg": "10",
            "thac0": "20 (19 CaC / 18 Proy)"
        },
        "archetype": "Honor marcial, devoción a Hachiman y escudo inquebrantable de los supervivientes.",
        "quote": "Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.",
        "icon": "swords",
        "badge_color": "amber",
        "accent": "#f59e0b",
        "primary_image": "images/asset_1793380967.jpg",
        "match_keys": [
            "Hiroyuki",
            "Hiroyuki Watanabe",
            "El Acero en la Forja"
        ],
        "full_lore": "### Hiroyuki Watanabe: El Acero en la Forja\n\n\n\nHiroyuki no nació con un linaje de sangre noble, pero su espíritu siempre ha vibrado con la disciplina de los **Escudos de la Justicia**.\n\n\n\nDe constitución atlética y una fuerza que rivaliza con la de los veteranos, Hiroyuki recorría las calles de la capital con un solo propósito: conseguir los fondos necesarios para ser aceptado formalmente en la casta de los samurai.\n\n\n\nPara él, el honor no era un regalo de nacimiento, sino un trofeo que debía ser comprado con sudor y mérito.\n\n\n\nEn la ciudad de Amatsukuni, mientras otros celebraban o rezaban, él trabajaba y entrenaba, preparándose para el día en que pudiera portar la *naginata* o la espada larga bajo el estandarte de **Hachiman**, el Guardián Marcial. Sin embargo, la noche del eclipse púrpura no trajo su iniciación, sino el fin de su mundo.\n\n\n\nCapturado por los piratas de Lyndoria tras la caída de los galeones, Hiroyuki se encuentra ahora despojado de sus ahorros y de su futuro planeado. Pero en la oscuridad de la bodega, rodeado por el carisma de **Ainur**, la bondad de **Glunt**, la sabiduría de **Kazgrim** y la severidad de **Sumiko**, Hiroyuki comprende una verdad fundamental: el verdadero samurai no es aquel que paga por su entrada al dojo, sino aquel que protege a los suyos cuando todo lo demás se ha perdido. \n\n\n\n*\"Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.\"*",
        "gallery": [
            "images/asset_1793380967.jpg"
        ],
        "saves": {
            "paralisis_veneno_muerte": 14,
            "varas_bastones_varitas": 16,
            "petrificacion_polimorfia": 15,
            "armas_aliento": 17,
            "conjuros": 17
        }
    },
    {
        "id": "sakura",
        "name": "Sakura",
        "title": "La Erudita de lo Arcano",
        "role": "Maga",
        "tag": "Maga",
        "stats": {
            "clase": "Maga 1 (Mage)",
            "raza": "Humana",
            "alineamiento": "Neutral",
            "fue": "18 (+1 atq / +2 daño)",
            "des": "11",
            "con": "17 (+3 PG/dado)",
            "int": "18 (Mente Suprema / 85% ap)",
            "sab": "18 (+4 vs magia mental)",
            "car": "6",
            "ca": "10",
            "pg": "8",
            "thac0": "20"
        },
        "archetype": "Mente incisiva, descifradora de secretos antiguos y actual portadora del Ojo de J'karaa.",
        "quote": "El conocimiento no es peligroso; ignorar sus consecuencias sí lo es.",
        "icon": "sparkles",
        "badge_color": "pink",
        "accent": "#ec4899",
        "primary_image": "images/asset_1843595399.jpg",
        "match_keys": [
            "Sakura",
            "Maga kunita",
            "tercer ojo"
        ],
        "full_lore": "Miembro fundador de Los Koonies. Mente incisiva, descifradora de secretos antiguos y actual portadora del Ojo de J'karaa..",
        "gallery": [
            "images/asset_1843595399.jpg"
        ],
        "saves": {
            "paralisis_veneno_muerte": 14,
            "varas_bastones_varitas": 11,
            "petrificacion_polimorfia": 13,
            "armas_aliento": 15,
            "conjuros": 12
        }
    },
    {
        "id": "ainur",
        "name": "Ainur",
        "title": "El Ojo Atento",
        "role": "Explorador",
        "tag": "Explorador",
        "stats": {
            "clase": "Explorador 1 / Pícaro 1",
            "raza": "Semielfo",
            "alineamiento": "Neutral",
            "fue": "14",
            "des": "18 (+2 proyectiles / -4 a CA)",
            "con": "16 (+2 PG/dado)",
            "int": "13",
            "sab": "16 (+2 vs mental)",
            "car": "15 (Reacción +3)",
            "ca": "6",
            "pg": "10",
            "thac0": "20 (18 Arcos)"
        },
        "archetype": "Carisma, sigilo, percepción extrasensorial y rastreador infalible en la niebla.",
        "quote": "La niebla oculta muchas cosas, pero ninguna que no deje rastro.",
        "icon": "eye",
        "badge_color": "indigo",
        "accent": "#6366f1",
        "primary_image": "images/asset_1067045487.jpg",
        "match_keys": [
            "Ainur",
            "Ojo de J'karaa",
            "Airun"
        ],
        "full_lore": "### Ainur\n\nEn su juventud, las llamas que Ainur prendió contra la \"civilización\" nacieron de un amor feroz por lo salvaje; una rebelión contra el progreso que devoraba la naturaleza. Pero el tiempo atemperó su fuego, convirtiendo la ira en carisma y la imprudencia en maestría de exploración. Sin embargo, nada en sus años bajo la fronda lo preparó para lo que sus ojos de elfo captarían en la hora del eclipse.\n\n\n\nMientras otros solo veían humo y muerte, la aguzada visión de Ainur atravesó el velo de la tormenta púrpura. Allí, donde los templos de Amatsukuni se hundían en el abismo, vio cómo el antiguo pueblo kunita se alzaba de nuevo... pero no como mártires, sino como cáscaras vacías abrazadas por la **podredumbre de la no muerte**.\n\n\n\nAinur sabe lo que el resto ignora: que su hogar no solo ha sido destruido, sino profanado. Ahora, en la penumbra de la bodega, su pasión por la naturaleza se ha transformado en un propósito más alto. Ya no busca quemar ciudades, sino encontrar un refugio donde la vida no sea una burla de sí misma y donde el rastro de la putrefacción que vio en Amatsukuni no pueda alcanzarles.\n\n\n\n*\"He visto a los muertos reclamar lo que el fuego no pudo consumir. Si la civilización es una plaga, lo que viene tras ella es el fin de todas las cosas.\"*\n\n### Glunt: El Gigante de Corazón de Cristal\n\n\n\nEl destino de Glunt estuvo marcado por el peso de su propia existencia desde el primer aliento. Nacido con un tamaño que la naturaleza no pudo sostener, su llegada al mundo supuso la partida de su madre. Aquellos minutos de silencio antes de su primera bocanada de aire dejaron una huella eterna en su mente, otorgándole una sencillez de espíritu que el mundo a menudo confunde con debilidad, pero que en realidad es **pureza absoluta**.\n\n\n\nHijo de un humilde labrador, Glunt creció entre surcos y arados, siendo el motor que aligeraba la vejez de su padre. Su viaje a la capital para el **Festival de Invierno** debía ser un premio, una maravilla de luces y alegría; en cambio, se convirtió en el inicio de su exilio. Con la misma entrega con la que araba la tierra, ayudó a cargar los grandes galeones, usando su inmensa fuerza (**Fuerza 17**) para salvar lo que pudiera del desastre.\n\nCuando el mundo se rompía en pedazos, su padre le dio una última instrucción: *\"Quédate en el barco\"*. \n\nY Glunt, fiel como una montaña, obedeció. No entiende de eclipses púrpura, ni de la no muerte que Ainur presintió; solo entiende que debe proteger a los que le rodean mientras espera volver a ver a su padre. En la oscuridad de la bodega de los piratas, Glunt es el único que mantiene una paz inquebrantable, convencido de que, si sigue siendo \"bueno\" y protege a sus amigos, cumplirá su palabra.\n\n\n\n*\"Padre dijo que me quedara. Glunt se queda. Glunt cuidará de los pequeños hasta que el sol vuelva a salir.\"*\n\n### Hiroyuki Watanabe: El Acero en la Forja\n\n\n\nHiroyuki no nació con un linaje de sangre noble, pero su espíritu siempre ha vibrado con la disciplina de los **Escudos de la Justicia**.\n\n\n\nDe constitución atlética y una fuerza que rivaliza con la de los veteranos, Hiroyuki recorría las calles de la capital con un solo propósito: conseguir los fondos necesarios para ser aceptado formalmente en la casta de los samurai.\n\n\n\nPara él, el honor no era un regalo de nacimiento, sino un trofeo que debía ser comprado con sudor y mérito.\n\n\n\nEn la ciudad de Amatsukuni, mientras otros celebraban o rezaban, él trabajaba y entrenaba, preparándose para el día en que pudiera portar la *naginata* o la espada larga bajo el estandarte de **Hachiman**, el Guardián Marcial. Sin embargo, la noche del eclipse púrpura no trajo su iniciación, sino el fin de su mundo.\n\n\n\nCapturado por los piratas de Lyndoria tras la caída de los galeones, Hiroyuki se encuentra ahora despojado de sus ahorros y de su futuro planeado. Pero en la oscuridad de la bodega, rodeado por el carisma de **Ainur**, la bondad de **Glunt**, la sabiduría de **Kazgrim** y la severidad de **Sumiko**, Hiroyuki comprende una verdad fundamental: el verdadero samurai no es aquel que paga por su entrada al dojo, sino aquel que protege a los suyos cuando todo lo demás se ha perdido. \n\n\n\n*\"Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.\"*\n\n# **La historia de Kazrim:**\n\nBackground del personaje\n\nNombre\n\nKazgrim Iwakura\n\n(pero todavía muchos lo llaman simplemente Kaz)\n\n\n\n\n# **Origen**\n\nKazgrim nació hace apenas 38 años, lo que para un enano sigue siendo casi un adolescente.\n\nCreció en un pequeño barrio de artesanos de piedra y metal en las cercanías de Kizuna-no-Miya, en el norte montañoso de Amatsukuni.\n\nSu clan no es famoso ni noble.\n\nSon canteros y constructores de templos, especialistas en trabajar la piedra volcánica de las montañas.\n\nDesde pequeño, Kazgrim creció escuchando dos cosas constantemente:\n\n- El sonido de los martillos sobre la piedra.\n- Las historias de los kami que habitan en las montañas y herramientas.\n\nEn Amatsukuni, incluso los objetos pueden albergar espíritus, y eso marcó profundamente su forma de ver el mundo. \n\n\n\n\n# **Infancia**\n\nKazgrim nunca fue el más fuerte del clan.\n\nMientras otros jóvenes competían en fuerza o en combate, él era conocido por:\n\n- hacer demasiadas preguntas\n- quedarse observando los rituales del templo\n- hablar con los ancianos y monjes\n\n\n\nSu abuelo solía decir:\n\n“La piedra escucha antes de romperse. Aprende a escuchar.”\n\nKazgrim se tomó esa frase demasiado en serio.\n\n\n\n\n# **El suceso que cambió su vida**\n\nCuando tenía 31 años, ocurrió algo extraño.\n\nDurante la reconstrucción de un pequeño santuario dedicado a Kagutsuchi, el dios del fuego, Kazgrim escuchó algo mientras trabajaba en la base del altar.\n\nNo fue una voz clara.\n\nMás bien una sensación, como si el calor de la piedra quisiera decirle algo.\n\nEsa misma noche soñó con un yunque ardiendo bajo una montaña.\n\nA la mañana siguiente, el anciano sacerdote del santuario le dijo algo inquietante:\n\n“A veces los kami hablan primero a quienes aún no saben escucharlos.”\n\nDesde entonces, Kazgrim comenzó a pasar cada vez más tiempo en templos y santuarios.\n\n\n\n\n# **Situación actual**\n\nKazgrim aún no es clérigo.\n\nEn realidad es poco más que un acólito curioso que ayuda con tareas simples:\n\n- limpiar altares\n- transportar ofrendas\n- mantener el fuego de los braseros\n- ayudar durante los festivales matsuri\n\nPero algo dentro de él está despertando.\n\nNo tiene formación completa.\n\nNo conoce aún los conjuros sagrados.\n\nSin embargo, cuando reza…\n\nlas velas a veces arden más intensamente de lo normal.\n\n\n\n\n# **Personalidad**\n\nKazgrim es:\n\n- curioso\n- sincero\n- un poco ingenuo\n- extremadamente respetuoso con las tradiciones\n\nTiene una fe instintiva, no dogmática.\n\nEn Amatsukuni es común venerar distintos kami según el momento de la vida, y Kazgrim todavía está intentando descubrir qué espíritu guía realmente su destino. \n\n\n\n\n# **Motivación para la aventura**\n\nKazgrim ha salido al mundo por tres razones:\n\n- Comprender la voz de los kami que cree haber escuchado.\n- Descubrir qué dios lo ha marcado realmente.\n- Demostrar a su clan que no hace falta ser el más fuerte para proteger a los demás.\n\n\n\n# **El guardian de la Llama perdida**\n\nEn los templos de Amatsukuni, el nombre de Kazgrim era sinónimo de devoción silenciosa y s\n\nabiduría profunda. Como enano de los templos, su vida estaba dedicada al estudio de los ciclos \n\ny a la protección de las reliquias sagradas. Se le confió la tarea más alta de su orden: \n\ncustodiar las escrituras de **==Kagutsuchi, el Fuego Renaciente==**, el dios que enseña que \n\nla destrucción es solo el preludio de la purificación.z\n\n\n\nSin embargo, la ingenuidad de su buen corazón no fue rival para la crueldad del acero pirata. \n\nEn la noche del naufragio, Kazgrim vio con horror cómo las llamas naturales de su dios eran \n\nsuperadas por el fuego de la traición. No pudo proteger los textos; las palabras sagradas se \n\nhundieron en el abismo junto con el orgullo de su pueblo.\n\nAhora, encadenado en la bodega, Kazgrim ya no es solo un bibliotecario de lo divino. \n\nEs un sabio que debe aprender que la verdadera escritura de Kagutsuchi no está en el \n\npapel, sino en la voluntad de renacer de las cenizas. Aunque se siente perdido, su sola \n\npresencia es un faro de calma para Glunt y una brújula moral para Ainur. Kazgrim busca \n\nsu camino, sin saber que el destino ya lo ha marcado para reescribir la historia de su pueblo \n\ncon sus propios actos.\n\n\n\n*\"El papel arde, pero la verdad es incombustible. Si el fuego lo devoró todo, es porque algo *\n\n*nuevo y más fuerte debe nacer de nuestras cenizas.\"*",
        "gallery": [
            "images/asset_1067045487.jpg"
        ],
        "saves": {
            "paralisis_veneno_muerte": 13,
            "varas_bastones_varitas": 14,
            "petrificacion_polimorfia": 12,
            "armas_aliento": 16,
            "conjuros": 15
        }
    },
    {
        "id": "kazgrim",
        "name": "Kazgrim Iwakura (Kaz)",
        "title": "El Guardián de la Llama Perdida",
        "role": "Clérigo",
        "tag": "Clérigo",
        "stats": {
            "clase": "Clérigo 1 (Kagutsuchi)",
            "raza": "Enano de las Colinas",
            "alineamiento": "Neutral",
            "fue": "16 (+1 daño)",
            "des": "14",
            "con": "15 (+1 PG/dado)",
            "int": "14 (7 idiomas / 60% ap)",
            "sab": "18 (+4 vs magia mental)",
            "car": "13 (Reacción +1)",
            "ca": "10",
            "pg": "9 (+5 en notas)",
            "thac0": "20"
        },
        "archetype": "Cantero enano (38 años) que escucha los kami en la roca y despierta el fuego renaciente.",
        "quote": "El papel arde, pero la verdad es incombustible. Si el fuego lo devoró todo, es porque algo nuevo y más fuerte debe nacer de nuestras cenizas.",
        "icon": "hammer",
        "badge_color": "orange",
        "accent": "#ea580c",
        "primary_image": "images/asset_-1175273093.png",
        "match_keys": [
            "Kazgrim",
            "Kaz",
            "Kazrim",
            "Iwakura",
            "Kagutsuchi",
            "La historia de Kazrim"
        ],
        "full_lore": "### Hiroyuki Watanabe: El Acero en la Forja\n\n\n\nHiroyuki no nació con un linaje de sangre noble, pero su espíritu siempre ha vibrado con la disciplina de los **Escudos de la Justicia**.\n\n\n\nDe constitución atlética y una fuerza que rivaliza con la de los veteranos, Hiroyuki recorría las calles de la capital con un solo propósito: conseguir los fondos necesarios para ser aceptado formalmente en la casta de los samurai.\n\n\n\nPara él, el honor no era un regalo de nacimiento, sino un trofeo que debía ser comprado con sudor y mérito.\n\n\n\nEn la ciudad de Amatsukuni, mientras otros celebraban o rezaban, él trabajaba y entrenaba, preparándose para el día en que pudiera portar la *naginata* o la espada larga bajo el estandarte de **Hachiman**, el Guardián Marcial. Sin embargo, la noche del eclipse púrpura no trajo su iniciación, sino el fin de su mundo.\n\n\n\nCapturado por los piratas de Lyndoria tras la caída de los galeones, Hiroyuki se encuentra ahora despojado de sus ahorros y de su futuro planeado. Pero en la oscuridad de la bodega, rodeado por el carisma de **Ainur**, la bondad de **Glunt**, la sabiduría de **Kazgrim** y la severidad de **Sumiko**, Hiroyuki comprende una verdad fundamental: el verdadero samurai no es aquel que paga por su entrada al dojo, sino aquel que protege a los suyos cuando todo lo demás se ha perdido. \n\n\n\n*\"Si Amatsukuni ha caído, yo seré el escudo de los que quedan, con o sin nombre de samurai.\"*\n\n# **La historia de Kazrim:**\n\nBackground del personaje\n\nNombre\n\nKazgrim Iwakura\n\n(pero todavía muchos lo llaman simplemente Kaz)\n\n\n\n\n# **Origen**\n\nKazgrim nació hace apenas 38 años, lo que para un enano sigue siendo casi un adolescente.\n\nCreció en un pequeño barrio de artesanos de piedra y metal en las cercanías de Kizuna-no-Miya, en el norte montañoso de Amatsukuni.\n\nSu clan no es famoso ni noble.\n\nSon canteros y constructores de templos, especialistas en trabajar la piedra volcánica de las montañas.\n\nDesde pequeño, Kazgrim creció escuchando dos cosas constantemente:\n\n- El sonido de los martillos sobre la piedra.\n- Las historias de los kami que habitan en las montañas y herramientas.\n\nEn Amatsukuni, incluso los objetos pueden albergar espíritus, y eso marcó profundamente su forma de ver el mundo. \n\n\n\n\n# **Infancia**\n\nKazgrim nunca fue el más fuerte del clan.\n\nMientras otros jóvenes competían en fuerza o en combate, él era conocido por:\n\n- hacer demasiadas preguntas\n- quedarse observando los rituales del templo\n- hablar con los ancianos y monjes\n\n\n\nSu abuelo solía decir:\n\n“La piedra escucha antes de romperse. Aprende a escuchar.”\n\nKazgrim se tomó esa frase demasiado en serio.\n\n\n\n\n# **El suceso que cambió su vida**\n\nCuando tenía 31 años, ocurrió algo extraño.\n\nDurante la reconstrucción de un pequeño santuario dedicado a Kagutsuchi, el dios del fuego, Kazgrim escuchó algo mientras trabajaba en la base del altar.\n\nNo fue una voz clara.\n\nMás bien una sensación, como si el calor de la piedra quisiera decirle algo.\n\nEsa misma noche soñó con un yunque ardiendo bajo una montaña.\n\nA la mañana siguiente, el anciano sacerdote del santuario le dijo algo inquietante:\n\n“A veces los kami hablan primero a quienes aún no saben escucharlos.”\n\nDesde entonces, Kazgrim comenzó a pasar cada vez más tiempo en templos y santuarios.\n\n\n\n\n# **Situación actual**\n\nKazgrim aún no es clérigo.\n\nEn realidad es poco más que un acólito curioso que ayuda con tareas simples:\n\n- limpiar altares\n- transportar ofrendas\n- mantener el fuego de los braseros\n- ayudar durante los festivales matsuri\n\nPero algo dentro de él está despertando.\n\nNo tiene formación completa.\n\nNo conoce aún los conjuros sagrados.\n\nSin embargo, cuando reza…\n\nlas velas a veces arden más intensamente de lo normal.\n\n\n\n\n# **Personalidad**\n\nKazgrim es:\n\n- curioso\n- sincero\n- un poco ingenuo\n- extremadamente respetuoso con las tradiciones\n\nTiene una fe instintiva, no dogmática.\n\nEn Amatsukuni es común venerar distintos kami según el momento de la vida, y Kazgrim todavía está intentando descubrir qué espíritu guía realmente su destino. \n\n\n\n\n# **Motivación para la aventura**\n\nKazgrim ha salido al mundo por tres razones:\n\n- Comprender la voz de los kami que cree haber escuchado.\n- Descubrir qué dios lo ha marcado realmente.\n- Demostrar a su clan que no hace falta ser el más fuerte para proteger a los demás.\n\n\n\n# **El guardian de la Llama perdida**\n\nEn los templos de Amatsukuni, el nombre de Kazgrim era sinónimo de devoción silenciosa y s\n\nabiduría profunda. Como enano de los templos, su vida estaba dedicada al estudio de los ciclos \n\ny a la protección de las reliquias sagradas. Se le confió la tarea más alta de su orden: \n\ncustodiar las escrituras de **==Kagutsuchi, el Fuego Renaciente==**, el dios que enseña que \n\nla destrucción es solo el preludio de la purificación.z\n\n\n\nSin embargo, la ingenuidad de su buen corazón no fue rival para la crueldad del acero pirata. \n\nEn la noche del naufragio, Kazgrim vio con horror cómo las llamas naturales de su dios eran \n\nsuperadas por el fuego de la traición. No pudo proteger los textos; las palabras sagradas se \n\nhundieron en el abismo junto con el orgullo de su pueblo.\n\nAhora, encadenado en la bodega, Kazgrim ya no es solo un bibliotecario de lo divino. \n\nEs un sabio que debe aprender que la verdadera escritura de Kagutsuchi no está en el \n\npapel, sino en la voluntad de renacer de las cenizas. Aunque se siente perdido, su sola \n\npresencia es un faro de calma para Glunt y una brújula moral para Ainur. Kazgrim busca \n\nsu camino, sin saber que el destino ya lo ha marcado para reescribir la historia de su pueblo \n\ncon sus propios actos.\n\n\n\n*\"El papel arde, pero la verdad es incombustible. Si el fuego lo devoró todo, es porque algo *\n\n*nuevo y más fuerte debe nacer de nuestras cenizas.\"*\n\nKazgrim **no es el típico clérigo de fuego**.\n\n\n\n- No busca quemar\n- No quiere hacer daño\n- Pero ha sido tocado por un dios que **sí lo exige en ciertos momentos**\n\n\n\n¿Qué merece salvarse… y qué debe arder?",
        "gallery": [
            "images/asset_-1175273093.png"
        ],
        "saves": {
            "paralisis_veneno_muerte": 10,
            "varas_bastones_varitas": 14,
            "petrificacion_polimorfia": 13,
            "armas_aliento": 16,
            "conjuros": 15
        }
    }
]
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
# 3. CURATE NPCS (CLASIFICADOS SEGÚN TLDRAW Y CAMPAÑA)
# -------------------------------------------------------------
curated_npcs = [
    # === CAMPAMENTO KUNITA EN ELKEN ===
    {
        "name": "Katsumi",
        "nickname": "Llama Custodia / Líder Temporal",
        "category": "Campamento Kunita en Elken",
        "race": "Humana Kunita",
        "age": "35-40",
        "role": "Clériga de Shien / Líder temporal del campamento",
        "location": "Campamento Kunita, Extramuros de Elken",
        "faction": "Refugiados de Amatsukuni / Culto de Shien",
        "attitude": "Protectora, devota y leal aliada",
        "status": "Viva",
        "notes": "Llama Custodia consagrada a Shien, la Llama Púrpura. Administra el campamento de los 40 supervivientes kunitas extramuros con su naginata sagrada. Al saber que los Koonies son los únicos supervivientes de su barco, la invade una gran melancolía. Pone casi todas sus esperanzas en hallar a Yoriko Asano. Revela que una hora antes del desastre, los clérigos de Amaterasu avisaron que el continente iba a ser destruido.",
        "image": "images/asset_-1819219958.png",
        "wiki_file": "katsumi__consejera_.md"
    },
    {
        "name": "Kaito",
        "nickname": "El Arraigado / El Carpintero",
        "category": "Campamento Kunita en Elken",
        "race": "Humano Kunita",
        "age": "35-40",
        "role": "Carpintero y Consejero del Campamento",
        "location": "Campamento Kunita, Extramuros de Elken",
        "faction": "Refugiados de Amatsukuni",
        "attitude": "Favorable y colaborativo",
        "status": "Vivo",
        "notes": "Comerciante y carpintero muy pragmático que considera la protección de los niños kunitas prioritaria. Intenta dirigir pero está acongojado por el futuro de su pueblo. Propuso investigar quién roba comida en la ciudad para evitar que acusen falsamente a los niños kunitas. Muy agradecido por la devolución de lo recuperado en la cala pirata.",
        "image": "images/asset_-271393713.png",
        "wiki_file": "kaito.md"
    },
    {
        "name": "Hanae",
        "nickname": "Voz de los Buscadores / La Maestra",
        "category": "Campamento Kunita en Elken",
        "race": "Humana Kunita",
        "age": "45-50",
        "role": "Maestra y Consejera / Custodia de Tradiciones",
        "location": "Campamento Kunita, Extramuros de Elken",
        "faction": "Refugiados de Amatsukuni",
        "attitude": "Favorable pero cautelosa",
        "status": "Viva",
        "notes": "Conserva la memoria histórica y las tradiciones. Su determinación por encontrar un nuevo hogar aumentó tras el regreso de los Koonies. Relata que Solkario, la Llama Purificadora, fue un dragón dorado que alcanzó la divinidad tras ayudar a vencer a los reyes nigromantes hace 300 años. Mostró reservas sobre entregar todo el botín pirata a las autoridades locales.",
        "image": "images/asset_947395825.png",
        "wiki_file": "hanae.md"
    },
    {
        "name": "Yoriko Asano",
        "nickname": "Líder de la Expedición Kunita",
        "category": "Campamento Kunita en Elken",
        "race": "Humana Kunita",
        "age": "Madura",
        "role": "Clériga de Shien & Líder original de la expedición",
        "location": "Desconocida (Desaparecida en el mar)",
        "faction": "Refugiados de Amatsukuni / Templo de Shien",
        "attitude": "Venerada por los supervivientes",
        "status": "Desaparecida",
        "notes": "Suma sacerdotisa de Shien y guía original de la flota kunita hacia Thir. Durante la travesía se quedó atrás en alta mar combatiendo a los piratas para permitir la huida del resto de navíos. No se le ha vuelto a ver con vida, pero Katsumi y el campamento mantienen viva la esperanza de encontrarla.",
        "image": "images/asset_-1408261844.png",
        "wiki_file": "yoriko_asano.md"
    },

    # === CIUDAD DE ELKEN ===
    {
        "name": "Soren Durnik",
        "nickname": "El Alcalde de Elken",
        "category": "Ciudad de Elken",
        "race": "Humano",
        "age": "Maduro",
        "role": "Alcalde de la Ciudad de Elken",
        "location": "Ayuntamiento de Elken",
        "faction": "Gobierno de Elken / Corona de Thir",
        "attitude": "Imparcial y calculador",
        "status": "Vivo",
        "notes": "Máxima autoridad civil de la ciudad. Negoció directamente la acogida de los refugiados kunitas, la venta de sus barcos y su reubicación en un campamento extramuros para evitar revueltas y descontento entre los ciudadanos de Elken.",
        "image": "images/asset_-1408261844.png",
        "wiki_file": "soren_durnik.md"
    },
    {
        "name": "Rurik Feldon",
        "nickname": "El Brazo Firme de Elken",
        "category": "Ciudad de Elken",
        "race": "Humano",
        "age": "50-55 años",
        "role": "Capitán de la Guardia de Elken",
        "location": "Cuartel del Puerto, Elken",
        "faction": "Guardia de la Ciudad de Elken",
        "attitude": "Justo, inteligente e imparcial",
        "status": "Vivo",
        "notes": "Comandante de la milicia urbana. Hombre honorable, perspicaz y de juicio ecuánime. Encontrado por primera vez en su despacho del muelle; trata los problemas de la ciudad con pragmatismo y respeta las intervenciones de los Koonies para sofocar el crimen organizado.",
        "image": "images/asset_-1266427559.png",
        "wiki_file": "rurik_feldon.md"
    },
    {
        "name": "Seraphine Alondar",
        "nickname": "La Voz de Solkarion (La Xenófoba)",
        "category": "Ciudad de Elken",
        "race": "Humana",
        "age": "35-40 años",
        "role": "Escribana Real, Magistrada y Clériga de Solkarion",
        "location": "Tribunal y Templo de Solkarion, Elken",
        "faction": "Culto de Solkarion / Corona de Thir",
        "attitude": "Hostil / Desprecia a extranjeros",
        "status": "Viva",
        "notes": "Alta, de porte severo, pelo oscuro recogido y vestido inmaculado. Dotada de una memoria prodigiosa pero implacable en su dogmatismo. Se opone firmemente a otorgar cartas de aventurero a refugiados kunitas y los somete a un escrutinio burocrático hostil. Atendió despectivamente a Glunt en el templo de Solkarion.",
        "image": "images/asset_1579031251.png",
        "wiki_file": "seraphine_alondar.md"
    },
    {
        "name": "Aleina",
        "nickname": "La Paladín Pinpín",
        "category": "Ciudad de Elken",
        "race": "Humana",
        "age": "26 años",
        "role": "Paladín de la Orden de Solkarion",
        "location": "Templo de Solkarion / En misión a la Capital",
        "faction": "Orden del Dragón Dorado de Thir",
        "attitude": "Recelosa y orgullosa",
        "status": "Viva",
        "notes": "Joven paladín consagrada a Solkarion. Conoció a los Koonies en la Taberna del Ganso y se sintió ofendida por sus maneras extravagantes, aunque les sanó las heridas. Marchó a la capital de Thir en cumplimiento de una misión de la Orden y no regresará en varios meses.",
        "image": "images/asset_-1825000868.png",
        "wiki_file": "aleina.md"
    },
    {
        "name": "Elara Frin",
        "nickname": "La Dulce Herbolaria",
        "category": "Ciudad de Elken",
        "race": "Halfling",
        "age": "Joven",
        "role": "Boticaria y Maestra de Remedios Naturales",
        "location": "Botica de Elara, Elken",
        "faction": "Amiga y Aliada de Los Koonies",
        "attitude": "Muy amigable y servicial",
        "status": "Viva",
        "notes": "Halfling bondadosa y alegre que siempre desprende aroma a tomillo fresco y adorna sus cabellos con flores silvestres. Fiel confidente del grupo: les provee ungüentos medicinales, indaga rumores sobre otros refugiados kunitas y compra hierbas raras recolectadas en la campiña de Thurmaster.",
        "image": "images/asset_-1336998075.png",
        "wiki_file": "elara_frin.md"
    },
    {
        "name": "Mandra Voss",
        "nickname": "La Anticuaria de los Arcanos",
        "category": "Ciudad de Elken",
        "race": "Humana",
        "age": "Anciana",
        "role": "Dueña de la tienda 'La Casa de los Tesoros'",
        "location": "Distrito Comercial, Elken",
        "faction": "Independiente / Erudita Arcana",
        "attitude": "Aliada comercial / Fascinada por reliquias",
        "status": "Desaparecida tras la Sesión XI",
        "notes": "Anciana perspicaz y gran coleccionista de tomos ocultos. Intercambió saberes mágicos y conjuros con Sakura a cambio de libros de valor. Mostró un singular interés por el medallón de Ainur y el grimorio de Zarcand. Al vislumbrar el Ojo de J'karaa, clausuró de improviso su negocio y desapareció sin dejar rastro.",
        "image": "images/asset_387950169.png",
        "wiki_file": "mandra_voss.md"
    },
    {
        "name": "Xikilla",
        "nickname": "La Moza del Ganso",
        "category": "Ciudad de Elken",
        "race": "Humana",
        "age": "Joven",
        "role": "Camarera de la Taberna del Ganso",
        "location": "Taberna del Ganso, Elken",
        "faction": "Población de Elken",
        "attitude": "Amable siempre que pagues la consumición",
        "status": "Viva",
        "notes": "Currita trabajadora y avispada de la Taberna del Ganso. Conoce a toda la clientela habitual del puerto y atiende incansable a los parroquianos entre jarras de hidromiel, siempre alerta a las monedas y propinas de los aventureros.",
        "image": "images/asset_-2115620674.png",
        "wiki_file": "xikilla.md"
    },
    {
        "name": "Sutter Izen",
        "nickname": "El Curtidor del Muelle",
        "category": "Ciudad de Elken",
        "race": "Humano",
        "age": "Desconocida",
        "role": "Curtidor / Intermediario de la emboscada",
        "location": "Antigua Curtiduría Fortificada, Elken (Prófugo)",
        "faction": "Crimen Organizado / Red de Holloway",
        "attitude": "Hostil / Criminal buscado",
        "status": "En busca y captura",
        "notes": "Su nombre apareció en la nota incautada en el cadáver de Harvey; fue el enlace que organizó el ataque armado contra los Koonies. Desalojó apresuradamente su curtiduría fortificada antes de que la guardia la interviniera. El grupo descubrió que allí mantuvo cautivos como rehenes a Lady Thora y a su hijo Itarus.",
        "image": "images/asset_-1408261844.png",
        "wiki_file": "sutter_izen.md"
    },
    {
        "name": "Bruiser Holloway",
        "nickname": "El Rostro del Dragón",
        "category": "Ciudad de Elken",
        "race": "Humano",
        "age": "Desconocida",
        "role": "Ladrón de Caballos y Forajido",
        "location": "Costa de los Naufragios / Prófugo",
        "faction": "Bandidos de Sutter Izen",
        "attitude": "Hostil / Peligroso forajido",
        "status": "En busca y captura (Recompensa: 1.000 PO)",
        "notes": "Temido forajido con un gran dragón tatuado en el rostro. Los Koonies descubrieron su cartel de busca y captura en el cuartel de la guardia. Mantiene vínculos estrechos de contrabando y tráfico con Sutter Izen.",
        "image": "images/asset_-1408261844.png",
        "wiki_file": "bruiser_holloway.md"
    },

    # === RIMED MALLOW ===
    {
        "name": "Mirna",
        "nickname": "La Loba de los Mares",
        "category": "Rimed Mallow",
        "race": "Humana",
        "age": "32 años",
        "role": "Capitana del Rimed Mallow & Miembro del Consejo",
        "location": "Navío Rimed Mallow / Puerto de Elken",
        "faction": "Gremio Marítimo / Consejo Municipal",
        "attitude": "Pragmática y calculadora",
        "status": "Viva",
        "notes": "Curtida capitana que rescató a los Koonies tras su naufragio en Korinn. Hábil negociadora y miembro respetado del Consejo de Elken. Se rumorea con fundamento que mantiene negocios en la sombra y acuerdos con redes de contrabando marítimo.",
        "image": "images/asset_612647077.png",
        "wiki_file": "mirna.md"
    },
    {
        "name": "Jelenneth (Jenneleth)",
        "nickname": "La Maga Samaritana",
        "category": "Rimed Mallow",
        "race": "Humana",
        "age": "21 años",
        "role": "Maga y Erudita / Aprendiz de Tauster",
        "location": "Milborne & Thurmaster",
        "faction": "Aliada Íntima de Sakura y Los Koonies",
        "attitude": "Muy amigable / 'Hermana de corazón' de Sakura",
        "status": "Viva",
        "notes": "Joven maga de mirada despierta con capa azul y alforja repleta de pergaminos. Aprendiz aventajada del maestro Tauster. Conoció a los Koonies a bordo del Rimed Mallow, donde entabló una fraternal amistad con Sakura. Ayudó a inspeccionar el Ojo de J'karaa y facilitó la llegada del grupo a Thurmaster.",
        "image": "images/asset_179927520.png",
        "wiki_file": "jelenneth__jenneleth_.md"
    },
    {
        "name": "Lord Emmothach",
        "nickname": "El Fenecido",
        "category": "Rimed Mallow",
        "race": "Humano",
        "age": "Noble maduro",
        "role": "Noble del Reino de Zahar",
        "location": "Navío Rimed Mallow / Costa de Thir",
        "faction": "Aristocracia de Zahar",
        "attitude": "Distante y señorial",
        "status": "Vivo",
        "notes": "Aristócrata del reino oriental de Zahar que viajaba como pasajero ilustre a bordo del Rimed Mallow. Su porte altivo, su comitiva y sus cofres atrajeron miradas codiciosas durante la navegación costera.",
        "image": "images/asset_-64360662.png",
        "wiki_file": "lord_emmothach.md"
    },
    {
        "name": "Lady Thora",
        "nickname": "La Dama Secuestrada",
        "category": "Rimed Mallow",
        "race": "Humana",
        "age": "Unos 30 años",
        "role": "Dama Noble / Pasajera del Rimed Mallow",
        "location": "Ciudad de Elken",
        "faction": "Nobleza Costera",
        "attitude": "Agradecida y aliviada",
        "status": "Viva",
        "notes": "Noble pasajera a bordo del Rimed Mallow. Tras desembarcar, fue secuestrada junto a su pequeño hijo Itarus por la trama criminal de Sutter Izen y encerrada en su curtiduría fortificada hasta que las pesquisas de los Koonies forzaron la huida de sus captores.",
        "image": "images/asset_2006248850.png",
        "wiki_file": "lady_thora.md"
    },
    {
        "name": "Itarus",
        "nickname": "El Zagal Secuestrado",
        "category": "Rimed Mallow",
        "race": "Humano",
        "age": "8 años",
        "role": "Hijo de Lady Thora",
        "location": "Ciudad de Elken",
        "faction": "Nobleza Costera",
        "attitude": "Inocente y curioso",
        "status": "Vivo",
        "notes": "Niño de 8 años que nunca se separa de su barquito de madera tallada. Fue raptado junto a su madre por los secuaces de Sutter Izen en la curtiduría hasta que los Koonies desmantelaron el complot.",
        "image": "images/asset_2006248850.png",
        "wiki_file": "itarus.md"
    },

    # === ISLA DE VILADEL ===
    {
        "name": "Keestake",
        "nickname": "El Antiguo Chambelán",
        "category": "Isla de Viladel",
        "race": "Humano",
        "age": "60-90 años",
        "role": "Antiguo Chambelán Real de Viladel",
        "location": "Mansión y Catacumbas de Viladel",
        "faction": "Supervivientes Corruptos de Viladel",
        "attitude": "Traidor / Manipulador",
        "status": "Muerto (Sesión 3, 24 de Sulmar)",
        "notes": "Anciano de largas barbas blancas y porte venerable, hallado supuestamente cautivo de orcos en Viladel. Fingió guiar al grupo hacia una ruta segura para tenderles una emboscada fatal en las catacumbas de la mansión en ruinas, donde cayó derrotado en combate.",
        "image": "images/asset_966061567.png",
        "wiki_file": "keestake.md"
    },

    # === VALLE DE MILBORNE & THURMASTER ===
    {
        "name": "Tauster",
        "nickname": "El Mago de la Torre de Thurmaster",
        "category": "Valle de Milborne & Thurmaster",
        "race": "Humano",
        "age": "Veterano erudito",
        "role": "Mago veterano, sabio y maestro de Jelenneth",
        "location": "Torre de Thurmaster",
        "faction": "Independiente / Círculo Arcano",
        "attitude": "Paranoico, brillante y desconfiado",
        "status": "Vivo",
        "notes": "Hechicero bajo, rechoncho y de mirada inquisitiva. Maestro de Jelenneth. Identificó con precisión los artefactos mágicos de los Koonies. Instó al grupo a asegurar una reliquia arcana antes que magos rivales y ofertó una elevada suma por el anillo sellador de la torre de Zenopus.",
        "image": "images/asset_-1273186683.png",
        "wiki_file": "tauster.md"
    },
    {
        "name": "El Viejo Oso",
        "nickname": "El Enano de la Ciudadela Perdida",
        "category": "Valle de Milborne & Thurmaster",
        "race": "Enano",
        "age": "Veterano anciano",
        "role": "Veterano combatiente enano y bebedor en Milborne",
        "location": "Posada de Milborne",
        "faction": "Antiguos Clanes Enanos de las Montañas",
        "attitude": "Amistoso / Revelador de enigmas",
        "status": "Vivo",
        "notes": "Cojea de una pierna rota en su mocedad durante el fallido asalto para recuperar su ciudadela natal. Compartió charlas y jarras con Kaz en la posada, revelando la existencia de inmensas forjas subterráneas y templos primitivos cuyas inscripciones coinciden con la escritura sagrada kunita.",
        "image": "images/asset_1063611285.jpg",
        "wiki_file": "el_viejo_oso.md"
    },

    # === MISTERIOS ARCANOS & NIGROMANCIA ===
    {
        "name": "Zenopus (Zenotus)",
        "nickname": "El Archimago de la Colina",
        "category": "Misterios Arcanos & Nigromancia",
        "race": "Humano",
        "age": "Histórico (Siglos atrás)",
        "role": "Archimago Nigromante y Erudito Primordial",
        "location": "Torre en Ruinas del Cementerio, Elken",
        "faction": "Círculo Arcano de Thir (Antiguo)",
        "attitude": "Amenaza Histórica y Misterio",
        "status": "Fallecido hace siglos",
        "notes": "Poderoso mago que alzó su torre sobre un santuario primordial. Sus manuscritos secretos revelaron el origen del azote de las venas negras y el remedio de Kanatsu-mi en el Río de la Vida. Su torre alberga autómatas de bronce y cámaras selladas.",
        "image": "images/asset_1060867694.png",
        "wiki_file": "zenopus__zenotus_.md"
    },
    {
        "name": "Zarcand (Z.)",
        "nickname": "El Nigromante del Tercer Ojo",
        "category": "Misterios Arcanos & Nigromancia",
        "race": "Humano",
        "age": "Desconocida",
        "role": "Nigromante de los Callejones de Elken",
        "location": "Bajos Fondos de Elken (Prófugo)",
        "faction": "Cultos Nigrománticos Prohibidos",
        "attitude": "Enemigo Mortal de Los Koonies",
        "status": "Malherido / En paradero desconocido",
        "notes": "Mago oscuro que operaba clandestinamente en un almacén portuario. Durante el combate final, Sakura le hendió una herida frontal que asemeja un 'tercer ojo' místico. Abandonó un valioso grimorio arcano antes de evadirse en las sombras.",
        "image": "images/asset_-1864950625.png",
        "wiki_file": "zarcand__z__.md"
    }
]

# -------------------------------------------------------------
# 4. MYSTERIES & ATLAS & TREASURY
# -------------------------------------------------------------
mysteries = [
    {
        "id": "frescos-kanatsu-mi",
        "title": "Los Frescos del Sanctum de Kanatsu-mi y el Décimo Dios",
        "priority": "Alta",
        "status": "Descubierto / Enigma Teológico",
        "category": "Destino de Kazgrim & Cosmología",
        "image": "images/asset_2330689914.jpg",
        "description": "Al entrar Kaz con su símbolo sagrado, las paredes del sanctum se iluminaron con cuatro frescos de la Corte Celestial. Revelan la Llama Dorada de Kagutsuchi que coexiste con el agua y nutre, un círculo de dioses concebido para diez pero pintado con nueve, la ausencia deliberada de Shien y un vigía solitario conteniendo la oscuridad exterior.",
        "clues": [
            "Panel I: Llegada a Thir-Lashan. Kagutsuchi porta una llama roja descendente (destrucción) y una dorada ascendente (crecimiento).",
            "Panel II: Comunión elemental. Las antiguas oraciones litúrgicas de Kaz eran instrucciones técnicas literales.",
            "Panel III: Kagutsuchi toca la fuente con fuego dorado. Fuego y agua coexisten sin destruirse en la piedra sagrada.",
            "Panel IV: Un vigía anónimo de espaldas mantiene a raya la oscuridad exterior. El círculo protector divino tiene espacio para un décimo dios.",
            "La Triple Ausencia de Shien: Omitida en la puerta de obsidiana, los estantes superiores y los frescos por razones desconocidas.",
            "Perspectiva fija: Todos los paneles comparten un punto de vista elevado idéntico y las sombras se alejan del espectador."
        ]
    },
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

deities = [
    {
        "id": "aelhar",
        "name": "Aelhar",
        "title": "la Madre Tierra",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Diosa Mayor",
        "plane": "Plano Material",
        "alignment": "N",
        "alignment_name": "Neutral Auténtico",
        "portfolio": [
            "Tierra",
            "Fertilidad",
            "Comunidad",
            "Ciclos naturales",
            "Refugio"
        ],
        "symbol": "Disco de piedra con una hoja y ramas.",
        "worshippers": "Agricultores, comunidades rurales, druidas, elfos de los bosques, tribus bárbaras que viven de la tierra, y toda sociedad que dependa de la siembra y la cosecha. Se la invoca en partos, matrimonios y funerales, y también en la construcción de hogares.",
        "cleric_order": "Custodios del Círculo (Druidas)",
        "cleric_requirements": "Los mismos que para druidas.",
        "cleric_alignment": "Neutral (N).",
        "weapons": "Bastón, hoz, lanza, honda, daga, garrote.",
        "armor": "Cualquier armadura no metálica.",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Animal",
            "Plant",
            "Weather",
            "Healing",
            "Creation",
            "Elemental (Earth)",
            "Protection",
            "Guardian."
        ],
        "spheres_minor": [
            "Divination",
            "Sun",
            "Travelers",
            "Charm",
            "Law",
            "Wards."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Comunión con la Naturaleza",
                "description": "Habilidades y progresión estándar de druida de AD&D 2ª Edición."
            },
            {
                "level": 3,
                "name": "Paso sin Huellas",
                "description": "Capacidad de transitar bosques y terrenos agrestes sin dejar rastro."
            },
            {
                "level": 7,
                "name": "Forma Animal",
                "description": "Capacidad de cambiar de forma a criaturas naturales de la tierra."
            }
        ],
        "vestment": "Túnicas verdes o pardas adornadas con hojas y semillas, coronas sencillas de ramas o flores en ceremonias. Para viajes, suelen vestir de manera práctica, con capas terrosas y bastón.",
        "organization": "Los Custodios del Círculo se organizan en pequeños círculos locales que toman decisiones colectivas. No existe una jerarquía centralizada; cada comunidad es autónoma, aunque todos los círculos reconocen ciertos puntos comunes: respeto por la tierra, neutralidad y preservación de los ciclos.",
        "rituals": "• El Primer Fruto: la primera cosecha o presa de la temporada se ofrece a la tierra en agradecimiento. • El Equinoccio de Otoño: acción de gracias por la cosecha. • Los Tres Días del Descanso: rito funerario en el que se devuelve al difunto a la tierra.",
        "allies_enemies": "Aliados: Tharion (el mar) en su cooperación con los ciclos; Veyran (pacto) en la organización social; Dalmar (umbrales) en los ritos de paso. Oponentes: Selkar, quien simboliza la traición y la muerte súbita que rompe el ciclo natural. Relación ambivalente: Issarel, pues sus terremotos destruyen la fertilidad de la tierra pero también la renuevan.",
        "dogma": "El culto de Aelhar enseña que todo tiene un tiempo: la siembra, la cosecha, el nacimiento y la muerte. Su mensaje central es la armonía con la tierra y la comunidad. Los Custodios del Círculo predican la moderación, la reciprocidad y el respeto por los ciclos. El desequilibrio —ya sea por codicia, guerra o traición— rompe el tejido natural y atrae la ruina.",
        "stronghold": "Los sacerdotes de Aelhar, al alcanzar nivel 9, pueden establecer un Círculo Sagrado, generalmente en bosques, claros o colinas fértiles. Allí atraen seguidores: druidas menores, campesinos devotos y animales protectores. Dichos círculos se convierten en centros de reunión, enseñanza y rituales de la comunidad.",
        "campaign_link": "Madre Tierra y deidad primordial de la naturaleza en Eranthys. Sus Círculos de druidas protegen las tierras agrestes y los ciclos de vida y cosecha.",
        "icon": "🌿"
    },
    {
        "id": "liryel",
        "name": "Liryel",
        "title": "Tejedora del Velo",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Diosa Mayor",
        "plane": "Arbórea",
        "alignment": "CB",
        "alignment_name": "Caótico Bueno",
        "portfolio": [
            "Magia",
            "Misterio",
            "Sueños",
            "Inspiración."
        ],
        "symbol": "Espiral azul con un ojo blanco en el centro.",
        "worshippers": "Soñadores, bardos, poetas, magos errantes, adivinos y todos aquellos que buscan la inspiración en lo oculto. Sus fieles suelen provenir de comunidades élficas, aunque también es venerada por artistas humanos y tribus que interpretan los sueños como mensajes divinos. Sus templos son raros, pero abundan los pequeños santuarios en bosques y colinas, donde se dejan ofrendas de flores y canciones nocturnas.",
        "cleric_order": "Tejedores del Velo",
        "cleric_requirements": "Sabiduría 12, Inteligencia 13",
        "cleric_alignment": "CB, CN, NB.",
        "weapons": "Daga, bastón, maza, honda.",
        "armor": "Armadura ligera no metálica.",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Charm",
            "Divination",
            "Healing",
            "Protection",
            "Thought",
            "Guardian."
        ],
        "spheres_minor": [
            "Creation",
            "Sun",
            "Travelers",
            "Weather",
            "Combat",
            "Necromantic."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Refugio del Velo",
                "description": "el clérigo puede lanzar sanctuary 1/día."
            },
            {
                "level": 5,
                "name": "Ecos del Espejo",
                "description": "el clérigo puede lanzar mirror image 1/semana."
            },
            {
                "level": 9,
                "name": "Mensaje Onírico",
                "description": "el clérigo puede lanzar dream 1/semana."
            }
        ],
        "vestment": "Los Tejedores del Velo llevan túnicas azul oscuro con bordados en plata que representan espirales y ojos. Sus símbolos suelen estar pintados en máscaras o velos semitransparentes que cubren parte del rostro.",
        "organization": "No existe una jerarquía central entre los sacerdotes de Liryel. Actúan de forma independiente, reuniéndose en ocasiones especiales para interpretar visiones colectivas o celebrar grandes festivales. Muchos viajan como consejeros o artistas errantes.",
        "rituals": "Los ritos anuales los celebra cada miembro en secreto.",
        "allies_enemies": "Aliados: Aelhar (ciclos y tierra) y Bereth (renovación y caza), pues los sueños anuncian la fertilidad y la protección. Oponentes: Selkar, cuya oscuridad y traición se oponen a la verdad revelada en los sueños. Relación ambivalente: Tharion, pues sus tormentas pueden traer inspiración o desesperación.",
        "dogma": "El culto de Liryel enseña que los sueños y misterios son el velo que cubre las verdades más profundas. A través de la inspiración, la magia y el arte, los fieles buscan comprender lo oculto y compartirlo con los demás. La mentira consciente es condenada, pero el enigma y la metáfora son considerados caminos hacia la sabiduría.",
        "stronghold": "Los sacerdotes de Liryel, al alcanzar nivel 9, pueden establecer un Santuario del Velo, normalmente en bosques, colinas o enclaves oníricos. Estos lugares atraen bardos, artistas, visionarios y soñadores. Se convierten en centros de inspiración, donde lo real y lo ilusorio se entremezclan.",
        "campaign_link": "Diosa Mayor de Arbórea. Fue invocada por Kazgrim en la oubliette (Sesión 4), respondiendo con un orbe celestial de luz que reveló la salida secreta a los Koonies.",
        "icon": "✨"
    },
    {
        "id": "selkar",
        "name": "Selkar",
        "title": "Portador de la Máscara",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Mayor",
        "plane": "Gehenna",
        "alignment": "NM",
        "alignment_name": "Neutral Malvado",
        "portfolio": [
            "Noche",
            "Secretos",
            "Traición",
            "Muerte súbita",
            "Venganza"
        ],
        "symbol": "Media máscara oscura con una daga.",
        "worshippers": "Asesinos, conspiradores, espías, vengadores solitarios, sectas ocultas y aquellos que buscan el poder a través del miedo y la traición. En aldeas pequeñas, se lo invoca en silencio para protegerse de la traición o vengar una ofensa; en las ciudades, se le rinde culto clandestino en gremios de asesinos o cofradías secretas.",
        "cleric_order": "Portadores de la Máscara",
        "cleric_requirements": "Sabiduría 12+, Destreza 12+.",
        "cleric_alignment": "NM, CM, CN.",
        "weapons": "Daga, espada corta, garrote, honda",
        "armor": "Cuero o cuero tachonado, escudos pequeños.",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Charm",
            "Divination",
            "Guardian",
            "Healing",
            "Necromantic",
            "Protection",
            "Wards."
        ],
        "spheres_minor": [
            "Combat",
            "Summoning",
            "Thought",
            "Travelers",
            "Weather."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Manto de Sombras",
                "description": "el clérigo puede moverse en la sombra y en silencio como un explorador de su nivel"
            },
            {
                "level": 5,
                "name": "Toque del Vengador",
                "description": "el clérigo puede lanzar cause serious wounds 1/día."
            },
            {
                "level": 9,
                "name": "Máscara del Engaño",
                "description": "el clérigo puede lanzar misdirection 1/día."
            }
        ],
        "vestment": "Los Portadores de la Máscara usan túnicas negras o grises, siempre cubriendo el rostro con una media máscara de madera o metal. La daga ceremonial es indispensable en todo rito.",
        "organization": "La iglesia de Selkar es secreta y descentralizada. Cada célula actúa como una cofradía independiente, muchas veces camufladas como gremios o sociedades nocturnas. Sus líderes se conocen como Sombras Mayores.",
        "rituals": "La Noche de las Cuchillas: celebración clandestina donde se hacen juramentos de venganza. El Velo de la Medianoche: rito mensual en el que los fieles permanecen en silencio absoluto, entregando secretos al dios. El Juramento Roto: rito de sangre en el que se ajustician a traidores bajo el amparo de Selkar.",
        "allies_enemies": "Aliados: Issarel (caos y ruptura), en ocasiones como herramienta de destrucción. Oponentes: Veyran (pacto), Dalmar (ley) y Aelhar (ciclos de vida). Relación ambivalente: Liryel, cuyo misterio y enigma pueden ser usados tanto para inspirar como para manipular.",
        "dogma": "Selkar enseña que la traición es un arma tan poderosa como la espada, y que la oscuridad guarda las verdades que otros temen. Sus fieles creen que la venganza es un deber sagrado y que los secretos son la moneda del poder.",
        "stronghold": "Los sacerdotes de Selkar, al alcanzar nivel 9, pueden fundar un Santuario de Sombras, normalmente escondido en catacumbas, callejones o cavernas. Estos lugares atraen asesinos, espías y vengadores.",
        "campaign_link": "Dios de las sombras, traición y muerte repentina. Venerado en los bajos fondos, gremios de ladrones y asesinos clandestinos; opuesto frontal a Dalmar y Aelhar.",
        "icon": "🎭"
    },
    {
        "id": "tharion",
        "name": "Tharion",
        "title": "Señor del Mar",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Mayor",
        "plane": "Ysgard",
        "alignment": "CN",
        "alignment_name": "Caótico Neutral",
        "portfolio": [
            "Mar",
            "Tormentas",
            "Viaje",
            "Pesca",
            "Peligro y oportunidad"
        ],
        "symbol": "Caracola azul sobre olas.",
        "worshippers": "Marineros, pescadores, navegantes, exploradores, tribus costeras y todos aquellos que viven bajo la amenaza y la bendición del mar. Es común entre comunidades de la Costa de los Naufragios, los clanes bárbaros que viajan por mar y los elfos marinos. Sus templos suelen ser altares en acantilados o muelles donde el mar rompe con fuerza.",
        "cleric_order": "Voces de la Tormenta",
        "cleric_requirements": "Sabiduría 12, Constitución 12.",
        "cleric_alignment": "Caótico Neutral (CN), Neutral (N), Caótico Bueno (CB).",
        "weapons": "Tridente, lanza, jabalina, red, daga, maza.",
        "armor": "Cualquier armadura ligera; escudos permitidos. Esferas mayores : All, Elemental (Water, Air), Weather, Combat, Protection, Divination, Travelers, Guardian. Esferas menores: Healing, Creation, Sun, Charm, Animal, Plant. Poderes concedidos: • Nivel 1 – Bendición del Navegante: el clérigo puede lanzar create water o purify food & drink 1/día (elige al obtener el poder). • Nivel 5 – Aliento del Mar: el clérigo puede lanzar water breathing 1/día. • Nivel 9 – Llamar la Tormenta: el clérigo puede lanzar call lightning 1/día, siempre bajo cielo abierto. Vestimenta clerical: Las Voces de la Tormenta visten túnicas azul oscuro o verde marino con bordados en plata que representan olas y rayos. Para el viaje, suelen llevar capas impermeables de pieles enceradas y collares con conchas o caracolas. ORGANIZACIÓN CLERICAL Su estructura es descentralizada. Cada puerto o comunidad costera tiene su propio consejo de sacerdotes, aunque todos reconocen a los templos erigidos en los acantilados de la Costa de los Naufragios como los más antiguos. Los sacerdotes de Tharion valoran la libertad personal y predican que el mar concede tanto como arrebata. FIESTAS Y RITUALES • El Sacrificio de la Ola: al inicio de la temporada de pesca, se arroja al mar la primera captura como ofrenda. • La Tormenta Sagrada: durante las primeras tormentas de verano, los fieles cantan y bailan bajo la lluvia en señal de aceptación de la voluntad del mar. • La Vigilia del Náufrago: rito funerario en el que los cuerpos son entregados al mar en balsas adornadas con antorchas. ALIADOS Y ENEMIGOS DIVINOS Aliados: Aelhar (tierra) en su cooperación de ciclos; Elineth (mareas) y Ydran (ríos), como parte de la misma corriente vital. Oponentes: Selkar, que encarna la traición y la muerte súbita que no respeta los ciclos ni la lucha justa. Relación ambivalente: Issarel, pues sus terremotos pueden desatar marejadas que devastan o renuevan. DOGMA Y CULTO El culto de Tharion enseña que el mar es un campo de pruebas: peligroso y fértil, generoso y cruel. La vida es un viaje de riesgos, y aquellos que se enfrentan a la tormenta con valor son los que prosperan. Las Voces de la Tormenta predican la aceptación de la incertidumbre y el respeto a la fuerza indómita del mar. SEGUIDORES Y FORTALEZAS Los sacerdotes de Tharion, al alcanzar nivel 9, pueden establecer un Templo de la Ola, normalmente en un puerto o en un acantilado. Estos templos atraen marineros, exploradores y aventureros que buscan la bendición del mar antes de partir. Los seguidores incluyen guerreros marinos, navegantes y bardos que honran al dios con cantos durante las tormentas.",
        "magic_items": "",
        "spheres_major": [],
        "spheres_minor": [
            "Healing",
            "Creation",
            "Sun",
            "Charm",
            "Animal",
            "Plant."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Bendición del Navegante",
                "description": "el clérigo puede lanzar create water o purify food & drink 1/día (elige al obtener el poder)."
            },
            {
                "level": 5,
                "name": "Aliento del Mar",
                "description": "el clérigo puede lanzar water breathing 1/día."
            },
            {
                "level": 9,
                "name": "Llamar la Tormenta",
                "description": "el clérigo puede lanzar call lightning 1/día, siempre bajo cielo abierto."
            }
        ],
        "vestment": "Las Voces de la Tormenta visten túnicas azul oscuro o verde marino con bordados en plata que representan olas y rayos. Para el viaje, suelen llevar capas impermeables de pieles enceradas y collares con conchas o caracolas.",
        "organization": "Su estructura es descentralizada. Cada puerto o comunidad costera tiene su propio consejo de sacerdotes, aunque todos reconocen a los templos erigidos en los acantilados de la Costa de los Naufragios como los más antiguos. Los sacerdotes de Tharion valoran la libertad personal y predican que el mar concede tanto como arrebata.",
        "rituals": "• El Sacrificio de la Ola: al inicio de la temporada de pesca, se arroja al mar la primera captura como ofrenda. • La Tormenta Sagrada: durante las primeras tormentas de verano, los fieles cantan y bailan bajo la lluvia en señal de aceptación de la voluntad del mar. • La Vigilia del Náufrago: rito funerario en el que los cuerpos son entregados al mar en balsas adornadas con antorchas.",
        "allies_enemies": "Aliados: Aelhar (tierra) en su cooperación de ciclos; Elineth (mareas) y Ydran (ríos), como parte de la misma corriente vital. Oponentes: Selkar, que encarna la traición y la muerte súbita que no respeta los ciclos ni la lucha justa. Relación ambivalente: Issarel, pues sus terremotos pueden desatar marejadas que devastan o renuevan.",
        "dogma": "El culto de Tharion enseña que el mar es un campo de pruebas: peligroso y fértil, generoso y cruel. La vida es un viaje de riesgos, y aquellos que se enfrentan a la tormenta con valor son los que prosperan. Las Voces de la Tormenta predican la aceptación de la incertidumbre y el respeto a la fuerza indómita del mar.",
        "stronghold": "Los sacerdotes de Tharion, al alcanzar nivel 9, pueden establecer un Templo de la Ola, normalmente en un puerto o en un acantilado. Estos templos atraen marineros, exploradores y aventureros que buscan la bendición del mar antes de partir. Los seguidores incluyen guerreros marinos, navegantes y bardos que honran al dios con cantos durante las tormentas.",
        "campaign_link": "Dios de las tempestades oceánicas y los marineros temerarios. Los barcos en la bahía de Elken y las rutas marítimas temen su cólera impredecible.",
        "icon": "🌊"
    },
    {
        "id": "veyran",
        "name": "Veyran",
        "title": "Guardián del Pacto",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Mayor",
        "plane": "Bytopia",
        "alignment": "NB",
        "alignment_name": "Neutral Bueno",
        "portfolio": [
            "Comercio",
            "Pacto",
            "Hospitalidad",
            "Justicia."
        ],
        "symbol": "Dos manos entrelazadas sobre una moneda.",
        "worshippers": "Mercaderes, jueces, notarios, posaderos, diplomáticos y toda persona que viva del acuerdo justo y la hospitalidad. Se le invoca en contratos, bodas y alianzas entre comunidades.",
        "cleric_order": "Guardianes del Pacto",
        "cleric_requirements": "Sabiduría 12, Carisma 13.",
        "cleric_alignment": "NB, LN, N.",
        "weapons": "Maza, martillo, daga, bastón.",
        "armor": "Cualquier armadura o escudo. Esferas mayores : All, Charm, Law, Healing, Protection, Guardian, Divination, Creation. Esferas menores: Travelers, Sun, Combat, Wards, Thought, Time, Elemental (Earth). Poderes concedidos: • Nivel 1 – Bendición del Anfitrión: el clérigo puede lanzar bless 1/día (como el conjuro de clérigo). • Nivel 5 – Escudo del Pacto: el clérigo y todos los aliados en un radio de 3 m reciben un bonificador de +2 a tiradas de salvación contra conjuros de Encantamiento/Compulsión durante 1 turno. Usable 1/día. • Nivel 9 – Juramento Sagrado: el clérigo puede lanzar geas (limitado como quest) 1/semana, solo para pactos aceptados voluntariamente. Vestimenta clerical: Los Guardianes del Pacto visten túnicas blancas o grises, ceñidas con cordones dorados. Llevan siempre consigo un sello o anillo con su símbolo sagrado, y suelen portar tablillas o rollos de pergamino para inscribir juramentos. ORGANIZACIÓN CLERICAL La iglesia de Veyran mantiene consejos regionales que actúan como mediadores y jueces. Aunque descentralizados, todos los consejos reconocen la autoridad de los más antiguos en Bytopia. El énfasis está en la cooperación y la justicia comunitaria. FIESTAS Y RITUALES • El Día del Sello: conmemoración anual en que se renuevan contratos y tratados. • La Noche de la Hospitalidad: todos los templos abren sus puertas y ofrecen comida y refugio a viajeros. • Juramentos de Sangre: rito solemne en el que dos partes sellan un pacto bajo la mirada de Veyran. ALIADOS Y ENEMIGOS DIVINOS Aliados: Dalmar (umbrales y ley), Aelhar (tierra fértil y comunidad). Oponentes: Selkar, por la traición y el quebranto de la palabra. Relación ambivalente: Tharion, cuya imprevisibilidad desafía la estabilidad de los pactos. DOGMA Y CULTO El culto de Veyran enseña que el pacto es sagrado: la palabra dada construye la comunidad y protege frente al caos. La hospitalidad es deber sagrado, y quien rompe un juramento se coloca fuera del círculo de la confianza. SEGUIDORES Y FORTALEZAS Los sacerdotes de Veyran, al alcanzar nivel 9, pueden establecer una Casa del Pacto, que actúa a la vez como templo, tribunal y posada. Estos lugares se convierten en centros de comercio, justicia y refugio para viajeros.",
        "magic_items": "",
        "spheres_major": [],
        "spheres_minor": [
            "Travelers",
            "Sun",
            "Combat",
            "Wards",
            "Thought",
            "Time",
            "Elemental (Earth)."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Bendición del Anfitrión",
                "description": "el clérigo puede lanzar bless 1/día (como el conjuro de clérigo)."
            },
            {
                "level": 5,
                "name": "Escudo del Pacto",
                "description": "el clérigo y todos los aliados en un radio de 3 m reciben un bonificador de +2 a tiradas de salvación contra conjuros de Encantamiento/Compulsión durante 1 turno. Usable 1/día."
            },
            {
                "level": 9,
                "name": "Juramento Sagrado",
                "description": "el clérigo puede lanzar geas (limitado como quest) 1/semana, solo para pactos aceptados voluntariamente."
            }
        ],
        "vestment": "Los Guardianes del Pacto visten túnicas blancas o grises, ceñidas con cordones dorados. Llevan siempre consigo un sello o anillo con su símbolo sagrado, y suelen portar tablillas o rollos de pergamino para inscribir juramentos.",
        "organization": "La iglesia de Veyran mantiene consejos regionales que actúan como mediadores y jueces. Aunque descentralizados, todos los consejos reconocen la autoridad de los más antiguos en Bytopia. El énfasis está en la cooperación y la justicia comunitaria.",
        "rituals": "• El Día del Sello: conmemoración anual en que se renuevan contratos y tratados. • La Noche de la Hospitalidad: todos los templos abren sus puertas y ofrecen comida y refugio a viajeros. • Juramentos de Sangre: rito solemne en el que dos partes sellan un pacto bajo la mirada de Veyran.",
        "allies_enemies": "Aliados: Dalmar (umbrales y ley), Aelhar (tierra fértil y comunidad). Oponentes: Selkar, por la traición y el quebranto de la palabra. Relación ambivalente: Tharion, cuya imprevisibilidad desafía la estabilidad de los pactos.",
        "dogma": "El culto de Veyran enseña que el pacto es sagrado: la palabra dada construye la comunidad y protege frente al caos. La hospitalidad es deber sagrado, y quien rompe un juramento se coloca fuera del círculo de la confianza.",
        "stronghold": "Los sacerdotes de Veyran, al alcanzar nivel 9, pueden establecer una Casa del Pacto, que actúa a la vez como templo, tribunal y posada. Estos lugares se convierten en centros de comercio, justicia y refugio para viajeros.",
        "campaign_link": "Dios del comercio justo, la hospitalidad y los pactos sellados. Sus sacerdotes ejercen de mediadores y garantes en tratados de ciudades y gremios.",
        "icon": "⚖️"
    },
    {
        "id": "bereth",
        "name": "Bereth",
        "title": "Guardián de la Manada",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Menor",
        "plane": "las Beastlands",
        "alignment": "NB",
        "alignment_name": "Neutral Bueno",
        "portfolio": [
            "Protección animal",
            "Caza justa",
            "Bestias guardianas"
        ],
        "symbol": "Huella de lobo sobre piedra.",
        "worshippers": "Cazadores, rangers, druidas, exploradores y tribus que dependen de la caza para sobrevivir. Sus fieles respetan a Bereth porque enseña que la caza debe hacerse con equilibrio: nunca por crueldad, siempre por necesidad y justicia. Es venerado en aldeas fronterizas, comunidades bárbaras y clanes élficos de bosques profundos.",
        "cleric_order": "Cazadores del Alba",
        "cleric_requirements": "Sabiduría 12+, Destreza 12+",
        "cleric_alignment": "NB, N, CB.",
        "weapons": "Arco largo, arco corto, lanza, jabalina, cimitarra, espada corta, daga.",
        "armor": "Hasta cota de mallas; escudos permitidos.",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Animal",
            "Healing",
            "Plant",
            "Protection",
            "Combat",
            "Guardian."
        ],
        "spheres_minor": [
            "Creation",
            "Divination",
            "Elemental (Earth)",
            "Travelers",
            "Sun",
            "Weather."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Sentido del Cazador",
                "description": "el clérigo puede lanzar animal friendship 1/día."
            },
            {
                "level": 5,
                "name": "Vista del Alba",
                "description": "el clérigo obtiene un bonificador constante de +2 a tiradas de salvación contra veneno."
            },
            {
                "level": 9,
                "name": "Aliado de la Manada",
                "description": "el clérigo puede lanzar conjure animals 1/semana."
            }
        ],
        "vestment": "Los Cazadores del Alba visten capas de piel o cuero teñidas en tonos verdes y marrones, adornadas con plumas y colmillos. Portan siempre un arco o lanza como símbolo de su deber.",
        "organization": "Los clérigos de Bereth forman círculos de caza que se dispersan por bosques y fronteras. Su jerarquía es flexible: el liderazgo lo ostenta aquel con más experiencia en la caza o en la protección de la comunidad.",
        "rituals": "• La Primera Caza: rito de iniciación en el que los jóvenes cazadores dedican su primera presa a Bereth. • El Aullido del Alba: ceremonia mensual al amanecer, donde los fieles entonan cánticos imitando a los lobos. • El Banquete Justo: tras una cacería importante, la carne se reparte equitativamente entre todos, reflejando el dogma de justicia y equilibrio.",
        "allies_enemies": "Aliados: Aelhar (ciclos y fertilidad) y Liryel (inspiración y sueños), pues juntos representan la vida y la renovación Oponentes: Selkar, que corrompe la caza en asesinato y traición. Relación ambivalente: Tharion, cuyas tormentas pueden arruinar o favorecer la caza.",
        "dogma": "El culto de Bereth enseña que la caza es un acto sagrado de equilibrio: el depredador y la presa son parte del mismo ciclo. Prohíbe la crueldad gratuita y condena el exceso. La manada (la comunidad) debe ser protegida por encima de los deseos individuales.",
        "stronghold": "Los sacerdotes de Bereth, al alcanzar nivel 9, pueden fundar un Refugio de la Manada, un santuario en los bosques o montañas donde se instruye en la caza justa y la protección animal. Estos refugios atraen rangers, druidas y exploradores que buscan equilibrio en la naturaleza.",
        "campaign_link": "Dios de la caza justa y las bestias guardianas en las Beastlands. Sus seguidores protegen el equilibrio faunístico y castigan la caza indiscriminada.",
        "icon": "🐺"
    },
    {
        "id": "dalmar",
        "name": "Dalmar",
        "title": "Vigilante del Umbral",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Menor",
        "plane": "Arcadia",
        "alignment": "LN",
        "alignment_name": "Legal Neutral",
        "portfolio": [
            "Umbrales",
            "Hogar",
            "Fronteras",
            "Protección",
            "Ley."
        ],
        "symbol": "Llave de hierro entrelazada con una rama.",
        "worshippers": "Guardianes de puertas y murallas, jueces, alcaldes de aldeas, paladines y comunidades que valoran la seguridad y la ley. Se le invoca al construir casas, erigir murallas o sellar pactos de defensa común. Es venerado en aldeas fortificadas, ciudades fronterizas y en cualquier lugar donde los habitantes deban resistir amenazas externas.",
        "cleric_order": "Vigilantes del Umbral",
        "cleric_requirements": "Sabiduría 12, Fuerza 12",
        "cleric_alignment": "LN, N, NB.",
        "weapons": "Maza, martillo, bastón, lanza, espada corta.",
        "armor": "Hasta cota de mallas; escudos permitidos. Esferas mayores : All, Protection, Guardian, Law, Combat, Divination, Healing. Esferas menores: Wards, Sun, Creation, Elemental (Earth), Thought, Travelers. Poderes concedidos: • Nivel 1 – Bendición del Hogar: el clérigo puede lanzar protection from evil 1/día. • Nivel 5 – Guardián Firme: el clérigo obtiene un bonificador constante de +1 a CA y +1 a todas las tiradas de salvación cuando defiende un umbral o lugar de paso (puerta, puente, entrada, santuario). • Nivel 9 – Sello del Umbral: el clérigo puede lanzar forbiddance 1/semana. Vestimenta clerical: Los Vigilantes del Umbral visten túnicas grises o blancas con bordados geométricos que recuerdan a llaves y puertas. Llevan siempre un colgante con forma de llave de hierro, símbolo de su dios. ORGANIZACIÓN CLERICAL La iglesia de Dalmar se organiza en torno a fortalezas-templo que sirven de baluarte para las comunidades. Los clérigos de mayor rango reciben el título de Custodios de Hierro. Su jerarquía es estricta, en sintonía con su alineamiento legal. FIESTAS Y RITUALES • El Alzamiento de las Llaves: ceremonia en la que se consagra una nueva casa o fortificación. • El Juramento del Umbral: rito de iniciación en el que el fiel promete proteger a la comunidad bajo la mirada de Dalmar. • La Vigilia de la Puerta: festividad anual en la que se montan guardias rituales en las entradas de pueblos y templos. ALIADOS Y ENEMIGOS DIVINOS Aliados: Veyran (pacto), Aelhar (comunidad) y Kelvar (muerte natural y ancestros). Oponentes: Selkar (traición) e Issarel (ruptura y caos) Relación ambivalente: Tharion, pues sus tormentas ponen a prueba las defensas. DOGMA Y CULTO El culto de Dalmar enseña que el hogar es sagrado y debe ser defendido contra toda amenaza. Los umbrales marcan la frontera entre el caos exterior y la paz interior. Mantener las promesas y proteger la comunidad es la mayor virtud. SEGUIDORES Y FORTALEZAS Los sacerdotes de Dalmar, al alcanzar nivel 9, pueden fundar un Templo del Umbral, que actúa como fortaleza y santuario. Estos templos atraen paladines, jueces y guardianes que buscan servir como murallas vivientes de sus comunidades.",
        "magic_items": "",
        "spheres_major": [],
        "spheres_minor": [
            "Wards",
            "Sun",
            "Creation",
            "Elemental (Earth)",
            "Thought",
            "Travelers."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Bendición del Hogar",
                "description": "el clérigo puede lanzar protection from evil 1/día."
            },
            {
                "level": 5,
                "name": "Guardián Firme",
                "description": "el clérigo obtiene un bonificador constante de +1 a CA y +1 a todas las tiradas de salvación cuando defiende un umbral o lugar de paso (puerta, puente, entrada, santuario)."
            },
            {
                "level": 9,
                "name": "Sello del Umbral",
                "description": "el clérigo puede lanzar forbiddance 1/semana."
            }
        ],
        "vestment": "Los Vigilantes del Umbral visten túnicas grises o blancas con bordados geométricos que recuerdan a llaves y puertas. Llevan siempre un colgante con forma de llave de hierro, símbolo de su dios.",
        "organization": "La iglesia de Dalmar se organiza en torno a fortalezas-templo que sirven de baluarte para las comunidades. Los clérigos de mayor rango reciben el título de Custodios de Hierro. Su jerarquía es estricta, en sintonía con su alineamiento legal.",
        "rituals": "• El Alzamiento de las Llaves: ceremonia en la que se consagra una nueva casa o fortificación. • El Juramento del Umbral: rito de iniciación en el que el fiel promete proteger a la comunidad bajo la mirada de Dalmar. • La Vigilia de la Puerta: festividad anual en la que se montan guardias rituales en las entradas de pueblos y templos.",
        "allies_enemies": "Aliados: Veyran (pacto), Aelhar (comunidad) y Kelvar (muerte natural y ancestros). Oponentes: Selkar (traición) e Issarel (ruptura y caos) Relación ambivalente: Tharion, pues sus tormentas ponen a prueba las defensas.",
        "dogma": "El culto de Dalmar enseña que el hogar es sagrado y debe ser defendido contra toda amenaza. Los umbrales marcan la frontera entre el caos exterior y la paz interior. Mantener las promesas y proteger la comunidad es la mayor virtud.",
        "stronghold": "Los sacerdotes de Dalmar, al alcanzar nivel 9, pueden fundar un Templo del Umbral, que actúa como fortaleza y santuario. Estos templos atraen paladines, jueces y guardianes que buscan servir como murallas vivientes de sus comunidades.",
        "campaign_link": "Vigilante del umbral y la ley doméstica en Arcadia. Sus bendiciones se tallan en dinteles y portones de fortalezas como las murallas de Elken y Thir.",
        "icon": "🗝️"
    },
    {
        "id": "drelk",
        "name": "Drelk",
        "title": "Señor de la Bruma",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Menor",
        "plane": "la Concordancia",
        "alignment": "N",
        "alignment_name": "Neutral Auténtico",
        "portfolio": [
            "Niebla",
            "Olvido",
            "Secretos",
            "Caminos ocultos"
        ],
        "symbol": "Espiral blanca entre sombras.",
        "worshippers": "Viajeros errantes, exploradores de pantanos, eremitas, sectas secretas y quienes buscan en el olvido una forma de paz. Sus fieles aceptan que la bruma y el olvido son parte de la vida, una transición entre lo que fue y lo que será. Es venerado en marismas, bosques cubiertos de niebla y en comunidades que valoran el silencio y el misterio.",
        "cleric_order": "Caminantes de la Bruma",
        "cleric_requirements": "Sabiduría 12, Destreza 12",
        "cleric_alignment": "N, NB, NM.",
        "weapons": "Daga, bastón, lanza, honda.",
        "armor": "Cuero o cuero tachonado; escudos pequeños",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Charm",
            "Divination",
            "Guardian",
            "Protection",
            "Weather",
            "Thought."
        ],
        "spheres_minor": [
            "Healing",
            "Creation",
            "Travelers",
            "Necromantic",
            "Combat",
            "Elemental (Water)."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Velo de Niebla",
                "description": "el clérigo puede lanzar obscurement 1/día."
            },
            {
                "level": 5,
                "name": "Sendero Velado",
                "description": "el clérigo puede lanzar pass without trace 1/día."
            },
            {
                "level": 9,
                "name": "Niebla de la Memoria",
                "description": "el clérigo puede lanzar confusion 1/semana."
            }
        ],
        "vestment": "Los Caminantes de la Bruma usan túnicas grises y blancas, a menudo deshilachadas, que parecen fundirse con la niebla. Sus símbolos suelen colgar de collares de hueso o madera blanqueada.",
        "organization": "La iglesia de Drelk no tiene una jerarquía clara. Sus sacerdotes actúan de manera dispersa, y muchos son solitarios. Cuando se reúnen, lo hacen en lugares ocultos por la bruma, sin líderes visibles, tomando decisiones por consenso silencioso.",
        "rituals": "La Vigilia de la Bruma: los fieles caminan en silencio por pantanos o bosques cubiertos de niebla, ofreciendo recuerdos escritos en tablillas que luego se sumergen en el agua. El Día del Olvido: ceremonia anual donde los fieles queman símbolos de dolor y viejas ofensas para dejarlas disolverse en el aire. Senderos Velados: rito mensual donde se recorren caminos ocultos en silencio como meditación.",
        "allies_enemies": "Aliados: Kelvar (muerte natural y ancestros) y Ydran (viajes y ríos). Oponentes: Selkar, que usa la oscuridad no para ocultar sino para traicionar. Relación ambivalente: Liryel, pues sus misterios inspiran tanto como confunden.",
        "dogma": "El culto de Drelk enseña que la niebla y el olvido no son enemigos, sino transiciones necesarias. Los secretos no son mentiras, sino velos que protegen lo que aún no debe ser revelado. El olvido es una forma de sanar.",
        "stronghold": "Los sacerdotes de Drelk, al alcanzar nivel 9, pueden fundar un Santuario de la Bruma, en pantanos, bosques o valles cubiertos de niebla. Estos lugares atraen a buscadores de paz, viajeros errantes y sectas que veneran el misterio.",
        "campaign_link": "Señor de la bruma, el silencio y los caminos olvidados. Invocado por errantes que buscan pasar inadvertidos o hallar paz frente a traumas pasados.",
        "icon": "🌫️"
    },
    {
        "id": "elineth",
        "name": "Elineth",
        "title": "Señora de las Mareas",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Diosa Menor",
        "plane": "la Concordancia",
        "alignment": "N",
        "alignment_name": "Neutral Auténtico",
        "portfolio": [
            "Mareas",
            "Pesca",
            "Ciclos lunares",
            "Navegación costera."
        ],
        "symbol": "Concha con una gota de agua en su interior.",
        "worshippers": "Pescadores, navegantes costeros, comunidades marineras y pueblos que dependen de las mareas para su sustento. Es una diosa de calma y continuidad, invocada para asegurar viajes seguros, buenas cosechas marinas y noches serenas a la luz de la luna. Sus templos suelen ser altares sencillos en playas o cabos, donde se dejan ofrendas de conchas y pescado.",
        "cleric_order": "Cantores de la Concha",
        "cleric_requirements": "Sabiduría 12, Constitución 12",
        "cleric_alignment": "N, NB, CN.",
        "weapons": "Tridente, lanza, jabalina, daga, red.",
        "armor": "Hasta cota de mallas; escudos permitidos. Esferas mayores (7): All, Elemental (Water), Healing, Divination, Protection, Guardian, Travelers. Esferas menores (6): Sun, Weather, Creation, Combat, Plant, Charm. Poderes concedidos: Nivel 1 – Don de las Aguas: el clérigo puede lanzar water breathing 1/día. Nivel 5 – Paso Lunar: el clérigo puede lanzar water walk 1/semana. Nivel 9 – Canto de las Mareas: el clérigo puede lanzar control water 1/semana. Vestimenta clerical: Los Cantores de la Concha visten túnicas en tonos azules y verdes, adornadas con conchas y perlas. Portan como símbolo sagrado una concha grande colgada al cuello o en el cinturón. ORGANIZACIÓN CLERICAL La iglesia de Elineth es sencilla y comunitaria. Cada aldea pesquera cuenta con un cantor o pequeña hermandad que dirige oraciones y ofrendas al mar. Los clérigos viajan con frecuencia entre pueblos costeros para mantener lazos de fraternidad. FIESTAS Y RITUALES El Canto de las Mareas: ceremonia diaria al amanecer y atardecer, donde se entonan himnos al ritmo de las olas. La Vigilia Lunar: rito mensual durante la luna llena, donde se encienden antorchas en la playa y se ofrecen conchas al mar. El Banquete del Mar: fiesta anual tras la primera gran pesca de primavera, en la que toda la comunidad comparte el alimento. ALIADOS Y ENEMIGOS DIVINOS Aliados: Tharion (mar y tormentas), Ydran (ríos y viajes) y Aelhar (ciclos de fertilidad). Oponentes: Selkar, pues la traición y la oscuridad quiebran la serenidad de las mareas. Relación ambivalente: Issarel, cuyos terremotos pueden alterar violentamente los mares. DOGMA Y CULTO El culto de Elineth enseña que la vida fluye en ciclos como las mareas: calma y tormenta, abundancia y escasez. La paciencia, la confianza en el ciclo y la unión comunitaria son virtudes sagradas. Se condena la avaricia y la sobrepesca, pues perturban el equilibrio del mar. SEGUIDORES Y FORTALEZAS Los sacerdotes de Elineth, al alcanzar nivel 9, pueden fundar un Santuario de la Concha, generalmente en cabos o islas costeras. Estos santuarios sirven como faros espirituales para marineros y pescadores, ofreciendo refugio, bendiciones y guía en la navegación.",
        "magic_items": "",
        "spheres_major": [],
        "spheres_minor": [],
        "powers_granted": [
            {
                "level": 1,
                "name": "Don de las Aguas",
                "description": "el clérigo puede lanzar water breathing 1/día."
            },
            {
                "level": 5,
                "name": "Paso Lunar",
                "description": "el clérigo puede lanzar water walk 1/semana."
            },
            {
                "level": 9,
                "name": "Canto de las Mareas",
                "description": "el clérigo puede lanzar control water 1/semana."
            }
        ],
        "vestment": "Los Cantores de la Concha visten túnicas en tonos azules y verdes, adornadas con conchas y perlas. Portan como símbolo sagrado una concha grande colgada al cuello o en el cinturón.",
        "organization": "La iglesia de Elineth es sencilla y comunitaria. Cada aldea pesquera cuenta con un cantor o pequeña hermandad que dirige oraciones y ofrendas al mar. Los clérigos viajan con frecuencia entre pueblos costeros para mantener lazos de fraternidad.",
        "rituals": "El Canto de las Mareas: ceremonia diaria al amanecer y atardecer, donde se entonan himnos al ritmo de las olas. La Vigilia Lunar: rito mensual durante la luna llena, donde se encienden antorchas en la playa y se ofrecen conchas al mar. El Banquete del Mar: fiesta anual tras la primera gran pesca de primavera, en la que toda la comunidad comparte el alimento.",
        "allies_enemies": "Aliados: Tharion (mar y tormentas), Ydran (ríos y viajes) y Aelhar (ciclos de fertilidad). Oponentes: Selkar, pues la traición y la oscuridad quiebran la serenidad de las mareas. Relación ambivalente: Issarel, cuyos terremotos pueden alterar violentamente los mares.",
        "dogma": "El culto de Elineth enseña que la vida fluye en ciclos como las mareas: calma y tormenta, abundancia y escasez. La paciencia, la confianza en el ciclo y la unión comunitaria son virtudes sagradas. Se condena la avaricia y la sobrepesca, pues perturban el equilibrio del mar.",
        "stronghold": "Los sacerdotes de Elineth, al alcanzar nivel 9, pueden fundar un Santuario de la Concha, generalmente en cabos o islas costeras. Estos santuarios sirven como faros espirituales para marineros y pescadores, ofreciendo refugio, bendiciones y guía en la navegación.",
        "campaign_link": "Señora de las mareas apacibles y la pesca costera. Sus cánticos de caracolas son la plegaria diaria de los pueblos pesqueros que rodean las costas.",
        "icon": "🐚"
    },
    {
        "id": "issarel",
        "name": "Issarel",
        "title": "Quebradora de Piedra",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Diosa Menor",
        "plane": "Limbo",
        "alignment": "CN",
        "alignment_name": "Caótico Neutral",
        "portfolio": [
            "Terremotos",
            "Cambio brusco",
            "Ruptura",
            "Reconstrucción."
        ],
        "symbol": "Piedra agrietada en dos mitades.",
        "worshippers": "Mineros, albañiles, pueblos montañeses, tribus bárbaras que veneran la fuerza de la tierra y quienes aceptan el caos como parte del ciclo de destrucción y renovación. Sus fieles creen que de la ruptura surge siempre una nueva forma.",
        "cleric_order": "Quebradores de Piedra",
        "cleric_requirements": "Sabiduría 12+, Fuerza 12.",
        "cleric_alignment": "CN, N, CB.",
        "weapons": "Martillo de guerra, maza, garrote, honda.",
        "armor": "Hasta cota de mallas; escudos permitidos. Esferas mayores (7): All, Elemental (Earth), Combat, Protection, Guardian, Healing, Weather. Esferas menores (6): Creation, Divination, Sun, Travelers, Necromantic, Wards. Poderes concedidos: • Nivel 1 – Golpe Telúrico: el clérigo puede lanzar shatter 1/día. • Nivel 7 – Piel de Piedra: el clérigo puede lanzar stoneskin 1/semana. • Nivel 9 – Furia del Terremoto: el clérigo puede lanzar earthquake 1/semana. Vestimenta clerical: Los Quebradores de Piedra visten túnicas en tonos marrones y grises, adornadas con fragmentos de roca y minerales. Suelen portar martillos de cantera como símbolo de su fe. ORGANIZACIÓN CLERICAL La iglesia de Issarel es descentralizada y caótica. Los clérigos se agrupan en pequeñas hermandades que aparecen y desaparecen como grietas en la tierra. Los más veteranos son llamados Eco de la Montaña. FIESTAS Y RITUALES • El Día de la Ruptura: ceremonia anual donde se quiebran piedras como ofrenda a Issarel. • El Ritual del Derrumbe: rito de iniciación en el que un aprendiz sobrevive a un derrumbe controlado de rocas. • La Vigilia de la Montaña: celebración en que los fieles meditan en silencio en lo alto de montañas o colinas. ALIADOS Y ENEMIGOS DIVINOS Aliados: Tharion (tormentas) y Drelk (niebla y olvido), pues el cambio es común a los tres. Oponentes: Dalmar (umbrales y ley), que busca preservar lo que Issarel rompe. Relación ambivalente: Aelhar, pues la ruptura destruye la fertilidad, pero también prepara nuevos ciclos. DOGMA Y CULTO El culto de Issarel enseña que la ruptura es necesaria para la renovación. Nada permanece para siempre: la tierra tiembla, la piedra se rompe y de las ruinas surge lo nuevo. Sus fieles celebran la destrucción como preludio de la creación. SEGUIDORES Y FORTALEZAS Los sacerdotes de Issarel, al alcanzar nivel 9, pueden fundar un Santuario de la Grieta, en montañas, cañones o fallas sísmicas. Estos lugares sirven como recordatorio de que todo se rompe y todo renace.",
        "magic_items": "",
        "spheres_major": [],
        "spheres_minor": [],
        "powers_granted": [
            {
                "level": 1,
                "name": "Golpe Telúrico",
                "description": "el clérigo puede lanzar shatter 1/día."
            },
            {
                "level": 7,
                "name": "Piel de Piedra",
                "description": "el clérigo puede lanzar stoneskin 1/semana."
            },
            {
                "level": 9,
                "name": "Furia del Terremoto",
                "description": "el clérigo puede lanzar earthquake 1/semana."
            }
        ],
        "vestment": "Los Quebradores de Piedra visten túnicas en tonos marrones y grises, adornadas con fragmentos de roca y minerales. Suelen portar martillos de cantera como símbolo de su fe.",
        "organization": "La iglesia de Issarel es descentralizada y caótica. Los clérigos se agrupan en pequeñas hermandades que aparecen y desaparecen como grietas en la tierra. Los más veteranos son llamados Eco de la Montaña.",
        "rituals": "• El Día de la Ruptura: ceremonia anual donde se quiebran piedras como ofrenda a Issarel. • El Ritual del Derrumbe: rito de iniciación en el que un aprendiz sobrevive a un derrumbe controlado de rocas. • La Vigilia de la Montaña: celebración en que los fieles meditan en silencio en lo alto de montañas o colinas.",
        "allies_enemies": "Aliados: Tharion (tormentas) y Drelk (niebla y olvido), pues el cambio es común a los tres. Oponentes: Dalmar (umbrales y ley), que busca preservar lo que Issarel rompe. Relación ambivalente: Aelhar, pues la ruptura destruye la fertilidad, pero también prepara nuevos ciclos.",
        "dogma": "El culto de Issarel enseña que la ruptura es necesaria para la renovación. Nada permanece para siempre: la tierra tiembla, la piedra se rompe y de las ruinas surge lo nuevo. Sus fieles celebran la destrucción como preludio de la creación.",
        "stronghold": "Los sacerdotes de Issarel, al alcanzar nivel 9, pueden fundar un Santuario de la Grieta, en montañas, cañones o fallas sísmicas. Estos lugares sirven como recordatorio de que todo se rompe y todo renace.",
        "campaign_link": "Quebradora de piedra y deidad de los seísmos en Limbo. Enseña que de la ruina y la fractura nace siempre una nueva oportunidad de creación.",
        "icon": "⚡"
    },
    {
        "id": "kelvar",
        "name": "Kelvar",
        "title": "Señor del Río Negro",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Menor",
        "plane": "la Concordancia",
        "alignment": "N",
        "alignment_name": "Neutral Auténtico",
        "portfolio": [
            "Muerte natural",
            "Ancestros",
            "Tránsito al más allá",
            "Ciclo vital."
        ],
        "symbol": "Un río negro que fluye en espiral hacia abajo.",
        "worshippers": "Ancianos, sabios, comunidades tribales que honran a sus muertos, guardianes de tumbas y quienes buscan aceptar la muerte como parte de la vida. Sus fieles no ven a Kelvar como destructor, sino como guía del último viaje. Sus santuarios suelen estar cerca de ríos, cementerios o cuevas profundas.",
        "cleric_order": "Hijos del Río Negro",
        "cleric_requirements": "Sabiduría 12, Constitución 12",
        "cleric_alignment": "N, NB, NM.",
        "weapons": "Bastón, maza, hoz, lanza.",
        "armor": "Hasta cota de mallas; escudos permitidos.",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Necromantic",
            "Healing",
            "Divination",
            "Guardian",
            "Protection",
            "Thought."
        ],
        "spheres_minor": [
            "Combat",
            "Creation",
            "Elemental (Water)",
            "Sun",
            "Travelers",
            "Wards."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Don del Paso Sereno",
                "description": "el clérigo puede lanzar calm emotions 1/día."
            },
            {
                "level": 5,
                "name": "Tacto del Ancestro",
                "description": "el clérigo puede lanzar speak with dead 1/semana."
            },
            {
                "level": 9,
                "name": "Llamado del Río Negro",
                "description": "el clérigo puede lanzar raise dead 1/semana, pero únicamente sobre quienes murieron de causas naturales o en combate honorable."
            }
        ],
        "vestment": "Los Hijos del Río Negro llevan túnicas negras y grises con ribetes azules, y suelen pintarse el rostro con franjas oscuras. Portan bastones decorados con huesos o piedras de río como símbolos sagrados.",
        "organization": "La iglesia de Kelvar es silenciosa y solemne. Los clérigos forman linajes de guardianes de tumbas y guías espirituales. Los más veteranos reciben el título de Custodios del Río.",
        "rituals": "• El Paso del Río: rito funerario en el que se dejan barcas con ofrendas en un río cercano. • La Noche de los Ancestros: festival anual donde se encienden antorchas en memoria de los muertos. • El Silencio del Alba: vigilia mensual de oración en silencio, recordando a los que partieron.",
        "allies_enemies": "Aliados: Aelhar (ciclos), Drelk (olvido y transición), Bereth (protección natural). Oponentes: Selkar, pues su traición rompe el ciclo natural de la muerte. Relación ambivalente: Liryel, cuyo misterio a veces inspira, pero también confunde el camino al más allá.",
        "dogma": "El culto de Kelvar enseña que la muerte es parte del ciclo vital, y debe ser aceptada sin temor. Los ancestros guían a los vivos, y honrar su memoria fortalece a la comunidad. Resucitar a los muertos es un acto sagrado que solo debe hacerse en armonía con el ciclo natural.",
        "stronghold": "Los sacerdotes de Kelvar, al alcanzar nivel 9, pueden fundar una Casa del Río Negro, santuario junto a ríos o cementerios. Allí custodian tumbas, guían funerales y mantienen la memoria de los ancestros. Estos lugares atraen a sabios, ancianos y guardianes.",
        "campaign_link": "Guardián de la muerte natural y barquero de las almas por el Río Negro. Venerado con respeto sereno en los ritos funerarios tradicionales.",
        "icon": "🛶"
    },
    {
        "id": "ydran",
        "name": "Ydran",
        "title": "Señor de los Ríos",
        "pantheon": "Lyndoria",
        "pantheon_title": "Panteón Lyndoriano (Antiguos Dioses)",
        "rank": "Dios Menor",
        "plane": "la Concordancia",
        "alignment": "N",
        "alignment_name": "Neutral Auténtico",
        "portfolio": [
            "Ríos",
            "Viajes",
            "Comercio fluvial",
            "Tránsito y movimiento."
        ],
        "symbol": "Onda doble en forma de corriente.",
        "worshippers": "Barqueros, comerciantes fluviales, viajeros, exploradores y pueblos asentados en riberas. Se lo invoca en cada travesía, tanto en ríos como en caminos, para pedir paso seguro. Sus templos suelen levantarse en puentes, encrucijadas y vados de río.",
        "cleric_order": "Hermanos del Río",
        "cleric_requirements": "Sabiduría 12, Destreza 12.",
        "cleric_alignment": "N, NB, CN.",
        "weapons": "Lanza, jabalina, tridente, espada corta, daga.",
        "armor": "Hasta cota de mallas; escudos permitidos.",
        "magic_items": "",
        "spheres_major": [
            "All",
            "Travelers",
            "Elemental (Water)",
            "Divination",
            "Protection",
            "Healing",
            "Guardian."
        ],
        "spheres_minor": [
            "Creation",
            "Weather",
            "Sun",
            "Plant",
            "Combat",
            "Charm."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Don del Río",
                "description": "el clérigo puede lanzar create water 1/día."
            },
            {
                "level": 5,
                "name": "Paso Seguro",
                "description": "el clérigo puede lanzar water walk 1/día."
            },
            {
                "level": 9,
                "name": "Salto del Viajero",
                "description": "el clérigo puede lanzar dimension door 1/día."
            }
        ],
        "vestment": "Los Hermanos del Río visten túnicas azules y blancas, adornadas con ondas y nudos fluviales. Portan bastones con símbolos de corrientes y suelen llevar conchas o piedras pulidas por el agua como amuletos.",
        "organization": "El culto de Ydran está organizado en hermandades itinerantes que viajan de puerto en puerto y de puente en puente. Carecen de jerarquías rígidas; los más experimentados reciben el título de Guías de Corriente.",
        "rituals": "• El Cruce Seguro: rito en el que se bendicen barcas, carros y viajeros antes de partir. • La Ofrenda al Río: ceremonia mensual en la que se arrojan flores o monedas a la corriente en agradecimiento. • La Fiesta de las Corrientes: celebración anual en primavera, cuando los ríos se deshielan y reanudan el comercio.",
        "allies_enemies": "Aliados: Elineth (mareas), Aelhar (fertilidad de la tierra) y Bereth (protección natural). Oponentes: Selkar, cuya traición rompe los pactos de tránsito. Relación ambivalente: Tharion, cuyo poder en tormentas puede ser tanto aliado como obstáculo en los viajes.",
        "dogma": "El culto de Ydran enseña que todo viaje es un río, y que el movimiento es sagrado. Ayudar al viajero y proteger el comercio justo son deberes de sus fieles. Detener el curso del río —sea físico o espiritual— es una ofensa.",
        "stronghold": "Los sacerdotes de Ydran, al alcanzar nivel 9, pueden fundar una Casa del Río, santuario en puentes, vados o encrucijadas. Estos templos ofrecen hospitalidad a viajeros y actúan como centros de intercambio y bendición de rutas.",
        "campaign_link": "Señor de las corrientes fluviales y los vados. Patrón de barqueros, viajeros y buscadores de conocimiento a través de los caminos del agua.",
        "icon": "🐟"
    },
    {
        "id": "amaterasu",
        "name": "Amaterasu",
        "title": "la Soberana Solar",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Diosa Mayor",
        "plane": "Monte Celestia",
        "alignment": "LB",
        "alignment_name": "Legal Bueno",
        "portfolio": [
            "Sol",
            "Luz",
            "Nobleza",
            "Autoridad",
            "Fertilidad",
            "Agricultura."
        ],
        "symbol": "Disco solar dorado con ocho rayos.",
        "worshippers": "Amaterasu es el pilar espiritual y político de Amatsukuni. Sus devotos abarcan desde campesinos que oran por buenas cosechas hasta nobles que reconocen en ella la fuente de su legitimidad. Sus templos son los más grandes y refinados del Imperio, centros de justicia, cultura y celebración. Disco solar dorado con ocho rayos Hijos de la Luz (Hikari no Ko) Laúd dorado sobre olas Canción de las Olas (Namiuta) Yelmo dorado o espadas cruzadas Escudos de la Justicia (Seigi no Tate) Racimo de arroz con zorro blanco Pueblo del Zorro Blanco (Byakko no Tami) Círculo yin/yang con loto y rama seca Guías de los Espíritus (Shiryō no Michibiki) Llama estilizada en rojo y dorado Antorchas del Fuego Eterno (Enka no Tomoshibi) Tambor atravesado por un rayo Tambores del Trueno (Ikazuchi no Taiko) Círculo púrpura con llama estilizada Llama Púrpura (Murasaki no Hi) Torbellino azul o espada con rayos Hijos del Viento (Kaze no Ko) Media luna plateada sobre fondo oscuro Sueños de la Noche Lunar (Tsukiyo no Yume)",
        "cleric_order": "Hijos de la Luz (Hikari no Ko)",
        "cleric_requirements": "Sabiduría 16, Carisma 15.",
        "cleric_alignment": "LB, NB.",
        "weapons": "Espada larga, naginata, arco largo, bastón.",
        "armor": "Todas las armaduras y escudos.",
        "magic_items": "Cualquier objeto permitido a clérigos.",
        "spheres_major": [
            "All",
            "Sun",
            "Law",
            "Healing",
            "Protection",
            "Guardian",
            "Creation",
            "Divination",
            "Charm",
            "Wards",
            "Combat."
        ],
        "spheres_minor": [
            "Weather",
            "Thought",
            "Numbers",
            "Time",
            "Plant",
            "Elemental (Fire)",
            "Astral",
            "Travelers."
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Luz de Amaterasu",
                "description": "puede lanzar light 1/día."
            },
            {
                "level": 5,
                "name": "Bendición del Sol",
                "description": "puede lanzar prayer 1/día."
            },
            {
                "level": 9,
                "name": "Aura Radiante",
                "description": "puede lanzar sunray 1/ semana."
            }
        ],
        "vestment": "Los Hijos de la Luz visten túnicas blancas bordadas en oro. Portan espejos pulidos como símbolos de la diosa, y durante ceremonias llevan tocados solares con ocho rayos.",
        "organization": "El clero de Amaterasu es jerárquico y centralizado. Sus templos principales se hallan en las capitales, donde la Suma Sacerdotisa actúa como portavoz de la diosa y consejera del Emperador.",
        "rituals": "• Festival del Sol Naciente: celebrado cada primavera, marca el inicio del ciclo agrícola. • Ceremonia del Espejo: rito donde los nuevos nobles y herederos presentan su legitimidad ante la diosa. • La Vigilia Dorada: oración diaria al amanecer con cantos y espejos ofrecidos al sol.",
        "allies_enemies": "Aliados: Tsukiyomi (ciclos lunares), Hachiman (protección y deber), Inari (fertilidad). Oponentes: deidades del caos destructivo sin propósito. Relación ambivalente: Susano-o, su hermano rebelde, cuya furia pone a prueba la luz de Amaterasu.",
        "dogma": "La enseñanza central de Amaterasu es que la luz es fuente de justicia, fertilidad y autoridad. Gobernar es reflejar la luz divina, y el pueblo debe honrar la armonía y el orden cósmico. La belleza, la pureza y la rectitud son virtudes sagradas en sus ceremonias y templos.",
        "stronghold": "Los sacerdotes de Amaterasu, al alcanzar nivel 9, pueden fundar un Templo Solar Imperial, que actúa tanto como santuario religioso como tribunal de justicia y centro de enseñanza.",
        "campaign_link": "Soberana del Sol y cúspide de la Corte Celestial en Amatsukuni. Símbolo del orden cósmico, la nobleza y la justicia suprema para los kunitas.",
        "icon": "☀️"
    },
    {
        "id": "benzaiten",
        "name": "Benzaiten",
        "title": "la Musa Celestial",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Diosa Menor",
        "plane": "Arborea",
        "alignment": "CB",
        "alignment_name": "Caótico Bueno",
        "portfolio": [
            "Magia",
            "Artes",
            "Música",
            "Belleza",
            "Fortuna"
        ],
        "symbol": "Un laúd dorado sobre olas",
        "worshippers": "Benzaiten es venerada por músicos, poetas, bailarines y artistas, así como por viajeros y quienes buscan la buena fortuna. Sus fieles ven en ella la encarnación de la belleza y la musa que inspira las obras mortales.",
        "cleric_order": "Cantores de las Olas (Namiuta)",
        "cleric_requirements": "Sabiduría 13, Carisma 15",
        "cleric_alignment": "CB, NB",
        "weapons": "Daga, bastón, arco corto, wakizashi",
        "armor": "Cuero o acolchada, sin metal ni escudos",
        "magic_items": "Objetos clericales, además de instrumentos encantados, varas y pergaminos arcanos Esferas mayores (9): All, Charm, Creation, Divination, Healing, Protection, Thought, Numbers, Travelers Esferas menores (7): Sun, Weather, Wards, Astral, Guardian, Plant, Elemental (Water) Poderes concedidos: • Nivel 3 Canto Fascinante: puede lanzar Enthrall 1/día • Nivel 7 Melodía Sanadora: Puede lanzar Song of Healing 1/día • Nivel 9 Sinfonía Radiante: Puede lanzar Brightsong 1/semana Vestimenta clerical: Los sacerdotes de Benzaiten visten túnicas coloridas decoradas con motivos acuáticos y florales. Los instrumentos musicales forman parte de su atuendo ceremonial y se utilizan tanto en los rituales como en los combates ceremoniales. ORGANIZACIÓN CLERICAL El culto de Benzaiten es libre y descentralizado, reflejo de la creatividad de la diosa. Sus templos suelen ser teatros, casas de música o jardines donde se celebran tanto la devoción como la belleza. Los sacerdotes actúan como artistas y guías espirituales más que como jerarcas. FIESTAS Y RITUALES • Festival de la Música Celestial: celebrado al inicio del verano con conciertos, danzas y recitales poéticos. • Rito de la Fuente Sonora: los fieles sumergen sus instrumentos en aguas sagradas para bendecirlos y otorgarles armonía. ALIADOS Y ENEMIGOS DIVINOS Aliados: Amaterasu (armonía y fertilidad), Inari (prosperidad). Enemigos: deidades de la corrupción o el silencio impuesto. Relación ambivalente: Shien, cuya solemnidad ritual contrasta con el gozo desenfadado de Benzaiten. DOGMA Y CULTO Benzaiten enseña que la magia y el arte son expresiones divinas, y que la música, la poesía y la danza embellecen la vida. La fortuna favorece a los audaces y a quienes transforman la existencia en un espectáculo digno de los dioses. SEGUIDORES Y FORTALEZAS Los sacerdotes de Benzaiten, al alcanzar nivel 9, pueden fundar un Templo del Laúd Dorado, que actúa como santuario, escuela de artes y lugar de peregrinación para músicos y viajeros.",
        "spheres_major": [],
        "spheres_minor": [],
        "powers_granted": [
            {
                "level": 3,
                "name": "Canto Fascinante",
                "description": "puede lanzar Enthrall 1/día"
            },
            {
                "level": 7,
                "name": "Melodía Sanadora",
                "description": "Puede lanzar Song of Healing 1/día"
            },
            {
                "level": 9,
                "name": "Sinfonía Radiante",
                "description": "Puede lanzar Brightsong 1/semana"
            }
        ],
        "vestment": "Los sacerdotes de Benzaiten visten túnicas coloridas decoradas con motivos acuáticos y florales. Los instrumentos musicales forman parte de su atuendo ceremonial y se utilizan tanto en los rituales como en los combates ceremoniales.",
        "organization": "El culto de Benzaiten es libre y descentralizado, reflejo de la creatividad de la diosa. Sus templos suelen ser teatros, casas de música o jardines donde se celebran tanto la devoción como la belleza. Los sacerdotes actúan como artistas y guías espirituales más que como jerarcas.",
        "rituals": "• Festival de la Música Celestial: celebrado al inicio del verano con conciertos, danzas y recitales poéticos. • Rito de la Fuente Sonora: los fieles sumergen sus instrumentos en aguas sagradas para bendecirlos y otorgarles armonía.",
        "allies_enemies": "Aliados: Amaterasu (armonía y fertilidad), Inari (prosperidad). Enemigos: deidades de la corrupción o el silencio impuesto. Relación ambivalente: Shien, cuya solemnidad ritual contrasta con el gozo desenfadado de Benzaiten.",
        "dogma": "Benzaiten enseña que la magia y el arte son expresiones divinas, y que la música, la poesía y la danza embellecen la vida. La fortuna favorece a los audaces y a quienes transforman la existencia en un espectáculo digno de los dioses.",
        "stronghold": "Los sacerdotes de Benzaiten, al alcanzar nivel 9, pueden fundar un Templo del Laúd Dorado, que actúa como santuario, escuela de artes y lugar de peregrinación para músicos y viajeros.",
        "campaign_link": "Musa de las artes, la música, la magia y la fortuna. Sus templos costeros albergan poetas, actrices y eruditos que buscan inspiración pura.",
        "icon": "🪕"
    },
    {
        "id": "hachiman",
        "name": "Hachiman",
        "title": "el Guardián Marcial",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Dios Menor",
        "plane": "Bytopia",
        "alignment": "LB",
        "alignment_name": "Legal Bueno",
        "portfolio": [
            "Guerra",
            "Protección",
            "Deber",
            "Honor",
            "Justicia marcial"
        ],
        "symbol": "Un yelmo dorado o dos espadas cruzadas",
        "worshippers": "Hachiman es adorado por soldados, oficiales, jueces de guerra y campesinos que toman las armas en defensa de sus tierras. También es patrón de los clanes que basan su prestigio en la disciplina y el honor marcial. DOGMA Y CULTO Hachiman enseña que la guerra debe librarse en defensa del pueblo y del orden, nunca por ambición o crueldad. El deber, el honor y la justicia deben guiar al guerrero en cada batalla. Proteger al inocente es la forma más alta de valor. SEGUIDORES Y FORTALEZAS Los sacerdotes de Hachiman, al alcanzar nivel 9, pueden fundar un Santuario Marcial, que funciona como templo, fortaleza defensiva y escuela de guerra para el pueblo y los clanes aliados. Inari, Guardiana de la Abundancia Diosa Menor de las Beastlands (nb)",
        "cleric_order": "Escudos de la Justicia (Seigi no Tate)",
        "cleric_requirements": "Sabiduría 13, Fuerza 13, Constitución 12",
        "cleric_alignment": "LB, NB, LN",
        "weapons": "Espada larga, arco, naginata, lanza, yari",
        "armor": "Todas las armaduras y escudos",
        "magic_items": "Objetos clericales y armas mágicas de tipo militar",
        "spheres_major": [
            "All",
            "Combat",
            "Healing",
            "Law",
            "Protection",
            "Guardian",
            "War",
            "Divination"
        ],
        "spheres_minor": [
            "Sun",
            "Creation",
            "Wards",
            "Thought",
            "Numbers",
            "Travelers"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Juramento de Honor",
                "description": "Bless 1/día"
            },
            {
                "level": 5,
                "name": "Espíritu Marcial",
                "description": "Spiritual Weapon 1/día"
            },
            {
                "level": 9,
                "name": "Furia del Guardián",
                "description": "Holy Word 1/semana"
            }
        ],
        "vestment": "Los sacerdotes de Hachiman visten armaduras ceremoniales, adornadas con emblemas dorados del clan y del dios. En las ceremonias suelen portar espadas en saya lacadas en negro y rojo, símbolos de su compromiso con la guerra justa.",
        "organization": "El clero de Hachiman es jerárquico y disciplinado, similar a una orden militar. Los templos funcionan también como cuarteles y academias de instrucción, donde se entrenan tanto soldados profesionales como milicias campesinas.",
        "rituals": "• Rito del Juramento de Espadas: los iniciados juran lealtad al clan y al dios, tocando las espadas cruzadas. • Festival de la Victoria Justa: celebrado tras una gran victoria defensiva, con ofrendas de armas y armaduras a los templos.",
        "allies_enemies": "Aliados: Amaterasu (autoridad y nobleza), Inari (prosperidad del pueblo), Tsukiyomi (sabiduría en los ciclos). Enemigos: deidades del caos y la violencia indiscriminada. Relación ambivalente: Susano-o, cuya furia guerrera contradice la disciplina de Hachiman.",
        "dogma": "Hachiman enseña que la guerra debe librarse en defensa del pueblo y del orden, nunca por ambición o crueldad. El deber, el honor y la justicia deben guiar al guerrero en cada batalla. Proteger al inocente es la forma más alta de valor.",
        "stronghold": "Los sacerdotes de Hachiman, al alcanzar nivel 9, pueden fundar un Santuario Marcial, que funciona como templo, fortaleza defensiva y escuela de guerra para el pueblo y los clanes aliados.",
        "campaign_link": "Dios de la guerra defensiva, el honor y el deber marcial. Modelo espiritual de los bushi y guerreros kunitas; enseña a luchar solo por protección.",
        "icon": "🛡️"
    },
    {
        "id": "inari",
        "name": "Inari",
        "title": "Guardiana de la Abundancia",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Diosa Menor",
        "plane": "las Beastlands",
        "alignment": "NB",
        "alignment_name": "Neutral Bueno",
        "portfolio": [
            "Fertilidad",
            "Cosecha",
            "Prosperidad",
            "Zorros tutelares"
        ],
        "symbol": "Un racimo de arroz acompañado por un zorro blanco",
        "worshippers": "Inari es venerada por campesinos, comerciantes y familias que buscan prosperidad. También le rinden culto los mercaderes ambulantes y las comunidades rurales que dependen de la fertilidad de la tierra. Los zorros blancos, considerados sus mensajeros, son protegidos en sus templos.",
        "cleric_order": "Pueblo del Zorro Blanco (Byakko no Tami)",
        "cleric_requirements": "Sabiduría 14, Carisma 13, Constitución 12",
        "cleric_alignment": "NB, N, CB",
        "weapons": "Arco corto, naginata, daga, bastón",
        "armor": "Hasta cota de malla; no se permiten armaduras completas",
        "magic_items": "Objetos clericales,",
        "spheres_major": [
            "All",
            "Charm",
            "Creation",
            "Healing",
            "Plant",
            "Protection",
            "Guardian",
            "Animal"
        ],
        "spheres_minor": [
            "Sun",
            "Divination",
            "Weather",
            "Elemental (Earth)",
            "Travelers",
            "Wards"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Susurro del Zorro",
                "description": "Animal Friendship 1/día"
            },
            {
                "level": 5,
                "name": "Don de la Cosecha",
                "description": "Create Food and Water 1/día"
            },
            {
                "level": 9,
                "name": "Bendición de la Abundancia",
                "description": "Heroes’ Feast 1/ semana"
            }
        ],
        "vestment": "Los sacerdotes de Inari visten ropajes blancos y rojos, adornados con motivos de espigas de arroz. En los rituales portan máscaras o tocados con forma de zorro blanco.",
        "organization": "El culto es comunitario y descentralizado. Los templos de Inari suelen estar situados junto a campos de cultivo o en las aldeas rurales. Sus sacerdotes cumplen también la función de jueces locales y mediadores de disputas.",
        "rituals": "• Festival de la Primera Siembra: celebrado al inicio de la primavera, con danzas y ofrendas de arroz. • Rito del Zorro Blanco: los fieles dejan ofrendas de comida a los zorros tutelares, considerados encarnaciones de la diosa.",
        "allies_enemies": "Aliados: Amaterasu (fertilidad y luz), Benzaiten (prosperidad y fortuna). Enemigos: deidades de la escasez, la corrupción y la codicia. Relación ambivalente: Susano-o, cuya furia marina arruina a menudo las cosechas y el comercio.",
        "dogma": "Inari enseña que la abundancia es fruto tanto del esfuerzo humano como de la bendición divina. Compartir la prosperidad y proteger a los más débiles son deberes sagrados. Los zorros, como mensajeros de la diosa, deben ser respetados y jamás dañados.",
        "stronghold": "Los sacerdotes de",
        "campaign_link": "Guardiana de la fertilidad, los arrozales y los zorros blancos mensajeros. Su culto es el más querido y cercano para las gentes comunes y mercaderes.",
        "icon": "🦊"
    },
    {
        "id": "izanagi_izanami",
        "name": "Izanagi e Izanami",
        "title": "Progenitores Eternos",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Dioses Mayores",
        "plane": "la Concordancia",
        "alignment": "N",
        "alignment_name": "Neutral Auténtico",
        "portfolio": [
            "Creación",
            "Nacimiento",
            "Muerte",
            "Transición"
        ],
        "symbol": "Un círculo yin/yang adornado con un loto y una rama seca",
        "worshippers": "Izanagi e Izanami son los dioses primordiales del pueblo kunita. Se les honra en los ritos de paso más importantes: nacimiento, matrimonio y muerte. Sus cultos están extendidos en todo Amatsukuni, y son seguidos por familias enteras, comadronas, ancianos y comunidades que buscan la armonía entre la vida y la muerte.",
        "cleric_order": "Guías de los Espíritus (Shiryō no Michibiki)",
        "cleric_requirements": "Sabiduría 13, Constitución 12",
        "cleric_alignment": "N, NB, NM",
        "weapons": "Bastón, naginata, arco corto, cuchillo ritual",
        "armor": "Hasta cota de malla; no se permiten armaduras pesadas",
        "magic_items": "Objetos clericales y reliquias funerarias",
        "spheres_major": [
            "All",
            "Creation",
            "Healing",
            "Protection",
            "Guardian",
            "Divination",
            "Necromantic",
            "Law",
            "Time"
        ],
        "spheres_minor": [
            "Sun",
            "Plant",
            "Thought",
            "Wards",
            "Astral",
            "Travelers",
            "Weather"
        ],
        "powers_granted": [
            {
                "level": 3,
                "name": "Toque Bimorfo",
                "description": "Cure Disease o Cause Disease (según aspecto de vida o muerte) 1/semana"
            },
            {
                "level": 7,
                "name": "Voz de los Ancestros",
                "description": "Speak with Dead 1/ semana"
            },
            {
                "level": 10,
                "name": "Juicio de los Progenitores",
                "description": "Raise Dead o Slay Living (según aspecto) 1/mes"
            }
        ],
        "vestment": "Los sacerdotes de Izanagi e Izanami visten túnicas blancas con franjas negras o grises, simbolizando el equilibrio entre la vida y la muerte. En los funerales suelen portar máscaras que evocan la serenidad de los antepasados.",
        "organization": "El culto está dividido en dos órdenes complementarias: Orden de Izanagi: encargada de los ritos de nacimiento, fertilidad y renovación. Orden de Izanami: guardiana de los funerales, las transiciones y la memoria de los muertos. Aunque trabajan en ámbitos distintos, ambas órdenes están unidas en la devoción común a los Progenitores.",
        "rituals": "• Ceremonia de los Tres Ciclos: ritos de paso en nacimiento, matrimonio y muerte. • Festival del Retorno al Polvo: celebrado en otoño, honra a los ancestros con procesiones de lámparas y ofrendas de arroz y flores.",
        "allies_enemies": "Aliados: Shien (purificación y orden), Amaterasu (fertilidad y nobleza). Enemigos: deidades que alteran el ciclo de la vida de forma antinatural. Relación ambivalente: Kagutsuchi, cuya destrucción rompe el ciclo armónico que los progenitores protegen.",
        "dogma": "Izanagi e Izanami enseñan que la vida y la muerte son dos caras de un mismo ciclo. Cada nacimiento y cada muerte deben ser aceptados con respeto y solemnidad. El culto exige honrar a los antepasados, aceptar la mortalidad y transmitir la vida con responsabilidad.",
        "stronghold": "Los sacerdotes de Izanagi e Izanami, al alcanzar nivel 9, pueden fundar un Templo de los Tres Ciclos, donde se celebran los ritos de paso y se guarda el equilibrio entre nacimiento y muerte en la comunidad.",
        "campaign_link": "Progenitores primordiales del universo kunita. Rigen el nacimiento, el matrimonio y el tránsito final al más allá, manteniendo el equilibrio del cosmos.",
        "icon": "☯️"
    },
    {
        "id": "kagutsuchi",
        "name": "Kagutsuchi",
        "title": "el Fuego Renaciente",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Dios Mayor",
        "plane": "Limbo",
        "alignment": "CN",
        "alignment_name": "Caótico Neutral",
        "portfolio": [
            "Fuego",
            "Destrucción",
            "Purificación",
            "Pasión",
            "Renovación"
        ],
        "symbol": "Una llama estilizada en rojo y dorado",
        "worshippers": "Kagutsuchi es venerado por herreros, guerreros, exorcistas y todos aquellos que creen en el poder del fuego para destruir y purificar. Los cultos rurales le ofrecen plegarias durante incendios rituales, mientras que en las ciudades sus templos son visitados por quienes buscan fuerza o catarsis.",
        "cleric_order": "Seguidores del Fuego Eterno (Enka no Tomoshibi)",
        "cleric_requirements": "Sabiduría 14, Constitución 13",
        "cleric_alignment": "CN, CB, N",
        "weapons": "Lanza, naginata, espada corta, bastón, cuchillo ritual",
        "armor": "Hasta cota de malla; no se permiten escudos grandes",
        "magic_items": "Objetos clericales, además de ítems vinculados al fuego o la purificación",
        "spheres_major": [
            "All",
            "Elemental (Fire)",
            "Combat",
            "Healing",
            "Protection",
            "Guardian",
            "Sun",
            "Chaos",
            "Creation"
        ],
        "spheres_minor": [
            "Divination",
            "Weather",
            "Wards",
            "Thought",
            "Travelers",
            "Plant"
        ],
        "powers_granted": [
            {
                "level": 3,
                "name": "Llama Purificadora",
                "description": "Burning Hands 1/día"
            },
            {
                "level": 7,
                "name": "Fuego del Exorcista",
                "description": "Dispel Evil 1/día"
            },
            {
                "level": 10,
                "name": "Incendio Renaciente",
                "description": "Fire Storm 1/ semana"
            }
        ],
        "vestment": "Los sacerdotes de Kagutsuchi usan túnicas rojas y naranjas, a menudo chamuscadas como señal de devoción. Portan antorchas benditas y marcas de ceniza en el rostro durante los rituales.",
        "organization": "El clero es apasionado y descentralizado. Los templos de Kagutsuchi suelen levantarse cerca de volcanes o forjas, y funcionan tanto como lugares de culto como centros de purificación. Los sacerdotes a menudo viajan para realizar exorcismos y ritos de fuego en aldeas alejadas.",
        "rituals": "• Festival de las Llamas Danzantes: celebrado en verano con hogueras, danzas y ofrendas al fuego. • Rito de la Ceniza Nueva: consiste en quemar objetos personales para simbolizar la renovación tras la destrucción.",
        "allies_enemies": "Aliados: Benzaiten (pasión creativa), Susano-o (tormenta y fuerza destructiva). Enemigos: Izanagi e Izanami, cuya armonía cíclica se ve alterada por la violencia del fuego. Relación ambivalente: Amaterasu, cuya luz comparte afinidad con el fuego pero en un marco más ordenado.",
        "dogma": "Kagutsuchi enseña que el fuego destruye, pero también purifica y da paso a la renovación. La pasión y la furia son fuerzas que deben abrazarse, pues en la llama se encuentra la verdad del cambio. Los fieles creen que la vida solo florece tras aceptar la destrucción necesaria.",
        "stronghold": "Los sacerdotes de Kagutsuchi, al alcanzar nivel 9, pueden fundar un Santuario de la Llama Renaciente, que actúa como templo y como lugar de exorcismos y ritos de fuego.",
        "campaign_link": "¡Patrón sagrado de Kazgrim! Señor del fuego primordial, la forja y la renovación. Los Frescos del Sanctum de Kanatsu-mi han revelado su Llama Dorada ascendente: un fuego que nutre la vida, reconstruye tras la ceniza y coexiste en armonía con el agua en la fuente sagrada.",
        "icon": "🔥"
    },
    {
        "id": "raijin",
        "name": "Raijin",
        "title": "el Tambor del Trueno",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Dios Menor",
        "plane": "Ysgard",
        "alignment": "CN",
        "alignment_name": "Caótico Neutral",
        "portfolio": [
            "Trueno",
            "Relámpagos",
            "Destrucción repentina"
        ],
        "symbol": "Un tambor atravesado por un rayo",
        "worshippers": "Raijin es venerado por marineros, guerreros, campesinos que temen las tormentas y músicos de percusión. Su culto mezcla miedo y devoción: se le ofrecen plegarias para desviar los rayos, pero también para invocar su furia contra los enemigos.",
        "cleric_order": "Tambores del Trueno (Ikazuchi no Taiko)",
        "cleric_requirements": "Sabiduría 12, Constitución 13",
        "cleric_alignment": "CN, CB",
        "weapons": "Maza, martillo de guerra, naginata, bastón",
        "armor": "Hasta cota de malla; no se permiten armaduras pesadas",
        "magic_items": "Objetos clericales y tambores encantados",
        "spheres_major": [
            "All",
            "Elemental (Air)",
            "Combat",
            "Chaos",
            "Weather",
            "Protection",
            "Guardian",
            "Sun"
        ],
        "spheres_minor": [
            "Divination",
            "Wards",
            "Healing",
            "Thought",
            "Travelers",
            "Creation"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Retumbar Sagrado",
                "description": "Shattert 1/día"
            },
            {
                "level": 5,
                "name": "Llamada de la Tormenta",
                "description": "Call Lightning 1/día"
            },
            {
                "level": 9,
                "name": "Ira del Cielo",
                "description": "Chain Lightning 1/semana"
            }
        ],
        "vestment": "Los sacerdotes de Raijin visten túnicas negras y rojas, adornadas con símbolos de rayos y nubes. Siempre portan tambores rituales que usan tanto en ceremonias como en combate para invocar al dios.",
        "organization": "El culto es más tribal y disperso que jerárquico. Los templos suelen estar en zonas montañosas o costeras expuestas a tormentas, donde los sacerdotes celebran ritos con estrépito de tambores y fuego.",
        "rituals": "• Festival del Rayo: celebrado en la estación de lluvias, con tambores y danzas bajo la tormenta. • Rito del Tambor Celestial: ceremonia nocturna en la que los tambores imitan los truenos para aplacar o invocar al dios.",
        "allies_enemies": "Aliados: Susano-o (tormenta y mar), Kagutsuchi (fuego y destrucción). Enemigos: Hachiman, cuyo orden militar contrasta con la furia imprevisible del trueno. Relación ambivalente: Amaterasu, a quien Raijin respeta pero cuya luz calma contradice su tempestad.",
        "dogma": "Raijin enseña que el trueno y el rayo son recordatorios de la fuerza indómita del mundo. La destrucción repentina es parte de la vida, y aceptar el caos natural es aceptar la verdad. Sus fieles abrazan la intensidad y el estrépito como parte del ciclo.",
        "stronghold": "Los sacerdotes de Raijin, al alcanzar nivel 9, pueden fundar un Santuario del Trueno, erigido en un lugar montañoso o costero donde las tormentas sean frecuentes, usado para invocar y honrar al dios con estrépito ritual.",
        "campaign_link": "Dios del trueno y el relámpago salvaje. Su estruendo ahuyenta a los malos espíritus y sus tambores marcan el pulso de las tormentas de verano.",
        "icon": "⚡"
    },
    {
        "id": "shien",
        "name": "Shien",
        "title": "la Llama Púrpura",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Diosa Mayor",
        "plane": "Mechanus",
        "alignment": "LN",
        "alignment_name": "Legal Neutral",
        "portfolio": [
            "Magia ordenada",
            "Muerte",
            "Belleza",
            "Purificación"
        ],
        "symbol": "Un círculo con una llama púrpura estilizada en su interior",
        "worshippers": "Shien es adorada por magas, jueces, guardianes de tumbas y todos aquellos que buscan armonizar la magia con el orden. Sus fieles incluyen artistas y sacerdotisas que valoran la belleza como reflejo del orden interno. La veneran también quienes temen la corrupción de la magia y desean mantener su pureza.",
        "cleric_order": "Llamas Custodias (Hi no Mamori / Murasaki no Hi)",
        "cleric_requirements": "Sabiduría 15, Inteligencia 14, Carisma 13",
        "cleric_alignment": "LN",
        "weapons": "Bastón, daga, naginata, arco corto, sai",
        "armor": "Ninguna (ni armaduras ni escudos)",
        "magic_items": "Cualquier objeto permitido a clérigos, más varas, bastones y pergaminos arcanos",
        "spheres_major": [
            "All",
            "Divination",
            "Guardian",
            "Healing",
            "Law",
            "Necromantic",
            "Protection",
            "Sun",
            "Charm",
            "Elemental (Fire)"
        ],
        "spheres_minor": [
            "Creation",
            "Elemental (Water)",
            "Thought",
            "Time",
            "Wards",
            "Numbers",
            "Astral",
            "Combat"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Ojo de la Llama",
                "description": "Detect Magic 1/día"
            },
            {
                "level": 3,
                "name": "Muralla contra la Oscuridad",
                "description": "Protection from Undead 1/día"
            },
            {
                "level": 7,
                "name": "Voz de los Ancestros",
                "description": "Commune con espíritus ancestrales 1/semana"
            }
        ],
        "vestment": "Las sacerdotisas de Shien visten kimonos púrpura bordados en dorado. En las ceremonias funerarias portan máscaras blancas de porcelana que evocan serenidad y belleza inmutable.",
        "organization": "El culto de Shien está fuertemente jerarquizado: Portadores de la Brasa: novicios encargados de tareas rituales menores. Llamas Custodias: sacerdotes encargados de funerales, rituales de purificación y custodia de secretos arcanos. Fulgor Púrpura: sumos sacerdotes que interpretan la voluntad de Shien y dirigen el culto.",
        "rituals": "• Festival de la Llama Eterna (equinoccio de primavera): ritual de purificación de objetos mágicos y grimorios. • Velada de los Mil Pétalos (solsticio de invierno): noche en la que se guían las almas al más allá con lámparas flotantes sobre ríos y estanques.",
        "allies_enemies": "Aliados: Deidades de la ley, la purificación y el equilibrio cósmico. Enemigos: Dioses del caos, la corrupción mágica y aquellos que imponen la no-muerte sin consentimiento.",
        "dogma": "Shien enseña que la magia es una llama sagrada, destinada a iluminar y purificar. La muerte es un tránsito natural, que puede aceptarse o transformarse según la voluntad de cada uno, siempre que sea de manera libre y consciente. La belleza es un reflejo del orden, y todo ritual debe ejecutarse con perfección estética. La no-muerte sólo es aceptable con consentimiento libre y consciente; imponerla es un crimen contra el orden. Los templos y ceremonias deben ser impecables, pues la armonía exterior refleja la interna.",
        "stronghold": "Los sacerdotes de Shien, al alcanzar nivel 9, pueden fundar un Santuario Púrpura, que actúa como templo, centro de estudios mágicos y lugar de ceremonias funerarias y de purificación.",
        "campaign_link": "¡Patrona de Katsumi y de las Llamas Custodias (Hi no Mamori)! Su deliberada y sistemática ausencia en Kanatsu-mi (puerta exterior de obsidiana, estanterías y los Frescos del Sanctum calculados geométricamente para diez dioses) constituye uno de los mayores enigmas teológicos del grupo.",
        "icon": "🔮"
    },
    {
        "id": "susanoo",
        "name": "Susano-o",
        "title": "el Señor de las Tormentas",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Dios Mayor",
        "plane": "Ysgard",
        "alignment": "CN",
        "alignment_name": "Caótico Neutral",
        "portfolio": [
            "Mar",
            "Tormentas",
            "Furia",
            "Destrucción",
            "Valor salvaje"
        ],
        "symbol": "Una ola coronada por un relámpago",
        "worshippers": "Susano-o es venerado por marineros, pescadores, guerreros temerarios y clanes que valoran la fuerza y la independencia por encima de todo. Su culto se encuentra a menudo en regiones costeras y entre comunidades que viven bajo la amenaza constante del mar y de las tormentas.",
        "cleric_order": "Hijos del Viento y las Olas (Kaze no Ko)",
        "cleric_requirements": "Sabiduría 12, Fuerza 13, Constitución 13",
        "cleric_alignment": "CA, CN",
        "weapons": "Espada larga, lanza, naginata, arco, tridente",
        "armor": "Hasta cota de malla; no se permiten armaduras pesadas",
        "magic_items": "Objetos clericales, además de armas vinculadas al mar y al trueno",
        "spheres_major": [
            "All",
            "Combat",
            "Chaos",
            "Weather",
            "Elemental (Water)",
            "Elemental (Air)",
            "Protection",
            "War",
            "Guardian"
        ],
        "spheres_minor": [
            "Divination",
            "Healing",
            "Sun",
            "Wards",
            "Travelers",
            "Creation"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Respiro de las Profundidades",
                "description": "Water Breathing 1/día"
            },
            {
                "level": 5,
                "name": "Furia de la Tormenta",
                "description": "Call Lightning 1/día"
            },
            {
                "level": 9,
                "name": "Señorío del Mar y del Cielo",
                "description": "Control Weather 1/semana"
            }
        ],
        "vestment": "Los sacerdotes de Susano-o visten túnicas azul oscuro y verde marino, adornadas con motivos de olas y rayos. En los rituales portan collares de conchas y llevan consigo tridentes o espadas largas bendecidas.",
        "organization": "El culto es indisciplinado y fragmentado. Cada templo costero funciona de manera independiente, dirigido por sacerdotes que combinan el oficio religioso con el mando de barcos o milicias locales. La jerarquía formal es mínima; prima la fuerza personal y el carisma.",
        "rituals": "• Festival de la Ola de Trueno: celebrado al inicio de la temporada de tormentas con carreras de barcos y danzas en la costa. • Rito del Mar Embravecido: plegarias y ofrendas lanzadas al océano para apaciguar o invocar la furia de Susano-o.",
        "allies_enemies": "Aliados: Raijin (trueno y tormentas), Kagutsuchi (fuego y destrucción). Enemigos: Hachiman, que representa el orden y la disciplina militar. Relación ambivalente: Amaterasu, su hermana, a quien respeta pero con quien rivaliza de forma constante.",
        "dogma": "Susano-o enseña que la vida debe enfrentarse con valor y sin miedo a la destrucción. El mar y la tormenta son fuerzas imparables que deben aceptarse y aprovecharse, no temerse. La furia y la libertad son dones divinos, y quienes los abrazan viven con plenitud.",
        "stronghold": "Los sacerdotes de Susano-o, al alcanzar nivel 9, pueden fundar un Santuario de la Tormenta, erigido en la costa o sobre un acantilado, desde donde ofician ritos y guían a las comunidades marineras bajo la protección del dios.",
        "campaign_link": "Dios de la furia marina, la tormenta indomable y el valor audaz. Rebelde de la Corte Celestial, venerado por quienes desafían el peligro cara a cara.",
        "icon": "🌪️"
    },
    {
        "id": "tsukiyomi",
        "name": "Tsukiyomi",
        "title": "el Guardián de la Luna",
        "pantheon": "Amatsukuni",
        "pantheon_title": "Señores Celestiales de Amatsukuni",
        "rank": "Dios Mayor",
        "plane": "Arbórea",
        "alignment": "NB",
        "alignment_name": "Neutral Bueno",
        "portfolio": [
            "Luna",
            "Ciclos",
            "Noche",
            "Misterio",
            "Contemplación"
        ],
        "symbol": "Un disco plateado con nubes que lo atraviesan",
        "worshippers": "Tsukiyomi es adorado por sabios, astrónomos, poetas y viajeros nocturnos. También lo veneran los campesinos que dependen de los ciclos lunares para sus cosechas y los navegantes que se guían por la luz de la luna.",
        "cleric_order": "Custodios de la Noche (Tsukiyo no Yume)",
        "cleric_requirements": "Sabiduría 14, Inteligencia 12",
        "cleric_alignment": "NB, N",
        "weapons": "Arco, naginata, bastón, daga",
        "armor": "Hasta cota de malla; no se permiten armaduras pesadas",
        "magic_items": "Objetos clericales, además de ítems relacionados con la adivinación o la luz lunar",
        "spheres_major": [
            "All",
            "Divination",
            "Protection",
            "Guardian",
            "Healing",
            "Creation",
            "Sun",
            "Thought",
            "Time"
        ],
        "spheres_minor": [
            "Charm",
            "Wards",
            "Astral",
            "Weather",
            "Travelers",
            "Plant"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Luz de la Medianoche",
                "description": "Faerie Fire 1/día"
            },
            {
                "level": 5,
                "name": "Claridad Lunar",
                "description": "Moonbeam 1/día"
            },
            {
                "level": 9,
                "name": "Espejo de la Noche",
                "description": "True Seeing 1/semana"
            }
        ],
        "vestment": "Los sacerdotes de Tsukiyomi visten túnicas blancas y plateadas, adornadas con símbolos de lunas crecientes y llenas. Llevan tiaras o tocados con discos de plata que reflejan la luz nocturna.",
        "organization": "El culto es contemplativo y descentralizado. Sus templos suelen levantarse en colinas, montañas o lugares desde los que la luna pueda observarse con claridad. Los sacerdotes son consejeros y guardianes de los ciclos naturales.",
        "rituals": "• Festival de la Luna Llena: celebrado cada mes con vigilias y plegarias nocturnas bajo la luz lunar. • Rito del Espejo Plateado: ceremonia de adivinación con agua iluminada por la luna.",
        "allies_enemies": "Aliados: Amaterasu (su hermana, de la que es complemento), Inari (fertilidad ligada a los ciclos). Enemigos: deidades del caos y la oscuridad corruptora. Relación ambivalente: Susano-o, cuya furia rompe la serenidad lunar.",
        "dogma": "Tsukiyomi enseña que todo en el mundo sigue ciclos: luz y sombra, vida y muerte, plenitud y vacío. Aceptar estos ciclos es vivir en armonía. La contemplación, la paciencia y la sabiduría son virtudes que iluminan incluso en la oscuridad.",
        "stronghold": "Los sacerdotes de Tsukiyomi, al alcanzar nivel 9, pueden fundar un Santuario Lunar, erigido en una colina o montaña abierta al cielo nocturno, desde donde guían a sus comunidades y celebran vigilias lunares.",
        "campaign_link": "Señor de la luna plateada, la introspección y los secretos nocturnos. Ofrece guía en la penumbra y preside la serenidad reflexiva.",
        "icon": "🌙"
    },
    {
        "id": "solkarion",
        "name": "Solkarion",
        "title": "La Llama Inmortal / El Sol Divino",
        "pantheon": "Amarkan",
        "pantheon_title": "Fe Monolítica de Amarkan (Culto Solar de Thir)",
        "rank": "Deidad Suprema (Monoteísmo)",
        "plane": "Monte Celestia / El Sol Radiante",
        "alignment": "LB",
        "alignment_name": "Legal Bueno / Dogmático",
        "portfolio": [
            "Sol",
            "Luz Absoluta",
            "Ley Imperial",
            "Justicia Inflexible",
            "Pureza Sagrada",
            "Cruzada contra la Herejía"
        ],
        "symbol": "Un dragón alado dorado inscrito en un disco solar ardiente",
        "worshippers": "Caballeros cruzados, paladines de Thir, inquisidores solares, magistrados imperiales, Seraphine Alondar y los ciudadanos de Amarkan.",
        "cleric_order": "Caballeros de la Llama Radiante / Inquisidores del Sol",
        "cleric_requirements": "Sabiduría 14+, Fuerza 12+, Carisma 13+",
        "cleric_alignment": "LB, LN",
        "weapons": "Espada bastarda, maza de armas, lanza solar, martillo de guerra",
        "armor": "Armadura de placas completa y escudos grandes dorados",
        "magic_items": "Cualquier objeto clerical, espadas y armaduras bendecidas con luz solar",
        "spheres_major": [
            "All",
            "Combat",
            "Divination",
            "Healing",
            "Law",
            "Protection",
            "Sun",
            "War"
        ],
        "spheres_minor": [
            "Guardian",
            "Necromantic (solo expulsión/reversión)",
            "Travelers",
            "Wards"
        ],
        "powers_granted": [
            {
                "level": 1,
                "name": "Resplandor Sagrado",
                "description": "Lanzar Light a voluntad; +2 a tiradas de salvación contra ceguera o fuego."
            },
            {
                "level": 5,
                "name": "Furia de la Aurora",
                "description": "Canalizar daño radiante extra en golpes cuerpo a cuerpo contra muertos vivientes o demonios 1/día."
            },
            {
                "level": 9,
                "name": "Voz Inquisitorial",
                "description": "Lanzar True Seeing o Dispel Evil 1/día."
            }
        ],
        "vestment": "Sobretúnicas blancas y doradas sobre armaduras pulidas como espejos; capas escarlatas con el dragón solar bordado.",
        "organization": "Estrictamente militar y vertical. La Sede Patriarcal en Amarkan rige obispados y comendadorías en cada provincia de Thir.",
        "rituals": "• La Oración del Cénit: plegaria obligatoria a mediodía cuando el sol alcanza su punto álgido. • La Pira de la Purificación: incineración solemne de restos de abominaciones.",
        "allies_enemies": "Aliados: Hachiman (por el honor marcial y la defensa), Amaterasu (por la veneración a la luz). Oponentes irreconciliables: Selkar, cultos nigrománticos, aberraciones del pozo y herejes.",
        "dogma": "La luz solar es la única verdad purificadora que mantiene a raya el caos primordial. La ley debe ser implacable para proteger al inocente, y la oscuridad no debe ser tolerada bajo ningún pacto.",
        "stronghold": "Basílica Fortificada de la Aurora al nivel 9, que acoge una guarnición de cruzados y clérigos devotos.",
        "campaign_link": "Deidad suprema del Culto Monolítico de Amarkan y fe oficial del Imperio de Thir. Venerado por Seraphine Alondar y los cruzados solares.",
        "icon": "🌞"
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
    "deities": deities,
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

# Generar y sincronizar wiki/pnjs/
pnjs_wiki_dir = os.path.join(WIKI_DIR, "pnjs")
os.makedirs(pnjs_wiki_dir, exist_ok=True)

for n in curated_npcs:
    wfile = n.get("wiki_file")
    if not wfile:
        slug = re.sub(r'[^a-zA-Z0-9_]', '_', n["name"].lower().replace(' ', '_')) + ".md"
        wfile = slug
    
    filepath = os.path.join(pnjs_wiki_dir, wfile)
    
    # Conservar el bloque especial de Katsumi si ya existe o crearlo
    extra_block = ""
    if n["name"] == "Katsumi":
        extra_block = """
---

## 🔮 Conexión Divina & El Enigma de Shien
Como clériga consagrada a **Shien (La Llama Púrpura)** y miembro de las *Llamas Custodias (Hi no Mamori)*, representa la devoción por la magia ordenada y el tránsito digno de los caídos. Sin embargo, el reciente descubrimiento en **[[../lore_y_misterios/frescos-kanatsu-mi|Los Frescos de Kanatsu-mi]]** plantea una inquietante incógnita para su fe: la diosa Shien ha sido deliberadamente omitida del sanctum primordial (en la puerta de obsidiana, los estantes y los frescos), pese a que la geometría sagrada fue concebida para diez dioses.
"""

    content = f"""# {n['name']}
> *{n.get('nickname', n['role'])}*

- **Categoría:** {n.get('category', 'Personaje de Campaña')}
- **Raza / Edad:** {n.get('race', 'Desconocida')} ({n.get('age', 'Edad desconocida')})
- **Rol / Profesión:** {n['role']}
- **Ubicación:** {n['location']}
- **Facción:** {n['faction']}
- **Actitud hacia el Grupo:** {n['attitude']}
- **Estado Actual:** {n['status']}

---

## 📝 Notas y Observaciones
{n['notes']}
{extra_block}
---
[[README|← Volver al Índice de la Wiki]]
"""
    with open(filepath, "w", encoding="utf-8") as wf:
        wf.write(content)

print(f"Build complete. {len(koonies_roster)} PJs, {len(curated_npcs)} NPCs (wiki generada), {len(curated_sessions)} Sessions.")

