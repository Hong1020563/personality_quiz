import streamlit as st
import math

st.title("元素坐标匹配器")

# 用滑块获取用户两组分数（行动力、冷静度）
fire_score = st.slider("火属性（行动力）", 0, 10, 5)
water_score = st.slider("水属性（冷静度）", 0, 10, 5)

# 用户坐标 + 预设模板坐标
user = [fire_score, water_score]
fire_type = [10, 4]
water_type = [4, 10]

if st.button("开始匹配"):
    # 计算距离
    d1 = math.sqrt((user[0] - fire_type[0])**2 + (user[1] - fire_type[1])**2)
    d2 = math.sqrt((user[0] - water_type[0])**2 + (user[1] - water_type[1])**2)
    
    st.write(f"距离烈焰模板：{d1:.2f}")
    st.write(f"距离潮汐模板：{d2:.2f}")
    
    # 判定结果
    if d1 < d2:
        st.success("匹配结果：烈焰型")
        st.balloons()
    else:
        st.success("匹配结果：潮汐型")
        st.balloons()