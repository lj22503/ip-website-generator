"""
Template Asset Registry — 外部模板资产注册表

来源：AI-Animation-Skill (MIT License)
github.com/Unclecheng-li/AI-Animation-Skill

格式：每条记录 = {name, path, source, license, content_type, use_case, features, mood}
"""

from pathlib import Path
from surfaces import EXTERNAL_TEMPLATES

# ============================================================
# 模板资产注册表
# ============================================================

# 实际模板文件应放在 templates/ 目录下
TEMPLATE_BASE = Path(__file__).parent.parent / "templates"


def list_template_assets():
    """列出所有已注册的外部模板资产。"""
    results = []
    for key, meta in EXTERNAL_TEMPLATES.items():
        results.append({
            "id": key,
            **meta,
        })
    return results


def get_template_by_id(template_id: str) -> dict:
    """按 ID 获取模板元数据。"""
    return EXTERNAL_TEMPLATES.get(template_id)


def get_template_path(template_id: str) -> Path:
    """获取模板文件的磁盘路径。"""
    meta = EXTERNAL_TEMPLATES.get(template_id)
    if not meta:
        return None
    rel_path = meta.get("path", "")
    full_path = TEMPLATE_BASE / rel_path
    return full_path if full_path.exists() else None


def load_template_html(template_id: str) -> str:
    """加载模板 HTML 文件内容。"""
    path = get_template_path(template_id)
    if path and path.exists():
        if path.is_dir():
            # 目录：尝试找 index.html 或 README
            index = path / "index.html"
            if index.exists():
                return index.read_text(encoding="utf-8")
        else:
            return path.read_text(encoding="utf-8")
    return ""  # 模板文件不存在时返回空字符串，调用方应提供 fallback


def template_count() -> int:
    """返回已注册模板总数。"""
    return sum(meta.get("count", 0) for meta in EXTERNAL_TEMPLATES.values())


# ============================================================
# Skill 模板格式（参考 html-anything 的 75 Skills 格式）
# ============================================================

# 用途分类（参考 html-anything 的 9 Surface）
SKILL_SURFACES = [
    "magazine_article",   # 杂志文章
    "keynote_deck",       # 演示幻灯片
    "resume",              # 简历
    "poster",              # 海报
    "xiaohongshu",         # 小红书
    "tweet_card",         # 社交卡片
    "web_prototype",      # 网页原型
    "data_report",        # 数据报告
    "landing_page",       # 落地页
]

# 格式分类（参考 html-anything 的 Skill 分类）
SKILL_CATEGORIES = [
    "web_prototype",
    "deck_presentation",
    "social_card",
    "office_operations",
]

# 内置 Skill 模板（扩展用）
BUILTIN_SKILLS = [
    {
        "id": "personal_site_story",
        "name": "个人叙事站",
        "surface": "story",
        "category": "web_prototype",
        "description": "故事驱动的个人网站，以叙事为核心",
        "modules": ["hero_story", "story", "skills", "projects", "contact"],
        "mood": "真实、有温度、成长感",
        "designs": ["notion", "claude", "airbnb"],
    },
    {
        "id": "personal_site_landing",
        "name": "产品落地页",
        "surface": "landing",
        "category": "web_prototype",
        "description": "单页产品/个人IP展示页",
        "modules": ["hero_featured", "about", "skills", "projects", "contact"],
        "mood": "专业、简洁、成果导向",
        "designs": ["linear.app", "vercel", "framer"],
    },
    {
        "id": "portfolio_grid",
        "name": "作品集网格",
        "surface": "portfolio",
        "category": "web_prototype",
        "description": "项目展示为主的作品集",
        "modules": ["hero_featured", "about", "skills", "projects", "awards", "contact"],
        "mood": "专业、成果、技术深度",
        "designs": ["figma", "linear.app", "supabase"],
    },
    {
        "id": "digital_resume",
        "name": "数字简历",
        "surface": "resume",
        "category": "web_prototype",
        "description": "经历和能力为主的数字简历",
        "modules": ["hero_featured", "about", "skills", "projects", "awards", "contact"],
        "mood": "专业、精炼、可信",
        "designs": ["apple", "notion", "stripe"],
    },
]
