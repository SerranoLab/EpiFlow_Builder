# Serrano Lab – EpiFlow Panel Builder

A single-page web application for designing spectrally aware flow cytometry panels, built around a curated inventory of 267 reagents from the Serrano Lab at Boston University's Center for Regenerative Medicine (CReM).

**[Live tool](https://serranolab.github.io/EpiFlow_Builder/)** · [![validate-data](https://github.com/SerranoLab/EpiFlow_Builder/actions/workflows/validate.yml/badge.svg)](https://github.com/SerranoLab/EpiFlow_Builder/actions/workflows/validate.yml) · Zenodo DOI badge: add once the concept DOI is minted 

**Version 1.3 · October 2026.** This release reconciles the inventory against the complete lab ordering sheets (2022–2026) and grows it from 221 to 267 entries. γH2AX (H2AX pS139, Miltenyi REAfinity clone REA502, Vio B515; purchased May 2026 for the replication-stress gate in the KMT2D S-phase experiments) is entry AB222. The reconciliation surfaced 46 purchased reagents that had never been entered: a Pacific Blue total-H3 (CST 12167), H3K9ac SignalFlex AF700 (CST 58010), H3K23ac AF488 (Abcam ab318548), DAPI and Hoechst 33342, the Click-iT EdU AF647 flow kit, AF647 phalloidin, the whole NOTCH working set (Jagged1 AF488 and purified, Notch1 D6F11, cleaved Notch1 Val1744, R&D DLL4, RBPJ), CXCR4-PE REAfinity, HIF-1α AF488, IL-6 RB780, RealBlue 613 streptavidin, PDGFRα-APC, O4-PE, MAP2-PE, Pax-6 PerCP-Cy5.5, β-catenin (FITC and purified), the CUT&RUN antibodies (EpiCypher H3K4me3 and H3K27me3, two SOX2), FKBP12 (dTAG validation), HSP90, and seventeen Alexa Fluor goat secondaries from the 2022 start-up order. Three corrections came from the purchase orders: BioLegend as the vendor of the CD57-PE pair, the duplicate CD144-PE entry merged (AB125 retired, ID not reused so saved panels stay valid), and size-variant catalog numbers recorded on the CD144, EPHB4, Notch1, CD31-APC, LIVE/DEAD Violet and anti-mouse CD140a entries rather than as duplicate cards (Sandeep's May 2026 clone review was re-checked line by line against this release; it is fully applied). The Core Panel preset is now a runnable 9-marker panel: the two same-detector alternates (H3K4me2-PE for H3K4me1-PE on YG1; H3K9ac-Pacific Blue for H3K27me3-Pacific Blue on V3) are offered as one-click swaps under the conflict box instead of being co-loaded. Smaller fixes: HOXC12 moved from the orphan `Developmental` label into Pericyte, two anti-mouse IgM secondaries given roles, the Aves anti-GFP catalog field cleaned, and five fluorochromes added to the spectral maps (RB613, DAPI, Hoechst 33342, BV570 on both instruments, PE-CF594 on the S8), with `instruments.json` resynchronized to `index.html`. Clone coverage is 243/267 (91%); the 24 blanks are dyes, fluorescent proteins, streptavidins, isotype controls, and seven antibodies whose clone the ordering sheet did not record (listed for verification in `CLONE_REVIEW.md`). Per-field changes are logged as round 4 in `fixes_log.json`.

**Version 1.2 · May 2026.** This release integrates the Round-3 clone-ID verification by Sandeep Sreerama (manual clone lookups, BD/BioLegend spot-checks, and verified conjugation and catalog-number corrections), raising clone coverage to 205/221 (93%), unifies the NG2 and Nestin marker labels so the alternative-conjugate suggestions resolve them, and adds a spectral-compatibility disclaimer to the tool footer.

---

## What it does

The EpiFlow Panel Builder helps you select antibodies and reagents for multi-parameter spectral flow cytometry panels. Unlike spectral viewers such as FluoroFinder, this tool operates one step earlier in the workflow: it helps you decide **which reagents to pull from the lab inventory** before you sit down at the instrument, catching detector conflicts and spectral overload before you waste cells and time.

The tool is organized around the **Core EpiFlow panel** — a 9-marker configuration for multiparametric histone H3 post-translational modification (H3-PTM) profiling — with interchangeable biology modules (Neural, Pericyte, Endothelial, Cardiac, Immune, NOTCH, etc.) that can be layered on top.

### Key capabilities

- **Search and filter** 267 reagents by marker, antibody name, catalog number, conjugation, module, or role.
- **Module filtering** with count badges showing how many conjugated reagents each module contains (Core EpiFlow, Cerebral/Neural, Pericyte, Endothelial, PBMC/Immune, NOTCH, Cardiac, Pluripotent, and more).
- **One-click Core Panel loading** pre-selects a runnable 9-marker EpiFlow panel with no detector conflicts: FxCycle Violet (DNA), Zombie NIR (viability), total H3-AF700, H3K27me3-Pacific Blue, H3K4me3-AF647, H3K27ac-PE-Cy7, H3K4me1-PE, phH3-AF532, Active Caspase-3-BV650. The two same-detector alternates in the Core module (H3K4me2-PE, which shares YG1 with H3K4me1-PE, and H3K9ac-Pacific Blue, which shares V3 with H3K27me3-Pacific Blue) are listed under the conflict box as one-click swaps rather than co-loaded. γH2AX-Vio B515 (B2) can be added to this panel without a conflict.
- **Dual instrument support** for Cytek Aurora 5L (64 channels) and BD FACSDiscover S8 (78 channels), with per-instrument fluorochrome-to-channel mapping derived from official Thermo Fisher selection guides.
- **Conflict detection**: primary detector overlap, fluorochrome reuse, and heuristic spectral load per Aurora/S8 channel.
- **Alternative-conjugate suggestions**: when a panel has a detector overlap or fluorochrome-reuse conflict, the tool surfaces other inventory entries for the same marker on different fluorochromes, marks which alternatives would resolve the conflict cleanly, and offers a one-click swap (feature suggested by Sandeep Sreerama).
- **Laser balance visualization** showing the proportional distribution of selected markers across UV, Violet, Blue, YG, and Red lasers.
- **Spectral fingerprint strips** on card hover, showing the heuristic emission profile of each fluorochrome across the instrument's detector array.
- **Export** your panel as clipboard text or CSV for lab notes and ordering.
- **Save/load named panel configurations** via localStorage (on a server) or JSON export/import (for local file:// use).

---

## Quick start

### Option 1: Open locally

Download `index.html` and open it in any modern browser (Chrome, Firefox, Edge, Safari). Everything is self-contained — no build step, no dependencies, no server required.

### Option 2: Deploy on GitHub Pages

1. Place `index.html` and `LICENSE` in a GitHub repository.
2. Enable GitHub Pages in the repo settings (Settings → Pages → Source: main branch).
3. The tool will be live at `https://<username>.github.io/<repo>/`.

GitHub Pages deployment enables `localStorage` for persistent panel saves across sessions.

### First use

1. Click **Load Core Panel** to pre-select the 9-marker Core EpiFlow configuration; use the **Core alternates** chips to swap in H3K4me2-PE or H3K9ac-Pacific Blue.
2. Use the **module buttons** to filter by biology (e.g., click "Neural" to see cerebral/neural reagents).
3. Click **Add** on any card to include it in your panel. The conflict checker updates in real time.
4. Check the **laser balance bar** — aim for reasonable distribution across all 5 lasers.
5. If conflicts appear (red warnings), look for alternative conjugates of the same marker in the grid.
6. **Copy to Clipboard** or **Save as CSV** to export your final panel.
7. **Save Panel** to store your configuration by name for future sessions.

---

## Reagent inventory

The 267-entry inventory was compiled from Serrano Lab purchase orders spanning 2022–2026 (fully reconciled against the ordering sheets in October 2026) and includes reagents from Cell Signaling Technology, BD Biosciences, BioLegend, R&D Systems, Miltenyi Biotec, Abcam, Thermo Fisher/Invitrogen, Novus Biologicals, Proteintech, and other vendors.

### Modules

| Module | Description | Examples |
|--------|-------------|----------|
| **Core EpiFlow** | H3-PTM profiling, cell cycle, viability, apoptosis | H3K27me3, H3K4me3, H3K27ac, H3K9ac, H3K4me1/me2, phH3, FxCycle Violet, Zombie NIR, Active Caspase-3 |
| **Cell Cycle** | Proliferation, cell cycle, DNA content and DNA-damage markers | Ki67, Cyclin D1, PCNA, p53, γH2AX, EdU, DAPI, Hoechst 33342 |
| **Epigenetic** | Chromatin writers/erasers (non-H3-PTM) | KMT2D, p53K372me |
| **Neural** | Neuronal, glial, and neural progenitor markers | PAX6, NEUN, GFAP, OLIG2, SOX10, TBR1, Nestin, SOX2, MAP2, MBP, HuC/HuD |
| **Pericyte** | Pericyte, mural cell, and mesoderm markers | NG2/CSPG4, CD140a/PDGFRa, CD140b/PDGFRb, CD13, RGS5, alpha-SMA, Brachyury/T, FOXF2 |
| **Vascular** | Endothelial, angiogenesis, and vasculogenesis | CD31/PECAM-1, CD144/VE-Cadherin, CD309/VEGFR-2, CD34, EPHB4 |
| **Immune** | PBMC and immune cell markers | CD45, CD3, CD19, CD33, CD56, CD57, CD68, CD14, CD11b |
| **NOTCH** | Notch signaling pathway | NOTCH1, cleaved NOTCH1 (NICD), NOTCH3, DLL4, Jagged1, RBPJ, HER4/ErbB4, EPHB4 |
| **Cardiac** | Cardiomyocyte markers | HOPX, cTnT, NFATc1 |
| **Pluripotent** | Stem cell markers | TRA-1-81, OCT4, SOX2 |
| **Structural** | Cytoskeletal and housekeeping markers | TUJ1/TUBB3, Vimentin, Acetylated Tubulin, beta-Actin, GAPDH |
| **Detection** | Tags, secondaries, fluorescent proteins, streptavidin | FLAG/DYKDDDDK, GFP, mCherry, RFP, secondary antibodies, streptavidin |
| **Phenotype** | Surface markers for cell identity/sorting | CD326/EpCAM, CD184/CXCR4, CD36, HK1, CD166/ALCAM |
| **Fluorescent Protein** | Fluorescent protein reporters with spectral profiles | EGFP/GFP, EYFP/YFP, ECFP/CFP, TagBFP/BFP, EBFP2, TagRFP/RFP, mCherry, tdTomato, mOrange2, DsRed, mKate2 |
| **Control** | Isotype controls | IgG and IgM isotypes in various conjugations |

### Viability options

Five viability reagents are available, each occupying a different detector channel:

| Reagent | Laser | Channel | Notes |
|---------|-------|---------|-------|
| FxCycle Violet | UV 355 | UV5 | DNA content / cell cycle |
| Zombie NIR | Red 640 | R8 | Fixable amine-reactive |
| LIVE/DEAD Fixable Lime 506 | Violet 405 | V5 | Fixable amine-reactive |
| LIVE/DEAD Fixable Violet | Violet 405 | V3 | Fixable amine-reactive |
| BD FVS780 | YG 561 | YG9 | Fixable, PE-Cy7 channel |

---

## Instrument support

### Cytek Aurora 5L (spectral analyzer)

Five lasers (355, 405, 488, 561, 640 nm), 64 detection channels. Channel layout and fluorophore-to-detector mappings derived from the [Thermo Fisher Cytek Aurora Fluorophore Selection Guide](https://www.thermofisher.com/flow) (PSTR-9668644, April 2025).

### BD FACSDiscover S8 (spectral cell sorter)

Five lasers (349, 405, 488, 561, 637 nm), 78 detection channels. The S8 has finer spectral resolution than the Aurora (22 UV channels vs. 16, 20 Violet vs. 16). Mappings derived from the [Thermo Fisher BD S8 Fluorophore Selection Guide](https://www.thermofisher.com/flow) (PSTR-9669173, March 2025).

Switching instruments via the dropdown remaps all fluorochrome-to-channel assignments and updates conflict detection accordingly.

---

## Spectral similarity (measured)

The tool ships with peak-normalized reference signatures for 18 fluorochromes measured on the lab's own Cytek Aurora (serial U1235) from the 18 June 2024 SSP bead library (`spectra/Cytek_Aurora_5L_beads_2024-06-18.json`, derived with `tools/signatures_from_fcs.py` as median(positive) − median(negative) per detector). For any panel whose fluorochromes have measured signatures, the panel area shows the full-array cosine similarity matrix (≥ 0.98 flagged red, 0.90–0.98 amber) and the condition number of the signature matrix. On the same panels, the bead-derived similarities reproduce SpectroFlo's similarity index to within 0.02 (mean difference 0.006 over 14 pairs); the condition number tracks the SpectroFlo Complexity Index (2.2 vs 2.4, 11.6 vs 14.6) without being identical to it. Fluorochromes without a measured signature are marked ~ in the matrix and use the heuristic spread. **Import spectra** accepts a CSV with one row per fluorochrome and one column per detector to add or override signatures for the selected instrument; imports are kept in the browser. Two peak detectors were corrected from the measurements: Vio B515 peaks in B1 (not B2) and mFluor Violet 500 in V7 (not V5) on the Aurora.

---

## Conflict detection

The panel builder checks three levels of compatibility:

1. **Primary detector overlap** — flags when two selected reagents map to the same primary detector channel on the active instrument (hard conflict — cannot be resolved by unmixing).

2. **Fluorochrome reuse** — flags when the same fluorochrome (e.g., PE, AF647) is used on two different markers (hard conflict).

3. **Spectral load (heuristic)** — sums the relative emission intensity of all selected fluorochromes in each detector channel. A channel load above 1.5 (equivalent to ~1.5 bright dyes in the same channel) is flagged as spectrally congested. This is a hand-tuned heuristic, not a quantitative unmixing model. Always validate with single-stained controls.

The **laser balance bar** provides a visual summary of how many conjugated markers are assigned to each laser. An imbalanced panel (e.g., 8 markers on YG but 0 on UV) is harder to unmix and more prone to spreading error.

### Resolving conflicts with alternative conjugates

When a detector overlap or fluorochrome-reuse conflict appears, the tool lists the other inventory entries for the same marker that use a different fluorochrome. Each alternative is shown as a chip with the candidate conjugate and laser badge:

- **Green chips** indicate alternatives that would resolve the conflict without introducing a new detector or fluor clash with the rest of the selected panel.
- **Yellow chips** indicate alternatives that would still conflict with another existing panel member (the chip explains which detector or fluor is at issue).

Clicking any alternative chip swaps the conflicted antibody for that conjugate in a single action. If no different-conjugate inventory exists for a given marker, the tool says so explicitly rather than silently suggesting nothing.

---

## Saving and sharing panels

### On a web server (GitHub Pages, etc.)

Panel configurations are saved to `localStorage` and persist across browser sessions. Name your panel, click **Save**, and it appears in the saved panels list. Click any saved panel to reload it.

### On local file:// URLs

Safari and some browsers block `localStorage` for `file://` URLs. The tool detects this automatically and shows a yellow note. Panels can still be saved in-session (they'll disappear on page reload). Use **Export (JSON)** to download your saved panels as a `.json` file, and **Import** to reload them later. This also lets lab members share panel configurations with each other.

---

## Customization

### Adding new antibodies

Add entries to `clean_antibodies.json` (the single source of truth), then run `python3 tools/build.py` to embed them in `index.html` and `python3 tools/validate.py` to check the result. Each entry needs:

```json
{
  "id": "AB269",
  "marker": "Your Marker",
  "antibody": "Full antibody product name",
  "catNo": "Catalog number",
  "clone": "Clone name or NA",
  "conjugation": "PE",
  "laser": "561-YG1",
  "role": "Brief description",
  "module": "Module Name",
  "locked": false,
  "vendor": "Vendor Name",
  "alternatives": "",
  "zebrafish": "",
  "link": "",
  "species": "human, mouse",
  "dilution": "",
  "epiflowValidated": "",
  "lastOrdered": "",
  "timesOrdered": 0
}
```

`species` (stated reactivity), `dilution` (titrated working dilution for the EpiFlow protocol) and `epiflowValidated` (any non-empty value shows an EpiFlow-validated badge) are shown on the card when filled. `lastOrdered` and `timesOrdered` are filled by `tools/reconcile_orders.py` from the lab ordering sheets. IDs are never reused: a retired entry leaves a gap so saved panels and shared links stay valid.

If the conjugation is a fluorochrome, also add an entry to `CONJ_MAP` mapping the conjugation string to its `FluorPeakByInstrument` key.

### Adding new fluorochromes

1. Add the fluorochrome key to `CONJ_MAP`.
2. Add its primary detector channel to `FluorPeakByInstrument` for each instrument.
3. Add a heuristic spectral spread to `FluorSpectra` with brightness tier (1=Low, 2=Medium, 3=High).

For a conjugate that is spectrally near-identical to one already in the reference set, you can skip steps 2–3 and instead alias it in `CONJ_MAP` to the existing fluorochrome key (e.g., `"VioBlue":"PACIFIC BLUE"`). The card still displays the true conjugate name from the `conjugation` field, while detector placement and conflict logic borrow the analog's channel and spectrum. This is an approximation — note it in the provenance and verify in dedicated spectral software.

### Adding new instruments

Add a new instrument object to `Instruments` with its channel array, then add a corresponding fluorochrome-to-channel map in `FluorPeakByInstrument`. Add the instrument as an `<option>` in the HTML `<select>` dropdown.

---

## Tooling

| Script | Purpose |
|---|---|
| `tools/validate.py` | Integrity checks (inline data equals JSON, ids and catalogs unique, every conjugation resolves, fluor maps complete on both instruments, modules known, core preset conflict-free). Runs in CI on every push via `.github/workflows/validate.yml`. |
| `tools/build.py` | Rebuilds the inline inventory and banner in `index.html` from `clean_antibodies.json`; resyncs `instruments.json`. |
| `tools/reconcile_orders.py` | Two-way match of inventory catalog numbers against the yearly ordering workbooks; writes a Markdown review list of purchased reagents missing from the inventory and inventory entries with no purchase record. |

---

## Data provenance

The antibody inventory was compiled through a systematic audit of all Serrano Lab purchase orders from 2022 through 2026, cross-referenced against vendor catalogs to verify catalog numbers, conjugation assignments, clone identities, and fluorochrome-to-detector mappings. The audit identified and corrected 50+ conjugation field errors, filled 65 missing marker names, removed 25 duplicate entries, and added 5 viability reagents that were ordered but missing from the original dataset.

A subsequent clone-ID audit (May 2026) extracted clone names embedded in product names but missing from the dedicated `clone` field for 41 entries, including all BD-format catalog listings (e.g., `Hu CD3 BUV805 SK7 100Tst` → clone `SK7`), parenthetical clone codes (e.g., `Pax6 Antibody (PAX6/1166)` → clone `PAX6/1166`), Abcam recombinant identifiers (e.g., `[EPR2673]`), and explicit polyclonal labels. The audit also corrected the H3K9ac PE-conjugate clone assignment (`C5B11`, not `C4B11`, per CST cat 28036) and a mislabel of EpCAM as `CD325` (the correct CD designation is `CD326`; CD325 is N-cadherin/CDH2). A full fixes log accompanies the inventory.

A Round-3 verification (Sandeep Sreerama, May 2026) closed out the remaining gaps: manual clone lookups for the vendor entries that could not be resolved from product names (Miltenyi REAfinity, Thermo/Invitrogen secondaries, Proteintech, Sigma, GeneTex), spot-checks of the BD/BioLegend clones whose provenance had not been fully captured, and verified corrections to several conjugation and catalog-number fields where the dataset disagreed with the vendor product page. Notable fixes include six Miltenyi entries mislabeled as `Purified` that are in fact conjugated (e.g., CD31 VioBlue, EPHB4 PE-Vio 770, CD34 APC-Vio 770), a CD36 clone that belonged to a different (FITC) product (`FA6-152`, not `CLB-IVC7`), a secondary mislabeled as Alexa Fluor 647 that is Alexa Fluor Plus 405, and three corrected Miltenyi/BioLegend catalog numbers. The NG2 and Nestin marker labels were unified so the alternative-conjugate feature, which matches on exact marker name, surfaces cross-conjugate suggestions across those families. Clone coverage now stands at **205/221 (93%)**; the 16 remaining blanks are isotype controls, streptavidin conjugates, and one recombinant FLAG ELISA peptide, none of which carry an antibody clone. The full per-field fixes log (`fixes_log.json`, 232 entries across four rounds) and the consolidated review (`CLONE_REVIEW.md`) accompany the inventory.

**Disclaimer — guidance only.** Detector assignments and conflict flags in this tool are spectral heuristics based on emission-peak channels, not measured spillover or a full spectral similarity/complexity analysis. Three conjugates added in this release that are not in the tool's reference fluorochrome set (VioBlue, CoraLite Plus 488, Alexa Fluor Plus 405) are mapped to their nearest spectral analog (Pacific Blue, AF488, AF405 respectively) for channel placement. Users are responsible for confirming spectral compatibility and final panel performance in dedicated spectral panel-design software (e.g., Cytek Full Spectrum Viewer, BD Spectrum Viewer / FACSDiscover software) and with single-stained controls on the target instrument before running samples.

Spectral conflict heuristics and the overall panel-builder architecture are inspired by the [PanelBuildeR](https://github.com/exaexa/panelbuilder) tool by Mirek Kratochvíl (Apache-2.0). The implementation and spectral model here are independent and simplified.

---

## File contents

| File | Description |
|------|-------------|
| `index.html` | Complete self-contained application (HTML + CSS + JS + data) |
| `LICENSE` | BSD 2-Clause license |
| `README.md` | This file |
| `IMPLEMENTATION_GUIDE.md` | Guide for adapting the tool to other core facilities |
| `clean_antibodies.json` | Machine-readable antibody inventory (267 entries; 243 with clone) |
| `instruments.json` | Instrument channel definitions and fluorochrome peak maps |
| `fixes_log.json` | Per-field correction log (168 entries across three audit rounds) |
| `CLONE_REVIEW.md` | Consolidated clone-ID review and verification record |

---

## Contributions & Acknowledgments

The EpiFlow Panel Builder was conceived, directed, and scientifically validated by **M.A. Serrano** (Serrano Lab, CReM, Boston University), who designed the original tool architecture, compiled the antibody inventory from four years of lab purchase orders (2022–2026), defined the Core EpiFlow panel composition and biological module organization, provided domain expertise for all antibody and conjugation corrections, and guided every UX and scientific decision throughout development.

User testing and feature suggestions were provided by **Sandeep Sreerama** (Serrano Lab), whose feedback during in-lab use of the tool surfaced the alternative-conjugate suggestion feature: when a panel has a detector overlap or fluorochrome-reuse conflict, the tool now lists the other inventory entries for the same marker on different fluorochromes and offers a one-click swap. Sandeep also led the Round-3 clone-ID verification (May 2026): manual clone lookups against vendor product pages for the entries that could not be resolved from product names, spot-checks of the BD/BioLegend clones, and verified corrections to conjugation and catalog-number fields, raising clone coverage to 205/221.

Development assistance was provided by **Claude** (Anthropic; Claude Opus 4.7 for the original build, Claude Opus 4.8 for the v1.2 verification-integration pass), an AI assistant that contributed to: programmatic parsing and cross-referencing of 500+ purchase order line items against the builder inventory; identification of conjugation errors, missing markers, duplicate entries, and clone-ID gaps; construction of the BD FACSDiscover S8 instrument model and fluorochrome-to-detector mappings from manufacturer selection guides; fluorescent protein spectral profile research; integration of the Round-3 verification into the inventory and the fluorochrome map; front-end implementation (HTML/CSS/JS) including the alternative-conjugate suggestion feature; and drafting of documentation including this README and the Implementation Guide. All AI-generated content was reviewed, corrected, and validated by M.A. Serrano — notably, several critical data errors (e.g., CoraLite Plus 647 vs. Alexa Fluor 647 distinction, FLAG clone conjugation status, AQP4 mislabeled as isotype control) were caught by human review after the automated audit, underscoring that domain expertise remains essential when working with AI-assisted workflows.

Spectral conflict heuristics and the overall panel-builder concept are inspired by [PanelBuildeR](https://github.com/exaexa/panelbuilder) by Mirek Kratochvíl (Apache-2.0). The implementation is independent.

---

## License

BSD 2-Clause License. Copyright © 2024–2026 M.A. Serrano, Center for Regenerative Medicine (CReM), Chobanian & Avedisian School of Medicine, Boston University.

See [LICENSE](LICENSE) for the full text.

---

## How to cite

A `CITATION.cff` file is included; GitHub shows a "Cite this repository" button from it. Please cite the Zenodo deposit (concept DOI, which always resolves to the latest version) and the EpiFlow method paper (Golden et al., 2025, *Epigenetics Reports*).

---

## Contact

Questions, corrections, or antibody additions: contact the [Serrano Lab](https://github.com/ma-serr) or open an issue in this repository.
