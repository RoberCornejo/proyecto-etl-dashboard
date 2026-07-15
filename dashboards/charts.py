import pandas as pd
import plotly.express as px

from dashboards.styles import aplicar_estilo_grafico, PALETA_BARRAS, NETFLIX_RED, ACCENT


def grafico_peliculas_por_anio(df, year_col):
    datos = (
        df[year_col]
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )
    datos.columns = ["Año", "Cantidad"]

    fig = px.line(
        datos,
        x="Año",
        y="Cantidad",
        markers=True,
        title="Evolución de películas por año",
        labels={
            "Año": "Año de estreno",
            "Cantidad": "Cantidad de películas"
        }
    )

    fig.update_traces(
        line=dict(color=ACCENT, width=3),
        marker=dict(size=8, color=NETFLIX_RED),
        hovertemplate=None,
        mode='lines+markers'
    )

    return aplicar_estilo_grafico(fig), datos


def grafico_top_paises(df, country_col):
    datos = (
        df[country_col]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )
    datos.columns = ["País", "Cantidad"]

    fig = px.bar(
        datos,
        x="País",
        y="Cantidad",
        text="Cantidad",
        title="Top 10 países con más películas",
        labels={
            "País": "País",
            "Cantidad": "Cantidad de películas"
        }
    )

    fig.update_traces(
        marker_color=PALETA_BARRAS[:len(datos)],
        textposition="outside",
        texttemplate='%{y}',
        hovertemplate=None,
        textfont=dict(color='white', size=12),
        cliponaxis=False
    )

    return aplicar_estilo_grafico(fig), datos


def grafico_top_generos(df, genre_col):
    generos = df[genre_col].dropna().str.split(", ").explode()

    datos = generos.value_counts().head(10).reset_index()
    datos.columns = ["Género", "Cantidad"]

    fig = px.bar(
        datos,
        x="Género",
        y="Cantidad",
        text="Cantidad",
        title="Top 10 géneros más frecuentes",
        labels={
            "Género": "Género",
            "Cantidad": "Cantidad de películas"
        }
    )

    fig.update_traces(
        marker_color=PALETA_BARRAS[:len(datos)],
        textposition="outside",
        texttemplate='%{y}',
        hovertemplate=None,
        textfont=dict(color='white', size=12),
        cliponaxis=False
    )

    return aplicar_estilo_grafico(fig), datos


def grafico_distribucion_imdb(df, imdb_col):
    df_imdb = df.dropna(subset=[imdb_col]).copy()

    bins = [0, 4, 5, 6, 7, 8, 10]
    labels = ["0-4", "4-5", "5-6", "6-7", "7-8", "8-10"]

    df_imdb["Rango IMDb"] = pd.cut(
        df_imdb[imdb_col],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    datos = df_imdb["Rango IMDb"].value_counts().sort_index().reset_index()
    datos.columns = ["Rango IMDb", "Cantidad"]

    fig = px.bar(
        datos,
        x="Rango IMDb",
        y="Cantidad",
        text="Cantidad",
        title="Películas por rango de calificación IMDb",
        labels={
            "Rango IMDb": "Rango de calificación IMDb",
            "Cantidad": "Cantidad de películas"
        }
    )

    fig.update_traces(
        marker_color=PALETA_BARRAS[:len(datos)],
        textposition="outside",
        texttemplate='%{y}',
        hovertemplate=None,
        textfont=dict(color='white', size=12),
        cliponaxis=False
    )

    return aplicar_estilo_grafico(fig), datos


def grafico_directores_mejor_evaluados(df, director_col, imdb_col, title_col):
    directores = (
        df
        .dropna(subset=[director_col, imdb_col])
        .groupby(director_col, as_index=False)
        .agg(
            Promedio_IMDb=(imdb_col, "mean"),
            Cantidad_peliculas=(title_col, "count")
        )
    )

    directores = directores.sort_values("Promedio_IMDb", ascending=False).head(10)
    directores["Promedio texto"] = directores["Promedio_IMDb"].round(2)

    fig = px.bar(
        directores,
        x="Promedio_IMDb",
        y=director_col,
        orientation="h",
        text="Promedio texto",
        title="Top 10 directores por promedio IMDb",
        labels={
            "Promedio_IMDb": "Promedio IMDb",
            director_col: "Director",
            "Cantidad_peliculas": "Cantidad de películas"
        },
        hover_data=["Cantidad_peliculas"]
    )

    fig.update_traces(
        marker_color=PALETA_BARRAS[:len(directores)],
        textposition="outside",
        texttemplate='%{x:.2f}',
        hovertemplate=None,
        textfont=dict(color='white', size=12),
        cliponaxis=False
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=560,
        margin=dict(l=230, r=80, t=90, b=80)
    )

    fig = aplicar_estilo_grafico(fig)

    return fig, directores


def grafico_top_peliculas_imdb(df, title_col, imdb_col):
    datos = (
        df
        .dropna(subset=[title_col, imdb_col])
        .sort_values(imdb_col, ascending=False)
        .head(10)
        .copy()
    )

    datos["IMDb texto"] = datos[imdb_col].round(2)

    fig = px.bar(
        datos,
        x=imdb_col,
        y=title_col,
        orientation="h",
        text="IMDb texto",
        title="Top 10 películas por IMDb",
        labels={
            imdb_col: "Calificación IMDb",
            title_col: "Película"
        }
    )

    fig.update_traces(
        marker_color=PALETA_BARRAS[:len(datos)],
        textposition="outside",
        texttemplate='%{x:.2f}',
        hovertemplate=None,
        textfont=dict(color='white', size=12),
        cliponaxis=False
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return aplicar_estilo_grafico(fig), datos


def grafico_histograma_imdb(df, imdb_col):
    datos = df.dropna(subset=[imdb_col]).copy()

    fig = px.histogram(
        datos,
        x=imdb_col,
        nbins=15,
        title="Distribución general de calificaciones IMDb",
        labels={
            imdb_col: "Calificación IMDb"
        }
    )

    colores = [
        "#ef4444",
        "#f97316",
        "#f59e0b",
        "#eab308",
        "#84cc16",
        "#22c55e",
        "#14b8a6",
        "#06b6d4",
        "#3b82f6",
        "#6366f1",
        "#8b5cf6",
        "#a855f7",
        "#d946ef",
        "#ec4899",
        "#f43f5e"
    ]

    for i, barra in enumerate(fig.data):
        barra.marker.color = colores[i % len(colores)]
        barra.marker.line.width = 0
        # show value labels on histogram bars is not typical; rely on hover

    fig.update_layout(
        bargap=0.03
    )

    return aplicar_estilo_grafico(fig), datos


def grafico_imdb_vs_metascore(df, imdb_col, metascore_col, title_col):
    datos = df.dropna(subset=[imdb_col, metascore_col]).copy()

    fig = px.scatter(
        datos,
        x=metascore_col,
        y=imdb_col,
        hover_name=title_col if title_col in datos.columns else None,
        title="Relación entre Metascore e IMDb",
        labels={
            metascore_col: "Metascore",
            imdb_col: "Calificación IMDb"
        }
    )

    fig.update_traces(
        marker=dict(
            size=9,
            color=ACCENT,
            opacity=0.85,
            line=dict(width=0)
        ),
        hovertemplate='<b>%{hovertext}</b><br>IMDb: %{y}<br>Metascore: %{x}',
        hoverlabel=dict(font=dict(size=12))
    )

    return aplicar_estilo_grafico(fig), datos