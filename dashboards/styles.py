import streamlit as st

# Palette and theme
NETFLIX_RED = "#E50914"
SECONDARY = "#564D80"
ACCENT = "#00D4FF"
DARK_BG = "#0B1020"
CARD_BG = "#141B2D"
TEXT = "#F8FAFC"
TEXT_SUB = "#CBD5E1"
CARD_RADIUS = "12px"

PALETA_BARRAS = [
    NETFLIX_RED, "#F59E0B", "#FACC15", "#22C55E", "#3B82F6",
    "#8B5CF6", "#EC4899", "#14B8A6", "#F97316", ACCENT
]


def aplicar_estilo_dashboard():
    """Inyecta CSS global para el tema corporativo y define clases para tarjetas KPI."""
    css = f"""
    <style>
    /* Root */
    .stApp {{
        background-color: {DARK_BG};
        color: {TEXT};
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }}

    /* Header / Hero */
    .hero {{
        padding: 24px 6px 12px 6px;
    }}

    .hero-title {{
        font-size: 56px;
        font-weight: 800;
        color: {TEXT};
        margin: 0 0 6px 0;
    }}

    .hero-subtitle {{
        font-size: 18px;
        color: {TEXT_SUB};
        margin: 0 0 8px 0;
    }}

    .hero-meta {{
        font-size: 14px;
        color: #94A3B8;
    }}

    /* KPI cards */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-top: 18px;
    }}

    .kpi-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.02));
        border-radius: {CARD_RADIUS};
        padding: 18px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.6);
        border: 1px solid rgba(255,255,255,0.03);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .kpi-icon {{
        font-size: 20px;
        margin-bottom: 6px;
    }}

    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        color: {TEXT};
    }}

    .kpi-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(2,6,23,0.75);
    }}

    .kpi-label {{
        font-size: 13px;
        color: {TEXT_SUB};
    }}

    /* Sidebar */
    .css-1d391kg {{ /* streamlit sidebar override hook */
        background-color: {CARD_BG} !important;
        border-radius: 12px;
        padding: 12px !important;
    }}

    /* Separators and headings */
    .section-title {{
        font-size: 20px;
        color: {TEXT};
        margin: 6px 0 12px 0;
        font-weight: 700;
    }}

    .section {{
        background: transparent;
        padding: 12px 0 22px 0;
    }}

    /* Responsive adjustments */
    @media (max-width: 1100px) {{
        .hero-title {{ font-size: 44px; }}
        .kpi-value {{ font-size: 24px; }}
        .kpi-grid {{ grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    }}

    @media (max-width: 720px) {{
        .hero-title {{ font-size: 32px; }}
        .kpi-value {{ font-size: 20px; }}
        .kpi-grid {{ grid-template-columns: repeat(1, 1fr); gap: 10px; }}
        .hero-subtitle {{ font-size: 14px; }}
    }}

    /* Ensure tables look good */
    .stDataFrame table {{
        background: transparent;
    }}

    /* Chart card */
    .chart-card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.02));
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(2,6,23,0.6);
        border: 1px solid rgba(255,255,255,0.035);
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def aplicar_estilo_grafico(fig):
    """Aplica estilo consistente a figuras Plotly para el tema oscuro.

    Hace fondos transparentes para integrarse con tarjetas y usa la paleta definida.
    """

    fig.update_layout(
        font=dict(
            family="Segoe UI, Roboto, Helvetica, Arial",
            size=12,
            color=TEXT
        ),
        title_font=dict(
            size=18,
            color=TEXT
        ),
        legend_font=dict(
            size=12,
            color=TEXT
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=24, t=72, b=40),
        hovermode='closest'
    )

    fig.update_xaxes(
        tickfont=dict(size=11, color=TEXT_SUB),
        title_font=dict(size=12, color=TEXT_SUB),
        gridcolor='rgba(255,255,255,0.03)'
    )

    fig.update_yaxes(
        tickfont=dict(size=11, color=TEXT_SUB),
        title_font=dict(size=12, color=TEXT_SUB),
        gridcolor='rgba(255,255,255,0.03)'
    )

    # Apply marker/trace defaults
    for trace in fig.data:
        if 'marker' in trace:
            trace.marker.line = dict(width=0)

    return fig