#!/usr/bin/env python3
"""Derive peak-normalized spectral signatures from single-stain reference FCS files.

    python3 tools/signatures_from_fcs.py "path/to/Reference Group/*.fcs" --instrument Cytek_Aurora_5L \
        --out spectra/Cytek_Aurora_5L_beads_YYYY-MM-DD.json

One file per fluorochrome plus one whose name contains "Unstained". The fluorochrome name is taken
from the SpectroFlo export pattern "Reference Group-<well> <name> (Beads|Cells).fcs". Per file:
bead/cell gate (central FSC/SSC, singlets by FSC-H/FSC-A), positives split on the peak detector,
signature = median(positive) - median(negative), clipped at 0, peak-normalized. On the 2024-06-18
bead library this reproduces SpectroFlo's similarity indices to within 0.02 (mean 0.006, n = 14 pairs).
Requires numpy only (tools/fcs_reader.py is a minimal FCS 3.x reader).
"""
import sys, glob, json, re, argparse, pathlib, datetime
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fcs_reader import read_fcs

DET = re.compile(r"^(UV|V|B|YG|R)(\d+)(?: \(\d+\))?-A$")   # Aurora "V3-A", FACSDiscover S8 "V3 (460)-A"

def load(path):
    kw, arr, names = read_fcs(path); idx = {n: i for i, n in enumerate(names)}
    fl = [n for n in names if DET.match(n)]
    ssc_name = "SSC-A" if "SSC-A" in idx else next(n for n in names if n.startswith("SSC") and n.endswith("-A"))
    fsc, ssc, fh = arr[:, idx["FSC-A"]], arr[:, idx[ssc_name]], arr[:, idx["FSC-H"]]
    r = fh / np.maximum(fsc, 1)
    g = ((fsc > np.percentile(fsc, 5)) & (fsc < np.percentile(fsc, 95)) & (ssc > np.percentile(ssc, 5)) &
         (ssc < np.percentile(ssc, 95)) & (np.abs(r - np.median(r)) < 2 * np.std(r)))
    chans = ["".join(DET.match(n).groups()) for n in fl]
    return arr[g][:, [idx[n] for n in fl]], chans, kw

def fluor_name(path):
    """SpectroFlo: 'Reference Group-<well> <name> (Beads|Cells).fcs'; FACSDiscover titrations: '<n>_<marker>_<fluor>_<dilution>.fcs'."""
    stem = pathlib.Path(path).stem
    m = re.search(r"Reference Group-[A-Z]\d+ (.*?) \((Beads|Cells)\)", stem)
    if m: return m.group(1)
    parts = stem.split("_")
    if len(parts) >= 3 and re.fullmatch(r"[\d.]+", parts[-1]):
        return parts[-3] if parts[-2].lower() in ("beads", "cells") and len(parts) >= 4 else parts[-2]
    return stem

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("globs", nargs="+"); ap.add_argument("--instrument", default="Cytek_Aurora_5L"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    files = sorted(p for g in a.globs for p in glob.glob(g))
    files = [f for f in files if "blank" not in pathlib.Path(f).stem.lower()]
    un_file = [f for f in files if "unstained" in f.lower()]
    if not un_file: sys.exit("need an Unstained reference file")
    un, chans, kw = load(un_file[0]); un_med = np.median(un, axis=0); un_hi = np.percentile(un, 99.5, axis=0)
    sig, report = {}, []
    cache = pathlib.Path(a.out)
    bright = {}
    if cache.exists():
        prev = json.loads(cache.read_text()); sig = prev.get("signatures", {}); bright = prev.get("brightness", {})
    un_spread = np.maximum(un_hi - un_med, 1.0)
    for f in files:
        if f in un_file: continue
        name = fluor_name(f)
        X, ch, _ = load(f)
        if ch != chans: sys.exit(f"channel layout differs in {f}")
        # Peak detector: largest excess of the stained 99th percentile over the unstained 99.5th percentile,
        # scaled by the unstained spread, so rare or dim positives are not outvoted by autofluorescence.
        score = (np.percentile(X, 99, axis=0) - un_hi) / un_spread
        peak = int(np.argmax(score))
        thr = un_hi[peak] + (np.percentile(X[:, peak], 99) - un_hi[peak]) * 0.3
        pos = X[:, peak] > thr; neg = ~pos
        if pos.sum() < 100: print(f"{name:28s} skipped: only {int(pos.sum())} positive events", flush=True); continue
        P, N = X[pos], (X[neg] if neg.sum() >= 200 else un)
        raw = np.median(P, axis=0) - np.median(N, axis=0)
        s = np.clip(raw, 0, None); s = s / s.max()
        b = float(raw[peak] / un_spread[peak])          # brightness of this control at its peak, in unstained-spread units
        if name in sig and bright.get(name, 0) >= b:
            print(f"{name:28s} kept earlier control (brighter: {bright[name]:.0f} vs {b:.0f})", flush=True); continue
        sig[name] = {c: round(float(v), 4) for c, v in zip(chans, s)}; bright[name] = round(b, 1)
        out = {"instrument": a.instrument, "cytometer": kw.get("$CYT", ""), "serial": kw.get("$CYTSN", ""),
               "generated": datetime.date.today().isoformat(), "source_files": [pathlib.Path(f).name for f in files],
               "method": "peak = argmax of (p99 stained - p99.5 unstained)/unstained spread; positives above 30% of the way from unstained p99.5 to stained p99; signature = median(positive) - median(negative or unstained), clipped at 0, peak-normalized; gate central 5-95% FSC/SSC + singlets; brightest control kept per fluorochrome",
               "channels": chans, "signatures": sig, "brightness": bright}
        cache.write_text(json.dumps(out, indent=1), encoding="utf-8")
        print(f"{name:28s} peak={chans[int(np.argmax(s))]:5s} positive={int(pos.sum()):6d} negative={int(neg.sum()):6d} brightness={b:7.0f}", flush=True)
    print(f"{len(sig)} signatures in {a.out}")

if __name__ == "__main__":
    main()
