import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
import plotly.express as px

from styles import aplicar_css, aplicar_estilo_grafico
from charts import (
    grafico_peliculas_por_anio,
    grafico_top_paises,
    grafico_top_generos,
    grafico_distribucion_imdb,
    grafico_top_peliculas_imdb,
    grafico_histograma_imdb,
    grafico_imdb_vs_metascore,
)
from analysis import (
    caja_analisis,
    analisis_general,
    analisis_evolucion,
    analisis_paises_generos,
    analisis_imdb_rangos,
    analisis_directores,
    analisis_top_peliculas,
    analisis_histograma_imdb,
    analisis_imdb_vs_metascore,
)

load_dotenv()

st.set_page_config(
    page_title="Dashboard Netflix + OMDb",
    page_icon="🎬",
    layout="wide"
)

aplicar_css()

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


def valor_limpio(valor):
    if pd.isna(valor) or str(valor).strip() in ["nan", "None", "N/A", "", "Sin información"]:
        return "No informado"
    return valor


df = cargar_datos()

TITLE = "title"
YEAR = "release_year"
COUNTRY = "country_omdb" if "country_omdb" in df.columns else "country"
GENRE = "genre"
IMDB = "imdb_rating"
VOTES = "imdb_votes"
METASCORE = "metascore"
DIRECTOR = "director_y"
ACTORS = "actors"
AWARDS = "awards"
DESCRIPTION = "description"

if YEAR in df.columns:
    df[YEAR] = pd.to_numeric(df[YEAR], errors="coerce")

if IMDB in df.columns:
    df[IMDB] = pd.to_numeric(df[IMDB], errors="coerce")

if METASCORE in df.columns:
    df[METASCORE] = pd.to_numeric(df[METASCORE], errors="coerce")

if VOTES in df.columns:
    df[VOTES] = df[VOTES].astype(str).str.replace(",", "", regex=False)
    df[VOTES] = pd.to_numeric(df[VOTES], errors="coerce")


st.markdown("""
<div style="padding-bottom:25px;">

<h1 style="
font-size:78px;
font-weight:900;
color:white;
margin-bottom:15px;
line-height:1;
">
🎬 Dashboard de Películas Netflix + OMDb
</h1>

<p style="
font-size:27px;
color:#CBD5E1;
line-height:1.8;
margin-bottom:15px;
">
Este dashboard integra información del catálogo de Netflix con datos complementarios obtenidos desde OMDb.
El objetivo es analizar el comportamiento del catálogo según año, país, género,
calificaciones, directores, votos y premios.
</p>

<p style="
font-size:20px;
color:#94A3B8;
">
Fuente de datos: Netflix Dataset + OMDb API + Supabase
</p>

</div>
""", unsafe_allow_html=True)

st.divider()


st.sidebar.header("🔎 Filtros de análisis")
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
            df_filtrado[GENRE].fillna("").apply(lambda x: any(g in x for g in generos_sel))
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


st.subheader("📊 Indicadores principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎬 Total películas", len(df_filtrado))

with col2:
    if IMDB in df_filtrado.columns and df_filtrado[IMDB].notna().any():
        st.metric("⭐ Promedio IMDb", round(df_filtrado[IMDB].mean(), 2))
    else:
        st.metric("⭐ Promedio IMDb", "No informado")

with col3:
    if GENRE in df_filtrado.columns and df_filtrado[GENRE].notna().any():
        generos_total = df_filtrado[GENRE].dropna().str.split(", ").explode()
        st.metric("🎭 Géneros únicos", generos_total.nunique())
    else:
        st.metric("🎭 Géneros únicos", "No informado")

with col4:
    if METASCORE in df_filtrado.columns and df_filtrado[METASCORE].notna().any():
        st.metric("🏆 Metascore promedio", round(df_filtrado[METASCORE].mean(), 1))
    else:
        st.metric("🏆 Metascore promedio", "No informado")

caja_analisis("Lectura general:", analisis_general(df_filtrado))

st.divider()


st.subheader("📈 Visualizaciones del catálogo")

if YEAR in df_filtrado.columns:
    st.markdown("### 📈 Evolución del catálogo por año")
    fig_anio, datos_anio = grafico_peliculas_por_anio(df_filtrado, YEAR)
    st.plotly_chart(fig_anio, use_container_width=True)
    caja_analisis("Análisis de evolución:", analisis_evolucion(datos_anio))


col_g1, col_g2 = st.columns(2)

top_paises = None
top_generos = None

with col_g1:
    if COUNTRY in df_filtrado.columns:
        st.markdown("### 🌍 Países con más películas")
        fig_paises, top_paises = grafico_top_paises(df_filtrado, COUNTRY)
        st.plotly_chart(fig_paises, use_container_width=True)

with col_g2:
    if GENRE in df_filtrado.columns:
        st.markdown("### 🎭 Géneros más frecuentes")
        fig_generos, top_generos = grafico_top_generos(df_filtrado, GENRE)
        st.plotly_chart(fig_generos, use_container_width=True)

caja_analisis(
    "Análisis de países y géneros:",
    analisis_paises_generos(top_paises, top_generos)
)


if IMDB in df_filtrado.columns:
    st.markdown("### ⭐ Distribución de calificaciones IMDb")
    fig_imdb, imdb_rangos = grafico_distribucion_imdb(df_filtrado, IMDB)
    st.plotly_chart(fig_imdb, use_container_width=True)
    caja_analisis("Análisis de calificaciones:", analisis_imdb_rangos(imdb_rangos))


col_g3, col_g4 = st.columns(2)

directores = None
top_imdb = None

with col_g3:
    st.markdown("### 🎬 Directores mejor evaluados")
    st.write("Promedio IMDb por director, considerando las películas disponibles en el catálogo.")

    if "director_y" in df_filtrado.columns and IMDB in df_filtrado.columns:
        directores = (
            df_filtrado
            .dropna(subset=["director_y", IMDB])
            .groupby("director_y", as_index=False)
            .agg(
                Promedio_IMDb=(IMDB, "mean"),
                Cantidad_peliculas=(TITLE, "count")
            )
        )

        directores = directores.sort_values("Promedio_IMDb", ascending=False).head(10)
        directores["Promedio texto"] = directores["Promedio_IMDb"].round(2)

        fig = px.bar(
            directores,
            x="Promedio_IMDb",
            y="director_y",
            orientation="h",
            text="Promedio texto",
            title="Top 10 directores por promedio IMDb",
            labels={
                "Promedio_IMDb": "Promedio IMDb",
                "director_y": "Director",
                "Cantidad_peliculas": "Cantidad de películas"
            },
            hover_data=["Cantidad_peliculas"]
        )

        fig.update_traces(
            marker_color=[
                "#EF4444", "#F59E0B", "#FACC15", "#22C55E", "#3B82F6",
                "#8B5CF6", "#EC4899", "#14B8A6", "#F97316", "#06B6D4"
            ][:len(directores)],
            textposition="outside"
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            height=560,
            margin=dict(l=230, r=80, t=90, b=80)
        )

        fig = aplicar_estilo_grafico(fig)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No se encontró la columna director_y o imdb_rating.")

with col_g4:
    st.markdown("### 🏆 Top 10 películas mejor evaluadas")
    if TITLE in df_filtrado.columns and IMDB in df_filtrado.columns:
        fig_top_imdb, top_imdb = grafico_top_peliculas_imdb(
            df_filtrado,
            TITLE,
            IMDB
        )
        st.plotly_chart(fig_top_imdb, use_container_width=True)

caja_analisis(
    "Análisis de directores:",
    analisis_directores(directores, DIRECTOR)
)

caja_analisis(
    "Análisis de películas destacadas:",
    analisis_top_peliculas(top_imdb, TITLE, IMDB)
)


col_g5, col_g6 = st.columns(2)

with col_g5:
    if IMDB in df_filtrado.columns:
        st.markdown("### 📊 Histograma de IMDb")
        fig_hist, datos_hist = grafico_histograma_imdb(df_filtrado, IMDB)
        st.plotly_chart(fig_hist, use_container_width=True)
        caja_analisis(
            "Análisis estadístico IMDb:",
            analisis_histograma_imdb(datos_hist, IMDB)
        )

with col_g6:
    if IMDB in df_filtrado.columns and METASCORE in df_filtrado.columns:
        st.markdown("### 📉 Relación IMDb vs Metascore")
        fig_scatter, datos_scatter = grafico_imdb_vs_metascore(
            df_filtrado,
            IMDB,
            METASCORE,
            TITLE
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        caja_analisis(
            "Análisis IMDb vs Metascore:",
            analisis_imdb_vs_metascore(datos_scatter, IMDB, METASCORE)
        )


st.divider()


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


st.subheader("📂 Datos procesados")

columnas_mostrar = {
    TITLE: "Título",
    YEAR: "Año",
    GENRE: "Género",
    COUNTRY: "País",
    DIRECTOR: "Director",
    ACTORS: "Actores",
    IMDB: "Calificación IMDb",
    VOTES: "Votos IMDb",
    METASCORE: "Metascore",
    AWARDS: "Premios"
}

columnas_existentes = []
for col in columnas_mostrar.keys():
    if col in df_filtrado.columns and col not in columnas_existentes:
        columnas_existentes.append(col)

df_tabla = df_filtrado[columnas_existentes].rename(columns=columnas_mostrar)

with st.expander("Ver dataset procesado"):
    st.dataframe(df_tabla, use_container_width=True)


st.divider()


st.subheader("📌 Conclusiones del análisis")

st.write("""
El análisis del catálogo permite observar cómo se distribuyen las películas según año, país, género y evaluación externa.
La integración entre Netflix Dataset, OMDb API y Supabase aporta valor al proceso, ya que transforma los datos originales
en una base enriquecida con calificaciones IMDb, Metascore, votos, premios, directores y actores.

A partir de las visualizaciones se pueden identificar tendencias relevantes, como los países con mayor presencia,
los géneros más frecuentes, los rangos de calificación predominantes y las películas o directores mejor evaluados.
De esta manera, el dashboard no solo muestra datos, sino que también entrega una interpretación más profunda del catálogo audiovisual.
""")