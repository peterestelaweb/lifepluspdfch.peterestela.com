# Biblioteca bilingüe de fichas Lifeplus

- `es/`: copia íntegra de los PDFs del catálogo fuente de `lifepluspdf.peterestela.com`.
- `de/`: fichas oficiales en alemán obtenidas desde la tienda de Estados Unidos.
- `registro_bilingue.csv`: relación por número de artículo entre el archivo español y el alemán.

La ruta oficial alemana comprobada sigue el patrón:

`https://ww2.lifeplus.com/media/pdf/piSheets/US/{SKU}-PI_DE.pdf`

Para reconstruir o actualizar la biblioteca:

```bash
python3 scripts/crear_biblioteca_bilingue.py
```

Después, para actualizar el buscador de la página bilingüe:

```bash
python3 scripts/generar_catalogo_web.py
```
