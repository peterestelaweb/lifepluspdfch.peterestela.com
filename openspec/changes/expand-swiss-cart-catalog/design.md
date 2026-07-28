## Context

El catálogo bilingüe conserva PDFs con SKU documentales que no siempre coinciden con el artículo comercial suizo. La tienda ofrece productos mediante ficha pública y otros únicamente desde el buscador de la cesta.

## Goals / Non-Goals

**Goals:**
- Mantener una capa comercial suiza separada de los archivos PDF.
- Resolver artículo, CHF, IP y acción de compra para cada equivalencia confirmada.
- Conservar PDFs ES/DE e imágenes oficiales sin eliminar documentación histórica.

**Non-Goals:**
- No crear traducciones propias presentadas como PDFs oficiales.
- No enlazar catálogos generales ni fichas de otros mercados como compra suiza.

## Decisions

- `catalogo-bilingue` seguirá describiendo documentos y `comercio-suiza` describirá el artículo comercial.
- La acción será `direct`, `cart` o `phone`; `cart` abrirá la cesta de Jessica e indicará el código exacto.
- Las equivalencias ambiguas quedarán fuera hasta comprobar el SKU.
- Las imágenes seguirán la prioridad Suiza, Alemania para el mismo producto verificado y consulta a la usuaria si no hay equivalencia segura.

## Risks / Trade-offs

- [Dos SKU para un producto] → deduplicar por artículo suizo conservando todos los PDFs internamente.
- [Producto retirado] → ocultar su acción comercial sin borrar el documento.
- [Cesta sin parámetro de búsqueda] → mostrar instrucciones visibles junto al botón.

## Migration Plan

Regenerar comercio, validar enlaces y PDFs, probar escritorio/móvil, desplegar por FTPS y comprobar marcadores y datos públicos. El rollback será el commit previo.

## Open Questions

Las fichas sin código suizo inequívoco seguirán pendientes de confirmación.
