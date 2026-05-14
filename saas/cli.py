"""
CLI interface for Personal IP Website Generator.
Provides interactive prompting and document upload support.
"""

import json
import sys
from pathlib import Path

from mbti_styles import MBTI_STYLES, get_style, recommend_mbti_from_content
from narrative_generator import generate_story, evaluate_8_knives, detect_ai_style
from html_renderer import render_website


def interactive_mode():
    """Interactive CLI mode with guided prompts."""
    print("\n" + "=" * 50)
    print("   Personal IP Website Generator")
    print("   雕龙叙事 · 个人IP网站生成器")
    print("=" * 50)
    print("\n📝 请回答以下问题，生成专属个人IP网站。")
    print("   （直接回车跳过，可之后修改）\n")
    
    # Name
    name = input("1️⃣  你的名字: ").strip()
    if not name:
        print("⚠️  名字不能为空")
        return
    
    # Role
    role = input("2️⃣  你的身份/Title（例：产品经理、独立开发者、投资人）: ").strip()
    if not role:
        role = "创作者"
    
    # MBTI
    print("\n3️⃣  你的MBTI类型: ")
    print("   可选: INTJ / INFP / ENFJ / ENFP / ENTJ / ENTP / ESFP / ISFJ")
    print("   直接回车=自动推断")
    mbti_input = input("   输入: ").strip().upper()
    
    # Experiences
    print("\n4️⃣  【核心】你做过什么？")
    print("   例：在字节跳动做产品3年，主导过DAU过亿项目，从0到1做过3款产品")
    print("   （尽量具体，写真实经历）")
    experiences = input("   ").strip()
    
    # Challenges
    print("\n5️⃣  【核心】你遭遇过什么？")
    print("   例：35岁被裁员、连续创业失败3次、从大厂螺丝钉到独立创作者的转型焦虑")
    print("   （真实困境比成就更打动人心）")
    challenges = input("   ").strip()
    
    # Insights
    print("\n6️⃣  【核心】你看重什么/你学到什么？")
    print("   例：真正重要的不是平台，是解决问题的能力；好的产品经理是站在用户角度思考")
    print("   （核心认知+价值观）")
    insights = input("   ").strip()
    
    # Highlights
    print("\n7️⃣  高光时刻（选填，直接回车跳过）:")
    print("   格式示例：")
    print('     [{"year": "2022", "title": "产品上线", "description": "DAU突破100万"}, ...]')
    highlights_input = input("   JSON数组或直接回车: ").strip()
    highlights = []
    if highlights_input:
        try:
            highlights = json.loads(highlights_input)
        except json.JSONDecodeError:
            print("⚠️  JSON格式错误，已跳过")
    
    # Contact
    print("\n8️⃣  联系方式（选填）:")
    print('   格式：email:xxx,wechat:xxx,github:xxx')
    contact_input = input("   ").strip()
    contact = {}
    if contact_input:
        for item in contact_input.split(","):
            if ":" in item:
                key, value = item.split(":", 1)
                contact[key.strip()] = value.strip()
    
    # Auto-detect MBTI
    mbti = mbti_input if mbti_input in MBTI_STYLES else None
    if not mbti:
        print("\n🔍 正在根据内容推断MBTI人格...")
        recommendation = recommend_mbti_from_content(
            name, role, experiences, challenges, insights
        )
        mbti = recommendation["mbti"]
        print(f"✅ 推断结果: {mbti} ({recommendation['reason']})")
        confirm = input(f"   确认使用 {mbti}？直接回车确认，输入其他MBTI重新选择: ").strip().upper()
        if confirm and confirm in MBTI_STYLES:
            mbti = confirm
    
    style = get_style(mbti)
    print(f"\n📐 风格方案: {style['name']} — {style['description']}")
    print(f"   核心特质: {' '.join(style['personality_traits'])}")
    
    # Generate
    print("\n✍️  正在生成叙事...")
    result = generate_story(
        name=name,
        role=role,
        experiences=experiences,
        challenges=challenges,
        insights=insights,
        mbti=mbti
    )
    
    # Quality report
    print("\n📊 质量评估:")
    eval_result = result["evaluation"]
    print(f"   八刀评估总分: {eval_result['total']:.1f}/10")
    weakest = eval_result.get("weakest", "")
    for dim, score in eval_result["scores"].items():
        marker = " ⚠️(最弱)" if dim == weakest else ""
        status = "✅" if score >= 7 else "⚠️"
        print(f"   {status} {dim}: {score}/10{marker}")
    if eval_result["suggestions"]:
        for dim, sug in eval_result["suggestions"].items():
            print(f"      → {sug}")
    
    de_ai = result["de_ai"]
    print(f"\n🤖 去AI化检测: {'✅ 通过' if de_ai['passed'] else f'⚠️ {de_ai[\"failed_count\"]}项未通过'}")
    for rule, (passed, detail) in de_ai["results"].items():
        status = "✅" if passed else "⚠️"
        print(f"   {status} {rule}: {detail}")
    
    # Render
    print("\n🎨 正在渲染HTML...")
    html = render_website(
        name=name,
        role=role,
        full_story=result["full_story"],
        short_story=result["short_story"],
        bio=result["bio"],
        mbti=mbti,
        highlights=highlights,
        contact=contact
    )
    
    # Save
    output_name = f"{name}.html"
    output_path = Path(output_name)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ 网站已生成: {output_path.absolute()}")
    print(f"   文件大小: {size_kb:.1f} KB")
    print(f"   风格: {mbti} ({style['name']})")
    print(f"\n🌐 可在浏览器打开查看效果")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Delegate to app.py for argument parsing
        from app import main
        main()
    else:
        interactive_mode()
