import streamlit as st


cal_nutrition_need = st.Page(
    "Nutrition/Tính nhu cầu dinh dưỡng.py", 
    title="Tính nhu cầu dinh dưỡng", icon=":material/nutrition:", 
    default=True
)

eval_nutrition_formula = st.Page(
    "Nutrition/Phân tích dinh dưỡng.py", 
    title="Phân tích dinh dưỡng", 
    icon=":material/calendar_meal:"
)


pg = st.navigation(
    {
        "Nutrition": [cal_nutrition_need, eval_nutrition_formula],
    }
)


pg.run()