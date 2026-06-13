import streamlit as st

# 网页标题、副标题
st.title("元素人格探测器")
st.caption("终端版小程序，第一次进化成网页形态")

# 输入框、选择框、按钮
name = st.text_input("输入你的代号")
choice = st.selectbox("选择元素", ["火","水","风","土"])
if st.button("开始探测"):
    st.success(f"{name}，你与{choice}元素产生了强烈共鸣。")