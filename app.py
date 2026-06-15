"""
赛博炼金术士 · 元素人格测试仪

功能说明：
- 通过10道测试题，分析用户的元素人格类型（火、水、风、土）
- 每道题的4个选项对应不同的元素特质
- 根据用户选择计算各元素得分，最终确定人格类型
- 提供详细的元素档案和个性化文案

应用流程：
1. 用户输入代号
2. 逐题回答10道测试题
3. 系统计算各元素得分
4. 显示最终人格类型和详细档案
"""

# ============================================================================
# 1. 导入库和配置
# ============================================================================

import streamlit as st
import random

# ============================================================================
# 1.1 页面配置
# ============================================================================

PAGE_TITLE = "赛博炼金术士 · 元素人格测试仪"
PAGE_ICON = "🔮"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 2. 常量和配置数据
# ============================================================================

# ============================================================================
# 2.1 元素主题配色（莫兰迪柔和版）
# ============================================================================

ELEMENT_THEME_COLOR = {
    "火": "#E67E7E",    # 柔和暖红
    "水": "#7EA8E6",    # 清透浅蓝
    "风": "#7EE6B8",    # 清新薄荷绿
    "土": "#E6C87E"     # 暖调浅黄
}

# ============================================================================
# 2.2 元素档案文案
# ============================================================================

ELEMENT_INTRO = """
- **火元素**：代表勇气、热情、行动力，天生的开拓者与领导者。
- **水元素**：代表冷静、细腻、共情力，善于观察与思考。
- **风元素**：代表自由、敏捷、创造力，适应力强、思维跳脱。
- **土元素**：代表稳重、坚守、责任感，团队中可靠的守护者。
"""

# ============================================================================
# 2.3 元素详细信息
# ============================================================================

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

# ============================================================================
# 2.4 测试题库（10道题）
# ============================================================================

QUESTION_LIST = [
    {
        "title": "问题1：团队陷入困境，你会？",
        "options": ["主动站出，带领大家突破", "冷静分析，找出问题根源", "提出新思路，灵活变通", "坚守岗位，稳定军心"],
        "tip": "这道题测试你在危机中的角色定位",
        "type": "radio"
    },
    {
        "title": "问题2：做决策时，你更倾向于？",
        "options": ["凭直觉，快速决断", "深思熟虑，权衡利弊", "收集信息，灵活调整", "遵循经验，稳妥行事"],
        "tip": "决策方式反映你的思维模式",
        "type": "radio"
    },
    {
        "title": "问题3：朋友向你倾诉烦恼，你会？",
        "options": ["直接给出解决方案", "耐心倾听，给予安慰", "转移话题，带TA散心", "默默陪伴，提供支持"],
        "tip": "与人相处的方式能反映你的元素特质",
        "type": "radio"
    },
    {
        "title": "问题4：周末你更想做什么？",
        "options": ["参加热闹的聚会", "在家安静看书或看电影", "探索新地方、尝试新事物", "整理房间、做些家务"],
        "tip": "休闲方式暴露你的内在需求",
        "type": "radio"
    },
    {
        "title": "问题5：面对批评，你的反应是？",
        "options": ["当场反驳，维护立场", "冷静接受，反思改进", "一笑置之，不当回事", "认真记录，逐步改进"],
        "tip": "面对负面反馈的态度很重要",
        "type": "radio"
    },
    {
        "title": "问题6：学习新技能时，你会？",
        "options": ["直接上手实践", "先研究理论再动手", "边学边玩，保持兴趣", "制定计划，循序渐进"],
        "tip": "学习方式体现你的性格特点",
        "type": "radio"
    },
    {
        "title": "问题7：团队合作中，你最看重？",
        "options": ["效率第一，快速完成", "氛围和谐，互相尊重", "创意激发，思维碰撞", "分工明确，各司其职"],
        "tip": "团队价值观反映你的处事原则",
        "type": "radio"
    },
    {
        "title": "问题8：遇到意外惊喜，你会？",
        "options": ["兴奋欢呼，与人分享", "内心喜悦，表面平静", "觉得有趣，一笑而过", "保持冷静，先确认情况"],
        "tip": "情绪表达能看出你的元素倾向",
        "type": "radio"
    },
    {
        "title": "问题9：你更喜欢的沟通方式？",
        "options": ["直截了当，开门见山", "委婉含蓄，顾及感受", "轻松幽默，不拘形式", "条理清晰，逻辑严谨"],
        "tip": "沟通风格体现你的性格类型",
        "type": "radio"
    },
    {
        "title": "问题10：你向往的生活状态是？",
        "options": ["充满激情与挑战", "平静安稳，内心丰盈", "自由随性，无拘无束", "踏实稳定，有所成就"],
        "tip": "理想生活反映你的核心追求",
        "type": "radio"
    }
]

TOTAL_QUESTION = 10

# ============================================================================
# 2.5 元素选项映射（用于计分）
# ============================================================================

# 火元素选项列表
FIRE_OPTIONS = [
    "主动站出，带领大家突破", "凭直觉，快速决断", "直接给出解决方案",
    "参加热闹的聚会", "当场反驳，维护立场", "直接上手实践",
    "效率第一，快速完成", "兴奋欢呼，与人分享", "直截了当，开门见山",
    "充满激情与挑战"
]

# 水元素选项列表
WATER_OPTIONS = [
    "冷静分析，找出问题根源", "深思熟虑，权衡利弊", "耐心倾听，给予安慰",
    "在家安静看书或看电影", "冷静接受，反思改进", "先研究理论再动手",
    "氛围和谐，互相尊重", "内心喜悦，表面平静", "委婉含蓄，顾及感受",
    "平静安稳，内心丰盈"
]

# 风元素选项列表
WIND_OPTIONS = [
    "提出新思路，灵活变通", "收集信息，灵活调整", "转移话题，带TA散心",
    "探索新地方、尝试新事物", "一笑置之，不当回事", "边学边玩，保持兴趣",
    "创意激发，思维碰撞", "觉得有趣，一笑而过", "轻松幽默，不拘形式",
    "自由随性，无拘无束"
]

# 土元素选项列表
EARTH_OPTIONS = [
    "坚守岗位，稳定军心", "遵循经验，稳妥行事", "默默陪伴，提供支持",
    "整理房间、做些家务", "认真记录，逐步改进", "制定计划，循序渐进",
    "分工明确，各司其职", "保持冷静，先确认情况", "条理清晰，逻辑严谨",
    "踏实稳定，有所成就"
]

# ============================================================================
# 3. 核心功能函数
# ============================================================================

def init_session_state():
    """
    初始化会话状态
    
    功能：
    - 初始化当前题目编号
    - 初始化各元素得分
    - 初始化用户答案列表
    """
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

def calc_radio_score(answer):
    """
    计算单选题得分
    
    功能：
    - 根据用户选择的答案，增加对应元素的得分
    - 火元素选项：选项索引0（每题第一个选项）
    - 水元素选项：选项索引1（每题第二个选项）
    - 风元素选项：选项索引2（每题第三个选项）
    - 土元素选项：选项索引3（每题第四个选项）
    
    参数：
        answer (str): 用户选择的答案文本
    """
    if answer in FIRE_OPTIONS:
        st.session_state.score_fire += 1
    elif answer in WATER_OPTIONS:
        st.session_state.score_water += 1
    elif answer in WIND_OPTIONS:
        st.session_state.score_wind += 1
    elif answer in EARTH_OPTIONS:
        st.session_state.score_earth += 1

def render_question(question_index):
    """
    渲染单个题目
    
    功能：
    - 显示题目标题、选项和提示信息
    - 处理用户答案选择
    - 提供上一题/下一题导航功能
    - 第一题只显示"下一题"按钮
    - 最后一题显示"查看结果"按钮
    
    参数：
        question_index (int): 题目索引（0-9）
    """
    question = QUESTION_LIST[question_index]
    question_number = question_index + 1
    
    # 获取已选择的答案索引（用于回显）
    selected_index = None
    if st.session_state.user_answers[question_index] is not None:
        selected_index = question["options"].index(st.session_state.user_answers[question_index])
    
    # 显示题目和选项
    answer = st.radio(question["title"], question["options"], index=selected_index)
    st.info(question["tip"])
    
    # 根据题目位置显示不同的导航按钮
    if question_number == 1:
        # 第一题：只有"下一题"按钮
        if st.button("下一题", key=f"next_{question_number}"):
            if answer is None:
                st.warning("请先选择一个答案再继续！")
            else:
                st.session_state.user_answers[question_index] = answer
                calc_radio_score(answer)
                st.session_state.current_q = question_number + 1
                st.toast("已完成本题，进入下一题")
                st.rerun()
    
    elif question_number == TOTAL_QUESTION:
        # 最后一题：显示"上一题"和"查看结果"按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("上一题", key=f"prev_{question_number}"):
                st.session_state.current_q = question_number - 1
                st.rerun()
        with col2:
            if st.button("查看结果", key=f"result_{question_number}"):
                if answer is None:
                    st.warning("请先选择一个答案再继续！")
                else:
                    st.session_state.user_answers[question_index] = answer
                    calc_radio_score(answer)
                    st.session_state.current_q = TOTAL_QUESTION + 1
                    st.toast("所有题目作答完毕，正在生成结果")
                    st.rerun()
    
    else:
        # 中间题目：显示"上一题"和"下一题"按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("上一题", key=f"prev_{question_number}"):
                st.session_state.current_q = question_number - 1
                st.rerun()
        with col2:
            if st.button("下一题", key=f"next_{question_number}"):
                if answer is None:
                    st.warning("请先选择一个答案再继续！")
                else:
                    st.session_state.user_answers[question_index] = answer
                    calc_radio_score(answer)
                    st.session_state.current_q = question_number + 1
                    st.toast("已完成本题，进入下一题")
                    st.rerun()

def get_element_result():
    """
    获取最终元素结果
    
    功能：
    - 根据各元素得分，确定用户的元素人格类型
    - 返回得分最高的元素
    
    返回：
        str: 元素类型（"火"、"水"、"风"、"土"）
    """
    scores = {
        "火": st.session_state.score_fire,
        "水": st.session_state.score_water,
        "风": st.session_state.score_wind,
        "土": st.session_state.score_earth
    }
    return max(scores, key=scores.get)

def render_result_page(name):
    """
    渲染结果页面
    
    功能：
    - 显示用户的元素人格类型
    - 显示详细的元素档案信息
    - 显示随机彩蛋文案
    - 显示各元素得分分布
    
    参数：
        name (str): 用户代号
    """
    # 获取最终元素类型
    element = get_element_result()
    element_info = ELEMENT_INFO[element]
    
    # 显示结果标题
    st.markdown(f"""
    <div style='background-color: {element_info["color"]}; 
                padding: 2rem; 
                border-radius: 15px; 
                text-align: center;
                margin-bottom: 2rem;'>
        <h2 style='color: white; margin: 0;'>🎉 {name} 的炼金身份揭晓</h2>
        <h1 style='color: white; margin: 1rem 0;'>{element_info["name"]}</h1>
        <p style='color: white; font-size: 1.2rem;'>{element_info["desc"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示随机彩蛋
    random_egg = random.choice(element_info["egg"])
    st.success(random_egg)
    
    # 显示得分分布
    st.subheader("📊 元素得分分布")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔥 火元素", st.session_state.score_fire)
    with col2:
        st.metric("💧 水元素", st.session_state.score_water)
    with col3:
        st.metric("🌪️ 风元素", st.session_state.score_wind)
    with col4:
        st.metric("🌍 土元素", st.session_state.score_earth)
    
    # 显示答题回顾
    st.divider()
    st.subheader("📝 答题回顾")
    for i, answer in enumerate(st.session_state.user_answers):
        if answer:
            st.write(f"**问题{i+1}**: {answer}")
    
    # 重新测试按钮
    st.divider()
    if st.button("🔄 重新测试", use_container_width=True):
        # 重置所有状态
        st.session_state.current_q = 1
        st.session_state.score_fire = 0
        st.session_state.score_water = 0
        st.session_state.score_wind = 0
        st.session_state.score_earth = 0
        st.session_state.user_answers = [None] * TOTAL_QUESTION
        st.rerun()

# ============================================================================
# 4. CSS样式定义
# ============================================================================

def render_styles():
    """
    渲染全局CSS样式
    
    功能：
    - 设置全局背景和字体
    - 定义标题和正文的字体大小
    - 优化按钮、单选按钮、输入框等组件样式
    - 添加响应式布局适配（手机和电脑）
    """
    css = """
    <style>
    /* 全局背景、字体 */
    html, body, .stApp {
        background-color: #FAF9F6;
        font-family: "Microsoft Yahei", "PingFang SC", sans-serif;
        font-size: 16px !important;
    }

    /* 标题字体大小 */
    h1 { font-size: 2.2rem !important; font-weight: 700; }
    h2 { font-size: 1.8rem !important; font-weight: 600; }
    h3 { font-size: 1.5rem !important; font-weight: 600; }
    h4 { font-size: 1.3rem !important; font-weight: 600; }

    /* 正文和标签字体 */
    p, div, label, .stMarkdown p, .stTextInput > div > div > input { 
        font-size: 1.1rem !important; 
        line-height: 1.6;
    }

    /* 响应式布局适配 */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.3rem !important; }
        h4 { font-size: 1.1rem !important; }
        p, div, label { font-size: 1rem !important; }
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

    /* 按钮通用样式 - 增大尺寸 */
    .stButton > button {
        border-radius: 10px;
        border: none;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600;
        transition: 0.2s;
        min-height: 48px !important;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }

    /* 单选按钮样式 */
    .stRadio > div {
        padding: 0.5rem 0;
    }
    .stRadio > div > label {
        font-size: 1.1rem !important;
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        transition: 0.2s;
    }
    .stRadio > div > label:hover {
        background-color: #F0F0F0;
    }

    /* 输入框样式优化 */
    .stTextInput > div, .stSelectbox > div, .stMultiSelect > div {
        border: 1px solid #E0E0E0 !important;
        border-radius: 10px !important;
        padding: 0.5rem;
    }
    .stTextInput input {
        font-size: 1.1rem !important;
    }

    /* 折叠面板样式 */
    .stExpander {
        border: 1px solid #E0E0E0 !important;
        border-radius: 10px !important;
    }
    .stExpander > button {
        font-size: 1.1rem !important;
    }

    /* 进度条样式 */
    div[data-testid="stProgress"] {
        height: 20px !important;
        border-radius: 10px;
        background-color: #E8E8E8;
    }
    div[data-testid="stProgress"] > div > div {
        border-radius: 10px;
    }

    /* 信息提示样式 */
    .stInfo, .stWarning, .stSuccess {
        padding: 1rem !important;
        border-radius: 10px;
        font-size: 1rem !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# 5. 主程序逻辑
# ============================================================================

def main():
    """
    主应用入口
    
    执行流程：
    1. 渲染CSS样式
    2. 初始化会话状态
    3. 显示页面头部和元素档案
    4. 获取用户代号输入
    5. 显示答题进度条
    6. 根据当前题目编号渲染对应题目或结果页面
    """
    # 1. 渲染样式
    render_styles()
    
    # 2. 初始化会话状态
    init_session_state()
    
    # 3. 显示页面头部
    st.title(PAGE_TITLE)
    st.caption("「当危机降临，你的本能会是什么？」逐题完成问卷，解锁专属炼金身份")
    st.divider()
    
    # 显示元素档案折叠面板
    with st.expander("四大元素档案（点击查看）"):
        st.markdown(ELEMENT_INTRO)
    st.divider()
    
    # 4. 获取用户代号
    name = st.text_input("你的代号是？", placeholder="比如：炼金学徒小A")
    st.divider()
    
    # 代号非空校验
    if not name:
        st.info("请先填写你的代号，再开始答题")
        st.stop()
    
    # 5. 显示答题区域
    st.subheader("炼金试炼问卷")
    
    # 显示进度条
    current_question = st.session_state.current_q
    if current_question <= TOTAL_QUESTION:
        progress = current_question / TOTAL_QUESTION
        st.progress(progress, text=f"答题进度：第{current_question}题 / 共{TOTAL_QUESTION}题")
    st.divider()
    
    # 6. 根据当前题目编号渲染对应内容
    if current_question <= TOTAL_QUESTION:
        # 答题阶段：渲染当前题目
        render_question(current_question - 1)
    else:
        # 结果阶段：渲染结果页面
        render_result_page(name)

# ============================================================================
# 6. 应用启动
# ============================================================================

if __name__ == "__main__":
    main()