"""
赛博炼金术士 · 元素人格测试仪

功能说明：
- 通过10道测试题，分析用户的元素人格类型（火、水、风、土）
- 每道题的4个选项对应不同的元素特质
- 根据用户选择计算各元素得分，最终确定人格类型
- 提供详细的元素档案和个性化文案

应用流程：
1. 新用户引导页
2. 用户输入代号
3. 逐题回答10道测试题
4. 显示最终人格类型和详细分析报告
"""

# ============================================================================
# 1. 导入库和配置
# ============================================================================

import streamlit as st
import random
import json

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

ELEMENT_EMOJI = {
    "火": "🔥",
    "水": "💧",
    "风": "🌪️",
    "土": "🌍"
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
        "strengths": ["勇敢果断", "充满热情", "行动力强", "敢于挑战"],
        "weaknesses": ["缺乏耐心", "容易冲动", "过于直接", "不愿妥协"],
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
        "strengths": ["心思细腻", "善于倾听", "富有同理心", "冷静理性"],
        "weaknesses": ["过于敏感", "犹豫不决", "容易情绪化", "不愿表达"],
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
        "strengths": ["思维敏捷", "创造力强", "适应力好", "善于沟通"],
        "weaknesses": ["缺乏专注", "容易分心", "不够踏实", "难以坚持"],
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
        "strengths": ["稳重可靠", "责任心强", "耐心细致", "踏实务实"],
        "weaknesses": ["过于保守", "不愿改变", "缺乏变通", "略显固执"],
        "egg": [
            "🌍 大地无言，却承载万物，可靠就是你的代名词。",
            "🌍 沉稳踏实、坚守本心，身边的人都愿意信任你。",
            "🌍 厚积薄发，你的稳重终将成为最强大的力量。"
        ]
    }
}

# ============================================================================
# 2.4 职业建议
# ============================================================================

CAREER_ADVICE = {
    "火": {
        "title": "🔥 适合你的职业方向",
        "advice": ["销售与营销", "创业与管理", "演艺与主持", "运动与竞技", "公关与谈判"],
        "reason": "你天生具有领导能力和感染力，适合需要勇气和行动力的工作"
    },
    "水": {
        "title": "💧 适合你的职业方向",
        "advice": ["心理咨询", "艺术设计", "写作编辑", "科研分析", "医疗护理"],
        "reason": "你细腻敏感，善于观察和倾听，适合与人打交道的工作"
    },
    "风": {
        "title": "🌪️ 适合你的职业方向",
        "advice": ["软件开发", "市场营销", "教育培训", "创意策划", "媒体传播"],
        "reason": "你思维敏捷、创意丰富，适合需要创新和灵活应变的工作"
    },
    "土": {
        "title": "🌍 适合你的职业方向",
        "advice": ["财务管理", "工程技术", "运营管理", "法律法务", "建筑设计"],
        "reason": "你稳重可靠、责任心强，适合需要严谨和踏实的工作"
    }
}

# ============================================================================
# 2.5 人际相处建议
# ============================================================================

RELATIONSHIP_ADVICE = {
    "火": {
        "title": "🔥 人际相处小贴士",
        "advice": [
            "学会倾听，给他人表达的机会",
            "放慢脚步，不要急于做出决定",
            "注意表达方式，避免过于直接伤人",
            "学会妥协，接受不同意见"
        ]
    },
    "水": {
        "title": "💧 人际相处小贴士",
        "advice": [
            "勇敢表达自己的需求，不要总是迁就他人",
            "学会拒绝，不必事事都答应",
            "适当释放情绪，不要憋在心里",
            "相信自己的判断，不必过分在意他人看法"
        ]
    },
    "风": {
        "title": "🌪️ 人际相处小贴士",
        "advice": [
            "做事更专注一些，避免注意力分散",
            "承诺的事情要坚持完成",
            "学会深入思考，不要浅尝辄止",
            "给朋友更多稳定可靠的感觉"
        ]
    },
    "土": {
        "title": "🌍 人际相处小贴士",
        "advice": [
            "尝试接受新事物，给自己更多可能性",
            "学会变通，不要过于固执",
            "适当放松，不要对自己要求太高",
            "多尝试冒险，体验不一样的人生"
        ]
    }
}

# ============================================================================
# 2.6 学习风格建议
# ============================================================================

LEARNING_STYLE = {
    "火": {
        "title": "🔥 你的学习风格",
        "style": "实践驱动型",
        "description": "你在实践中学习效果最好，通过动手操作和尝试错误来掌握知识。",
        "tips": [
            "多进行项目实践，从做中学",
            "设定明确的目标和期限",
            "将学习内容与实际应用结合",
            "定期总结实践经验"
        ]
    },
    "水": {
        "title": "💧 你的学习风格",
        "style": "深度思考型",
        "description": "你善于深入思考和分析，喜欢在理解原理后再进行实践。",
        "tips": [
            "先建立理论框架，再逐步深入",
            "多阅读和研究相关资料",
            "做详细的笔记和思维导图",
            "与他人讨论以加深理解"
        ]
    },
    "风": {
        "title": "🌪️ 你的学习风格",
        "style": "灵活探索型",
        "description": "你喜欢探索多种可能性，思维敏捷，适应力强。",
        "tips": [
            "尝试不同的学习方法和工具",
            "保持好奇心，广泛涉猎",
            "将不同领域的知识交叉应用",
            "设置合理的专注时间"
        ]
    },
    "土": {
        "title": "🌍 你的学习风格",
        "style": "稳步积累型",
        "description": "你注重基础和系统性，喜欢按部就班地学习。",
        "tips": [
            "制定详细的学习计划",
            "注重基础知识的巩固",
            "定期复习和总结",
            "循序渐进，不急于求成"
        ]
    }
}

# ============================================================================
# 2.7 恋爱相处建议
# ============================================================================

LOVE_ADVICE = {
    "火": {
        "title": "🔥 恋爱相处指南",
        "strengths": ["热情主动", "浪漫大方", "敢于表达", "行动力强"],
        "tips": [
            "在表达爱意的同时，也要倾听对方的感受",
            "给对方一些私人空间，不要过于粘人",
            "学会控制情绪，避免冲动吵架",
            "用行动证明你的爱意，而不只是言语"
        ],
        "match": ["水", "土"]
    },
    "水": {
        "title": "💧 恋爱相处指南",
        "strengths": ["温柔体贴", "善解人意", "情感丰富", "细腻敏感"],
        "tips": [
            "勇敢表达自己的需求，不要让对方猜",
            "学会拒绝，保持自我边界",
            "不要过于依赖对方，保持独立",
            "多与伴侣沟通，分享内心感受"
        ],
        "match": ["火", "风"]
    },
    "风": {
        "title": "🌪️ 恋爱相处指南",
        "strengths": ["风趣幽默", "思想开放", "善于沟通", "充满创意"],
        "tips": [
            "保持承诺的稳定性，不要轻易改变计划",
            "在社交活动中也要关注伴侣的感受",
            "学会专注倾听，不要分心",
            "用行动证明你的关心"
        ],
        "match": ["土", "水"]
    },
    "土": {
        "title": "🌍 恋爱相处指南",
        "strengths": ["可靠稳定", "责任心强", "细心周到", "踏实务实"],
        "tips": [
            "偶尔制造一些浪漫惊喜",
            "学会表达情感，不要过于内敛",
            "尝试接受伴侣的新想法",
            "多给对方一些赞美和肯定"
        ],
        "match": ["火", "风"]
    }
}

# ============================================================================
# 2.8 名人类型参考
# ============================================================================

CELEBRITY_REFERENCE = {
    "火": [
        {"name": "史蒂夫·乔布斯", "desc": "苹果公司创始人，充满激情与创造力"},
        {"name": "埃隆·马斯克", "desc": "特斯拉CEO，敢于冒险的创新者"},
        {"name": "麦当娜", "desc": "流行天后，勇于突破传统"},
        {"name": "马云", "desc": "阿里巴巴创始人，激情澎湃的领导者"}
    ],
    "水": [
        {"name": "爱因斯坦", "desc": "伟大物理学家，深邃的思考者"},
        {"name": "村上春树", "desc": "著名作家，细腻的文字表达"},
        {"name": "奥黛丽·赫本", "desc": "优雅女神，温柔而坚韧"},
        {"name": "李安", "desc": "著名导演，细腻的情感表达"}
    ],
    "风": [
        {"name": "达芬奇", "desc": "文艺复兴全才，多才多艺"},
        {"name": "理查德·布兰森", "desc": "维珍集团创始人，自由不羁的冒险家"},
        {"name": "周星驰", "desc": "喜剧之王，天马行空的创意"},
        {"name": "乔布斯", "desc": "产品设计天才，跨界创新者"}
    ],
    "土": [
        {"name": "巴菲特", "desc": "股神，稳健的投资大师"},
        {"name": "任正非", "desc": "华为创始人，踏实务实的领导者"},
        {"name": "科比·布莱恩特", "desc": "篮球巨星，勤奋坚持的代表"},
        {"name": "董明珠", "desc": "格力董事长，坚韧不拔的企业家"}
    ]
}

# ============================================================================
# 2.6 测试题库（优化版，增加区分度）
# ============================================================================

QUESTION_LIST = [
    {
        "title": "问题1：团队项目遇到重大瓶颈，大家都很沮丧，你会怎么做？",
        "options": [
            "拍案而起，大声激励大家：'这点困难算什么！跟我来！'",
            "召集大家围坐一圈，冷静分析问题：'我们一步步拆解这个难题'",
            "讲个自嘲的笑话活跃气氛：'看来我们需要一点魔法来突破困境'",
            "默默回到工位，把自己负责的部分做到完美：'做好本分就是对团队最大的支持'"
        ],
        "tip": "危机中的第一反应最能暴露你的核心特质",
        "type": "radio"
    },
    {
        "title": "问题2：领导突然让你接手一个全新领域的项目，你会？",
        "options": [
            "立刻答应：'没问题！我马上开始！'，然后边做边摸索",
            "先问清楚：'能给我一天时间调研吗？我想先了解清楚'",
            "兴奋地说：'太棒了！终于有机会挑战新东西了'",
            "谨慎回应：'我需要看看相关资料，制定详细计划后再开始'"
        ],
        "tip": "面对未知挑战的态度反映你的性格底色",
        "type": "radio"
    },
    {
        "title": "问题3：朋友失恋后哭着找你倾诉，你会怎么做？",
        "options": [
            "拍桌而起：'那个渣男/渣女！走，我陪你去找TA理论！'",
            "递上纸巾，默默听TA说完，然后温柔地说：'我懂你的感受'",
            "转移话题：'别难过了，我带你去吃好吃的/看场电影'",
            "默默煮一杯热茶放在TA面前，安静地坐在旁边陪伴"
        ],
        "tip": "安慰他人的方式暴露你的情感表达方式",
        "type": "radio"
    },
    {
        "title": "问题4：公司组织团建，你会选择参加哪个活动？",
        "options": [
            "激情四射的篝火晚会，围着篝火唱歌跳舞",
            "安静的茶话会，和同事们轻声聊天交流",
            "刺激的密室逃脱或户外探险",
            "温馨的厨艺比赛，大家一起动手做饭"
        ],
        "tip": "休闲偏好揭示你的能量来源",
        "type": "radio"
    },
    {
        "title": "问题5：会议上有人公开指出你的方案有漏洞，你会？",
        "options": [
            "立刻反驳：'你根本没理解我的方案！'",
            "认真记录：'谢谢你的建议，我会仔细考虑'",
            "笑着化解：'哈哈，被你发现了！我们一起来完善它吧'",
            "冷静回应：'这个问题确实存在，我们会后详细讨论解决方案'"
        ],
        "tip": "面对质疑的态度展现你的成熟度",
        "type": "radio"
    },
    {
        "title": "问题6：你想学一门新语言，你会从哪里开始？",
        "options": [
            "直接找个外国朋友聊天，边聊边学",
            "先买本语法书，系统学习基础规则",
            "看剧、听歌，在娱乐中自然习得",
            "制定学习计划，每天背单词、做练习"
        ],
        "tip": "学习方式反映你的认知模式",
        "type": "radio"
    },
    {
        "title": "问题7：小组作业临近截止，成员进度落后，你会？",
        "options": [
            "主动承担最难的部分：'把这个交给我！我来搞定！'",
            "组织大家开个线上会议：'我们来梳理一下每个人的进度'",
            "在群里发搞笑表情包鼓励大家：'加油！我们一定能搞定！'",
            "默默把自己负责的部分做完，然后帮落后的同学补位"
        ],
        "tip": "团队协作中的行为模式暴露你的角色定位",
        "type": "radio"
    },
    {
        "title": "问题8：路上偶遇多年未见的老同学，你会？",
        "options": [
            "冲上去给TA一个熊抱：'天哪！好久不见！太想你了！'",
            "微笑着点头：'好久不见，你还好吗？找个地方坐坐？'",
            "惊喜地挥手：'哇！这么巧！快加个微信，改天约！'",
            "礼貌地打招呼：'你好，好久没见了'"
        ],
        "tip": "社交场合的反应展现你的情感表达风格",
        "type": "radio"
    },
    {
        "title": "问题9：朋友向你借钱，你会怎么回应？",
        "options": [
            "豪爽地说：'要多少？我现在就转你！'",
            "温和地问：'遇到困难了吗？需要我帮什么忙？'",
            "开玩笑说：'哇，发财了记得还我啊！'然后爽快转账",
            "认真地说：'我需要了解一下用途，然后看我的情况'"
        ],
        "tip": "金钱往来的态度反映你的处事原则",
        "type": "radio"
    },
    {
        "title": "问题10：周末你计划旅行，你会怎么安排？",
        "options": [
            "说走就走！收拾行李立刻出发，路上再规划",
            "提前查好攻略，订好酒店和机票，做好详细计划",
            "随心所欲！走到哪里算哪里，享受在路上的感觉",
            "选择一个熟悉的地方，按往年的经验轻松出行"
        ],
        "tip": "旅行方式暴露你的生活态度",
        "type": "radio"
    }
]

TOTAL_QUESTION = 10

# ============================================================================
# 2.7 元素选项映射（用于计分）
# ============================================================================

ELEMENT_OPTIONS = {
    "火": [
        "拍案而起，大声激励大家：'这点困难算什么！跟我来！'",
        "立刻答应：'没问题！我马上开始！'，然后边做边摸索",
        "拍桌而起：'那个渣男/渣女！走，我陪你去找TA理论！'",
        "激情四射的篝火晚会，围着篝火唱歌跳舞",
        "立刻反驳：'你根本没理解我的方案！'",
        "直接找个外国朋友聊天，边聊边学",
        "主动承担最难的部分：'把这个交给我！我来搞定！'",
        "冲上去给TA一个熊抱：'天哪！好久不见！太想你了！'",
        "豪爽地说：'要多少？我现在就转你！'",
        "说走就走！收拾行李立刻出发，路上再规划"
    ],
    "水": [
        "召集大家围坐一圈，冷静分析问题：'我们一步步拆解这个难题'",
        "先问清楚：'能给我一天时间调研吗？我想先了解清楚'",
        "递上纸巾，默默听TA说完，然后温柔地说：'我懂你的感受'",
        "安静的茶话会，和同事们轻声聊天交流",
        "认真记录：'谢谢你的建议，我会仔细考虑'",
        "先买本语法书，系统学习基础规则",
        "组织大家开个线上会议：'我们来梳理一下每个人的进度'",
        "微笑着点头：'好久不见，你还好吗？找个地方坐坐？'",
        "温和地问：'遇到困难了吗？需要我帮什么忙？'",
        "提前查好攻略，订好酒店和机票，做好详细计划"
    ],
    "风": [
        "讲个自嘲的笑话活跃气氛：'看来我们需要一点魔法来突破困境'",
        "兴奋地说：'太棒了！终于有机会挑战新东西了'",
        "转移话题：'别难过了，我带你去吃好吃的/看场电影'",
        "刺激的密室逃脱或户外探险",
        "笑着化解：'哈哈，被你发现了！我们一起来完善它吧'",
        "看剧、听歌，在娱乐中自然习得",
        "在群里发搞笑表情包鼓励大家：'加油！我们一定能搞定！'",
        "惊喜地挥手：'哇！这么巧！快加个微信，改天约！'",
        "开玩笑说：'哇，发财了记得还我啊！'然后爽快转账",
        "随心所欲！走到哪里算哪里，享受在路上的感觉"
    ],
    "土": [
        "默默回到工位，把自己负责的部分做到完美：'做好本分就是对团队最大的支持'",
        "谨慎回应：'我需要看看相关资料，制定详细计划后再开始'",
        "默默煮一杯热茶放在TA面前，安静地坐在旁边陪伴",
        "温馨的厨艺比赛，大家一起动手做饭",
        "冷静回应：'这个问题确实存在，我们会后详细讨论解决方案'",
        "制定学习计划，每天背单词、做练习",
        "默默把自己负责的部分做完，然后帮落后的同学补位",
        "礼貌地打招呼：'你好，好久没见了'",
        "认真地说：'我需要了解一下用途，然后看我的情况'",
        "选择一个熟悉的地方，按往年的经验轻松出行"
    ]
}

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
    - 初始化访问状态（用于新用户引导）
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
    if "visited" not in st.session_state:
        st.session_state.visited = False

def render_welcome_page():
    """
    渲染新用户引导页（增强版）
    
    功能：
    - 介绍测试的目的和背景
    - 展示四大元素的特点（带悬停动画）
    - 说明测试规则（图标展示）
    - 提供开始测试按钮（带动画效果）
    """
    # 动态背景标题区域
    st.markdown("""
    <div class="welcome-header" style='text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); border-radius: 20px; margin-bottom: 2rem;'>
        <div style='animation: float 3s ease-in-out infinite;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 1rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>🔮 赛博炼金术士</h1>
        </div>
        <p style='font-size: 1.4rem; color: rgba(255,255,255,0.9);'>探索你的元素人格，解锁专属炼金身份</p>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.7); margin-top: 1rem;'>源自古老炼金术的人格测试，揭示你内心的元素力量</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 元素介绍卡片（带悬停动画）
    st.subheader("🌌 四大元素档案")
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div class="element-card fire-card" style='background: linear-gradient(135deg, rgba(230, 126, 126, 0.1) 0%, rgba(230, 126, 126, 0.05) 100%); 
                    border-radius: 15px; padding: 1.5rem; border: 2px solid rgba(230, 126, 126, 0.2); 
                    transition: all 0.3s ease; cursor: pointer;'>
            <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                <span style='font-size: 2.5rem; margin-right: 1rem;'>🔥</span>
                <h3 style='color: #E67E7E; font-size: 1.4rem;'>火元素</h3>
            </div>
            <p style='color: #666; line-height: 1.6;'>代表勇气、热情、行动力</p>
            <p style='color: #E67E7E; font-weight: 600; margin-top: 0.5rem;'>天生的开拓者与领导者</p>
            <div style='margin-top: 1rem; display: flex; gap: 0.5rem;'>
                <span style='background-color: rgba(230, 126, 126, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #E67E7E;'>勇敢</span>
                <span style='background-color: rgba(230, 126, 126, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #E67E7E;'>果断</span>
                <span style='background-color: rgba(230, 126, 126, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #E67E7E;'>热情</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="element-card water-card" style='background: linear-gradient(135deg, rgba(126, 168, 230, 0.1) 0%, rgba(126, 168, 230, 0.05) 100%); 
                    border-radius: 15px; padding: 1.5rem; border: 2px solid rgba(126, 168, 230, 0.2); 
                    transition: all 0.3s ease; cursor: pointer;'>
            <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                <span style='font-size: 2.5rem; margin-right: 1rem;'>💧</span>
                <h3 style='color: #7EA8E6; font-size: 1.4rem;'>水元素</h3>
            </div>
            <p style='color: #666; line-height: 1.6;'>代表冷静、细腻、共情力</p>
            <p style='color: #7EA8E6; font-weight: 600; margin-top: 0.5rem;'>善于观察与思考</p>
            <div style='margin-top: 1rem; display: flex; gap: 0.5rem;'>
                <span style='background-color: rgba(126, 168, 230, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #7EA8E6;'>细腻</span>
                <span style='background-color: rgba(126, 168, 230, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #7EA8E6;'>理性</span>
                <span style='background-color: rgba(126, 168, 230, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #7EA8E6;'>包容</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="element-card wind-card" style='background: linear-gradient(135deg, rgba(126, 230, 184, 0.1) 0%, rgba(126, 230, 184, 0.05) 100%); 
                    border-radius: 15px; padding: 1.5rem; border: 2px solid rgba(126, 230, 184, 0.2); 
                    transition: all 0.3s ease; cursor: pointer;'>
            <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                <span style='font-size: 2.5rem; margin-right: 1rem;'>🌪️</span>
                <h3 style='color: #7EE6B8; font-size: 1.4rem;'>风元素</h3>
            </div>
            <p style='color: #666; line-height: 1.6;'>代表自由、敏捷、创造力</p>
            <p style='color: #7EE6B8; font-weight: 600; margin-top: 0.5rem;'>适应力强、思维跳脱</p>
            <div style='margin-top: 1rem; display: flex; gap: 0.5rem;'>
                <span style='background-color: rgba(126, 230, 184, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #7EE6B8;'>灵活</span>
                <span style='background-color: rgba(126, 230, 184, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #7EE6B8;'>创新</span>
                <span style='background-color: rgba(126, 230, 184, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #7EE6B8;'>乐观</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="element-card earth-card" style='background: linear-gradient(135deg, rgba(230, 200, 126, 0.1) 0%, rgba(230, 200, 126, 0.05) 100%); 
                    border-radius: 15px; padding: 1.5rem; border: 2px solid rgba(230, 200, 126, 0.2); 
                    transition: all 0.3s ease; cursor: pointer;'>
            <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                <span style='font-size: 2.5rem; margin-right: 1rem;'>🌍</span>
                <h3 style='color: #E6C87E; font-size: 1.4rem;'>土元素</h3>
            </div>
            <p style='color: #666; line-height: 1.6;'>代表稳重、坚守、责任感</p>
            <p style='color: #E6C87E; font-weight: 600; margin-top: 0.5rem;'>团队中可靠的守护者</p>
            <div style='margin-top: 1rem; display: flex; gap: 0.5rem;'>
                <span style='background-color: rgba(230, 200, 126, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #E6C87E;'>踏实</span>
                <span style='background-color: rgba(230, 200, 126, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #E6C87E;'>可靠</span>
                <span style='background-color: rgba(230, 200, 126, 0.2); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; color: #E6C87E;'>负责</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 测试说明（图标展示）
    st.subheader("📋 测试说明")
    instruction_cols = st.columns(4)
    
    with instruction_cols[0]:
        st.markdown("""
        <div class="instruction-card" style='text-align: center; padding: 1.5rem 1rem; background-color: #F8F9FA; border-radius: 12px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📝</div>
            <div style='font-weight: 600; color: #333; margin-bottom: 0.5rem;'>10道题目</div>
            <div style='font-size: 0.9rem; color: #666;'>预计3-5分钟</div>
        </div>
        """, unsafe_allow_html=True)
    
    with instruction_cols[1]:
        st.markdown("""
        <div class="instruction-card" style='text-align: center; padding: 1.5rem 1rem; background-color: #F8F9FA; border-radius: 12px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>💭</div>
            <div style='font-weight: 600; color: #333; margin-bottom: 0.5rem;'>第一反应</div>
            <div style='font-size: 0.9rem; color: #666;'>不要过度思考</div>
        </div>
        """, unsafe_allow_html=True)
    
    with instruction_cols[2]:
        st.markdown("""
        <div class="instruction-card" style='text-align: center; padding: 1.5rem 1rem; background-color: #F8F9FA; border-radius: 12px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>✨</div>
            <div style='font-weight: 600; color: #333; margin-bottom: 0.5rem;'>没有对错</div>
            <div style='font-size: 0.9rem; color: #666;'>只有真实的你</div>
        </div>
        """, unsafe_allow_html=True)
    
    with instruction_cols[3]:
        st.markdown("""
        <div class="instruction-card" style='text-align: center; padding: 1.5rem 1rem; background-color: #F8F9FA; border-radius: 12px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🎁</div>
            <div style='font-weight: 600; color: #333; margin-bottom: 0.5rem;'>专属报告</div>
            <div style='font-size: 0.9rem; color: #666;'>深度人格分析</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 开始测试按钮（带脉冲动画）
    st.markdown("""
    <style>
    .start-btn-wrapper {
        text-align: center;
        padding: 1rem;
    }
    .start-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 4rem;
        font-size: 1.3rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: pulse 2s ease-in-out infinite;
    }
    .start-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    .start-btn:active {
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 使用Streamlit原生按钮，通过CSS美化
    st.markdown('<div class="start-btn-wrapper">', unsafe_allow_html=True)
    if st.button("✨ 开始探索我的炼金身份", key="start_test_button", use_container_width=False):
        st.session_state.visited = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def calc_radio_score(answer):
    """
    计算单选题得分
    
    功能：
    - 根据用户选择的答案，增加对应元素的得分
    
    参数：
        answer (str): 用户选择的答案文本
    """
    # 中文元素名到英文键名的映射
    element_key_map = {
        "火": "fire",
        "水": "water",
        "风": "wind",
        "土": "earth"
    }
    
    for element, options in ELEMENT_OPTIONS.items():
        if answer in options:
            key_suffix = element_key_map.get(element, element)
            st.session_state[f"score_{key_suffix}"] += 1
            break

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
        if st.button("下一题 →", key=f"next_{question_number}"):
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
            if st.button("← 上一题", key=f"prev_{question_number}"):
                st.session_state.current_q = question_number - 1
                st.rerun()
        with col2:
            if st.button("✨ 查看结果", key=f"result_{question_number}"):
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
            if st.button("← 上一题", key=f"prev_{question_number}"):
                st.session_state.current_q = question_number - 1
                st.rerun()
        with col2:
            if st.button("下一题 →", key=f"next_{question_number}"):
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
    渲染结果页面（深度分析版）
    
    功能：
    - 显示用户的元素人格类型
    - 显示详细的元素档案信息
    - 显示各元素得分分布和分析
    - 显示职业建议和人际相处建议
    - 显示答题回顾
    - 提供分享功能
    - 提供重新测试按钮
    
    参数：
        name (str): 用户代号
    """
    # 获取最终元素类型
    element = get_element_result()
    element_info = ELEMENT_INFO[element]
    
    # 显示结果标题（带动画效果）
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {element_info["color"]} 0%, {element_info["color"]}dd 100%); 
                padding: 2.5rem; 
                border-radius: 20px; 
                text-align: center;
                margin-bottom: 2rem;
                animation: fadeInUp 0.6s ease-out;'>
        <h2 style='color: white; margin: 0 0 1rem 0;'>🎉 {name} 的炼金身份揭晓</h2>
        <h1 style='color: white; margin: 0 0 1rem 0; font-size: 2.5rem;'>{ELEMENT_EMOJI[element]} {element_info["name"]}</h1>
        <p style='color: white; font-size: 1.2rem; opacity: 0.95;'>{element_info["desc"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示随机彩蛋
    random_egg = random.choice(element_info["egg"])
    st.success(random_egg)
    
    # 显示得分分布（详细分析）
    st.subheader("📊 元素得分分析")
    scores = {
        "火": st.session_state.score_fire,
        "水": st.session_state.score_water,
        "风": st.session_state.score_wind,
        "土": st.session_state.score_earth
    }
    
    for elem, score in scores.items():
        percentage = (score / TOTAL_QUESTION) * 100
        color = ELEMENT_THEME_COLOR[elem]
        
        # 生成进度条
        st.markdown(f"""
        <div style='margin-bottom: 1rem;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                <span style='font-weight: 600;'>{ELEMENT_EMOJI[elem]} {elem}元素</span>
                <span style='color: {color}; font-weight: 600;'>{score}分 ({percentage:.0f}%)</span>
            </div>
            <div style='height: 20px; background-color: #E8E8E8; border-radius: 10px; overflow: hidden;'>
                <div style='height: 100%; width: {percentage}%; background: linear-gradient(90deg, {color}88, {color}); border-radius: 10px; transition: width 0.5s ease-out;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 添加得分解读
        if percentage >= 70:
            st.markdown(f"  <span style='color: {color};'>🌟</span> 你在{elem}元素上表现突出，这是你的主导特质！", unsafe_allow_html=True)
        elif percentage >= 40:
            st.markdown(f"  <span style='color: {color};'>✨</span> {elem}元素是你的潜在特质，可以进一步发展", unsafe_allow_html=True)
        else:
            st.markdown(f"  <span style='color: #999;'>💡</span> {elem}元素有待发展，尝试多接触相关活动", unsafe_allow_html=True)
    
    st.divider()
    
    # 显示性格特质分析
    st.subheader("🎭 性格特质分析")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ 你的优势
        """)
        for strength in element_info["strengths"]:
            st.markdown(f"- {strength}")
    
    with col2:
        st.markdown("""
        ### ⚠️ 待提升
        """)
        for weakness in element_info["weaknesses"]:
            st.markdown(f"- {weakness}")
    
    st.divider()
    
    # 显示职业建议
    st.subheader("💼 职业适配建议")
    career = CAREER_ADVICE[element]
    st.info(career["reason"])
    st.markdown("**适合你的职业方向：**")
    for idx, advice in enumerate(career["advice"], 1):
        st.markdown(f"{idx}. {advice}")
    
    st.divider()
    
    # 显示人际相处建议
    st.subheader("👥 人际相处小贴士")
    relationship = RELATIONSHIP_ADVICE[element]
    for tip in relationship["advice"]:
        st.markdown(f"- 💡 {tip}")
    
    st.divider()
    
    # 显示学习风格建议
    st.subheader("📚 学习风格分析")
    learning = LEARNING_STYLE[element]
    st.markdown(f"**你的学习风格：** <span style='color: {element_info['color']}; font-weight: 600;'>{learning['style']}</span>", unsafe_allow_html=True)
    st.info(learning['description'])
    st.markdown("**学习建议：**")
    for tip in learning['tips']:
        st.markdown(f"- 📖 {tip}")
    
    st.divider()
    
    # 显示恋爱相处建议
    st.subheader("💕 恋爱相处指南")
    love = LOVE_ADVICE[element]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**恋爱优势：**")
        for strength in love['strengths']:
            st.markdown(f"- ✨ {strength}")
    with col2:
        st.markdown("**匹配元素：**")
        for match_elem in love['match']:
            st.markdown(f"- {ELEMENT_EMOJI[match_elem]} {match_elem}元素")
    st.markdown("**相处小贴士：**")
    for tip in love['tips']:
        st.markdown(f"- 💝 {tip}")
    
    st.divider()
    
    # 显示名人类型参考
    st.subheader("🌟 名人类型参考")
    celebrities = CELEBRITY_REFERENCE[element]
    for celeb in celebrities:
        st.markdown(f"""
        <div style='background-color: #F8F9FA; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;'>
            <strong>{celeb['name']}</strong>
            <p style='color: #666; margin: 0.3rem 0 0 0;'>{celeb['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 显示答题回顾
    with st.expander("📝 答题回顾"):
        for i, answer in enumerate(st.session_state.user_answers):
            if answer:
                st.write(f"**问题{i+1}**: {answer}")
    
    st.divider()
    
    # 分享功能
    st.subheader("📤 分享你的炼金身份")
    
    share_text = f"我在「赛博炼金术士」测试中获得了「{ELEMENT_EMOJI[element]} {element_info['name']}」称号！快来测测你的元素人格吧！"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 复制分享文案按钮
        copy_button_key = f"copy_share_{name}_{element}"
        # 转义分享文本中的特殊字符，确保JavaScript安全
        escaped_share_text = share_text.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        if st.button("📋 复制文案", key=copy_button_key, use_container_width=True):
            # 使用JavaScript实现剪贴板复制
            copy_script = f"""
            <script>
            (function() {{
                navigator.clipboard.writeText("{escaped_share_text}").then(function() {{
                    console.log("Copied!");
                }}).catch(function(err) {{
                    console.error("Failed to copy:", err);
                }});
            }})();
            </script>
            """
            st.markdown(copy_script, unsafe_allow_html=True)
            st.toast("✅ 已复制到剪贴板！", icon="📋")
        
        # 同时提供可复制的文本框作为备选方案
        st.text_area("分享文案", share_text, height=60, key=f"share_text_{name}", disabled=True)
    
    with col2:
        # 生成分享图片（文本形式）
        share_image_text = f"""╔══════════════════════════════╗
║      赛博炼金术士            ║
╚══════════════════════════════╝

    {ELEMENT_EMOJI[element]} {element_info['name']}
    
    {name} 的炼金身份
    
    🔥 火元素: {st.session_state.score_fire}分
    💧 水元素: {st.session_state.score_water}分
    🌪️ 风元素: {st.session_state.score_wind}分
    🌍 土元素: {st.session_state.score_earth}分
    
    {element_info['desc']}
    
    快来测试你的元素人格吧！
"""
        st.download_button(
            "📥 下载结果",
            data=share_image_text,
            file_name=f"{name}_炼金身份测试结果.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # 生成详细版分享报告
        detailed_report = f"""
赛博炼金术士 - 元素人格测试报告
================================

测试者：{name}
测试结果：{ELEMENT_EMOJI[element]} {element_info['name']}

【元素得分分布】
----------------
🔥 火元素：{st.session_state.score_fire}分 ({(st.session_state.score_fire/TOTAL_QUESTION)*100:.0f}%)
💧 水元素：{st.session_state.score_water}分 ({(st.session_state.score_water/TOTAL_QUESTION)*100:.0f}%)
🌪️ 风元素：{st.session_state.score_wind}分 ({(st.session_state.score_wind/TOTAL_QUESTION)*100:.0f}%)
🌍 土元素：{st.session_state.score_earth}分 ({(st.session_state.score_earth/TOTAL_QUESTION)*100:.0f}%)

【人格描述】
-----------
{element_info['desc']}

【性格优势】
-----------
{chr(10).join([f"- {s}" for s in element_info['strengths']])}

【待提升方面】
-------------
{chr(10).join([f"- {w}" for w in element_info['weaknesses']])}

【职业建议】
-----------
{CAREER_ADVICE[element]['reason']}
适合方向：{chr(10).join([f"{i+1}. {a}" for i, a in enumerate(CAREER_ADVICE[element]['advice'])])}

【随机彩蛋】
-----------
{random.choice(element_info['egg'])}

================================
快来测试你的元素人格吧！
            """.strip()
        st.download_button(
            "📄 下载完整报告",
            data=detailed_report,
            file_name=f"{name}_炼金术士完整报告.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.divider()
    
    # 重新测试按钮
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
# 4. CSS样式定义（含动画效果）
# ============================================================================

def render_styles():
    """
    渲染全局CSS样式
    
    功能：
    - 设置全局背景和字体
    - 定义标题和正文的字体大小
    - 优化按钮、单选按钮、输入框等组件样式
    - 添加响应式布局适配（手机和电脑）
    - 添加页面切换动画效果
    """
    css = """
    <style>
    /* 全局背景、字体 */
    html, body, .stApp {
        background-color: #FAF9F6;
        font-family: "Microsoft Yahei", "PingFang SC", sans-serif;
        font-size: 16px !important;
    }

    /* 页面切换动画 */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }

    @keyframes fadeInDown {
        from { 
            opacity: 0; 
            transform: translateY(-20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }

    @keyframes fadeInLeft {
        from { 
            opacity: 0; 
            transform: translateX(-20px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }

    @keyframes fadeInRight {
        from { 
            opacity: 0; 
            transform: translateX(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.6); }
    }

    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateX(-100%); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }

    @keyframes bounceIn {
        0% { 
            opacity: 0; 
            transform: scale(0.3); 
        }
        50% { 
            transform: scale(1.05); 
        }
        70% { 
            transform: scale(0.9); 
        }
        100% { 
            opacity: 1; 
            transform: scale(1); 
        }
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }

    @keyframes ripple {
        0% { 
            transform: scale(0.8); 
            opacity: 1; 
        }
        100% { 
            transform: scale(2.4); 
            opacity: 0; 
        }
    }

    .block-container {
        animation: fadeIn 0.4s ease-out;
    }

    .result-card {
        animation: fadeInUp 0.6s ease-out;
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
        transition: all 0.2s ease;
        min-height: 48px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* 单选按钮样式 */
    .stRadio > div {
        padding: 0.5rem 0;
    }
    .stRadio > div > label {
        font-size: 1.1rem !important;
        padding: 0.75rem;
        border-radius: 10px;
        transition: all 0.2s ease;
        background-color: #F8F9FA;
        margin-bottom: 0.5rem;
    }
    .stRadio > div > label:hover {
        background-color: #E8F5E9;
        transform: translateX(5px);
    }
    .stRadio > div > label[data-baseweb-radio] {
        border: 2px solid transparent;
    }
    .stRadio > div > label[data-baseweb-radio]:has(input:checked) {
        background-color: #E3F2FD;
        border-color: #2196F3;
    }

    /* 输入框样式优化 */
    .stTextInput > div, .stSelectbox > div, .stMultiSelect > div {
        border: 2px solid #E0E0E0 !important;
        border-radius: 10px !important;
        padding: 0.5rem;
        transition: all 0.2s ease;
    }
    .stTextInput > div:focus-within, .stSelectbox > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    .stTextInput input {
        font-size: 1.1rem !important;
    }

    /* 折叠面板样式 */
    .stExpander {
        border: 1px solid #E0E0E0 !important;
        border-radius: 10px !important;
        overflow: hidden;
    }
    .stExpander > button {
        font-size: 1.1rem !important;
        background-color: #F8F9FA;
    }

    /* 进度条样式 */
    div[data-testid="stProgress"] {
        height: 24px !important;
        border-radius: 12px;
        background-color: #E8E8E8;
        overflow: hidden;
    }
    div[data-testid="stProgress"] > div > div {
        border-radius: 12px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.5s ease-out;
    }

    /* 信息提示样式 */
    .stInfo, .stWarning, .stSuccess {
        padding: 1rem !important;
        border-radius: 10px;
        font-size: 1rem !important;
        animation: fadeIn 0.3s ease-out;
    }

    /* Toast通知样式 */
    .stToast {
        border-radius: 10px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
    }

    /* 卡片悬浮效果 */
    .metric-card {
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }

    /* 元素卡片动画效果 */
    .element-card {
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out forwards;
    }
    .element-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }

    /* 火元素卡片特殊效果 */
    .fire-card:hover {
        border-color: #E67E7E !important;
        box-shadow: 0 15px 35px rgba(230, 126, 126, 0.3);
    }

    /* 水元素卡片特殊效果 */
    .water-card:hover {
        border-color: #7EA8E6 !important;
        box-shadow: 0 15px 35px rgba(126, 168, 230, 0.3);
    }

    /* 风元素卡片特殊效果 */
    .wind-card:hover {
        border-color: #7EE6B8 !important;
        box-shadow: 0 15px 35px rgba(126, 230, 184, 0.3);
    }

    /* 土元素卡片特殊效果 */
    .earth-card:hover {
        border-color: #E6C87E !important;
        box-shadow: 0 15px 35px rgba(230, 200, 126, 0.3);
    }

    /* 欢迎页头部动画 */
    .welcome-header {
        animation: fadeInDown 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }

    /* 开始按钮动画 */
    #start-btn {
        animation: pulse 2s ease-in-out infinite, glow 2s ease-in-out infinite;
    }

    /* 指令卡片动画 */
    .instruction-card {
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out forwards;
    }
    .instruction-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    /* 进度条动画 */
    div[data-testid="stProgress"] > div > div {
        border-radius: 12px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.5s ease-out;
    }

    /* 结果卡片动画 */
    .result-card {
        animation: bounceIn 0.6s ease-out;
    }

    /* 得分条动画 */
    .score-bar {
        animation: slideIn 0.5s ease-out;
    }

    /* 按钮点击涟漪效果 */
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s, opacity 0.3s;
        opacity: 0;
    }
    .stButton > button:active::after {
        width: 200px;
        height: 200px;
        opacity: 0;
    }

    /* 单选按钮选中动画 */
    .stRadio > div > label[data-baseweb-radio]:has(input:checked) {
        background-color: #E3F2FD;
        border-color: #2196F3;
        animation: fadeIn 0.2s ease-out;
    }

    /* 页面标题动画 */
    h1 { 
        font-size: 2.2rem !important; 
        font-weight: 700; 
        animation: fadeInDown 0.4s ease-out;
    }

    /* 二级标题动画 */
    h2 { 
        font-size: 1.8rem !important; 
        font-weight: 600; 
        animation: fadeInLeft 0.4s ease-out;
    }

    /* 三级标题动画 */
    h3 { 
        font-size: 1.5rem !important; 
        font-weight: 600; 
        animation: fadeInLeft 0.3s ease-out;
    }

    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%);
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
    3. 判断是否为首次访问，显示引导页或答题页
    4. 显示页面头部和元素档案
    5. 获取用户代号输入
    6. 显示答题进度条
    7. 根据当前题目编号渲染对应题目或结果页面
    """
    # 1. 渲染样式
    render_styles()
    
    # 2. 初始化会话状态
    init_session_state()
    
    # 3. 判断是否显示欢迎页
    if not st.session_state.visited:
        render_welcome_page()
        return
    
    # 4. 显示页面头部
    st.title(PAGE_TITLE)
    st.caption("「当危机降临，你的本能会是什么？」逐题完成问卷，解锁专属炼金身份")
    st.divider()
    
    # 5. 获取用户代号
    name = st.text_input("你的代号是？", placeholder="比如：炼金学徒小A")
    st.divider()
    
    # 代号非空校验
    if not name:
        st.info("请先填写你的代号，再开始答题")
        st.stop()
    
    # 6. 显示答题区域
    st.subheader("⚗️ 炼金试炼问卷")
    
    # 显示进度条
    current_question = st.session_state.current_q
    if current_question <= TOTAL_QUESTION:
        progress = current_question / TOTAL_QUESTION
        st.progress(progress, text=f"答题进度：第{current_question}题 / 共{TOTAL_QUESTION}题")
    st.divider()
    
    # 7. 根据当前题目编号渲染对应内容
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