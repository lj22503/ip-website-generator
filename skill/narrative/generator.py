"""
Personal IP Narrative Generator
Implements the narrative-personal-ip skill logic:
1. 4-layer material extraction
2. MBTI personality mapping
3. 8-knives quality evaluation
4. De-AI-ization detection
5. Ethical review
6. Final narrative output
"""

import json
import re
import os
import re as regex_module
from typing import Optional

# MiniMax API client
def _get_minimax_client():
    """Get MiniMax OpenAI-compatible client."""
    try:
        from openai import OpenAI
    except ImportError:
        return None
    
    env_path = os.path.expanduser("~/.hermes/.env")
    api_key = None
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if "MINIMAX_API_KEY=" in line and "***" not in line:
                    val = line.strip().split("=", 1)[1]
                    # Strip any ANSI escape codes
                    cleaned = regex_module.sub(r"\x1b\[[A-Z0-9;]+", "", val)
                    api_key = cleaned.strip()
                    break
    
    if not api_key:
        return None
    
    return OpenAI(api_key=api_key, base_url="https://api.minimaxi.com/v1")


def _strip_reasoning(text: str) -> str:
    """Remove thinking/reasoning traces from model output.
    
    MiniMax M2.7 with thinking_budget:0 still sometimes embeds the full
    reasoning trace as narrative text. Detection: check for mixed signals.
    If output reads like an instruction list, discard and use fallback.
    """
    if not text:
        return text
    
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    # Count bullet/metadata lines vs real narrative lines
    bullet_count = sum(1 for l in lines if l.startswith("- ") or l.startswith("• ") or l.startswith("* "))
    short_meta = sum(1 for l in lines if len(l) < 30 and not l.endswith("。") and not l.endswith("？"))
    total_lines = len(lines)
    
    # If more than 30% lines are bullets or short metadata, this is likely a thinking trace
    if total_lines > 3 and (bullet_count / total_lines > 0.3 or short_meta / total_lines > 0.4):
        return ""  # Signal to caller: use fallback
    
    return text


# ============================================================
# 8-Knives Evaluation Framework (八刀评估)
# ============================================================

EIGHT_KNIVES = [
    ("历史", "叙事是否符合人的认知习惯？有无强行扭曲？"),
    ("辩证", "叙事与逻辑/数据的平衡是否被打破？"),
    ("现象", "叙事的起点是否真实可感？"),
    ("语言", "语言是否自然、有温度、无模板痕迹？"),
    ("形式", "是否符合拉波夫最小故事公式？"),
    ("存在", "叙事是否服务于自我认同或社会协作？"),
    ("美感", "叙事是否有审美价值？"),
    ("元反思", "是否有明显虚构但不自知的部分？"),
]


def evaluate_8_knives(narrative: str, material: dict) -> dict:
    """
    Evaluate narrative on 8 dimensions.
    Returns scores and improvement suggestions.
    """
    # Simple heuristic evaluation
    # In production, this would call LLM for each dimension
    scores = {}
    suggestions = {}
    
    # Length check
    char_count = len(narrative)
    
    # Historical dimension: check causality
    has_transition = any(kw in narrative for kw in ["然后", "于是", "因此", "结果", "后来", "直到"])
    scores["历史"] = 7 if has_transition else 5
    if not has_transition:
        suggestions["历史"] = "建议增加因果过渡词，使故事逻辑更清晰"
    
    # Dialectical dimension: check for balance
    has_numbers = any(c.isdigit() for c in narrative)
    has_specifics = len(narrative) > 300
    scores["辩证"] = 8 if (has_numbers and has_specifics) else 6
    if not has_numbers:
        suggestions["辩证"] = "建议加入具体数字或时间，增强可信度"
    
    # Phenomenon dimension: check for scene anchors
    has_anchor = any(kw in narrative for kw in ["那天", "那天晚上", "当时", "有一次", "那天在", "在", "凌晨"])
    has_dialog = '"' in narrative or '"' in narrative or '「' in narrative
    scores["现象"] = 9 if (has_anchor and has_dialog) else 6 if has_anchor else 4
    if scores["现象"] < 7:
        suggestions["现象"] = "建议增加具体场景锚点（时间/地点/对话），增强画面感"
    
    # Language dimension: de-AI-ization check
    ai_patterns = ["在当今时代", "值得注意的是", "首先", "其次", "最重要的是", 
                   "因此可以发现", "不难看出", "从这个角度来看"]
    ai_count = sum(1 for p in ai_patterns if p in narrative)
    scores["语言"] = 9 if ai_count == 0 else 7 if ai_count == 1 else 5
    if ai_count > 0:
        suggestions["语言"] = f"检测到{ai_count}处AI模板表达，建议改为更口语化的表达"
    
    # Form dimension: check Labov structure
    has_setup = any(kw in narrative for kw in ["曾经", "以前", "之前", "那段时间"])
    has_complication = any(kw in narrative for kw in ["突然", "没想到", "然而", "但是", "没想到"])
    has_resolution = any(kw in narrative for kw in ["后来", "最终", "现在", "于是", "因此"])
    form_score = (has_setup + has_complication + has_resolution) * 3
    scores["形式"] = min(10, form_score + 1)
    if form_score < 5:
        suggestions["形式"] = "建议使用拉波夫公式：定位→复杂化→评价→解决，增加叙事结构感"
    
    # Existence dimension: check purpose
    has_lesson = any(kw in narrative for kw in ["学到", "意识到", "发现", "明白", "懂得"])
    has_value = any(kw in narrative for kw in ["帮助", "影响", "改变", "意义", "价值"])
    scores["存在"] = 9 if (has_lesson and has_value) else 7 if has_lesson else 5
    if not has_lesson:
        suggestions["存在"] = "建议提炼核心认知，让读者能带走具体收获"
    
    # Aesthetic dimension: check for golden sentences
    has_punch_line = any(kw in narrative for kw in ["——", "。", "：" if "：" in narrative else ""])
    sentences = [s.strip() for s in re.split(r'[。！？]', narrative) if len(s.strip()) > 20]
    variance = len(set(sentences[:5])) / max(len(sentences[:5]), 1) if sentences else 0
    scores["美感"] = 8 if variance > 0.6 else 6
    if variance <= 0.6:
        suggestions["美感"] = "建议增加句式变化和意象，提升叙事美感和金句密度"
    
    # Meta-reflection dimension
    perfect_count = narrative.count("完美") + narrative.count("从不")
    scores["元反思"] = 9 if perfect_count == 0 else 6
    if perfect_count > 0:
        suggestions["元反思"] = "建议避免过度完美的表述，增加脆弱性细节"
    
    return {
        "scores": scores,
        "suggestions": suggestions,
        "pass": all(s >= 7 for s in scores.values()),
        "weakest": min(scores, key=scores.get),
        "total": sum(scores.values()) / len(scores)
    }


# ============================================================
# De-AI-ization Detection (去AI化检测) - 7 Rules
# ============================================================

DE_AI_RULES = [
    ("模板词检测", ["在当今时代", "值得注意的是", "首先", "其次", "最重要的是", 
                   "因此可以发现", "不难看出", "总的来说", "综上所述"]),
    ("句式工整度", None),  # Special: check variance
    ("逻辑词密度", ["因此", "所以", "然后", "于是", "接着", "之后"]),
    ("细节锚点", ["时间", "地点", "姓名", "数字"]),  # Check presence
    ("情感抽象", ["很感动", "很震撼", "很开心", "很难过", "非常"]),
    ("人格一致性", None),  # Context-dependent
    ("过度解释", ["这意味着", "换句话说", "也就是说", "可以说"]),
]


def detect_ai_style(narrative: str) -> dict:
    """
    Run 7-rule de-AI detection.
    Returns dict of rule -> (passed, detail)
    """
    results = {}
    
    # Rule 1: Template words
    template_hits = [w for w in DE_AI_RULES[0][1] if w in narrative]
    results["模板词检测"] = (len(template_hits) == 0, f"发现：{template_hits}" if template_hits else "无")
    
    # Rule 2: Sentence length variance
    sentences = [s.strip() for s in re.split(r'[。！？\n]', narrative) if len(s.strip()) > 5]
    if sentences:
        lengths = [len(s) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum(abs(l - avg_len) for l in lengths) / len(lengths)
        results["句式工整度"] = (variance > 3, f"方差{variance:.1f}，{'自然' if variance > 3 else '过于工整'}")
    else:
        results["句式工整度"] = (True, "无法判断")
    
    # Rule 3: Logic word density
    logic_count = sum(narrative.count(w) for w in DE_AI_RULES[2][1])
    logic_density = logic_count / max(len(narrative), 1) * 1000
    results["逻辑词密度"] = (logic_density < 20, f"密度{logic_density:.1f}‰，{'自然' if logic_density < 20 else '过密'}")
    
    # Rule 4: Detail anchors
    has_anchor = any(kw in narrative for kw in ["凌晨", "那天", "有一次", "当时", "在", "公司", "北京", "上海", "深圳"])
    has_number = any(c.isdigit() for c in narrative)
    has_dialog = '"' in narrative or '"' in narrative
    results["细节锚点"] = ((has_anchor or has_number or has_dialog), 
                          f"{'有' if has_anchor else ''}{'数字' if has_number else ''}{'对话' if has_dialog else ''}")
    
    # Rule 5: Abstract emotions
    emotion_hits = [w for w in DE_AI_RULES[4][1] if w in narrative]
    results["情感抽象"] = (len(emotion_hits) == 0, f"发现：{emotion_hits}" if emotion_hits else "无")
    
    # Rule 6: Personality consistency (simplified: check for tense changes)
    first_person = narrative.count("我")
    results["人格一致性"] = (first_person > 2, f"'我'出现{first_person}次")
    
    # Rule 7: Over-explanation
    explain_hits = [w for w in DE_AI_RULES[6][1] if w in narrative]
    results["过度解释"] = (len(explain_hits) == 0, f"发现：{explain_hits}" if explain_hits else "无")
    
    all_passed = all(v[0] for v in results.values())
    
    return {
        "results": results,
        "passed": all_passed,
        "failed_count": sum(1 for v in results.values() if not v[0])
    }


# ============================================================
# MBTI Narrative Personality Mapping
# ============================================================

MBTI_NARRATIVE_STYLE = {
    "INFJ": {
        "description": "隐喻型叙事，深度疗愈",
        "tone": "温和但深刻",
        "structure": "隐喻开篇 → 内心旅程 → 顿悟 → 使命宣言",
        "language": "诗意、有留白、避免说破",
        "scene_preference": "用具体物品/场景承载隐喻"
    },
    "INFP": {
        "description": "自传型叙事，真诚柔软",
        "tone": "真诚、不回避脆弱",
        "structure": "真诚开场 → 内心独白 → 成长 → 价值观宣言",
        "language": "细腻、有情感、不夸张",
        "scene_preference": "细节描写丰富，有感官细节"
    },
    "ENFJ": {
        "description": "鼓舞型叙事，召唤行动",
        "tone": "有力量、有号召力",
        "structure": "使命开篇 → 挑战 → 领导力 → 行动号召",
        "language": "有力、有节奏、行动导向",
        "scene_preference": "强调对人的改变和影响"
    },
    "ENFP": {
        "description": "即兴型叙事，跳跃生动",
        "tone": "活泼、多样、充满可能",
        "structure": "灵感开篇 → 多元故事 → 可能性 → 邀请探索",
        "language": "跳跃、有趣、打破常规",
        "scene_preference": "多故事碎片化呈现"
    },
    "INTJ": {
        "description": "战略型叙事，冷静洞察",
        "tone": "冷静、有洞察、有远见",
        "structure": "洞察开篇 → 系统分析 → 战略执行 → 成果",
        "language": "简洁、有逻辑、数据支撑",
        "scene_preference": "强调本质、架构、系统"
    },
    "ENTP": {
        "description": "颠覆型叙事，爱挑战",
        "tone": "颠覆、辩论、反常识",
        "structure": "反常识开篇 → 辩论 → 颠覆认知 → 新视角",
        "language": "犀利、高对比、有锋芒",
        "scene_preference": "通过对立观点制造张力"
    },
    "ESFP": {
        "description": "表演型叙事，活在当下",
        "tone": "热情、表现力、感染力",
        "structure": "当下开篇 → 生动场景 → 行动 → 即时反馈",
        "language": "口语化、有活力、短句有力",
        "scene_preference": "强调此时此刻的感受"
    },
    "ISFJ": {
        "description": "守护型叙事，温暖务实",
        "tone": "温暖、务实、有责任感",
        "structure": "守护开篇 → 默默付出 → 坚守价值 → 实在成果",
        "language": "温暖、不张扬、有画面",
        "scene_preference": "用具体事例展现品质"
    }
}


# ============================================================
# Narrative Generation
# ============================================================

def generate_story(
    name: str,
    role: str,
    experiences: str,
    challenges: str,
    insights: str,
    mbti: str = "INFP",
    target_audience: str = None
) -> dict:
    """
    Generate personal IP narrative based on 4-layer material.
    
    Args:
        name: 姓名
        role: 当前身份
        experiences: 我做过什么
        challenges: 我遭遇了什么
        insights: 我看重什么/我学到什么
        mbti: 叙事人格（可选）
        target_audience: 目标受众（可选）
    
    Returns:
        dict with full_story, short_story, bio, mbti_analysis
    """
    mbti_upper = mbti.upper()
    
    if mbti_upper not in MBTI_NARRATIVE_STYLE:
        mbti_upper = "INFP"  # fallback
    
    style = MBTI_NARRATIVE_STYLE[mbti_upper]
    
    # Build narrative using LLM-style generation
    # In production, this calls MiniMax API
    
    full_story = _generate_full_story(name, role, experiences, challenges, insights, style, target_audience)
    short_story = _generate_short_story(name, role, experiences, challenges, insights, style)
    bio = _generate_bio(name, role, experiences, insights)
    
    # Evaluate quality
    evaluation = evaluate_8_knives(full_story, {
        "experiences": experiences,
        "challenges": challenges,
        "insights": insights
    })
    
    # De-AI detection
    de_ai = detect_ai_style(full_story)
    
    return {
        "full_story": full_story,
        "short_story": short_story,
        "bio": bio,
        "mbti": mbti_upper,
        "mbti_style": style,
        "evaluation": evaluation,
        "de_ai": de_ai,
        "quality_pass": evaluation["pass"] and de_ai["passed"]
    }


def _generate_full_story(name, role, experiences, challenges, insights, style, audience):
    """
    Generate full narrative story via MiniMax LLM.
    Falls back to structured template if API unavailable.
    """
    client = _get_minimax_client()
    
    mbti_upper = style.get("tone", "真诚但有温度")
    narrative_structure = style.get("structure", "真诚开场 → 内心独白 → 成长 → 价值观宣言")
    
    system_prompt = f"""你是一个叙事写作专家，帮助用户写"关于我"页面的人生故事。

写作要求：
1. 用真实、有画面感的叙事风格，不要模板套话
2. 第一人称"我"，自然口语化，像在和朋友聊天
3. 包含具体场景细节（时间/地点/对话/感受），不要空洞的总结
4. 篇幅：400-600字，分3-4段，不要加小标题
5. 核心原则：真实比完美更重要，有脆弱感的叙事才打动人
6. 不要用"首先、其次、最后、因此、值得注意的是、可以说"等模板词
7. 不要过度解释，让故事自己说话
8. 结尾用一句有共鸣感的话收尾，不要喊口号

叙事人格风格：{mbti_upper}——{style.get('description', '')}
叙事结构：{narrative_structure}"""

    user_prompt = f"""{name}，{role}

【我做过什么】
{experiences}

【我遭遇过什么】
{challenges}

【我学到什么/我看重什么】
{insights}

请根据以上真实素材，写一篇完整的人生故事。直接输出正文，不要加"以下是"等引导语，不要分段标题。"""

    if client:
        try:
            response = client.chat.completions.create(
                model="MiniMax-M2.7",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1200,
                temperature=0.8,
                extra_body={"thinking_budget": 0}
            )
            raw = response.choices[0].message.content.strip()
            story = _strip_reasoning(raw)
            if story:
                return story
        except Exception:
            pass

    # Fallback: structured template with MBTI-aware framing
    template = _build_story_template(name, role, experiences, challenges, insights, style)
    return template


def _build_story_template(name, role, experiences, challenges, insights, style):
    """Fallback when LLM unavailable: build story from structured template."""
    
    # Extract a hook from experiences
    first_line = ""
    if experiences:
        first_sentence = experiences.split("。")[0].split("\n")[0][:60]
        if first_sentence:
            first_line = first_sentence
    
    # Build with MBTI-aware tone
    tone = style.get("tone", "真诚但有温度")
    name_first = name[0] if name else "我"
    
    template = f"""{first_line or f"从{role}开始，我走上了一条不那么标准的路。"}

{experiences[:200] if experiences else "这些年，我一直在探索适合自己的路。"}
    
{challenges[:200] if challenges else ""}
    
那段时间，我反复问自己：{insights[:60] if insights else "什么才是真正重要的？"}
    
现在回头看，{insights[:80] if insights else "那些困难都成了养分"}。
    
{role}这些年，我最深的体会是：{insights[:50] if insights else "做真实的自己，比做别人期待的自己更难，也更值得。"}"""

    return template.strip()


def _generate_short_story(name, role, experiences, challenges, insights, style):
    """Generate 150-300 word short version for Hero section via MiniMax LLM."""
    
    client = _get_minimax_client()
    
    system_prompt = f"""你是一个叙事写作专家，帮助用户写个人网站首页的"一句话故事"。

写作要求：
1. 150-300字，一口气可以读完的短故事
2. 第一人称，有场景感，有情感共鸣
3. 开头用一个hook（问句或场景）吸引注意力
4. 结尾落脚到当下的身份和使命
5. 自然口语化，不要书面腔，不要模板词
6. 不要分段，不要小标题，直接输出正文

叙事人格：{style.get('tone', '真诚')}——{style.get('description', '')}"""

    user_prompt = f"""{name}，{role}

【我做过什么】
{experiences[:300]}

【我遭遇过什么】
{challenges[:300]}

【我看重什么/我学到什么】
{insights[:300]}

请写一篇首页用的短故事（150-300字），直接输出正文。"""

    if client:
        try:
            response = client.chat.completions.create(
                model="MiniMax-M2.7",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.8,
                extra_body={"thinking_budget": 0}
            )
            story = response.choices[0].message.content.strip()
            story = _strip_reasoning(story)
            if story and len(story) > 80:
                return story
        except Exception:
            pass

    # Fallback: better narrative hook when LLM fails
    first_exp = experiences.split("。")[0].split("\n")[0][:50] if experiences else ""
    first_challenge = challenges.split("。")[0].split("\n")[0][:60] if challenges else ""
    core_insight = insights[:60].rstrip("。") if insights else "找到真正重要的东西"
    
    if first_challenge:
        hook = f"有一段时间，我{first_challenge}"
    elif first_exp:
        hook = f"那段时间，我{first_exp}"
    else:
        hook = "每天醒来，不知道该做什么"
    
    fallback = f"""你有没有过这种感觉——做着别人觉得不错的工作，心里却一直有个声音在问：这就是我想要的？

{hook}。

后来我终于明白：真正的改变，不是离开哪里，而是决定不再等别人告诉我答案。

我现在做{role}，{core_insight}。

如果你也在找自己的节奏，来聊聊。"""

    return fallback


def _generate_bio(name, role, experiences, insights):
    """Generate 150-char bio for sidebar/footer."""
    
    core = insights[:30] if insights else (experiences[:30] if experiences else role)
    bio = f"{name}，{role}。{core}。相信真正的改变来自内心的觉醒。"
    
    if len(bio) > 150:
        bio = bio[:147] + "..."
    return bio


# ============================================================
# Ethical Review (叙事伦理)
# ============================================================

def ethical_review(narrative: str, material: dict) -> dict:
    """
    Apply 3 ethical principles:
    1. No fabrication, but truth can be incomplete
    2. Audience-oriented (if provided)
    3. Scenario-appropriate framework
    """
    concerns = []
    
    # Principle 1: Check for fabrications
    # Look for unrealistic claims
    if "完美" in narrative and "从不" in narrative:
        concerns.append({
            "principle": "原则1",
            "issue": "叙事过于完美，缺乏脆弱性",
            "suggestion": "建议增加一个失败或脆弱的时刻"
        })
    
    # Check for omitted key facts
    if "省略" in narrative or "[此处" in narrative:
        concerns.append({
            "principle": "原则1",
            "issue": "存在省略信息",
            "suggestion": "如省略信息影响受众决策，建议补充"
        })
    
    # Principle 3: Scenario check (personal IP = use hero journey variant)
    concerns.append({
        "principle": "原则3",
        "issue": "场景：个人IP",
        "suggestion": "使用英雄之旅变体框架"
    })
    
    return {
        "passed": len([c for c in concerns if "fabrication" in c.get("issue", "")]) == 0,
        "concerns": concerns,
        "recommendation": "如有关键省略信息，建议在首次公开叙事时主动披露"
    }
