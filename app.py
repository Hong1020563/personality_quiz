import streamlit as st
import time

# 页面全局配置
st.set_page_config(
    page_title="赛博炼金术士 · 元素人格测试仪",
    page_icon="🔮",
    layout="centered"
)

# 初始化会话状态（控制逐题显示）
if "current_q" not in st.session_state:
    st.session_state.current_q = 1

# 初始化分数
if "score_fire" not in st.session_state:
    st.session_state.score_fire = 0
if "score_water" not in st.session_state:
    st.session_state.score_water = 0
if "score_wind" not in st.session_state:
    st.session_state.score_wind = 0
if "score_earth" not in st.session_state:
    st.session_state.score_earth = 0

# 头部标题与介绍
st.title("赛博炼金术士 · 元素人格测试仪")
st.caption("「当危机降临，你的本能会是什么？」逐题完成问卷，解锁专属炼金身份")
st.divider()

# 元素简介折叠面板
with st.expander("四大元素档案（点击查看）"):
    st.markdown("""
    - **火元素**：代表勇气、热情、行动力，天生的开拓者与领导者。
    - **水元素**：代表冷静、细腻、共情力，善于观察与思考。
    - **风元素**：代表自由、敏捷、创造力，适应力强、思维跳脱。
    - **土元素**：代表稳重、坚守、责任感，团队中可靠的守护者。
    """)
st.divider()

# 基础信息
name = st.text_input("你的代号是？", placeholder="比如：炼金学徒小A")
st.divider()

st.subheader("炼金试炼问卷")
q_num = st.session_state.current_q

# 题目1
if q_num == 1:
    ans1 = st.radio("问题1：遇到突发危机，你第一反应是？",
                   ["主动出手，直面挑战", "冷静观察，伺机行动",
                    "灵活周旋，快速脱身", "坚守原地，守护同伴"])
    if st.button("下一题"):
        if ans1 == "主动出手，直面挑战":
            st.session_state.score_fire += 1
        elif ans1 == "冷静观察，伺机行动":
            st.session_state.score_water += 1
        elif ans1 == "灵活周旋，快速脱身":
            st.session_state.score_wind += 1
        else:
            st.session_state.score_earth += 1
        st.session_state.current_q = 2
        st.rerun()

# 题目2
elif q_num == 2:
    ans2 = st.radio("问题2：日常处事风格更偏向？",
                   ["热情直率，敢想敢做", "心思细腻，共情力强",
                    "随性自由，不喜束缚", "稳重踏实，信守承诺"])
    if st.button("下一题"):
        if ans2 == "热情直率，敢想敢做":
            st.session_state.score_fire += 1
        elif ans2 == "心思细腻，共情力强":
            st.session_state.score_water += 1
        elif ans2 == "随性自由，不喜束缚":
            st.session_state.score_wind += 1
        else:
            st.session_state.score_earth += 1
        st.session_state.current_q = 3
        st.rerun()

# 题目3
elif q_num == 3:
    ans3 = st.radio("问题3：团队中你更愿意扮演？",
                   ["冲锋的领导者", "幕后的观察者",
                    "活跃的协调者", "可靠的支撑者"])
    if st.button("下一题"):
        if ans3 == "冲锋的领导者":
            st.session_state.score_fire += 1
        elif ans3 == "幕后的观察者":
            st.session_state.score_water += 1
        elif ans3 == "活跃的协调者":
            st.session_state.score_wind += 1
        else:
            st.session_state.score_earth += 1
        st.session_state.current_q = 4
        st.rerun()

# 题目4
elif q_num == 4:
    ans4 = st.radio("问题4：更喜欢的环境氛围？",
                   ["热闹热烈", "安静温润",
                    "开阔自由", "安稳踏实"])
    if st.button("下一题"):
        if ans4 == "热闹热烈":
            st.session_state.score_fire += 1
        elif ans4 == "安静温润":
            st.session_state.score_water += 1
        elif ans4 == "开阔自由":
            st.session_state.score_wind += 1
        else:
            st.session_state.score_earth += 1
        st.session_state.current_q = 5
        st.rerun()

# 题目5 滑块
elif q_num == 5:
    ans5 = st.slider("问题5：你的耐心程度偏向哪一端？", 1, 4, 2,
                    help="1=缺乏耐心、行动优先 | 4=极具耐心、沉稳优先")
    st.caption("1：急躁好动 | 2：中等耐心 | 3：比较耐心 | 4：极度沉稳")
    if st.button("下一题"):
        if ans5 == 1:
            st.session_state.score_fire += 1
        elif ans5 == 2:
            st.session_state.score_wind += 1
        elif ans5 == 3:
            st.session_state.score_water += 1
        else:
            st.session_state.score_earth += 1
        st.session_state.current_q = 6
        st.rerun()

# 题目6 多选
elif q_num == 6:
    ans6 = st.multiselect("问题6：你偏爱哪些特质？（可多选）",
                          ["勇敢果敢", "温柔内敛", "洒脱自在", "踏实可靠"])
    if st.button("查看结果"):
        if "勇敢果敢" in ans6:
            st.session_state.score_fire += 1
        if "温柔内敛" in ans6:
            st.session_state.score_water += 1
        if "洒脱自在" in ans6:
            st.session_state.score_wind += 1
        if "踏实可靠" in ans6:
            st.session_state.score_earth += 1
        st.session_state.current_q = 7
        st.rerun()

# 最终结果页
elif q_num == 7:
    st.divider()
    st.subheader("你的元素得分明细")
    st.write(f"火元素得分：{st.session_state.score_fire} 分")
    st.write(f"水元素得分：{st.session_state.score_water} 分")
    st.write(f"风元素得分：{st.session_state.score_wind} 分")
    st.write(f"土元素得分：{st.session_state.score_earth} 分")

    st.divider()
    # 判定最终元素
    all_score = {
        "火": st.session_state.score_fire,
        "水": st.session_state.score_water,
        "风": st.session_state.score_wind,
        "土": st.session_state.score_earth
    }
    final_choice = max(all_score, key=all_score.get)

    # 元素资料
    element_info = {
        "火": {
            "name": "烈焰炼金术士",
            "desc": "你像火焰一样热烈而果敢，危机面前从不退缩，是团队里最可靠的破局者。",
            "color": "#FF4B4B"
        },
        "水": {
            "name": "潮汐观察者",
            "desc": "你如水般温柔而坚韧，总能在混乱中保持冷静，用细腻的观察找到出路。",
            "color": "#4B8BFF"
        },
        "风": {
            "name": "疾风游侠",
            "desc": "你如风般自由而敏捷，反应快、适应力强，总能用意想不到的方式化解危机。",
            "color": "#4BFFA5"
        },
        "土": {
            "name": "大地守卫者",
            "desc": "你像大地一样沉稳而可靠，是团队的基石，总能在关键时刻撑起一片天。",
            "color": "#FFD700"
        }
    }

    res_name = element_info[final_choice]["name"]
    res_desc = element_info[final_choice]["desc"]
    res_color = element_info[final_choice]["color"]

    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem; border-radius: 12px; background-color: {res_color}20;">
        <h2 style="color: {res_color};">{res_name}</h2>
        <p style="font-size: 1.1rem;">{name}，你的本命元素为【{final_choice}】</p >
        <p style="font-style: italic; color: #555; font-size: 1rem;">{res_desc}</p >
    </div>
    """, unsafe_allow_html=True)

    st.toast("匹配完成！炼金身份已激活")

    # 重新测试按钮
    if st.button("重新测试"):
        # 清空所有状态，回到第一题
        st.session_state.current_q = 1
        st.session_state.score_fire = 0
        st.session_state.score_water = 0
        st.session_state.score_wind = 0
        st.session_state.score_earth = 0
        st.rerun()