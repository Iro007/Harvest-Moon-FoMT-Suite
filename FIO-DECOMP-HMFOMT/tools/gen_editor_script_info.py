"""Genera la tabla de scripts que usa mapa_editor_corregido.html.

Para cada script de assets/events/evento_NNNN.txt guarda sus Warp_Player(escena, x, y)
y el primer mensaje (como etiqueta corta). La colisión de un mapa enlaza con estos scripts:
  - campo «evento» (bits 2..15)  -> script = evento
  - campo «objeto» (bits 16..31) -> script = objeto >> 1

Uso:  python tools/gen_editor_script_info.py  > script_info.json
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVENTS = os.path.join(HERE, "..", "assets", "events")
NAMES = os.path.join(HERE, "..", "assets", "data", "map_names.json")

WARP = re.compile(r"Warp_Player\(\s*(0x[0-9A-Fa-f]+|\d+)\s*,\s*(0x[0-9A-Fa-f]+|\d+)\s*,\s*(0x[0-9A-Fa-f]+|\d+)\s*\)")
MSG = re.compile(r'const MESSAGE_0 = "(.*)";')


def label(raw: str) -> str:
    s = re.sub(r"\\x[0-9A-Fa-f]{2}|\\[A-Z_]+|\\r|\\n", " ", raw)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:40]


def main() -> None:
    scripts = {}
    for name in sorted(os.listdir(EVENTS)):
        m = re.match(r"evento_(\d+)\.txt$", name)
        if not m:
            continue
        text = open(os.path.join(EVENTS, name), encoding="utf-8", errors="replace").read()
        warps = []
        for w in WARP.findall(text):
            t = [int(v, 0) for v in w]
            if t not in warps:
                warps.append(t)
        msg = MSG.search(text)
        entry = {}
        if warps:
            entry["w"] = warps[:4]
        if msg and label(msg.group(1)):
            entry["m"] = label(msg.group(1))
        if entry:
            scripts[int(m.group(1))] = entry
    scenes = {}
    for row in json.load(open(NAMES, encoding="utf-8"))[1:]:
        scenes[int(row[1].strip(), 16)] = row[0].strip()
    json.dump({"scenes": scenes, "scripts": scripts}, sys.stdout, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main()
