## Purpose

Garantiza que cada tarjeta del catálogo PDF Suiza use la vía de compra que demuestra el inventario actual de Lifeplus y que las rutas directas sigan perteneciendo a la tienda `SHX4C7`.

## ADDED Requirements

### Requirement: La ficha pública prevalece sobre el pedido telefónico
El sistema SHALL publicar una referencia como compra directa cuando el inventario suizo exponga una ficha pública comprable para ese artículo.

#### Scenario: Artículo presente en productSet
- **WHEN** una referencia aparece en el inventario público suizo `productSet`
- **THEN** su tarjeta enlaza a `/SHX4C7/ch/de/product-details/<artículo>` y no muestra pedido telefónico

#### Scenario: Referencias 5828 y 5830
- **WHEN** se generan las tarjetas de `5828` y `5830`
- **THEN** ambas ofrecen compra directa en la tienda `SHX4C7`

### Requirement: El producto de cesta conserva la búsqueda por código
El sistema SHALL dirigir a la cesta `SHX4C7` los artículos disponibles únicamente en el inventario secundario suizo.

#### Scenario: Artículo presente solo en nmp
- **WHEN** una referencia aparece en `nmp` pero no en `productSet`
- **THEN** su tarjeta abre la cesta e indica el código exacto que se debe buscar

### Requirement: Auditoría completa antes del despliegue
El sistema MUST verificar todas las tarjetas visibles contra el inventario suizo actual y MUST rechazar discrepancias de artículo, precio, IP o tipo de compra.

#### Scenario: Validación sin discrepancias
- **WHEN** se valida una versión candidata
- **THEN** cada tarjeta visible coincide en artículo, precio CHF, IP y ruta con la fuente suiza

#### Scenario: Verificación móvil
- **WHEN** se busca una referencia desde un viewport móvil
- **THEN** la tarjeta resultante conserva la ruta de compra correcta y la Shop-ID `SHX4C7`

### Requirement: Producción verificable
El despliegue MUST publicar un marcador con el commit y MUST demostrar en la URL pública que los datos corregidos están activos.

#### Scenario: Despliegue aceptado
- **WHEN** termina el workflow de producción
- **THEN** `deploy-marker.txt` contiene el commit desplegado y los datos públicos clasifican `5828` y `5830` como `direct`
