import base64
import streamlit as st
from pathlib import Path

md_path = Path("Nutrition/nutrition_utils/Ghi chú dinh dưỡng.md")

def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Sau khi đọc nội dung Markdown
md_content = md_path.read_text(encoding="utf-8")

# Tìm và thay thế thẻ ảnh bằng dữ liệu Base64
img_base64 = get_image_base64("Nutrition/images/ion_need.png")
md_content = md_content.replace("ion_need.png", f"data:image/png;base64,{img_base64}")

st.markdown(md_content, unsafe_allow_html=True)