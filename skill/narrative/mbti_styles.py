"""
MBTI-driven HTML style definitions for personal IP website generator.
Each MBTI type has a distinct visual personality mapped to CSS properties.
"""

MBTI_STYLES = {
    "INFJ": {
        "name": "隐喻型",
        "description": "文学感、留白、深度疗愈",
        "primary_color": "#1a2744",       # 深蓝
        "secondary_color": "#f5f0e8",      # 米白
        "accent_color": "#8b9dc3",        # 淡紫蓝
        "text_color": "#2c3e50",
        "bg_color": "#faf8f5",
        "font_heading": "Georgia, 'Noto Serif SC', serif",
        "font_body": "'Noto Serif SC', Georgia, serif",
        "layout": "centered",             # 居中布局，大量留白
        "hero_align": "center",
        "card_style": "minimal",          # 卡片风格：无边框、柔和阴影
        "spacing": "generous",            # 间距：宽松
        "decorative": "quote_marks",      # 装饰元素：引号、线条
        "animation": "subtle_fade",
        "personality_traits": ["内省", "理想主义", "洞察力", "坚定"],
    },
    "INFP": {
        "name": "自传型",
        "description": "真诚温柔、柔和细腻",
        "primary_color": "#6b5b7a",       # 淡紫灰
        "secondary_color": "#fef6f0",      # 暖白
        "accent_color": "#d4a5a5",        # 淡粉
        "text_color": "#3d3d3d",
        "bg_color": "#fff9f5",
        "font_heading": "'LXGW WenKai', 'Noto Serif SC', serif",
        "font_body": "'LXGW WenKai', 'Noto Serif SC', sans-serif",
        "layout": "centered",
        "hero_align": "center",
        "card_style": "soft_shadow",
        "spacing": "relaxed",
        "decorative": "handwritten_note",
        "animation": "soft_rise",
        "personality_traits": ["真诚", "同理心", "创造力", "内省"],
    },
    "ENFJ": {
        "name": "鼓舞型",
        "description": "有号召力、行动导向",
        "primary_color": "#c0392b",       # 深红
        "secondary_color": "#fff8f0",      # 暖白
        "accent_color": "#e67e22",        # 橙色
        "text_color": "#2c2c2c",
        "bg_color": "#ffffff",
        "font_heading": "'Noto Sans SC', sans-serif",
        "font_body": "'Noto Sans SC', sans-serif",
        "layout": "full_width",           # 全宽布局
        "hero_align": "left",
        "card_style": "bold_border",
        "spacing": "balanced",
        "decorative": "bold_lines",
        "animation": "slide_up",
        "personality_traits": ["同理心", "感染力", "责任感", "魅力"],
    },
    "ENFP": {
        "name": "即兴型",
        "description": "活泼跳跃、碎片化创意",
        "primary_color": "#8e44ad",       # 紫色
        "secondary_color": "#fef9e7",      # 淡黄
        "accent_color": "#27ae60",        # 绿色
        "text_color": "#2c3e50",
        "bg_color": "#fffdf7",
        "font_heading": "'Noto Sans SC', sans-serif",
        "font_body": "'Noto Sans SC', sans-serif",
        "layout": "asymmetric",           # 不对称布局
        "hero_align": "left",
        "card_style": "colorful_border",
        "spacing": "varied",
        "decorative": "color_blocks",
        "animation": "playful_bounce",
        "personality_traits": ["热情", "创意", "洞察力", "适应力"],
    },
    "INTJ": {
        "name": "战略型",
        "description": "冷静、结构化、逻辑清晰",
        "primary_color": "#1a1a2e",       # 深墨
        "secondary_color": "#f8f9fa",     # 冷白
        "accent_color": "#4a90d9",        # 冷蓝
        "text_color": "#1a1a2e",
        "bg_color": "#fafbfc",
        "font_heading": "'JetBrains Mono', 'Noto Sans SC', monospace",
        "font_body": "'Noto Sans SC', 'Inter', sans-serif",
        "layout": "structured_grid",      # 结构化网格
        "hero_align": "left",
        "card_style": "grid_card",
        "spacing": "compact",
        "decorative": "geometric_lines",
        "animation": "crisp_fade",
        "personality_traits": ["独立", "战略思维", "高标准", "理性"],
    },
    "ENTP": {
        "name": "颠覆型",
        "description": "颠覆感、高对比、话题感",
        "primary_color": "#e74c3c",       # 红色
        "secondary_color": "#1a1a1a",      # 黑色
        "accent_color": "#f39c12",        # 黄色
        "text_color": "#1a1a1a",
        "bg_color": "#ffffff",
        "font_heading": "'Noto Sans SC', sans-serif",
        "font_body": "'Noto Sans SC', sans-serif",
        "layout": "bold_contrast",        # 高对比
        "hero_align": "left",
        "card_style": "dark_card",
        "spacing": "balanced",
        "decorative": "diagonal_stripes",
        "animation": "sharp_slide",
        "personality_traits": ["创新", "辩论力", "好奇心", "魅力"],
    },
    "ESFP": {
        "name": "表演型",
        "description": "热情、视觉系、图片为主",
        "primary_color": "#e91e63",       # 粉色
        "secondary_color": "#fff176",      # 明黄
        "accent_color": "#00bcd4",        # 青色
        "text_color": "#2c2c2c",
        "bg_color": "#ffffff",
        "font_heading": "'Noto Sans SC', sans-serif",
        "font_body": "'Noto Sans SC', sans-serif",
        "layout": "visual_heavy",         # 图片为主
        "hero_align": "full",
        "card_style": "photo_card",
        "spacing": "tight",
        "decorative": "emoji_dots",
        "animation": "bouncy_entry",
        "personality_traits": ["热情", "表现力", "活在当下", "魅力"],
    },
    "ISFJ": {
        "name": "守护型",
        "description": "温暖、叙事性强、柔和",
        "primary_color": "#5d6d7e",       # 灰蓝
        "secondary_color": "#fdf5e6",      # 米色
        "accent_color": "#cd853f",        # 棕色
        "text_color": "#3d3d3d",
        "bg_color": "#fdfaf5",
        "font_heading": "'Noto Serif SC', Georgia, serif",
        "font_body": "'Noto Serif SC', Georgia, serif",
        "layout": "narrative_flow",       # 叙事流
        "hero_align": "center",
        "card_style": "warm_card",
        "spacing": "relaxed",
        "decorative": "flourish_border",
        "animation": "gentle_fade",
        "personality_traits": ["可靠", "忠诚", "务实", "守护"],
    },
}


def get_style(mbti_type: str) -> dict:
    """Get style definition for a given MBTI type."""
    mbti = mbti_type.upper()
    if mbti not in MBTI_STYLES:
        # Default to INFP if unknown
        return MBTI_STYLES["INFP"]
    return MBTI_STYLES[mbti]


def generate_css(style: dict, mbti_type: str) -> str:
    """Generate CSS code for a given MBTI style."""
    
    layout = style.get("layout", "centered")
    
    base = f"""
/* ============================================
   {mbti_type} - {style['name']} 风格
   描述：{style['description']}
   核心特质：{' '.join(style['personality_traits'])}
   ============================================ */

:root {{
    --primary: {style['primary_color']};
    --secondary: {style['secondary_color']};
    --accent: {style['accent_color']};
    --text: {style['text_color']};
    --bg: {style['bg_color']};
    --font-heading: {style['font_heading']};
    --font-body: {style['font_body']};
}}

/* 重置基础样式 */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    line-height: 1.8;
    -webkit-font-smoothing: antialiased;
}}

/* 标题字体 */
h1, h2, h3 {{
    font-family: var(--font-heading);
    font-weight: 700;
    line-height: 1.3;
    color: var(--primary);
}}

/* ===== 布局系统 ===== */
"""

    if layout == "centered":
        base += """
.container { max-width: 720px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: center; padding: 80px 0 60px; }
"""
    elif layout == "full_width":
        base += """
.container { max-width: 1100px; margin: 0 auto; padding: 0 32px; }
.hero { text-align: left; padding: 100px 0 80px; }
"""
    elif layout == "asymmetric":
        base += """
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 80px 0 60px; }
.hero-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 48px; align-items: center; }
"""
    elif layout == "structured_grid":
        base += """
.container { max-width: 960px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 60px 0 40px; }
.grid-section { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
"""
    elif layout == "bold_contrast":
        base += """
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 60px 0 40px; border-left: 6px solid var(--primary); padding-left: 32px; }
"""
    elif layout == "visual_heavy":
        base += """
.container { max-width: 100%; padding: 0; }
.hero { text-align: left; padding: 0; }
.hero-full { width: 100%; height: 70vh; background: var(--primary); }
"""
    elif layout == "narrative_flow":
        base += """
.container { max-width: 680px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: center; padding: 100px 0 80px; }
"""
    else:
        base += """
.container { max-width: 960px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 60px 0 40px; }
"""

    # Animations
    anim = style.get("animation", "subtle_fade")
    if anim == "subtle_fade":
        anim_css = """
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: fadeInUp 0.6s ease-out forwards; }
"""
    elif anim == "soft_rise":
        anim_css = """
@keyframes softRise { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: softRise 0.8s ease-out forwards; }
"""
    elif anim == "slide_up":
        anim_css = """
@keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: slideUp 0.5s ease-out forwards; }
"""
    elif anim == "playful_bounce":
        anim_css = """
@keyframes playfulBounce { 0% { opacity: 0; transform: translateY(20px); } 60% { transform: translateY(-8px); } 100% { opacity: 1; transform: translateY(0); } }
.animate-in { animation: playfulBounce 0.6s ease-out forwards; }
"""
    elif anim == "crisp_fade":
        anim_css = """
@keyframes crispFade { from { opacity: 0; } to { opacity: 1; } }
.animate-in { animation: crispFade 0.4s ease-out forwards; }
.section { opacity: 0; }
.section.visible { animation: crispFade 0.5s ease-out forwards; }
"""
    elif anim == "sharp_slide":
        anim_css = """
@keyframes sharpSlide { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
.animate-in { animation: sharpSlide 0.4s ease-out forwards; }
"""
    elif anim == "bouncy_entry":
        anim_css = """
@keyframes bouncyEntry { 0% { opacity: 0; transform: scale(0.95); } 70% { transform: scale(1.02); } 100% { opacity: 1; transform: scale(1); } }
.animate-in { animation: bouncyEntry 0.5s ease-out forwards; }
"""
    else:
        anim_css = """
@keyframes gentleFade { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: gentleFade 0.7s ease-out forwards; }
"""

    base += anim_css

    # Hero section
    spacing = style.get("spacing", "balanced")
    spacing_val = {"generous": "48px 0", "relaxed": "36px 0", "balanced": "32px 0", "compact": "24px 0", "varied": "24px 0", "tight": "16px 0"}.get(spacing, "32px 0")

    base += f"""
/* ===== Hero ===== */
.hero-name {{
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.02em;
    margin-bottom: 8px;
    font-family: var(--font-heading);
}}
.hero-role {{
    font-size: 1.1rem;
    color: var(--accent);
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: {spacing_val};
}}
.hero-story {{
    font-size: 1.15rem;
    line-height: 2;
    color: var(--text);
    max-width: 600px;
    margin: 0 auto;
    opacity: 0.9;
}}
"""

    # Section styles
    base += """
/* ===== 通用Section ===== */
.section { padding: 60px 0; }
.section-title { 
    font-size: 1.8rem; 
    margin-bottom: 32px; 
    position: relative;
    display: inline-block;
}
"""

    # Card styles
    card = style.get("card_style", "minimal")
    if card == "minimal":
        base += """
.card { 
    background: transparent;
    padding: 24px 0;
    border: none;
    box-shadow: none;
}
"""
    elif card == "soft_shadow":
        base += """
.card {
    background: var(--secondary);
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
"""
    elif card == "bold_border":
        base += """
.card {
    background: var(--secondary);
    padding: 28px;
    border-left: 4px solid var(--primary);
}
"""
    elif card == "grid_card":
        base += """
.card {
    background: white;
    padding: 24px;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
}
"""
    elif card == "warm_card":
        base += """
.card {
    background: var(--secondary);
    padding: 28px;
    border-radius: 12px;
    border: 1px solid rgba(205,133,63,0.2);
}
"""
    else:
        base += """
.card {
    background: white;
    padding: 24px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
"""

    # Decorative elements
    deco = style.get("decorative", "quote_marks")
    if deco == "quote_marks":
        base += """
.quote-block {
    position: relative;
    padding: 0 32px;
    margin: 24px 0;
}
.quote-block::before {
    content: '"';
    font-size: 4rem;
    color: var(--accent);
    position: absolute;
    left: 0;
    top: -10px;
    font-family: Georgia, serif;
    opacity: 0.4;
}
"""
    elif deco == "bold_lines":
        base += """
.section-title::after {
    content: '';
    display: block;
    width: 48px;
    height: 3px;
    background: var(--primary);
    margin-top: 12px;
}
"""
    elif deco == "flourish_border":
        base += """
.section-title {
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8px;
}
"""

    # Footer
    base += """
/* ===== Footer ===== */
.footer {
    text-align: center;
    padding: 40px 0;
    border-top: 1px solid rgba(0,0,0,0.08);
    font-size: 0.85rem;
    color: #888;
}
.footer a { color: var(--accent); text-decoration: none; }
"""

    return base


def recommend_mbti_from_content(name: str, role: str, experiences: str, 
                                  challenges: str, insights: str) -> dict:
    """
    Recommend MBTI type based on content analysis.
    Returns: {"mbti": "INFJ", "reason": "..."}
    """
    # This is a simple heuristic-based recommendation
    # In production, this would call an LLM
    
    combined = f"{experiences} {challenges} {insights}".lower()
    
    # High-level strategic keywords
    strategic_kw = ["战略", "系统", "架构", "模型", "框架", "分析", "逻辑", "规划", "长期", "本质"]
    creative_kw = ["创意", "灵感", "感受", "体验", "直觉", "可能", "想象", "探索", "可能"]
    social_kw = ["帮助", "团队", "他人", "影响", "连接", "赋能", "激励", "带领", "沟通"]
    intro_kw = ["独自", "独立", "反思", "沉淀", "深度", "内向", "安静"]
    action_kw = ["行动", "执行", "快", "立即", "现在", "落地", "实践"]
    vision_kw = ["愿景", "未来", "使命", "意义", "价值", "长远", "改变世界"]
    detail_kw = ["细节", "具体", "精确", "扎实", "务实", "一步一步"]
    
    scores = {k: 0 for k in ["INTJ", "INFJ", "ENFJ", "ENFP", "INFP", "ENTP", "ESFP", "ISFJ"]}
    
    for kw in strategic_kw:
        if kw in combined:
            scores["INTJ"] += 1
            scores["ENTP"] += 1
    for kw in creative_kw:
        if kw in combined:
            scores["INFP"] += 1
            scores["ENFP"] += 1
    for kw in social_kw:
        if kw in combined:
            scores["ENFJ"] += 1
            scores["ISFJ"] += 1
    for kw in intro_kw:
        if kw in combined:
            scores["INFJ"] += 1
            scores["INTJ"] += 1
            scores["ISFJ"] += 1
    for kw in action_kw:
        if kw in combined:
            scores["ESFP"] += 1
            scores["ENTP"] += 1
    for kw in vision_kw:
        if kw in combined:
            scores["ENFJ"] += 1
            scores["INFJ"] += 1
    for kw in detail_kw:
        if kw in combined:
            scores["ISFJ"] += 1
            scores["INTJ"] += 1
    
    # Length heuristic
    if len(combined) > 500:
        scores["INFJ"] += 1
        scores["INTJ"] += 1
    if len(combined) < 200:
        scores["ESFP"] += 1
        scores["ENFP"] += 1
    
    best_mbti = max(scores, key=scores.get)
    max_score = scores[best_mbti]
    
    if max_score == 0:
        # Default fallback
        best_mbti = "INFP"
    
    reasons = {
        "INFJ": "内容中体现深度思考、使命感和对人性的洞察，适合INFJ隐喻型叙事风格",
        "INTJ": "内容中展现战略思维和逻辑架构能力，适合INTJ冷静结构化风格",
        "ENFJ": "内容中强调对人的影响和使命感，适合ENFJ鼓舞型叙事风格",
        "ENFP": "内容中体现创意、多样性和可能性，适合ENFP即兴跳跃风格",
        "INFP": "内容中流露真诚、价值观和对意义的追寻，适合INFP自传型叙事风格",
        "ENTP": "内容中展现颠覆性和辩论思维，适合ENTP高对比风格",
        "ESFP": "内容中体现行动力和表现力，适合ESFP视觉表演型风格",
        "ISFJ": "内容中展现务实、守护和叙事性，适合ISFJ温暖叙事流风格",
    }
    
    return {
        "mbti": best_mbti,
        "reason": reasons.get(best_mbti, "综合判断推荐"),
        "all_scores": scores
    }
