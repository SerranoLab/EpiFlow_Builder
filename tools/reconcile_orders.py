#!/usr/bin/env python3
"""Reconcile the Panel Builder inventory against the lab ordering sheets.

    python3 tools/reconcile_orders.py "path/to/Ordering/**/*.xlsx" [--out RECONCILIATION.md]

Reads every yearly ordering workbook, keeps the confirmed-order tabs (template, draft,
recurring and reimbursement-summary tabs are skipped), and reports in both directions:
  A. antibody-like purchase lines whose catalog number matches no inventory entry
  B. inventory entries whose catalog number appears in no purchase line
Catalog numbers are normalised the way vendors write them inconsistently (CST "#54826"
vs "54826S", Fisher's "BDB" prefix for BD, trailing size suffixes). Requires openpyxl.
"""
import sys, re, json, glob, datetime, pathlib, argparse, collections, warnings
warnings.filterwarnings("ignore")
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_TABS = {"Grant Template", "Ordering Template", "Order template", "Startup Grant", "To Order",
             "Climate Action Plan Grant", "Climate Action Plan Grant 22-23", "Sheet5"}
REQUEST_TABS = {"Draft Orders", "Recurring Orders", "Non-Cat Orders"}
AB_KW = re.compile(r"antibod|anti-|anti |mab\b|monoclonal|polyclonal|clone|reafinity|isotype|streptavidin|zombie|"
                   r"live/dead|fixable|fxcycle|viability|alexa|\bpe\b|pe-|\bapc\b|\bbv\d|buv|\bbb\d|fitc|percp|vio\b|"
                   r"vioblue|brilliant|conjugat|dapi|hoechst|igg|igm|coralite|dylight|cardinal red|rb\d{3}|mfluor|phalloidin|edu", re.I)
EXCL = re.compile(r"\btip|tube|flask|pipet|plate|glove|serum\b|albumin|medium|media\b|buffer|primer|oligo|paper|"
                  r"trypsin|accutase|collagenase|dispase|dnase|rnase|matrigel|laminin|vitronectin|protease|thrombin|"
                  r"aprotinin|ficoll|hyaluronidase|papain|cysteine|filter|box|water|alcohol|microbeads", re.I)

def ncat(s):
    s = str(s or "").upper().strip().split("(")[0].split("|")[0].strip()
    s = re.sub(r"^CELL ?SIGNAL(ING)?\s*", "", s); s = re.sub(r"^CAT#?\s*", "", s); s = s.replace("#", "")
    s = re.sub(r"\.0$", "", s); s = re.sub(r"^BDB(?=\d{6})", "", s)
    return re.sub(r"[\s\-_/]", "", s)

def variants(s):
    n = ncat(s); v = {n}
    m = re.match(r"^(\d{4,6})([STW]\d?)?$", n)
    if m: v.add(m.group(1))
    v.add(re.sub(r"(100UL|50UL|25UL|100TESTS|25UG|100UG|50UG|100G|1G|10G|5MG|1MG|10MG|1L|SP)$", "", n))
    return {x for x in v if len(x) >= 3}

def norm_date(v):
    if isinstance(v, datetime.datetime): return v.date().isoformat()
    s = str(v or "").strip()
    m = re.match(r"^(\d{1,2})[./](\d{1,2})[./](\d{4})$", s)
    if m: return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    return m.group(0) if m else ""

def read_orders(paths):
    rows = []
    for f in paths:
        year = (re.search(r"(20\d\d)", f) or [None, "?"])[1]
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        for ws in wb.worksheets:
            if ws.title in SKIP_TABS: continue
            kind = "request" if ws.title in REQUEST_TABS else "order"
            data = list(ws.iter_rows(values_only=True))
            if not data: continue
            hdr = [str(c or "").strip().upper() for c in data[0]]
            def col(*names):
                for n in names:
                    if n in hdr: return hdr.index(n)
            ci, pi, co = col("CATALOG #"), col("PRODUCT"), col("COMPANY")
            ri, li = col("PERSON REQUESTED", "REQUESTED BY", "ORDERED BY"), col("LINK")
            if pi is None: continue
            for r in data[1:]:
                r = list(r) + [""] * 20
                prod = str(r[pi] or "").strip()
                if not prod: continue
                cat = r[ci] if ci is not None else ""
                if isinstance(cat, float) and cat.is_integer(): cat = str(int(cat))
                rows.append(dict(year=year, sheet=ws.title, kind=kind, date=norm_date(r[0]),
                                 company=str(r[co] or "").strip() if co is not None else "",
                                 catalog=str(cat or "").strip(), product=prod,
                                 requester=str(r[ri] or "").strip() if ri is not None else "",
                                 link=str(r[li] or "").strip() if li is not None else ""))
    return rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("globs", nargs="+"); ap.add_argument("--out", default="RECONCILIATION.md")
    args = ap.parse_args()
    paths = sorted(p for g in args.globs for p in glob.glob(g, recursive=True))
    if not paths: sys.exit("no workbooks matched")
    rows = read_orders(paths)
    inv = json.loads((ROOT / "clean_antibodies.json").read_text(encoding="utf-8"))
    po_index, inv_index = collections.defaultdict(list), collections.defaultdict(list)
    for r in rows:
        for v in variants(r["catalog"]): po_index[v].append(r)
    for a in inv:
        for v in variants(a["catNo"]): inv_index[v].append(a)
        for m in re.findall(r"#\s?(\d{4,6})", a["antibody"]): inv_index[m].append(a)
        for m in re.findall(r"(?:ordered as|Fisher)\s+([A-Z0-9][A-Z0-9\-]{4,})", a["antibody"]):
            for v in variants(m): inv_index[v].append(a)
    ab_like = [r for r in rows if r["kind"] == "order" and AB_KW.search(r["product"]) and
               (not EXCL.search(r["product"]) or re.search(r"antibod|anti-|reafinity|streptavidin", r["product"], re.I))]
    missing = collections.OrderedDict()
    for r in sorted(ab_like, key=lambda r: r["date"] or "0000"):
        if any(v in inv_index for v in variants(r["catalog"])): continue
        key = ncat(r["catalog"]) or r["product"][:30].upper()
        missing.setdefault(key, []).append(r)
    def alt_cats(a): return re.findall(r"(?:ordered as|Fisher)\s+([A-Z0-9][A-Z0-9\-]{4,})", a["antibody"])
    unmatched = [a for a in inv if a["catNo"].strip() and not any(v in po_index for c in [a["catNo"], *alt_cats(a)] for v in variants(c))]
    out = [f"# Inventory vs ordering sheets — {datetime.date.today().isoformat()}", "",
           f"Workbooks: {len(paths)} · purchase lines: {len(rows)} · antibody-like lines: {len(ab_like)} · inventory: {len(inv)}", "",
           f"## A. Purchased antibody-like lines not in the inventory ({len(missing)})", "",
           "| First ordered | Times | Company | Catalog | Product | Requester |", "|---|---|---|---|---|---|"]
    for k, rs in missing.items():
        r = rs[0]; dates = sorted({x["date"] for x in rs if x["date"]})
        out.append(f"| {dates[0] if dates else '?'} | {len(rs)} | {r['company'][:24]} | {r['catalog'][:24]} | {r['product'][:80].replace('|','/')} | {r['requester'][:16]} |")
    out += ["", f"## B. Inventory entries with no purchase line ({len(unmatched)})", "", "| ID | Marker | Catalog | Vendor |", "|---|---|---|---|"]
    for a in unmatched: out.append(f"| {a['id']} | {a['marker']} | {a['catNo']} | {a['vendor']} |")
    out += ["", "Section A is a review list, not an add list: it includes non-flow reagents that matched the keyword net. Section B entries were never ordered under that catalog number; check the vial."]
    pathlib.Path(args.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"A: {len(missing)} candidate purchases not in inventory · B: {len(unmatched)} inventory entries without a PO · report: {args.out}")

if __name__ == "__main__":
    main()
