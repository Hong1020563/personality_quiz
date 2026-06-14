import streamlit as st
import math

st.title("元素坐标匹配器（三维维度版）")

# 三个维度滑块：行动力、冷静度、冒险度
fire_score = st.slider("行动力", 0, 10, 5)
water_score = st.slider("冷静度", 0, 10, 5)
risk_score = st.slider("冒险度", 0, 10, 5)

# 三维用户坐标 [x, y, z]
user = [fire_score, water_score, risk_score]

# 三维模板坐标
fire_type = [10, 4, 9]
water_type = [4, 10, 3]
wind_type = [7, 7, 6]

if st.button("开始匹配"):
    # 三维距离计算
    d_fire = math.sqrt(
        (user[0] - fire_type[0])**2 +
        (user[1] - fire_type[1])**2 +
        (user[2] - fire_type[2])**2
    )
    d_water = math.sqrt(
        (user[0] - water_type[0])**2 +
        (user[1] - water_type[1])**2 +
        (user[2] - water_type[2])**2
    )
    d_wind = math.sqrt(
        (user[0] - wind_type[0])**2 +
        (user[1] - wind_type[1])**2 +
        (user[2] - wind_type[2])**2
    )

    # 输出距离
    st.write(f"距离烈焰型：{d_fire:.2f}")
    st.write(f"距离潮汐型：{d_water:.2f}")
    st.write(f"距离疾风型：{d_wind:.2f}")

    # 匹配判断
    min_dist = min(d_fire, d_water, d_wind)
    if min_dist == d_fire:
        st.success("匹配结果：你更接近【烈焰型】")
    elif min_dist == d_water:
        st.success("匹配结果：你更接近【潮汐型】")
    else:
        st.success("匹配结果：你更接近【疾风型】")

    st.balloons()