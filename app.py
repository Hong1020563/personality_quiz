import streamlit as st
import pandas as pd
import time

# ===================== 全局配置（隐藏侧边栏） =====================
st.set_page_config(
    page_title="赛博炼金术士 · 元素人格测试仪",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===================== 架构优化：统一全局文案 & 题库 & 彩蛋文案 =====================
# 元素档案文案
ELEMENT_INTRO = """
- **火元素**：代表勇气、热情、行动力，天生的开拓者与领导者。
- **水元素**：代表冷静、细腻、共情力，善于观察与思考。
- **风元素**：代表自由、敏捷、创造力，适应力强、思维跳脱。
- **土元素**：代表稳重、坚守、责任感，团队中可靠的守护者。
"""

# 元素对应资料：名称、描述、配色、专属彩蛋文案（每个元素独立彩蛋）
ELEMENT_INFO = {
    "火": {
        "name": "烈焰炼金术士",
        "desc": "你像火焰一样热烈而果敢，危机面前从不退缩，是团队里最可靠的破局者。",
        "color": "#FF4B4B",
        "egg": [
            "🔥 心火不灭，勇气永远是你最强的炼金符文！",
            "🔥 热烈是你的底色，走到哪里都能点燃身边人的热情。",
            "🔥 不惧挑战、一往无前，这就是属于火焰的荣耀。"
        ]
    },
    "水": {
        "name": "潮汐观察者",
        "desc": "你如水般温柔而坚韧，总能在混乱中保持冷静，用细腻的观察找到出路。",
        "color": "#4B8BFF",
        "egg": [
            "💧 上善若水，你的温柔与智慧总能化解一切纷争。",
            "💧 静水流深，细腻的心思让你看见别人忽略的细节。",
            "💧 包容且坚韧，如水一般，无坚不摧。"
        ]
    },
    "风": {
        "name": "疾风游侠",
        "desc": "你如风般自由而敏捷，反应快、适应力强，总能用意想不到的方式化解危机。",
        "color": "#4BFFA5",
        "egg": [
            "🌪️ 心随风动，自由洒脱是你刻在骨子里的特质。",
            "🌪️ 来去自如、思维灵动，没有人能困住追风的人。",
            "🌪️ 轻盈又敏捷，你永远拥有探索新世界的勇气。"
        ]
    },
    "土": {
        "name": "大地守卫者",
        "desc": "你像大地一样沉稳而可靠，是团队的基石，总能在关键时刻撑起一片天。",
        "color": "#FFD700",
        "egg": [
            "🌍 大地无言，却承载万物，可靠就是你的代名词。",
            "🌍 沉稳踏实、坚守本心，身边的人都愿意信任你。",
            "🌍 厚积薄发，你的稳重终将成为最强大的力量。"
        ]
    }
}

# 题库：统一存放所有题目、选项、提示（新增题目直接在这里追加）
QUESTION_LIST = [
    {
        "title": "问题1：遇到突发危机，你第一反应是？",
        "options": ["主动出手，直面挑战", "冷静观察，伺机行动", "灵活周旋，快速脱身", "坚守原地，守护同伴"],
        "tip": "小提示：这道题测试你面对危机的本能反应",
        "type": "radio"
    },
    {
        "title": "问题2：日常处事风格更偏向？",
        "options": ["热情直率，敢想敢做", "心思细腻，共情力强", "随性自由，不喜束缚", "稳重踏实，信守承诺"],
        "tip": "小提示：这道题测试你日常的性格与行事风格",
        "type": "radio"
    },
    {
        "title": "问题3：团队中你更愿意扮演？",
        "options": ["冲锋的领导者", "幕后的观察者", "活跃的协调者", "可靠的支撑者"],
        "tip": "小提示：这道题测试你在团队里的角色定位",
        "type": "radio"
    },
    {
        "title": "问题4：更喜欢的环境氛围？",
        "options": ["热闹热烈", "安静温润", "开阔自由", "安稳踏实"],
        "tip": "环境偏好也能反映你的内在性格特质",
        "type": "radio"
    },
    {
        "title": "问题5：你的耐心程度偏向哪一端？",
        "options": "",
        "tip": "小提示：耐心程度对应不同元素的性格特征",
        "type": "slider"
    },
    {
        "title": "问题6：你偏爱哪些特质？（可多选）",
        "options": ["勇敢果敢", "温柔内敛", "洒脱自在", "踏实可靠"],
        "tip": "小提示：可以多选，选择你最认可的个人特质",
        "type": "multiselect"
    }
]
TOTAL_QUESTION = 6

# ===================== 架构优化：封装计分函数 =====================
def calc_radio_score(answer):
    """单选题目计分"""
    if answer in ("主动出手，直面挑战", "热情直率，敢想敢做", "冲锋的领导者", "热闹热烈"):
        st.session_state.score_fire += 1
    elif answer in ("冷静观察，伺机行动", "心思细腻，共情力强", "幕后的观察者", "安静温润"):
        st.session_state.score_water += 1
    elif answer in ("灵活周旋，快速脱身", "随性自由，不喜束缚", "活跃的协调者", "开阔自由"):
        st.session_state.score_wind += 1
    else:
        st.session_state.score_earth += 1

def calc_slider_score(answer):
    """滑块题目计分"""
    if answer == 1:
        st.session_state.score_fire += 1
    elif answer == 2:
        st.session_state.score_wind += 1
    elif answer == 3:
        st.session_state.score_water += 1
    else:
        st.session_state.score_earth += 1

def calc_multiselect_score(answer_list):
    """多选题目计分"""
    if "勇敢果敢" in answer_list:
        st.session_state.score_fire += 1
    if "温柔内敛" in answer_list:
        st.session_state.score_water += 1
    if "洒脱自在" in answer_list:
        st.session_state.score_wind += 1
    if "踏实可靠" in answer_list:
        st.session_state.score_earth += 1

# ===================== 初始化会话状态（新增计时相关） =====================
if "current_q" not in st.session_state:
    st.session_state.current_q = 1
if "score_fire" not in st.session_state:
    st.session_state.score_fire = 0
if "score_water" not in st.session_state:
    st.session_state.score_water = 0
if "score_wind" not in st.session_state:
    st.session_state.score_wind = 0
if "score_earth" not in st.session_state:
    st.session_state.score_earth = 0
# 答题计时：记录开始时间
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ===================== 页面头部 =====================
st.title("赛博炼金术士 · 元素人格测试仪")
st.caption("「当危机降临，你的本能会是什么？」逐题完成问卷，解锁专属炼金身份")
st.divider()

# 元素档案折叠面板
with st.expander("四大元素档案（点击查看）"):
    st.markdown(ELEMENT_INTRO)
st.divider()

# 代号输入 + 非空校验
name = st.text_input("你的代号是？", placeholder="比如：炼金学徒小A")
st.divider()
if not name:
    st.info("请先填写你的代号，再开始答题")
    st.stop()

# 答题区域
st.subheader("炼金试炼问卷")
q_num = st.session_state.current_q

# 进度条
if q_num <= TOTAL_QUESTION:
    progress = q_num / TOTAL_QUESTION
    st.progress(progress, text=f"答题进度：第{q_num}题 / 共{TOTAL_QUESTION}题")
st.divider()

# ===================== 逐题渲染逻辑 =====================
# 第1题
if q_num == 1:
    q = QUESTION_LIST[0]
    ans = st.radio(q["title"], q["options"], index=None)
    st.info(q["tip"])

    if st.button("下一题"):
        if not ans:
            st.warning("请先选择一个答案再继续！")
        else:
            calc_radio_score(ans)
            st.session_state.current_q = 2
            st.toast("已完成本题，进入下一题")
            st.rerun()

# 第2题
elif q_num == 2:
    q = QUESTION_LIST[1]
    ans = st.radio(q["title"], q["options"], index=None)
    st.info(q["tip"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 1
            st.rerun()
    with col2:
        if st.button("下一题"):
            if not ans:
                st.warning("请先选择一个答案再继续！")
            else:
                calc_radio_score(ans)
                st.session_state.current_q = 3
                st.toast("已完成本题，进入下一题")
                st.rerun()

# 第3题
elif q_num == 3:
    q = QUESTION_LIST[2]
    ans = st.radio(q["title"], q["options"], index=None)
    st.info(q["tip"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 2
            st.rerun()
    with col2:
        if st.button("下一题"):
            if not ans:
                st.warning("请先选择一个答案再继续！")
            else:
                calc_radio_score(ans)
                st.session_state.current_q = 4
                st.toast("已完成本题，进入下一题")
                st.rerun()

# 第4题
elif q_num == 4:
    q = QUESTION_LIST[3]
    ans = st.radio(q["title"], q["options"], index=None)
    st.info(q["tip"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 3
            st.rerun()
    with col2:
        if st.button("下一题"):
            if not ans:
                st.warning("请先选择一个答案再继续！")
            else:
                calc_radio_score(ans)
                st.session_state.current_q = 5
                st.toast("已完成本题，进入下一题")
                st.rerun()

# 第5题 滑块
elif q_num == 5:
    q = QUESTION_LIST[4]
    ans = st.slider(q["title"], 1, 4, 2, help="1=缺乏耐心、行动优先 | 4=极具耐心、沉稳优先")
    st.caption("1：急躁好动 | 2：中等耐心 | 3：比较耐心 | 4：极度沉稳")
    st.info(q["tip"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 4
            st.rerun()
    with col2:
        if st.button("下一题"):
            calc_slider_score(ans)
            st.session_state.current_q = 6
            st.toast("已完成本题，进入下一题")
            st.rerun()

# 第6题 多选
elif q_num == 6:
    q = QUESTION_LIST[5]
    ans = st.multiselect(q["title"], q["options"])
    st.info(q["tip"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 5
            st.rerun()
    with col2:
        if st.button("查看结果"):
            if not ans:
                st.warning("请至少选择一项特质再继续！")
            else:
                calc_multiselect_score(ans)
                st.session_state.current_q = 7
                st.toast("所有题目作答完毕，正在生成结果")
                st.rerun()

# ===================== 结果页面（计时+彩蛋+动效+背景音乐） =====================
elif q_num == 7:
    # 1. 计算答题用时
    end_time = time.time()
    use_time = round(end_time - st.session_state.start_time, 1)
    st.info(f"⏱️ 本次答题总用时：{use_time} 秒")
    st.divider()

    # 2. 分数展示 + 柱状图
    st.subheader("你的元素得分明细")
    st.write(f"火元素得分：{st.session_state.score_fire} 分")
    st.write(f"水元素得分：{st.session_state.score_water} 分")
    st.write(f"风元素得分：{st.session_state.score_wind} 分")
    st.write(f"土元素得分：{st.session_state.score_earth} 分")

    st.subheader("分数可视化图表")
    score_data = {
        "元素": ["火", "水", "风", "土"],
        "分数": [
            st.session_state.score_fire,
            st.session_state.score_water,
            st.session_state.score_wind,
            st.session_state.score_earth
        ]
    }
    df = pd.DataFrame(score_data)
    st.bar_chart(df, x="元素", y="分数", use_container_width=True)
    st.divider()

    # 3. 平局判断
    all_score = {
        "火": st.session_state.score_fire,
        "水": st.session_state.score_water,
        "风": st.session_state.score_wind,
        "土": st.session_state.score_earth
    }
    max_score = max(all_score.values())
    tie_list = [k for k, v in all_score.items() if v == max_score]

    if len(tie_list) > 1:
        st.info(f"出现平局！你同时契合：{'、'.join(tie_list)} 多种元素特质")
        final_choice = tie_list[0]
    else:
        final_choice = max(all_score, key=all_score.get)

    # 4. 获取元素信息 + 随机抽取专属彩蛋文案
    res_name = ELEMENT_INFO[final_choice]["name"]
    res_desc = ELEMENT_INFO[final_choice]["desc"]
    res_color = ELEMENT_INFO[final_choice]["color"]
    egg_list = ELEMENT_INFO[final_choice]["egg"]
    # 随机选一条彩蛋，每次结果文案不一样
    import random
    egg_text = random.choice(egg_list)

    # 5. 结果卡片 + CSS简单动效（渐入动画）
    st.markdown(f"""
    <style>
    @keyframes fadeIn {{
        from {{opacity: 0; transform: scale(0.95);}}
        to {{opacity: 1; transform: scale(1);}}
    }}
    .result-card {{
        animation: fadeIn 1s ease-in-out;
        text-align: center; 
        padding: 1.5rem; 
        border-radius: 12px; 
        background-color: {res_color}20;
    }}
    </style>
    <div class="result-card">
        <h2 style="color: {res_color};">{res_name}</h2>
        <p style="font-size: 1.1rem;">{name}，你的本命元素为【{final_choice}】</p>
        <p style="font-style: italic; color: #555; font-size: 1rem;">{res_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # 6. 展示元素专属彩蛋文案
    st.success(f"✨ 专属寄语：{egg_text}")
    st.toast("匹配完成！炼金身份已激活")
    st.divider()


    # 7. 分享文案
    share_text = f"我完成了元素人格测试！代号：{name}，本命元素：{final_choice}，身份：{res_name}，答题用时：{use_time}秒"
    st.text_area("一键复制分享", value=share_text, height=80)
    st.divider()

    # 8. 重新测试（重置计时+分数+题号）
    if st.button("重新测试"):
        st.session_state.current_q = 1
        st.session_state.score_fire = 0
        st.session_state.score_water = 0
        st.session_state.score_wind = 0
        st.session_state.score_earth = 0
        st.session_state.start_time = time.time()  # 重置计时
        st.rerun()