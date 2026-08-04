## 1. Corrección de datos

- [x] 1.1 Eliminar las excepciones telefónicas de 5828 y 5830 en el generador
- [x] 1.2 Regenerar comercio-suiza.json y comercio-suiza.js desde el inventario suizo actual
- [x] 1.3 Confirmar que 5828 y 5830 tienen purchase direct y URL SHX4C7

## 2. Prevención de regresiones

- [x] 2.1 Añadir una validación automatizada de las 105 tarjetas contra productSet y nmp
- [x] 2.2 Añadir aserciones específicas de ruta directa para 5828 y 5830
- [x] 2.3 Reforzar la verificación pública del workflow para ambos artículos

## 3. Verificación completa

- [x] 3.1 Ejecutar validadores locales y OpenSpec strict
- [x] 3.2 Comprobar búsqueda y rutas en viewport móvil
- [x] 3.3 Revisar el diff y preservar los archivos no relacionados del usuario

## 4. Despliegue y producción

- [ ] 4.1 Crear commit y desplegar por el workflow FTP cautivo
- [ ] 4.2 Confirmar el commit en deploy-marker.txt y los datos corregidos en producción
- [ ] 4.3 Repetir la auditoría pública y documentar el dictamen final
