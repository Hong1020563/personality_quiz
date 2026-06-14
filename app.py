import streamlit as st
import pandas as pd
import random

# ===================== 全局配置 =====================
PAGE_TITLE = "赛博炼金术士 · 元素人格测试仪"
PAGE_ICON = "🔮"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===================== 全局常量 & 文案 & 题库 & 元素配色（莫兰迪柔和版） =====================
# 四大元素主色调（低饱和度，更耐看）
ELEMENT_THEME_COLOR = {
    "火": "#E67E7E",    # 柔和暖红
    "水": "#7EA8E6",    # 清透浅蓝
    "风": "#7EE6B8",    # 清新薄荷绿
    "土": "#E6C87E"     # 暖调浅黄
}

# 元素档案文案
ELEMENT_INTRO = """
- **火元素**：代表勇气、热情、行动力，天生的开拓者与领导者。
- **水元素**：代表冷静、细腻、共情力，善于观察与思考。
- **风元素**：代表自由、敏捷、创造力，适应力强、思维跳脱。
- **土元素**：代表稳重、坚守、责任感，团队中可靠的守护者。
"""

# 元素对应资料
ELEMENT_INFO = {
    "火": {
        "name": "烈焰炼金术士",
        "desc": "你像火焰一样热烈而果敢，危机面前从不退缩，是团队里最可靠的破局者。",
        "color": "#E67E7E",
        "egg": [
            "🔥 心火不灭，勇气永远是你最强的炼金符文！",
            "🔥 热烈是你的底色，走到哪里都能点燃身边人的热情。",
            "🔥 不惧挑战、一往无前，这就是属于火焰的荣耀。"
        ]
    },
    "水": {
        "name": "潮汐观察者",
        "desc": "你如水般温柔而坚韧，总能在混乱中保持冷静，用细腻的观察找到出路。",
        "color": "#7EA8E6",
        "egg": [
            "💧 上善若水，你的温柔与智慧总能化解一切纷争。",
            "💧 静水流深，细腻的心思让你看见别人忽略的细节。",
            "💧 包容且坚韧，如水一般，无坚不摧。"
        ]
    },
    "风": {
        "name": "疾风游侠",
        "desc": "你如风般自由而敏捷，反应快、适应力强，总能用意想不到的方式化解危机。",
        "color": "#7EE6B8",
        "egg": [
            "🌪️ 心随风动，自由洒脱是你刻在骨子里的特质。",
            "🌪️ 来去自如、思维灵动，没有人能困住追风的人。",
            "🌪️ 轻盈又敏捷，你永远拥有探索新世界的勇气。"
        ]
    },
    "土": {
        "name": "大地守卫者",
        "desc": "你像大地一样沉稳而可靠，是团队的基石，总能在关键时刻撑起一片天。",
        "color": "#E6C87E",
        "egg": [
            "🌍 大地无言，却承载万物，可靠就是你的代名词。",
            "🌍 沉稳踏实、坚守本心，身边的人都愿意信任你。",
            "🌍 厚积薄发，你的稳重终将成为最强大的力量。"
        ]
    }
}

# 题库
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

# ===================== 封装计分函数 =====================
def calc_radio_score(answer):
    if answer in ("主动出手，直面挑战", "热情直率，敢想敢做", "冲锋的领导者", "热闹热烈"):
        st.session_state.score_fire += 1
    elif answer in ("冷静观察，伺机行动", "心思细腻，共情力强", "幕后的观察者", "安静温润"):
        st.session_state.score_water += 1
    elif answer in ("灵活周旋，快速脱身", "随性自由，不喜束缚", "活跃的协调者", "开阔自由"):
        st.session_state.score_wind += 1
    else:
        st.session_state.score_earth += 1

def calc_slider_score(answer):
    if answer == 1:
        st.session_state.score_fire += 1
    elif answer == 2:
        st.session_state.score_wind += 1
    elif answer == 3:
        st.session_state.score_water += 1
    else:
        st.session_state.score_earth += 1

def calc_multiselect_score(answer_list):
    if "勇敢果敢" in answer_list:
        st.session_state.score_fire += 1
    if "温柔内敛" in answer_list:
        st.session_state.score_water += 1
    if "洒脱自在" in answer_list:
        st.session_state.score_wind += 1
    if "踏实可靠" in answer_list:
        st.session_state.score_earth += 1

# ===================== 初始化会话状态 =====================
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
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * TOTAL_QUESTION

# ===================== 全局响应式样式（适配手机+电脑，优化配色） =====================
base_css = """
<style>
/* 全局背景、字体 */
html, body, .stApp {
    background-color: #FAF9F6;
    font-family: "Microsoft Yahei", sans-serif;
}

/* 响应式布局适配 */
@media (max-width: 768px) {
    /* 手机端字体缩放 */
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.3rem !important; }
    h3 { font-size: 1.1rem !important; }
    p, div, label, .stMarkdown p { font-size: 0.9rem !important; }
    /* 手机端内边距 */
    .block-container { padding: 1rem !important; }
    .result-card { padding: 1rem !important; }
}

/* 隐藏多余边框、阴影 */
div[data-testid="stVerticalBlock"] > div {
    border: none !important;
    box-shadow: none !important;
}

hr {
    border-top: 1px solid #E8E8E8 !important;
    margin: 1rem 0;
}

/* 按钮通用样式 */
.stButton > button {
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    transition: 0.2s;
    font-weight: 500;
}
.stButton > button:hover {
    opacity: 0.9;
}

/* 输入框、选择框样式优化 */
.stTextInput > div, .stSelectbox > div, .stMultiSelect > div, .stSlider > div {
    border: 1px solid #E0E0E0 !important;
    border-radius: 8px !important;
}

/* 折叠面板样式 */
.stExpander {
    border: 1px solid #E0E0E0 !important;
    border-radius: 8px !important;
}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)

# ===================== 页面头部 =====================
st.title(PAGE_TITLE)
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

# ===================== 逐题逻辑（修复答案记忆index类型错误） =====================
# 第1题
if q_num == 1:
    q = QUESTION_LIST[0]
    selected_index = None
    if st.session_state.user_answers[0] is not None:
        selected_index = q["options"].index(st.session_state.user_answers[0])
    ans = st.radio(q["title"], q["options"], index=selected_index)
    st.info(q["tip"])
    if st.button("下一题"):
        if ans is None:
            st.warning("请先选择一个答案再继续！")
        else:
            st.session_state.user_answers[0] = ans
            calc_radio_score(ans)
            st.session_state.current_q = 2
            st.toast("已完成本题，进入下一题")
            st.rerun()

# 第2题
elif q_num == 2:
    q = QUESTION_LIST[1]
    selected_index = None
    if st.session_state.user_answers[1] is not None:
        selected_index = q["options"].index(st.session_state.user_answers[1])
    ans = st.radio(q["title"], q["options"], index=selected_index)
    st.info(q["tip"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 1
            st.rerun()
    with col2:
        if st.button("下一题"):
            if ans is None:
                st.warning("请先选择一个答案再继续！")
            else:
                st.session_state.user_answers[1] = ans
                calc_radio_score(ans)
                st.session_state.current_q = 3
                st.toast("已完成本题，进入下一题")
                st.rerun()

# 第3题
elif q_num == 3:
    q = QUESTION_LIST[2]
    selected_index = None
    if st.session_state.user_answers[2] is not None:
        selected_index = q["options"].index(st.session_state.user_answers[2])
    ans = st.radio(q["title"], q["options"], index=selected_index)
    st.info(q["tip"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 2
            st.rerun()
    with col2:
        if st.button("下一题"):
            if ans is None:
                st.warning("请先选择一个答案再继续！")
            else:
                st.session_state.user_answers[2] = ans
                calc_radio_score(ans)
                st.session_state.current_q = 4
                st.toast("已完成本题，进入下一题")
                st.rerun()

# 第4题
elif q_num == 4:
    q = QUESTION_LIST[3]
    selected_index = None
    if st.session_state.user_answers[3] is not None:
        selected_index = q["options"].index(st.session_state.user_answers[3])
    ans = st.radio(q["title"], q["options"], index=selected_index)
    st.info(q["tip"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 3
            st.rerun()
    with col2:
        if st.button("下一题"):
            if ans is None:
                st.warning("请先选择一个答案再继续！")
            else:
                st.session_state.user_answers[3] = ans
                calc_radio_score(ans)
                st.session_state.current_q = 5
                st.toast("已完成本题，进入下一题")
                st.rerun()

# 第5题 滑块
elif q_num == 5:
    q = QUESTION_LIST[4]
    default_val = st.session_state.user_answers[4] if st.session_state.user_answers[4] is not None else 2
    ans = st.slider(q["title"], 1, 4, default_val, help="1=缺乏耐心、行动优先 | 4=极具耐心、沉稳优先")
    st.caption("1：急躁好动 | 2：中等耐心 | 3：比较耐心 | 4：极度沉稳")
    st.info(q["tip"])
    col1, col2 = st.columns(2)
    with col1:
        if st.button("上一题"):
            st.session_state.current_q = 4
            st.rerun()
    with col2:
        if st.button("下一题"):
            st.session_state.user_answers[4] = ans
            calc_slider_score(ans)
            st.session_state.current_q = 6
            st.toast("已完成本题，进入下一题")
            st.rerun()

# 第6题 多选
elif q_num == 6:
    q = QUESTION_LIST[5]
    ans = st.multiselect(q["title"], q["options"], default=st.session_state.user_answers[5])
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
                st.session_state.user_answers[5] = ans
                calc_multiselect_score(ans)
                st.session_state.current_q = 7
                st.toast("所有题目作答完毕，正在生成结果")
                st.rerun()

# ===================== 结果页面：动态元素主题色 + 美化进度条 =====================
# ===================== 结果页面：无图表，纯文字卡片展示 =====================
elif q_num == 7:
    # 计算总分、判定本命元素
    all_score = {
        "火": st.session_state.score_fire,
        "水": st.session_state.score_water,
        "风": st.session_state.score_wind,
        "土": st.session_state.score_earth
    }
    max_score = max(all_score.values())
    tie_list = [k for k, v in all_score.items() if v == max_score]
    if len(tie_list) > 1:
        final_choice = tie_list[0]
        st.info(f"出现平局！你同时契合：{'、'.join(tie_list)} 多种元素特质")
    else:
        final_choice = max(all_score, key=all_score.get)

    # 获取当前元素专属主题色
    main_color = ELEMENT_THEME_COLOR[final_choice]

    # 动态CSS：结果页专属主题色
    theme_css = f"""
    <style>
    .stApp {{
        background-color: {main_color}12 !important;
    }}
    div[data-testid="stProgress"] > div > div {{
        background-color: {main_color} !important;
        border-radius: 10px;
    }}
    div[data-testid="stProgress"] {{
        border-radius: 10px;
        background-color: #E8E8E8;
    }}
    .stButton > button {{
        background-color: {main_color} !important;
        color: #FFFFFF !important;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: scale(0.95);}}
        to {{opacity: 1; transform: scale(1);}}
    }}
    .result-card {{
        animation: fadeIn 1s ease-in-out;
        text-align: center; 
        padding: 1.5rem; 
        border-radius: 12px; 
        background-color: {main_color}20;
        border: 1px solid {main_color}40;
    }}
    .score-card {{
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--color);
    }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

    st.divider()

    # 分数明细（用卡片展示，带元素主题色边框）
    st.subheader("你的元素得分明细")
    score_items = [
        ("火", st.session_state.score_fire, ELEMENT_THEME_COLOR["火"]),
        ("水", st.session_state.score_water, ELEMENT_THEME_COLOR["水"]),
        ("风", st.session_state.score_wind, ELEMENT_THEME_COLOR["风"]),
        ("土", st.session_state.score_earth, ELEMENT_THEME_COLOR["土"])
    ]
    # 按分数从高到低排序
    score_items.sort(key=lambda x: x[1], reverse=True)

    for elem, score, color in score_items:
        st.markdown(f"""
        <div class="score-card" style="--color: {color};">
            <strong>{elem}元素</strong>：{score} 分
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 元素信息与彩蛋
    res_name = ELEMENT_INFO[final_choice]["name"]
    res_desc = ELEMENT_INFO[final_choice]["desc"]
    egg_list = ELEMENT_INFO[final_choice]["egg"]
    egg_text = random.choice(egg_list)

    # 结果卡片
    st.markdown(f"""
    <div class="result-card">
        <h2 style="color: {main_color};">{res_name}</h2>
        <p style="font-size: 1.1rem;">{name}，你的本命元素为【{final_choice}】</p>
        <p style="font-style: italic; color: #555; font-size: 1rem;">{res_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"✨ 专属寄语：{egg_text}")
    st.toast("匹配完成！炼金身份已激活")
    st.divider()

    # 分享文案
    share_text = f"我完成了元素人格测试！代号：{name}，本命元素：{final_choice}，身份：{res_name}"
    st.text_area("一键复制分享", value=share_text, height=80)
    st.divider()

    # 重置确认弹窗
    st.subheader("重新测试")
    confirm = st.checkbox("确认清空所有记录，重新开始测试？")
    if st.button("点击重置") and confirm:
        st.session_state.current_q = 1
        st.session_state.score_fire = 0
        st.session_state.score_water = 0
        st.session_state.score_wind = 0
        st.session_state.score_earth = 0
        st.session_state.user_answers = [None] * TOTAL_QUESTION
        st.rerun()