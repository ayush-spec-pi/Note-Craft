import os
import base64
import streamlit as st


def _get_logo_html(size: int = 34) -> str:
    """Returns an inline image tag for logo.png if available."""
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return (
            f'<img src="data:image/png;base64,{b64}" '
            f'style="width:{size}px; height:{size}px; border-radius:8px; '
            f'object-fit:cover; border:1px solid var(--border-color);" />'
        )
    return ""


def render_dashboard_tab(profile: dict):
    with st.container(border=True):
        logo_html = _get_logo_html(36)
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; padding-bottom:12px; border-bottom:1px solid var(--border-color); margin-bottom:14px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    {logo_html}
                    <div>
                        <div style="font-size:16px; font-weight:600; color:var(--text-main);">Real-Time Weakness Analytics</div>
                        <div style="font-size:12px; color:var(--text-muted);">
                            {profile['year']} · {profile['cycle']} · {profile['branch']} · Unit &amp; topic-wise weakness tracker
                        </div>
                    </div>
                </div>
                <span class="nc-badge">Live Plotly Tracker</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.info("Unit & Topic-wise sorted Plotly weakness tracker will connect to weakness_tracker.py on Hackathon Day.")