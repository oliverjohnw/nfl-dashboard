import streamlit as st

def streamlit_css(
    css_path: str
) -> None:
    """
    Load a CSS file into Streamlit.
    
    Args:
        css_path (srt): path to CSS file
    """
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    return
