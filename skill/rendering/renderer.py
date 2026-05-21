"""
HTML Renderer — Generates full HTML from design system + content modules.
Handles both Portfolio and Personal Site products.
"""

from .css_builder import build_css, get_spec

# ============================================================
# Module HTML Generators
# ============================================================

def _badges(items):
    """Render list of badge items."""
    return "".join(f'<span class="badge">{item}</span>' for item in items)


def _split_paragraphs(text):
    """Split text into paragraphs, return HTML."""
    return "".join(f"<p>{para}</p>" for para in text.split("\n") if para.strip())


def render_hero_featured(data, spec, dark):
    """精选封面."""
    title = data.get("title", "")
    subtitle = data.get("subtitle", "")
    featured_projects = data.get("featured_projects", [])

    badges_html = _badges(featured_projects) if featured_projects else ""
    projects_section = ""
    if badges_html:
        projects_section = f"""
        <div class="featured-projects">
            <p class="caption">精选项目</p>
            <div class="project-tags">{badges_html}</div>
        </div>
        """

    return f"""
<section class="hero section">
    <div class="container">
        <h1 class="display">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
        {projects_section}
        <div class="hero-cta">
            <a href="#projects" class="btn btn-primary">看我的作品</a>
            <a href="#contact" class="btn btn-secondary">联系我</a>
        </div>
    </div>
</section>
"""


def render_hero_story(data, spec, dark):
    """故事封面."""
    headline = data.get("headline", "")
    subtitle = data.get("subtitle", "")
    return f"""
<section class="hero-story section">
    <div class="container-narrow">
        <p class="hero-label">我是谁</p>
        <h1 class="display hero-headline">{headline}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
</section>
"""


def render_about(data, spec, dark):
    """关于我."""
    headline = data.get("headline", "")
    bio = data.get("bio", "")
    photo = data.get("photo", "")
    photo_html = f'<img src="{photo}" alt="个人照片" class="about-photo">' if photo else ""
    bio_html = _split_paragraphs(bio)
    return f"""
<section class="about section" id="about">
    <div class="container">
        <h2 class="section-title">关于我</h2>
        <div class="about-grid">
            {photo_html}
            <div class="about-text">
                <p class="about-headline">{headline}</p>
                <div class="about-bio">{bio_html}</div>
            </div>
        </div>
    </div>
</section>
"""


def render_story(data, spec, dark):
    """我的故事."""
    experiences = data.get("experiences", "")
    challenges = data.get("challenges", "")
    insights = data.get("insights", "")

    phases = [
        ("做过什么", experiences),
        ("遭遇过什么", challenges),
        ("学到什么", insights),
    ]

    phases_html = ""
    for title, text in phases:
        para = _split_paragraphs(text)
        phases_html += f'<div class="story-phase"><h3>{title}</h3><div>{para}</div></div>'

    return f"""
<section class="story section" id="story">
    <div class="container-narrow">
        <h2 class="section-title">我的故事</h2>
        <div class="story-timeline">{phases_html}</div>
    </div>
</section>
"""


def render_skills(data, spec, dark):
    """技能."""
    categories = data.get("categories", [])
    cats_html = ""
    if isinstance(categories, list):
        for cat in categories:
            if isinstance(cat, dict):
                name = cat.get("name", "")
                items = cat.get("items", [])
                badges = _badges(items) if items else ""
                cats_html += f"""
                <div class="skill-category">
                    <h3 class="skill-cat-name">{name}</h3>
                    <div class="skill-items">{badges}</div>
                </div>
                """
            elif isinstance(cat, str):
                cats_html += f'<span class="badge">{cat}</span>'

    return f"""
<section class="skills section" id="skills">
    <div class="container">
        <h2 class="section-title">技能</h2>
        <div class="skills-grid">{cats_html}</div>
    </div>
</section>
"""


def render_projects(data, spec, dark):
    """作品/项目."""
    projects = data.get("projects", [])
    if not isinstance(projects, list):
        projects = [projects] if projects else []

    cards = ""
    for p in projects:
        if isinstance(p, dict):
            title = p.get("title", "")
            year = p.get("year", "")
            role = p.get("role", "")
            background = p.get("background", "")
            outcome = p.get("outcome", "")
            tags = p.get("tags", [])
            url = p.get("url", "")

            badges = _badges(tags) if tags else ""
            year_html = f'<span class="caption">{year}</span>' if year else ""
            role_html = f'<p class="project-role caption">{role}</p>' if role else ""
            bg_html = f'<p class="project-background">{background}</p>' if background else ""
            outcome_html = f'<p class="project-outcome"><strong>成果：</strong>{outcome}</p>' if outcome else ""
            tags_html = f'<div class="project-tags">{badges}</div>' if badges else ""
            url_html = f'<a href="{url}" target="_blank" class="project-link">查看项目 &#8594;</a>' if url else ""

            cards += f"""
            <div class="project-card card">
                <div class="project-header">
                    <h3 class="project-title">{title}</h3>
                    {year_html}
                </div>
                {role_html}
                {bg_html}
                {outcome_html}
                {tags_html}
                {url_html}
            </div>
            """

    return f"""
<section class="projects section" id="projects">
    <div class="container">
        <h2 class="section-title">作品</h2>
        <div class="projects-grid">{cards}</div>
    </div>
</section>
"""


def render_awards(data, spec, dark):
    """荣誉/奖项."""
    awards = data.get("awards", [])
    if not isinstance(awards, list):
        awards = [awards] if awards else []

    items = ""
    for a in awards:
        if isinstance(a, dict):
            title = a.get("title", "")
            year = a.get("year", "")
            issuer = a.get("issuer", "")
            issuer_str = f" &#183; {issuer}" if issuer else ""
            items += f"""
            <div class="award-item">
                <span class="award-title">{title}</span>
                <span class="caption">{year}{issuer_str}</span>
            </div>
            """

    return f"""
<section class="awards section" id="awards">
    <div class="container">
        <h2 class="section-title">荣誉</h2>
        <div class="awards-list">{items}</div>
    </div>
</section>
"""


def render_contact(data, spec, dark):
    """联系方式."""
    email = data.get("email", "")
    links = data.get("links", [])

    links_html = ""
    if isinstance(links, list):
        for link in links:
            if isinstance(link, dict):
                platform = link.get("platform", "")
                url = link.get("url", "")
                if url:
                    links_html += f'<a href="{url}" target="_blank" class="contact-link">{platform}</a>'
            elif isinstance(link, str) and "|" in link:
                parts = link.split("|")
                links_html += f'<a href="{parts[1].strip()}" target="_blank" class="contact-link">{parts[0].strip()}</a>'

    return f"""
<section class="contact section" id="contact">
    <div class="container-narrow">
        <h2 class="section-title">联系我</h2>
        <p class="contact-email">
            <a href="mailto:{email}" class="btn btn-primary">{email}</a>
        </p>
        <div class="contact-links">{links_html}</div>
    </div>
</section>
"""


def render_social(data, spec, dark):
    """社交链接."""
    links = data.get("links", [])

    items = ""
    if isinstance(links, list):
        for link in links:
            if isinstance(link, dict):
                platform = link.get("platform", "")
                url = link.get("url", "")
                if url:
                    items += f'<a href="{url}" target="_blank" class="social-link">{platform}</a>'
            elif isinstance(link, str) and "|" in link:
                parts = link.split("|")
                items += f'<a href="{parts[1].strip()}" target="_blank" class="social-link">{parts[0].strip()}</a>'

    return f"""
<section class="social section" id="social">
    <div class="container">
        <h2 class="section-title">社交</h2>
        <div class="social-grid">{items}</div>
    </div>
</section>
"""


def render_blog(data, spec, dark):
    """博客/文章列表."""
    posts = data.get("posts", [])
    if not isinstance(posts, list):
        posts = [posts] if posts else []

    posts_html = ""
    for p in posts:
        if isinstance(p, dict):
            title = p.get("title", "")
            date = p.get("date", "")
            excerpt = p.get("excerpt", "")
            url = p.get("url", "#")
            tags = p.get("tags", [])
            badges = _badges(tags) if tags else ""

            date_html = f'<div class="post-meta caption">{date}</div>' if date else ""
            excerpt_html = f'<p class="post-excerpt">{excerpt}</p>' if excerpt else ""
            tags_html = f'<div class="post-tags">{badges}</div>' if badges else ""

            posts_html += f"""
            <article class="blog-post card">
                {date_html}
                <h3 class="post-title"><a href="{url}">{title}</a></h3>
                {excerpt_html}
                {tags_html}
            </article>
            """

    return f"""
<section class="blog section" id="blog">
    <div class="container">
        <h2 class="section-title">博客</h2>
        <div class="blog-list">{posts_html}</div>
    </div>
</section>
"""


def render_newsletter(data, spec, dark):
    """Newsletter订阅."""
    headline = data.get("headline", "订阅我的 newsletter")
    placeholder = data.get("placeholder", "你的邮箱")
    cta = data.get("cta", "订阅")
    return f"""
<section class="newsletter section" id="newsletter">
    <div class="container-narrow">
        <div class="newsletter-box card">
            <h2 class="newsletter-headline">{headline}</h2>
            <form class="newsletter-form" onsubmit="return false;">
                <input type="email" placeholder="{placeholder}" class="newsletter-input">
                <button type="submit" class="btn btn-primary">{cta}</button>
            </form>
        </div>
    </div>
</section>
"""


# ============================================================
# Module Registry
# ============================================================

MODULE_RENDERERS = {
    "hero_featured": render_hero_featured,
    "hero_story": render_hero_story,
    "about": render_about,
    "story": render_story,
    "skills": render_skills,
    "projects": render_projects,
    "awards": render_awards,
    "contact": render_contact,
    "social": render_social,
    "blog": render_blog,
    "newsletter": render_newsletter,
}


# ============================================================
# Navigation
# ============================================================

def render_nav(module_names, dark):
    """Generate nav based on enabled modules."""
    nav_items = {
        "hero_featured": ("作品", "#projects"),
        "hero_story": ("故事", "#story"),
        "about": ("关于", "#about"),
        "skills": ("技能", "#skills"),
        "projects": ("作品", "#projects"),
        "awards": ("荣誉", "#awards"),
        "blog": ("博客", "#blog"),
        "contact": ("联系", "#contact"),
    }

    links = ""
    for mod in module_names:
        if mod in nav_items:
            label, href = nav_items[mod]
            links += f'<a href="{href}" class="nav-link">{label}</a>'

    return f"""
<nav class="site-nav">
    <div class="container nav-inner">
        <span class="nav-brand"></span>
        <div class="nav-links">{links}</div>
    </div>
</nav>
"""


def render_footer(data=None, dark=False):
    """Footer."""
    year = ""
    if data and isinstance(data, dict):
        year = data.get("year", "")
    return f"""
<footer class="site-footer">
    <div class="container">
        <p class="caption">&#169; {year or 2026} &#183; 用 <a href="#">Personal IP Website Generator</a> 生成</p>
    </div>
</footer>
"""


# ============================================================
# Main Render Function
# ============================================================

def render_page(
    design_system,
    content,
    selected_modules,
    product_type="portfolio",
):
    """
    Render complete HTML page.

    Args:
        design_system: Design system name (e.g. "linear.app", "notion")
        content: Dict keyed by module name, each containing module data
        selected_modules: Ordered list of module names to render
        product_type: "portfolio" or "personal_site"
    """
    spec = get_spec(design_system)
    bg = spec["colors"].get("bg", "#ffffff")

    dark = _is_dark(bg)
    css = build_css(design_system)
    nav = render_nav(selected_modules, dark)

    # Render modules
    modules_html = ""
    for mod_name in selected_modules:
        mod_data = content.get(mod_name, {})
        renderer = MODULE_RENDERERS.get(mod_name)
        if renderer and mod_data:
            modules_html += renderer(mod_data, spec, dark)

    if not modules_html:
        modules_html = """
        <div class="section container">
            <p style="text-align:center; color: var(--text-secondary); padding: 80px 0;">
                还没有内容。运行交互式 CLI 来填充内容。
            </p>
        </div>
        """

    meta_desc = ""
    if isinstance(content.get("about"), dict):
        bio = content["about"].get("bio", "")
        meta_desc = bio[:160] if bio else ""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content.get("about", {}).get("headline", "我的个人网站")}</title>
    <meta name="description" content="{meta_desc}">
    <style>
{css}

/* ---- Nav ---- */
.site-nav {{
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}}

.nav-inner {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
}}

.nav-links {{
    display: flex;
    gap: 24px;
}}

.nav-link {{
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 500;
    transition: color 0.2s;
    text-decoration: none;
}}
.nav-link:hover {{
    color: var(--text-primary);
}}

/* Hero */
.hero {{
    min-height: 70vh;
    display: flex;
    align-items: center;
}}

.hero .display {{
    margin-bottom: 16px;
}}

.hero-subtitle {{
    font-size: 20px;
    color: var(--text-secondary);
    margin-bottom: 32px;
}}

.hero-cta {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}}

.featured-projects {{
    margin: 32px 0;
}}

.project-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}}

/* Hero Story */
.hero-story {{
    min-height: 60vh;
    display: flex;
    align-items: center;
    text-align: center;
}}

.hero-label {{
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 24px;
    color: var(--accent, var(--text-secondary));
}}

.hero-headline {{
    margin-bottom: 16px;
}}

/* About */
.about-grid {{
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 48px;
    align-items: start;
}}

@media (max-width: 640px) {{
    .about-grid {{
        grid-template-columns: 1fr;
    }}
}}

.about-photo {{
    width: 180px;
    height: 180px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--border);
}}

.about-headline {{
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
    color: var(--text-primary);
}}

.about-bio p {{
    margin-bottom: 12px;
    color: var(--text-secondary);
    line-height: 1.7;
}}

/* Story Timeline */
.story-timeline {{
    display: flex;
    flex-direction: column;
    gap: 48px;
    margin-top: 40px;
}}

.story-phase h3 {{
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 12px;
    font-weight: 600;
}}

.story-phase p {{
    color: var(--text-secondary);
    margin-bottom: 8px;
    line-height: 1.8;
}}

/* Skills */
.skills-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 32px;
}}

.skill-cat-name {{
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--text-primary);
}}

.skill-items {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}

/* Projects */
.project-card {{
    margin-bottom: 0;
}}

.project-header {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 8px;
}}

.project-title {{
    font-size: 20px;
    font-weight: 600;
}}

.project-role {{
    margin-bottom: 12px;
}}

.project-background,
.project-outcome {{
    color: var(--text-secondary);
    margin-bottom: 12px;
    line-height: 1.6;
}}

.project-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
}}

.project-link {{
    font-size: 14px;
    font-weight: 500;
}}

/* Awards */
.awards-list {{
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.award-item {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
}}

.award-title {{
    font-weight: 500;
}}

/* Contact */
.contact {{
    text-align: center;
}}

.contact-email {{
    margin: 32px 0;
}}

.contact-links {{
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
}}

.contact-link {{
    font-size: 15px;
    color: var(--text-secondary);
}}
.contact-link:hover {{
    color: var(--accent);
}}

/* Social */
.social-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}}

.social-link {{
    padding: 12px 24px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-weight: 500;
    transition: all 0.2s;
}}
.social-link:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

/* Blog */
.blog-list {{
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

.post-meta {{
    margin-bottom: 8px;
}}

.post-title {{
    font-size: 22px;
    margin-bottom: 8px;
}}

.post-title a {{
    color: var(--text-primary);
}}
.post-title a:hover {{
    color: var(--accent);
}}

.post-excerpt {{
    color: var(--text-secondary);
    margin-bottom: 12px;
}}

.post-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}

/* Newsletter */
.newsletter-box {{
    text-align: center;
    padding: 48px 32px;
}}

.newsletter-headline {{
    margin-bottom: 24px;
}}

.newsletter-form {{
    display: flex;
    gap: 12px;
    max-width: 480px;
    margin: 0 auto;
    flex-wrap: wrap;
    justify-content: center;
}}

.newsletter-input {{
    flex: 1;
    min-width: 240px;
    padding: 10px 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--bg);
    color: var(--text-primary);
    font-size: 15px;
}}

/* Section Title */
.section-title {{
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 40px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}}

/* Footer */
.site-footer {{
    padding: 48px 0;
    border-top: 1px solid var(--border);
    text-align: center;
}}

.site-footer .caption {{
    color: var(--text-tertiary);
}}

.site-footer a {{
    color: var(--text-secondary);
}}

/* Scroll Animations */
.section {{
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}}
.section.visible {{
    opacity: 1;
    transform: translateY(0);
}}
    </style>
</head>
<body>
    {nav}
    {modules_html}
    {render_footer(content, dark)}

    <script>
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add("visible");
            }}
        }});
    }}, {{ threshold: 0.1 }});

    document.querySelectorAll(".section").forEach(section => {{
        observer.observe(section);
    }});
    </script>
</body>
</html>"""
    return html


def _is_dark(bg):
    """Check if background is dark."""
    bg = bg.lstrip("#")
    if len(bg) == 3:
        bg = "".join(c * 2 for c in bg)
    if len(bg) != 6:
        return False
    r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return luminance < 128
