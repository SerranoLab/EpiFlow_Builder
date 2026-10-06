# EpiFlow Panel Builder — Clone-ID & Data Review (May 2026)

> **Round-3 resolution (Sandeep Sreerama, May 2026) — incorporated into v1.2.**
> Parts 4 and 5 below are now closed out. Part 4 spot-check: 22 of 23 BD/BioLegend clones confirmed as-is; one correction (AB111 CD36 BUV496 → `FA6-152`, the prior `CLB-IVC7` belonged to a different FITC product). Part 5: all 61 manual-lookup clones filled, plus the additional Sandeep entries (GFP, NR2F2, NG2-APC, etc.). Verified conjugation corrections were applied where the dataset disagreed with the vendor page — six Miltenyi entries labeled `Purified` are in fact conjugated (AB133 VioBlue, AB134 PE-Vio 615, AB135 PE-Vio 770, AB136 APC-Vio 770, AB138 APC-Vio 770, AB142 PE-Vio 615), AB005 is CoraLite Plus 488, AB152 is Alexa Fluor 488 (not FITC), and AB165 is Alexa Fluor Plus 405 (not AF647). Catalog-number corrections: AB097 → `130-118-495`, AB151 → `130-126-625`, AB123 → `359611`. Marker labels unified (NG2 family → `NG2/CSPG4`; AB065 → `Nestin`). AB058 (Biomatik FLAG ELISA peptide) is **left pending Angie's decision** on whether it belongs in a flow panel. Clone coverage after this round: **205/221 (93%)**. Per-field detail in `fixes_log.json` (round 3).

This review consolidates two clone-audit passes against the original 221-entry inventory. Coverage went from 56/221 (25%) entries with clones to 129/221 (58%) after both passes.

---

## Part 1 — Verified errors corrected (5)

| ID | Marker | Field | Old | New | Source |
|---|---|---|---|---|---|
| AB032 | H3K9ac | clone | `C4B11` | `C5B11` | CST cat 28036 H3K9ac PE conjugate is clone C5B11 (cellsignal.com) |
| AB103 | CD326/EpCAM | antibody | `APC ... CD325 (EpCAM)` | `APC ... CD326 (EpCAM)` | CD325 is N-Cadherin/CDH2; CD326 is EpCAM |
| AB092 | Acetylated Tubulin | antibody | `... Tublin ...` | `... Tubulin ...` | Spelling |
| AB097 | CD144/VE-Cadherin | antibody | `... conjudated CLon ...` | `... conjugated Clone ...` | Spelling |
| AB164 | PCNA | antibody | `... prodcued ...` | `... produced ...` | Spelling |

## Part 2 — Clone IDs auto-extracted from product names (36)

Clones already embedded in the existing product-name strings — extracted programmatically, no vendor lookup needed. Worth a sanity check but very low error risk.

**BD listing-format extractions (13):** AB171 (CD11b → D12), AB172 (CD146 → P1H12), AB173 (CD163 → GHI/61), AB174 (CD19 → SJ25C1), AB176 (CD3 → SK7), AB179 (CD33 → WM53), AB180 (CD34 → 8G12), AB181 (CD45 → HI30), AB182 (CD45RA → HI100), AB183 (CD45RO → UCHL1), AB184 (CD56 → B159), AB185 (CD68 → Y1/82A), AB200 (NG2 → 7.1).

**Parenthetical / bracketed clones (9):** AB070 PAX6 → PAX6/1166, AB073 SOX10 → SOX10/991, AB079 p53 → DO-7, AB161 OLIG2 → EPR2673, AB163 Pro-Caspase-3 → E61, plus four IgG isotype controls (AB009 RbNP15, AB010 P3.6.2.8.1, AB022 eBM2a, AB023 eBMG2b).

**Polyclonal labels (14):** Set `clone = Polyclonal` for entries explicitly marked polyclonal in the antibody name (AB007, AB014, AB064, AB076, AB078, AB083, AB084, AB089, AB094, AB119, AB130, AB189, AB190, AB191).

## Part 3 — Round-2 vendor lookups (14)

Verified by direct search of vendor product pages this session:

| ID | Marker | Conjugate | Vendor | Cat. | Clone | Confidence | Source |
|---|---|---|---|---|---|---|---|
| AB062 | Brachyury/T | APC | R&D Systems | IC2085A | `Polyclonal` | high | R&D Systems IC2085A: Goat Anti-Human/Mouse Brachyury polyclonal antibody |
| AB063 | Brachyury/T | PE | R&D Systems | IC2085P | `Polyclonal` | high | R&D Systems IC2085P: Goat Anti-Human/Mouse Brachyury polyclonal antibody |
| AB065 | NESTIN | Alexa Fluor 594 | R&D Systems | IC1259T-100UG | `196908` | high | R&D Systems IC1259T: URL slug includes clone 196908 |
| AB071 | SOX10 | Alexa Fluor 647 | Abcam | ab270151 | `SP267` | high | Abcam ab270151: Alexa Fluor 647 Anti-SOX10 [SP267] |
| AB074 | SOX10 | Purified | R&D Systems | AF2864-SP | `Polyclonal` | high | R&D Systems AF2864: Goat Anti-Human SOX10 polyclonal antibody |
| AB077 | alpha-SMA/ACTA2 | PerCP | R&D Systems | IC1420C | `1A4` | high | R&D Systems IC1420C: alpha-Smooth Muscle Actin PerCP, clone 1A4 |
| AB115 | CD13 | BV421 | BioLegend | 301716 | `WM15` | high | BioLegend product page 301716 CD13 BV421 |
| AB124 | CD57 | PE | BioLegend | 359612 | `HNK-1` | high | BioLegend product page 359612 CD57 PE |
| AB158 | Nestin | BV421 | BioLegend | 656808 | `10C2` | medium | BioLegend Nestin product family |
| AB160 | NG2/CSPG4 | Purified | Abcam | ab255811 | `EPR22410-145` | high | Abcam ab255811: Recombinant Anti-NG2 antibody [EPR22410-145] |
| AB178 | CD31 | Purified | R&D Systems | BBA7 | `9G11` | high | R&D Systems BBA7: CD31/PECAM-1 monoclonal, clone 9G11 |
| AB194 | SOX9 | PE | Abcam | ab224019 | `EPR14335-78` | high | Abcam ab224019: SOX9 PE conjugate uses clone EPR14335-78 |
| AB199 | NG2 | Alexa Fluor 700 | R&D Systems | FAB2585N | `LHM-2` | high | R&D Systems FAB2585N: NG2/MCSP AF700 - clone LHM-2 |
| AB204 | Tubulin | Alexa Fluor 488 | R&D Systems | IC1195G-100 | `TUJ-1` | high | R&D Systems IC1195G: Neuron-specific beta-III Tubulin AF488, clone TUJ-1 |

## Part 4 — Clones present but provenance not fully captured (23) — **spot-check before publication**

These BD/BioLegend entries have clone values populated, and the values match what I recognize as the canonical BD clones for each catalog (e.g., WM15 for CD13, αR1 for CD140a, B56 for Ki-67, 12G5 for CXCR4 — all standard BD products). However, my session logs don't capture the exact moment I added them, so I'm flagging them as needing a quick spot-check rather than claiming verification. Sandeep can confirm each in 5-10 minutes by searching the BD catalog by cat. number — the BD product pages list the clone prominently.

| ID | Marker | Conjugate | Cat. | Current clone (verify) |
|---|---|---|---|---|
| AB004 | GFAP | Alexa Fluor 647 | 561470 | `1B4` |
| AB069 | PAX6 | PE | 561552 | `O18-1330` |
| AB081 | TUJ1/TUBB3 | Purified | 801213 | `TUJ1` |
| AB098 | EOMES/TBR2 | BUV395 | 567171 | `X4-83` |
| AB103 | CD326/EpCAM | APC | 566842 | `9C4` |
| AB110 | CD271/NGFR | Alexa Fluor 488 | 567393 | `C40-1457` |
| AB111 | CD36 | BUV496 | 756799 | `CLB-IVC7` |
| AB113 | HK1 | BUV661 | 570557 | `EPR10134(B)` |
| AB114 | CD140a/PDGFRa | BUV805 | 748620 | `αR1` |
| AB116 | CD13 | BV786 | 740967 | `WM15` |
| AB120 | CD57 | PE | 560844 | `NK-1` |
| AB121 | CD140b/PDGFRb | PE | 558821 | `28D4` |
| AB122 | CD56/NCAM1 | PE | 561903 | `B159` |
| AB126 | CD140a/PDGFRa | PE | 556002 | `αR1` |
| AB137 | CD184/CXCR4 | BUV737 | 741862 | `12G5` |
| AB139 | DLL4 | BUV563 | 748346 | `MHD4-46` |
| AB140 | HER4/ErbB4 | BV711 | 756650 | `P6-1` |
| AB143 | CD140b/PDGFRb | Purified | 558820 | `28D4` |
| AB144 | CD13 | Purified | 555393 | `WM15` |
| AB145 | NOTCH3 | BV711 | 745463 | `MHN3-21` |
| AB149 | Ki67 | BUV395 | 564071 | `B56` |
| AB197 | Chondroitin Sulfate/NG2 | Alexa Fluor 488 | 562413 | `9.2.27` |
| AB201 | OCT4 | Alexa Fluor 647 | 560329 | `40/Oct-3` |

## Part 5 — Entries still needing manual clone lookup (61)

Grouped by vendor. The Miltenyi REAfinity cluster is the largest — each product page on miltenyibiotec.com lists the REA clone code prominently, so this is fast batch-lookup work.

### Aves Lab (1)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB101 | GFP | Purified | GFP-1010 |

### Aviva (1)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB075 | NR2F2/COUP-TFII | FITC | ARP39466_T100-FITC |

### Bio-techne (ordered through fisher) (1)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB198 | NG2 | APC | FAB2585A |

### Cell Signaling (2)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB085 | beta-Actin | Purified | 4967S |
| AB096 | Biotin (detection) | HRP | 7075S |

### Fisher (3)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB153 | Mouse IgG2a (secondary) | Alexa Fluor 568 | A-21134 |
| AB155 | Mouse IgG2a (secondary) | Alexa Fluor 647 | A-21241 |
| AB192 | KMT2D | Purified | 50-173-5625 |

### GeneTex (3)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB003 | Ki67 | Purified | GTX20833 |
| AB087 | mCherry | Purified | GTX128508 |
| AB203 | SOX2 | Purified | GTX124477 |

### MilliporeSigma (1)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB057 | FLAG/DYKDDDDK | Purified | F3165-.2MG |

### Miltenyi Biotec (21)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB097 | CD144/VE-Cadherin | PE | 120-118-495 |
| AB106 | CD309/VEGFR-2 | APC-Vio 770 | 130-117-914 |
| AB107 | CD309/VEGFR-2 | APC | 130-120-478 |
| AB108 | CD309/VEGFR-2 | APC | 130-117-984 |
| AB117 | DLL4 | Biotin | 130-118-234 |
| AB118 | NOTCH1 | Biotin | 130-112-523 |
| AB125 | CD144/VE-Cadherin | PE | 130-118-495 |
| AB127 | DLL4 | PE-Vio 615 | 130-118-229 |
| AB128 | CD309/VEGFR-2 | PE-Vio 615 | 130-117-985 |
| AB132 | PAX3 | Vio B515 | 130-131-114 |
| AB133 | CD31/PECAM-1 | Purified | 130-110-812 |
| AB134 | DLL4 | Purified | 130-118-383 |
| AB135 | EPHB4 | Purified | 130-115-598 |
| AB136 | CD34 | Purified | 130-124-457 |
| AB138 | CD140a/PDGFRa | Purified | 130-115-241 |
| AB141 | cTnT | Vio B515 | 130-129-225 |
| AB142 | CD166/ALCAM | Purified | 130-132-832 |
| AB147 | CD309/VEGFR-2 | Vio Bright V423 | 130-128-286 |
| AB148 | NOTCH1 | Vio Bright V423 | 130-128-652 |
| AB151 | CD140a/PDGFRa | APC-Vio 770 | 130-125-521 |
| AB205 | CD31/PECAM-1 | APC | 130-119-976 |

### Novus (1)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB066 | NEUN | Alexa Fluor 647 | NBP1-92693AF647 |

### Proteintech (4)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB005 | OLIG2 | Purified | CL488-13999 |
| AB054 | FLAG/DYKDDDDK | CoraLite Plus 647 | CL647-66008 |
| AB195 | TBR1 | CoraLite 594 | CL594-66564 |
| AB196 | TBR1 | Purified | 20932-1-AP |

### R&D but bought from Fisher (1)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB080 | O4 | Purified | MAB1326SP |

### Sigma Aldrich (4)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB092 | Acetylated Tubulin | Purified | T7451-25ul |
| AB150 | KMT2D | Purified | HPA035977-100UL |
| AB157 | MBP | Purified | AB9348 |
| AB164 | PCNA | Purified | P8825-25UL |

### Thermo (3)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB006 | OLIG2 | Purified | MA5-15810 |
| AB086 | GAPDH | Purified | AM4300 |
| AB168 | Rabbit IgG (secondary) | HRP | 656120 |

### Thermo Fisher (15)

| ID | Marker | Conjugation | Cat. No. |
|---|---|---|---|
| AB025 | AQP4 | Purified | PIMA541556 |
| AB058 | FLAG/DYKDDDDK | Purified | 50-228-8484 |
| AB099 | Goat IgG (Donkey secondary) | Alexa Fluor 488 | A-11055 |
| AB100 | Goat IgG (Donkey secondary) | Alexa Fluor 568 | A-11057 |
| AB109 | CD14 | APC-Fire 810 | 50-207-8325 |
| AB123 | CD57 | PE | 35911 |
| AB129 | CD69 | PE-Fire 640 | 50-207-3478 |
| AB152 | Mouse IgM (secondary) | FITC | A-21042 |
| AB154 | Mouse IgM (secondary) | Alexa Fluor 647 | A-21238 |
| AB156 | Mouse IgG (secondary) | HRP | 31430 |
| AB162 | PAX6 | Purified | 901301 |
| AB165 | Rabbit IgG (secondary) | Alexa Fluor 647 | PIA48254 |
| AB166 | Rabbit IgG (secondary) | Alexa Fluor 647 | A-31573 |
| AB167 | Rabbit IgG (secondary) | Alexa Fluor 647 | 10543623 |
| AB202 | SOX2 | APC | IC2018A |

---

## Other observations

**Marker-name consolidation.** The NG2 marker is split across four labels (AB160 `NG2/CSPG4`, AB197 `Chondroitin Sulfate/NG2`, AB198–200 `NG2`). The alternative-conjugate suggestions feature uses exact marker-name matching, so cross-suggestions won't appear until the labels are unified. Consider standardizing on `NG2/CSPG4` for all five entries. Same case for `Nestin` (AB158) vs `NESTIN` (AB065).

**AB058 (Biomatik FLAG-Tag, Thermo Fisher 50-228-8484).** Listed as `Biomatik Corporation FLAG-Tag (DYKDDDDK-Tag Protein) ELISA`. This appears to be a recombinant FLAG peptide for ELISA standards, not a flow-cytometry antibody. Worth confirming whether this entry should remain in the panel builder.

**AB081 (TUJ1, BioLegend cat 801213).** Catalog field reads `Cat# 801213`; strip the prefix.

**AB080 (O4).** Vendor field is `R&D but bought from Fisher`; pick one (R&D Systems is the manufacturer, Fisher the distributor).

**AB025 (AQP4).** The string `Ms IgG2k` in the antibody field is the host/isotype, not a clone. Thermo catalog should give the actual clone.


---

## Round 4 (October 2026) — entries added from the ordering-sheet reconciliation that still need a clone

These seven reagents were purchased (confirmed order tabs, 2022–2026) but the ordering sheet does not record a clone. Verify against the vial or vendor page and fill the `clone` field.

| ID | Marker | Vendor | Catalog | Conjugation | Note |
|----|--------|--------|---------|-------------|------|
| AB234 | DLL4 | R&D Systems | MAB1506 | Purified | Rat monoclonal; ordered 3× in 2026 |
| AB235 | RBPJ | Santa Cruz | sc-271128 | Purified | "IP-verified monoclonal" on the 2023 order |
| AB240 | CD140a/PDGFRα | Thermo Fisher | MA1-10097 | APC | 2024 order; mouse monoclonal |
| AB242 | MAP2 | Sigma-Aldrich | FCMAB318PE | PE | Milli-Mark conjugate, 2024 |
| AB247 | SOX2 | Antibodies Inc | SOX2-0020 | Purified | CUT&RUN, 2026 |
| AB248 | H3K4me3 | EpiCypher | 13-0060 | Purified | SNAP-Certified CUT&RUN; EpiCypher lists a clone on the datasheet |
| AB249 | H3K27me3 | EpiCypher | 13-0055 | Purified | SNAP-Certified CUT&RUN; EpiCypher lists a clone on the datasheet |

Also flagged, not changed: **AB045** (Histone H3 D1H2 purified, CST 4499) appears in no ordering sheet 2022–2026; confirm it is in the freezer or retire it. **AB058** (Biomatik FLAG-tag ELISA kit) is not a flow reagent and remains pending a decision.
