import streamlit as st
import pandas as pd


def caja_analisis(titulo, texto):
    st.markdown(
        f"""
        <div class="analysis-box">
            <b>{titulo}</b><br>
            {texto}
        </div>
        """,
        unsafe_allow_html=True
    )


def analisis_general(df_filtrado):
    total = len(df_filtrado)

    return (
        f"Actualmente se están analizando <b>{total}</b> películas según los filtros seleccionados. "
        "Estos indicadores permiten observar rápidamente el tamaño del catálogo, su evaluación promedio "
        "y la diversidad de géneros presentes."
    )


def analisis_evolucion(datos_anio):
    if datos_anio is None or datos_anio.empty:
        return "No hay datos suficientes para analizar la evolución por año."

    anio_max = datos_anio.loc[datos_anio["Cantidad"].idxmax(), "Año"]
    cant_max = datos_anio["Cantidad"].max()

    return (
        f"El año con mayor cantidad de películas es <b>{int(anio_max)}</b>, "
        f"con <b>{cant_max}</b> registros. Esto permite identificar los periodos "
        "con mayor concentración de títulos dentro del catálogo."
    )


def analisis_paises_generos(top_paises, top_generos):
    if top_paises is None or top_paises.empty or top_generos is None or top_generos.empty:
        return "No hay datos suficientes para analizar países y géneros."

    pais_top = top_paises.iloc[0]["País"]
    pais_cantidad = top_paises.iloc[0]["Cantidad"]

    genero_top = top_generos.iloc[0]["Género"]
    genero_cantidad = top_generos.iloc[0]["Cantidad"]

    return (
        f"El país con mayor presencia es <b>{pais_top}</b>, con <b>{pais_cantidad}</b> películas. "
        f"El género más frecuente es <b>{genero_top}</b>, con <b>{genero_cantidad}</b> apariciones. "
        "Esto ayuda a reconocer qué regiones y tipos de contenido predominan dentro del catálogo."
    )


def analisis_imdb_rangos(imdb_rangos):
    if imdb_rangos is None or imdb_rangos.empty:
        return "No hay datos suficientes para analizar la distribución de calificaciones IMDb."

    rango_top = imdb_rangos.loc[imdb_rangos["Cantidad"].idxmax(), "Rango IMDb"]
    cantidad_rango = imdb_rangos["Cantidad"].max()
    total = imdb_rangos["Cantidad"].sum()

    porcentaje = round((cantidad_rango / total) * 100, 1) if total > 0 else 0

    return (
        f"La mayor concentración de películas se encuentra en el rango IMDb <b>{rango_top}</b>, "
        f"con <b>{cantidad_rango}</b> películas, equivalente al <b>{porcentaje}%</b> del total con calificación disponible. "
        "Este resultado permite observar si el catálogo se concentra principalmente en títulos de evaluación baja, media o alta."
    )


def analisis_directores(directores, director_col):
    if directores is None or directores.empty:
        return "No hay datos suficientes para analizar directores."

    mejor_director = directores.iloc[0][director_col]
    mejor_promedio = round(directores.iloc[0]["Promedio_IMDb"], 2)
    cantidad_director = directores.iloc[0]["Cantidad_peliculas"]

    return (
        f"El director con mejor promedio IMDb dentro del conjunto filtrado es <b>{mejor_director}</b>, "
        f"con una calificación promedio de <b>{mejor_promedio}</b> y <b>{cantidad_director}</b> película(s) registrada(s). "
        "Este resultado debe interpretarse considerando la cantidad de películas disponibles por director, "
        "ya que un promedio alto con una sola película no tiene el mismo peso analítico que un promedio alto con varias producciones."
    )


def analisis_top_peliculas(top_imdb, title_col, imdb_col):
    if top_imdb is None or top_imdb.empty:
        return "No hay datos suficientes para analizar las películas mejor evaluadas."

    mejor_pelicula = top_imdb.iloc[0][title_col]
    mejor_nota = round(top_imdb.iloc[0][imdb_col], 2)

    return (
        f"La película mejor evaluada dentro del conjunto filtrado es <b>{mejor_pelicula}</b>, "
        f"con una calificación IMDb de <b>{mejor_nota}</b>. "
        "Este ranking permite destacar los títulos con mejor recepción del público dentro del catálogo analizado."
    )


def analisis_histograma_imdb(datos_histograma, imdb_col):
    if datos_histograma is None or datos_histograma.empty:
        return "No hay datos suficientes para analizar la distribución general de IMDb."

    promedio = round(datos_histograma[imdb_col].mean(), 2)
    mediana = round(datos_histograma[imdb_col].median(), 2)
    minimo = round(datos_histograma[imdb_col].min(), 2)
    maximo = round(datos_histograma[imdb_col].max(), 2)

    return (
        f"Las calificaciones IMDb presentan un promedio de <b>{promedio}</b> y una mediana de <b>{mediana}</b>. "
        f"El valor mínimo observado es <b>{minimo}</b> y el máximo es <b>{maximo}</b>. "
        "La comparación entre promedio y mediana ayuda a identificar si las evaluaciones se distribuyen de forma equilibrada "
        "o si existen valores extremos que influyen en el promedio general."
    )


def analisis_imdb_vs_metascore(datos_scatter, imdb_col, metascore_col):
    if datos_scatter is None or datos_scatter.empty:
        return "No hay datos suficientes para analizar la relación entre IMDb y Metascore."

    correlacion = datos_scatter[[imdb_col, metascore_col]].corr().iloc[0, 1]

    if pd.isna(correlacion):
        return "No se puede calcular una correlación válida entre IMDb y Metascore con los datos disponibles."

    correlacion = round(correlacion, 2)

    if correlacion >= 0.7:
        fuerza = "una relación positiva fuerte"
    elif correlacion >= 0.4:
        fuerza = "una relación positiva moderada"
    elif correlacion >= 0.2:
        fuerza = "una relación positiva débil"
    elif correlacion <= -0.4:
        fuerza = "una relación negativa relevante"
    else:
        fuerza = "una relación débil o poco evidente"

    return (
        f"La correlación entre IMDb y Metascore es de <b>{correlacion}</b>, lo que sugiere <b>{fuerza}</b>. "
        "Esto permite comparar si la valoración del público y la crítica especializada tienden a comportarse de manera similar."
    )