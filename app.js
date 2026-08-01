const state = { products: [], query: "", language: "both" };
const commerce = window.LIFEPLUS_COMMERCE || { products: {} };
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
  if (product.commercial_only) return state.language === "both";
  if (state.language === "es") return Boolean(product.spanish);
  if (state.language === "de") return Boolean(product.german);
  return Boolean(product.spanish || product.german);
}

function getVisible() {
  const words = normalize(state.query).split(" ").filter(Boolean);
  const seenArticles = new Set();
  return state.products
    .filter(product => {
      const sale = commerce.products[product.sku];
      const searchable = `${product.search} ${normalize(sale?.article)}`;
      return sale && matchesFilter(product) && words.every(word => searchable.includes(word));
    })
    .sort((a, b) => (a.category || "General").localeCompare(b.category || "General", "es", { sensitivity: "base" }) || a.title.localeCompare(b.title, "es", { sensitivity: "base" }))
    .filter(product => {
      const article = commerce.products[product.sku].article;
      if (seenArticles.has(article)) return false;
      seenArticles.add(article);
      return true;
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
    : product.commercial_only
      ? `<div class="product-image pack-image" aria-hidden="true"><span>PACK</span><b>Lifeplus</b></div>`
      : `<div class="product-image" aria-hidden="true"></div>`;
  const esAction = product.spanish && state.language !== "de"
    ? `<a class="pdf-link" href="${encodeURI(product.spanish)}" target="_blank" rel="noopener">Ficha en español · ES</a>`
    : "";
  const deAction = product.german && state.language !== "es"
    ? `<a class="pdf-link de" href="${encodeURI(product.german)}" target="_blank" rel="noopener">Datenblatt · DE</a>`
    : "";
  const sale = commerce.products[product.sku];
  const shopAction = sale.purchase === "direct"
    ? `<a class="shop-link" href="${sale.url}" target="_blank" rel="noopener" aria-label="${escapeHTML(product.title)} kaufen · Comprar ${escapeHTML(product.title)}">Comprar producto · Produkt kaufen <span aria-hidden="true">↗</span></a>`
    : sale.purchase === "cart"
      ? `<a class="shop-link" href="${sale.url}" target="_blank" rel="noopener">Comprar desde la cesta · Über den Warenkorb kaufen <span aria-hidden="true">↗</span></a><p class="phone-note">En la cesta, busca el Art. ${escapeHTML(sale.article)} y pulsa “In den Warenkorb”.</p>`
      : `<a class="shop-link phone" href="${commerce.phone_href}">Llamar para pedir · Zum Bestellen anrufen</a><p class="phone-note">Comunica el Art. ${escapeHTML(sale.article)} y la Shop-ID ${escapeHTML(commerce.shop_id)} al operador.</p>`;
  return `<article class="product" style="animation-delay:${Math.min(index, 8) * 35}ms">
    ${image}
    <div class="product-info">
      <div class="product-meta"><b>Lifeplus</b><span>Art. ${escapeHTML(sale.article)}</span></div>
      <h2>${escapeHTML(product.title)}</h2>
      <p class="product-description">${escapeHTML(product.description)}</p>
      ${product.note ? `<p class="document-note">${escapeHTML(product.note)}</p>` : ""}
      ${product.commercial_only ? `<p class="pack-note">Pack comercial sin ficha PDF propia · Verkaufspaket ohne eigenes PDF</p>` : ""}
      <div class="product-price"><strong>CHF ${escapeHTML(sale.price_chf)}</strong><span>IP ${escapeHTML(sale.ip)}</span></div>
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
  state.products = [...(data?.products || []), ...(commerce.standalone_products || [])];
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
