import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
 
# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Farm Analytics Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');
 
    :root {
        --bg: #080b12;
        --surface: #0f1320;
        --surface2: #161b2e;
        --accent: #4fffb0;
        --accent2: #ff5e7e;
        --accent3: #ffcb47;
        --accent4: #5b9cf6;
        --text: #cdd5e0;
        --muted: #4a5568;
        --border: #1e2540;
    }
 
    .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }
 
    /* main content padding */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 100% !important;
    }
 
    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--muted) !important;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    /* fix white selectbox */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: var(--surface2) !important;
        border-color: var(--border) !important;
        color: var(--text) !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: var(--text) !important;
    }
    /* slider accent color */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: var(--accent) !important;
    }
 
    /* ── KPI CARDS ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 16px 0 8px 0;
    }
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px 20px;
        position: relative;
        overflow: hidden;
        transition: border-color 0.2s;
    }
    .kpi-card:hover { border-color: #2e3a5a; }
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        opacity: 0.7;
    }
    .kpi-card.green::after  { background: var(--accent); }
    .kpi-card.red::after    { background: var(--accent2); }
    .kpi-card.yellow::after { background: var(--accent3); }
    .kpi-card.blue::after   { background: var(--accent4); }
 
    .kpi-icon {
        font-size: 18px;
        margin-bottom: 10px;
        display: block;
    }
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 24px;
        font-weight: 600;
        color: var(--text);
        line-height: 1;
        letter-spacing: -0.02em;
    }
    .kpi-value span {
        font-size: 13px;
        font-weight: 400;
        color: var(--muted);
        margin-left: 4px;
        letter-spacing: 0;
    }
 
    /* ── SECTION HEADERS ── */
    .section-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--accent);
        margin: 28px 0 12px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title::before {
        content: '';
        display: inline-block;
        width: 3px;
        height: 12px;
        background: var(--accent);
        border-radius: 2px;
    }
 
    /* ── DASHBOARD TITLE ── */
    .dash-header {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin-bottom: 4px;
    }
    .dash-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 22px;
        font-weight: 600;
        color: var(--text);
        letter-spacing: -0.03em;
    }
    .dash-badge {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        font-weight: 600;
        color: var(--accent);
        background: rgba(79, 255, 176, 0.08);
        border: 1px solid rgba(79, 255, 176, 0.2);
        border-radius: 4px;
        padding: 3px 8px;
        letter-spacing: 0.05em;
    }
    .dash-sub {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--muted);
        margin-top: 2px;
    }
 
    /* hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
 
    /* tighten chart containers */
    [data-testid="stPlotlyChart"] {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql("SELECT * FROM farm_data", conn)
    conn.close()
    return df
 
df = load_data()
 
# ─────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌾 Filters")
    st.markdown("---")
 
    # Crop type filter
    all_crops = ["All"] + sorted(df["Crop_Type"].unique().tolist())
    selected_crop = st.selectbox("Crop Type", all_crops)
 
    st.markdown("---")
 
    # Continuous range sliders
    yield_min, yield_max = float(df["Crop_Yield_ton"].min()), float(df["Crop_Yield_ton"].max())
    yield_range = st.slider(
        "Crop Yield (ton)",
        min_value=yield_min, max_value=yield_max,
        value=(yield_min, yield_max), step=0.1
    )
 
    sustain_min, sustain_max = float(df["Sustainability_Score"].min()), float(df["Sustainability_Score"].max())
    sustain_range = st.slider(
        "Sustainability Score",
        min_value=sustain_min, max_value=sustain_max,
        value=(sustain_min, sustain_max), step=0.5
    )
 
    soil_min, soil_max = float(df["Soil_pH"].min()), float(df["Soil_pH"].max())
    soil_range = st.slider(
        "Soil pH",
        min_value=soil_min, max_value=soil_max,
        value=(soil_min, soil_max), step=0.01
    )
 
    rainfall_min, rainfall_max = float(df["Rainfall_mm"].min()), float(df["Rainfall_mm"].max())
    rainfall_range = st.slider(
        "Rainfall (mm)",
        min_value=rainfall_min, max_value=rainfall_max,
        value=(rainfall_min, rainfall_max), step=1.0
    )
 
    st.markdown("---")
    st.markdown(f"<span style='color:#6b7280;font-size:12px;'>Showing filtered rows</span>", unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────
filtered = df.copy()
if selected_crop != "All":
    filtered = filtered[filtered["Crop_Type"] == selected_crop]
filtered = filtered[
    (filtered["Crop_Yield_ton"] >= yield_range[0]) & (filtered["Crop_Yield_ton"] <= yield_range[1]) &
    (filtered["Sustainability_Score"] >= sustain_range[0]) & (filtered["Sustainability_Score"] <= sustain_range[1]) &
    (filtered["Soil_pH"] >= soil_range[0]) & (filtered["Soil_pH"] <= soil_range[1]) &
    (filtered["Rainfall_mm"] >= rainfall_range[0]) & (filtered["Rainfall_mm"] <= rainfall_range[1])
]
 
# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div class="dash-title">🌾 Farm Analytics</div>
    <div class="dash-badge">LIVE</div>
</div>
<div class="dash-sub">{len(filtered):,} farms matching current filters</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
 
avg_yield      = filtered["Crop_Yield_ton"].mean()
avg_sustain    = filtered["Sustainability_Score"].mean()
avg_fertilizer = filtered["Fertilizer_Usage_kg"].mean()
avg_pesticide  = filtered["Pesticide_Usage_kg"].mean()
 
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card green">
        <div class="kpi-label">Avg Crop Yield</div>
        <div class="kpi-value">{avg_yield:.2f}<span>ton</span></div>
    </div>
    <div class="kpi-card yellow">
        <div class="kpi-label">Avg Sustainability</div>
        <div class="kpi-value">{avg_sustain:.1f}<span>/ 100</span></div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Avg Fertilizer</div>
        <div class="kpi-value">{avg_fertilizer:.1f}<span>kg</span></div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-label">Avg Pesticide</div>
        <div class="kpi-value">{avg_pesticide:.1f}<span>kg</span></div>
    </div>
</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────
# PLOTLY THEME (dark)
# ─────────────────────────────────────────
PLOT_THEME = dict(
    paper_bgcolor="#0f1320",
    plot_bgcolor="#0f1320",
    font=dict(color="#8892a4", family="Inter", size=12),
    title_font=dict(color="#cdd5e0", family="IBM Plex Mono", size=13),
    xaxis=dict(gridcolor="#1e2540", linecolor="#1e2540", tickfont=dict(color="#4a5568")),
    yaxis=dict(gridcolor="#1e2540", linecolor="#1e2540", tickfont=dict(color="#4a5568")),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="#1e2540",
        font=dict(color="#8892a4", size=11)
    ),
    margin=dict(l=40, r=20, t=40, b=40),
)
COLORS = ["#4fffb0", "#ff5e7e", "#ffcb47", "#5b9cf6"]
 
# ─────────────────────────────────────────
# ROW 1 — Yield analysis + Crop distribution
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Crop Yield Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
 
with col1:
    # Bar chart — avg yield by crop type
    yield_by_crop = filtered.groupby("Crop_Type")["Crop_Yield_ton"].mean().reset_index()
    yield_by_crop.columns = ["Crop_Type", "Avg_Yield"]
    fig = px.bar(
        yield_by_crop, x="Crop_Type", y="Avg_Yield",
        color="Crop_Type", color_discrete_sequence=COLORS,
        title="Average Yield by Crop Type"
    )
    fig.update_traces(width=0.5)
    fig.update_layout(**PLOT_THEME, showlegend=False,
                      xaxis_title="", yaxis_title="tons")
    st.plotly_chart(fig, use_container_width=True)
 
with col2:
    # Pie chart — crop type distribution
    crop_counts = filtered["Crop_Type"].value_counts().reset_index()
    crop_counts.columns = ["Crop_Type", "Count"]
    fig2 = px.pie(
        crop_counts, names="Crop_Type", values="Count",
        color_discrete_sequence=COLORS,
        title="Crop Type Distribution",
        hole=0.4
    )
    fig2.update_layout(**PLOT_THEME, title_font=dict(size=13, color="#cdd5e0"),
                       legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5,
                                   font=dict(color="#8892a4", size=11), bgcolor="rgba(0,0,0,0)"))
    fig2.update_traces(textfont_color="#cdd5e0", textfont_size=12)
    st.plotly_chart(fig2, use_container_width=True)
 
# ─────────────────────────────────────────
# ROW 2 — Histograms
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Distributions</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
 
with col3:
    fig3 = px.histogram(
        filtered, x="Crop_Yield_ton", color="Crop_Type",
        color_discrete_sequence=COLORS, nbins=40,
        title="Crop Yield Distribution", barmode="overlay", opacity=0.7
    )
    fig3.update_layout(**PLOT_THEME, xaxis_title="yield (ton)", yaxis_title="count")
    st.plotly_chart(fig3, use_container_width=True)
 
with col4:
    fig4 = px.histogram(
        filtered, x="Sustainability_Score", color="Crop_Type",
        color_discrete_sequence=COLORS, nbins=40,
        title="Sustainability Score Distribution", barmode="overlay", opacity=0.7
    )
    fig4.update_layout(**PLOT_THEME, xaxis_title="score", yaxis_title="count")
    st.plotly_chart(fig4, use_container_width=True)
 
# ─────────────────────────────────────────
# ROW 3 — Scatter plots
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Soil & Weather vs Yield</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)
 
with col5:
    fig5 = px.scatter(
        filtered, x="Soil_pH", y="Crop_Yield_ton",
        color="Crop_Type", color_discrete_sequence=COLORS,
        opacity=0.4, title="Soil pH vs Crop Yield"
    )
    fig5.update_layout(**PLOT_THEME, xaxis_title="soil pH", yaxis_title="yield (ton)")
    st.plotly_chart(fig5, use_container_width=True)
 
with col6:
    fig6 = px.scatter(
        filtered, x="Rainfall_mm", y="Crop_Yield_ton",
        color="Crop_Type", color_discrete_sequence=COLORS,
        opacity=0.4, title="Rainfall vs Crop Yield"
    )
    fig6.update_layout(**PLOT_THEME, xaxis_title="rainfall (mm)", yaxis_title="yield (ton)")
    st.plotly_chart(fig6, use_container_width=True)
 
# ─────────────────────────────────────────
# ROW 4 — Fertilizer & Pesticide
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Fertilizer & Pesticide Usage</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)
 
with col7:
    fert_by_crop = filtered.groupby("Crop_Type")["Fertilizer_Usage_kg"].mean().reset_index()
    fig7 = px.bar(
        fert_by_crop, x="Crop_Type", y="Fertilizer_Usage_kg",
        color="Crop_Type", color_discrete_sequence=COLORS,
        title="Avg Fertilizer Usage by Crop Type"
    )
    fig7.update_traces(width=0.5)
    fig7.update_layout(**PLOT_THEME, showlegend=False, xaxis_title="", yaxis_title="kg")
    st.plotly_chart(fig7, use_container_width=True)
 
with col8:
    fig8 = px.scatter(
        filtered, x="Fertilizer_Usage_kg", y="Crop_Yield_ton",
        color="Crop_Type", color_discrete_sequence=COLORS,
        opacity=0.4, title="Fertilizer Usage vs Crop Yield"
    )
    fig8.update_layout(**PLOT_THEME, xaxis_title="fertilizer (kg)", yaxis_title="yield (ton)")
    st.plotly_chart(fig8, use_container_width=True)
 
# ─────────────────────────────────────────
# ROW 5 — Sustainability
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Sustainability Score Trends</div>', unsafe_allow_html=True)
col9, col10 = st.columns(2)
 
with col9:
    sustain_by_crop = filtered.groupby("Crop_Type")["Sustainability_Score"].mean().reset_index()
    fig9 = px.bar(
        sustain_by_crop, x="Crop_Type", y="Sustainability_Score",
        color="Crop_Type", color_discrete_sequence=COLORS,
        title="Avg Sustainability Score by Crop Type"
    )
    fig9.update_traces(width=0.5)
    fig9.update_layout(**PLOT_THEME, showlegend=False, xaxis_title="", yaxis_title="score")
    st.plotly_chart(fig9, use_container_width=True)
 
with col10:
    fig10 = px.scatter(
        filtered, x="Pesticide_Usage_kg", y="Sustainability_Score",
        color="Crop_Type", color_discrete_sequence=COLORS,
        opacity=0.4, title="Pesticide Usage vs Sustainability Score"
    )
    fig10.update_layout(**PLOT_THEME, xaxis_title="pesticide (kg)", yaxis_title="sustainability score")
    st.plotly_chart(fig10, use_container_width=True)
 
# ─────────────────────────────────────────
# RAW DATA TABLE
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Raw Data</div>', unsafe_allow_html=True)
with st.expander("View filtered data table"):
    st.dataframe(filtered, use_container_width=True, height=400)
    st.markdown(f"<span style='color:#6b7280;font-size:12px;'>{len(filtered):,} rows</span>",
                unsafe_allow_html=True)