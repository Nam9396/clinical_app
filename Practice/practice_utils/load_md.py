from pathlib import Path
import streamlit as st

PRACTICE_REGISTRY = {
    "Hạ Kali": "emergency/hạ kali.md", 
    "Hạ Natri": "emergency/hạ natri.md", 
    "Hạ Canxi": "emergency/hạ canxi.md", 
    "Tăng Kali": "emergency/tăng kali.md", 
    "Tăng Natri": "emergency/tăng natri.md",
    "Hạ đường huyết": "emergency/hạ đường huyết.md",
    "Tăng áp nội sọ": "emergency/tăng áp nội sọ.md",
    "Toan chuyển hóa": "emergency/toan chuyển hóa.md",
}


@st.cache_data(show_spinner=False)
def load_practice_markdown(practice_code):
    protocol_uri = Path("Practice") / f"{PRACTICE_REGISTRY[practice_code]}"
    return protocol_uri.read_text(encoding="utf-8") 
