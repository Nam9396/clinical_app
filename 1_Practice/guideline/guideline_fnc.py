from pathlib import Path
import streamlit as st

GUIDELINE_REGISTRY = {

}


@st.cache_data(show_spinner=False)
def load_guideline_markdown(guideline_code):
    guideline_uri = Path("1_Practice/guidelines") / f"{GUIDELINE_REGISTRY[guideline_code]}.md"
    return guideline_uri.read_text(encoding="utf-8") 
