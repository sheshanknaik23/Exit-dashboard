import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Exit Analytics · JoulestoWatts",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background: #0F172A !important;
}
.block-container {
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(99,179,237,0.15) !important;
}
[data-testid="stSidebar"] * { color: #a0aec0 !important; }
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #63b3ed !important;
    font-size: 13px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
}

/* ── Multiselect tags ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(99,179,237,0.2) !important;
    border: 1px solid rgba(99,179,237,0.4) !important;
    color: #63b3ed !important;
}
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background: #0d1220 !important;
    border-color: rgba(99,179,237,0.2) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] button {
    color: #4a5568 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #63b3ed !important;
    border-bottom: 2px solid #63b3ed !important;
    background: transparent !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(99,179,237,0.1) !important;
}

/* ── KPI ROW 1 — big cards ── */
.kpi-big {
    background: #1E293B;
    border: 1px solid rgba(99,179,237,0.18);
    border-radius: 16px;
    padding: 22px 24px 18px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
    height: 130px;
}
.kpi-big:hover {
    transform: translateY(-2px);
    border-color: rgba(99,179,237,0.4);
}
.kpi-big .accent-bar {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 16px 0 0 16px;
}
.kpi-big .icon {
    font-size: 22px;
    position: absolute;
    right: 20px;
    top: 20px;
    opacity: 0.35;
}
.kpi-big .label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #4a6080;
    margin-bottom: 10px;
    padding-left: 12px;
}
.kpi-big .value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 30px;
    font-weight: 700;
    color: #e2e8f0;
    padding-left: 12px;
    line-height: 1;
}
.kpi-big .sub {
    font-size: 11px;
    color: #4a6080;
    padding-left: 12px;
    margin-top: 8px;
}

/* ── KPI ROW 2 — small cards ── */
.kpi-sm {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
}
.kpi-sm .accent-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    vertical-align: middle;
}
.kpi-sm .label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a6080;
    margin-bottom: 8px;
}
.kpi-sm .value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 22px;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1;
}

/* ── Section headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2.2rem 0 1rem 0;
}
.sec-head .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #63b3ed;
    box-shadow: 0 0 8px #63b3ed;
    flex-shrink: 0;
}
.sec-head .title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #63b3ed;
    white-space: nowrap;
}
.sec-head .line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,179,237,0.3), transparent);
}

/* ── Chart card wrapper ── */
.chart-card {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    overflow: hidden;
    padding: 4px 4px 0 4px;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(99,179,237,0.1);
    margin-bottom: 0.5rem;
}
.page-title {
    font-size: 22px;
    font-weight: 800;
    color: #e2e8f0;
    letter-spacing: -0.5px;
}
.page-sub {
    font-size: 12px;
    color: #2d4a6a;
    margin-top: 3px;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge {
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.25);
    color: #63b3ed;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
}

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHART DEFAULTS
# ─────────────────────────────────────────────
COLORS = ["#63b3ed","#68d391","#f6ad55","#fc8181","#b794f4","#76e4f7","#faf089","#f687b3","#9ae6b4","#90cdf4"]

def chart_layout(title="", h=320):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#4a6080", size=11),
        title=dict(text=title, font=dict(size=13, color="#a0aec0", family="Inter"), x=0.02, y=0.97),
        margin=dict(l=10, r=10, t=40, b=10),
        height=h,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#718096", size=11),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.06)",
                   tickfont=dict(color="#4a6080", size=10), showline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.06)",
                   tickfont=dict(color="#4a6080", size=10), showline=False),
    )

# ─────────────────────────────────────────────
# MONTH SORT
# ─────────────────────────────────────────────
MONTH_ORDER = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
               "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

def msort(m):
    try:
        p = str(m).replace("\u2019","'").split("'")
        return int(p[1])*100 + MONTH_ORDER.get(p[0][:3], 0)
    except: return 0

# ─────────────────────────────────────────────
# FILE PATH  ← YOUR PATH
# ─────────────────────────────────────────────
FILE_PATH = r"C:\Users\E36250348\OneDrive - JoulestoWatts Business Solutions Pvt Ltd\Desktop\Exit Dashboard\Exit & Exit Pip.xlsx"

@st.cache_data(ttl=300)
def load_data(path):
    xl = pd.ExcelFile(path)
    exit_df = xl.parse("Exit")
    pipe_df = xl.parse("Exit Pipeline")
    org_df  = xl.parse("Org Mapping")

    for df in [exit_df, pipe_df, org_df]:
        df.columns = df.columns.str.strip()

    org_df["Domain"] = org_df["Domain"].str.strip().str.title()
    org_slim = org_df[["Client","Domain","Business Head"]].drop_duplicates("Client")

    exit_df = exit_df.merge(org_slim, left_on="company_name", right_on="Client", how="left")
    pipe_df = pipe_df.merge(org_slim, left_on="company_name", right_on="Client", how="left")

    for df in [exit_df, pipe_df]:
        if "Business Head" not in df.columns:
            df["Business Head"] = df.get("BH", pd.NA)
        else:
            df["Business Head"] = df["Business Head"].fillna(df.get("BH", pd.NA))
        df["p_o_value"] = pd.to_numeric(df["p_o_value"], errors="coerce").fillna(0)
        df["margin"]    = pd.to_numeric(df["margin"],    errors="coerce").fillna(0)
        df["Month"]     = df["Month"].astype(str).str.strip()

    exit_df["last_work_day"]       = pd.to_datetime(exit_df["last_work_day"], errors="coerce")
    pipe_df["tentative_exit_date"] = pd.to_datetime(pipe_df["tentative_exit_date"], errors="coerce")
    return exit_df, pipe_df, org_df

try:
    exit_df, pipe_df, org_df = load_data(FILE_PATH)
except FileNotFoundError:
    st.error(f"❌ File not found: **{FILE_PATH}**"); st.stop()
except Exception as e:
    st.error(f"❌ Error: {e}"); st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ EXIT ANALYTICS")
    st.markdown("---")

    bh_all = sorted(set(exit_df["Business Head"].dropna()) | set(pipe_df["Business Head"].dropna()))
    bh_sel = st.multiselect("👤  Business Head", bh_all, placeholder="All")

    domain_all = sorted(set(exit_df["Domain"].dropna()) | set(pipe_df["Domain"].dropna()))
    domain_sel = st.multiselect("🏢  Domain", domain_all, placeholder="All")

    client_all = sorted(set(exit_df["company_name"].dropna()) | set(pipe_df["company_name"].dropna()))
    client_sel = st.multiselect("🏭  Client", client_all, placeholder="All")

    all_months = sorted(set(exit_df["Month"].dropna()) | set(pipe_df["Month"].dropna()), key=msort)
    month_sel  = st.multiselect("📅  Month", all_months, placeholder="All")

    st.markdown("---")
    if st.button("🔄  Refresh Data", use_container_width=True):
        st.cache_data.clear(); st.rerun()

    st.markdown(f"""
    <div style="margin-top:2rem;padding:12px;background:rgba(99,179,237,0.05);
         border-radius:8px;border:1px solid rgba(99,179,237,0.1);">
        <div style="font-size:10px;color:#2d4a6a;letter-spacing:2px;text-transform:uppercase;
             font-weight:600;margin-bottom:6px;">DATA SOURCE</div>
        <div style="font-size:11px;color:#4a6080;">Exit & Exit Pip.xlsx</div>
        <div style="font-size:10px;color:#2d4a6a;margin-top:4px;">Auto-refresh: 5 min</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
def filt(df):
    f = df.copy()
    if bh_sel:     f = f[f["Business Head"].isin(bh_sel)]
    if domain_sel: f = f[f["Domain"].isin(domain_sel)]
    if client_sel: f = f[f["company_name"].isin(client_sel)]
    if month_sel:  f = f[f["Month"].isin(month_sel)]
    return f

ef = filt(exit_df)
pf = filt(pipe_df)

# ─────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────
total_exits     = len(ef)
total_pipeline  = len(pf)
total_employees = total_exits + total_pipeline
projection_po   = pf["p_o_value"].sum()
projection_mar  = pf["margin"].sum()
total_po        = ef["p_o_value"].sum() + pf["p_o_value"].sum()
total_margin    = ef["margin"].sum() + pf["margin"].sum()
exit_po         = ef["p_o_value"].sum()
exit_margin     = ef["margin"].sum()

# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div>
        <div class="page-title">⚡ Exit Analytics Dashboard</div>
        <div class="page-sub">JoulestoWatts Business Solutions · Real-time Intelligence</div>
    </div>
    <div>
        <span class="badge">LIVE DATA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 1 — PRIMARY KPIs (5 big cards)
# ─────────────────────────────────────────────
def big_kpi(col, label, value, sub, accent, icon):
    col.markdown(f"""
    <div class="kpi-big">
        <div class="accent-bar" style="background:{accent};box-shadow:0 0 12px {accent}55;"></div>
        <div class="icon">{icon}</div>
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def sm_kpi(col, label, value, dot_color):
    col.markdown(f"""
    <div class="kpi-sm">
        <div class="label"><span class="accent-dot" style="background:{dot_color};box-shadow:0 0 6px {dot_color};"></span>{label}</div>
        <div class="value">{value}</div>
    </div>""", unsafe_allow_html=True)

def sec(title):
    st.markdown(f"""
    <div class="sec-head">
        <div class="dot"></div>
        <div class="title">{title}</div>
        <div class="line"></div>
    </div>""", unsafe_allow_html=True)

sec("KEY METRICS")

r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)
big_kpi(r1c1, "Total Exits",     f"{total_exits:,}",     f"Confirmed exits",                "#fc8181","🚪")
big_kpi(r1c2, "Exit Pipeline",   f"{total_pipeline:,}",  f"At-risk headcount",              "#f6ad55","⚠️")
big_kpi(r1c3, "Projection",      f"₹{projection_po:,.0f}", f"Pipeline P.O · Margin ₹{projection_mar:,.0f}", "#b794f4","📈")
big_kpi(r1c4, "Total Headcount", f"{total_employees:,}", f"Exit + Pipeline combined",       "#63b3ed","👥")
big_kpi(r1c5, "Total P.O Value", f"₹{total_po:,.0f}",   f"Margin ₹{total_margin:,.0f}",    "#68d391","💰")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ROW 2 — SECONDARY KPIs (P.O & Margin split)
r2c1, r2c2, r2c3, r2c4 = st.columns(4)
sm_kpi(r2c1, "Exit P.O Value",      f"₹{exit_po:,.0f}",      "#fc8181")
sm_kpi(r2c2, "Exit Margin",         f"₹{exit_margin:,.0f}",  "#f6ad55")
sm_kpi(r2c3, "Pipeline P.O Value",  f"₹{projection_po:,.0f}","#b794f4")
sm_kpi(r2c4, "Pipeline Margin",     f"₹{projection_mar:,.0f}","#68d391")

# ─────────────────────────────────────────────
# ROW 3 — CLIENT WISE
# ─────────────────────────────────────────────
sec("CLIENT WISE ANALYSIS")

cc1, cc2 = st.columns(2)

with cc1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    top_c = (ef.groupby("company_name").size()
               .reset_index(name="Exits").sort_values("Exits").tail(12))
    fig = go.Figure(go.Bar(
        x=top_c["Exits"], y=top_c["company_name"],
        orientation="h",
        marker=dict(
            color=top_c["Exits"],
            colorscale=[[0,"#0d2040"],[0.5,"#2b6cb0"],[1,"#63b3ed"]],
            line=dict(width=0)
        ),
        text=top_c["Exits"], textposition="outside",
        textfont=dict(color="#63b3ed", size=10)
    ))
    fig.update_layout(**chart_layout("Top Clients · Exit Count", h=380))
    fig.update_xaxes(showticklabels=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with cc2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    top_po = (ef.groupby("company_name")["p_o_value"].sum()
                .reset_index(name="PO").sort_values("PO").tail(12))
    fig2 = go.Figure(go.Bar(
        x=top_po["PO"], y=top_po["company_name"],
        orientation="h",
        marker=dict(
            color=top_po["PO"],
            colorscale=[[0,"#1a0d33"],[0.5,"#553c9a"],[1,"#b794f4"]],
            line=dict(width=0)
        ),
        text=[f"₹{v:,.0f}" for v in top_po["PO"]],
        textposition="outside",
        textfont=dict(color="#b794f4", size=10)
    ))
    fig2.update_layout(**chart_layout("Top Clients · P.O Value", h=380))
    fig2.update_xaxes(showticklabels=False)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 4 — BUSINESS HEAD WISE
# ─────────────────────────────────────────────
sec("BUSINESS HEAD WISE ANALYSIS")

bc1, bc2, bc3 = st.columns(3)

with bc1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bh_exit = (ef.groupby("Business Head").size()
                 .reset_index(name="Exits").sort_values("Exits"))
    fig3 = go.Figure(go.Bar(
        x=bh_exit["Exits"], y=bh_exit["Business Head"],
        orientation="h",
        marker=dict(color=COLORS[:len(bh_exit)], line=dict(width=0)),
        text=bh_exit["Exits"], textposition="outside",
        textfont=dict(size=10, color="#a0aec0")
    ))
    fig3.update_layout(**chart_layout("Exits by Business Head", h=320))
    fig3.update_xaxes(showticklabels=False)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with bc2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bh_po = (ef.groupby("Business Head")["p_o_value"].sum()
               .reset_index(name="PO").sort_values("PO"))
    fig4 = go.Figure(go.Bar(
        x=bh_po["PO"], y=bh_po["Business Head"],
        orientation="h",
        marker=dict(color=COLORS[:len(bh_po)], line=dict(width=0)),
        text=[f"₹{v/1e5:.1f}L" for v in bh_po["PO"]],
        textposition="outside",
        textfont=dict(size=10, color="#a0aec0")
    ))
    fig4.update_layout(**chart_layout("P.O Value by Business Head", h=320))
    fig4.update_xaxes(showticklabels=False)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with bc3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bh_pipe = (pf.groupby("Business Head").size()
                 .reset_index(name="Pipeline").sort_values("Pipeline"))
    fig5 = go.Figure(go.Bar(
        x=bh_pipe["Pipeline"], y=bh_pipe["Business Head"],
        orientation="h",
        marker=dict(color=COLORS[2:2+len(bh_pipe)], line=dict(width=0)),
        text=bh_pipe["Pipeline"], textposition="outside",
        textfont=dict(size=10, color="#a0aec0")
    ))
    fig5.update_layout(**chart_layout("Pipeline by Business Head", h=320))
    fig5.update_xaxes(showticklabels=False)
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 5 — DOMAIN WISE
# ─────────────────────────────────────────────
sec("DOMAIN WISE ANALYSIS")

dc1, dc2, dc3 = st.columns(3)

with dc1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    dom_exit = ef["Domain"].value_counts().reset_index()
    dom_exit.columns = ["Domain","Count"]
    fig6 = go.Figure(go.Pie(
        labels=dom_exit["Domain"], values=dom_exit["Count"],
        hole=0.55,
        marker=dict(colors=COLORS[:len(dom_exit)],
                    line=dict(color="#070b14", width=3)),
        textfont=dict(color="#e2e8f0", size=11),
        textinfo="label+percent"
    ))
    fig6.update_layout(**chart_layout("Exits by Domain", h=300))
    fig6.update_layout(showlegend=False)
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with dc2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    dom_po = (ef.groupby("Domain")["p_o_value"].sum()
                .reset_index(name="PO").sort_values("PO", ascending=False))
    fig7 = go.Figure(go.Bar(
        x=dom_po["Domain"], y=dom_po["PO"],
        marker=dict(color=COLORS[:len(dom_po)], line=dict(width=0)),
        text=[f"₹{v/1e5:.1f}L" for v in dom_po["PO"]],
        textposition="outside",
        textfont=dict(size=10, color="#a0aec0")
    ))
    fig7.update_layout(**chart_layout("P.O Value by Domain", h=300))
    fig7.update_yaxes(showticklabels=False)
    st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with dc3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    dom_mar = (ef.groupby("Domain")["margin"].sum()
                 .reset_index(name="Margin").sort_values("Margin", ascending=False))
    fig8 = go.Figure(go.Bar(
        x=dom_mar["Domain"], y=dom_mar["Margin"],
        marker=dict(color=COLORS[4:4+len(dom_mar)], line=dict(width=0)),
        text=[f"₹{v/1e5:.1f}L" for v in dom_mar["Margin"]],
        textposition="outside",
        textfont=dict(size=10, color="#a0aec0")
    ))
    fig8.update_layout(**chart_layout("Margin by Domain", h=300))
    fig8.update_yaxes(showticklabels=False)
    st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 6 — EXIT TYPE WISE + MONTHLY TREND
# ─────────────────────────────────────────────
sec("EXIT TYPE & MONTHLY TREND")

ec1, ec2, ec3 = st.columns([1, 1, 1.2])

with ec1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    et = ef["exit_type"].value_counts().reset_index()
    et.columns = ["Type","Count"]
    fig9 = go.Figure(go.Pie(
        labels=et["Type"], values=et["Count"],
        hole=0.5,
        marker=dict(colors=COLORS[:len(et)],
                    line=dict(color="#070b14", width=3)),
        textfont=dict(color="#e2e8f0", size=10),
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
    ))
    fig9.update_layout(**chart_layout("Exit Type — Exits", h=300))
    fig9.update_layout(
        legend=dict(orientation="v", x=1.02, y=0.5,
                    font=dict(color="#718096", size=10),
                    bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with ec2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pt = pf["exit_type"].value_counts().reset_index()
    pt.columns = ["Type","Count"]
    fig10 = go.Figure(go.Pie(
        labels=pt["Type"], values=pt["Count"],
        hole=0.5,
        marker=dict(colors=COLORS[3:3+len(pt)],
                    line=dict(color="#070b14", width=3)),
        textfont=dict(color="#e2e8f0", size=10),
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
    ))
    fig10.update_layout(**chart_layout("Exit Type — Pipeline", h=300))
    fig10.update_layout(
        legend=dict(orientation="v", x=1.02, y=0.5,
                    font=dict(color="#718096", size=10),
                    bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig10, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with ec3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    trend_months = sorted(ef["Month"].dropna().unique(), key=msort)
    trend = (ef.groupby("Month")
               .agg(Exits=("employee_id","count"), PO=("p_o_value","sum"))
               .reindex(trend_months).reset_index())
    fig11 = make_subplots(specs=[[{"secondary_y": True}]])
    fig11.add_trace(go.Bar(
        x=trend["Month"], y=trend["Exits"],
        name="Exit Count",
        marker=dict(color="rgba(99,179,237,0.3)",
                    line=dict(color="#63b3ed", width=1)),
    ), secondary_y=False)
    fig11.add_trace(go.Scatter(
        x=trend["Month"], y=trend["PO"],
        name="P.O Value",
        line=dict(color="#68d391", width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color="#68d391",
                    line=dict(color="#070b14", width=2))
    ), secondary_y=True)
    lo = chart_layout("Monthly Exit Trend", h=300)
    lo["xaxis"]["tickfont"] = dict(color="#4a6080", size=10)
    fig11.update_layout(**lo)
    fig11.update_yaxes(secondary_y=False,
                       gridcolor="rgba(255,255,255,0.04)",
                       tickfont=dict(color="#4a6080", size=10),
                       title_font=dict(color="#4a6080"))
    fig11.update_yaxes(secondary_y=True,
                       gridcolor="rgba(0,0,0,0)",
                       tickfont=dict(color="#4a6080", size=10),
                       title_font=dict(color="#4a6080"))
    st.plotly_chart(fig11, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 7 — RAW DATA TABLES
# ─────────────────────────────────────────────
sec("RAW DATA")

tab1, tab2 = st.tabs(["  📋  Exit Records  ", "  🔄  Pipeline Records  "])

EXIT_COLS = ["full_name","employee_id","employee_type","company_name",
             "Domain","Business Head","exit_type","last_work_day",
             "p_o_value","margin","recruiter_name","manager_name","Month"]
PIPE_COLS = ["full_name","employee_id","employee_type","company_name",
             "Domain","Business Head","exit_type","tentative_exit_date",
             "p_o_value","margin","recruiter_name","manager_name","Month"]

with tab1:
    c = [x for x in EXIT_COLS if x in ef.columns]
    st.dataframe(ef[c].reset_index(drop=True), use_container_width=True, height=360)
    st.caption(f"📊 {len(ef):,} records  ·  P.O ₹{ef['p_o_value'].sum():,.0f}  ·  Margin ₹{ef['margin'].sum():,.0f}")

with tab2:
    c2 = [x for x in PIPE_COLS if x in pf.columns]
    st.dataframe(pf[c2].reset_index(drop=True), use_container_width=True, height=360)
    st.caption(f"📊 {len(pf):,} records  ·  P.O ₹{pf['p_o_value'].sum():,.0f}  ·  Margin ₹{pf['margin'].sum():,.0f}")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding:1.2rem 0;
     border-top:1px solid rgba(99,179,237,0.08);
     display:flex;justify-content:space-between;align-items:center;">
    <div style="font-size:11px;color:#1e3a5f;font-weight:600;letter-spacing:2px;">
        ⚡ JOULESTOWAATTS EXIT ANALYTICS
    </div>
    <div style="font-size:10px;color:#1e3a5f;">
        Auto-refreshes every 5 minutes · Data from Exit & Exit Pip.xlsx
    </div>
</div>
""", unsafe_allow_html=True)
