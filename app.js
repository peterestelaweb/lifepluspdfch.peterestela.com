const state = { products: [], query: "", filter: "all" };
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
  if (state.filter === "both") return product.spanish && product.german;
  if (state.filter === "es") return Boolean(product.spanish);
  if (state.filter === "de") return Boolean(product.german);
  return true;
}

function getVisible() {
  const words = normalize(state.query).split(" ").filter(Boolean);
  return state.products.filter(product =>
    matchesFilter(product) && words.every(word => product.search.includes(word))
  );
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
  const deAction = product.german
    ? `<a class="pdf-link de" href="${encodeURI(product.german)}" target="_blank" rel="noopener">Datenblatt · DE</a>`
    : `<span class="unavailable">DE no disponible</span>`;
  return `<article class="product" style="animation-delay:${Math.min(index, 8) * 35}ms">
    ${image}
    <div class="product-info">
      <div class="product-meta"><b>Lifeplus</b>${product.sku ? `<span>Art. ${escapeHTML(product.sku)}</span>` : ""}</div>
      <h2>${escapeHTML(product.title)}</h2>
      <p class="product-description">${escapeHTML(product.description)}</p>
      <div class="actions">
        <a class="pdf-link" href="${encodeURI(product.spanish)}" target="_blank" rel="noopener">Ficha en español · ES</a>
        ${deAction}
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
  document.querySelector(".filter.active")?.classList.remove("active");
  button.classList.add("active");
  state.filter = button.dataset.filter;
  render();
}));

fetch("data/catalogo-bilingue.json")
  .then(response => { if (!response.ok) throw new Error("No se pudo cargar el catálogo"); return response.json(); })
  .then(data => { state.products = data.products || []; render(); })
  .catch(() => { count.textContent = "No se pudo cargar el catálogo"; empty.hidden = false; });
