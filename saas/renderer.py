"""
HTML Website Renderer
Takes MBTI style + narrative content → complete personal IP website HTML
"""

from mbti_styles import MBTI_STYLES, get_style, generate_css


def render_website(
    name: str,
    role: str,
    full_story: str,
    short_story: str,
    bio: str,
    mbti: str,
    highlights: list = None,
    contact: dict = None,
    **kwargs
) -> str:
    """
    Render complete personal IP website.
    
    Args:
        name: 姓名
        role: 当前身份/Title
        full_story: 完整故事（400-800字）
        short_story: 短故事（150-300字，Hero用）
        bio: 简介（150字内）
        mbti: MBTI类型
        highlights: 高光时刻列表，每项含 title/description
        contact: 联系信息 {"email": "...", "wechat": "...", "link": "..."}
    """
    
    style = get_style(mbti)
    css = generate_css(style, mbti)
    
    highlights_html = _render_highlights(highlights or [], style)
    contact_html = _render_contact(contact or {}, style)
    layout = style.get("layout", "centered")
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} | {role}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{css}

/* ===== 额外组件样式 ===== */

/* 高光时刻卡片 */
.highlight-card {{
    padding: 24px;
    margin-bottom: 20px;
}}
.highlight-year {{
    font-size: 0.8rem;
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}}
.highlight-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 8px;
}}
.highlight-desc {{
    font-size: 0.9rem;
    line-height: 1.7;
    opacity: 0.85;
}}

/* 联系方式 */
.contact-section {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    padding: 32px 0;
}}
.contact-item {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--secondary);
    border-radius: 24px;
    font-size: 0.85rem;
    color: var(--text);
    text-decoration: none;
    transition: all 0.2s ease;
}}
.contact-item:hover {{
    background: var(--accent);
    color: white;
    transform: translateY(-2px);
}}

/* 标签 */
.tag {{
    display: inline-block;
    padding: 4px 12px;
    background: var(--secondary);
    color: var(--text);
    border-radius: 16px;
    font-size: 0.75rem;
    margin: 4px;
    opacity: 0.8;
}}

/* MBTI Badge */
.mbti-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: var(--primary);
    color: white;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-top: 16px;
}}

/* Scroll animations */
.section {{
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease-out;
}}
.section.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Responsive */
@media (max-width: 768px) {{
    .hero-name {{ font-size: 2.2rem; }}
    .hero-story {{ font-size: 1rem; }}
    .container {{ padding: 0 16px; }}
    .section {{ padding: 40px 0; }}
    {f'.hero-grid {{ grid-template-columns: 1fr !important; }}' if layout == "asymmetric" else ""}
}}

/* Footer custom */
.footer-generate {{
    margin-top: 8px;
    font-size: 0.7rem;
    opacity: 0.5;
}}
</style>
</head>
<body>
"""

    # Hero Section
    hero_class = "hero"
    if layout == "asymmetric":
        hero_class = "hero-grid"
        hero_html = f"""
<section class="hero container">
    <div>
        <p class="hero-role">{role}</p>
        <h1 class="hero-name">{name}</h1>
        <div class="mbti-badge">MBTI · {mbti} · {style['name']}</div>
    </div>
    <div class="hero-story">{short_story}</div>
</section>"""
    elif layout == "visual_heavy":
        hero_html = f"""
<div class="hero-full">
    <div class="container" style="padding-top: 15vh;">
        <p class="hero-role" style="color: rgba(255,255,255,0.7);">{role}</p>
        <h1 class="hero-name" style="color: white; font-size: 3.5rem;">{name}</h1>
        <div class="mbti-badge" style="background: rgba(255,255,255,0.2); margin-top: 16px;">MBTI · {mbti} · {style['name']}</div>
    </div>
</div>
<section class="container" style="padding: 60px 0;">
    <p class="hero-story" style="color: white;">{short_story}</p>
</section>"""
    else:
        hero_html = f"""
<section class="hero container">
    <p class="hero-role">{role}</p>
    <h1 class="hero-name">{name}</h1>
    <div class="mbti-badge">MBTI · {mbti} · {style['name']}</div>
    <p class="hero-story" style="margin-top: 32px;">{short_story}</p>
</section>"""

    html += hero_html

    # Divider
    divider_style = {
        "centered": '<div style="text-align:center; padding: 20px 0;"><span style="color: var(--accent); opacity: 0.4;">· · ·</span></div>',
        "full_width": '<div style="height: 1px; background: linear-gradient(to right, transparent, var(--accent), transparent); margin: 0 auto; max-width: 600px;"></div>',
        "bold_contrast": '<div style="height: 3px; background: var(--primary); width: 60px; margin: 40px auto;"></div>',
    }.get(layout, '<div style="text-align:center; padding: 20px 0;"><span style="color: var(--accent); opacity: 0.4;">· · ·</span></div>')
    
    html += f"\n{divider_style}\n"

    # About / Story Section
    html += f"""
<section class="section container" id="about">
    <h2 class="section-title">我的故事</h2>
    <div style="max-width: 680px; margin: 0 auto;">
        <div class="card" style="padding: 32px 0; background: transparent;">
            <div style="line-height: 2.2; font-size: 1.05rem; text-align: justify;">
                {full_story.replace(chr(10), '<br>')}
            </div>
        </div>
    </div>
</section>
"""

    # Highlights
    if highlights or []:
        html += f"""
<div class="container">
    {divider_style}
</div>
<section class="section container" id="highlights">
    <h2 class="section-title">高光时刻</h2>
    <div class="section-content">
        {highlights_html}
    </div>
</section>
"""

    # Contact
    html += f"""
<div class="container">
    {divider_style}
</div>
<section class="section container" id="contact">
    <h2 class="section-title">连接</h2>
    <div style="text-align: center;">
        {contact_html}
        <p class="bio-short" style="margin-top: 24px; font-size: 0.9rem; opacity: 0.7;">{bio}</p>
    </div>
</section>
"""

    # Footer
    html += f"""
<footer class="footer container">
    <p>&copy; {name}</p>
    <p class="footer-generate">Generated by Diaolong Personal IP</p>
</footer>
"""

    # Scroll animation JS
    html += """
<script>
// Intersection Observer for scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.section').forEach(el => observer.observe(el));
</script>
</body>
</html>
"""

    return html


def _render_highlights(highlights: list, style: dict) -> str:
    """Render highlights section."""
    if not highlights:
        return ""
    
    html = '<div class="grid-section">' if style.get("layout") == "structured_grid" else '<div>'
    
    for h in highlights:
        year = h.get("year", "")
        title = h.get("title", "")
        desc = h.get("description", "")
        
        html += f"""
        <div class="card highlight-card">
            {f'<p class="highlight-year">{year}</p>' if year else ''}
            <h3 class="highlight-title">{title}</h3>
            <p class="highlight-desc">{desc}</p>
        </div>
        """
    
    html += '</div>'
    return html


def _render_contact(contact: dict, style: dict) -> str:
    """Render contact section."""
    items = []
    
    icons = {
        "email": "✉",
        "wechat": "💬",
        "link": "🔗",
        "github": "⌨",
        "twitter": "🐦",
        "phone": "📞"
    }
    
    for key, value in contact.items():
        if not value:
            continue
        icon = icons.get(key, "•")
        if key == "email":
            items.append(f'<a href="mailto:{value}" class="contact-item">{icon} {value}</a>')
        elif key == "link":
            items.append(f'<a href="{value}" target="_blank" class="contact-item">{icon} 访问</a>')
        else:
            items.append(f'<span class="contact-item">{icon} {value}</span>')
    
    return '<div class="contact-section">' + '\n'.join(items) + '</div>' if items else ""
