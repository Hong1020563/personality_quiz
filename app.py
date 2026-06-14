import streamlit as st
import math

st.title("元素人格自动匹配器")

fire_score = st.slider("火属性（行动力）", 0, 10, 5)
water_score = st.slider("水属性（冷静度）", 0, 10, 5)
user = [fire_score, water_score]

# 新增：惊雷型模板
profiles = {
    "烈焰型": [10, 4],
    "潮汐型": [4, 10],
    "疾风型": [7, 7],
    "惊雷型": [9, 6]   # 新增模板
}

min_dist = 999999.0
best_match = ""

if st.button("自动匹配"):
    for name, coords in profiles.items():
        dist = math.sqrt((user[0] - coords[0])**2 + (user[1] - coords[1])**2)
        st.write(f"{name} 距离：{dist:.2f}")
        if dist < min_dist:
            min_dist = dist
            best_match = name

    st.divider()
    st.success(f"最终匹配结果：{best_match}")
    st.balloons()