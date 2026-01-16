import streamlit as st
import os
from langchain_openai import ChatOpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

rag_prompt_template = """
Bạn là một người hỗ trợ cho bác sĩ ung thư. Nhiệm vụ của bạn là đọc phác đồ, trả lời câu hỏi và hỗ trợ bác sĩ đưa ra các quyết định điều trị. 

### Hướng dẫn: 
-	Liệt kê thông tin nền. 
-   Nhớ kiểm tra điều kiện tuổi khi xác định loại thuốc cần dùng
-	Xem xét dữ kiện cung cấp, đối chiếu với phác đồ. 
-	Tư duy và đưa ra câu trả lời.

### Về cách trình bày:
1.	Bố cục câu trả lời rõ ràng, súc tích, sử dụng **headings, bullet points**, or **numbered sections** nếu cần thiết.
2.	Nếu có liên quan, hãy bao gồm bảng tóm tắt nêu bật các kết quả chính, so sánh, hoặc các điểm dữ liệu quan trọng được đề cập trong tài liệu.

### Lưu ý quan trọng: 
- **CHỈ** sử dụng thông tin trong phần **Nguồn tài liệu**.
- **KHÔNG ĐƯỢC** bao gồm kiến thức chung, giả định, hoặc diễn giải cá nhân.
- Nếu **Nguồn tài liệu** không đủ để trả lời câu hỏi, hãy thừa nhận giới hạn của câu trả lời.

---
**Thông tin nền**:
{base_info}

**Câu hỏi**: {input}

**Nguồn tài liệu**:
{context}
"""

abg_prompt_template = """
Nhiệm vụ của bạn là phân tích kết quả khí máu động mạch dựa trên thông tin được cung cấp. 

### Nhiệm vụ
-	Xác định các giá trị khí máu là bình thường hay bất thường 
-	Xác định kết quả khí máu có sai sót kĩ thuật không
-	Chỉ ra tương quan giữa SpO2 với SaO2 
-	Nhận xét ngắn gọn về tình trạng thông khí của bệnh nhân 
-	Nhận xét ngắn gọn về nồng độ hemoglobin 
-	So sánh PaO2 dự đoán với FiO2, đưa ra kết luận 
-	Đánh giá tình trạng ARDS
-	Tính shunt bệnh lý và đưa ra kết luận 
-	Tính AaDO2, tăng giảm hay bình thường
-	Đánh giá pH, toan kiềm hay bình thường 
-	Xác định nguyên nhân rối loạn pH, do hô hấp hay chuyển hóa 
-	Nhấn mạnh giá trị BE 
-	Nếu là do rối loạn hô hấp, xác định cấp hay mạn và mức độ bù trừ 
-	Nếu là do rối loạn chuyển hóa, xác định mức độ bù trừ 
-	Nếu là toan chuyển hóa, tính AG và xác định phân loại toan chuyển hóa 

### Hướng dẫn: 
- Tư duy và đưa ra câu trả lời.
- Trường có giá trị bằng 0 là trường thiếu dữ liệu
- Bố cục câu trả lời rõ ràng, súc tích, sử dụng **headings, bullet points**, or **numbered sections** nếu cần thiết.

### Lưu ý quan trọng: 
- **CHỈ** sử dụng thông tin trong phần **Nguồn tài liệu**.
- **KHÔNG ĐƯỢC** bao gồm kiến thức chung, giả định, hoặc diễn giải cá nhân.
- Nếu **Nguồn tài liệu** không đủ để trả lời câu hỏi, hãy thừa nhận giới hạn của câu trả lời.

---
**Thông tin đầu vào**:
{input_info}

**Nguồn tài liệu**:
{context}
"""


@st.cache_resource(show_spinner=True)
def get_rag_model():
    return ChatOpenAI(
        model=st.session_state.get("LLM_MODEL", "gpt-5-mini"),
        api_key=OPENAI_API_KEY,
        temperature=0.2,
        # top_p=0.9,
        # presence_penalty=0.1,
        # frequency_penalty=0.2
    )
