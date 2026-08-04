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

Pendiente de completar tras el despliegue: commit, ejecución, marcador público y repetición de la auditoría sobre los archivos publicados.
