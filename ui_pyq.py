import streamlit as st

def render_pyq_tab(profile: dict):
    st.markdown("#### PYQ Vault (RIT Notebook Archive)")
    st.info(f"Scoped to: {profile['year']} · {profile['cycle']} · {profile['branch']}. Full Drive PYQ search & frequency trends coming on Hackathon Day.")