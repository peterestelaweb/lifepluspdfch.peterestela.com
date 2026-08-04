## Why

La auditoría completa de producción del 4 de agosto de 2026 confirmó que los artículos suizos `5828` y `5830` tienen fichas públicas comprables en la tienda `SHX4C7`, pero la web PDF Suiza todavía los presenta como pedido telefónico. Esta clasificación obliga a la persona usuaria a abandonar una ruta directa que funciona y fue el error observado desde móvil.

## What Changes

- Eliminar las excepciones telefónicas de `5828` y `5830` en el generador comercial suizo.
- Regenerar los datos JSON y JavaScript para que ambos artículos usen compra directa.
- Añadir validaciones que impidan volver a clasificar como teléfono una referencia con ficha pública comprobada.
- Verificar las 105 tarjetas públicas, la experiencia móvil, la Shop-ID `SHX4C7` y el despliegue real mediante marcador público.

## Capabilities

### New Capabilities

- `audited-direct-purchase-routing`: Enrutamiento de compra derivado del inventario suizo actual, con pruebas de regresión y verificación pública por referencia.

### Modified Capabilities

Ninguna. El cambio anterior todavía no está archivado como especificación base; el comportamiento reforzado queda definido íntegramente en la nueva capacidad auditable.

## Impact

Afecta a `scripts/generar_comercio_suiza.py`, `data/comercio-suiza.json`, `data/comercio-suiza.js`, validadores, documentación, workflow de despliegue y la web pública `lifepluspdfch.peterestela.com`.
