import os
import base64
import streamlit as st
from ui_study import render_study_tab
from ui_pyq import render_pyq_tab
from ui_test import render_test_tab
from ui_dashboard import render_dashboard_tab

LOGO_PATH = "logo.png"


def get_logo_base64(path: str = LOGO_PATH) -> str:
    """Encodes the local logo image as base64 for inline HTML rendering."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


logo_b64 = get_logo_base64()

st.set_page_config(
    page_title="NoteCraft AI · MSRIT",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "📓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CLEAN LIGHT-MODE SWISS / NOTION CSS ---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-app: #FAFAFA;
            --bg-card: #FFFFFF;
            --bg-subtle: #F3F4F6;
            --border-color: #E5E7EB;
            --border-strong: #D1D5DB;
            --text-main: #111827;
            --text-muted: #6B7280;
            --accent-bg: #18181B;
            --accent-text: #FFFFFF;
            --amber-bg: #FFFBEB;
            --amber-border: #FDE68A;
            --amber-text: #92400E;
            --amber-sub: #78350F;
            --green-bg: #F0FDF4;
            --green-border: #BBF7D0;
            --green-text: #166534;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #FAFAFA;
        }

        /* Hide default Streamlit chrome */
        #MainMenu, footer { visibility: hidden; }
        [data-testid="stDecoration"] { display: none; }
        header[data-testid="stHeader"] { background: transparent; height: 2rem; }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1240px;
        }

        /* Crisp white cards for bordered containers */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB !important;
            border-radius: 14px !important;
            padding: 0.4rem !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }

        /* Segmented pill navigation tabs */
        div[data-baseweb="tab-list"] {
            background-color: #F3F4F6;
            padding: 5px;
            border-radius: 10px;
            border: 1px solid #E5E7EB;
            gap: 4px;
            width: fit-content;
            margin-bottom: 1.2rem;
        }
        div[data-baseweb="tab-highlight"],
        div[data-baseweb="tab-border"] {
            display: none !important;
        }
        button[data-baseweb="tab"] {
            border-radius: 7px !important;
            padding: 7px 18px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #4B5563 !important;
            background: transparent !important;
            transition: all 0.15s ease;
        }
        button[data-baseweb="tab"]:hover {
            color: #111827 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #18181B !important;
            color: #FFFFFF !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        }
        button[data-baseweb="tab"][aria-selected="true"] * {
            color: #FFFFFF !important;
        }

        /* Primary buttons (matte black with crisp white text) */
        .stButton > button[kind="primary"] {
            background-color: #18181B !important;
            color: #FFFFFF !important;
            border: 1px solid #18181B !important;
            border-radius: 9px;
            font-weight: 500;
            padding: 0.55rem 1.1rem;
            transition: background-color 0.15s ease;
        }
        .stButton > button[kind="primary"] * {
            color: #FFFFFF !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #27272A !important;
            border-color: #27272A !important;
        }

        /* Secondary & download buttons (white with dark text) */
        .stButton > button[kind="secondary"],
        .stDownloadButton > button {
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 9px;
            font-weight: 500;
            font-size: 0.82rem;
        }
        .stButton > button[kind="secondary"] *,
        .stDownloadButton > button * {
            color: #111827 !important;
        }
        .stButton > button[kind="secondary"]:hover,
        .stDownloadButton > button:hover {
            background-color: #F9FAFB !important;
            border-color: #18181B !important;
        }

        /* File uploader dropzone */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #FAFAFA;
            border: 1px dashed #D1D5DB;
            border-radius: 10px;
        }
        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #18181B;
            background-color: #F3F4F6;
        }

        /* Custom layout components */
        .mono {
            font-family: 'JetBrains Mono', monospace;
        }
        .nc-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 14px 20px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        }
        .nc-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .nc-logo {
            width: 36px;
            height: 36px;
            border-radius: 9px;
            background: #18181B;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: -0.5px;
        }
        .nc-title {
            font-size: 16px;
            font-weight: 600;
            color: #111827;
            line-height: 1.2;
        }
        .nc-sub {
            font-size: 12px;
            color: #6B7280;
            margin-top: 2px;
        }
        .nc-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid #E5E7EB;
            background: #FAFAFA;
            color: #374151;
        }
        .nc-badge-green {
            border-color: #BBF7D0;
            background: #F0FDF4;
            color: #166534;
        }
        .nc-badge-amber {
            border-color: #FDE68A;
            background: #FFFBEB;
            color: #92400E;
        }
        .nc-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #16A34A;
            display: inline-block;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- STARTUP ONBOARDING (Centered Editorial Card) ---
if "profile" not in st.session_state:
    st.write("")
    st.write("")
    _, center_col, _ = st.columns([1, 2.2, 1])

    with center_col:
        onboarding_logo = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="width:72px; height:72px; border-radius:18px; object-fit:cover; '
            f'border:1px solid #E5E7EB; box-shadow:0 4px 12px rgba(0,0,0,0.08);" />'
            if logo_b64
            else '<div class="nc-logo" style="width:64px; height:64px; border-radius:16px; font-size:20px;">NC</div>'
        )

        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:22px;">
                <div style="display:flex; justify-content:center; margin-bottom:14px;">
                    {onboarding_logo}
                </div>
                <div style="display:inline-flex; align-items:center; gap:8px; padding:5px 12px; border-radius:999px; border:1px solid #E5E7EB; background:#FFFFFF; font-family:'JetBrains Mono',monospace; font-size:11px; color:#4B5563; margin-bottom:12px;">
                    MSRIT · Team NetRunners · wHACKiest 2026
                </div>
                <div style="font-size:32px; font-weight:700; letter-spacing:-0.03em; color:#111827; line-height:1.15;">
                    NoteCraft AI
                </div>
                <div style="font-size:14px; color:#6B7280; margin-top:8px;">
                    Connect classroom lectures, teacher emphasis &amp; RIT Notebook PYQs in one workspace.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.markdown("##### Configure Your Academic Context")
            st.caption("Your Drive catalog, PYQ Vault, and Weakness Dashboard automatically adapt to this.")
            st.write("")

            c1, c2 = st.columns(2)
            year = c1.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
            cycle = c2.selectbox(
                "Cycle / Semester",
                ["Physics Cycle", "Chemistry Cycle", "Sem 3", "Sem 4", "Sem 5", "Sem 6"]
            )
            branch = st.selectbox(
                "Branch",
                ["AI & Data Science", "CSE", "ISE", "CSE (AI & ML)", "ECE", "Other"]
            )

            st.write("")
            if st.button("Enter Workspace →", type="primary", use_container_width=True):
                st.session_state["profile"] = {
                    "year": year,
                    "cycle": cycle,
                    "branch": branch
                }
                st.rerun()
    st.stop()

# --- TOP NAVIGATION BAR ---
profile = st.session_state["profile"]
nav_left, nav_profile = st.columns([5.2, 1], vertical_alignment="center")

navbar_logo = (
    f'<img src="data:image/png;base64,{logo_b64}" '
    f'style="width:38px; height:38px; border-radius:9px; object-fit:cover; border:1px solid #E5E7EB;" />'
    if logo_b64
    else '<div class="nc-logo">NC</div>'
)

with nav_left:
    st.markdown(
        f"""
        <div class="nc-navbar">
            <div class="nc-brand">
                {navbar_logo}
                <div>
                    <div class="nc-title">NoteCraft AI <span style="font-weight:400; color:#9CA3AF;">/ MSRIT</span></div>
                    <div class="nc-sub">{profile['year']} · {profile['cycle']} · {profile['branch']}</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="nc-badge nc-badge-green"><span class="nc-dot"></span>OpenRouter + Whisper Ready</span>
                <span class="nc-badge">Team NetRunners</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with nav_profile:
    if st.button("Switch Profile", use_container_width=True):
        del st.session_state["profile"]
        st.rerun()

st.write("")

# --- 4-TAB SEGMENTED NAVIGATION ---
tab_study, tab_pyq, tab_test, tab_dash = st.tabs([
    "Study Pack", "PYQ Vault", "Test Me", "Analytics"
])

with tab_study:
    render_study_tab(profile)
with tab_pyq:
    render_pyq_tab(profile)
with tab_test:
    render_test_tab(profile)
with tab_dash:
    render_dashboard_tab(profile)