/***********************************************
 * Example data subset. Replace with your full 56 entries.
 * Each antibody has:
 * - id (unique for front-end)
 * - marker
 * - antibody
 * - catNo (catalog)
 * - clone
 * - conjugation
 * - laser
 * - role
 * - module
 * - locked (true if core, false otherwise)
 ***********************************************/
const antibodies = [
  {
    id: 1,
    marker: "DNA content",
    antibody: "FxCycle™ Violet Ready Flow™ Reagent",
    catNo: "R37166",
    clone: "NA",
    conjugation: "Violet",
    laser: "355-UV7",
    role: "Cell cycle Profile",
    module: "Core EpiFlow",
    locked: true
  },
  {
    id: 3,
    marker: "H3K27me3",
    antibody: "Tri-Methyl-Histone H3 (Pacific Blue™)",
    catNo: "89120",
    clone: "C36B11",
    conjugation: "Pacific Blue",
    laser: "405-V3",
    role: "Repressive mark",
    module: "Core EpiFlow",
    locked: true
  },
  {
    id: 13,
    marker: "Dead",
    antibody: "Zombie NIR (BioLegend #423106)",
    catNo: "423106",
    clone: "NA",
    conjugation: "Zombie Red??",
    laser: "640-R6",
    role: "Live/Dead",
    module: "Core EpiFlow",
    locked: true
  },
  {
    id: 14,
    marker: "NG2",
    antibody: "BD OptiBuild™ BUV496 Mouse Anti-Human NG2",
    catNo: "756711",
    clone: "7.1",
    conjugation: "BUV496",
    laser: "355-UV7",
    role: "Pericyte marker",
    module: "Pericyte",
    locked: false
  },
  {
    id: 19,
    marker: "HK1",
    antibody: "BD Horizon™ BUV661 Rabbit Anti-Human HK1",
    catNo: "570557",
    clone: "EPR10134(B)",
    conjugation: "BUV661",
    laser: "355-UV11",
    role: "Glucose Metabolism",
    module: "Phenotype",
    locked: false
  }
];

/***********************************************
 * Global references to DOM elements
 ***********************************************/
const searchInput = document.getElementById("searchInput");
const moduleSelect = document.getElementById("moduleSelect");
const antibodyList = document.getElementById("antibodyList");
const selectedList = document.getElementById("selectedList");
const warningContainer = document.getElementById("warningContainer");

const copyButton = document.getElementById("copyButton");
const saveButton = document.getElementById("saveButton");
const alertBox = document.getElementById("alert");

/***********************************************
 * State data
 ***********************************************/
// Which antibodies are currently "selected" in the side panel?
let selectedIds = new Set(); // store ID numbers

/***********************************************
 * On load, initialize the UI
 ***********************************************/
document.addEventListener("DOMContentLoaded", () => {
  // 1) Populate the module dropdown
  populateModuleDropdown();

  // 2) Render the full antibody list initially
  renderAntibodyList();

  // 3) Attach event listeners
  searchInput.addEventListener("input", renderAntibodyList);
  moduleSelect.addEventListener("change", renderAntibodyList);

  copyButton.addEventListener("click", copyPanelToClipboard);
  saveButton.addEventListener("click", savePanelAsJSON);
});

/***********************************************
 * Functions
 ***********************************************/

/**
 * Creates a unique list of modules, then populates the dropdown
 */
function populateModuleDropdown() {
  // Gather all modules from the data
  const modules = antibodies.map((ab) => ab.module);
  // Unique
  const uniqueModules = ["All Modules", ...new Set(modules)];

  // Populate the <select>
  uniqueModules.forEach((m) => {
    const option = document.createElement("option");
    option.value = m;
    option.textContent = m;
    moduleSelect.appendChild(option);
  });
}

/**
 * Renders the main antibody list based on search + filter
 */
function renderAntibodyList() {
  antibodyList.innerHTML = ""; // clear old

  const searchTerm = searchInput.value.toLowerCase().trim();
  const selectedModule = moduleSelect.value;

  // Filter the array
  let filtered = antibodies.filter((ab) => {
    // filter by module?
    if (selectedModule !== "All Modules" && ab.module !== selectedModule) {
      return false;
    }
    // search check across marker, catNo, role, antibody
    const haystack = (
      ab.marker +
      ab.antibody +
      ab.catNo +
      ab.role
    ).toLowerCase();
    if (!haystack.includes(searchTerm)) {
      return false;
    }
    return true;
  });

  // For each filtered antibody, build a "card"
  filtered.forEach((ab) => {
    const card = document.createElement("div");
    card.className = "ab-card";

    // top row: checkbox + marker
    const header = document.createElement("div");
    header.className = "ab-header";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "ab-checkbox";
    checkbox.checked = selectedIds.has(ab.id);
    checkbox.disabled = ab.locked; // if it's core, lock it on
    checkbox.addEventListener("change", () => toggleSelected(ab.id));

    const markerSpan = document.createElement("span");
    markerSpan.className = "ab-marker";
    markerSpan.textContent = ab.marker;

    header.appendChild(checkbox);
    header.appendChild(markerSpan);

    card.appendChild(header);

    // module label
    const moduleLabel = document.createElement("span");
    moduleLabel.className = "ab-module";
    if (ab.module.includes("Core EpiFlow")) {
      moduleLabel.classList.add("core-epiflow");
    }
    moduleLabel.textContent = ab.module;
    card.appendChild(moduleLabel);

    // detail lines
    const details = document.createElement("div");
    details.className = "ab-details";
    details.innerHTML = `
      <div><strong>Clone:</strong> ${ab.clone}</div>
      <div><strong>Conjugation:</strong> ${ab.conjugation}</div>
      <div><strong>Laser:</strong> ${ab.laser}</div>
      <div><strong>Role:</strong> ${ab.role}</div>
      <div><strong>Catalog #:</strong> ${ab.catNo}</div>
    `;
    card.appendChild(details);

    // add to the list
    antibodyList.appendChild(card);
  });
}

/**
 * Toggle the "selected" state of an antibody by id
 */
function toggleSelected(id) {
  if (selectedIds.has(id)) {
    // user unchecked => remove from selected
    selectedIds.delete(id);
  } else {
    // user checked => add
    selectedIds.add(id);
  }
  // re-draw the side panel
  renderSelectedList();
}

/**
 * Builds the side-panel listing of selected items
 * Also checks for conflicts
 */
function renderSelectedList() {
  selectedList.innerHTML = "";

  // Gather the actual antibody objects for the selected IDs
  const selectedAb = antibodies.filter((ab) => selectedIds.has(ab.id));

  selectedAb.forEach((ab) => {
    const item = document.createElement("div");
    item.className = "selected-item";

    // Marker + (maybe module or conjugation)
    item.textContent = `${ab.marker} [${ab.conjugation}]`;
    // Remove button
    const removeBtn = document.createElement("button");
    removeBtn.className = "remove-btn";
    removeBtn.textContent = "x";
    removeBtn.title = "Remove from Panel";
    removeBtn.addEventListener("click", () => {
      // uncheck
      selectedIds.delete(ab.id);
      // re-render
      renderAntibodyList();
      renderSelectedList();
    });

    item.appendChild(removeBtn);
    selectedList.appendChild(item);
  });

  // Now check for conflicts
  checkConflicts(selectedAb);
}

/**
 * Check if multiple selected items share the same laser OR the same conjugation.
 * If conflict found, show a warning in the side panel.
 */
function checkConflicts(selectedArray) {
  warningContainer.innerHTML = ""; // clear old

  // Group by laser
  const laserMap = {};
  // Group by conjugation
  const conjMap = {};

  selectedArray.forEach((ab) => {
    if (!laserMap[ab.laser]) laserMap[ab.laser] = [];
    laserMap[ab.laser].push(ab);

    if (!conjMap[ab.conjugation]) conjMap[ab.conjugation] = [];
    conjMap[ab.conjugation].push(ab);
  });

  let messages = [];

  // Check for laser collisions
  Object.keys(laserMap).forEach((l) => {
    if (laserMap[l].length > 1) {
      const markers = laserMap[l].map((x) => x.marker).join(", ");
      messages.push(`Detector conflict on "${l}" => [${markers}]`);
    }
  });

  // Check for conjugation collisions
  Object.keys(conjMap).forEach((c) => {
    if (conjMap[c].length > 1) {
      const markers = conjMap[c].map((x) => x.marker).join(", ");
      messages.push(`Conjugate conflict "${c}" => [${markers}]`);
    }
  });

  // Render them
  if (messages.length > 0) {
    messages.forEach((msg) => {
      const p = document.createElement("p");
      p.className = "warning";
      p.textContent = msg;
      warningContainer.appendChild(p);
    });
  }
}

/**
 * Copy the final panel (selected items) to clipboard as text
 */
function copyPanelToClipboard() {
  const selectedAb = antibodies.filter((ab) => selectedIds.has(ab.id));
  if (selectedAb.length === 0) return;

  // build a textual summary
  let text = "Serrano Lab – Selected Panel:\n";
  selectedAb.forEach((ab) => {
    text += `- ${ab.marker} [${ab.conjugation}] (Laser: ${ab.laser})\n`;
  });

  navigator.clipboard
    .writeText(text)
    .then(() => {
      showAlert();
    })
    .catch((err) => {
      console.error("Clipboard copy failed", err);
    });
}

/**
 * Download the final panel as a JSON file
 */
function savePanelAsJSON() {
  const selectedAb = antibodies.filter((ab) => selectedIds.has(ab.id));
  if (selectedAb.length === 0) return;

  // Turn to JSON
  const jsonStr = JSON.stringify(selectedAb, null, 2);
  const blob = new Blob([jsonStr], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  // Create a temporary link and auto-click
  const link = document.createElement("a");
  link.href = url;
  link.download = "serrano_lab_panel.json";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Shows the “Copied to clipboard” alert briefly
 */
function showAlert() {
  alertBox.classList.add("show");
  setTimeout(() => {
    alertBox.classList.remove("show");
  }, 2000);
}
