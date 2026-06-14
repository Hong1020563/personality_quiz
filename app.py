import streamlit as st

st.title("元素人格测试仪")
name = st.text_input("输入你的代号：")

# 初始化分数
fire_score = 0
water_score = 0

# 第一题
q1 = st.radio("1. 面对未知洞穴，你会？", ["直接进去看看", "先观察四周"])
# 第二题
q2 = st.selectbox("2. 行动偏好？", ["快速突进", "稳妥试探"])

if st.button("开始分析"):
    # 逐题加分
    if q1 == "直接进去看看":
        fire_score += 10
    else:
        water_score += 10

    if q2 == "快速突进":
        fire_score += 10
    else:
        water_score += 10

    # 判断最终结果
    if fire_score > water_score:
        res = "烈焰型"
    elif water_score > fire_score:
        res = "潮汐型"
    else:
        res = "平衡型"

    # 展示结果
    st.write(f"分数统计 → 火：{fire_score}  水：{water_score}")
    st.success(f"{name}，你的测试结果：{res}")