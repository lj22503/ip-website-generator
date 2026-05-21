#!/usr/bin/env python3
"""
Personal IP Website Generator — App Entry Point

Usage:
    python app.py                           # Interactive CLI
    python app.py --design linear.app      # Specify design system
    python app.py --list-designs            # List all design systems
    python app.py --demo                    # Generate demo with sample data
    python app.py --preview                 # Preview in browser
    python app.py --product personal_site    # Use personal_site instead of portfolio
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
        "hero_story": {
            "headline": "我用3年时间，把副业收入超过了主业",
            "subtitle": "前字节产品经理 | 独立开发者 | 知识炼金士",
        },
        "story": {
            "experiences": """2019年，我从字节离职。带着一个判断：未来的工作形态是「一人公司」。

这3年，我做过50个项目。其中：
- 3个项目做到了月入过万
- 12个项目中途夭折
- 剩下的35个，默默死在了文件夹里。""",
            "challenges": """最大的挑战不是做产品，而是和自己对抗。

当副业收入开始超过主业，我开始怀疑自己是不是在逃避职场。当副业也失败，我发现自己在害怕成功。

每一个失败的项目，都像一面镜子，照出了我性格里的某种缺陷。""",
            "insights": """我学到了一件事：失败不是成功之母，失败是成功之母——的前提是你愿意直视它。

把失败写成文档，不是为了记录，是为了理解自己为什么会这样决策。

然后有一天，我突然明白：我不是在创业，我是在通过创业这件事，把自己变成一个更完整的人。""",
            "mbti": "INTJ",
        },
        "skills": {
            "categories": [
                {"name": "产品能力", "items": ["产品策略", "用户增长", "数据驱动"]},
                {"name": "技术实现", "items": ["React", "Python", "AI应用"]},
                {"name": "内容创作", "items": ["写作", "播客", "视频"]},
            ],
        },
        "projects": {
            "projects": [
                {
                    "title": "副业收入追踪器",
                    "year": "2024",
                    "role": "独立开发",
                    "background": "自己需要追踪多个副业收入，顺便做了一个给自己用。",
                    "outcome": "帮助超过5000人追踪副业财务状况。",
                    "tags": ["SaaS", "独立开发"],
                    "url": "",
                },
            ],
        },
        "blog": {
            "posts": [
                {
                    "title": "为什么我不建议你做「一人公司」",
                    "date": "2024-11-15",
                    "excerpt": "独立工作的自由是真的，但孤独也是真的。这是我3年后才想明白的事。",
                    "url": "#",
                },
            ],
        },
        "contact": {
            "email": "hello@example.com",
            "links": [
                "Twitter | https://twitter.com/example",
                "小宇宙 | https://xiaoyuzhoufm.com/example",
            ],
        },
    },
    "selected_modules": ["hero_story", "story", "skills", "projects", "blog", "contact"],
}


# ============================================================
# Commands
# ==========================================================

def list_designs():
    """List all available design systems."""
    print("\n可用设计系统（共{}套）:\n".format(len(DESIGN_SPECS)))
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


def generate(args):
    """Generate website."""
    design = args.design
    product = args.product or "portfolio"

    # Build content from args or demo
    if args.demo:
        demo = DEMO_PERSONAL_SITE if product == "personal_site" else DEMO_PORTFOLIO
        content = demo["content"]
        selected_modules = demo["selected_modules"]
        print(f"[Demo模式] 使用 {design} 设计系统生成 {product} ...")
    else:
        # Load content from JSON file if provided
        if args.content:
            with open(args.content) as f:
                content = json.load(f)
        else:
            content = {}
        selected_modules = args.modules.split(",") if args.modules else []

    output_path = args.output or f"/tmp/ip_website_{design.replace('.', '_')}.html"

    html = render_page(
        design_system=design,
        content=content,
        selected_modules=selected_modules,
        product_type=product,
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
    parser.add_argument("--demo", action="store_true",
                        help="使用示例数据生成演示网站")
    parser.add_argument("--output", "-o",
                        help="输出HTML路径（默认: /tmp/ip_website_*.html）")
    parser.add_argument("--content", "-c",
                        help="内容JSON文件路径")
    parser.add_argument("--modules",
                        help="逗号分隔的模块列表（覆盖默认顺序）")
    parser.add_argument("--preview", action="store_true",
                        help="生成后浏览器预览")

    args = parser.parse_args()

    if args.list_designs:
        list_designs()
        return

    if args.demo or args.content:
        generate(args)
    else:
        # Default: run interactive CLI
        from cli import interactive_mode
        interactive_mode()


if __name__ == "__main__":
    main()
