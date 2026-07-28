const state = { products: [], query: "", language: "both" };
const LIFEPLUS_SHOP_BASE = "https://www.lifeplus.com/SHX4C7/ch/de/product-details/";
// Product numbers in the PDFs do not always match the current Swiss catalogue.
// Only verified, purchasable Swiss product numbers belong in this map.
const SWISS_SHOP_SKUS = {
  "1021": "1021", "170": "6695", "2629": "2629", "2630": "2630",
  "2631": "2631", "2632": "2632", "3415": "5828", "3443": "5825",
  "3446": "5827", "4033": "5821", "4095": "5871", "4129": "4129",
  "4130": "4130", "4131": "4131", "4132": "4132", "4133": "4133",
  "4134": "4134", "4144": "4144", "4173": "4173", "4174": "4174",
  "4998": "5049", "6108": "5826", "6112": "5823", "6134": "6134",
  "6140": "5834", "6192": "5829", "6237": "5822", "6618": "5413",
  "6648": "5869", "6651": "5870", "6654": "6654", "6656": "5874",
  "6658": "5875", "6673": "5879", "6678": "5884", "6679": "5885",
  "6687": "5887", "6688": "5888", "6689": "5889", "6692": "5390",
  "6697": "5894", "6698": "5895", "6699": "5896", "6861": "4000",
  "7796": "4655", "7797": "4656"
};
const input = document.querySelector("#searchInput");
const results = document.querySelector("#results");
const count = document.querySelector("#resultCount");
const empty = document.querySelector("#emptyState");
const clearButton = document.querySelector("#clearSearch");

function normalize(value) {
  return String(value || "").toLowerCase().normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, " ").trim();
}

function matchesFilter(product) {
  if (state.language === "es") return Boolean(product.spanish);
  if (state.language === "de") return Boolean(product.german);
  return Boolean(product.spanish || product.german);
}

function getVisible() {
  const words = normalize(state.query).split(" ").filter(Boolean);
  return state.products
    .filter(product =>
      matchesFilter(product) && words.every(word => product.search.includes(word))
    )
    .sort((a, b) => {
      const purchaseDifference = Number(Boolean(SWISS_SHOP_SKUS[b.sku])) - Number(Boolean(SWISS_SHOP_SKUS[a.sku]));
      return purchaseDifference || a.title.localeCompare(b.title, "es", { sensitivity: "base" });
    });
}

function escapeHTML(value) {
  return String(value).replace(/[&<>'"]/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[char]);
}

function card(product, index) {
  const image = product.image
    ? `<div class="product-image"><img src="${encodeURI(product.image)}" alt="${escapeHTML(product.title)}" loading="lazy"></div>`
    : `<div class="product-image" aria-hidden="true"></div>`;
  const esAction = product.spanish && state.language !== "de"
    ? `<a class="pdf-link" href="${encodeURI(product.spanish)}" target="_blank" rel="noopener">Ficha en español · ES</a>`
    : "";
  const deAction = product.german && state.language !== "es"
    ? `<a class="pdf-link de" href="${encodeURI(product.german)}" target="_blank" rel="noopener">Datenblatt · DE</a>`
    : "";
  const shopSku = SWISS_SHOP_SKUS[product.sku];
  const shopAction = shopSku
    ? `<a class="shop-link" href="${LIFEPLUS_SHOP_BASE}${encodeURIComponent(shopSku)}" target="_blank" rel="noopener" aria-label="${escapeHTML(product.title)} kaufen · Comprar ${escapeHTML(product.title)}">Comprar producto · Produkt kaufen <span aria-hidden="true">↗</span></a>`
    : `<span class="shop-unavailable">Producto no disponible para comprar en la tienda · Produkt derzeit nicht im Shop erhältlich</span>`;
  return `<article class="product" style="animation-delay:${Math.min(index, 8) * 35}ms">
    ${image}
    <div class="product-info">
      <div class="product-meta"><b>Lifeplus</b>${product.sku ? `<span>Art. ${escapeHTML(product.sku)}</span>` : ""}</div>
      <h2>${escapeHTML(product.title)}</h2>
      <p class="product-description">${escapeHTML(product.description)}</p>
      <div class="actions">
        ${esAction}
        ${deAction}
        ${shopAction}
      </div>
    </div>
  </article>`;
}

function render() {
  const visible = getVisible();
  results.innerHTML = visible.map(card).join("");
  count.textContent = `${visible.length} ${visible.length === 1 ? "producto" : "productos"}`;
  empty.hidden = visible.length !== 0;
  clearButton.classList.toggle("visible", Boolean(state.query));
}

input.addEventListener("input", event => { state.query = event.target.value; render(); });
document.querySelector("#searchForm").addEventListener("submit", event => event.preventDefault());
clearButton.addEventListener("click", () => { input.value = ""; state.query = ""; input.focus(); render(); });
document.querySelectorAll(".filter").forEach(button => button.addEventListener("click", () => {
  const activeButton = document.querySelector(".filter.active");
  activeButton?.classList.remove("active");
  activeButton?.setAttribute("aria-pressed", "false");
  button.classList.add("active");
  button.setAttribute("aria-pressed", "true");
  state.language = button.dataset.language;
  render();
}));

function loadCatalog(data) {
  state.products = data?.products || [];
  render();
}

if (window.LIFEPLUS_CATALOG) {
  loadCatalog(window.LIFEPLUS_CATALOG);
} else {
  fetch("data/catalogo-bilingue.json")
    .then(response => { if (!response.ok) throw new Error("No se pudo cargar el catálogo"); return response.json(); })
    .then(loadCatalog)
    .catch(() => { count.textContent = "No se pudo cargar el catálogo"; empty.hidden = false; });
}
