# Serrano Lab – Spectral Panel Builder

This is a single‐page web application designed for building and visualizing spectral flow cytometry panels. It uses a set of 56 antibodies (some of which are “Core EpiFlow,” locked in place and always selected) and allows you to:

- **Search** for antibodies by marker name, catalog #, conjugation, module, etc.
- **Filter** by module (e.g. “Core EpiFlow,” “Pericyte,” “Notch,” “PBMC,” etc.).
- **Add / remove** antibodies from your panel.
- **Check** for conflicts if multiple selected antibodies share the same laser or conjugation.
- **Copy** your selected panel to the clipboard as a text summary.
- **Save** your panel as a `.csv` file for data management or documentation.

---

## Features

1. **Top Banner & Logo**  
   The banner has a gradient from dark blue to light blue. The lab logo is placed within a white circular background to enhance visibility.

2. **Core EpiFlow Markers**  
   Some antibodies are `locked: true`, meaning they are always included in the selected panel and cannot be removed.

3. **Search Bar**  
   A text input that filters the antibody list in real time. It matches text against:
   - Marker
   - Antibody name
   - Catalog number
   - Conjugation
   - Role
   - Module

4. **Module Filter Buttons**  
   Each antibody has a “module” field (sometimes multiple). The filter buttons (e.g. “Core EpiFlow,” “Phenotype,” “NOTCH,” etc.) let you quickly show or hide antibodies from specific modules.

5. **Conflict Detection**  
   If more than one selected antibody uses the same `laser` or the same `conjugation`, a warning is shown in a red‐tinted box. This helps prevent incompatible or overlapping fluorophores.

6. **Copy to Clipboard**  
   Clicking **“Copy to Clipboard”** creates a text summary of the currently selected panel (marker + conjugation + laser). A small toast message confirms the copy action.

7. **Save as CSV**  
   Clicking **“Save as CSV”** exports the currently selected list of antibodies to a `.csv` file. Columns include: Marker, Antibody, Clone, Conjugation, Laser, Catalog #, Role, and Module.

---

## How To Use

1. **Open the HTML File**  
   Simply open the HTML file in any modern web browser (Chrome, Firefox, Edge, Safari, etc.). Everything is self‐contained (HTML, CSS, JS all in one file).

2. **Search & Filter**  
   - Type in the “Search” bar to filter by text.  
   - Click on module buttons (like “All,” “Core EpiFlow,” “PBMC,” etc.) to filter by module.

3. **Select / Deselect Markers**  
   - Each antibody is displayed in a “card.”  
   - Click **“Add”** to select an antibody.  
   - Click **“Remove”** to deselect it.  
   - “Locked” antibodies (core) are always selected (the **“Remove”** button is disabled).

4. **Check Conflicts**  
   - As soon as you select multiple markers, the app checks for shared lasers or conjugations.  
   - If any conflicts exist, they appear in the red box under “Your Selected Panel.”

5. **Copy to Clipboard**  
   - Under “Your Selected Panel,” click **“Copy to Clipboard.”**  
   - A toast near the bottom confirms once the data has been copied.

6. **Save as CSV**  
   - Also under “Your Selected Panel,” click **“Save as CSV.”**  
   - Your browser will prompt to download `serrano_panel.csv`.

---

## File Contents

- **HTML**: Contains the structure and the entire JavaScript logic embedded in `<script>` tags. Also includes the CSS styles in a `<style>` block.
- **CSS**: Embedded within the HTML under `:root { … }` and subsequent style sections, referencing Serrano Lab brand colors.
- **JavaScript**:  
  - Defines the full `antibodies` array of 56 items (with fields like `id`, `marker`, `antibody`, `laser`, `module`, `locked`, etc.).  
  - Implements searching, filtering, conflict checking, and CSV export.

---

## Customization

1. **Adjusting Colors**  
   - In the `:root` section, you can tweak the values for `--blue-dark`, `--blue-light`, `--orange-dark`, `--orange-light` to match your preference.

2. **Changing “locked” Items**  
   - If you don’t want an antibody to be mandatory, set `locked: false`.

3. **Export Format**  
   - Currently exports to `.csv` in `saveAsCSV()`. You could adapt it to other formats if desired.

4. **Additional Fields**  
   - If you want more columns in your CSV, add them to the `headers` array and ensure you push the corresponding data into each row.

---

## Browser Compatibility

- Tested on recent versions of Chrome, Firefox, and Edge.  
- Should work in any ES6‐capable browser since it relies on standard JavaScript methods (like `Array.filter`, `Blob`, `fetch`, etc.).

---

## License

This code is intended for internal use in Serrano Lab. If you wish to distribute or modify it for other labs, please retain credits and disclaimers as relevant.

---


**Questions or issues?**  
Contact the Serrano Lab for support or open an issue on the relevant GitHub repository if it’s hosted there.
