#!/usr/bin/env python3
"""
验证脚本：测试三个模板的渲染

使用方法：
    python verify_templates.py

这个脚本：
1. 加载 test_data_all_fields.json（全字段测试数据）
2. 对每个模板运行 data_adapter
3. 用 Jinja2 渲染 template.html
4. 验证输出包含关键内容（不报错）
"""

import json
import sys
import os
from pathlib import Path

# 确保可以导入项目模块
sys.path.insert(0, str(Path(__file__).parent))

from modules.data_adapter import to_developerfolio, to_alfolio, to_rahulbeniwal


def load_test_data():
    """加载全字段测试数据"""
    test_data_path = Path(__file__).parent / "test_data_all_fields.json"
    with open(test_data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_template(template_name: str) -> str:
    """加载模板 HTML"""
    template_path = Path(__file__).parent / "html_templates" / template_name / "template.html"
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_template(template_html: str, data: dict) -> str:
    """用 Jinja2 渲染模板"""
    try:
        from jinja2 import Template
        template = Template(template_html)
        return template.render(data=data)
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


def verify_developerfolio():
    """验证 developerfolio 模板"""
    print("\n" + "=" * 60)
    print("测试 developerfolio")
    print("=" * 60)

    test_data = load_test_data()
    template_html = load_template("developerfolio")
    adapted = to_developerfolio(test_data)
    rendered = render_template(template_html, {"data": adapted})

    # 检查关键内容
    checks = [
        ("name=苏轼", "苏轼" in rendered),
        ("title存在", "北宋文学家" in rendered or "书画家" in rendered),
        ("hero_story headline", "一蓑烟雨" in rendered),
        ("about section", "关于我" in rendered),
        ("skills section", "技能" in rendered),
        ("experience section", "职业经历" in rendered),
        ("education section", "教育背景" in rendered),
        ("projects section", "项目作品" in rendered),
        ("achievements section", "荣誉成就" in rendered),
        ("contact section", "联系我" in rendered),
        ("mbti传递", "ENFP" in rendered),
        ("timeline数据", "experiences_paragraphs" in str(adapted) or "timeline" in adapted),
        ("testimonials传递", "testimonials" in adapted),
        ("resources传递", "resources" in adapted),
        ("framework_items传递", "framework_items" in adapted),
        ("stats传递", "stats" in adapted),
    ]

    passed = 0
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
        if result:
            passed += 1

    # 检查是否有 Jinja2 错误
    if "ERROR:" in rendered:
        print(f"  ❌ 渲染错误: {rendered[:200]}")
        passed = 0
    else:
        print(f"  ✅ 渲染成功，输出长度: {len(rendered)} bytes")

    return passed, len(checks)


def verify_alfolio():
    """验证 alfolio 模板"""
    print("\n" + "=" * 60)
    print("测试 alfolio")
    print("=" * 60)

    test_data = load_test_data()
    template_html = load_template("alfolio")
    adapted = to_alfolio(test_data)
    rendered = render_template(template_html, {"data": adapted})

    checks = [
        ("name=苏轼", "苏轼" in rendered),
        ("sidebar存在", "sidebar" in rendered.lower() or "关于我" in rendered),
        ("about section", "关于我" in rendered),
        ("skills section", "技能" in rendered),
        ("experience section", "职业经历" in rendered),
        ("projects section", "项目作品" in rendered),
        ("contact section", "联系方式" in rendered or "联系" in rendered),
        ("mbti传递", "ENFP" in rendered),
        ("testimonials传递", "testimonials" in adapted),
        ("framework_items传递", "framework_items" in adapted),
        ("stats传递", "stats" in adapted),
    ]

    passed = 0
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
        if result:
            passed += 1

    if "ERROR:" in rendered:
        print(f"  ❌ 渲染错误: {rendered[:200]}")
        passed = 0
    else:
        print(f"  ✅ 渲染成功，输出长度: {len(rendered)} bytes")

    return passed, len(checks)


def verify_rahulbeniwal():
    """验证 rahulbeniwal 模板"""
    print("\n" + "=" * 60)
    print("测试 rahulbeniwal")
    print("=" * 60)

    test_data = load_test_data()
    template_html = load_template("rahulbeniwal")
    adapted = to_rahulbeniwal(test_data)
    rendered = render_template(template_html, {"data": adapted})

    checks = [
        ("name=苏轼", "苏轼" in rendered),
        ("hero存在", "一蓑烟雨" in rendered or "hero" in rendered.lower()),
        ("about section", "关于" in rendered),
        ("skills section", "技能" in rendered),
        ("projects section", "项目" in rendered),
        ("mini_projects传递", "mini_projects" in adapted),
        ("open_source传递", "open_source" in adapted),
        ("experience section", "职业经历" in rendered),
        ("contact section", "联系" in rendered),
        ("mbti传递", "ENFP" in rendered),
        ("testimonials传递", "testimonials" in adapted),
        ("framework_items传递", "framework_items" in adapted),
        ("stats传递", "stats" in adapted),
    ]

    passed = 0
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
        if result:
            passed += 1

    if "ERROR:" in rendered:
        print(f"  ❌ 渲染错误: {rendered[:200]}")
        passed = 0
    else:
        print(f"  ✅ 渲染成功，输出长度: {len(rendered)} bytes")

    return passed, len(checks)


def main():
    print("=" * 60)
    print("Personal IP Site Generator — 模板验证")
    print("=" * 60)

    total_passed = 0
    total_checks = 0

    p1, t1 = verify_developerfolio()
    total_passed += p1
    total_checks += t1

    p2, t2 = verify_alfolio()
    total_passed += p2
    total_checks += t2

    p3, t3 = verify_rahulbeniwal()
    total_passed += p3
    total_checks += t3

    print("\n" + "=" * 60)
    print(f"总计: {total_passed}/{total_checks} 检查通过")
    print("=" * 60)

    if total_passed == total_checks:
        print("✅ 所有检查通过！")
        return 0
    else:
        print("❌ 部分检查失败，请修复后重试")
        return 1


if __name__ == "__main__":
    sys.exit(main())
