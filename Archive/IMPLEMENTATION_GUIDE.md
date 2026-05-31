# EpiFlow Panel Builder — Implementation Guide for Flow Cytometry Core Facilities

**Version 1.0 · March 2026**
**M.A. Serrano, Center for Regenerative Medicine (CReM), Boston University**

---

## Purpose

This guide is intended for research groups who want to adapt the EpiFlow Panel Builder for use with their own spectral flow cytometry instruments and antibody inventories. It is designed to be used **in collaboration with your local flow cytometry core director or spectral expert**, who will have instrument-specific knowledge that is critical for panel success.

The EpiFlow Panel Builder is a pre-experiment planning tool — it helps you decide what to put in a tube before you sit at the instrument. It does **not** replace single-stain validation, instrument-specific unmixing libraries, or the expertise of your core facility team. This guide outlines the collaborative workflow for getting from a digital panel design to a validated, reproducible assay.

---

## Part 1: Before You Start — Meeting with the Core Director

### Why this meeting matters

The panel builder uses heuristic spectral models that approximate fluorochrome behavior. Your core director has empirical knowledge of how specific dyes actually perform on the specific instrument in your facility — including quirks, autofluorescence backgrounds, and known problematic combinations that no heuristic model can fully capture. Schedule a 30-minute meeting before your first experiment.

### Agenda for the initial meeting

Bring a printout or screenshot of your proposed panel (the builder's "Copy to Clipboard" output works well for this). Discuss the following:

**1. Instrument configuration and reference library**

- Which instrument will you use? (Cytek Aurora, BD S8, other)
- Is the instrument running the latest firmware and reference library?
- Does the facility maintain a shared single-stain reference library, or do you need to build your own?
- How often is the instrument QC'd (daily CS&T / SpectroFlo Daily QC)?
- Are there known channels with high background or noise on this specific instrument?

**2. Known problematic signatures**

Ask specifically about:

- **Fluorescent proteins**: EGFP, mCherry, and tdTomato have broad emission spectra that spread into multiple channels. Autofluorescence from culture media or fixation artifacts can mimic FP signals. The core director may have experience with which FPs unmix cleanly and which cause problems on their specific instrument.
- **Tandem dyes (PE-Cy7, APC-Cy7, PE-Cy5.5)**: These can degrade over time, with the tandem breaking down and creating a "donor-only" population that bleeds into the parent dye channel. The core may have preferred lots or alternative tandems.
- **Fixation effects on dyes**: BV421, BV605, and some BUV dyes can change spectral signatures after fixation. If your protocol includes fixation/permeabilization (required for intracellular H3-PTM staining in EpiFlow), discuss which dyes are stable post-fix.
- **Viability dyes with fixation**: Zombie NIR, Fixable Violet, and Fixable Lime must be applied before fixation. FxCycle Violet (DNA stain) is added after. Mixing these up is a common error.
- **UV dyes (BUV series)**: Brilliant Stain Buffer (BD #659611 or #563794) is required when using two or more Brilliant dyes in the same panel to prevent polymer interaction artifacts.
- **Autofluorescence**: iPSC-derived cells, organoid dissociates, and primary neurons often have high intrinsic autofluorescence in the FITC/GFP channel (B2). The core director can advise whether autofluorescence extraction is available and effective on their instrument.

**3. Controls strategy**

Agree on a controls plan before you run anything. The core should define what they expect, but here is a starting framework:

---

## Part 2: Controls — The Non-Negotiable Foundation

### Minimum controls for every experiment

| Control | Purpose | Notes |
|---------|---------|-------|
| **Unstained cells** | Defines autofluorescence baseline | Must be the same cell type as your experimental samples. iPSCs, organoid dissociates, and PBMCs all have different autofluorescence profiles. |
| **Single-stain references** | Builds the unmixing matrix | One tube per fluorochrome in the panel. Use compensation beads for antibodies; use cells for FxCycle, Zombie NIR, and fluorescent proteins. |
| **Viability stain only** | Validates live/dead discrimination | Especially important for fixation protocols. Include a heat-killed or ethanol-permeabilized positive control. |
| **FMO (Fluorescence Minus One)** | Defines positive/negative gating boundaries | One FMO per marker where the positive/negative boundary is ambiguous. Not needed for clearly bimodal markers (e.g., CD45, viability). Essential for continuous markers (H3-PTMs, transcription factors). |
| **Isotype controls** | Context-specific; discuss with core | For intracellular staining (H3-PTMs), isotypes matched to species/isotype/conjugation are recommended. For surface markers, FMOs are generally preferred over isotypes. |

### Controls specific to EpiFlow (H3-PTM panels)

The Core EpiFlow panel involves intracellular staining of histone modifications, which requires fixation and permeabilization. This introduces specific considerations:

- **FxCycle Violet** is a DNA intercalator added **after** fixation/permeabilization. It does not require live cells. Single-stain control: fixed cells + FxCycle Violet only.
- **Zombie NIR** is an amine-reactive viability dye applied **before** fixation. Single-stain control: mix of live and heat-killed cells + Zombie NIR only (no fixation needed for the control, but note the spectral signature may shift slightly post-fix — validate).
- **H3-PTM antibodies** (PE, Pacific Blue, AF647, AF700, PE-Cy7, AF532 conjugates) should use **single-stain cells** rather than beads, because histone modification levels vary by cell state and the signal dynamic range on cells differs from beads. Alternatively, the core may accept beads for initial unmixing with a cell-based verification.
- **Total H3** (AF700) serves as a normalization control — the ratio of each H3-PTM to total H3 is more meaningful than raw MFI. Discuss with the core how to implement this in their analysis pipeline.

### Controls for fluorescent protein panels

- **Single-color FP controls**: Must be actual FP-expressing cells, not beads. Beads cannot replicate the spectral signature of an intracellular fluorescent protein, which is influenced by cellular autofluorescence, protein folding, and maturation state.
- **Non-fluorescent parental cells**: Same cell line without the FP, cultured and prepared identically. This is critical because culture-induced autofluorescence (e.g., from phenol red, riboflavin, or tryptophan metabolites) can confound FP detection.
- **Mixed populations**: A 1:1 mix of FP-positive and FP-negative cells is extremely useful for validating that the unmixing correctly separates the populations. This is more informative than running them in separate tubes.

---

## Part 3: Panel Validation Workflow

### Step 1: Digital panel design (EpiFlow Panel Builder)

Use the builder to select your markers, check for detector overlaps, and verify laser balance. Export your panel as CSV for documentation.

### Step 2: Core director review

Share the panel with the core director. Discuss any flagged conflicts, tandem dye concerns, and autofluorescence expectations. The core may suggest swapping specific conjugates based on their empirical experience (e.g., "PE-Cy7 degrades in our hands — use PE-Vio 770 instead").

### Step 3: Single-stain reference acquisition

Run all single-stain controls on the target instrument. The core director should evaluate:

- Does each fluorochrome produce a clean, well-resolved spectral signature?
- Are there any unexpected spectral features (e.g., degraded tandems, fixation-induced shifts)?
- Is the autofluorescence extraction from the unstained control working properly?

### Step 4: Full panel pilot

Run the complete panel on a small number of samples (2-3 tubes) with all controls. Evaluate:

- **Unmixing quality**: Check each parameter for unmixing artifacts (negative populations, spreading, residual spillover). The core director can assess the condition number of the spectral matrix.
- **Sensitivity**: Can you resolve the biological populations of interest? For H3-PTMs, can you distinguish the expected range of modification levels (e.g., H3K27me3-high in progenitors vs. H3K27me3-low in differentiated neurons)?
- **Reproducibility**: If possible, run two replicates to check consistency.

### Step 5: Documentation

Record the following for each validated panel:

- Instrument name and software version
- Reference library used (date created, fluorochrome list)
- Antibody lot numbers and expiration dates
- Staining protocol (including fixation/permeabilization timing)
- Gating strategy
- Any known limitations or caveats

---

## Part 4: Adapting the Builder for Your Facility

### Adding your own antibody inventory

The EpiFlow Panel Builder ships with the Serrano Lab's 220-reagent inventory. To adapt it for another facility:

1. **Export your inventory** from your LIMS, ordering system, or spreadsheet. You need: marker name, antibody product name, clone, catalog number, conjugation, vendor.
2. **Assign fluorochrome-to-detector mappings** based on your instrument's configuration. The builder includes Cytek Aurora 5L and BD FACSDiscover S8 mappings from official Thermo Fisher selection guides, but your instrument may have a custom filter configuration.
3. **Organize into modules** that reflect your research focus. The default modules (Core EpiFlow, Neural, Pericyte, Vascular, Immune, etc.) reflect the Serrano Lab's research program. A hematology core might reorganize around modules like "T-cell panel," "B-cell panel," "Myeloid panel," "HSC panel."
4. **Validate detector assignments** with your core director. The heuristic spectral model is approximate — your director may know that certain dyes perform differently on your specific instrument configuration.

### Adding new instruments

The builder supports multiple instruments via the `Instruments` and `FluorPeakByInstrument` data structures. To add a new instrument:

1. Define all detection channels (ID, laser wavelength, center wavelength)
2. Map each fluorochrome to its primary detection channel on that instrument
3. Add the instrument as a dropdown option

Consult the manufacturer's fluorophore selection guide for your instrument. Thermo Fisher publishes these for most spectral cytometers.

---

## Part 5: Common Pitfalls and Troubleshooting

### Panel design pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| **Too many markers on one laser** | Poor unmixing, high spreading error | Use the laser balance bar; aim for roughly equal distribution across lasers |
| **Bright dye on low-abundance marker** | Wastes dynamic range; increases spread into neighboring channels | Match dye brightness to antigen abundance (bright dyes for rare markers, dim dyes for abundant markers) |
| **Tandem dye degradation** | Creates false-positive population in parent dye channel | Use fresh lots; protect from light; consider non-tandem alternatives |
| **Skipping FMO controls** | Cannot set accurate gates for continuous markers | Run FMOs for every H3-PTM and transcription factor |
| **Using beads for FP reference** | Wrong spectral signature for unmixing | Always use FP-expressing cells for fluorescent protein references |
| **Mixing viability dye timing** | Amine-reactive dyes fail after fixation; DNA stains fail before | Apply Zombie/Fixable dyes before fix; apply FxCycle/DAPI after fix |
| **Forgetting Brilliant Stain Buffer** | BUV/BV polymer dyes interact, creating artifactual staining | Required when using 2+ Brilliant dyes; add to staining buffer |
| **Not accounting for autofluorescence** | False positives in GFP/FITC channel | Run unstained control of same cell type; enable autofluorescence extraction |

### Fluorescent protein-specific pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| **GFP + AF488 antibody** | Both detected in B2 channel; cannot separate | Use antibodies on different channels when working with GFP lines |
| **tdTomato + PE antibody** | Both in YG1; tdTomato is very bright and will dominate | Choose AF594 or PE-CF594 conjugates instead of PE |
| **mCherry + PE-eFluor 610** | Both in YG3 | Use AF647 or APC conjugates for the antibody |
| **BFP/CFP overlap with viability dyes** | TagBFP in V3 conflicts with Fixable Violet; CFP in V4 conflicts with BV480 | Choose viability dyes on other channels (Zombie NIR on R8, FxCycle on UV) |
| **FP maturation variability** | Spectral signature shifts with protein folding state | Allow sufficient expression time (24-48h for most FPs); validate with freshly transduced cells |
| **FP photobleaching during sort** | Signal drops over long sort runs (>1h) | Minimize laser exposure time; discuss sort parameters with core |

### iPSC and organoid-specific considerations

- **High autofluorescence**: iPSC-derived cells, especially after differentiation, often have elevated autofluorescence in the 500-600 nm range. This primarily affects the B2 (GFP/FITC) and B3-B4 channels. Consider avoiding dim dyes in these channels.
- **Cell dissociation effects**: Organoid dissociation protocols (Accutase, TrypLE, papain) can cleave surface epitopes. Validate that your surface markers survive dissociation. Intracellular markers (H3-PTMs, transcription factors) are not affected.
- **Dead cell percentage**: Dissociated organoids often have 20-40% dead cells. Robust viability gating is essential. Consider using two viability markers on different channels for stringent dead-cell exclusion.
- **Doublet discrimination**: Large organoid fragments can form doublets. Use FSC-H vs. FSC-A (and SSC-H vs. SSC-A) gating. Spectral unmixing does not resolve doublets.
- **Fixation timing**: For intracellular H3-PTM panels, cells must be fixed and permeabilized. The protocol (methanol vs. formaldehyde/saponin) affects antibody accessibility and spectral properties. Methanol fixation is standard for histone modifications but can reduce surface marker signal — discuss the order of staining (surface first, then fix, then intracellular) with the core.

---

## Part 6: Implementation Checklist

Use this checklist when setting up the EpiFlow Panel Builder for a new facility or experiment:

### Pre-experiment (1-2 weeks before)

- [ ] Meet with core director to review proposed panel
- [ ] Discuss known problematic dyes/combinations on the target instrument
- [ ] Agree on controls strategy (unstained, single-stains, FMOs, isotypes)
- [ ] Verify antibody lot numbers and expiration dates
- [ ] Order any missing reagents (Brilliant Stain Buffer, compensation beads, viability dyes)
- [ ] Confirm instrument availability and booking

### Panel design

- [ ] Use the EpiFlow Panel Builder to select markers and check conflicts
- [ ] Verify laser balance (no more than ~40% of markers on any single laser)
- [ ] Export panel as CSV for documentation
- [ ] Review alternative conjugates for any flagged conflicts

### Controls preparation

- [ ] Prepare single-stain controls for each fluorochrome
- [ ] Prepare unstained control (same cell type, same preparation)
- [ ] Prepare viability control (live + dead mix)
- [ ] Prepare FMO controls for continuous markers
- [ ] Prepare FP-expressing cells (if applicable) for FP single-stain references

### Instrument day

- [ ] Confirm daily QC passed
- [ ] Run unstained control first to assess autofluorescence
- [ ] Run single-stains and verify spectral signatures
- [ ] Run full panel pilot on 2-3 samples
- [ ] Evaluate unmixing quality with core director
- [ ] Document any adjustments to gating or unmixing

### Post-experiment

- [ ] Save panel configuration in EpiFlow Builder (Save Panel + Export JSON)
- [ ] Record lot numbers, instrument settings, and gating strategy
- [ ] Share validated panel configuration with lab members (JSON export)
- [ ] Report any problematic signatures to core director for their reference library

---

## Part 7: Recommended Reading

1. **Spectral flow cytometry best practices**: Novo et al. (2024) "Guidelines for the generation, execution, analysis, and reporting of high-dimensional flow cytometry data." *European Journal of Immunology*.
2. **Panel design principles**: Maecker et al. (2012) "Standardizing immunophenotyping for the Human Immunology Project." *Nature Reviews Immunology*.
3. **Fluorescent proteins for flow cytometry**: Telford et al. (2012) "Flow cytometry of fluorescent proteins." *Methods* 57:318-330.
4. **Spectral unmixing fundamentals**: Nolan & Condello (2013) "Spectral flow cytometry." *Current Protocols in Cytometry* 63:1.27.1-1.27.13.
5. **EpiFlow methodology**: Golden et al. (2025) "EpiFlow: spectral flow cytometry for multiparametric histone H3 post-translational modification profiling." *Epigenetics Reports*.

---

## Contact

Questions about this guide or the EpiFlow Panel Builder: contact the [Serrano Lab](https://github.com/ma-serr) or the CReM Flow Cytometry team at Boston University.

---

*BSD 2-Clause License. Copyright © 2024-2026 M.A. Serrano, Center for Regenerative Medicine (CReM), Chobanian & Avedisian School of Medicine, Boston University.*
