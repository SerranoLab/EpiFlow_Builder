# Serrano Lab – Spectral Panel Builder

This is a single‑page web application for building and *spectrally* aware flow cytometry panels, designed around a curated library of >200 antibodies (including “Core EpiFlow” epigenetic reagents, neural, pericyte, endothelial, immune, cardiac, pluripotent, NOTCH, structural, and control modules). 

It helps you:

* **Search** by marker, antibody name, catalog #, conjugation, module, etc.
* **Filter** by module (e.g. *Core EpiFlow, Pericyte, NOTCH, PBMC/Immune, Endothelial, Cerebral/Neural,* etc.).
* **Hide unconjugated / secondary** reagents (Purified, Biotin, HRP, MicroBeads) when you’re building a *strictly fluor-conjugated* panel.
* **Visualize spectral behavior** of each fluor on a **Cytek Aurora 5L** (primary detector + heuristic spread across channels).
* **See mini spectral fingerprints** per antibody (tiny bar‑plot strips grouped by laser family on card hover).
* **Detect conflicts** by:

  * primary detector overlap,
  * re‑using the same fluorochrome,
  * and **spectral “load”** within specific Aurora channels.
* **Get heuristic swap suggestions** when channels are congested.
* **Check relative brightness tiers** for each fluor (3 = very bright, 2 = bright, 1 = moderate/dim).
* **Copy** your selected panel to the clipboard as a text summary (with instrument‑specific laser/detector info).
* **Save** your panel as a `.csv` file for documentation or downstream analysis.



## Features

### 1. Top Banner & Logo

* Gradient banner (dark → light blue) with Serrano Lab logo in a white circular badge.
* Subtitle reminds you this is an instrument‑aware, conflict‑checking panel builder. 

### 2. Large Antibody Library & Modules

* > 200 reagents defined in a single `antibodies` array (IDs `AB001`–`AB235`).
* Each entry includes: `marker`, `antibody`, `clone`, `catNo`, `conjugation`, `laser` (when known), `role`, `module`, and flags for zebrafish usage, alternatives, vendor, and links. 
* A secondary `antibodyPatch` map refines marker names, roles, and modules for many reagents (e.g. distinguishing *pericyte*, *endothelial*, *NOTCH*, *PBMC/Immune*, *structural*, etc.).
* Modules can be composite (e.g. `"Cerebral|Neural|Pericyte|Angiogenesis"`), and module chips are **color‑coded** on each card based on category (neural, pericyte, endothelial, immune, cardiac, pluripotent, structural, flexible, control, phenotype, NOTCH, etc.). 

> Note: Unlike the original 56‑antibody demo, this version is a broad Serrano Lab inventory including intracellular, surface, tags, secondaries, and epigenetic reagents.

### 3. Search, Module Filter & “Hide Unconjugated”

* **Search bar** filters the antibody grid in real time using a combined text haystack (marker, antibody name, catalog #, role, conjugation, module). 
* **Module buttons** (`All`, `Core EpiFlow`, `PBMC`, `Neural`, `Endothelial|Angiogenesis|Vasculogenesis`, `Pericyte|Mesoderm`, `Pluripotent`, `NOTCH`, etc.) filter by module substring.
* **“Hide unconjugated / secondary” checkbox** removes reagents whose conjugation is:

  * *Purified* with no detectable fluor,
  * Biotin, HRP, or MicroBeads,
  * or other clearly non‑fluorescent formats. This is inferred via `isUnconjugated()` and the fluor detection logic. 

### 4. Instrument & Spectral Model (Cytek Aurora 5L)

* Current instrument dropdown: **“Cytek Aurora 5L (5‑laser, spectral)”**.
* Internally, `Instruments.Cytek_Aurora_5L` defines **UV, Violet, Blue, YG, Red** channel IDs and center wavelengths (e.g. `UV1–UV16`, `V1–V16`, `B1–B14`, `YG1–YG10`, `R1–R8`). 
* A `FluorPeak` map associates fluorochromes (e.g. `BUV395`, `BV421`, `Pacific Blue`, `AF488`, `PE`, `PE-Cy7`, `APC`, `AF647`, `AF700`, `APC-Fire 810`) with their **primary detector channel** on Aurora.
* `FluorSpectra` provides a **heuristic per‑channel spread** for each fluor:

  * Rough relative intensities across channels (0–1 range).
  * A brightness flag (`1–3`) indicating dim → bright.

> This is **not** a quantitative unmixing model; it’s a hand‑tuned heuristic to highlight congested channels and suggest safer panel layouts. Always validate with single‑stained controls.

### 5. Per‑Marker Excitation & Spectral Fingerprint Mini‑Plots

For every antibody card:

* The app automatically infers:

  * **Fluor key** from the antibody name + conjugation (`detectFluorKey()`),
  * **Instrument laser & primary detector** from `FluorPeak` + Aurora metadata (`getExcitationAndDetector()`),
  * **Laser badge** (UV, Violet, Blue, YG, Red). 
* On hover, each card shows a compact **spectral fingerprint strip**:

  * Grouped by laser family (UV, V, B, YG, R).
  * Within each group, narrow vertical bars represent the relative emission weight in each channel (e.g. `YG1`, `YG2`, `R2`, etc.).
  * Heights are normalized within the fluor, giving a quick visual sense of where emission is concentrated across the Aurora detector array.

This helps you see, at a glance, which fluor lives in the same detection neighborhood as others.

### 6. Selection, Locked Reagents & Module Badges

* Each antibody appears as a card with an **“Add / Remove”** button in the corner.
* When selected, the card is styled as *selected* and the button toggles to **“Remove”**.
* Support exists for `locked: true` (e.g. “Core EpiFlow” style markers that cannot be removed once selected), though currently all entries are `locked: false`.
* Module badges on each card show color‑coded categories (e.g. *Core EpiFlow*, *Pericyte*, *Endothelial*, *PBMC/Immune*, etc.), with an extra **“Core” pill** when the module includes `Core EpiFlow`. 

### 7. Advanced Conflict & Spectral Load Detection

The **Selected Panel** section now does much more than simple “same laser / same conjugation” warnings:

1. **Primary detector conflicts**

   * Identifies when multiple selected antibodies map to the **same primary Aurora channel** (e.g. both are effectively “YG3”).
   * Reports this as:

     > `Primary detector overlap "YG3": Marker1, Marker2, Marker3`

2. **Fluor reuse conflicts**

   * Detects when the exact same fluor key (e.g. `AF647`, `PE-Cy7`, `BV421`) is reused across different markers.
   * Reported as:

     > `Fluorochrome reuse "AF647": MarkerA, MarkerB`

3. **Laser usage summary**

   * Counts how many selected markers excite off each laser (UV, Violet, Blue, YG, Red) and shows a compact summary (e.g. `UV: 2 | Violet: 5 | YG: 8 | Red: 6`).

4. **Spectral load per channel (heuristic)**

   * Using `FluorSpectra`, the app sums relative intensities for all fluorochromes in each Aurora channel (`computeSpectralLoad()`).
   * A channel with load ≈1 behaves like “one bright dye”; **>1.5** is flagged as **“spectral overload”**. 
   * Overloaded channels are listed, e.g.:

     > `Spectral overload: YG3 (load 2.10), R2 (load 1.70)`

5. **Top‑10 channel mini heatmap**

   * Displays the ~10 most loaded channels as small pill‑shaped cells with intensity‑encoded background (`YG3 2.1`, `R2 1.7`, etc.).
   * Darker pills indicate heavier spectral congestion in that channel.

6. **Brightness summary**

   * Collapses brightness tiers across fluorochromes and lists markers by brightness:

     * `3: H3K27ac [PE], H3K4me3 [AF647], …`
     * `2: NG2 [AF700], …`

7. **Heuristic swap suggestions**

   * For each overloaded channel, the app looks at markers heavily contributing to that channel and checks if the library contains **alternative conjugates for the same marker** that load that channel less.
   * Where alternatives exist, it suggests lines such as:

     > `• Channel YG3: H3K27ac [PE] → consider AF647→main R2; Pacific Blue→main V3`
   * These are purely heuristic and based on library availability + spectral model; they must be checked against biology, clone performance, and reagent availability.

### 8. Selected Panel Summary, Copy & CSV Export

Under **Your Selected Panel**:

* Shows each selected marker as a compact line: `Marker [Conjugation]`, with a small **“x”** remove button (unless locked).
* **Copy to Clipboard**:

  * Copies a text summary that includes:

    * Marker name, conjugation (or fluor key),
    * Instrument label (currently Cytek Aurora 5L),
    * Laser label (e.g. “561 nm (YG)”) and primary detector channel. 
* **Save as CSV**:

  * Downloads `serrano_panel.csv` with columns:
    `Marker, Antibody, Clone, Conjugation, Laser, Detector, Catalog, Role, Module`.
  * Laser and detector fields use the instrument‑aware mapping (not just free text).

### 9. Floating “Click to Rest” Bubble

* A small animated bubble in the bottom‑right corner labeled **“Click to Rest”** opens a separate Serrano Lab game / webpage (`https://serranolab.github.io/GAME_webpage/`) in a new tab.
* This is a fun Easter‑egg / mental break for long panel design sessions. 


## How To Use

1. **Open the HTML File**

   * Open `index2.html` in any modern browser (Chrome, Firefox, Edge, Safari). Everything is self‑contained (HTML, CSS, JS in one file).

2. **Search & Filter**

   * Use the **Search** bar to filter by any text (marker, catalog, vendor, conjugation, role, etc.).
   * Use **module buttons** to restrict the grid to specific biology (e.g. `Core EpiFlow`, `Pericyte`, `PBMC`, `NOTCH`, `Pluripotent`, `Cardiac`).
   * Enable **“Hide unconjugated / secondary”** to view only fluor‑conjugated reagents.

3. **Inspect Antibody Cards**

   * Each card shows marker, full antibody name, clone, conjugation, laser, detector, catalog #, and role.
   * Module chip color gives you context (e.g. Neural vs PBMC vs Endothelial).
   * Hover to view the **mini spectral fingerprint** (strip of channel bars grouped by laser).

4. **Select / Deselect Markers**

   * Click **“Add”** to include an antibody in your panel; it will highlight and the button switches to **“Remove”**.
   * Click **“Remove”** (or the small `x` in the selected list) to deselect.
   * If a reagent is ever marked `locked: true`, the remove button will be disabled.

5. **Check Conflicts & Spectral Load**

   * As you add markers, check the **Selected Panel** section:

     * Detector overlaps
     * Fluor reuse
     * Laser usage summary
     * Spectral load / overload per Aurora channel
     * Brightness tiers
     * Suggested swaps (when available)

6. **Copy or Export**

   * Click **“Copy to Clipboard”** to copy a textual summary (handy for emails, lab notes, or ordering).
   * Click **“Save as CSV”** to download your current panel configuration.



## File Contents

* **HTML**

  * All layout structure (banner, controls, antibody grid, selected panel, footer) plus a floating “Click to Rest” bubble. 

* **CSS (in `<style>` block)**

  * Root color variables for Serrano Lab palette.
  * Card styling, module chip color variants, laser badges, spectral strip styling, and warning/heatmap presentation.

* **JavaScript (in `<script>` block)**

  * `antibodies`: full reagent library.
  * `antibodyPatch`: normalized markers/roles/modules for many entries.
  * **Instrument model** (`Instruments`), **fluor → channel map** (`FluorPeak`), and **heuristic spectra** (`FluorSpectra`).
  * Fluor inference (`detectFluorKey`, `getFluorKey`), laser labeling, and `getExcitationAndDetector()`.
  * Unconjugated detection (`isUnconjugated`).
  * UI state: selected IDs, active module, search query, unconjugated filter.
  * Rendering functions (`renderGrid`, `renderSelected`) and module button generation.
  * Spectral math: `computeSpectralLoad`, `computeBrightnessSummary`, `suggestSwaps`, and the conflict reporter `checkConflicts`.
  * Utility functions for **copy to clipboard** and **CSV export**.


## Customization

1. **Colors & Branding**

   * Edit `:root` in the CSS to adjust `--blue-dark`, `--blue-light`, `--orange-dark`, `--orange-light`, and other neutrals.

2. **Adding / Editing Antibodies**

   * Add new entries to the `antibodies` array.
   * Optionally add/adjust entries in `antibodyPatch` to refine `marker`, `role`, and `module`.

3. **Instrument Models**

   * You can extend `Instruments` with additional cytometers and channel maps.
   * Add corresponding `FluorPeak` / `FluorSpectra` entries (or reuse) and update `instrumentSelect` options in the HTML.

4. **Spectral Heuristics**

   * `FluorSpectra` can be tuned if you have better per‑channel response curves for your specific instrument configuration.
   * Thresholds for “overload” can be changed in `checkConflicts()`.

5. **CSV Format**

   * To add more columns (e.g. `vendor`, `zebrafish`, `link`), extend the `headers` array and row construction in `saveAsCSV()`.




## License & Attribution

* **BSD 2‑Clause License** (see footer in the HTML).
* Spectral conflict ideas and overall architecture are inspired by the **PanelBuildeR** tool by Mirek Kratochvíl (`exaexa/panelbuilder`, Apache‑2.0), but the implementation and spectral heuristics here are independent and simplified. 
* Always validate final panels with **single‑stained controls** on your own instrument configuration.


**Questions or issues?**
Contact the Serrano Lab, or open an issue in the corresponding GitHub repository if the app is hosted there.
