import streamlit as st
import math

st.title("元素匹配器")
# 滑块实时获取分数
fire_score = st.slider("火属性分数", 0, 10, 5)
water_score = st.slider("水属性分数", 0, 10, 5)

# 用户坐标
user = [fire_score, water_score]
# 模板坐标
fire_type = [10, 4]
water_type = [4, 10]

if st.button("开始匹配"):
    # 计算距离
    d1 = math.sqrt((user[0]-fire_type[0])**2 + (user[1]-fire_type[1])**2)
    d2 = math.sqrt((user[0]-water_type[0])**2 + (user[1]-water_type[1])**2)
    if d1 < d2:
        st.success("匹配：烈焰型")
    else:
        st.success("匹配：潮汐型")