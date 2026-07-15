import logging
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
import plotly.express as px

from dashboards.styles import aplicar_estilo_grafico, aplicar_estilo_dashboard
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

#aplicar_css()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@st.cache_data
def cargar_datos():
    supabase_available = False
    local_movies_path = "data/movies_final.csv"
    local_netflix_path = "data/netflix_titles.csv"

    if SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            response = supabase.table("movies_final").select("*").execute()

            if response.error:
                raise RuntimeError(response.error)

            if response.data:
                df = pd.DataFrame(response.data)
                # Registrar internamente la fuente
                df.attrs['data_source'] = 'supabase'
                df.attrs['data_updated'] = None
                logger.info("Datos cargados desde Supabase con %d registros", len(df))
                return df

            logger.warning("Supabase respondió correctamente, pero no devolvió registros.")
            supabase_available = False
        except Exception as exc:
            # Solo log; no mostrar mensajes de Supabase al usuario (según requerimiento)
            logger.warning(
                "Fallo al conectar con Supabase: %s. Se continúa con fallback local.",
                exc,
            )
            supabase_available = False
    else:
        logger.info("No se encontraron credenciales de Supabase en el entorno.")

    if os.path.exists(local_movies_path):
        try:
            df = pd.read_csv(local_movies_path)
            # Metadata interna para indicar fuente y fecha de actualización
            df.attrs['data_source'] = 'movies_final.csv'
            try:
                df.attrs['data_updated'] = pd.to_datetime(
                    os.path.getmtime(local_movies_path), unit='s'
                )
            except Exception:
                df.attrs['data_updated'] = None

            logger.info("Datos cargados desde %s con %d registros", local_movies_path, len(df))
            return df
        except Exception as exc:
            logger.exception("Error al leer %s", local_movies_path)
    else:
        logger.info("Archivo %s no encontrado. Se intentará netflix_titles.csv.", local_movies_path)

    try:
        df = pd.read_csv(local_netflix_path)
        df.attrs['data_source'] = 'netflix_titles.csv'
        try:
            df.attrs['data_updated'] = pd.to_datetime(
                os.path.getmtime(local_netflix_path), unit='s'
            )
        except Exception:
            df.attrs['data_updated'] = None

        logger.info("Datos cargados desde %s con %d registros", local_netflix_path, len(df))
        return df
    except Exception as exc:
        logger.exception("Error al leer %s", local_netflix_path)
        st.error(
            "No se pudo cargar ningún dataset local. Verifique que los archivos existan y sean legibles.",
        )
        raise


def valor_limpio(valor):
    if pd.isna(valor) or str(valor).strip() in ["nan", "None", "N/A", "", "Sin información"]:
        return "No informado"
    return valor


df = cargar_datos()

# Aplicar estilos globales del dashboard (tema corporativo)
aplicar_estilo_dashboard()

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


# Header / Hero
data_source = df.attrs.get('data_source', 'local')
updated_ts = df.attrs.get('data_updated', None)
updated_str = updated_ts.strftime('%Y-%m-%d %H:%M') if updated_ts is not None else 'Desconocida'

st.markdown(f"""
<div class="hero">
    <div class="hero-title">🎬 Dashboard Netflix + OMDb</div>
    <div class="hero-subtitle">Análisis ejecutivo del catálogo — métricas y visualizaciones enriquecidas.</div>
    <div class="hero-meta">Fuente de datos: Netflix + OMDb &nbsp;•&nbsp; Última actualización: {updated_str}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.06)'/>", unsafe_allow_html=True)


st.sidebar.markdown("<div style='font-weight:700; font-size:18px; margin-bottom:6px;'>🔎 Filtros de análisis</div>", unsafe_allow_html=True)
df_filtrado = df.copy()

with st.sidebar.expander("Filtros", expanded=True):
    # Año
    if YEAR in df.columns:
        anios = sorted(df[YEAR].dropna().unique())
        if 'anios_sel' not in st.session_state:
            st.session_state['anios_sel'] = anios
        anios_sel = st.multiselect("Año de estreno", anios, default=st.session_state['anios_sel'], key='anios_sel')
        if anios_sel:
            df_filtrado = df_filtrado[df_filtrado[YEAR].isin(anios_sel)]

    # País
    if COUNTRY in df.columns:
        paises = sorted(df[COUNTRY].dropna().unique())
        if 'paises_sel' not in st.session_state:
            st.session_state['paises_sel'] = []
        paises_sel = st.multiselect("País", paises, default=st.session_state['paises_sel'], key='paises_sel')
        if paises_sel:
            df_filtrado = df_filtrado[df_filtrado[COUNTRY].isin(paises_sel)]

    # Género
    if GENRE in df.columns:
        generos_lista = sorted(df[GENRE].dropna().str.split(", ").explode().unique())
        if 'generos_sel' not in st.session_state:
            st.session_state['generos_sel'] = []
        generos_sel = st.multiselect("Género", generos_lista, default=st.session_state['generos_sel'], key='generos_sel')
        if generos_sel:
            df_filtrado = df_filtrado[
                df_filtrado[GENRE].fillna("").apply(lambda x: any(g in x for g in generos_sel))
            ]

    # Rango IMDb
    if IMDB in df.columns and df[IMDB].notna().any():
        min_imdb = float(df[IMDB].min())
        max_imdb = float(df[IMDB].max())
        if 'rango_imdb' not in st.session_state:
            st.session_state['rango_imdb'] = (min_imdb, max_imdb)
        rango_imdb = st.slider(
            "Rango IMDb",
            min_value=min_imdb,
            max_value=max_imdb,
            value=st.session_state['rango_imdb'],
            step=0.1,
            key='rango_imdb'
        )
        df_filtrado = df_filtrado[
            (df_filtrado[IMDB] >= rango_imdb[0]) &
            (df_filtrado[IMDB] <= rango_imdb[1])
        ]

    # Acciones de filtros
    btn_col1, btn_col2 = st.columns([2,1])
    with btn_col1:
        if st.button("Limpiar filtros"):
            # Resetear valores en session_state a defaults
            if YEAR in df.columns:
                st.session_state['anios_sel'] = anios
            if COUNTRY in df.columns:
                st.session_state['paises_sel'] = []
            if GENRE in df.columns:
                st.session_state['generos_sel'] = []
            if IMDB in df.columns and df[IMDB].notna().any():
                st.session_state['rango_imdb'] = (min_imdb, max_imdb)
            st.experimental_rerun()
    with btn_col2:
        st.markdown("<div style='font-size:12px;color:#94A3B8;margin-top:6px;'>Aplicado en tiempo real</div>", unsafe_allow_html=True)

    # Mostrar filtros activos
    active = []
    if YEAR in df.columns and st.session_state.get('anios_sel'):
        active.append(f"Años: {len(st.session_state.get('anios_sel'))}")
    if COUNTRY in df.columns and st.session_state.get('paises_sel'):
        active.append(f"Países: {', '.join(st.session_state.get('paises_sel')[:3])}{'...' if len(st.session_state.get('paises_sel'))>3 else ''}")
    if GENRE in df.columns and st.session_state.get('generos_sel'):
        active.append(f"Géneros: {', '.join(st.session_state.get('generos_sel')[:3])}{'...' if len(st.session_state.get('generos_sel'))>3 else ''}")
    if IMDB in df.columns and st.session_state.get('rango_imdb'):
        r = st.session_state.get('rango_imdb')
        active.append(f"IMDb: {r[0]}–{r[1]}")

    if active:
        st.markdown("<hr style='border:0.5px solid rgba(255,255,255,0.04)'/>", unsafe_allow_html=True)
        st.markdown("**Filtros activos:** " + " • ".join(active))


st.markdown('<div class="section-title">📊 Indicadores Ejecutivos</div>', unsafe_allow_html=True)

# Calcular KPIs
total_peliculas = len(df_filtrado)
promedio_imdb = round(df_filtrado[IMDB].mean(), 2) if IMDB in df_filtrado.columns and df_filtrado[IMDB].notna().any() else 'No informado'
promedio_metascore = round(df_filtrado[METASCORE].mean(), 1) if METASCORE in df_filtrado.columns and df_filtrado[METASCORE].notna().any() else 'No informado'
generos_unicos = df_filtrado[GENRE].dropna().str.split(", ").explode().nunique() if GENRE in df_filtrado.columns and df_filtrado[GENRE].notna().any() else 'No informado'
directores_unicos = df_filtrado[DIRECTOR].nunique() if DIRECTOR in df_filtrado.columns else 'No informado'
paises_representados = df_filtrado[COUNTRY].dropna().nunique() if COUNTRY in df_filtrado.columns else 'No informado'
_box_series = df_filtrado.get('box_office', pd.Series(dtype=float)).dropna()
if not _box_series.empty:
    # Limpiar símbolos de moneda, separadores de miles y espacios, convertir a float
    _box_clean = (
        _box_series.astype(str)
        .str.replace(r"[^0-9.\-]", "", regex=True)
        .replace("", pd.NA)
    )
    _box_numeric = pd.to_numeric(_box_clean, errors="coerce").dropna()
    box_office_prom = round(_box_numeric.mean(), 2) if not _box_numeric.empty else 'No informado'
else:
    box_office_prom = 'No informado'
peliculas_premios = df_filtrado[AWARDS].dropna().apply(lambda x: 1 if str(x).strip() not in ['', 'None', 'Sin información'] else 0).sum() if AWARDS in df_filtrado.columns else 'No informado'

cards_html = f"""
<div class="kpi-grid">
  <div class="kpi-card"><div class="kpi-icon">📽</div><div class="kpi-value">{total_peliculas}</div><div class="kpi-label">Total Películas</div></div>
  <div class="kpi-card"><div class="kpi-icon">⭐</div><div class="kpi-value">{promedio_imdb}</div><div class="kpi-label">IMDb Promedio</div></div>
  <div class="kpi-card"><div class="kpi-icon">🏆</div><div class="kpi-value">{promedio_metascore}</div><div class="kpi-label">Metascore Promedio</div></div>
  <div class="kpi-card"><div class="kpi-icon">🎭</div><div class="kpi-value">{generos_unicos}</div><div class="kpi-label">Géneros Únicos</div></div>
  <div class="kpi-card"><div class="kpi-icon">🎬</div><div class="kpi-value">{directores_unicos}</div><div class="kpi-label">Directores Únicos</div></div>
  <div class="kpi-card"><div class="kpi-icon">🌎</div><div class="kpi-value">{paises_representados}</div><div class="kpi-label">Países Representados</div></div>
  <div class="kpi-card"><div class="kpi-icon">💰</div><div class="kpi-value">{box_office_prom}</div><div class="kpi-label">Box Office Promedio</div></div>
  <div class="kpi-card"><div class="kpi-icon">🏅</div><div class="kpi-value">{peliculas_premios}</div><div class="kpi-label">Películas con Premios</div></div>
</div>
"""

st.markdown(cards_html, unsafe_allow_html=True)

caja_analisis("Lectura general:", analisis_general(df_filtrado))

st.divider()


st.subheader("📈 Visualizaciones del catálogo")

if YEAR in df_filtrado.columns:
    st.markdown("### 📈 Evolución del catálogo por año")
    fig_anio, datos_anio = grafico_peliculas_por_anio(df_filtrado, YEAR)
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig_anio, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    caja_analisis("Análisis de evolución:", analisis_evolucion(datos_anio))


col_g1, col_g2 = st.columns(2)

top_paises = None
top_generos = None

with col_g1:
    if COUNTRY in df_filtrado.columns:
        st.markdown("### 🌍 Países con más películas")
        fig_paises, top_paises = grafico_top_paises(df_filtrado, COUNTRY)
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_paises, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with col_g2:
    if GENRE in df_filtrado.columns:
        st.markdown("### 🎭 Géneros más frecuentes")
        fig_generos, top_generos = grafico_top_generos(df_filtrado, GENRE)
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_generos, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

caja_analisis(
    "Análisis de países y géneros:",
    analisis_paises_generos(top_paises, top_generos)
)


if IMDB in df_filtrado.columns:
    st.markdown("### ⭐ Distribución de calificaciones IMDb")
    fig_imdb, imdb_rangos = grafico_distribucion_imdb(df_filtrado, IMDB)
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.plotly_chart(fig_imdb, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
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
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_top_imdb, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
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
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
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
La integración entre el dataset de Netflix y OMDb aporta valor al proceso, ya que transforma los datos originales
en una base enriquecida con calificaciones IMDb, Metascore, votos, premios, directores y actores.

A partir de las visualizaciones se pueden identificar tendencias relevantes, como los países con mayor presencia,
los géneros más frecuentes, los rangos de calificación predominantes y las películas o directores mejor evaluados.
De esta manera, el dashboard no solo muestra datos, sino que también entrega una interpretación más profunda del catálogo audiovisual.
""")