import streamlit as st
from backend.chains._1_qa_chain import practice_chain



st.markdown("## TRA CỨU CÁC VẤN ĐỀ THỰC HÀNH")

guideline_list = [
    
]

with st.form(key='guideline_form'):

    guideline_code = st.selectbox(
        "Tên vấn đề thực hành",
        options=guideline_list,
    )

    query = st.text_area("Đặt câu hỏi về thực hành lâm sàng", height="content")

    submit = st.form_submit_button('Thực hiện')


if submit and query and guideline_code :

    guideline_text = load_guideline_markdown(guideline_code)

    with st.expander("📄 Nội dung hướng dẫn"):
        st.markdown(guideline_text)
    
    with st.spinner("Đang suy nghĩ ...", show_time=True):
        answer = practice_chain(
            query=query, 
            context=guideline_text
        )
        st.markdown(answer)

    



