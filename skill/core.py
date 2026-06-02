#!/usr/bin/env python3
"""
Personal IP Website Generator — App Entry Point

Usage:
    python app.py                           # Interactive CLI
    python app.py --design linear.app       # Specify design system
    python app.py --list-designs            # List all design systems
    python app.py --list-surfaces           # List all surfaces (用途层)
    python app.py --list-templates          # List external template assets
    python app.py --demo                    # Generate demo with sample data
    python app.py --preview                 # Preview in browser
    python app.py --product personal_site   # Use personal_site instead of portfolio
    python app.py --surface story           # Choose surface (用途场景)
    python app.py --fetch-templates         # Download external templates
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rendering.renderer import render_page
from rendering.css_builder import build_css, get_spec, DESIGN_SPECS
from design_systems.registry import get_design_system, list_design_systems, get_categories
from modules.registry import get_required_modules, get_optional_modules, get_modules_by_product
from surfaces import (
    get_surface, list_surfaces, suggest_surface,
    SURFACES, EXTERNAL_TEMPLATES
)
from template_registry import list_template_assets, template_count


# ============================================================
# Sample Data
# ============================================================

DEMO_PORTFOLIO = {
    "content": {
        "hero_featured": {
            "title": "把100个失败案例变成方法论的人",
            "subtitle": "产品设计师 | 独立开发者 | 连续创业者",
            "featured_projects": ["Z型人才规划器", "失败博物馆", "日课App"],
        },
        "about": {
            "headline": "专注产品体验设计的6年老鸟，擅长从0到1",
            "bio": """毕业于清华美院，曾在字节、腾讯担任产品设计师。

过去6年，我主导过3个从0到1的产品，服务用户超过500万。但比这些数字更让我兴奋的是——我踩过的那些坑。

100多个失败的项目，每一个都是我亲手埋葬的。正是这些失败，逼着我总结出了一套「失败优先」的设计方法论：先想清楚什么不做，再想清楚做什么。

现在，我用这套方法帮助独立开发者和初创团队，用更少的试错做出更好的产品。""",
        },
        "skills": {
            "categories": [
                {"name": "设计工具", "items": ["Figma", "Sketch", "Framer", "Protopie"]},
                {"name": "专业能力", "items": ["产品策略", "用户体验设计", "设计系统", "用户研究"]},
                {"name": "技术栈", "items": ["React", "TypeScript", "Python", "SQL"]},
            ],
        },
        "projects": {
            "projects": [
                {
                    "title": "Z型人才规划器",
                    "year": "2024",
                    "role": "独立产品设计 + 开发",
                    "background": "发现很多人对自己的人生规划感到迷茫——不是不知道想要什么，而是不知道自己的优势能匹配什么样的机会。",
                    "process": "用3个月时间，访谈了50个职场人，总结出「Z型发展路径」模型，然后独立开发了这款工具。",
                    "outcome": "上线6个月，付费用户超过3000人，ARR突破50万。",
                    "tags": ["产品设计", "独立开发", "Growth"],
                    "url": "https://example.com",
                },
                {
                    "title": "失败博物馆",
                    "year": "2023",
                    "role": "发起人与策展人",
                    "background": "互联网行业对失败讳莫如深。但失败才是最好的老师。",
                    "process": "邀请了50位创业者、设计师、开发者，分享他们最记忆深刻的项目失败。线上展览 + 线下沙龙同步进行。",
                    "outcome": "全网超过100万人参观，成为年度现象级内容IP。",
                    "tags": ["内容IP", "策展", "社区"],
                    "url": "",
                },
            ],
        },
        "contact": {
            "email": "hello@example.com",
            "links": [
                "LinkedIn | https://linkedin.com/in/example",
                "GitHub | https://github.com/example",
            ],
        },
    },
    "selected_modules": ["hero_featured", "about", "skills", "projects", "contact"],
}


DEMO_PERSONAL_SITE = {
    "content": {
        "name": "苏轼",
        "role": "北宋文学家、书画家、政治家",
        "hero_story": {
            "headline": "一蓑烟雨任平生",
            "subtitle": "唐宋八大家 · 苏东坡 · 豪放派词宗",
        },
        "story": {
            "experiences": """苏轼一生历经北宋仁宗、英宗、神宗、哲宗、徽宗五朝，仕途屡起屡落。

早年随父苏洵、弟苏辙进京应试，嘉祐二年（1057年）进士及第，主考官欧阳修叹曰："老夫当避路，放他出一头地也。"

中年因反对王安石变法，自请外任杭州、密州、徐州、湖州。熙宁九年（1077年）黄河决口徐州，苏轼亲率军民筑堤七十余日，保全全城。

元丰三年（1080年），因"乌台诗案"贬黄州任团练副使，躬耕东坡，自号"东坡居士"，完成《易传》《论语说》。

元祐年间还朝，任翰林学士、知制诰，主张校量利害新旧两法，不偏不废。

绍圣元年（1094年）起，远贬惠州、儋州，于儋州开馆授学，培养海南首位举人。""",
            "challenges": """苏轼一生三次贬谪，每每置于死地而后生。

黄州贬谪：四十三岁因"乌台诗案"下狱百余日，几近处死，贬黄州团练副使不得签书公事，人生跌入谷底。

惠州、儋州再贬：年近六旬再被远贬海南儋州，"垂沈渡海"九死南荒，在当时被视为仅次于处死的极刑。

然而苏轼将三次贬谪视为"平生功业"："问汝平生功业，黄州惠州儋州。"逆境中的达观，成为他最动人的人格光辉。""",
            "insights": """苏轼的旷达并非天生，而是一次次与命运博弈后的超脱。

他曾说："吾上可陪玉皇大帝，下可陪卑田院乞儿。"——无论庙堂还是田间，他都能与人真诚相对。

他论画："论画以形似，见与儿童邻。"——不拘形似，重神似，写意，这是中国文人画的理论基础。

他论文："文理自然，姿态横生。"——文章如行云流水，反对雕琢。

他将儒家的入世、道家的旷达、佛家的超脱融为一体，形成了独特的"东坡式"人生哲学：面对命运的不公，既不逃避，也不扭曲，而是以审美的方式超越。""",
            "mbti": "ENFP",
        },
        "about": {
            "subtitle": "关于苏轼",
            "bio": "苏轼是宋代文学最高成就代表，中国文学史上最全面的天才之一。诗、词、文、书、画五绝皆精，散文与欧阳修并称「欧苏」，诗与黄庭坚并称「苏黄」，词与辛弃疾并称「苏辛」，书法为「宋四家」之首。兼擅水利、医药、烹饪、酿酒、养生。一生屡遭贬谪而从不坠志，以旷达超脱的人生态度成为中国文人精神丰碑。",
        },
        "experience": [
            {
                "duration": "1061-1065",
                "role": "大理评事、凤翔签判",
                "company": "凤翔府",
                "location": "陕西凤翔",
                "description": "协助知府处理文书刑狱，改革衙前役法减轻百姓负担，组织修建东湖。",
                "achievements": ["改革衙前役法", "修建东湖"],
            },
            {
                "duration": "1071-1079",
                "role": "通判/知州（杭州/密州/徐州/湖州）",
                "company": "地方州府",
                "location": "杭州、密州、徐州、湖州",
                "description": "自请外任，历任杭州通判、密州知州、徐州知州、湖州知州。徐州抗洪保全全城，湖州到任即因乌台诗案被贬。",
                "achievements": ["徐州抗洪", "密州治蝗收养弃婴", "治理西湖"],
            },
            {
                "duration": "1080-1084",
                "role": "黄州团练副使",
                "company": "黄州",
                "location": "湖北黄冈",
                "description": "因乌台诗案贬黄州，躬耕东坡，自号东坡居士。完成《易传》《论语说》两部学术著作。",
                "achievements": ["躬耕东坡", "完成《易传》《论语说》", "创制东坡肉"],
            },
            {
                "duration": "1089-1091",
                "role": "知州",
                "company": "杭州",
                "location": "浙江杭州",
                "description": "主持疏浚西湖，用淤泥筑成苏堤，建三塔，设立中国第一家公立医院「安乐坊」。",
                "achievements": ["筑苏堤", "疏浚西湖", "建安乐坊"],
            },
            {
                "duration": "1094-1101",
                "role": "贬谪流放",
                "company": "惠州、儋州",
                "location": "广东惠州、海南儋州",
                "description": "远贬惠州、儋州，为广州设计城市自来水系统，推广秧马；在儋州开馆授学，培养海南首位举人。",
                "achievements": ["设计广州自来水系统", "推广秧马", "儋州办学培养姜唐佐"],
            },
        ],
        "education": [
            {
                "duration": "1037-1056",
                "degree": "自幼家学",
                "institution": "眉山家中",
                "description": "父苏洵亲授经史，母程氏以东汉范滂事迹勉励其砥砺名节。幼年于眉山天庆观读书，后拜刘巨门下。",
            },
            {
                "duration": "1056-1057",
                "degree": "进士及第",
                "institution": "汴京",
                "description": "随父苏洵、弟苏辙出川赴京应试，嘉祐二年进士第二（榜眼），复试春秋对义居第一。欧阳修叹曰「出人头地」。",
            },
        ],
        "achievements": [
            {"title": "徐州抗洪", "description": "黄河决口，亲率军民筑堤七十余日，保全全城。建黄楼纪念，后人称「苏黄楼」。", "date": "1077"},
            {"title": "疏浚西湖筑苏堤", "description": "用淤泥筑成长堤，植柳桃，建六桥，今「苏堤春晓」为西湖十景之首。", "date": "1089-1090"},
            {"title": "天下第三行书", "description": "《黄州寒食诗帖》被誉为「天下第三行书」，奠定苏轼「宋四家」之首地位。", "date": "1082"},
            {"title": "儋州办学", "description": "在海南开馆授学，培养海南历史上首位举人姜唐佐，开文化教育先河。", "date": "1098"},
        ],
        "skills": {
            "categories": [
                {"name": "文学创作", "items": ["诗", "词", "散文", "赋", "记", "论", "书", "志"]},
                {"name": "艺术成就", "items": ["行书", "楷书", "枯木怪石画", "文人画理论"]},
                {"name": "政治实务", "items": ["水利工程", "城市供水系统", "抗洪救灾", "变法讨论"]},
                {"name": "生活技艺", "items": ["烹饪（东坡肉/羹）", "酿酒", "养生", "古琴"]},
            ],
            "bars": [
                {"name": "诗词创作", "percentage": 98},
                {"name": "书法绘画", "percentage": 95},
                {"name": "散文成就", "percentage": 97},
                {"name": "政治实务", "percentage": 80},
                {"name": "生活艺术", "percentage": 90},
            ],
        },
        "projects": {
            "projects": [
                {
                    "title": "徐州抗洪（1077年）",
                    "year": "1077",
                    "role": "知徐州",
                    "background": "黄河决口，苏轼「庐于城上，过家不入」，组织五千民夫筑堤抗洪。",
                    "outcome": "堤成，全城保全。朝廷嘉奖，建黄楼纪念。",
                    "tags": ["水利", "抗洪", "政绩"],
                    "url": "#",
                },
                {
                    "title": "杭州苏堤与西湖疏浚",
                    "year": "1089-1090",
                    "role": "知杭州",
                    "background": "用湖底淤泥筑成长堤，建三塔，疏浚西湖，恢复水域生态。",
                    "outcome": "苏堤至今为西湖十景之首，西湖焕然一新。",
                    "tags": ["水利", "市政", "文化遗存"],
                    "url": "#",
                },
                {
                    "title": "《黄州寒食诗帖》",
                    "year": "1082",
                    "role": "书画家",
                    "background": "黄州第三年书写的两首寒食诗，自嘲诗书俱老，情感沉郁顿挫。",
                    "outcome": "被誉为「天下第三行书」，现存于台北故宫博物院。",
                    "tags": ["书法", "诗词", "文人画"],
                    "url": "#",
                },
                {
                    "title": "广州自来水工程",
                    "year": "1094-1096",
                    "role": "惠州贬谪",
                    "background": "建议太守王古用竹管引蒲涧山泉入城，设石槽蓄水，再分引至各坊。",
                    "outcome": "世界最早的城市管道供水系统之一。",
                    "tags": ["市政工程", "技术创新"],
                    "url": "#",
                },
            ],
        },
        "blog": {
            "posts": [
                {"title": "《念奴娇·赤壁怀古》", "date": "1082", "excerpt": "大江东去，浪淘尽，千古风流人物", "url": "#"},
                {"title": "《水调歌头·明月几时有》", "date": "1076", "excerpt": "但愿人长久，千里共婵娟", "url": "#"},
                {"title": "《前赤壁赋》", "date": "1082", "excerpt": "惟江上之清风，与山间之明月，耳得之而为声，目遇之而成色", "url": "#"},
            ],
        },
        "contact": {
            "email": "sudongpo@history.cn",
            "socials": {
                "email": "sudongpo@history.cn",
                "location": "眉州眉山（今四川眉山）",
            },
            "links": [
                "公众号 | 苏东坡研究",
                "知乎专栏 | #",
            ],
        },
        "badges": ["唐宋八大家", "宋四家之首", "豪放派词宗", "文人画开创者"],
        "avatar": "",
        "resume_url": "#",
        "accent_color": "#8b5cf6",
        "accent_secondary": "#f59e0b",
        # Resources dimension
        "resources": {
            "network": [
                {"name": "欧阳修", "role": "恩师/伯乐", "description": "宋代文坛宗主，读苏轼文章后预言「三十年后无人道着我」"},
                {"name": "王安石", "role": "政敌/晚年和解", "description": "虽政治对立，晚年于金陵相逢，赞叹「不知更几百年方有如此人物」"},
                {"name": "黄庭坚", "role": "学生/词友", "description": "与苏轼亦师亦友，并称「苏黄」"},
            ],
            "tools": ["东坡易传", "东坡志林", "东坡酒经", "苏沈良方"],
            "communities": ["元祐党人", "蜀学学派"],
            "influence": ["后世文人精神偶像", "日本汉诗影响深远", "韩国东坡热"],
        },
        # Form dimension
        "testimonials": [
            {"quote": "吾今又为吾子孙得太平宰相两人。", "author": "宋仁宗", "title": "皇帝", "company": "北宋朝廷"},
            {"quote": "老夫当避路，放他出一头地也。", "author": "欧阳修", "title": "主考官", "company": "北宋文坛"},
            {"quote": "不知更几百年，方有如此人物！", "author": "王安石", "title": "宰相", "company": "北宋朝廷"},
            {"quote": "坡公之可爱者，多其不掩性情。", "author": "袁宏道", "title": "明代文人", "company": "明代公安派"},
        ],
        "form": {
            "keywords": ["旷达", "乐天派", "全才", "一蓑烟雨任平生", "千古文人"],
            "style": "豪放中见细腻，逆境中见超脱，学问中见性情",
            "external_presence": ["文学作品", "书法绘画真迹", "苏堤等历史遗迹", "民间美食传说"],
        },
    },
    "selected_modules": ["hero_story", "story", "about", "experience", "education", "skills", "projects", "achievements", "blog", "contact", "resources"],
}


# ============================================================
# Commands
# ==========================================================

def list_designs():
    """List all available design systems."""
    print(f"\n可用设计系统（共{len(DESIGN_SPECS)}套）:\n")
    print(f"{'名称':<20} {'分类':<25} {'描述':<40} {'适用'}")
    print("-" * 100)

    for name, spec in DESIGN_SPECS.items():
        reg = get_design_system(name)
        category = reg.get("category", "") if reg else ""
        desc = reg.get("description", "")[:38] if reg else ""
        mood = reg.get("mood", "")[:18] if reg else ""

        print(f"{name:<20} {category:<25} {desc:<40} {mood}")

    print("\n提示：用 --design <name> 选择设计系统，例：")
    print("  python app.py --design notion --demo")
    print("  python app.py --design linear.app --demo")


def list_surfaces_cmd():
    """List all available surfaces (用途层)."""
    surfaces = list_surfaces()
    print(f"\n可用场景（共{len(surfaces)}种）:\n")
    print(f"{'ID':<15} {'名称':<20} {'描述':<35} {'推荐设计系统'}")
    print("-" * 100)
    for s in surfaces:
        rec = ", ".join(s.get("recommended_designs", [])[:3])
        print(f"{s['id']:<15} {s['name']:<20} {s['description']:<35} {rec}")
    print("\n提示：用 --surface <id> 选择场景，例：")
    print("  python app.py --surface story --design notion --demo")


def list_templates_cmd():
    """List all external template assets."""
    assets = list_template_assets()
    total = template_count()
    print(f"\n外部模板资产（共{len(assets)}类，{total}个文件）:\n")
    print(f"{'ID':<30} {'名称':<30} {'数量':<6} {'使用场景'}")
    print("-" * 90)
    for a in assets:
        print(f"{a['id']:<30} {a['name']:<30} {a.get('count',0):<6} {a.get('use_case','')}")
    print("\n来源: AI-Animation-Skill (MIT License)")
    print("提示: 下载模板: python app.py --fetch-templates")


def generate(args):
    """Generate website."""
    design = args.design
    product = args.product or "portfolio"
    surface = args.surface

    # Surface overrides product and modules
    if surface:
        surface_data = get_surface(surface)
        if surface_data:
            # Surface explicitly sets modules
            selected_modules = surface_data.get("modules", [])
            # Surface suggests product type
            if surface in ("story",):
                demo = DEMO_PERSONAL_SITE
                product = "personal_site"
            else:
                demo = DEMO_PORTFOLIO
                product = "portfolio"
            # Load user content if provided, otherwise use demo
            if args.content:
                with open(args.content, encoding="utf-8") as f:
                    raw = json.load(f)
                    # Support both flat JSON and {"content": {...}} wrapped JSON
                    content = raw.get("content", raw)
            else:
                content = demo["content"]
            print(f"[Surface模式] {surface} | {design} | {product}")
        else:
            print(f"⚠️ 未知 surface: {surface}")
            return
    elif args.demo:
        demo = DEMO_PERSONAL_SITE if product == "personal_site" else DEMO_PORTFOLIO
        content = demo["content"]
        selected_modules = demo["selected_modules"]
        print(f"[Demo模式] 使用 {design} 设计系统生成 {product} ...")
    else:
        # Load content from JSON file if provided
        if args.content:
            with open(args.content, encoding="utf-8") as f:
                raw = json.load(f)
                content = raw.get("content", raw)
        else:
            content = {}
        selected_modules = args.modules.split(",") if args.modules else []

    output_path = args.output or f"/tmp/ip_website_{surface or product}_{design.replace('.', '_')}.html"

    # Multi-template mode: use full Jinja2 template instead of CSS builder
    if args.template:
        from rendering.renderer import render_html_template
        tpl_name = args.template
        # Support both flat JSON and {"content": {...}} wrapped
        # Pass FULL raw JSON so adapter can access top-level name/role
        if args.content:
            with open(args.content, encoding="utf-8") as f:
                raw = json.load(f)
                content = raw  # keep raw so adapter sees name/role at top level
        elif args.demo:
            demo = DEMO_PERSONAL_SITE if product == "personal_site" else DEMO_PORTFOLIO
            content = demo
        else:
            content = {}
        html = render_html_template(tpl_name, content, output_path=output_path)
        size = os.path.getsize(output_path)
        print(f"\n✅ 生成完成: {output_path} ({size:,} bytes)")
        print(f"   模板: {tpl_name}")
        print(f"   (自适应内容数据 → {tpl_name} 专属结构)")
        if args.preview:
            preview(output_path)
        return

    html = render_page(
        design_system=design,
        content=content,
        selected_modules=selected_modules,
        product_type=product,
        surface=surface,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size = os.path.getsize(output_path)
    print(f"\n✅ 生成完成: {output_path} ({size:,} bytes)")
    print(f"   设计系统: {design}")
    print(f"   产品类型: {product}")
    print(f"   模块数量: {len(selected_modules)}")

    if args.preview:
        preview(output_path)


def preview(path: str):
    """Open HTML in browser."""
    import webbrowser
    url = f"file://{path}"
    webbrowser.open(url)
    print(f"浏览器预览: {url}")


def main():
    parser = argparse.ArgumentParser(
        description="Personal IP Website Generator — 作品集 or 个人网站生成器"
    )
    parser.add_argument("--design", "-d", default="notion",
                        help="设计系统名称（默认: notion）")
    parser.add_argument("--product", "-p", default=None,
                        choices=["portfolio", "personal_site"],
                        help="产品类型（默认: portfolio）")
    parser.add_argument("--list-designs", "-l", action="store_true",
                        help="列出所有设计系统")
    parser.add_argument("--list-surfaces", action="store_true",
                        help="列出所有用途场景（Surface）")
    parser.add_argument("--list-templates", action="store_true",
                        help="列出外部模板资产")
    parser.add_argument("--demo", action="store_true",
                        help="使用示例数据生成演示网站")
    parser.add_argument("--surface", "-s", default=None,
                        choices=["landing", "story", "portfolio", "resume"],
                        help="选择用途场景（Surface）")
    parser.add_argument("--fetch-templates", action="store_true",
                        help="下载外部模板资产（AI-Animation-Skill MIT）")
    parser.add_argument("--output", "-o",
                        help="输出HTML路径（默认: /tmp/ip_website_*.html）")
    parser.add_argument("--content", "-c",
                        help="内容JSON文件路径")
    parser.add_argument("--modules",
                        help="逗号分隔的模块列表（覆盖默认顺序）")
    parser.add_argument("--preview", action="store_true",
                        help="生成后浏览器预览")
    parser.add_argument("--template", "-t", default=None,
                        choices=["developerfolio", "alfolio", "rahulbeniwal"],
                        help="使用完整HTML模板（多套不同页面结构）")

    args = parser.parse_args()

    if args.list_designs:
        list_designs()
        return

    if args.list_surfaces:
        list_surfaces_cmd()
        return

    if args.list_templates:
        list_templates_cmd()
        return

    if args.fetch_templates:
        from fetch_templates import download_all
        print("开始下载外部模板资产...")
        download_all()
        return

    if args.demo or args.content:
        generate(args)
    else:
        # Default: run interactive CLI
        from cli import interactive_mode
        interactive_mode()


if __name__ == "__main__":
    main()
