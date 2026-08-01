## ADDED Requirements

### Requirement: Relación de PDF y artículo suizo
El sistema SHALL relacionar cada PDF publicado con un artículo suizo confirmado sin sustituir el SKU documental dentro del archivo.

#### Scenario: Equivalencia confirmada
- **WHEN** un PDF ES o DE corresponde inequívocamente a un SKU suizo
- **THEN** la tarjeta muestra los documentos disponibles y los datos comerciales suizos

### Requirement: Conservación documental
El sistema MUST conservar internamente los PDFs aunque el producto deje de tener una acción comercial publicable.

#### Scenario: Producto retirado
- **WHEN** desaparece la disponibilidad comercial
- **THEN** el documento no se elimina del archivo interno

### Requirement: Ficha oficial de otro mercado
El catálogo SHALL permitir asociar una ficha oficial alemana con un SKU documental distinto cuando la equivalencia del producto esté comprobada y no exista una ficha estadounidense equivalente.

#### Scenario: Lycopin Plus Alemania
- **WHEN** la ficha española usa el artículo 3457 y la ficha alemana oficial usa el artículo 5509
- **THEN** la tarjeta enlaza ambos documentos intactos, mantiene el artículo comercial suizo 5509 e informa de que no existe ficha equivalente en Estados Unidos
