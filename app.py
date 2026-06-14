import streamlit as st

# 数据层：统一管理所有内容（不写死在组件里）
profiles = {
    "火": {"title":"烈焰炼金术士", "desc":"行动迅速，爆发力强"},
    "水": {"title":"潮汐观察者", "desc":"心思细腻，适应力好"},
    "风": {"title":"疾风游侠", "desc":"思维活跃，行事灵活"},
    "土": {"title":"大地守卫者", "desc":"沉稳可靠，抗压能力强"}
}

# 页面交互层
st.title("元素人格探测器")
name = st.text_input("请输入你的代号：")
# 提取字典的键作为下拉选项
element = st.selectbox("选择你的元素", list(profiles.keys()))

# 点击按钮展示查询结果
if st.button("开始匹配"):
    st.success(f"{name}，你的专属身份：{profiles[element]['title']}")
    st.write("性格描述：", profiles[element]["desc"])