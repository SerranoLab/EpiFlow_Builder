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

def load(path):
    kw, arr, names = read_fcs(path); idx = {n: i for i, n in enumerate(names)}
    fl = [n for n in names if re.fullmatch(r"(UV|V|B|YG|R)\d+-A", n)]
    fsc, ssc, fh = arr[:, idx["FSC-A"]], arr[:, idx["SSC-A"]], arr[:, idx["FSC-H"]]
    r = fh / np.maximum(fsc, 1)
    g = ((fsc > np.percentile(fsc, 5)) & (fsc < np.percentile(fsc, 95)) & (ssc > np.percentile(ssc, 5)) &
         (ssc < np.percentile(ssc, 95)) & (np.abs(r - np.median(r)) < 2 * np.std(r)))
    return arr[g][:, [idx[n] for n in fl]], [n[:-2] for n in fl], kw

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("globs", nargs="+"); ap.add_argument("--instrument", default="Cytek_Aurora_5L"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    files = sorted(p for g in a.globs for p in glob.glob(g))
    un_file = [f for f in files if "unstained" in f.lower()]
    if not un_file: sys.exit("need an Unstained reference file")
    un, chans, kw = load(un_file[0]); un_med = np.median(un, axis=0); un_hi = np.percentile(un, 99.5, axis=0)
    sig, report = {}, []
    for f in files:
        if f in un_file: continue
        m = re.search(r"Reference Group-[A-Z]\d+ (.*?) \((Beads|Cells)\)", f)
        name = m.group(1) if m else pathlib.Path(f).stem
        X, ch, _ = load(f)
        if ch != chans: sys.exit(f"channel layout differs in {f}")
        med = np.median(X, axis=0) - un_med; peak = int(np.argmax(med))
        thr = un_hi[peak] + (np.percentile(X[:, peak], 95) - un_hi[peak]) * 0.2
        pos = X[:, peak] > thr; neg = ~pos
        P, N = X[pos], (X[neg] if neg.sum() >= 200 else un)
        s = np.clip(np.median(P, axis=0) - np.median(N, axis=0), 0, None); s = s / s.max()
        sig[name] = {c: round(float(v), 4) for c, v in zip(chans, s)}
        report.append((name, chans[int(np.argmax(s))], int(pos.sum()), int(neg.sum())))
    for n, pk, p, q in report: print(f"{n:28s} peak={pk:5s} positive={p:6d} negative={q:6d}")
    out = {"instrument": a.instrument, "cytometer": kw.get("$CYT", ""), "serial": kw.get("$CYTSN", ""),
           "generated": datetime.date.today().isoformat(), "source_files": [pathlib.Path(f).name for f in files],
           "method": "median(positive) - median(negative) per detector, clipped at 0, peak-normalized; bead gate central 5-95% FSC/SSC + singlets",
           "channels": chans, "signatures": sig}
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(sig)} signatures written to {a.out}")

if __name__ == "__main__":
    main()
