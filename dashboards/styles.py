import streamlit as st

PALETA_BARRAS = [
    "#EF4444", "#F59E0B", "#FACC15", "#22C55E", "#3B82F6",
    "#8B5CF6", "#EC4899", "#14B8A6", "#F97316", "#06B6D4"
]

COLOR_FONDO = "#0F172A"
COLOR_CARD = "#111827"
COLOR_TEXTO = "#F8FAFC"
COLOR_TEXTO_SUAVE = "#CBD5E1"
COLOR_GRILLA = "#334155"
# Tamaños de fuente
TAMANO_ENCABEZADO = 90
TAMANO_SUBTITULO = 28
TAMANO_FUENTE = 22
TAMANO_H2 = 46
TAMANO_H3 = 36

st.markdown(f"""
<style>

h1 {{
    font-size:{TAMANO_H2}px !important;
    font-weight:800 !important;
}}

h2 {{
    font-size:{TAMANO_H2}px !important;
}}

h3 {{
    font-size:{TAMANO_H3}px !important;
}}

p {{
    font-size:{TAMANO_FUENTE}px !important;
}}

.hero-title {{
    font-size:{TAMANO_ENCABEZADO}px !important;
    font-weight:900 !important;
    color:#FFFFFF !important;
    line-height:1.05;
    margin-bottom:18px;
}}

.hero-subtitle {{
    font-size:{TAMANO_SUBTITULO}px !important;
    color:#CBD5E1 !important;
    line-height:1.7;
}}

.hero-source {{
    font-size:20px !important;
    color:#94A3B8 !important;
}}

</style>
""", unsafe_allow_html=True)


def aplicar_estilo_grafico(fig):

    fig.update_layout(
        font=dict(
            size=20,
            color=COLOR_TEXTO
        ),

        title_font=dict(
            size=30,
            color=COLOR_TEXTO
        ),

        xaxis_title_font=dict(
            size=22,
            color=COLOR_TEXTO_SUAVE
        ),

        yaxis_title_font=dict(
            size=22,
            color=COLOR_TEXTO_SUAVE
        ),

        legend_font=dict(
            size=18,
            color=COLOR_TEXTO
        ),

        plot_bgcolor=COLOR_FONDO,
        paper_bgcolor=COLOR_FONDO,

        margin=dict(
            l=70,
            r=70,
            t=100,
            b=100
        )
    )

    fig.update_xaxes(
        tickfont=dict(
            size=18,
            color=COLOR_TEXTO_SUAVE
        ),
        showgrid=True,
        gridcolor=COLOR_GRILLA
    )

    fig.update_yaxes(
        tickfont=dict(
            size=18,
            color=COLOR_TEXTO_SUAVE
        ),
        showgrid=True,
        gridcolor=COLOR_GRILLA
    )

    fig.update_traces(
        textfont=dict(
            size=20,
            color=COLOR_TEXTO
        ),
        cliponaxis=False
    )

    return fig

def mostrar_encabezado():
    st.markdown("""
    <div style="padding: 20px 0 35px 0;">

        <div style="
            font-size: 90px;
            font-weight: 900;
            color: #FFFFFF;
            line-height: 1.05;
            letter-spacing: -2px;
            margin-bottom: 20px;
        ">
            🎬 Dashboard de Películas Netflix + OMDb
        </div>

        <div style="
            font-size: 30px;
            color: #CBD5E1;
            line-height: 1.7;
            max-width: 1500px;
            margin-bottom: 18px;
        ">
            Este dashboard integra información del catálogo de Netflix con datos complementarios obtenidos desde OMDb.
            El objetivo es analizar el comportamiento del catálogo según año, país, género, calificaciones,
            directores, votos y premios.
        </div>

        <div style="
            font-size: 22px;
            color: #94A3B8;
            margin-top: 8px;
        ">
            Fuente de datos: Netflix Dataset + OMDb API + Supabase
        </div>

    </div>
    """, unsafe_allow_html=True)