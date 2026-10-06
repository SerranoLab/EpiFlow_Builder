#!/usr/bin/env python3
"""Integrity checks for the EpiFlow Panel Builder data layer.

Run from the repository root:  python3 tools/validate.py
Exit status 1 on any failure. Stdlib only, so it runs in CI without installs.
"""
import json, re, sys, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODULES = {"Core EpiFlow", "Cell Cycle", "Epigenetic", "Neural", "Pericyte", "Vascular", "Immune",
           "NOTCH", "Cardiac", "Pluripotent", "Structural", "Detection", "Fluorescent Protein", "Control",
           "Phenotype"}
fails, warns = [], []

def block(html, name):
    m = re.search(r'const ' + name + r'=(\{.*?\}|\[.*?\]);\n', html, re.S)
    if not m:
        fails.append(f"index.html: cannot find `const {name}`"); return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        fails.append(f"index.html: `const {name}` is not valid JSON ({e})"); return None

html = (ROOT / "index.html").read_text(encoding="utf-8")
inv = json.loads((ROOT / "clean_antibodies.json").read_text(encoding="utf-8"))
inst_json = json.loads((ROOT / "instruments.json").read_text(encoding="utf-8"))
inline = block(html, "antibodies")
conj_map = block(html, "CONJ_MAP")
peaks = block(html, "FluorPeakByInstrument")
spectra = block(html, "FluorSpectra")
instruments = block(html, "Instruments")
m = re.search(r'const NON_FLUOR=new Set\((\[.*?\])\)', html)
non_fluor = set(json.loads(m.group(1))) if m else set()
m = re.search(r'const CORE_PANEL_IDS=(\[.*?\]);', html)
core_ids = json.loads(m.group(1)) if m else []

# 1. inline data equals the JSON file
if inline is not None and inline != inv:
    fails.append("inline `antibodies` array in index.html differs from clean_antibodies.json (rebuild with tools/build.py)")

# 2. ids and catalogs
ids = [a["id"] for a in inv]
for i, c in collections.Counter(ids).items():
    if c > 1: fails.append(f"duplicate id {i}")
for a in inv:
    if not re.fullmatch(r"AB\d{3}", a["id"]): fails.append(f"malformed id {a['id']!r}")
cats = collections.Counter(a["catNo"].strip().upper() for a in inv if a["catNo"].strip())
for c, n in cats.items():
    if n > 1: fails.append(f"duplicate catalog number {c} ({n} entries)")

# 3. every conjugation resolves; every fluor key has peaks and spectra on every instrument
for a in inv:
    conj = a.get("conjugation", "")
    if conj not in conj_map and conj not in non_fluor:
        fails.append(f"{a['id']} {a['marker']}: conjugation {conj!r} is not in CONJ_MAP or NON_FLUOR")
for key in set(conj_map.values()):
    for inst_name, mp in peaks.items():
        if key not in mp: fails.append(f"fluor key {key} has no peak detector for {inst_name}")
    if key not in spectra: fails.append(f"fluor key {key} has no FluorSpectra entry")
for inst_name, mp in peaks.items():
    chans = {c["id"] for c in instruments[inst_name]["channels"]}
    for key, det in mp.items():
        if det not in chans: fails.append(f"{inst_name}: {key} points at unknown detector {det}")

# 4. instruments.json mirrors index.html
if inst_json.get("fluor_peaks") != peaks:
    fails.append("instruments.json fluor_peaks differs from FluorPeakByInstrument in index.html")

# 5. modules
for a in inv:
    for mod in a["module"].split("|"):
        if mod.strip() not in MODULES: fails.append(f"{a['id']} {a['marker']}: unknown module {mod.strip()!r}")

# 6. core preset exists and is conflict-free by peak detector (Aurora)
by_id = {a["id"]: a for a in inv}
dets = collections.defaultdict(list)
for cid in core_ids:
    if cid not in by_id: fails.append(f"CORE_PANEL_IDS references missing id {cid}"); continue
    key = conj_map.get(by_id[cid]["conjugation"])
    if key: dets[peaks["Cytek_Aurora_5L"].get(key)].append(by_id[cid]["marker"])
for d, ms in dets.items():
    if len(ms) > 1: fails.append(f"core preset detector overlap on {d}: {', '.join(ms)}")

# 7. soft warnings
for a in inv:
    if a["conjugation"] in conj_map and not a["laser"]: warns.append(f"{a['id']} conjugated but laser field empty")
    if not a["role"]: warns.append(f"{a['id']} {a['marker']}: empty role")
    if re.search(r"cat#|\s\(", a["catNo"], re.I): warns.append(f"{a['id']}: catalog field looks unclean: {a['catNo']!r}")
banner = re.search(r"v(\d+\.\d+) · (\d+) reagents \((\d+) with clone\)", html)
if banner:
    n, nc = int(banner.group(2)), int(banner.group(3))
    real_nc = sum(1 for a in inv if a["clone"].strip())
    if n != len(inv): fails.append(f"banner says {n} reagents, inventory has {len(inv)}")
    if nc != real_nc: warns.append(f"banner says {nc} with clone, inventory has {real_nc}")

for w in warns: print("WARN ", w)
for f in fails: print("FAIL ", f)
print(f"{len(inv)} entries · {len(fails)} failures · {len(warns)} warnings")
sys.exit(1 if fails else 0)
