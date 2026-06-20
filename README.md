## ✅ Arquitectura ETL

El proyecto sigue un enfoque modular:

- **Extract**: Lectura de datos desde CSV (Netflix dataset)
- **Transform**: Limpieza y validación de datos
- **Load**: Preparación para consumo en API y Dashboard

---

## ✅ Flujo del sistema

```text
[CSV Netflix] → [Transform] → [Extract] → [API OMDb]
                                 ↓
                         [Dataset Final]
                                 ↓
                            [Dashboard]


