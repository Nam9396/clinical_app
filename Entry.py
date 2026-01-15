import streamlit as st

# ==== Trang dinh dưỡng ===

cal_nutrition_need = st.Page(
    "Nutrition/1_Tính nhu cầu dinh dưỡng.py", 
    title="Tính nhu cầu dinh dưỡng", icon=":material/nutrition:", 
    default=True
)

eval_nutrition_formula = st.Page(
    "Nutrition/2_Phân tích dinh dưỡng.py", 
    title="Phân tích dinh dưỡng", 
    icon=":material/calendar_meal:"
)

nutrition_note = st.Page(
    "Nutrition/3_Ghi chú dinh dưỡng.py", 
    title="Ghi chú dinh dưỡng", 
    icon=":material/notes:"
)

# === Trang KMĐM ===

abg_analysis = st.Page(
    "ABG/1_Phân tích khí máu.py", 
    title="Phân tích khí máu", icon=":material/spo2:", 
)



pg = st.navigation(
    {
        "Nutrition": [cal_nutrition_need, eval_nutrition_formula, nutrition_note],
        "ABG": [abg_analysis]
    }
)


pg.run()