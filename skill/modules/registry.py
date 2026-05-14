"""
Content Module Registry
Defines all modules for Portfolio and Personal Brand Site products.
Modules are solidified, with optional ones clearly marked.
"""

# ============================================================
# Field Schemas
# ============================================================

class Field:
    """Field definition for a module."""
    def __init__(self, name: str, label: str, field_type: str = "text",
                 required: bool = False, hint: str = "", options: list = None):
        self.name = name
        self.label = label
        self.type = field_type  # text / textarea / image / url / email / select / tags / list
        self.required = required
        self.hint = hint
        self.options = options or []


# ============================================================
# Module Definitions
# ============================================================

PORTFOLIO_MODULES = {
    # ---- 核心必选模块 ----
    "hero_featured": {
        "name": "精选封面",
        "name_en": "Featured Hero",
        "description": "视觉冲击力强的封面，展示最得意的1-3个项目",
        "required": True,
        "cardinality": "one",
        "fields": [
            Field("title", "标题", "text", required=True,
                  hint="例：把100个失败案例变成方法论的人"),
            Field("subtitle", "副标题", "text", required=True,
                  hint="例：产品设计师 | 独立开发者 | 连续创业者"),
            Field("cover_image", "封面图", "image", required=False,
                  hint="强烈建议上传，比例建议16:9或4:3"),
            Field("featured_projects", "精选项目", "tags", required=False,
                  hint="从下方作品案例中选择1-3个作为精选，填入项目标题"),
        ],
    },
    "about": {
        "name": "关于我",
        "name_en": "About",
        "description": "专业背景、设计理念、个人特点",
        "required": True,
        "cardinality": "one",
        "fields": [
            Field("headline", "一句话介绍", "text", required=True,
                  hint="例：专注产品体验设计的6年老鸟，擅长从0到1"),
            Field("bio", "详细介绍", "textarea", required=True,
                  hint="你的专业背景、核心能力和独特优势（建议200-400字）"),
            Field("photo", "个人照片", "image", required=False,
                  hint="建议使用真实照片，增加信任感"),
        ],
    },
    "skills": {
        "name": "技能",
        "name_en": "Skills",
        "description": "分门别类列出工具和专业能力",
        "required": True,
        "cardinality": "one",
        "fields": [
            Field("categories", "技能分类", "list", required=True,
                  hint="每个分类：名称 + 技能项列表。例：设计工具（Figma, Sketch, PS）"),
        ],
    },
    "projects": {
        "name": "作品/项目",
        "name_en": "Projects",
        "description": "每个案例含背景、你的角色、过程、最终成果",
        "required": True,
        "cardinality": "multiple",  # 可以添加多个
        "fields": [
            Field("title", "项目名称", "text", required=True),
            Field("year", "年份", "text", required=False,
                  hint="例：2024"),
            Field("role", "我的角色", "text", required=True,
                  hint="例：主导产品设计，独立开发"),
            Field("background", "项目背景", "textarea", required=True,
                  hint="这个项目要解决什么问题？为什么做？"),
            Field("process", "我的过程", "textarea", required=False,
                  hint="你是怎么做的？核心挑战和解决方案"),
            Field("outcome", "最终成果", "textarea", required=True,
                  hint="上线后的效果：数据、获奖、用户反馈等"),
            Field("images", "项目图片", "image", required=False,
                  hint="上传1-4张项目相关图片"),
            Field("tags", "技术/标签", "tags", required=False,
                  hint="例：Figma, React, 用户增长"),
            Field("url", "项目链接", "url", required=False,
                  hint="线上地址或GitHub链接"),
        ],
    },
    "contact": {
        "name": "联系",
        "name_en": "Contact",
        "description": "方便客户或雇主联系",
        "required": True,
        "cardinality": "one",
        "fields": [
            Field("email", "邮箱", "email", required=True),
            Field("links", "社交链接", "list", required=False,
                  hint="格式：平台名称 + 链接。例：LinkedIn | GitHub | 微信公众号"),
        ],
    },

    # ---- 可选模块 ----
    "awards": {
        "name": "荣誉/奖项",
        "name_en": "Awards",
        "description": "行业奖项、媒体报道",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("title", "奖项名称", "text", required=True),
            Field("year", "年份", "text", required=False),
            Field("issuer", "颁发机构", "text", required=False),
            Field("description", "说明", "textarea", required=False),
        ],
    },
    "clients": {
        "name": "客户/合作伙伴",
        "name_en": "Clients",
        "description": "合作过的知名品牌",
        "required": False,
        "cardinality": "one",
        "fields": [
            Field("clients", "客户/合作方", "list", required=True,
                  hint="品牌名称列表，例：字节跳动、阿里巴巴、腾讯"),
        ],
    },
    "testimonials": {
        "name": "推荐信/评价",
        "name_en": "Testimonials",
        "description": "客户或同事的真实评价",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("quote", "评价内容", "textarea", required=True),
            Field("author", "评价人", "text", required=True),
            Field("title", "职位/身份", "text", required=False),
            Field("company", "公司", "text", required=False),
        ],
    },
    "social": {
        "name": "社交链接",
        "name_en": "Social Links",
        "description": "GitHub、小红书、微博等社交媒体",
        "required": False,
        "cardinality": "one",
        "fields": [
            Field("links", "链接列表", "list", required=True,
                  hint="格式：平台名称 + 链接URL"),
        ],
    },
    "resume": {
        "name": "简历下载",
        "name_en": "Resume",
        "description": "提供PDF简历下载",
        "required": False,
        "cardinality": "one",
        "fields": [
            Field("resume_file", "简历PDF", "file", required=True,
                  hint="上传PDF格式简历"),
            Field("resume_text", "简历链接文字", "text", required=False,
                  hint="默认文字：下载简历"),
        ],
    },
}


PERSONAL_SITE_MODULES = {
    # 继承全部作品集模块
    **{k: v.copy() if isinstance(v, dict) else v for k, v in PORTFOLIO_MODULES.items()},

    # ---- 核心替换/增强模块 ----
    "story": {
        "name": "我的故事",
        "name_en": "My Story",
        "description": "叙事化的个人故事（雕龙叙事引擎驱动）",
        "required": True,
        "cardinality": "one",
        "mbti_driven": True,  # 叙事引擎驱动
        "fields": [
            Field("experiences", "我做过什么", "textarea", required=True,
                  hint="具体经历：做了什么、产出了什么。尽量真实具体"),
            Field("challenges", "我遭遇过什么", "textarea", required=True,
                  hint="真实困境和挑战，比成就更打动人心"),
            Field("insights", "我看重什么/学到什么", "textarea", required=True,
                  hint="核心认知和价值观，这是故事的终点"),
            Field("mbti", "MBTI类型", "select", required=False,
                  options=["INTJ", "INFJ", "ENFJ", "ENFP", "ENTP", "ESFP", "ISFJ", "INFP"],
                  hint="不填=自动根据内容推断"),
        ],
    },
    "hero_story": {
        "name": "故事封面",
        "name_en": "Story Hero",
        "description": "用故事吸引访客，一句话让别人记住你",
        "required": True,
        "cardinality": "one",
        "fields": [
            Field("headline", "金句/Hook", "text", required=True,
                  hint="一句话让别人记住你。例：我用3年时间，把副业收入超过了主业"),
            Field("subtitle", "身份/标签", "text", required=True,
                  hint="例：前字节产品经理 | 独立开发者 | 知识炼金士"),
            Field("hero_image", "封面图", "image", required=False,
                  hint="建议用真实场景照片或精心设计的视觉"),
        ],
    },

    # ---- 扩展可选模块 ----
    "blog": {
        "name": "博客/文章",
        "name_en": "Blog",
        "description": "行业见解、教程、生活随笔",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("title", "文章标题", "text", required=True),
            Field("date", "发布日期", "text", required=False),
            Field("excerpt", "摘要", "textarea", required=False),
            Field("content", "正文", "textarea", required=False,
                  hint="支持Markdown格式"),
            Field("cover_image", "封面图", "image", required=False),
            Field("tags", "标签", "tags", required=False),
            Field("url", "原文链接", "url", required=False),
        ],
    },
    "life": {
        "name": "生活瞬间",
        "name_en": "Life",
        "description": "旅行、兴趣爱好，让形象更立体",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("title", "标题", "text", required=True),
            Field("description", "描述", "textarea", required=False),
            Field("images", "照片", "image", required=False,
                  hint="可上传多张"),
            Field("tags", "标签", "tags", required=False),
        ],
    },
    "gallery": {
        "name": "相册/影音",
        "name_en": "Gallery",
        "description": "摄影作品、歌单或视频创作",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("title", "标题", "text", required=True),
            Field("type", "类型", "select", required=True,
                  options=["photo", "music", "video"]),
            Field("media", "媒体文件", "file", required=False),
            Field("url", "外部链接", "url", required=False,
                  hint="Spotify/网易云/YouTube等"),
            Field("description", "描述", "textarea", required=False),
        ],
    },
    "services": {
        "name": "服务/商店",
        "name_en": "Services",
        "description": "咨询、设计服务或周边产品",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("title", "服务名称", "text", required=True),
            Field("description", "服务描述", "textarea", required=True),
            Field("price", "价格/说明", "text", required=False),
            Field("cta", "行动按钮文字", "text", required=False,
                  hint="例：预约咨询"),
            Field("cta_url", "行动链接", "url", required=False),
        ],
    },
    "newsletter": {
        "name": " Newsletter订阅",
        "name_en": "Newsletter",
        "description": "邮件订阅，建立长期连接",
        "required": False,
        "cardinality": "one",
        "fields": [
            Field("headline", "订阅引导语", "text", required=False,
                  hint="例：每周一篇深度思考，和你一起进化"),
            Field("placeholder", "输入框占位文字", "text", required=False,
                  hint="例：你的邮箱"),
            Field("cta", "按钮文字", "text", required=False,
                  hint="例：订阅"),
        ],
    },
    "podcast": {
        "name": "播客/视频",
        "name_en": "Podcast / Video",
        "description": "音频或视频内容专栏",
        "required": False,
        "cardinality": "multiple",
        "fields": [
            Field("title", "标题", "text", required=True),
            Field("platform", "平台", "select", required=False,
                  options=["小宇宙", "喜马拉雅", "Spotify", "YouTube", "Bilibili"]),
            Field("url", "链接", "url", required=True),
            Field("description", "描述", "textarea", required=False),
            Field("cover_image", "封面", "image", required=False),
        ],
    },
}


def get_module(product_type: str, module_name: str) -> dict:
    """Get module definition by product type and module name."""
    registry = {
        "portfolio": PORTFOLIO_MODULES,
        "personal_site": PERSONAL_SITE_MODULES,
    }.get(product_type, {})
    return registry.get(module_name)


def get_modules_by_product(product_type: str) -> dict:
    """Get all modules for a product type."""
    return {
        "portfolio": PORTFOLIO_MODULES,
        "personal_site": PERSONAL_SITE_MODULES,
    }.get(product_type, {})


def get_required_modules(product_type: str) -> list:
    """Get list of required module names for a product type."""
    modules = get_modules_by_product(product_type)
    return [name for name, mod in modules.items() if mod.get("required")]


def get_optional_modules(product_type: str) -> list:
    """Get list of optional module names for a product type."""
    modules = get_modules_by_product(product_type)
    return [name for name, mod in modules.items() if not mod.get("required")]
