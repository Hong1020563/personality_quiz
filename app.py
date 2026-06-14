import streamlit as st

# 页面标题与说明
st.title("赛博炼金术士：元素人格探测器")
st.caption("回答问题，匹配专属元素属性")

# 1. 收集用户信息
name = st.text_input("请输入你的代号：")
ans1 = st.radio("1. 发现发光的门，你会？", ["立刻推开", "先观察四周", "找人一起"])
ans2 = st.selectbox("2. 偏好哪种施法媒介？", ["法杖", "水晶球", "符文卷轴", "空手"])

# 2. 点击按钮触发结果
if st.button("开始匹配"):
    st.divider()  # 分割线
    st.success(f"{name}，你的元素特质已匹配完成！")
    st.balloons()