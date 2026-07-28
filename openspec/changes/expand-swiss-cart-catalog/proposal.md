## Why

La tienda suiza publica menos fichas de producto que artículos comprables desde su cesta. El catálogo bilingüe de PDFs debe mostrar también esas equivalencias suizas y ofrecer una acción honesta de ficha, cesta o teléfono sin eliminar las fichas documentales existentes.

## What Changes

- Cruzar los PDFs ES/DE con artículos confirmados tanto en el catálogo público como en el inventario secundario de la cesta.
- Mostrar artículo suizo, CHF, IP y uno de tres métodos: ficha directa, cesta con búsqueda por código o llamada.
- Conservar internamente los PDFs aunque una equivalencia comercial deje de publicarse.
- Incorporar imágenes oficiales suizas y recurrir a Alemania solo para el mismo producto verificado.
- Validar buscador, filtros, PDFs, imágenes, enlaces, teléfono y despliegue público en escritorio y móvil.

## Capabilities

### New Capabilities

- `bilingual-cart-pdf-catalog`: Relación entre documentación bilingüe y artículos suizos visibles o disponibles por cesta.
- `verified-purchase-routing`: Enrutamiento verificable a ficha, cesta o llamada sin enlaces generales engañosos.
- `cross-market-official-images`: Uso controlado de imágenes alemanas cuando Suiza no publique la imagen.

### Modified Capabilities


## Impact

Afecta a los generadores de catálogo y comercio, datos JSON/JS, `app.js`, estilos, activos de producto, verificadores Playwright y workflow FTPS de `lifepluspdfch.peterestela.com`.
