#!/usr/bin/env python3
"""Rebuild the embedded data in index.html from the JSON sources.

    python3 tools/build.py

- clean_antibodies.json is the single source of truth for the inventory: its contents replace
  the inline `const antibodies=[...]` array, and the banner counts are refreshed.
- The fluorochrome maps (CONJ_MAP, FluorPeakByInstrument, FluorSpectra, Instruments) are edited
  in index.html; this script mirrors FluorPeakByInstrument back into instruments.json so the two
  never drift. Run tools/validate.py afterwards.
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
html_path, json_path, inst_path = ROOT / "index.html", ROOT / "clean_antibodies.json", ROOT / "instruments.json"
html = html_path.read_text(encoding="utf-8")
inv = json.loads(json_path.read_text(encoding="utf-8"))

m = re.search(r"const antibodies=(\[.*?\]);\n", html, re.S)
html = html[:m.start(1)] + json.dumps(inv, indent=2, ensure_ascii=False) + html[m.end(1):]

n_clone = sum(1 for a in inv if a["clone"].strip())
html, n_sub = re.subn(r"(v\d+\.\d+ · )\d+ reagents \(\d+ with clone\)", rf"\g<1>{len(inv)} reagents ({n_clone} with clone)", html)
html_path.write_text(html, encoding="utf-8")

peaks = json.loads(re.search(r"const FluorPeakByInstrument=(\{.*?\});\n", html, re.S).group(1))
inst = json.loads(inst_path.read_text(encoding="utf-8"))
if inst.get("fluor_peaks") != peaks:
    inst["fluor_peaks"] = peaks
    inst_path.write_text(json.dumps(inst, indent=2) + "\n", encoding="utf-8")
    print("instruments.json fluor_peaks resynced")
print(f"index.html rebuilt: {len(inv)} entries, {n_clone} with clone, banner updated={bool(n_sub)}")
