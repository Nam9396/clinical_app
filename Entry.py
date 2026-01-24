import streamlit as st

# ==== Trang dinh dưỡng ===

cal_nutrition_need = st.Page(
    "3_Nutrition/1_Tính nhu cầu dinh dưỡng.py", 
    title="Tính nhu cầu dinh dưỡng", icon=":material/nutrition:", 
    default=True
)

eval_nutrition_formula = st.Page(
    "3_Nutrition/2_Phân tích dinh dưỡng.py", 
    title="Phân tích dinh dưỡng", 
    icon=":material/calendar_meal:"
)

nutrition_note = st.Page(
    "3_Nutrition/3_Ghi chú dinh dưỡng.py", 
    title="Ghi chú dinh dưỡng", 
    icon=":material/notes:"
)

# === Trang KMĐM ===

abg_analysis = st.Page(
    "2_ABG/1_Phân tích khí máu.py", 
    title="Phân tích khí máu", icon=":material/spo2:", 
)

abg_note = st.Page(
    "2_ABG/2_Ghi chú ABG.py", 
    title="Ghi chú khí máu", icon=":material/notes:", 
)

# === Trang hướng dẫn thực hành ===

practice = st.Page(
    "1_Practice/1_Thực hành.py", 
    title="Thực hành", icon=":material/quick_reference:", 
)


# =================================
 
pg = st.navigation(
    {
        "1_Practice": [practice],
        "2_ABG": [abg_analysis, abg_note], 
        "3_Nutrition": [cal_nutrition_need, eval_nutrition_formula, nutrition_note],
    }
)


pg.run()