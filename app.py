import streamlit as st
import math

st.title("元素人格自动匹配器（均衡判断版）")

fire_score = st.slider("火属性（行动力）", 0, 10, 5)
water_score = st.slider("水属性（冷静度）", 0, 10, 5)
user = [fire_score, water_score]

profiles = {
    "烈焰型": [10, 4],
    "潮汐型": [4, 10],
    "疾风型": [7, 7]
}

min_dist = 999999.0
best_match = ""
# 新增：记录有多少个模板同为最小距离
equal_count = 0

if st.button("自动匹配"):
    for name, coords in profiles.items():
        dist = math.sqrt((user[0] - coords[0])**2 + (user[1] - coords[1])**2)
        st.write(f"{name} 距离：{dist:.2f}")

        # 情况1：找到更小值，重置计数
        if dist < min_dist:
            min_dist = dist
            best_match = name
            equal_count = 1
        # 情况2：距离和当前最小值相等
        elif dist == min_dist:
            equal_count += 1

    st.divider()
    st.write(f"最小匹配距离：{min_dist:.2f}")
    # 判断是否多个模板距离相同
    if equal_count > 1:
        st.info("多个模板匹配度一致，属性均衡！")
    else:
        st.success(f"最终匹配结果：{best_match}")
    st.balloons()