import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings, requests, io
from datetime import date, timedelta
warnings.filterwarnings("ignore")

EMP_TYPE_MAP = {1:"Contractor", 2:"Permanent", 4:"Intern", 6:"Contract Staff", 7:"Consultant"}

st.set_page_config(page_title="Onboarding & Exit Analytics · JoulestoWatts", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────
# THEMES
# ─────────────────────────────────────────────
THEMES = {
    "🌑 Deep Space": {
        "app_bg":       "#0e1525",
        "sidebar_bg":   "#152033",
        "card_bg":      "#162032",
        "border":       "#243450",
        "sidebar_border":"#2a3f5f",
        "input_bg":     "#1e3250",
        "text_main":    "#f1f5f9",
        "text_muted":   "#475569",
        "text_dim":     "#334155",
        "grid":         "#1e2d45",
        "plot_bg":      "rgba(0,0,0,0)",
    },
    "🌊 Ocean Pro": {
        "app_bg":        "#020c18",
        "sidebar_bg":    "#041020",
        "card_bg":       "#061628",
        "border":        "#0d3158",
        "sidebar_border":"#0d3158",
        "input_bg":      "#082040",
        "text_main":     "#e0f2fe",
        "text_muted":    "#38bdf8",
        "text_dim":      "#0c4a6e",
        "grid":          "#0a2540",
        "plot_bg":       "rgba(0,0,0,0)",
    },
    "🏙️ Carbon Steel": {
        "app_bg":        "#0a0a0a",
        "sidebar_bg":    "#111111",
        "card_bg":       "#161616",
        "border":        "#2a2a2a",
        "sidebar_border":"#2a2a2a",
        "input_bg":      "#1e1e1e",
        "text_main":     "#f5f5f5",
        "text_muted":    "#a3a3a3",
        "text_dim":      "#404040",
        "grid":          "#1f1f1f",
        "plot_bg":       "rgba(0,0,0,0)",
    },
}

if "theme" not in st.session_state:
    st.session_state["theme"] = "🌑 Deep Space"

def inject_css(t):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
*, html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; }}
.stApp {{ background: {t['app_bg']} !important; }}
.block-container {{ padding: 1.5rem 2rem 3rem 2rem !important; max-width: 100% !important; }}
[data-testid="stSidebar"] {{ background: {t['sidebar_bg']} !important; border-right: 1px solid {t['sidebar_border']} !important; }}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {{ color: #ffffff !important; }}
[data-testid="stSidebar"] .stMarkdown h3 {{ color: #60a5fa !important; font-size: 12px !important; letter-spacing: 2.5px !important; text-transform: uppercase !important; }}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{ background: {t['input_bg']} !important; border-color: {t['border']} !important; color: #ffffff !important; }}
[data-testid="stSidebar"] svg {{ fill: #60a5fa !important; }}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{ background: #1e4080 !important; border: 1px solid #3b82f6 !important; color: #ffffff !important; }}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{ color: #ffffff !important; }}
[data-testid="stSidebar"] .stButton button {{ background: {t['input_bg']} !important; border: 1px solid #3b82f6 !important; color: #60a5fa !important; font-weight: 600 !important; border-radius: 8px !important; }}
[data-baseweb="popover"] ul li {{ background: {t['input_bg']} !important; color: #ffffff !important; }}
[data-baseweb="popover"] ul li:hover {{ background: #1e4080 !important; }}
[data-baseweb="popover"] [role="option"] {{ color: #ffffff !important; }}
[data-baseweb="popover"] {{ background: {t['input_bg']} !important; }}
[data-baseweb="menu"] {{ background: {t['input_bg']} !important; border: 1px solid {t['border']} !important; }}
[data-baseweb="menu"] li {{ color: #ffffff !important; }}
[data-baseweb="menu"] li:hover {{ background: #1e4080 !important; }}
[data-testid="stDateInput"] input {{ background: {t['input_bg']} !important; color: #ffffff !important; border-color: {t['border']} !important; }}
button[data-baseweb="tab"] {{ color: #64748b !important; font-weight: 500 !important; font-size:13px !important;}}
button[data-baseweb="tab"][aria-selected="true"] {{ color: #60a5fa !important; border-bottom-color: #60a5fa !important; font-weight: 700 !important; }}
.kpi-main {{ border-radius: 16px; padding: 22px 22px 18px 22px; position: relative; overflow: hidden; height: 128px; }}
.kpi-main .top-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 4px; border-radius: 16px 16px 0 0; }}
.kpi-main .kpi-label {{ font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }}
.kpi-main .kpi-value {{ font-family: 'JetBrains Mono', monospace !important; font-size: 30px; font-weight: 700; line-height: 1; color: #ffffff; }}
.kpi-main .kpi-sub  {{ font-size: 11px; margin-top: 8px; }}
.kpi-main .kpi-icon {{ position: absolute; top: 20px; right: 20px; font-size: 22px; opacity: 0.18; }}
.kpi-cr {{ border-radius:14px; padding:18px 20px 14px 20px; position:relative; overflow:hidden; border:1px solid {t['border']}; background:{t['card_bg']}; }}
.kpi-cr .top-bar {{ position:absolute; top:0; left:0; right:0; height:3px; border-radius:14px 14px 0 0; }}
.kpi-cr .lbl {{ font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }}
.kpi-cr .hc  {{ font-family:'JetBrains Mono',monospace; font-size:30px; font-weight:700; color:#fff; line-height:1; }}
.kpi-cr .po  {{ font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600; margin-top:5px; }}
.sec-hdr {{ display:flex; align-items:center; gap:10px; margin:2.2rem 0 0.9rem 0; }}
.sec-hdr-dot {{ width:7px; height:7px; border-radius:50%; flex-shrink:0; }}
.sec-hdr-title {{ font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#cbd5e1; }}
.sec-hdr-line {{ flex:1; height:1px; background:{t['grid']}; }}
.chart-wrap {{ background:{t['card_bg']}; border:1px solid {t['border']}; border-radius:14px; overflow:hidden; padding:2px; }}
.totals-bar {{ background:linear-gradient(135deg,#1a3a6b,{t['card_bg']}); border:1px solid #2a4a7f; border-radius:12px; padding:14px 20px; display:flex; gap:0; margin-top:8px; }}
.tot-item {{ flex:1; text-align:center; border-right:1px solid {t['border']}; padding:0 12px; }}
.tot-item:last-child {{ border-right:none; }}
.tot-label {{ font-size:9px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#64748b; margin-bottom:5px; }}
.tot-value {{ font-family:'JetBrains Mono',monospace; font-size:15px; font-weight:700; color:{t['text_main']}; }}
.tot-value.blue {{ color:#60a5fa; }} .tot-value.green {{ color:#34d399; }} .tot-value.amber {{ color:#fb923c; }} .tot-value.purple {{ color:#a78bfa; }}
.pg-hdr {{ padding:0.3rem 0 1.4rem 0; border-bottom:1px solid {t['grid']}; margin-bottom:0.3rem; display:flex; justify-content:space-between; align-items:flex-end; }}
.pg-title {{ font-size:24px; font-weight:800; color:{t['text_main']}; }}
.pg-sub {{ font-size:11px; color:{t['text_muted']}; margin-top:4px; letter-spacing:1.5px; text-transform:uppercase; }}
.live-badge {{ background:#052e16; border:1px solid #16a34a; color:#4ade80; font-size:10px; font-weight:700; padding:5px 14px; border-radius:20px; letter-spacing:2px; }}
.op-sign {{ display:flex; align-items:center; justify-content:center; height:128px; font-size:36px; color:{t['text_dim']}; font-weight:300; }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility:hidden; }}
</style>
""", unsafe_allow_html=True)

T = THEMES[st.session_state["theme"]]
inject_css(T)

PALETTE = ["#60a5fa","#34d399","#fb923c","#f472b6","#a78bfa","#38bdf8","#facc15","#f87171","#86efac","#c4b5fd"]

def clayout(title="", h=330):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#94a3b8", size=11),
        title=dict(text=f"<b>{title}</b>", font=dict(size=13, color="#e2e8f0"), x=0.02, y=0.97),
        margin=dict(l=10, r=16, t=42, b=10), height=h,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)),
        xaxis=dict(gridcolor=T["grid"], zerolinecolor=T["border"], tickfont=dict(color="#64748b", size=10), showline=False),
        yaxis=dict(gridcolor=T["grid"], zerolinecolor=T["border"], tickfont=dict(color="#64748b", size=10), showline=False),
    )

def sec(title, color="#60a5fa"):
    st.markdown(f"""<div class="sec-hdr">
        <div class="sec-hdr-dot" style="background:{color};box-shadow:0 0 8px {color}99;"></div>
        <div class="sec-hdr-title">{title}</div>
        <div class="sec-hdr-line"></div>
    </div>""", unsafe_allow_html=True)

MO = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
def msort(m):
    try:
        p = str(m).replace("\u2019","'").split("'")
        return int(p[1])*100 + MO.get(p[0][:3], 0)
    except: return 0

FILE_PATH = "https://j2w-my.sharepoint.com/:x:/g/personal/sheshank_suresh_joulestowatts_com/IQAbN1Juu0wxQaQeQrs_ALpaAf5cbpmso_hp1POy6u9adds?download=1"

@st.cache_data(ttl=300)
def load_data(path):
    response = requests.get(path)
    response.raise_for_status()
    xl = pd.ExcelFile(io.BytesIO(response.content))

    exit_df = xl.parse("Exit")
    pipe_df = xl.parse("Exit Pipeline")
    ob_df   = xl.parse("Onboarding")
    op_df   = xl.parse("Onboarding Pipeline")
    org_df  = xl.parse("Org Mapping")

    for df in [exit_df, pipe_df, ob_df, op_df, org_df]:
        df.columns = df.columns.str.strip()

    org_df["Domain"] = org_df["Domain"].str.strip().str.title()
    org_slim = org_df[["Client","Domain","Business Head","HRBP"]].drop_duplicates("Client")

    # Normalize company_name for onboarding pipeline
    if "Company_name" in op_df.columns:
        op_df.rename(columns={"Company_name":"company_name"}, inplace=True)

    # Merge org mapping onto all sheets
    exit_df = exit_df.merge(org_slim, left_on="company_name", right_on="Client", how="left", suffixes=("","_org"))
    pipe_df = pipe_df.merge(org_slim, left_on="company_name", right_on="Client", how="left", suffixes=("","_org"))
    ob_df   = ob_df.merge(org_slim,   left_on="company_name", right_on="Client", how="left", suffixes=("","_org"))
    op_df   = op_df.merge(org_slim,   left_on="company_name", right_on="Client", how="left", suffixes=("","_org"))

    # Exit & Pipeline processing
    for df in [exit_df, pipe_df]:
        if "Business Head" in df.columns:
            df["Business Head"] = df["Business Head"].fillna(df.get("BH",""))
        else:
            df["Business Head"] = df.get("BH", pd.NA)
        if "Domain" not in df.columns: df["Domain"] = pd.NA
        if "HRBP"   not in df.columns: df["HRBP"]   = pd.NA
        df["employee_type"] = df["employee_type"].map(EMP_TYPE_MAP).fillna(df["employee_type"].astype(str))
        df["p_o_value"] = pd.to_numeric(df["p_o_value"], errors="coerce").fillna(0)
        df["margin"]    = pd.to_numeric(df["margin"],    errors="coerce").fillna(0)
        df["Month"]     = df["Month"].astype(str).str.strip()
        df["exit_type"] = df["exit_type"].astype(str).str.strip()
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["created_date"] = df["created_at"].dt.date

    exit_df["last_work_day"]       = pd.to_datetime(exit_df["last_work_day"], errors="coerce").dt.date
    exit_df["joining_date"]        = pd.to_datetime(exit_df["joining_date"],  errors="coerce").dt.date
    pipe_df["tentative_exit_date"] = pd.to_datetime(pipe_df["tentative_exit_date"], errors="coerce").dt.date

    # Onboarding processing
    for df in [ob_df, op_df]:
        if "Business Head" in df.columns:
            df["Business Head"] = df["Business Head"].fillna(df.get("BH",""))
        else:
            df["Business Head"] = df.get("BH", pd.NA)
        if "Domain" not in df.columns: df["Domain"] = pd.NA
        if "HRBP"   not in df.columns: df["HRBP"]   = pd.NA
        if "employee_type" in df.columns:
            df["employee_type"] = df["employee_type"].map(EMP_TYPE_MAP).fillna(df["employee_type"].astype(str))
        df["p_o_value"]    = pd.to_numeric(df["p_o_value"], errors="coerce").fillna(0)
        df["margin"]       = pd.to_numeric(df["margin"],    errors="coerce").fillna(0)
        df["Month"]        = df["Month"].astype(str).str.strip()
        df["display_date"] = pd.to_datetime(df["display_date"], errors="coerce").dt.date
        if "offer_created_date" in df.columns:
            df["offer_created_date"] = pd.to_datetime(df["offer_created_date"], errors="coerce").dt.date

    return exit_df, pipe_df, ob_df, op_df, org_df

try:
    exit_df, pipe_df, ob_df, op_df, org_df = load_data(FILE_PATH)
except Exception as e:
    st.error(f"❌ Error loading file: {e}"); st.stop()

# Exit created date range
all_min = min(exit_df["created_at"].dropna().dt.date.min(), pipe_df["created_at"].dropna().dt.date.min())
all_max = max(exit_df["created_at"].dropna().dt.date.max(), pipe_df["created_at"].dropna().dt.date.max())
today   = date.today()

if "cr_from" not in st.session_state: st.session_state["cr_from"] = all_min
if "cr_to"   not in st.session_state: st.session_state["cr_to"]   = all_max

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ ONBOARDING & EXIT")

    # Theme switcher
    st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:2px;color:#60a5fa;margin:8px 0 6px 0;'>🎨 THEME</div>", unsafe_allow_html=True)
    for theme_name in THEMES.keys():
        is_active = st.session_state["theme"] == theme_name
        if st.button(f"{'✅ ' if is_active else ''}{theme_name}", use_container_width=True, key=f"theme_{theme_name}"):
            st.session_state["theme"] = theme_name; st.rerun()

    st.markdown("---")
    st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:2px;color:#60a5fa;margin-bottom:6px;'>🔍 COMMON FILTERS</div>", unsafe_allow_html=True)

    # BH — from all 4 sheets
    all_bh = sorted(
        (set(exit_df["Business Head"].dropna()) | set(pipe_df["Business Head"].dropna()) |
         set(ob_df["Business Head"].dropna())   | set(op_df["Business Head"].dropna())) - {"","nan"}
    )
    bh_sel = st.multiselect("👤  Business Head", all_bh, placeholder="All")

    def bh_f(df): return df[df["Business Head"].isin(bh_sel)] if bh_sel else df
    ef_bh = bh_f(exit_df); pf_bh = bh_f(pipe_df)
    ob_bh = bh_f(ob_df);   op_bh = bh_f(op_df)

    # Domain — cascades from BH
    all_dom = sorted(
        (set(ef_bh["Domain"].dropna()) | set(pf_bh["Domain"].dropna()) |
         set(ob_bh["Domain"].dropna()) | set(op_bh["Domain"].dropna())) - {"","nan"}
    )
    domain_sel = st.multiselect("🏢  Domain", all_dom, placeholder="All")

    def dom_f(df): return df[df["Domain"].isin(domain_sel)] if domain_sel else df
    ef_dom = dom_f(ef_bh); pf_dom = dom_f(pf_bh)
    ob_dom = dom_f(ob_bh); op_dom = dom_f(op_bh)

    # Client — cascades from Domain
    all_cli = sorted(
        (set(ef_dom["company_name"].dropna()) | set(pf_dom["company_name"].dropna()) |
         set(ob_dom["company_name"].dropna()) | set(op_dom["company_name"].dropna())) - {"","nan"}
    )
    client_sel = st.multiselect("🏭  Client", all_cli, placeholder="All")

    def cli_f(df): return df[df["company_name"].isin(client_sel)] if client_sel else df
    ef_cli = cli_f(ef_dom); pf_cli = cli_f(pf_dom)

    # HRBP — exit only
    hrbp_options = sorted((set(ef_cli["HRBP"].dropna()) | set(pf_cli["HRBP"].dropna())) - {"","nan"})
    hrbp_sel = st.multiselect("👔  HRBP", hrbp_options, placeholder="All")

    # Exit Type
    def hrbp_f(df): return df[df["HRBP"].isin(hrbp_sel)] if hrbp_sel else df
    ef_hrbp = hrbp_f(ef_cli); pf_hrbp = hrbp_f(pf_cli)
    exit_type_options = sorted((set(ef_hrbp["exit_type"].dropna()) | set(pf_hrbp["exit_type"].dropna())) - {"","nan"})
    exit_type_sel = st.multiselect("🚪  Exit Type", exit_type_options, placeholder="All")

    # Month — always full data so selection never clears
    month_options = sorted(
        (set(exit_df["Month"].dropna()) | set(pipe_df["Month"].dropna()) |
         set(ob_df["Month"].dropna())   | set(op_df["Month"].dropna())) - {"","nan"},
        key=msort
    )
    month_sel = st.multiselect("📅  Month", month_options, placeholder="All")

    st.markdown("---")

    # Created date — EXIT ONLY
    st.markdown("<div style='font-size:10px;font-weight:700;letter-spacing:2px;color:#4ade80;margin-bottom:8px;'>📆 EXIT CREATED DATE</div>", unsafe_allow_html=True)
    st.caption("Applies to Exit & Exit Pipeline only")

    qc1, qc2 = st.columns(2)
    with qc1:
        if st.button("Today", use_container_width=True):
            st.session_state["cr_from"] = today; st.session_state["cr_to"] = today; st.rerun()
    with qc2:
        if st.button("This Week", use_container_width=True):
            st.session_state["cr_from"] = today - timedelta(days=today.weekday()); st.session_state["cr_to"] = today; st.rerun()
    qc3, qc4 = st.columns(2)
    with qc3:
        if st.button("This Month", use_container_width=True):
            st.session_state["cr_from"] = today.replace(day=1); st.session_state["cr_to"] = today; st.rerun()
    with qc4:
        if st.button("All Time", use_container_width=True):
            st.session_state["cr_from"] = all_min; st.session_state["cr_to"] = all_max; st.rerun()

    cr_from = st.date_input("From", value=st.session_state["cr_from"], min_value=all_min, max_value=all_max)
    cr_to   = st.date_input("To",   value=st.session_state["cr_to"],   min_value=all_min, max_value=all_max)
    st.session_state["cr_from"] = cr_from
    st.session_state["cr_to"]   = cr_to

    st.markdown("---")
    if st.button("🔄  Refresh Data", use_container_width=True):
        st.cache_data.clear(); st.rerun()

    st.markdown(f"""<div style="margin-top:1rem;padding:12px 14px;background:{T['app_bg']};border-radius:10px;border:1px solid {T['grid']};">
        <div style="font-size:10px;color:{T['text_dim']};letter-spacing:2px;text-transform:uppercase;font-weight:600;margin-bottom:5px;">Data Source</div>
        <div style="font-size:11px;color:#60a5fa;font-weight:500;">Exit & Exit Pip.xlsx</div>
        <div style="font-size:10px;color:{T['text_dim']};margin-top:3px;">Refreshes every 5 min</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
def apply_exit(df):
    f = df.copy()
    if bh_sel:        f = f[f["Business Head"].isin(bh_sel)]
    if domain_sel:    f = f[f["Domain"].isin(domain_sel)]
    if client_sel:    f = f[f["company_name"].isin(client_sel)]
    if hrbp_sel:      f = f[f["HRBP"].isin(hrbp_sel)]
    if exit_type_sel: f = f[f["exit_type"].isin(exit_type_sel)]
    if month_sel:     f = f[f["Month"].isin(month_sel)]
    return f

def apply_ob(df):
    f = df.copy()
    if bh_sel:     f = f[f["Business Head"].isin(bh_sel)]
    if domain_sel: f = f[f["Domain"].isin(domain_sel)]
    if client_sel: f = f[f["company_name"].isin(client_sel)]
    if month_sel:  f = f[f["Month"].isin(month_sel)]
    return f

ef  = apply_exit(exit_df)
pf  = apply_exit(pipe_df)
obf = apply_ob(ob_df)
opf = apply_ob(op_df)

# Exit created filter
ef_cr = ef[(ef["created_at"].dt.date >= cr_from) & (ef["created_at"].dt.date <= cr_to)]
pf_cr = pf[(pf["created_at"].dt.date >= cr_from) & (pf["created_at"].dt.date <= cr_to)]

# Metrics
exit_hc  = len(ef);  pipe_hc  = len(pf)
exit_po  = ef["p_o_value"].sum(); pipe_po  = pf["p_o_value"].sum()
exit_mar = ef["margin"].sum();    pipe_mar = pf["margin"].sum()
ob_hc    = len(obf); op_hc    = len(opf)
ob_po    = obf["p_o_value"].sum(); op_po  = opf["p_o_value"].sum()
ob_mar   = obf["margin"].sum();    op_mar = opf["margin"].sum()
cr_exit_hc = len(ef_cr); cr_pipe_hc = len(pf_cr)
cr_exit_po = ef_cr["p_o_value"].sum(); cr_pipe_po = pf_cr["p_o_value"].sum()
cr_exit_mar = ef_cr["margin"].sum();   cr_pipe_mar = pf_cr["margin"].sum()

# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────
st.markdown(f"""<div class="pg-hdr">
    <div>
        <div class="pg-title">⚡ Onboarding & Exit Analytics Dashboard</div>
        <div class="pg-sub">JoulestoWatts Business Solutions · Workforce Intelligence</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:11px;color:{T['text_muted']};">Theme: <b style="color:#60a5fa;">{st.session_state['theme']}</b></span>
        <span class="live-badge">● LIVE</span>
    </div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN TABS — Onboarding first, Exit second
# ─────────────────────────────────────────────
main_tab1, main_tab2 = st.tabs([
    "  🎯  ONBOARDING DASHBOARD  ",
    "  🚪  EXIT DASHBOARD  "
])

# ═══════════════════════════════════════════════
# TAB 1 — ONBOARDING
# ═══════════════════════════════════════════════
with main_tab1:

    # Row 1 — HC
    sec("ONBOARDING HEADCOUNT OVERVIEW", "#34d399")
    oh1,oh2,oh3,oh4,oh5 = st.columns([1,0.12,1,0.12,1])
    with oh1:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#064e3b,#065f46);border:1px solid #059669;">
            <div class="top-bar" style="background:linear-gradient(90deg,#34d399,#10b981);"></div>
            <div class="kpi-icon">🎯</div>
            <div class="kpi-label" style="color:#6ee7b7;">Onboarding HC</div>
            <div class="kpi-value">{ob_hc:,}</div>
            <div class="kpi-sub" style="color:#6ee7b7;">Confirmed onboardings</div>
        </div>""", unsafe_allow_html=True)
    with oh2: st.markdown('<div class="op-sign">+</div>', unsafe_allow_html=True)
    with oh3:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#1e3a5f,#1a4080);border:1px solid #2563eb;">
            <div class="top-bar" style="background:linear-gradient(90deg,#38bdf8,#0ea5e9);"></div>
            <div class="kpi-icon">📋</div>
            <div class="kpi-label" style="color:#bae6fd;">Onboarding Pipeline</div>
            <div class="kpi-value">{op_hc:,}</div>
            <div class="kpi-sub" style="color:#bae6fd;">Upcoming onboardings</div>
        </div>""", unsafe_allow_html=True)
    with oh4: st.markdown('<div class="op-sign">=</div>', unsafe_allow_html=True)
    with oh5:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#2e1065,#3b0764);border:1px solid #7c3aed;">
            <div class="top-bar" style="background:linear-gradient(90deg,#a78bfa,#8b5cf6);"></div>
            <div class="kpi-icon">👥</div>
            <div class="kpi-label" style="color:#c4b5fd;">Total Onboarding HC</div>
            <div class="kpi-value">{ob_hc+op_hc:,}</div>
            <div class="kpi-sub" style="color:#c4b5fd;">{ob_hc:,} Confirmed + {op_hc:,} Pipeline</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Row 2 — PO
    sec("ONBOARDING P.O VALUE & MARGIN", "#a78bfa")
    op1,op2,op3,op4,op5 = st.columns([1,0.12,1,0.12,1])
    with op1:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#064e3b,#065f46);border:1px solid #059669;">
            <div class="top-bar" style="background:linear-gradient(90deg,#34d399,#10b981);"></div>
            <div class="kpi-icon">💼</div>
            <div class="kpi-label" style="color:#6ee7b7;">Onboarding P.O Value</div>
            <div class="kpi-value" style="font-size:22px;">₹{ob_po:,.0f}</div>
            <div class="kpi-sub" style="color:#6ee7b7;">Margin ₹{ob_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with op2: st.markdown('<div class="op-sign">+</div>', unsafe_allow_html=True)
    with op3:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#1e3a5f,#1a4080);border:1px solid #2563eb;">
            <div class="top-bar" style="background:linear-gradient(90deg,#38bdf8,#0ea5e9);"></div>
            <div class="kpi-icon">📊</div>
            <div class="kpi-label" style="color:#bae6fd;">Pipeline P.O Value</div>
            <div class="kpi-value" style="font-size:22px;">₹{op_po:,.0f}</div>
            <div class="kpi-sub" style="color:#bae6fd;">Margin ₹{op_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with op4: st.markdown('<div class="op-sign">=</div>', unsafe_allow_html=True)
    with op5:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#2e1065,#3b0764);border:1px solid #7c3aed;">
            <div class="top-bar" style="background:linear-gradient(90deg,#a78bfa,#8b5cf6);"></div>
            <div class="kpi-icon">💰</div>
            <div class="kpi-label" style="color:#c4b5fd;">Total Onboarding P.O</div>
            <div class="kpi-value" style="font-size:22px;">₹{ob_po+op_po:,.0f}</div>
            <div class="kpi-sub" style="color:#c4b5fd;">Total Margin ₹{ob_mar+op_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Client wise
    sec("CLIENT WISE ANALYSIS", "#38bdf8")
    oct1, oct2 = st.tabs(["  🎯 Onboarding  ","  📋 Onboarding Pipeline  "])
    def ob_client_charts(df, label, bar_color, text_color):
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            top_c = df.groupby("company_name").size().reset_index(name=label).sort_values(label).tail(12)
            fig = go.Figure(go.Bar(x=top_c[label], y=top_c["company_name"], orientation="h",
                marker=dict(color=bar_color, opacity=0.9, line=dict(width=0)),
                text=top_c[label], textposition="outside",
                textfont=dict(color=text_color, size=11, family="JetBrains Mono")))
            fig.update_layout(**clayout(f"Top Clients · {label} Count", 390)); fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key="chart_1")
            st.markdown('</div>', unsafe_allow_html=True)
        with cc2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            top_po = df.groupby("company_name")["p_o_value"].sum().reset_index(name="PO").sort_values("PO").tail(12)
            fig2 = go.Figure(go.Bar(x=top_po["PO"], y=top_po["company_name"], orientation="h",
                marker=dict(color="#0ea5e9", opacity=0.9, line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in top_po["PO"]], textposition="outside",
                textfont=dict(color="#bae6fd", size=11, family="JetBrains Mono")))
            fig2.update_layout(**clayout(f"Top Clients · {label} P.O Value", 390)); fig2.update_xaxes(showticklabels=False)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False}, key="chart_2")
            st.markdown('</div>', unsafe_allow_html=True)
    with oct1: ob_client_charts(obf, "Onboarding", "#10b981", "#6ee7b7")
    with oct2: ob_client_charts(opf, "Pipeline", "#0ea5e9", "#bae6fd")

    # BH wise
    sec("BUSINESS HEAD WISE ANALYSIS", "#34d399")
    obt1, obt2 = st.tabs(["  🎯 Onboarding  ","  📋 Onboarding Pipeline  "])
    def ob_bh_charts(df, label):
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            bh_count = df.groupby("Business Head").size().reset_index(name=label).sort_values(label)
            fig3 = go.Figure(go.Bar(x=bh_count[label], y=bh_count["Business Head"], orientation="h",
                marker=dict(color=PALETTE[:len(bh_count)], line=dict(width=0)),
                text=bh_count[label], textposition="outside",
                textfont=dict(color="#e2e8f0", size=11, family="JetBrains Mono")))
            fig3.update_layout(**clayout(f"{label} by Business Head", 330)); fig3.update_xaxes(showticklabels=False)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False}, key="chart_3")
            st.markdown('</div>', unsafe_allow_html=True)
        with bc2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            bh_po = df.groupby("Business Head")["p_o_value"].sum().reset_index(name="PO").sort_values("PO")
            fig4 = go.Figure(go.Bar(x=bh_po["PO"], y=bh_po["Business Head"], orientation="h",
                marker=dict(color=PALETTE[:len(bh_po)], line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in bh_po["PO"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=11, family="JetBrains Mono")))
            fig4.update_layout(**clayout(f"{label} P.O Value by Business Head", 330)); fig4.update_xaxes(showticklabels=False)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False}, key="chart_4")
            st.markdown('</div>', unsafe_allow_html=True)
    with obt1: ob_bh_charts(obf, "Onboarding")
    with obt2: ob_bh_charts(opf, "Pipeline")

    # Domain wise
    sec("DOMAIN WISE ANALYSIS", "#fb923c")
    odt1, odt2 = st.tabs(["  🎯 Onboarding  ","  📋 Onboarding Pipeline  "])
    def ob_domain_charts(df, label):
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            dom_e = df["Domain"].value_counts().reset_index(); dom_e.columns = ["Domain","Count"]
            fig6 = go.Figure(go.Pie(labels=dom_e["Domain"], values=dom_e["Count"], hole=0.52,
                marker=dict(colors=PALETTE[:len(dom_e)], line=dict(color=T['app_bg'], width=3)),
                textfont=dict(color="#ffffff", size=12), textinfo="label+percent"))
            fig6.update_layout(**clayout(f"{label} by Domain", 310)); fig6.update_layout(showlegend=False)
            st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar":False}, key="chart_5")
            st.markdown('</div>', unsafe_allow_html=True)
        with dc2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            dom_po = df.groupby("Domain")["p_o_value"].sum().reset_index(name="PO").sort_values("PO", ascending=False)
            fig7 = go.Figure(go.Bar(x=dom_po["Domain"], y=dom_po["PO"],
                marker=dict(color=PALETTE[:len(dom_po)], line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in dom_po["PO"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=12, family="JetBrains Mono")))
            fig7.update_layout(**clayout(f"{label} P.O Value by Domain", 310)); fig7.update_yaxes(showticklabels=False)
            st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar":False}, key="chart_6")
            st.markdown('</div>', unsafe_allow_html=True)
        with dc3:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            dom_m = df.groupby("Domain")["margin"].sum().reset_index(name="Margin").sort_values("Margin", ascending=False)
            fig8 = go.Figure(go.Bar(x=dom_m["Domain"], y=dom_m["Margin"],
                marker=dict(color=PALETTE[3:3+len(dom_m)], line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in dom_m["Margin"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=12, family="JetBrains Mono")))
            fig8.update_layout(**clayout(f"{label} Margin by Domain", 310)); fig8.update_yaxes(showticklabels=False)
            st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar":False}, key="chart_7")
            st.markdown('</div>', unsafe_allow_html=True)
    with odt1: ob_domain_charts(obf, "Onboarding")
    with odt2: ob_domain_charts(opf, "Pipeline")

    # Monthly trend
    sec("MONTHLY ONBOARDING TREND", "#f472b6")
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    om = sorted(obf["Month"].dropna().unique(), key=msort)
    otr = obf.groupby("Month").agg(Count=("employee_id","count"), PO=("p_o_value","sum")).reindex(om).reset_index()
    otr["Count"] = pd.to_numeric(otr["Count"], errors="coerce").fillna(0)
    otr["PO"]    = pd.to_numeric(otr["PO"],    errors="coerce").fillna(0)
    fig_ot = make_subplots(specs=[[{"secondary_y": True}]])
    fig_ot.add_trace(go.Bar(x=otr["Month"], y=otr["Count"], name="Onboarding Count",
        marker=dict(color="rgba(52,211,153,0.35)", line=dict(color="#34d399", width=1.5))), secondary_y=False)
    fig_ot.add_trace(go.Scatter(x=otr["Month"], y=otr["PO"], name="P.O Value",
        line=dict(color="#a78bfa", width=2.5), mode="lines+markers",
        marker=dict(size=8, color="#a78bfa", line=dict(color=T['app_bg'], width=2))), secondary_y=True)
    lo_ot = clayout("Monthly Onboarding Trend", 330)
    lo_ot["legend"] = dict(orientation="h", y=1.06, x=1, xanchor="right", bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1", size=10))
    fig_ot.update_layout(**lo_ot)
    fig_ot.update_yaxes(gridcolor=T['grid'], tickfont=dict(color="#64748b", size=10), secondary_y=False)
    fig_ot.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#64748b", size=10), secondary_y=True)
    st.plotly_chart(fig_ot, use_container_width=True, config={"displayModeBar":False}, key="chart_8")
    st.markdown('</div>', unsafe_allow_html=True)

    # Onboarding Raw Data
    sec("RAW DATA", "#64748b")
    ort1, ort2 = st.tabs(["  🎯  Onboarding Records  ","  📋  Pipeline Records  "])
    OB_COLS = {"full_name":"Full Name","employee_id":"Employee ID","employee_type":"Emp Type",
               "company_name":"Client","Domain":"Domain","Business Head":"Business Head","HRBP":"HRBP",
               "display_date":"Display Date","p_o_value":"P.O Value (₹)","margin":"Margin (₹)",
               "recruiter_name":"Recruiter","manager_name":"Manager","Month":"Month","Status":"Status"}
    OP_COLS = {"full_name":"Full Name","company_name":"Client","Domain":"Domain",
               "Business Head":"Business Head","display_date":"Display Date",
               "p_o_value":"P.O Value (₹)","margin":"Margin (₹)",
               "recruiter_name":"Recruiter","manager_name":"Manager","Month":"Month","Status":"Status"}

    def show_ob_table(df, col_map, label):
        avail = {k:v for k,v in col_map.items() if k in df.columns}
        ddf = df[list(avail.keys())].copy().rename(columns=avail)
        if "P.O Value (₹)" in ddf.columns: ddf["P.O Value (₹)"] = ddf["P.O Value (₹)"].apply(lambda x: f"₹{x:,.0f}")
        if "Margin (₹)"    in ddf.columns: ddf["Margin (₹)"]    = ddf["Margin (₹)"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(ddf.reset_index(drop=True), use_container_width=True, height=360)
        po = df["p_o_value"].sum(); mar = df["margin"].sum()
        uniq_c = df["company_name"].nunique()
        st.markdown(f"""<div class="totals-bar">
            <div class="tot-item"><div class="tot-label">Total {label}</div><div class="tot-value blue">{len(df):,} HC</div></div>
            <div class="tot-item"><div class="tot-label">Total P.O Value</div><div class="tot-value green">₹{po:,.0f}</div></div>
            <div class="tot-item"><div class="tot-label">Total Margin</div><div class="tot-value amber">₹{mar:,.0f}</div></div>
            <div class="tot-item"><div class="tot-label">Unique Clients</div><div class="tot-value purple">{uniq_c:,}</div></div>
        </div>""", unsafe_allow_html=True)
    with ort1: show_ob_table(obf, OB_COLS, "Onboarding")
    with ort2: show_ob_table(opf, OP_COLS, "Pipeline")

# ═══════════════════════════════════════════════
# TAB 2 — EXIT DASHBOARD (your exact original code)
# ═══════════════════════════════════════════════
with main_tab2:

    # Row 1 — HC
    sec("HEADCOUNT OVERVIEW", "#60a5fa")
    h1,h2,h3,h4,h5 = st.columns([1,0.12,1,0.12,1])
    with h1:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#1a3a6b,#1e4080);border:1px solid #2d5aa0;">
            <div class="top-bar" style="background:linear-gradient(90deg,#60a5fa,#3b82f6);"></div>
            <div class="kpi-icon">🚪</div>
            <div class="kpi-label" style="color:#93c5fd;">Exit Headcount</div>
            <div class="kpi-value">{exit_hc:,}</div>
            <div class="kpi-sub" style="color:#93c5fd;">Confirmed exits</div>
        </div>""", unsafe_allow_html=True)
    with h2: st.markdown('<div class="op-sign">+</div>', unsafe_allow_html=True)
    with h3:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#7c2d12,#9a3412);border:1px solid #c2410c;">
            <div class="top-bar" style="background:linear-gradient(90deg,#fb923c,#f97316);"></div>
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label" style="color:#fdba74;">Pipeline Headcount</div>
            <div class="kpi-value">{pipe_hc:,}</div>
            <div class="kpi-sub" style="color:#fdba74;">At-risk headcount</div>
        </div>""", unsafe_allow_html=True)
    with h4: st.markdown('<div class="op-sign">=</div>', unsafe_allow_html=True)
    with h5:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#064e3b,#065f46);border:1px solid #059669;">
            <div class="top-bar" style="background:linear-gradient(90deg,#34d399,#10b981);"></div>
            <div class="kpi-icon">📊</div>
            <div class="kpi-label" style="color:#6ee7b7;">Projection (Total HC)</div>
            <div class="kpi-value">{exit_hc+pipe_hc:,}</div>
            <div class="kpi-sub" style="color:#6ee7b7;">{exit_hc:,} Exit + {pipe_hc:,} Pipeline</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # Row 2 — PO
    sec("P.O VALUE & MARGIN OVERVIEW", "#a78bfa")
    p1,p2,p3,p4,p5 = st.columns([1,0.12,1,0.12,1])
    with p1:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#1a3a6b,#1e4080);border:1px solid #2d5aa0;">
            <div class="top-bar" style="background:linear-gradient(90deg,#60a5fa,#3b82f6);"></div>
            <div class="kpi-icon">💼</div>
            <div class="kpi-label" style="color:#93c5fd;">Exit P.O Value</div>
            <div class="kpi-value" style="font-size:22px;">₹{exit_po:,.0f}</div>
            <div class="kpi-sub" style="color:#93c5fd;">Margin ₹{exit_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with p2: st.markdown('<div class="op-sign">+</div>', unsafe_allow_html=True)
    with p3:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#7c2d12,#9a3412);border:1px solid #c2410c;">
            <div class="top-bar" style="background:linear-gradient(90deg,#fb923c,#f97316);"></div>
            <div class="kpi-icon">📋</div>
            <div class="kpi-label" style="color:#fdba74;">Pipeline P.O Value</div>
            <div class="kpi-value" style="font-size:22px;">₹{pipe_po:,.0f}</div>
            <div class="kpi-sub" style="color:#fdba74;">Margin ₹{pipe_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with p4: st.markdown('<div class="op-sign">=</div>', unsafe_allow_html=True)
    with p5:
        st.markdown(f"""<div class="kpi-main" style="background:linear-gradient(135deg,#2e1065,#3b0764);border:1px solid #7c3aed;">
            <div class="top-bar" style="background:linear-gradient(90deg,#a78bfa,#8b5cf6);"></div>
            <div class="kpi-icon">💰</div>
            <div class="kpi-label" style="color:#c4b5fd;">Projection (Total P.O)</div>
            <div class="kpi-value" style="font-size:22px;">₹{exit_po+pipe_po:,.0f}</div>
            <div class="kpi-sub" style="color:#c4b5fd;">Total Margin ₹{exit_mar+pipe_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Client wise
    sec("CLIENT WISE ANALYSIS", "#38bdf8")
    client_tab1, client_tab2 = st.tabs(["  🚪 Exit  ", "  🔄 Exit Pipeline  "])
    def client_charts(df, label):
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            top_c = df.groupby("company_name").size().reset_index(name=label).sort_values(label).tail(12)
            fig = go.Figure(go.Bar(x=top_c[label], y=top_c["company_name"], orientation="h",
                marker=dict(color="#3b82f6", opacity=0.9, line=dict(width=0)),
                text=top_c[label], textposition="outside",
                textfont=dict(color="#93c5fd", size=11, family="JetBrains Mono")))
            fig.update_layout(**clayout(f"Top Clients · {label} Count", 390)); fig.update_xaxes(showticklabels=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key="chart_9")
            st.markdown('</div>', unsafe_allow_html=True)
        with cc2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            top_po_c = df.groupby("company_name")["p_o_value"].sum().reset_index(name="PO").sort_values("PO").tail(12)
            fig2 = go.Figure(go.Bar(x=top_po_c["PO"], y=top_po_c["company_name"], orientation="h",
                marker=dict(color="#8b5cf6", opacity=0.9, line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in top_po_c["PO"]], textposition="outside",
                textfont=dict(color="#c4b5fd", size=11, family="JetBrains Mono")))
            fig2.update_layout(**clayout(f"Top Clients · {label} P.O Value", 390)); fig2.update_xaxes(showticklabels=False)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False}, key="chart_10")
            st.markdown('</div>', unsafe_allow_html=True)
    with client_tab1: client_charts(ef, "Exit")
    with client_tab2: client_charts(pf, "Pipeline")

    # BH wise
    sec("BUSINESS HEAD WISE ANALYSIS", "#34d399")
    bh_tab1, bh_tab2 = st.tabs(["  🚪 Exit  ", "  🔄 Exit Pipeline  "])
    def bh_charts(df, label):
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            bh_count = df.groupby("Business Head").size().reset_index(name=label).sort_values(label)
            fig3 = go.Figure(go.Bar(x=bh_count[label], y=bh_count["Business Head"], orientation="h",
                marker=dict(color=PALETTE[:len(bh_count)], line=dict(width=0)),
                text=bh_count[label], textposition="outside",
                textfont=dict(color="#e2e8f0", size=11, family="JetBrains Mono")))
            fig3.update_layout(**clayout(f"{label} by Business Head", 330)); fig3.update_xaxes(showticklabels=False)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False}, key="chart_11")
            st.markdown('</div>', unsafe_allow_html=True)
        with bc2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            bh_po = df.groupby("Business Head")["p_o_value"].sum().reset_index(name="PO").sort_values("PO")
            fig4 = go.Figure(go.Bar(x=bh_po["PO"], y=bh_po["Business Head"], orientation="h",
                marker=dict(color=PALETTE[:len(bh_po)], line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in bh_po["PO"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=11, family="JetBrains Mono")))
            fig4.update_layout(**clayout(f"{label} P.O Value by Business Head", 330)); fig4.update_xaxes(showticklabels=False)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False}, key="chart_12")
            st.markdown('</div>', unsafe_allow_html=True)
    with bh_tab1: bh_charts(ef, "Exit")
    with bh_tab2: bh_charts(pf, "Pipeline")

    # Domain wise
    sec("DOMAIN WISE ANALYSIS", "#fb923c")
    domain_tab1, domain_tab2 = st.tabs(["  🚪 Exit  ", "  🔄 Exit Pipeline  "])
    def domain_charts(df, label):
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            dom_e = df["Domain"].value_counts().reset_index(); dom_e.columns = ["Domain","Count"]
            fig6 = go.Figure(go.Pie(labels=dom_e["Domain"], values=dom_e["Count"], hole=0.52,
                marker=dict(colors=PALETTE[:len(dom_e)], line=dict(color=T['app_bg'], width=3)),
                textfont=dict(color="#ffffff", size=12), textinfo="label+percent"))
            fig6.update_layout(**clayout(f"{label} by Domain", 310)); fig6.update_layout(showlegend=False)
            st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar":False}, key="chart_13")
            st.markdown('</div>', unsafe_allow_html=True)
        with dc2:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            dom_po = df.groupby("Domain")["p_o_value"].sum().reset_index(name="PO").sort_values("PO", ascending=False)
            fig7 = go.Figure(go.Bar(x=dom_po["Domain"], y=dom_po["PO"],
                marker=dict(color=PALETTE[:len(dom_po)], line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in dom_po["PO"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=12, family="JetBrains Mono")))
            fig7.update_layout(**clayout(f"{label} P.O Value by Domain", 310)); fig7.update_yaxes(showticklabels=False)
            st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar":False}, key="chart_14")
            st.markdown('</div>', unsafe_allow_html=True)
        with dc3:
            st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
            dom_m = df.groupby("Domain")["margin"].sum().reset_index(name="Margin").sort_values("Margin", ascending=False)
            fig8 = go.Figure(go.Bar(x=dom_m["Domain"], y=dom_m["Margin"],
                marker=dict(color=PALETTE[3:3+len(dom_m)], line=dict(width=0)),
                text=[f"₹{v/1e5:.1f}L" for v in dom_m["Margin"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=12, family="JetBrains Mono")))
            fig8.update_layout(**clayout(f"{label} Margin by Domain", 310)); fig8.update_yaxes(showticklabels=False)
            st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar":False}, key="chart_15")
            st.markdown('</div>', unsafe_allow_html=True)
    with domain_tab1: domain_charts(ef, "Exit")
    with domain_tab2: domain_charts(pf, "Pipeline")

    # Exit type + trend
    sec("EXIT TYPE & MONTHLY TREND", "#f472b6")
    ec1, ec2, ec3 = st.columns([1, 1, 1.4])
    with ec1:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        et = ef["exit_type"].value_counts().reset_index(); et.columns = ["Type","Count"]
        fig9 = go.Figure(go.Pie(labels=et["Type"], values=et["Count"], hole=0.5,
            marker=dict(colors=PALETTE[:len(et)], line=dict(color=T['app_bg'], width=2)),
            textfont=dict(color="#ffffff", size=10), textinfo="percent"))
        fig9.update_layout(**clayout("Exit Type · Exits", 330))
        fig9.update_layout(legend=dict(orientation="v", x=1.02, y=0.5, font=dict(color="#cbd5e1",size=9), bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar":False}, key="chart_16")
        st.markdown('</div>', unsafe_allow_html=True)
    with ec2:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        pt = pf["exit_type"].value_counts().reset_index(); pt.columns = ["Type","Count"]
        if not pt.empty:
            fig10 = go.Figure(go.Pie(labels=pt["Type"], values=pt["Count"], hole=0.5,
                marker=dict(colors=PALETTE[3:3+len(pt)], line=dict(color=T['app_bg'], width=2)),
                textfont=dict(color="#ffffff", size=10), textinfo="percent"))
            fig10.update_layout(**clayout("Exit Type · Pipeline", 330))
            fig10.update_layout(legend=dict(orientation="v", x=1.02, y=0.5, font=dict(color="#cbd5e1",size=9), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig10, use_container_width=True, config={"displayModeBar":False}, key="chart_17")
        else:
            st.info("No pipeline data.")
        st.markdown('</div>', unsafe_allow_html=True)
    with ec3:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        trend_months = sorted(ef["Month"].dropna().unique(), key=msort)
        trend = (ef.groupby("Month").agg(Exits=("employee_id","count"), PO=("p_o_value","sum"))
                   .reindex(trend_months).reset_index())
        trend["Exits"] = pd.to_numeric(trend["Exits"], errors="coerce").fillna(0)
        trend["PO"]    = pd.to_numeric(trend["PO"],    errors="coerce").fillna(0)
        fig11 = make_subplots(specs=[[{"secondary_y": True}]])
        fig11.add_trace(go.Bar(x=trend["Month"], y=trend["Exits"], name="Exit Count",
            marker=dict(color="rgba(59,130,246,0.35)", line=dict(color="#60a5fa", width=1.5))), secondary_y=False)
        fig11.add_trace(go.Scatter(x=trend["Month"], y=trend["PO"], name="P.O Value",
            line=dict(color="#34d399", width=2.5), mode="lines+markers",
            marker=dict(size=8, color="#34d399", line=dict(color=T['app_bg'], width=2))), secondary_y=True)
        lo = clayout("Monthly Exit Trend", 330)
        lo["legend"] = dict(orientation="h", y=1.06, x=1, xanchor="right", bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1",size=10))
        fig11.update_layout(**lo)
        fig11.update_yaxes(gridcolor=T['grid'], tickfont=dict(color="#64748b",size=10), secondary_y=False)
        fig11.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=dict(color="#64748b",size=10), secondary_y=True)
        st.plotly_chart(fig11, use_container_width=True, config={"displayModeBar":False}, key="chart_18")
        st.markdown('</div>', unsafe_allow_html=True)

    # Raw Data
    sec("RAW DATA", "#64748b")
    tab1, tab2 = st.tabs(["  📋  Exit Records  ", "  🔄  Pipeline Records  "])
    EXIT_COLS = {"full_name":"Full Name","employee_id":"Employee ID","employee_type":"Emp Type",
                 "company_name":"Client","Domain":"Domain","Business Head":"Business Head","HRBP":"HRBP",
                 "exit_type":"Exit Type","last_work_day":"Last Working Day",
                 "p_o_value":"P.O Value (₹)","margin":"Margin (₹)",
                 "recruiter_name":"Recruiter","manager_name":"Manager","Month":"Month","created_date":"Created Date"}
    PIPE_COLS = {"full_name":"Full Name","employee_id":"Employee ID","employee_type":"Emp Type",
                 "company_name":"Client","Domain":"Domain","Business Head":"Business Head","HRBP":"HRBP",
                 "exit_type":"Exit Type","tentative_exit_date":"Tentative Exit Date",
                 "p_o_value":"P.O Value (₹)","margin":"Margin (₹)",
                 "recruiter_name":"Recruiter","manager_name":"Manager","Month":"Month","created_date":"Created Date"}

    def show_table(df, col_map, label):
        avail = {k:v for k,v in col_map.items() if k in df.columns}
        ddf = df[list(avail.keys())].copy().rename(columns=avail)
        if "P.O Value (₹)" in ddf.columns: ddf["P.O Value (₹)"] = ddf["P.O Value (₹)"].apply(lambda x: f"₹{x:,.0f}")
        if "Margin (₹)"    in ddf.columns: ddf["Margin (₹)"]    = ddf["Margin (₹)"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(ddf.reset_index(drop=True), use_container_width=True, height=360)
        total_po  = df["p_o_value"].sum(); total_mar = df["margin"].sum()
        uniq_cli  = df["company_name"].nunique(); uniq_dom = df["Domain"].nunique()
        st.markdown(f"""<div class="totals-bar">
            <div class="tot-item"><div class="tot-label">Total {label}</div><div class="tot-value blue">{len(df):,} HC</div></div>
            <div class="tot-item"><div class="tot-label">Total P.O Value</div><div class="tot-value green">₹{total_po:,.0f}</div></div>
            <div class="tot-item"><div class="tot-label">Total Margin</div><div class="tot-value amber">₹{total_mar:,.0f}</div></div>
            <div class="tot-item"><div class="tot-label">Unique Clients</div><div class="tot-value purple">{uniq_cli:,}</div></div>
            <div class="tot-item"><div class="tot-label">Unique Domains</div><div class="tot-value">{uniq_dom:,}</div></div>
        </div>""", unsafe_allow_html=True)
    with tab1: show_table(ef, EXIT_COLS, "Exits")
    with tab2: show_table(pf, PIPE_COLS, "Pipeline")

    # Created HC & PO — EXIT ONLY
    sec(f"CREATED HEADCOUNT & P.O VALUE  ·  {cr_from.strftime('%d %b %Y')} → {cr_to.strftime('%d %b %Y')}", "#4ade80")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-cr" style="border-color:#2d5aa0;">
            <div class="top-bar" style="background:linear-gradient(90deg,#60a5fa,#3b82f6);"></div>
            <div class="lbl" style="color:#93c5fd;">🚪 Exit Created HC</div>
            <div class="hc">{cr_exit_hc:,}</div>
            <div class="po" style="color:#60a5fa;">P.O  ₹{cr_exit_po:,.0f}</div>
            <div class="po" style="color:#475569;font-size:11px;">Margin  ₹{cr_exit_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-cr" style="border-color:#c2410c;">
            <div class="top-bar" style="background:linear-gradient(90deg,#fb923c,#f97316);"></div>
            <div class="lbl" style="color:#fdba74;">⚠️ Pipeline Created HC</div>
            <div class="hc">{cr_pipe_hc:,}</div>
            <div class="po" style="color:#fb923c;">P.O  ₹{cr_pipe_po:,.0f}</div>
            <div class="po" style="color:#475569;font-size:11px;">Margin  ₹{cr_pipe_mar:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-cr" style="border-color:#059669;background:linear-gradient(135deg,#052e16,#064e3b);">
            <div class="top-bar" style="background:linear-gradient(90deg,#34d399,#10b981);"></div>
            <div class="lbl" style="color:#6ee7b7;">📊 Total Created HC</div>
            <div class="hc">{cr_exit_hc + cr_pipe_hc:,}</div>
            <div class="po" style="color:#34d399;">P.O  ₹{cr_exit_po + cr_pipe_po:,.0f}</div>
            <div class="po" style="color:#475569;font-size:11px;">Exit + Pipeline</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        days = max((cr_to - cr_from).days, 1)
        avg  = cr_exit_hc / days
        st.markdown(f"""<div class="kpi-cr" style="border-color:#7c3aed;background:linear-gradient(135deg,#1e1b4b,#2e1065);">
            <div class="top-bar" style="background:linear-gradient(90deg,#a78bfa,#8b5cf6);"></div>
            <div class="lbl" style="color:#c4b5fd;">📈 Avg Exits / Day</div>
            <div class="hc">{avg:.1f}</div>
            <div class="po" style="color:#a78bfa;">Over {days} day(s)</div>
            <div class="po" style="color:#475569;font-size:11px;">Based on exit created</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    cl_tab1, cl_tab2 = st.tabs(["  🚪 Exit Created — Client List  ", "  🔄 Pipeline Created — Client List  "])

    def client_list_view(df_cr):
        if df_cr.empty:
            st.info("No records found for the selected date range."); return
        m1, m2, m3, m4 = st.columns(4)
        def stat_card(col, label, value, color):
            col.markdown(f"""<div style="background:#1e2d45;border:1px solid #2a4a7f;border-radius:10px;
                 padding:14px 18px;border-top:3px solid {color};">
                <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#94a3b8;margin-bottom:8px;">{label}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:700;color:#f1f5f9;">{value}</div>
            </div>""", unsafe_allow_html=True)
        stat_card(m1, "Total HC",       f"{len(df_cr):,}",                     "#60a5fa")
        stat_card(m2, "Total P.O",      f"₹{df_cr['p_o_value'].sum():,.0f}",   "#34d399")
        stat_card(m3, "Total Margin",   f"₹{df_cr['margin'].sum():,.0f}",      "#fb923c")
        stat_card(m4, "Unique Clients", f"{df_cr['company_name'].nunique():,}", "#a78bfa")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        summary = (df_cr.groupby("company_name")
                        .agg(HC=("employee_id","count"), PO=("p_o_value","sum"), Margin=("margin","sum"))
                        .reset_index().sort_values("HC", ascending=False)
                        .rename(columns={"company_name":"Client"}))
        summary["P.O Value (₹)"] = summary["PO"].apply(lambda x: f"₹{x:,.0f}")
        summary["Margin (₹)"]    = summary["Margin"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(summary[["Client","HC","P.O Value (₹)","Margin (₹)"]].reset_index(drop=True),
                     use_container_width=True, height=min(60 + len(summary) * 35, 500))

    with cl_tab1: client_list_view(ef_cr)
    with cl_tab2: client_list_view(pf_cr)

# ── FOOTER ──
st.markdown(f"""<div style="margin-top:3rem;padding:1rem 0;border-top:1px solid {T['grid']};
     display:flex;justify-content:space-between;align-items:center;">
    <div style="font-size:11px;color:{T['text_dim']};font-weight:700;letter-spacing:2px;">⚡ JOULESTOWAATTS · ONBOARDING & EXIT ANALYTICS</div>
    <div style="font-size:10px;color:{T['text_dim']};">Auto-refreshes every 5 min · Exit & Exit Pip.xlsx</div>
</div>""", unsafe_allow_html=True)
