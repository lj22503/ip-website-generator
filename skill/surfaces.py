"""
Surface Registry — 用途层抽象

Surface = 用户的使用场景/目的，决定用什么组件和模板组合。
Design System = 视觉风格，决定 CSS token 和外观。
Component = 具体 UI 组件（Badge、Card、Timeline 等）。
Template = 具体内容模板（故事线、项目卡片等）。

层级关系：
  Surface（用途） → Design System（视觉） → Component（组件） → Template（内容）
"""

# ============================================================
# Surface Definitions
# ============================================================

SURFACES = {
    # ---- 落地页类 ----
    "landing": {
        "name": "产品落地页",
        "description": "单页产品展示，适合个人 IP、工具、作品推广",
        "modules": ["hero_featured", "about", "skills", "projects", "contact"],
        "nav_order": ["hero_featured", "about", "skills", "projects", "contact"],
        "mood_keywords": ["专业", "简洁", "成果导向"],
        "recommended_designs": ["linear.app", "notion", "vercel", "framer", "apple"],
    },
    # ---- 个人叙事类 ----
    "story": {
        "name": "个人叙事站",
        "description": "故事驱动，适合思想领袖、内容创作者",
        "modules": ["hero_story", "story", "skills", "projects", "contact"],
        "nav_order": ["hero_story", "story", "skills", "projects", "contact"],
        "mood_keywords": ["真实", "有温度", "成长感"],
        "recommended_designs": ["notion", "claude", "airbnb", "miro"],
    },
    # ---- 作品集类 ----
    "portfolio": {
        "name": "作品集",
        "description": "项目展示为主，适合设计师、开发者",
        "modules": ["hero_featured", "about", "skills", "projects", "awards", "contact"],
        "nav_order": ["hero_featured", "about", "skills", "projects", "awards", "contact"],
        "mood_keywords": ["专业", "成果", "技术深度"],
        "recommended_designs": ["linear.app", "figma", "framer", "supabase", "vercel"],
    },
    # ---- 简历类 ----
    "resume": {
        "name": "数字简历",
        "description": "经历和能力为主，适合求职、申请",
        "modules": ["hero_featured", "about", "skills", "projects", "awards", "contact"],
        "nav_order": ["hero_featured", "about", "skills", "projects", "awards", "contact"],
        "mood_keywords": ["专业", "精炼", "可信"],
        "recommended_designs": ["notion", "apple", "stripe", "claude"],
    },
}


# ============================================================
# Component Registry — 可复用 UI 组件
# ============================================================

class Component:
    """组件定义：名称、渲染函数签名、所需 CSS 变量。"""
    def __init__(self, name, html_template="", css_vars=None, description=""):
        self.name = name
        self.html_template = html_template
        self.css_vars = css_vars or []
        self.description = description


COMPONENTS = {
    # ---- 基础组件 ----
    "badge": Component(
        name="Badge",
        description="技能/标签展示的小标签",
        css_vars=["--badge-bg", "--badge-text", "--badge-radius"],
    ),
    "card": Component(
        name="Card",
        description="通用卡片容器",
        css_vars=["--card-bg", "--card-shadow", "--card-radius", "--card-padding"],
    ),
    "timeline": Component(
        name="Timeline",
        description="时间线，用于故事/经历展示",
        css_vars=["--timeline-line", "--timeline-dot"],
    ),
    "cta": Component(
        name="CTA Button",
        description="行动按钮",
        css_vars=["--cta-bg", "--cta-text", "--cta-radius", "--cta-hover"],
    ),
    "nav_link": Component(
        name="Nav Link",
        description="导航链接",
        css_vars=["--nav-link-color", "--nav-link-hover"],
    ),
    # ---- 展示组件 ----
    "hero_label": Component(
        name="Hero Label",
        description="Hero 区块的 intro 标签（如「我是谁」）",
        css_vars=["--label-size", "--label-color", "--label-transform"],
    ),
    "section_title": Component(
        name="Section Title",
        description="区块标题",
        css_vars=["--title-size", "--title-weight", "--title-color"],
    ),
    "project_card": Component(
        name="Project Card",
        description="项目卡片",
        css_vars=["--card-bg", "--card-shadow", "--card-radius"],
    ),
    "skill_category": Component(
        name="Skill Category",
        description="技能分类",
        css_vars=["--skill-cat-name-color"],
    ),
}


# ============================================================
# External Template Assets — 外部模板（MIT License）
# ============================================================

# AI-Animation-Skill 模板元数据（MIT License — github.com/Unclecheng-li/AI-Animation-Skill）
# 实际 HTML 文件路径: templates/ppt-level2/ 系列
EXTERNAL_TEMPLATES = {
    "ppt_level2_series1": {
        "name": "PPT-L2 系列1：VS对比卡",
        "count": 1,
        "use_case": "概念引入、对比",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series1",
        "features": ["VS对比卡片", "SVG流程图"],
    },
    "ppt_level2_series2": {
        "name": "PPT-L2 系列2：层级结构",
        "count": 1,
        "use_case": "概念定义、层级结构",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series2",
        "features": ["13种动画", "多元化布局"],
    },
    "ppt_level2_series3": {
        "name": "PPT-L2 系列3：轻量步骤",
        "count": 3,
        "use_case": "轻量/步骤/极简",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series3",
        "features": ["极简", "最轻量331行"],
    },
    "ppt_level2_series4": {
        "name": "PPT-L2 系列4：案例代码",
        "count": 3,
        "use_case": "案例/实验/代码",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series4",
        "features": ["代码雨动画"],
    },
    "ppt_level2_series5": {
        "name": "PPT-L2 系列5：警示危险",
        "count": 4,
        "use_case": "警示/失败/危险",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series5",
        "features": ["15种动画", "13页"],
    },
    "ppt_level2_series6": {
        "name": "PPT-L2 系列6：架构护栏",
        "count": 4,
        "use_case": "护栏/架构/反馈",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series6",
        "features": ["红绿VS对比"],
    },
    "ppt_level2_series7": {
        "name": "PPT-L2 系列7：追踪Doom",
        "count": 4,
        "use_case": "追踪/上下文/Doom Loop",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series7",
        "features": ["17种动画"],
    },
    "ppt_level2_series8": {
        "name": "PPT-L2 系列8：辩论对比",
        "count": 3,
        "use_case": "辩论/对比/融合",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series8",
        "features": ["30组VS对比"],
    },
    "ppt_level2_series9": {
        "name": "PPT-L2 系列9：总结精炼",
        "count": 3,
        "use_case": "总结/共识/精炼",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-level2/series9",
        "features": ["最精炼5页"],
    },
    "ppt_basic": {
        "name": "PPT 基础模板",
        "count": 4,
        "use_case": "通用演示",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/ppt-basic",
        "features": ["PPT-Generate-3 视觉最佳"],
    },
    "animation_flowchart": {
        "name": "流程图模板",
        "count": 14,
        "use_case": "科普动画、流程说明",
        "source": "AI-Animation-Skill (MIT)",
        "path": "templates/animation",
        "features": ["RNN-3(通用)", "14种主题"],
    },
}


# ============================================================
# Surface × Template 矩阵
# ============================================================

SURFACE_TEMPLATE_MATRIX = {
    "landing": {
        "primary_template": "landing_page",
        "fallback_templates": ["ppt_level2_series3", "ppt_basic"],
        "animation_eligible": True,
    },
    "story": {
        "primary_template": "personal_story",
        "fallback_templates": ["ppt_level2_series2", "ppt_level2_series7"],
        "animation_eligible": True,
    },
    "portfolio": {
        "primary_template": "project_portfolio",
        "fallback_templates": ["ppt_level2_series4", "ppt_level2_series8"],
        "animation_eligible": True,
    },
    "resume": {
        "primary_template": "digital_resume",
        "fallback_templates": ["ppt_level2_series9", "ppt_basic"],
        "animation_eligible": False,
    },
}


# ============================================================
# API Functions
# ============================================================

def get_surface(name: str) -> dict:
    """获取 Surface 定义。"""
    return SURFACES.get(name)


def list_surfaces() -> list:
    """列出所有 Surface。"""
    return [{"id": k, **v} for k, v in SURFACES.items()]


def get_surface_templates(surface_name: str) -> dict:
    """获取某 Surface 对应的模板信息。"""
    matrix = SURFACE_TEMPLATE_MATRIX.get(surface_name, {})
    primary = matrix.get("primary_template", "landing_page")
    fallbacks = matrix.get("fallback_templates", [])

    primary_info = EXTERNAL_TEMPLATES.get(primary, {"name": primary, "source": "built-in"})
    fallback_info = [EXTERNAL_TEMPLATES.get(f, {"name": f, "source": "built-in"}) for f in fallbacks]

    return {
        "surface": surface_name,
        "primary": primary_info,
        "fallbacks": fallback_info,
        "animation_eligible": matrix.get("animation_eligible", False),
    }


def suggest_surface(mood_keywords: list = None, product_type: str = None) -> str:
    """根据关键词或产品类型推荐 Surface。"""
    if product_type in ("landing", "product", "saas"):
        return "landing"
    if product_type in ("story", "narrative", "blog"):
        return "story"
    if product_type in ("portfolio", "designer", "dev"):
        return "portfolio"
    if product_type in ("resume", "cv", "job"):
        return "resume"

    if mood_keywords:
        for kw in mood_keywords:
            kw_lower = kw.lower()
            if any(w in kw_lower for w in ["叙事", "故事", "成长", "真实"]):
                return "story"
            if any(w in kw_lower for w in ["作品", "展示", "技术"]):
                return "portfolio"
            if any(w in kw_lower for w in ["求职", "简历", "经历"]):
                return "resume"
            if any(w in kw_lower for w in ["产品", "推广", "落地"]):
                return "landing"

    return "landing"  # default


def get_component(name: str) -> Component:
    """获取组件定义。"""
    return COMPONENTS.get(name)
