const examples = {
  python: `from librandomizer import random_int

value = random_int()`,
  javascript: `const { randomInt } = require("@librandomizer/javascript");

const value = randomInt();`,
  go: `import "github.com/asparks1987/librandomizer/packages/go"

value := librandomizer.RandomInt()`,
  rust: `use librandomizer::random_int;

let value = random_int();`,
  swift: `import LibRandomizer

let value = LibRandomizer.randomInt()`,
};

const catalogEndpoint = "assets/beta-output-types.json";
const code = document.querySelector("#example-code");
const copyButton = document.querySelector(".copy-button");
const tabs = Array.from(document.querySelectorAll(".tab"));
const catalogRoot = document.querySelector("[data-beta-catalog]");
const catalogSearch = document.querySelector("[data-catalog-search]");
const catalogVisibleCount = document.querySelector("[data-catalog-visible]");
const catalogVisibleCategories = document.querySelector("[data-catalog-visible-categories]");
const catalogTotalCount = document.querySelector("[data-catalog-total]");
const catalogTotalCategories = document.querySelector("[data-catalog-total-categories]");

function normalizeText(value) {
  return String(value || "").toLowerCase();
}

function createPill(label, className) {
  const pill = document.createElement("span");
  pill.className = className;
  pill.textContent = label;
  return pill;
}

function renderCatalogStats(visibleCount, totalCount, categoryCount, activeCategories) {
  if (catalogVisibleCount) {
    catalogVisibleCount.textContent = String(visibleCount);
  }
  if (catalogVisibleCategories) {
    catalogVisibleCategories.textContent = String(activeCategories);
  }
  if (catalogTotalCount) {
    catalogTotalCount.textContent = String(totalCount);
  }
  if (catalogTotalCategories) {
    catalogTotalCategories.textContent = String(categoryCount);
  }
}

function buildCatalogMatch(entry) {
  return [
    entry.id,
    entry.name,
    entry.category,
    entry.api,
    entry.status,
    entry.description,
  ]
    .map(normalizeText)
    .join(" ");
}

function matchesQuery(entry, query) {
  if (!query) {
    return true;
  }

  const fields = buildCatalogMatch(entry);
  return fields.includes(query);
}

function buildCatalogCard(entry) {
  const article = document.createElement("article");
  article.className = `catalog-type status-${entry.status}`;

  const header = document.createElement("div");
  header.className = "catalog-type-header";

  const title = document.createElement("div");
  title.className = "catalog-type-title";

  const name = document.createElement("h4");
  name.textContent = entry.name;

  const api = document.createElement("code");
  api.textContent = entry.api;

  title.append(name, api);
  header.append(title, createPill(entry.status.replace(/-/g, " "), `catalog-status ${entry.status}`));

  const meta = document.createElement("div");
  meta.className = "catalog-type-meta";
  const id = document.createElement("span");
  id.textContent = entry.id;
  const category = document.createElement("span");
  category.textContent = entry.category;
  meta.append(id, category);

  const description = document.createElement("p");
  description.textContent = entry.description;

  article.append(header, meta, description);
  return article;
}

function buildCatalogSection(category, entries, openDefault) {
  const details = document.createElement("details");
  details.open = openDefault;

  const summary = document.createElement("summary");
  summary.append(document.createTextNode(category));
  summary.append(createPill(String(entries.length), "catalog-count"));

  const list = document.createElement("div");
  list.className = "catalog-types";
  entries.forEach((entry) => {
    list.append(buildCatalogCard(entry));
  });

  details.append(summary, list);
  return details;
}

function renderCatalog(catalog, queryValue) {
  const query = normalizeText(queryValue).trim();
  const filtered = catalog.types.filter((entry) => matchesQuery(entry, query));
  const totalCount = catalog.types.length;
  const totalCategories = new Set(catalog.types.map((entry) => entry.category)).size;
  const visibleCategories = new Set(filtered.map((entry) => entry.category)).size;

  renderCatalogStats(filtered.length, totalCount, totalCategories, visibleCategories);

  catalogRoot.replaceChildren();

  if (!filtered.length) {
    const emptyState = document.createElement("p");
    emptyState.className = "catalog-loading";
    emptyState.textContent = "No output types match that search.";
    catalogRoot.append(emptyState);
    return;
  }

  const grouped = filtered.reduce((accumulator, entry) => {
    if (!accumulator.has(entry.category)) {
      accumulator.set(entry.category, []);
    }
    accumulator.get(entry.category).push(entry);
    return accumulator;
  }, new Map());

  let first = true;
  for (const [category, entries] of grouped.entries()) {
    catalogRoot.append(buildCatalogSection(category, entries, first));
    first = false;
  }
}

async function loadCatalog() {
  if (!catalogRoot) {
    return;
  }

  try {
    const response = await fetch(catalogEndpoint);
    if (!response.ok) {
      throw new Error(`Unable to load beta catalog (${response.status})`);
    }

    const catalog = await response.json();
    renderCatalog(catalog, catalogSearch ? catalogSearch.value : "");

    if (catalogSearch) {
      catalogSearch.addEventListener("input", () => {
        renderCatalog(catalog, catalogSearch.value);
      });
    }
  } catch (error) {
    catalogRoot.replaceChildren();
    const message = document.createElement("p");
    message.className = "catalog-loading";
    message.textContent =
      "The beta catalog could not be loaded right now. Serve the docs site over HTTP to enable the live list.";
    catalogRoot.append(message);
    console.error(error);
  }
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    code.textContent = examples[tab.dataset.language];
    copyButton.textContent = "Copy";
  });
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(code.textContent);
    copyButton.textContent = "Copied";
  } catch {
    copyButton.textContent = "Select";
  }
});

loadCatalog();
