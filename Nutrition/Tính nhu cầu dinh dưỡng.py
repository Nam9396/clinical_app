import streamlit as st
import pandas as pd
from Nutrition.nutrition_utils.nutrition_store import protein_ls, lipid_ls, glucose_ls, na_ls, k_ls, ca_ls, mg_ls, po_nutrition_ls
from Nutrition.nutrition_utils.nutrition_fnc import calc_fluid_need_holliday_segar, calc_ree, solve_glucose_mix_safe, display_row

st.set_page_config(page_title="Tính nhu cầu dinh dưỡng", layout="centered")
st.markdown("## Tính nhu cầu dinh dưỡng")


# ================== CONTAINER ==================

st.markdown("### Thông tin bệnh nhân")

c1, c2 = st.columns(2)
with c1:
    age = st.number_input("Tuổi", min_value=0, max_value=120, value=1, key="age")
    weight = st.number_input("Cân nặng (kg)", min_value=0.0, value=0.0, key="weight")
    extra_fluid = st.number_input("Dịch tăng thêm", min_value=0.0, value=0.0, key="extra_fluid")
with c2:
    sex = st.selectbox("Giới", ["Nam", "Nữ"], key="sex")
    height = st.number_input("Chiều cao (cm)", min_value=0.0, value=0.0, key="height")
    stress_index = st.number_input("Chỉ số stress", min_value=0.0, value=1.0, key="stress_index", help="1.2: Dinh dưỡng tốt, vết thương lành tốt. 1.5: Sepsis, suy tim, suy dinh dưỡng. 2: Stress nặng, bỏng nặng")

st.markdown("---") 


if st.session_state["age"] == 0 or st.session_state["weight"] == 0 or st.session_state["height"] == 0: 
    st.warning("Vui lòng điền đủ thông tin bệnh nhân")
    st.stop()


# ================== CONTAINER ==================

# st.markdown("### Loại thức ăn đường miệng")

c1, c2, c3 = st.columns(3)
with c1:
    choice = st.selectbox(
        "Chọn thức ăn đường miệng",
        po_nutrition_ls,
        format_func=lambda x: x["name"], 
        key="po_sol"
    )
with c2:
    vol = st.number_input(
        "Số ml",
        min_value=0.0,
        value=0.0,
        key="po_ml"
    )
with c3:
    vol = st.number_input(
        "Số cữ",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="num_feeds"
    )

st.markdown("---")


# ================== CONTAINER ==================

# st.markdown("### Nhập tổng thể tích thuốc")

c1, c2 = st.columns(2, vertical_alignment="center")
with c1:
    c1_label = st.markdown("Nhập tổng thể tích thuốc")
with c2:
    c2_input = st.number_input(
        "Thể tích thuốc",
        label_visibility="collapsed",
        min_value=0.0,
        key="med_vol"
    )

st.markdown("---")


# ================== CONTAINER ==================

# st.markdown("### Nhu cầu dinh dưỡng")

# tạo object nhu cầu dinh dưỡng
nutrition_needs = [
    {
        "label": "Nhu cầu protein", 
        "value": 1.0, 
        "key": "protein_need"
    },
    {
        "label": "Nhu cầu lipid", 
        "value": 1.0, 
        "key": "lipid_need"
    },
    {
        "label": "Nhu cầu Natri", 
        "value": 3.0, 
        "key": "na_need"
    },
    {
        "label": "Nhu cầu Kali", 
        "value": 2.0, 
        "key": "k_need"
    },
    {
        "label": "Nhu cầu Canxi", 
        "value": 1.0, 
        "key": "ca_need"
    },
    {
        "label": "Nhu cầu Magne", 
        "value": 0.5, 
        "key": "mg_need"
    }, 
    {
        "label": "Nhu cầu Phospho", 
        "value": None, 
        "key": "p_need"
    },
]

# tạo ra các dòng

def nutrition_row(nutri_obj):
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        c1_label = st.markdown(nutri_obj["label"])
    with c2:
        c2_input = st.number_input(
            f"{nutri_obj['key']}",
            label_visibility="collapsed",
            min_value=0.0,
            value=nutri_obj["value"],
            key=nutri_obj["key"]
        )
    return c1_label, c2_input

for obj in nutrition_needs: 
    nutrition_row(obj)

st.markdown("---")


# ================== CONTAINER ==================

# st.markdown("### Dinh dưỡng tĩnh mạch")

c1, c2 = st.columns(2, vertical_alignment="center")
with c1:
    st.markdown("Chọn đường truyền")
with c2:
    iv_route = st.selectbox(
        label="Chọn đường truyền", 
        label_visibility="collapsed", 
        options=["Ngoại biên", "Trung ương"],
        key="iv_route"
    )

def nutrition_row(label, options, key_prefix):
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        c1_label = st.markdown(f"Chọn dịch {label.lower()}")
    with c2:
        c2_choice = st.selectbox(
            f"Chọn dịch {label.lower()}",
            options,
            label_visibility="collapsed",
            format_func=lambda x: x["name"], 
            key=f"{key_prefix}_type"
        )
    return c1_label, c2_choice

nutrition_row("Protein", protein_ls, "protein")
nutrition_row("Lipid", lipid_ls, "lipid")
nutrition_row("Glucose 30%", [glucose_ls[1]], "glucose_30")
nutrition_row("Glucose 10%", [glucose_ls[0]], "glucose_10")
nutrition_row("Natri", na_ls, "na")
nutrition_row("Kali", k_ls, "k")
nutrition_row("Calci", ca_ls, "ca")
nutrition_row("Magne", mg_ls, "mg")
# nutrition_row("Phospho", electrolyte_ls, "phos")

st.markdown("---")


# ================== CONTAINER ==================

st.markdown("### Phân tích nhu cầu dinh dưỡng")

fluid_need = round((calc_fluid_need_holliday_segar() + st.session_state["extra_fluid"]), 1)
energy_need = round((calc_ree() * st.session_state["stress_index"]), 1)
po_vol = round(st.session_state["po_ml"] * st.session_state["num_feeds"], 1)
po_energy = round(st.session_state["po_sol"]["kcal_ml"] * po_vol, 1)
med_vol = st.session_state["med_vol"]
iv_vol = round(fluid_need - po_vol - med_vol, 1)
iv_energy = round(energy_need - po_energy, 1)
# infusion_rate = iv_vol / 24

protein_ml = round(st.session_state["protein_need"] * st.session_state["weight"] / st.session_state["protein_type"]["con_per_ml"], 1)
lipid_ml = round(st.session_state["lipid_need"] * st.session_state["weight"] / st.session_state["lipid_type"]["con_per_ml"], 1)
na_ml = round(st.session_state["na_need"] * st.session_state["weight"] / st.session_state["na_type"]["con_per_ml"], 1)
k_ml = round(st.session_state["k_need"] * st.session_state["weight"] / st.session_state["k_type"]["con_per_ml"], 1)
ca_ml = round(st.session_state["ca_need"] * st.session_state["weight"] / st.session_state["ca_type"]["con_per_ml"], 1)
mg_ml = round(st.session_state["mg_need"] * st.session_state["weight"] / st.session_state["mg_type"]["con_per_ml"], 1)
# p_ml = round(st.session_state["p_need"] * st.session_state["weight"] / st.session_state["p_type"]["con_per_ml"], 1)

lipid_rate = round(lipid_ml / 24, 1)
final_iv_vol = round(iv_vol - lipid_ml, 1)
final_iv_rate = round(final_iv_vol / 24, 1)

protein_kcal = round(st.session_state["protein_need"] * st.session_state["weight"] * 4, 1)
lipid_kcal = round(st.session_state["lipid_need"] * st.session_state["weight"] * 10, 1)
glucose_kcal = round(iv_energy - protein_kcal - lipid_kcal, 1)
glucose_g = round(glucose_kcal / 3.4, 1)
glucose_ml = round(final_iv_vol - protein_ml - na_ml - k_ml - ca_ml - mg_ml, 1)
g30_ml, g10_ml = solve_glucose_mix_safe(glucose_ml, glucose_g)
glucose_con = round(glucose_g / final_iv_vol * 100, 1) 
glucose_rate = round(glucose_con / 100 * 1000 * final_iv_rate / 60 / st.session_state["weight"], 1)


st.markdown(f"Nhu cầu dịch: **{fluid_need}** ml")
st.markdown(f"Nhu năng lượng: **{energy_need}** kcal")

st.markdown("---")

st.markdown("#### Dinh dưỡng đường miệng")
st.markdown(f"{st.session_state['po_sol']['name']}: {st.session_state['po_ml']} ml/cữ - {st.session_state['num_feeds']} cữ/ngày")
st.markdown(f"Thể tích dinh dưỡng đường miệng: **{po_vol}** ml")
st.markdown(f"Năng lượng dinh dưỡng đường miệng: **{po_energy}** ml")

st.markdown("---")

st.markdown("#### Dinh dưỡng đường tĩnh mạch")

display_row("Thể tích dung dịch lipid", f"{lipid_ml} ml")
display_row("Tốc độ truyền lipid", f"{lipid_rate} ml/giờ")
display_row("Thể tích thuốc", f"{med_vol} ml")
display_row("Thể tích dịch tĩnh mạch", f"{final_iv_vol} ml")
display_row(f'{st.session_state["protein_type"]["name"]}', f"{protein_ml} ml")
display_row(f'{st.session_state["lipid_type"]["name"]}', f"{lipid_ml} ml")
display_row("Glucose 30%", f"{round(g30_ml, 1)} ml")
display_row("Glucose 10%", f"{round(g10_ml, 1)} ml")
display_row(f'{st.session_state["na_type"]["name"]}', f"{na_ml} ml")
display_row(f'{st.session_state["k_type"]["name"]}', f"{k_ml} ml")
display_row(f'{st.session_state["ca_type"]["name"]}', f"{ca_ml} ml")
display_row(f'{st.session_state["mg_type"]["name"]}', f"{mg_ml} ml")
display_row("Tốc độ truyền dịch tĩnh mạch", f"{final_iv_rate} ml/giờ")
display_row(f"Nồng độ đường ({st.session_state['iv_route']})", f"{glucose_con}%")
display_row(f"Tốc độ đường ({st.session_state['iv_route']})", f"{glucose_rate} mg/kg/phút")

st.markdown("---")

st.markdown("""
- Nồng độ đường cho đường ngoại biên: < 12.5%
- Nồng độ đường cho đường trung tâm: < 25%
- Tốc độ đường khởi đầu: 6 - 8 mg/kg/phút
- Tốc độ đường mục tiêu: 10 - 14 mg/kg/phút, tối đa 15 mg/kg/phút
""")




