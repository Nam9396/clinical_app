import streamlit as st


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

pg = st.navigation(
    {
        "Nutrition": [cal_nutrition_need, eval_nutrition_formula, nutrition_note],
    }
)


pg.run()