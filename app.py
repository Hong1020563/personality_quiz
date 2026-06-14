import streamlit as st
import math

st.title("元素人格自动匹配器")

# 1. 获取用户坐标（二维分数）
fire_score = st.slider("火属性（行动力）", 0, 10, 5)
water_score = st.slider("水属性（冷静度）", 0, 10, 5)
user = [fire_score, water_score]

# 2. 定义所有模板（字典：名称-坐标）
profiles = {
    "烈焰型": [10, 4],
    "潮汐型": [4, 10],
    "疾风型": [7, 7]
}

# 3. 擂台变量初始化（必须写在循环外）
min_dist = 999999.0
best_match = ""

if st.button("自动匹配"):
    # 4. 循环遍历所有模板
    for name, coords in profiles.items():
        # 计算两点距离
        dist = math.sqrt(
            (user[0] - coords[0]) ** 2 +
            (user[1] - coords[1]) ** 2
        )
        # 展示每一个模板的距离
        st.write(f"{name} 距离：{dist:.2f}")
        
        # 5. 打擂台：更新最小值和最优匹配
        if dist < min_dist:
            min_dist = dist
            best_match = name

    # 6. 输出最终结果
    st.divider()
    st.success(f"最终匹配结果：{best_match}")
    st.balloons()