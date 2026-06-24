import os
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

st.set_page_config(
    page_title="Dashboard Netflix + OMDb",
    page_icon="🎬",
    layout="wide"
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


@st.cache_data
def cargar_datos():
    try:
        if SUPABASE_URL and SUPABASE_KEY:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            response = supabase.table("movies_final").select("*").execute()

            if response.data:
                return pd.DataFrame(response.data)

        return pd.read_csv("data/movies_final.csv")

    except Exception as e:
        st.warning(f"No se pudo cargar desde Supabase o archivo local: {e}")
        return pd.read_csv("data/netflix_titles.csv")


df = cargar_datos()

# Columnas reales
TITLE = "title"
YEAR = "release_year"
COUNTRY = "country_omdb" if "country_omdb" in df.columns else "country"
GENRE = "genre"
IMDB = "imdb_rating"
VOTES = "imdb_votes"
METASCORE = "metascore"
DIRECTOR = "director_y" if "director_y" in df.columns else "director_x"
ACTORS = "actors"
AWARDS = "awards"
DESCRIPTION = "description"

# Limpieza numérica
if YEAR in df.columns:
    df[YEAR] = pd.to_numeric(df[YEAR], errors="coerce")

if IMDB in df.columns:
    df[IMDB] = pd.to_numeric(df[IMDB], errors="coerce")

if METASCORE in df.columns:
    df[METASCORE] = pd.to_numeric(df[METASCORE], errors="coerce")

if VOTES in df.columns:
    df[VOTES] = df[VOTES].astype(str).str.replace(",", "", regex=False)
    df[VOTES] = pd.to_numeric(df[VOTES], errors="coerce")


# Paleta profesional
COLOR_AZUL = "#2563EB"
COLOR_VERDE = "#10B981"
COLOR_NARANJO = "#F59E0B"
COLOR_MORADO = "#8B5CF6"
COLOR_VINO = "#C2410C"


def valor_limpio(valor):
    if pd.isna(valor) or str(valor).strip() in ["nan", "None", "N/A", "", "Sin información"]:
        return "No informado"
    return valor


def aplicar_estilo_grafico(fig):
    fig.update_layout(
        font=dict(size=16),
        title_font=dict(size=22),
        xaxis_title_font=dict(size=17),
        yaxis_title_font=dict(size=17),
        legend_font=dict(size=15),
        margin=dict(l=40, r=40, t=70, b=70)
    )
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))
    return fig


# Encabezado
st.title("🎬 Dashboard de Películas Netflix + OMDb")

st.markdown("""
Este dashboard reúne información del catálogo de películas disponible en Netflix junto con datos complementarios obtenidos desde la API OMDb. 
La integración de ambas fuentes permite enriquecer cada registro con indicadores como calificación IMDb, Metascore, géneros, actores, premios y país de producción.

Los datos fueron consolidados mediante un proceso ETL y almacenados en Supabase, permitiendo explorar el catálogo a través de filtros, indicadores y visualizaciones interactivas.
""")

st.caption("Fuente de datos: Netflix Dataset + OMDb API + Supabase")

st.divider()


# Filtros
st.sidebar.header("🔎 Filtros")

df_filtrado = df.copy()

if YEAR in df.columns:
    anios = sorted(df[YEAR].dropna().unique())
    anios_sel = st.sidebar.multiselect("Año de estreno", anios, default=anios)
    df_filtrado = df_filtrado[df_filtrado[YEAR].isin(anios_sel)]

if COUNTRY in df.columns:
    paises = sorted(df[COUNTRY].dropna().unique())
    paises_sel = st.sidebar.multiselect("País", paises)
    if paises_sel:
        df_filtrado = df_filtrado[df_filtrado[COUNTRY].isin(paises_sel)]

if GENRE in df.columns:
    generos_lista = sorted(df[GENRE].dropna().str.split(", ").explode().unique())
    generos_sel = st.sidebar.multiselect("Género", generos_lista)
    if generos_sel:
        df_filtrado = df_filtrado[
            df_filtrado[GENRE].fillna("").apply(
                lambda x: any(g in x for g in generos_sel)
            )
        ]

if IMDB in df.columns and df[IMDB].notna().any():
    min_imdb = float(df[IMDB].min())
    max_imdb = float(df[IMDB].max())
    rango_imdb = st.sidebar.slider(
        "Rango IMDb",
        min_value=min_imdb,
        max_value=max_imdb,
        value=(min_imdb, max_imdb),
        step=0.1
    )
    df_filtrado = df_filtrado[
        (df_filtrado[IMDB] >= rango_imdb[0]) &
        (df_filtrado[IMDB] <= rango_imdb[1])
    ]


# KPIs
st.subheader("📊 Indicadores principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎬 Total de películas", len(df_filtrado))

with col2:
    if IMDB in df_filtrado.columns and df_filtrado[IMDB].notna().any():
        st.metric("⭐ Promedio IMDb", round(df_filtrado[IMDB].mean(), 2))
    else:
        st.metric("⭐ Promedio IMDb", "No informado")

with col3:
    if GENRE in df_filtrado.columns and df_filtrado[GENRE].notna().any():
        generos = df_filtrado[GENRE].dropna().str.split(", ").explode()
        st.metric("🎭 Géneros", generos.nunique())
    else:
        st.metric("🎭 Géneros", "No informado")

with col4:
    if METASCORE in df_filtrado.columns and df_filtrado[METASCORE].notna().any():
        st.metric("🏆 Metascore promedio", round(df_filtrado[METASCORE].mean(), 1))
    else:
        st.metric("🏆 Metascore promedio", "No informado")

st.divider()


# Visualizaciones
st.subheader("📈 Visualizaciones del catálogo")


# 1. Películas por año
st.markdown("### 📈 Evolución del catálogo")
st.write("Cantidad de películas según su año de estreno.")

if YEAR in df_filtrado.columns:
    peliculas_por_anio = (
        df_filtrado[YEAR]
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )
    peliculas_por_anio.columns = ["Año", "Cantidad"]

    fig = px.line(
        peliculas_por_anio,
        x="Año",
        y="Cantidad",
        markers=True,
        title="Películas por año",
        labels={"Año": "Año de estreno", "Cantidad": "Cantidad de películas"}
    )
    fig.update_traces(line_color=COLOR_AZUL)
    fig = aplicar_estilo_grafico(fig)
    st.plotly_chart(fig, use_container_width=True)


col_g1, col_g2 = st.columns(2)

# 2. Países
with col_g1:
    st.markdown("### 🌍 Países con más películas")
    st.write("Países con mayor presencia dentro del catálogo.")

    if COUNTRY in df_filtrado.columns:
        top_paises = (
            df_filtrado[COUNTRY]
            .dropna()
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_paises.columns = ["País", "Cantidad"]

        fig = px.bar(
            top_paises,
            x="País",
            y="Cantidad",
            title="Top 10 países",
            labels={"País": "País", "Cantidad": "Cantidad de películas"}
        )
        fig.update_traces(marker_color=COLOR_VERDE)
        fig = aplicar_estilo_grafico(fig)
        st.plotly_chart(fig, use_container_width=True)


# 3. Géneros
with col_g2:
    st.markdown("### 🎭 Géneros más frecuentes")
    st.write("Géneros predominantes dentro del catálogo enriquecido.")

    if GENRE in df_filtrado.columns:
        generos = df_filtrado[GENRE].dropna().str.split(", ").explode()
        top_generos = generos.value_counts().head(10).reset_index()
        top_generos.columns = ["Género", "Cantidad"]

        fig = px.bar(
            top_generos,
            x="Género",
            y="Cantidad",
            title="Top 10 géneros",
            labels={"Género": "Género", "Cantidad": "Cantidad de películas"}
        )
        fig.update_traces(marker_color=COLOR_NARANJO)
        fig = aplicar_estilo_grafico(fig)
        st.plotly_chart(fig, use_container_width=True)


# 4. Distribución IMDb por rangos
st.markdown("### ⭐ Distribución de calificaciones IMDb")
st.write("Cantidad de películas agrupadas según rango de calificación IMDb.")

if IMDB in df_filtrado.columns:
    df_imdb = df_filtrado.dropna(subset=[IMDB]).copy()

    bins = [0, 4, 5, 6, 7, 8, 10]
    labels = ["0-4", "4-5", "5-6", "6-7", "7-8", "8-10"]
    df_imdb["Rango IMDb"] = pd.cut(df_imdb[IMDB], bins=bins, labels=labels, include_lowest=True)

    imdb_rangos = df_imdb["Rango IMDb"].value_counts().sort_index().reset_index()
    imdb_rangos.columns = ["Rango IMDb", "Cantidad"]

    fig = px.bar(
        imdb_rangos,
        x="Rango IMDb",
        y="Cantidad",
        title="Películas por rango de calificación IMDb",
        labels={"Rango IMDb": "Rango de calificación IMDb", "Cantidad": "Cantidad de películas"}
    )
    fig.update_traces(marker_color=COLOR_MORADO)
    fig = aplicar_estilo_grafico(fig)
    st.plotly_chart(fig, use_container_width=True)


col_g3, col_g4 = st.columns(2)

# 5. Directores mejor evaluados
with col_g3:
    st.markdown("### 🎬 Directores mejor evaluados")
    st.write("Promedio IMDb por director, considerando las películas disponibles en el catálogo.")

    if DIRECTOR in df_filtrado.columns and IMDB in df_filtrado.columns:
        directores = (
            df_filtrado
            .dropna(subset=[DIRECTOR, IMDB])
            .groupby(DIRECTOR, as_index=False)
            .agg(
                Promedio_IMDb=(IMDB, "mean"),
                Cantidad_peliculas=(TITLE, "count")
            )
        )

        directores = directores.sort_values("Promedio_IMDb", ascending=False).head(10)

        fig = px.bar(
            directores,
            x="Promedio_IMDb",
            y=DIRECTOR,
            orientation="h",
            title="Top 10 directores por promedio IMDb",
            labels={
                "Promedio_IMDb": "Promedio IMDb",
                DIRECTOR: "Director",
                "Cantidad_peliculas": "Cantidad de películas"
            },
            hover_data=["Cantidad_peliculas"]
        )
        fig.update_traces(marker_color=COLOR_AZUL)
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig = aplicar_estilo_grafico(fig)
        st.plotly_chart(fig, use_container_width=True)


# 6. Top 10 películas
with col_g4:
    st.markdown("### 🏆 Top 10 películas mejor evaluadas")
    st.write("Películas con mayor calificación IMDb dentro del catálogo.")

    if TITLE in df_filtrado.columns and IMDB in df_filtrado.columns:
        top_imdb = (
            df_filtrado
            .dropna(subset=[TITLE, IMDB])
            .sort_values(IMDB, ascending=False)
            .head(10)
        )

        fig = px.bar(
            top_imdb,
            x=IMDB,
            y=TITLE,
            orientation="h",
            title="Top 10 películas por IMDb",
            labels={
                IMDB: "Calificación IMDb",
                TITLE: "Película"
            }
        )
        fig.update_traces(marker_color=COLOR_VINO)
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        fig = aplicar_estilo_grafico(fig)
        st.plotly_chart(fig, use_container_width=True)

st.divider()


# Ficha técnica
st.subheader("🎥 Explorar película")

if TITLE in df_filtrado.columns and len(df_filtrado) > 0:
    pelicula_sel = st.selectbox(
        "Selecciona una película",
        sorted(df_filtrado[TITLE].dropna().unique())
    )

    pelicula = df_filtrado[df_filtrado[TITLE] == pelicula_sel].iloc[0]

    st.markdown(f"## 🎬 {valor_limpio(pelicula.get(TITLE))}")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("⭐ IMDb", valor_limpio(pelicula.get(IMDB)))

    with c2:
        st.metric("🏆 Metascore", valor_limpio(pelicula.get(METASCORE)))

    with c3:
        anio = pelicula.get(YEAR)
        st.metric("📅 Año", int(anio) if pd.notna(anio) else "No informado")

    with c4:
        st.metric("🌍 País", valor_limpio(pelicula.get(COUNTRY)))

    st.markdown("### 📄 Ficha técnica")

    ficha1, ficha2 = st.columns(2)

    with ficha1:
        st.write(f"**🎭 Género:** {valor_limpio(pelicula.get(GENRE))}")
        st.write(f"**🎬 Director:** {valor_limpio(pelicula.get(DIRECTOR))}")
        st.write(f"**👥 Actores:** {valor_limpio(pelicula.get(ACTORS))}")

    with ficha2:
        st.write(f"**🏅 Premios:** {valor_limpio(pelicula.get(AWARDS))}")
        st.write(f"**🗳️ Votos IMDb:** {valor_limpio(pelicula.get(VOTES))}")

    st.markdown("### 📖 Sinopsis")
    st.write(valor_limpio(pelicula.get(DESCRIPTION)))

else:
    st.info("No hay películas disponibles con los filtros seleccionados.")

st.divider()


# Dataset procesado
st.subheader("📂 Datos procesados")

columnas_mostrar = {
    "title": "Título",
    "release_year": "Año",
    "genre": "Género",
    "country_omdb": "País",
    "director_y": "Director",
    "actors": "Actores",
    "imdb_rating": "Calificación IMDb",
    "imdb_votes": "Votos IMDb",
    "metascore": "Metascore",
    "awards": "Premios"
}

columnas_existentes = [col for col in columnas_mostrar.keys() if col in df_filtrado.columns]

df_tabla = df_filtrado[columnas_existentes].rename(columns=columnas_mostrar)

with st.expander("Ver dataset procesado"):
    st.dataframe(df_tabla, use_container_width=True)

st.divider()


# Conclusiones
st.subheader("📌 Conclusiones del análisis")

st.write("""
- El catálogo analizado permite observar la distribución de películas según año, país y género.
- La integración con OMDb permite complementar los datos originales con métricas de evaluación como IMDb y Metascore.
- Los géneros y países predominantes permiten identificar tendencias dentro del catálogo.
- Las calificaciones IMDb permiten destacar tanto películas individuales como directores con mejor valoración promedio.
""")