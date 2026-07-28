## ADDED Requirements

### Requirement: Imagen oficial verificada
El catálogo SHALL usar una imagen suiza o, si falta, una imagen oficial alemana del mismo producto comprobado.

#### Scenario: Recuperación desde Alemania
- **WHEN** Suiza no publica una imagen utilizable
- **THEN** se comprueba visualmente la equivalencia alemana antes de incorporarla

### Requirement: Sin mezcla comercial
El uso de una imagen alemana MUST NOT introducir enlaces, SKU ni precios alemanes.

#### Scenario: Tarjeta con imagen alemana
- **WHEN** una tarjeta utiliza ese activo
- **THEN** conserva artículo, CHF, IP y acción suizos
