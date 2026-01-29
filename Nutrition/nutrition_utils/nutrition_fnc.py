import streamlit as st

# công thức tính nhu cầu dịch
def calc_fluid_need_holliday_segar():
    if st.session_state["weight"] <= 0:
        return 0
    if st.session_state["weight"] <= 10:
        return st.session_state["weight"] * 100
    elif st.session_state["weight"] <= 20:
        return 1000 + (st.session_state["weight"] - 10) * 50
    else:
        return 1500 + (st.session_state["weight"] - 20) * 20
    
# công thức tính REE
def calc_ree(): 
    sex = st.session_state["sex"]
    age = st.session_state["age"]
    weight = st.session_state["weight"]
    height = st.session_state["height"]

    if sex not in ["Nữ", "Nam"]:
        raise ValueError("sex must be 'Nam' or 'Nữ'")
    if age < 0:
        return 0
    if sex == "Nam":
        if age < 3:
            ree = (0.167 * weight) + (15.174 * height) - 617.6
        elif age < 10:
            ree = (19.59 * weight) + (1.303 * height) + 414.9
        else:  # 10–18
            ree = (16.25 * weight) + (1.372 * height) + 515.5
    else:
        if age < 3:
            ree = (16.252 * weight) + (10.232 * height) - 413.5
        elif age < 10:
            ree = (16.969 * weight) + (1.618 * height) + 371.2
        else:  # 10–18
            ree = (8.365 * weight) + (4.65 * height) + 200
    return max(0, ree) 

# tính ml glucose 10% và 30%
def solve_glucose_mix_safe(glucose_vol: float, glucose_g: float):
    if glucose_vol <= 0:
        return None, None
    
    # if not (0.1 * glucose_vol <= glucose_g <= 0.3 * glucose_vol):
    #     raise ValueError("Giá trị glucose không thể pha từ G10% và G30%")

    x = 5 * glucose_g - 0.5 * glucose_vol
    y = glucose_vol - x

    return x, y

# hiển thị dòng dữ liệu với label và value 
def display_row(label, value):
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        c1_label = st.markdown(label)
    with c2:
        c2_label = st.markdown(value)
    return c1_label, c2_label

# tính só ml glucose 10% và 30%
def calc_glucose_solution(
    V_bag_total: float,     # tổng thể tích chai dịch (ml)
    V_glucose: float,       # thể tích dành để bơm glucose (ml)
    G_target: float,        # gram glucose mục tiêu
    iv_route: str,          # "Ngoại biên" | "Trung ương"
):
    """
    return:
        g30_ml, g10_ml, G_delivered
    """

    if V_bag_total <= 0 or V_glucose <= 0:
        return 0.0, 0.0, 0.0

    # 1. Giới hạn nồng độ theo đường truyền (tính trên TOÀN CHAI)
    if iv_route == "Ngoại biên":
        max_conc = 0.125
    else:
        max_conc = 0.25

    G_max_by_conc = V_bag_total * max_conc

    # 2. Giới hạn bởi thể tích glucose có thể bơm
    G_max_by_volume = 0.3 * V_glucose

    # 3. Lượng glucose thực sự có thể cho
    G_effective = min(G_target, G_max_by_conc, G_max_by_volume)

    if G_effective <= 0:
        return 0.0, 0.0, 0.0

    V = V_glucose
    G = G_effective

    # 4. Quyết định chiến lược pha

    # Chỉ G10
    if G <= 0.1 * V:
        g10_ml = V
        g30_ml = 0.0
        G_delivered = 0.1 * V

    # Chỉ G30
    elif G >= 0.3 * V:
        g30_ml = V
        g10_ml = 0.0
        G_delivered = 0.3 * V

    # Phối hợp
    else:
        # x + y = V
        # 0.3x + 0.1y = G
        x = 5 * G - 0.5 * V   # ml G30
        y = V - x             # ml G10

        # bảo vệ số học
        x = max(0.0, min(V, x))
        y = max(0.0, min(V, y))

        g30_ml = x
        g10_ml = y
        G_delivered = 0.3 * g30_ml + 0.1 * g10_ml

    return g30_ml, g10_ml, G_delivered
