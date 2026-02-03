import streamlit as st

# ==== Trang dinh dưỡng ===

cal_nutrition_need = st.Page(
    "Nutrition/1_nutrition_cal.py", 
    title="Tính nhu cầu dinh dưỡng", icon=":material/nutrition:", 
)

eval_nutrition_formula = st.Page(
    "Nutrition/2_nutrition_analysis.py", 
    title="Phân tích dinh dưỡng", 
    icon=":material/calendar_meal:"
)

nutrition_note = st.Page(
    "Nutrition/3_nutrition_note.py", 
    title="Ghi chú dinh dưỡng", 
    icon=":material/notes:"
)

# === Trang KMĐM ===

abg_analysis = st.Page(
    "ABG/1_abg_analysis.py", 
    title="Phân tích khí máu", icon=":material/spo2:", 
)

abg_note = st.Page(
    "ABG/2_abg_note.py", 
    title="Ghi chú khí máu", icon=":material/notes:", 
)

# === Trang hướng dẫn thực hành ===

practice = st.Page(
    "Practice/1_practice.py", 
    title="Thực hành", icon=":material/quick_reference:", 
    default=True        
)

# === Trang thông tin thuốc ===

med_cal = st.Page(
    "Medication/1_med_cal.py", 
    title="Thông tin thuốc", icon=":material/pill:", 
)



# =================================
 
pg = st.navigation(
    {
        "Practice": [practice],
        "Mediaction": [med_cal],
        "ABG": [abg_analysis, abg_note], 
        "Nutrition": [cal_nutrition_need, eval_nutrition_formula, nutrition_note],
    }
)

pg.run()