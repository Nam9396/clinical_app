import streamlit as st
from backend.chains._1_qa_chain import med_cal_chain
from Medication.med_utils.load_md import load_med_markdown


st.title("HỎI ĐÁP THÔNG TIN THUỐC")

med_list = [
    # thuốc kháng sinh
    "Acyclovir", 
    "Amikacin", 
    "Cefepime", 
    "Cefotaxime", 
    "Ceftazidime", 
    "Ceftriaxone", 
    "Ciprofloxacin", 
    "Clindamycin", 
    "Gentamicin", 
    "Imipenem", 
    "Linezolid", 
    "Meropenem", 
    "Metronidazole", 
    "Oxacillin", 
    "Ticarcillin", 
    "Vancomycin", 

    # thuốc thần kinh
    "Diazepam", 
    "Midazolam",
    "Phenobarbital"
]


with st.form(key='protocol_form'):
    med_code = st.selectbox(
        "Các thuốc thường dùng",
        options=med_list,
    )
    query = st.text_area("Đặt câu hỏi về thuốc", height="content")
    submit = st.form_submit_button('Thực hiện')

if submit:    

    med_info_text = load_med_markdown(med_code)

    with st.expander("📄 Thông tin về thuốc"):
        st.markdown(med_info_text)
    
    with st.spinner("Đang suy nghĩ ...", show_time=True):
        answer = med_cal_chain(
            query=query, 
            context=med_info_text
        )
        
        st.markdown(answer)

    



