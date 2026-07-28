## ADDED Requirements

### Requirement: Tres métodos de compra verificables
Cada tarjeta comercial SHALL usar exactamente una acción `direct`, `cart` o `phone` basada en la disponibilidad suiza comprobada.

#### Scenario: Producto con ficha
- **WHEN** existe una ficha comprable en `SHX4C7/ch/de`
- **THEN** el botón abre esa ficha concreta

#### Scenario: Producto de cesta
- **WHEN** el artículo solo aparece en la búsqueda de cesta
- **THEN** el botón abre la cesta y la tarjeta indica el SKU que debe buscarse

#### Scenario: Producto telefónico
- **WHEN** no existe una vía de compra web comprobada
- **THEN** el botón utiliza `tel:0800321026` e indica artículo y Shop-ID
