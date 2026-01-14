import streamlit as st
import pandas as pd
from Nutrition.nutrition_utils.nutrition_store import protein_ls, lipid_ls, glucose_ls, na_ls, k_ls, ca_ls, mg_ls, po_nutrition_ls
from Nutrition.nutrition_utils.nutrition_fnc import calc_fluid_need_holliday_segar, calc_ree

st.set_page_config(page_title="Phân tích dinh dưỡng", layout="centered")
st.markdown("## Phân tích dinh dưỡng")

# ================== CONTAINER ==================

st.markdown("### Thông tin bệnh nhân")

c1, c2 = st.columns(2)

with c1:
    age = st.number_input("Tuổi", min_value=0, max_value=120, value=1, key="age")
    sex = st.selectbox("Giới", ["Nam", "Nữ"], key="sex")
    
with c2:
    weight = st.number_input("Cân nặng (kg)", min_value=0.0, value=0.0, key="weight")
    height = st.number_input("Chiều cao (cm)", min_value=0.0, value=0.0, key="height")

stress_index = st.number_input("Chỉ số stress", min_value=0.5, max_value=3.0, value=1.0, step=0.1, key="stress_index",
                         help="1.2: Dinh dưỡng tốt, vết thương lành tốt. 1.5: Sepsis, suy tim, suy dinh dưỡng. 2: Stress nặng, bỏng nặng")

extra_vol = st.number_input("Nhu cầu dịch tăng thêm", min_value=0.0, value=0.0, key="extra_vol", help="Dịch mất do tiêu chảy, lỗ rò, đa niệu, mỗi độ > 38 độ C tăng 5ml/kg/ngày")

customized_kcal = st.number_input(
    "Nhập nhu cầu năng lượng cá thể hóa", 
    min_value=0.0, 
    help="Nhập số kcal/kg/ngày theo ý muốn, nếu không, mặc định tính nhu cầu năng lượng theo chiều cao và cân nặng",
    key="customized_kcal"
)

st.markdown("---")

if st.session_state["age"] == 0 or st.session_state["weight"] == 0 or st.session_state["height"] == 0: 
    st.warning("Vui lòng điền đủ thông tin bệnh nhân")
    st.stop()


# ================== CONTAINER ==================

st.markdown("### Dinh dưỡng đường miệng")

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
        step=1.0,
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

st.markdown("### Dinh dưỡng tĩnh mạch")

c1, c2 = st.columns(2, vertical_alignment="center")
with c1:
    st.markdown("Chọn đường truyền")
with c2:
    iv_route = st.selectbox(
        label="label", 
        label_visibility="collapsed", 
        options=["Ngoại biên", "Trung ương"],
        key="iv_route"
    )

def nutrition_row(label, options, key_prefix):
    c1, c2 = st.columns(2)
    with c1:
        choice = st.selectbox(
            f"Chọn dịch {label.lower()}",
            options,
            format_func=lambda x: x["name"], 
            key=f"{key_prefix}_type"
        )
    with c2:
        vol = st.number_input(
            "Số ml",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key=f"{key_prefix}_ml"
        )
    return choice, vol

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

# Tốc độ truyền
c1, c2, c3 = st.columns([1.2, 2.5, 1], vertical_alignment="center")
with c1:
    st.markdown("**Tốc độ truyền**")
with c2:
    infusion_rate = st.number_input(label="Tốc độ truyền",label_visibility='collapsed', min_value=0.0, value=0.0, step=5.0, key="infusion_rate")
with c3:
    st.markdown("ml")

st.markdown("---")


# ================== CONTAINER ==================

st.markdown("### Phân tích nhu cầu dịch")

po_ml = st.session_state["po_ml"] * st.session_state["num_feeds"]
lipid_ml = st.session_state['lipid_ml']
# iv_ml = st.session_state["infusion_rate"] * 24
iv_ml = st.session_state["protein_ml"] + st.session_state["glucose_30_ml"] + st.session_state["glucose_10_ml"] + st.session_state["na_ml"] + st.session_state["k_ml"] + st.session_state["ca_ml"] + st.session_state["mg_ml"]
total_actual_ml = po_ml + iv_ml + lipid_ml + st.session_state['med_vol']

st.markdown("---")

c1, c2 = st.columns(2, vertical_alignment="center")
with c1: 
    st.markdown("Nhu cầu dịch theo Holliday Segar")
    st.markdown("Nhu cầu dịch tăng thêm")
    st.markdown("Tổng nhu cầu dịch lý thuyết")
with c2:
    st.markdown(f"{calc_fluid_need_holliday_segar()} ml")
    st.markdown(f"{extra_vol} ml")
    st.markdown(f"{calc_fluid_need_holliday_segar() + extra_vol} ml")

st.markdown("---")

c1, c2 = st.columns(2, vertical_alignment="center")
with c1: 
    st.markdown("Thể tích dịch đường miệng")
    st.markdown("Thể tích dịch đường IV")
    st.markdown("Thể tích lipid")
    st.markdown("Thể tích thuốc")
    st.markdown("Tổng thể tích dịch thực tế")
    st.markdown("Gấp bao nhiêu lần lý thuyết")
with c2:
    st.markdown(f"{po_ml} ml")
    st.markdown(f"{iv_ml} ml")
    st.markdown(f"{lipid_ml} ml")
    st.markdown(f"{st.session_state['med_vol']} ml")
    st.markdown(f"{total_actual_ml} ml")
    st.markdown(f"{round(total_actual_ml / (calc_fluid_need_holliday_segar() + extra_vol), 1)} lần")

st.markdown("---")


# ================== CONTAINER ==================

st.markdown("### Phân tích nhu cầu năng lượng")

po_kcal = round(st.session_state["po_sol"]["kcal_ml"] * st.session_state["po_ml"] * st.session_state["num_feeds"], 1)

protein_kcal = st.session_state["protein_type"]["con_per_ml"] * st.session_state["protein_ml"] * 4
lipid_kcal = st.session_state["lipid_type"]["con_per_ml"] * st.session_state["lipid_ml"] * 10
glucose_10_g = st.session_state["glucose_10_type"]["con_per_ml"] * st.session_state["glucose_10_ml"]
glucose_30_g = st.session_state["glucose_30_type"]["con_per_ml"] * st.session_state["glucose_30_ml"]
glucose_kcal = (glucose_10_g + glucose_30_g) * 3.4
iv_kcal = round(protein_kcal + lipid_kcal + glucose_kcal, 1)

total_kcal = po_kcal + iv_kcal

if customized_kcal == 0 or customized_kcal == None: 
    ree = round(calc_ree(), 1)
else: 
    ree = round((customized_kcal * st.session_state["weight"]), 1)

extra_kcal = ree * st.session_state["stress_index"]

c1, c2 = st.columns(2)
with c1: 
    st.markdown("Năng lượng dinh dưỡng đường miệng")
    st.markdown("Năng lượng dinh dưỡng đường IV")
    st.markdown("Tổng năng lượng thực tế")
    st.markdown("Năng lượng nghỉ (REE) lý thuyết")
    st.markdown("Năng lượng cộng thêm stress lý thuyết")
    st.markdown("So với mục tiêu")
    st.markdown("% Năng lượng từ đường (kì vọng 70%)")
    st.markdown("% Năng lượng từ đạm (kì vọng 70%)")
    st.markdown("% Năng lượng từ lipid (kì vọng 30%)")
with c2:
    st.markdown(f"{po_kcal} kcal")
    st.markdown(f"{iv_kcal} kcal")
    st.markdown(f"{total_kcal} kcal")
    st.markdown(f"{round(ree, 1)} kcal")
    st.markdown(f"{round(extra_kcal, 1)} kcal")
    st.markdown(f"{round(total_kcal / extra_kcal * 100, 1)}%" if extra_kcal != 0 else 'N/A')
    st.markdown(f"{round(glucose_kcal / iv_kcal * 100, 1)}%" if glucose_kcal != 0 and total_kcal != 0 else 'N/A')
    st.markdown(f"{round(protein_kcal / iv_kcal * 100, 1)}%" if protein_kcal != 0 and total_kcal != 0 else 'N/A')
    st.markdown(f"{round(lipid_kcal / total_kcal * 100, 1)}%" if lipid_kcal != 0 and total_kcal != 0 else 'N/A')



st.markdown("---")


# ================== CONTAINER ==================

st.markdown("### Phân tích nhu cầu các chất dinh dưỡng")

def calc_amount(type_key, ml_key):
    if type_key not in st.session_state or ml_key not in st.session_state:
        return None
    
    sol = st.session_state.get(type_key)
    ml = st.session_state.get(ml_key)

    if sol is None or ml is None:
        return None
    try:
        return round(sol["con_per_ml"] * ml, 1)
    except:
        return None

def calc_per_kg(amount, weight):
    if amount is None or weight is None:
        return None
    if weight == 0:
        return None
    try:
        return amount / weight
    except:
        return None

protein_amount = calc_amount("protein_type", "protein_ml")
lipid_amount   = calc_amount("lipid_type", "lipid_ml")
glucose_10_amount = calc_amount("glucose_10_type", "glucose_10_ml")
glucose_30_amount = calc_amount("glucose_30_type", "glucose_30_ml")
na_amount      = calc_amount("na_type", "na_ml")
k_amount       = calc_amount("k_type", "k_ml")
ca_amount      = calc_amount("ca_type", "ca_ml")
mg_amount      = calc_amount("mg_type", "mg_ml")
# phos_amount    = calc_amount("phos_type", "phos_ml")

protein_kg = calc_per_kg(protein_amount, weight)
lipid_kg   = calc_per_kg(lipid_amount, weight)
na_kg      = calc_per_kg(na_amount, weight)
k_kg       = calc_per_kg(k_amount, weight)
ca_kg      = calc_per_kg(ca_amount, weight)
mg_kg      = calc_per_kg(mg_amount, weight)
# phos_kg    = calc_per_kg(phos_amount, weight)

total_iv_vol = st.session_state["protein_ml"] + st.session_state["lipid_ml"] + st.session_state["glucose_10_ml"] + st.session_state["glucose_30_ml"] + st.session_state["na_ml"] + st.session_state["k_ml"] + st.session_state["ca_ml"] + st.session_state["mg_ml"]


def safe(x):
    if x is None:
        return None
    try:
        if x == 0:
            return 0
        return round(x, 1)
    except:
        return None

data = [
    [f"{safe(protein_amount)} g",  f"{safe(protein_kg)} g/kg",  "(1 - 4 g/kg/ngày)"],
    [f"{safe(lipid_amount)} g",    f"{safe(lipid_kg)} g/kg",    "(1 - 3 g/kg/ngày)"],
    [f"{safe(na_amount)} mEq",     f"{safe(na_kg)} mEq/kg",     "(2 - 4 mEq/kg/ngày)"],
    [f"{safe(k_amount)} mEq",      f"{safe(k_kg)} mEq/kg",      "(2 - 3 mEq/kg/ngày)"],
    [f"{safe(ca_amount)} mEq",     f"{safe(ca_kg)} mEq/kg",     "(0.5 - 2.5 mEq/kg/ngày)"],
    [f"{safe(mg_amount)} mEq",     f"{safe(mg_kg)} mEq/kg",     "(0.25 - 0.5 mEq/kg/ngày)"],
]

df = pd.DataFrame(
    data,
    columns=["Lượng", "Theo cân nặng", "Nhu cầu"], 
    index=["Protein", "Lipid", "Natri", "Kali", "Calci", "Magne"]
)

st.table(df)

st.markdown("---")

st.markdown("**Dinh dưỡng thành phần đường**")

if total_iv_vol != 0:
    st.markdown(f"Nồng độ đường: **{round((glucose_10_amount + glucose_30_amount) / total_iv_vol * 100, 1)}%**") 
else:
    st.markdown("Nồng độ đường: N/A")

st.markdown("""
- Nồng độ đường cho đường ngoại biên: < 12.5%
- Nồng độ đường cho đường trung tâm: < 25%
""")

gir = (glucose_10_amount + glucose_30_amount) * 1000 / st.session_state["weight"] / 1440

if infusion_rate != 0:
    st.markdown(f"Tốc độ đường: **{round(gir, 1)} mg/kg/phút**") 
else:
    st.markdown("Tốc độ đường: N/A")

st.markdown("""
- Tốc độ đường khởi đầu: 6 - 8 mg/kg/phút
- Tốc độ đường mục tiêu: 10 - 14 mg/kg/phút, tối đa 15 mg/kg/phút
""")

st.markdown("---")