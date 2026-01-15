import streamlit as st
from pathlib import Path

md_path = Path("ABG/abg_utils/Ghi chú ABG.md")

# Sau khi đọc nội dung Markdown
md_content = md_path.read_text(encoding="utf-8")

st.markdown(md_content, unsafe_allow_html=True)