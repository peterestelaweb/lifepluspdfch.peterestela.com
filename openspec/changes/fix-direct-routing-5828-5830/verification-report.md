# Informe de verificación

Fecha: 2026-08-04

## Alcance

- Auditoría de las 105 tarjetas visibles contra los inventarios suizos actuales `productSet` y `nmp`.
- Comprobación de artículo, precio CHF, IP y tipo de compra.
- Corrección de las rutas de los artículos 5828 y 5830.
- Comprobación responsive en un viewport móvil de 390 × 844 px.

## Resultado local

- 105 de 105 referencias coinciden en artículo, precio CHF, IP y ruta de compra.
- Art. 5828 (`Phase'oMine`): compra directa mediante `https://www.lifeplus.com/SHX4C7/ch/de/product-details/5828`.
- Art. 5830 (`Proanthenol 50mg`): compra directa mediante `https://www.lifeplus.com/SHX4C7/ch/de/product-details/5830`.
- En móvil, la búsqueda devuelve una sola tarjeta para cada referencia y no muestra la instrucción de compra telefónica/cesta.
- OpenSpec valida en modo estricto y el diff no contiene errores de espacios.

## Producción

- Commit funcional desplegado: `d883185464bcfce85f7d29654be6f75295791f88`.
- Ejecución GitHub Actions: `30906363858`, completada correctamente.
- El marcador público confirmó el commit y la ejecución anteriores.
- El SHA-256 del `data/comercio-suiza.json` público coincide con el archivo local auditado: `39e686b98ef0b929d3cdf91fef38c103d6a50ea53db6d750592f28ff74c726d9`.
- La repetición final del validador produjo: `PASS: 105 referencias visibles coinciden en artículo, CHF, IP y ruta; 5828 y 5830 son direct en SHX4C7.`

## Dictamen

La corrección está verificada y lista para aprobación final. Las 105 tarjetas usan artículos, precios, IP y rutas compatibles con el inventario suizo actual. Los artículos 5828 y 5830 ya no se presentan como compra telefónica/cesta y enlazan directamente a la tienda correcta `SHX4C7`.
