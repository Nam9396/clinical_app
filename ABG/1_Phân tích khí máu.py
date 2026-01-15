import streamlit as st
import time 
from pathlib import Path
from App.graphs._1_qa_chain import abg_qa
from App.components.ui import display_retry_loop_error

st.set_page_config(page_title="Phân tích khí máu động mạch", layout="centered")
st.markdown("## Phân tích khí máu động mạch")


# === Tải nội dung hướng dẫn ===

PROTOCOL_DIR = Path("ABG")
protocol_file = PROTOCOL_DIR / "abg_utils" / "abg_guide.md"

if not protocol_file.exists():
    st.error(f"Không tìm thấy hướng dẫn")
    st.stop()

@st.cache_data(show_spinner=False)
def load_protocol_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")

guideline_text = load_protocol_markdown(protocol_file)

if guideline_text:
    if "guideline_text" not in st.session_state:
        st.session_state["guideline_text"] = guideline_text
else: 
    st.error(f"Lỗi khi tải hướng dẫn: {guideline_text}")
    st.stop()

with st.expander("📄 Nội dung hướng dẫn"):
    st.markdown(guideline_text)


# === Nhập dữ liệu đầu vào ===

def nutrition_row(label):
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        c1_label = st.markdown(label)
    with c2:
        c2_input = st.number_input(
            f"{label}", 
            label_visibility="collapsed",
            key=label
        )
    return c1_label, c2_input

input_components = [
    "Tuổi", 
    "SpO2",
    "FiO2",
    "pH", 
    "PaCO2", 
    "PaO2", 
    "SaO2", 
    "HCO3",
    "BE", 
    "Lactate", 
    "Na", 
    "K", 
    "Cl"
]

for item in input_components:
    nutrition_row(item)

input_info = {
    "Tuổi": st.session_state["Tuổi"], 
    "SpO2": st.session_state["SpO2"],
    "FiO2": st.session_state["FiO2"],
    "pH": st.session_state["pH"], 
    "PaCO2": st.session_state["PaCO2"], 
    "PaO2": st.session_state["PaO2"], 
    "HCO3": st.session_state["HCO3"],
    "BE": st.session_state["BE"], 
    "Lactate": st.session_state["Lactate"], 
    "Na": st.session_state["Na"], 
    "K": st.session_state["K"], 
    "Cl": st.session_state["Cl"]
}

st.markdown("---")

with st.form(key='qa_form'):
    submit = st.form_submit_button("Thực hiện")


# === Đưa ra câu trả lời ===

if submit:

    with st.spinner("Đang xử lý ... Vui lòng đợi trong giây lát⏳", show_time=True):     
        response = None

        for attempt in range(3):
            try:
                response = abg_qa(
                    input_info=input_info, 
                    context=guideline_text,
                )
                break
            except Exception as e:
                display_retry_loop_error(e)
                time.sleep(2)
        
        if response is None:
            st.error(f"[FAILED] Thất bại sau 3 lần thử. Bấm tải lại chương trình sau vài phút.")
            st.stop()
    
        st.markdown("#### CÂU TRẢ LỜI")

        st.markdown(response)


        


