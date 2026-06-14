import streamlit as st
import math

st.title("元素坐标匹配器（三模板版）")

# 滑块获取用户分数：行动力、冷静度
fire_score = st.slider("火属性（行动力）", 0, 10, 5)
water_score = st.slider("水属性（冷静度）", 0, 10, 5)

# 用户坐标
user = [fire_score, water_score]

# 预设三大模板
fire_type = [10, 4]    # 烈焰型
water_type = [4, 10]   # 潮汐型
wind_type = [7, 7]     # 疾风型（新增）

if st.button("开始匹配"):
    # 分别计算到三个模板的距离
    d_fire = math.sqrt((user[0] - fire_type[0]) ** 2 + (user[1] - fire_type[1]) ** 2)
    d_water = math.sqrt((user[0] - water_type[0]) ** 2 + (user[1] - water_type[1]) ** 2)
    d_wind = math.sqrt((user[0] - wind_type[0]) ** 2 + (user[1] - wind_type[1]) ** 2)

    # 展示所有距离
    st.write(f"距离烈焰型：{d_fire:.2f}")
    st.write(f"距离潮汐型：{d_water:.2f}")
    st.write(f"距离疾风型：{d_wind:.2f}")

    # 判断最小距离，匹配对应类型
    min_dist = min(d_fire, d_water, d_wind)
    if min_dist == d_fire:
        st.success("匹配结果：你更接近【烈焰型】")
    elif min_dist == d_water:
        st.success("匹配结果：你更接近【潮汐型】")
    else:
        st.success("匹配结果：你更接近【疾风型】")
    
    st.balloons()