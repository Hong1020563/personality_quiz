# 导入Streamlit网页开发库
import streamlit as st

# 页面主标题
st.title("赛博炼金术士 · 元素人格测试仪")
# 副标题/说明文字
st.caption("基于你的元素选择，匹配专属炼金身份")

# 交互组件：获取用户输入与选择
name = st.text_input("你的代号是？")  # 文本输入框
choice = st.selectbox("遇到危机时，你更像哪一种元素？", ["火", "水", "风", "土"])  # 下拉选择框

# 点击按钮触发匹配逻辑
if st.button("开始最终匹配"):
    # 元素身份判断逻辑（核心逻辑，未修改）
    if choice == "火":
        result = "烈焰炼金术士"
    elif choice == "水":
        result = "潮汐观察者"
    elif choice == "风":
        result = "疾风游侠"
    else:
        result = "大地守卫者"
    
    st.divider()  # 分割线，优化界面层级
    # 醒目展示最终结果
    st.success(f"{name}，你的最终元素身份是：{result}")
    st.toast("匹配完成！")  # 弹窗轻提示