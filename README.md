## ✅ Arquitectura ETL

El proyecto sigue un enfoque modular:

- **Extract**: Lectura de datos desde CSV (Netflix dataset)
- **Transform**: Limpieza y validación de datos
- **Load**: Carga del dataset integrado hacia Supabase para su posterior consumo en dashboards.

---
## 🎬 Integración de fuentes de datos

El proyecto utiliza dos fuentes principales de información:

### Fuente 1: Dataset Netflix
- Archivo: `data/netflix_titles.csv`
- Lectura mediante Pandas.
- Filtrado de registros tipo Movie.
- Eliminación de duplicados.
- Tratamiento de valores nulos.
- Estandarización de títulos.

### Fuente 2: API OMDb
- Consulta mediante título y año de estreno.
- Obtención de información enriquecida:
  - IMDb ID
  - Rating IMDb
  - Director
  - Género
  - Actores
  - Metascore
  - Recaudación
  - Premios

### Llave de integración
La unión entre ambas fuentes se realiza utilizando:

- `title`
- `release_year`

Esto permite complementar la información del dataset Netflix con los datos obtenidos desde OMDb.

---

## 🔄 Flujo ETL actualizado

```text
[Netflix CSV]
      ↓
[Limpieza y Validación]
      ↓
[Extracción de Películas]
      ↓
[Consulta API OMDb]
      ↓
[Integración Netflix + OMDb]
      ↓
[Transformación de Datos]
      ↓
[movies_final.csv]
      ↓
[Supabase]
      ↓
[Dashboard]
```

---

## 📊 Transformaciones realizadas

- Eliminación de registros duplicados.
- Eliminación de valores nulos críticos.
- Estandarización de títulos.
- Conversión de tipos de datos.
- Generación de variables para análisis:
  - `runtime_minutes`
  - `imdb_rating`
  - `imdb_votes_numeric`
  - `box_office_numeric`

- Generación del dataset integrado:
  - `data/movies_final.csv`


