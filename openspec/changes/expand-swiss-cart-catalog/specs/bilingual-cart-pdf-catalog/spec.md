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
