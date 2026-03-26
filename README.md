# Serrano Lab – EpiFlow Panel Builder

A single-page web application for designing spectrally aware flow cytometry panels, built around a curated inventory of 221 reagents from the Serrano Lab at Boston University's Center for Regenerative Medicine (CReM).

**[Live tool →](https://serranolab.github.io/EpiFlow_Builder/)** *(update URL after deployment)*

---

## What it does

The EpiFlow Panel Builder helps you select antibodies and reagents for multi-parameter spectral flow cytometry panels. Unlike spectral viewers such as FluoroFinder, this tool operates one step earlier in the workflow: it helps you decide **which reagents to pull from the lab inventory** before you sit down at the instrument, catching detector conflicts and spectral overload before you waste cells and time.

The tool is organized around the **Core EpiFlow panel** — an 11-marker configuration for multiparametric histone H3 post-translational modification (H3-PTM) profiling — with interchangeable biology modules (Neural, Pericyte, Endothelial, Cardiac, Immune, NOTCH, etc.) that can be layered on top.

### Key capabilities

- **Search and filter** 210 reagents by marker, antibody name, catalog number, conjugation, module, or role.
- **Module filtering** with count badges showing how many conjugated reagents each module contains (Core EpiFlow, Cerebral/Neural, Pericyte, Endothelial, PBMC/Immune, NOTCH, Cardiac, Pluripotent, and more).
- **One-click Core Panel loading** pre-selects the canonical 11-marker EpiFlow panel: FxCycle Violet (DNA), Zombie NIR (viability), total H3-AF700, H3K27me3-Pacific Blue, H3K4me3-AF647, H3K27ac-PE-Cy7, H3K9ac-Pacific Blue, H3K4me1-PE, H3K4me2-PE, phH3-AF532, Active Caspase-3-BV650.
- **Dual instrument support** for Cytek Aurora 5L (64 channels) and BD FACSDiscover S8 (78 channels), with per-instrument fluorochrome-to-channel mapping derived from official Thermo Fisher selection guides.
- **Conflict detection**: primary detector overlap, fluorochrome reuse, and heuristic spectral load per Aurora/S8 channel.
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

1. Click **Load Core Panel** to pre-select the 11-marker Core EpiFlow configuration.
2. Use the **module buttons** to filter by biology (e.g., click "Neural" to see cerebral/neural reagents).
3. Click **Add** on any card to include it in your panel. The conflict checker updates in real time.
4. Check the **laser balance bar** — aim for reasonable distribution across all 5 lasers.
5. If conflicts appear (red warnings), look for alternative conjugates of the same marker in the grid.
6. **Copy to Clipboard** or **Save as CSV** to export your final panel.
7. **Save Panel** to store your configuration by name for future sessions.

---

## Reagent inventory

The 210-entry inventory was compiled from Serrano Lab purchase orders spanning 2022–2026 and includes reagents from Cell Signaling Technology, BD Biosciences, BioLegend, R&D Systems, Miltenyi Biotec, Abcam, Thermo Fisher/Invitrogen, Novus Biologicals, Proteintech, and other vendors.

### Modules

| Module | Description | Examples |
|--------|-------------|----------|
| **Core EpiFlow** | H3-PTM profiling, cell cycle, viability, apoptosis | H3K27me3, H3K4me3, H3K27ac, H3K9ac, H3K4me1/me2, phH3, FxCycle Violet, Zombie NIR, Active Caspase-3 |
| **Cell Cycle** | Proliferation and cell cycle markers | Ki67, Cyclin D1, PCNA, p53 |
| **Epigenetic** | Chromatin writers/erasers (non-H3-PTM) | KMT2D, p53K372me |
| **Neural** | Neuronal, glial, and neural progenitor markers | PAX6, NEUN, GFAP, OLIG2, SOX10, TBR1, Nestin, SOX2, MAP2, MBP, HuC/HuD |
| **Pericyte** | Pericyte, mural cell, and mesoderm markers | NG2/CSPG4, CD140a/PDGFRa, CD140b/PDGFRb, CD13, RGS5, alpha-SMA, Brachyury/T, FOXF2 |
| **Vascular** | Endothelial, angiogenesis, and vasculogenesis | CD31/PECAM-1, CD144/VE-Cadherin, CD309/VEGFR-2, CD34, EPHB4 |
| **Immune** | PBMC and immune cell markers | CD45, CD3, CD19, CD33, CD56, CD57, CD68, CD14, CD11b |
| **NOTCH** | Notch signaling pathway | NOTCH1, NOTCH3, DLL4, Jagged1, HER4/ErbB4, EPHB4 |
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

## Conflict detection

The panel builder checks three levels of compatibility:

1. **Primary detector overlap** — flags when two selected reagents map to the same primary detector channel on the active instrument (hard conflict — cannot be resolved by unmixing).

2. **Fluorochrome reuse** — flags when the same fluorochrome (e.g., PE, AF647) is used on two different markers (hard conflict).

3. **Spectral load (heuristic)** — sums the relative emission intensity of all selected fluorochromes in each detector channel. A channel load above 1.5 (equivalent to ~1.5 bright dyes in the same channel) is flagged as spectrally congested. This is a hand-tuned heuristic, not a quantitative unmixing model. Always validate with single-stained controls.

The **laser balance bar** provides a visual summary of how many conjugated markers are assigned to each laser. An imbalanced panel (e.g., 8 markers on YG but 0 on UV) is harder to unmix and more prone to spreading error.

---

## Saving and sharing panels

### On a web server (GitHub Pages, etc.)

Panel configurations are saved to `localStorage` and persist across browser sessions. Name your panel, click **Save**, and it appears in the saved panels list. Click any saved panel to reload it.

### On local file:// URLs

Safari and some browsers block `localStorage` for `file://` URLs. The tool detects this automatically and shows a yellow note. Panels can still be saved in-session (they'll disappear on page reload). Use **Export (JSON)** to download your saved panels as a `.json` file, and **Import** to reload them later. This also lets lab members share panel configurations with each other.

---

## Customization

### Adding new antibodies

Add entries to the `antibodies` array in the `<script>` block. Each entry needs:

```json
{
  "id": "AB211",
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
  "link": ""
}
```

If the conjugation is a fluorochrome, also add an entry to `CONJ_MAP` mapping the conjugation string to its `FluorPeakByInstrument` key.

### Adding new fluorochromes

1. Add the fluorochrome key to `CONJ_MAP`.
2. Add its primary detector channel to `FluorPeakByInstrument` for each instrument.
3. Add a heuristic spectral spread to `FluorSpectra` with brightness tier (1=Low, 2=Medium, 3=High).

### Adding new instruments

Add a new instrument object to `Instruments` with its channel array, then add a corresponding fluorochrome-to-channel map in `FluorPeakByInstrument`. Add the instrument as an `<option>` in the HTML `<select>` dropdown.

---

## Data provenance

The antibody inventory was compiled through a systematic audit of all Serrano Lab purchase orders from 2022 through 2026, cross-referenced against vendor catalogs to verify catalog numbers, conjugation assignments, clone identities, and fluorochrome-to-detector mappings. The audit identified and corrected 50+ conjugation field errors, filled 65 missing marker names, removed 25 duplicate entries, and added 5 viability reagents that were ordered but missing from the original dataset.

Spectral conflict heuristics and the overall panel-builder architecture are inspired by the [PanelBuildeR](https://github.com/exaexa/panelbuilder) tool by Mirek Kratochvíl (Apache-2.0). The implementation and spectral model here are independent and simplified.

---

## File contents

| File | Description |
|------|-------------|
| `index.html` | Complete self-contained application (HTML + CSS + JS + data) |
| `LICENSE` | BSD 2-Clause license |
| `README.md` | This file |
| `IMPLEMENTATION_GUIDE.md` | Guide for adapting the tool to other core facilities |
| `clean_antibodies.json` | Machine-readable antibody inventory (221 entries) |
| `instruments.json` | Instrument channel definitions and fluorochrome peak maps |

---

## Contributions & Acknowledgments

The EpiFlow Panel Builder was conceived, directed, and scientifically validated by **M.A. Serrano** (Serrano Lab, CReM, Boston University), who designed the original tool architecture, compiled the antibody inventory from four years of lab purchase orders (2022–2026), defined the Core EpiFlow panel composition and biological module organization, provided domain expertise for all antibody and conjugation corrections, and guided every UX and scientific decision throughout development.

Development assistance was provided by **Claude** (Anthropic, claude-opus-4-6), an AI assistant that contributed to: programmatic parsing and cross-referencing of 500+ purchase order line items against the builder inventory; identification of conjugation errors, missing markers, and duplicate entries; construction of the BD FACSDiscover S8 instrument model and fluorochrome-to-detector mappings from manufacturer selection guides; fluorescent protein spectral profile research; front-end implementation (HTML/CSS/JS); and drafting of documentation including this README and the Implementation Guide. All AI-generated content was reviewed, corrected, and validated by M.A. Serrano — notably, several critical data errors (e.g., CoraLite Plus 647 vs. Alexa Fluor 647 distinction, FLAG clone conjugation status, AQP4 mislabeled as isotype control) were caught by human review after the automated audit, underscoring that domain expertise remains essential when working with AI-assisted workflows.

Spectral conflict heuristics and the overall panel-builder concept are inspired by [PanelBuildeR](https://github.com/exaexa/panelbuilder) by Mirek Kratochvíl (Apache-2.0). The implementation is independent.

---

## License

BSD 2-Clause License. Copyright © 2024–2026 M.A. Serrano, Center for Regenerative Medicine (CReM), Chobanian & Avedisian School of Medicine, Boston University.

See [LICENSE](LICENSE) for the full text.

---

## Contact

Questions, corrections, or antibody additions: contact the [Serrano Lab](https://github.com/ma-serr) or open an issue in this repository.
