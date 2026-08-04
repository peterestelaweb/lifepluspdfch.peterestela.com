## Context

El generador obtiene `productSet` y `nmp` de Lifeplus Suiza. La lógica normal ya considera directo todo artículo de `productSet`, pero `PHONE_OVERRIDES = {"5828", "5830"}` anulaba esa evidencia. La página consume copias JSON y JavaScript del mismo payload, y se despliega por FTPS cautivo mediante GitHub Actions.

## Goals / Non-Goals

**Goals:**

- Derivar la ruta de compra de la fuente suiza sin excepciones obsoletas.
- Probar explícitamente las dos referencias afectadas y las 105 tarjetas públicas.
- Confirmar la versión desplegada mediante el marcador y los datos públicos.

**Non-Goals:**

- Cambiar nombres, precios, IP, PDFs o imágenes que ya coinciden.
- Modificar la web histórica `lifepluspdf.peterestela.com`.
- Añadir productos nuevos fuera del catálogo actual.

## Decisions

1. Eliminar `PHONE_OVERRIDES` en lugar de sustituir sus valores. `productSet` es la fuente autoritativa para ficha directa; conservar excepciones manuales permitiría que el error reapareciera.
2. Regenerar ambos formatos (`comercio-suiza.json` y `.js`) desde un único payload para que servidor y apertura local permanezcan idénticos.
3. Añadir una validación local independiente que compare cada tarjeta generada con `productSet`/`nmp`, además de aserciones específicas para `5828` y `5830`.
4. Mantener el despliegue FTP existente, reforzando la verificación pública para buscar `"purchase": "direct"` junto a ambos artículos y comprobar `deploy-marker.txt`.

## Risks / Trade-offs

- [Lifeplus cambia el inventario entre generación y prueba] → descargar una sola fuente para cada ejecución y registrar la fecha de auditoría.
- [Una sesión de navegador sustituye la tienda por otra anterior] → validar enlaces y móvil en una sesión limpia, y comprobar que producción publica literalmente `SHX4C7`.
- [Workflow verde pero raíz pública antigua] → exigir que el marcador público contenga el commit actual y que el JSON público contenga las rutas corregidas.

## Migration Plan

1. Eliminar las excepciones y regenerar datos.
2. Ejecutar validaciones de datos, interfaz y móvil.
3. Confirmar diff limitado, crear commit y enviar a `main`.
4. Esperar el workflow y verificar marcador, HTML y JSON públicos.
5. Si falla producción, revertir el commit y no declarar finalizada la corrección.
