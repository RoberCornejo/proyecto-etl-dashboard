# 🎬 Proyecto ETL y Dashboard Interactivo: Netflix + OMDb

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Collaboration-181717?logo=github)

---

# 📖 Descripción

Este proyecto fue desarrollado para la asignatura **Programación para Ciencia de Datos** y tiene como objetivo implementar un proceso **ETL (Extract, Transform, Load)** que permita integrar múltiples fuentes de datos para construir un **dashboard interactivo** destinado al análisis del catálogo de películas de Netflix.

El sistema combina información proveniente de un dataset público de Netflix con datos enriquecidos obtenidos desde la API **OMDb**, generando un conjunto de datos consolidado que posteriormente es almacenado en **Supabase** y utilizado por un dashboard desarrollado en **Streamlit**.

Durante el desarrollo se aplicaron buenas prácticas de limpieza de datos, integración de fuentes, control de versiones mediante Git y trabajo colaborativo utilizando GitHub.

---

# 🎯 Objetivos

## Objetivo General

Desarrollar un pipeline ETL capaz de integrar distintas fuentes de información para construir un dashboard interactivo que facilite el análisis del catálogo de películas de Netflix.

## Objetivos Específicos

- Extraer información desde un dataset CSV.
- Consumir información complementaria desde una API REST.
- Integrar ambas fuentes de datos.
- Limpiar y transformar la información.
- Generar un dataset consolidado para análisis.
- Almacenar los datos en Supabase.
- Construir un dashboard interactivo utilizando Streamlit.
- Implementar un flujo de trabajo colaborativo mediante GitHub.

---

# 👥 Integrantes

| Integrante | Rol |
|------------|-----|
| Maria Aguirre| ETL e Integración de Datos |
| Pamela Albanese | Dashboard y Visualización |
| Roberto Cornejo | DevOps, Integración y Control de Calidad |

---

# 🏗 Arquitectura General

El proyecto sigue una arquitectura basada en un proceso ETL que integra información proveniente de distintas fuentes antes de ser consumida por el dashboard.

```text
                +----------------------+
                | Netflix Dataset CSV  |
                +----------+-----------+
                           |
                           |
                           ▼
                Extracción de Datos
                           |
                           ▼
           Limpieza y Transformación
                           |
                           ▼
                 Consulta API OMDb
                           |
                           ▼
          Integración de ambas fuentes
                           |
                           ▼
                movies_final.csv
                           |
                           ▼
                   Base de Datos
                     Supabase
                           |
                           ▼
              Dashboard Streamlit
                           |
                           ▼
          Visualización y Análisis
```

---

# 📂 Estructura del Proyecto

```text
proyecto-etl-dashboard/

├── api/
├── dashboards/
├── data/
│   ├── netflix_titles.csv
│   └── movies_final.csv
├── docs/
├── etl/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠 Tecnologías Utilizadas

- Python
- Pandas
- Requests
- Streamlit
- Supabase
- OMDb API
- Git
- GitHub
- python-dotenv

---

# 📊 Fuentes de Datos

El proyecto integra información proveniente de dos fuentes principales.

## 📁 Dataset Netflix

Corresponde al conjunto de datos base utilizado para iniciar el proceso ETL.

Archivo:

```text
data/netflix_titles.csv
```

Información disponible:

- Título
- Año de estreno
- Duración
- País
- Director
- Clasificación
- Género
- Descripción

Durante la etapa de extracción y transformación se realizaron procesos de:

- Lectura mediante Pandas.
- Filtrado de películas.
- Eliminación de registros duplicados.
- Tratamiento de valores nulos.
- Normalización de títulos.
- Conversión de tipos de datos.

---

## 🌐 API OMDb

La API OMDb fue utilizada para enriquecer la información obtenida desde el dataset de Netflix.

La consulta se realiza utilizando:

- Título
- Año de estreno

Información incorporada:

- IMDb ID
- IMDb Rating
- IMDb Votes
- Director
- Actores
- Género
- Idioma
- País
- Premios
- Metascore
- Recaudación (Box Office)

También se implementó manejo de errores para controlar respuestas vacías, problemas de conexión y películas no encontradas.

---

# 🔄 Proceso ETL

El proyecto implementa un proceso **ETL (Extract, Transform, Load)** para integrar información proveniente de distintas fuentes y generar un conjunto de datos preparado para su análisis y visualización.

---

## 📥 Extract (Extracción)

En la etapa de extracción se obtuvieron datos desde dos fuentes diferentes:

### Fuente 1: Dataset Netflix

Se cargó el archivo `netflix_titles.csv` utilizando la biblioteca **Pandas**, seleccionando únicamente los registros correspondientes a películas.

Durante esta etapa se realizaron las siguientes acciones:

- Lectura del archivo CSV.
- Revisión de la estructura del dataset.
- Identificación de columnas relevantes.
- Filtrado de registros tipo **Movie**.

---

### Fuente 2: API OMDb

Posteriormente se realizó una consulta individual a la API **OMDb** para cada película obtenida desde el dataset de Netflix.

La búsqueda se realizó utilizando:

- Título de la película.
- Año de estreno.

Cada respuesta permitió enriquecer el dataset con información adicional no disponible en el archivo original.

---

# 🔄 Transform (Transformación)

Una vez obtenida la información desde ambas fuentes, se inició el proceso de transformación de datos.

Las principales transformaciones fueron:

## 🧹 Limpieza de datos

- Eliminación de registros duplicados.
- Eliminación de valores nulos críticos.
- Corrección de formatos inconsistentes.
- Normalización de títulos.
- Validación de años de estreno.

---

## 🔗 Integración de fuentes

La integración entre Netflix y OMDb se realizó utilizando como llave de búsqueda:

- `title`
- `release_year`

Esta estrategia permitió disminuir errores asociados a películas con títulos similares o diferentes versiones.

---

## 📊 Variables generadas

Durante el proceso se crearon nuevas variables para facilitar el análisis posterior.

Entre ellas:

| Variable | Descripción |
|----------|-------------|
| runtime_minutes | Duración en minutos |
| imdb_rating | Calificación IMDb |
| imdb_votes_numeric | Cantidad de votos convertida a valor numérico |
| box_office_numeric | Recaudación convertida a formato numérico |

---

## 🔍 Calidad de los datos

Como parte del proceso ETL se implementaron distintas validaciones para garantizar la calidad del dataset.

Se verificó:

- Registros duplicados.
- Valores faltantes.
- Conversión correcta de tipos de datos.
- Integridad de la información obtenida desde OMDb.

En aquellos casos donde la API no entregó información, se conservaron valores nulos controlados para evitar la pérdida de registros.

---

# 📤 Load (Carga)

Una vez finalizado el proceso de integración y transformación, se generó el dataset consolidado:

```text
data/movies_final.csv
```

Este archivo constituye el resultado principal del proceso ETL y contiene la información lista para ser utilizada en análisis y visualizaciones.

---

# 🗄 Base de Datos (Supabase)

Como etapa final del proceso, el dataset consolidado fue almacenado en una base de datos **Supabase**.

La base de datos permite:

- Centralizar la información procesada.
- Evitar ejecutar nuevamente el ETL para cada consulta.
- Facilitar el acceso al dashboard.
- Mantener una única fuente de datos para el proyecto.

La información fue cargada en la tabla:

```text
movies_final
```

---

# 🔄 Flujo General del Proyecto

El flujo completo implementado en el proyecto es el siguiente:

```text
                 Netflix Dataset
                        │
                        ▼
             Lectura del archivo CSV
                        │
                        ▼
          Limpieza y validación inicial
                        │
                        ▼
              Consulta API OMDb
                        │
                        ▼
           Integración de ambas fuentes
                        │
                        ▼
          Transformación de los datos
                        │
                        ▼
              movies_final.csv
                        │
                        ▼
                 Base de datos
                  (Supabase)
                        │
                        ▼
           Dashboard desarrollado
              con Streamlit
```

---

# 📈 Resultado del ETL

Como resultado del proceso se obtuvo un dataset consolidado que reúne información proveniente del catálogo de Netflix y datos complementarios obtenidos desde la API OMDb.

El dataset final se encuentra preparado para:

- Análisis exploratorio.
- Construcción de indicadores.
- Desarrollo de visualizaciones.
- Consumo desde el dashboard interactivo.

Este conjunto de datos representa la base sobre la cual se desarrolló todo el proceso analítico del proyecto.

# ⚙️ Requisitos del Proyecto

Antes de ejecutar el proyecto, asegúrese de contar con los siguientes requisitos instalados:

- Python 3.11 o superior
- Git
- pip
- Cuenta en Supabase (opcional, si se desea utilizar la base de datos)
- API Key de OMDb

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/RoberCornejo/proyecto-etl-dashboard.git
```

Ingresar al proyecto:

```bash
cd proyecto-etl-dashboard
```

---

## 2. Crear un entorno virtual

### Windows

```bash
python -m venv .venv
```

Activar el entorno:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

# 🔐 Variables de Entorno

Para proteger las credenciales del proyecto, se utilizan variables de entorno mediante un archivo `.env`.
(En esta oportunidad hemos cargado las credenciales para evitar conflictos)
Crear un archivo llamado:

```text
.env
```

Agregar las siguientes variables:

```env
OMDB_API_KEY=12a2233e
SUPABASE_URL=https://gaaurgrajxyjlzdaowgk.supabase.co
SUPABASE_KEY=sb_publishable_URLeBdWKv2
```

> **Importante:** No publique sus credenciales reales en el repositorio. El archivo `.env` debe estar incluido en el archivo `.gitignore`.

---

# ▶️ Ejecutar el Proceso ETL

Una vez configuradas las variables de entorno, ejecutar:

```bash
python etl/main.py
```

Al finalizar el proceso se generará el archivo:

```text
data/movies_final.csv
```

Si el proyecto está configurado para ello, el dataset también podrá cargarse en la base de datos Supabase.

---

# 📊 Ejecutar el Dashboard

El dashboard fue desarrollado utilizando **Streamlit**.

Para iniciarlo, debo ubicarse en la raíz del proyecto (proyecto-etl-dashboard)
luego debe ejecutar:

```bash
python -m streamlit run dashboards/app.py
```
---

## 🌐 Visualización del Dashboard

Una vez ejecutado el comando anterior, Streamlit iniciará un servidor local y mostrará un mensaje similar al siguiente:

```text
Local URL: http://localhost:8501
```

Abra esa dirección en su navegador web para acceder al dashboard interactivo.

Desde la interfaz será posible explorar los datos mediante filtros dinámicos y gráficos interactivos.

---

# 📈 Funcionalidades del Dashboard

El dashboard permite analizar el catálogo de películas mediante diferentes visualizaciones.

Entre las funcionalidades implementadas se encuentran:

- Indicadores generales del catálogo.
- Distribución de películas por año de estreno.
- Distribución por país.
- Distribución por género.
- Top 10 películas mejor evaluadas.
- Directores con mayor cantidad de películas.
- Relación entre premios y calificaciones IMDb.
- Distribución de duración de las películas.
- Filtros dinámicos para explorar la información.

---

# 🧪 Ejecución de Pruebas

El proyecto incorpora pruebas para verificar el correcto funcionamiento del proceso ETL.

Ejecutar:

```bash
pytest
```

Las pruebas permiten validar:

- Lectura del dataset.
- Transformaciones de datos.
- Integración con la API.
- Correcta generación del dataset final.

---

# 📁 Archivos Generados

Como resultado de la ejecución del proyecto se generan los siguientes recursos:

| Archivo | Descripción |
|----------|-------------|
| `movies_final.csv` | Dataset consolidado Netflix + OMDb |
| Tabla `movies_final` | Dataset almacenado en Supabase |
| Dashboard Streamlit | Visualización interactiva del proyecto |

---

# 📊 Resultados Esperados

Al ejecutar correctamente el proyecto se obtiene:

- Dataset limpio y validado.
- Información enriquecida mediante la API OMDb.
- Integración de múltiples fuentes de datos.
- Dataset consolidado para análisis.
- Dashboard interactivo con filtros y visualizaciones.
- Base de datos lista para futuras consultas.

# 🌿 Flujo de Trabajo Colaborativo

El desarrollo del proyecto se realizó utilizando **Git** y **GitHub** como herramientas de control de versiones, permitiendo que cada 
integrante trabajara de forma independiente sin afectar el trabajo del resto del equipo.

Se utilizó una estrategia basada en ramas (*Git Flow*) con la siguiente estructura:

```text
main
│
├── develop
│
├── feature/etl
├── feature/dashboard
└── feature/devops
```

## Estrategia de trabajo

- Cada integrante desarrolló sus funcionalidades en una rama independiente.
- Los cambios fueron integrados mediante **Pull Requests**.
- Antes de realizar cada integración se verificó que no existieran conflictos y que el proyecto continuara funcionandocorrectamente.
- La rama **develop** fue utilizada para integrar el trabajo del equipo.
- Finalmente, la rama **main** quedó como la versión estable del proyecto.

---

# 👥 Distribución del Trabajo

El proyecto fue desarrollado de manera colaborativa, distribuyendo las responsabilidades entre los integrantes del equipo.

## Maria Aguirre – ETL e Integración de Datos

Responsable de:

- Extracción de datos desde el dataset de Netflix.
- Consumo de la API OMDb.
- Integración de ambas fuentes.
- Limpieza y transformación de datos.
- Generación del dataset consolidado.
- Carga de información en Supabase.

---

## Pamela Albanese – Dashboard

Responsable de:

- Diseño de la interfaz del dashboard.
- Desarrollo de visualizaciones interactivas.
- Implementación de filtros dinámicos.
- Construcción de indicadores y gráficos.
- Consumo de la información desde Supabase.

---

## Roberto Cornejo – DevOps e Integración

Responsable de:

- Organización del repositorio.
- Gestión de ramas.
- Integración mediante Pull Requests.
- Validación del funcionamiento general del proyecto.
- Ejecución de pruebas.
- Control de calidad e integración final.

---

# ✅ Resultados Obtenidos

Al finalizar el proyecto se logró:

- Integrar información proveniente de múltiples fuentes.
- Automatizar el proceso ETL.
- Generar un dataset limpio y consolidado.
- Almacenar la información en Supabase.
- Desarrollar un dashboard interactivo para el análisis de datos.
- Aplicar un flujo de trabajo colaborativo utilizando Git y GitHub.

El resultado corresponde a una solución completa para el procesamiento, integración y visualización de datos, 
siguiendo una arquitectura modular que facilita futuras mejoras y ampliaciones.

---

# 🚀 Mejoras Futuras

Como trabajo futuro, el proyecto podría incorporar nuevas funcionalidades, tales como:

- Integración con nuevas fuentes de datos.
- Automatización de la actualización periódica del ETL.
- Incorporación de nuevos indicadores y gráficos.
- Optimización del rendimiento del proceso de integración.
- Publicación del dashboard en un servicio de alojamiento en la nube.

---

# 📚 Aprendizajes

Durante el desarrollo del proyecto se fortalecieron competencias relacionadas con:

- Procesos ETL.
- Integración de APIs REST.
- Limpieza y transformación de datos.
- Bases de datos en la nube.
- Visualización de datos mediante Streamlit.
- Trabajo colaborativo utilizando Git y GitHub.
- Documentación técnica de proyectos de ciencia de datos.

---

# 📄 Licencia

Este proyecto fue desarrollado con fines exclusivamente académicos para la asignatura **Programación para Ciencia de Datos**.

El contenido del repositorio puede utilizarse como referencia para fines educativos, respetando la autoría de sus desarrolladores.

---

# ⭐ Agradecimientos

Agradecemos al equipo docente de la asignatura por el acompañamiento durante el desarrollo del proyecto y a todos los integrantes 
del equipo por su compromiso, colaboración y participación en las distintas etapas de implementación.
