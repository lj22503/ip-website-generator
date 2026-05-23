/**
 * HTML Renderer — TypeScript port from html_renderer.py
 * Generates full HTML from design system + content modules.
 * Handles both Portfolio and Personal Site products.
 *
 * Ported from saas/html_renderer.py (863 lines)
 */

import { buildCss, getSpec } from './css-builder';

// ============================================================
// Types
// ============================================================

export interface ModuleData {
  [key: string]: any;
}

export interface RenderPageOptions {
  designSystem: string;
  content: ModuleData;
  selectedModules: string[];
  productType?: 'portfolio' | 'personal_site';
}

// ============================================================
// Utility Functions
// ============================================================

function isDark(bg: string): boolean {
  const hex = bg.replace('#', '');
  const expanded = hex.length === 3 ? hex.split('').map(c => c + c).join('') : hex;
  if (expanded.length !== 6) return false;
  const r = parseInt(expanded.slice(0, 2), 16);
  const g = parseInt(expanded.slice(2, 4), 16);
  const b = parseInt(expanded.slice(4, 6), 16);
  return 0.299 * r + 0.587 * g + 0.114 * b < 128;
}

function badges(items: string[]): string {
  return items.map(item => `<span class="badge">${item}</span>`).join('');
}

function splitParagraphs(text: string): string {
  return text.split('\n')
    .filter(p => p.trim())
    .map(p => `<p>${p}</p>`)
    .join('');
}

// ============================================================
// Module HTML Generators
// ============================================================

function renderHeroFeatured(data: any, spec: any, dark: boolean): string {
  const title = data.title || '';
  const subtitle = data.subtitle || '';
  const featuredProjects = data.featured_projects || [];

  let badgesHtml = '';
  let projectsSection = '';

  if (featuredProjects.length > 0) {
    badgesHtml = badges(featuredProjects);
    projectsSection = `
        <div class="featured-projects">
            <p class="caption">精选项目</p>
            <div class="project-tags">${badgesHtml}</div>
        </div>
    `;
  }

  return `
<section class="hero section">
    <div class="container">
        <h1 class="display">${title}</h1>
        <p class="hero-subtitle">${subtitle}</p>
        ${projectsSection}
        <div class="hero-cta">
            <a href="#projects" class="btn btn-primary">看我的作品</a>
            <a href="#contact" class="btn btn-secondary">联系我</a>
        </div>
    </div>
</section>
`;
}

function renderHeroStory(data: any, spec: any, dark: boolean): string {
  const headline = data.headline || '';
  const subtitle = data.subtitle || '';
  return `
<section class="hero-story section">
    <div class="container-narrow">
        <p class="hero-label caption">我是谁</p>
        <h1 class="display hero-headline">${headline}</h1>
        <p class="hero-subtitle">${subtitle}</p>
    </div>
</section>
`;
}

function renderAbout(data: any, spec: any, dark: boolean): string {
  const headline = data.headline || '';
  const bio = data.bio || '';
  const photo = data.photo || '';
  const photoHtml = photo
    ? `<img src="${photo}" alt="个人照片" class="about-photo">`
    : '';
  const bioHtml = splitParagraphs(bio);

  return `
<section class="about section" id="about">
    <div class="container">
        <h2 class="section-title">关于我</h2>
        <div class="about-grid">
            ${photoHtml}
            <div class="about-text">
                <p class="about-headline">${headline}</p>
                <div class="about-bio">${bioHtml}</div>
            </div>
        </div>
    </div>
</section>
`;
}

function renderStory(data: any, spec: any, dark: boolean): string {
  const experiences = data.experiences || '';
  const challenges = data.challenges || '';
  const insights = data.insights || '';

  const phases: [string, string][] = [
    ['做过什么', experiences],
    ['遭遇过什么', challenges],
    ['学到什么', insights],
  ];

  const phasesHtml = phases
    .filter(([, text]) => text)
    .map(([title, text]) => {
      const para = splitParagraphs(text);
      return `<div class="story-phase"><h3>${title}</h3><div>${para}</div></div>`;
    })
    .join('');

  if (!phasesHtml) return '';

  return `
<section class="story section" id="story">
    <div class="container-narrow">
        <h2 class="section-title">我的故事</h2>
        <div class="story-timeline">${phasesHtml}</div>
    </div>
</section>
`;
}

function renderSkills(data: any, spec: any, dark: boolean): string {
  const categories = data.categories || [];
  let catsHtml = '';

  for (const cat of categories) {
    if (typeof cat === 'object' && cat !== null) {
      const name = cat.name || '';
      const items = cat.items || [];
      const badgesStr = badges(items);
      catsHtml += `
                <div class="skill-category">
                    <h3 class="skill-cat-name">${name}</h3>
                    <div class="skill-items">${badgesStr}</div>
                </div>
      `;
    } else if (typeof cat === 'string') {
      catsHtml += `<span class="badge">${cat}</span>`;
    }
  }

  if (!catsHtml) return '';

  return `
<section class="skills section" id="skills">
    <div class="container">
        <h2 class="section-title">技能</h2>
        <div class="skills-grid">${catsHtml}</div>
    </div>
</section>
`;
}

function renderProjects(data: any, spec: any, dark: boolean): string {
  let projects = data.projects || [];
  if (!Array.isArray(projects)) {
    projects = projects ? [projects] : [];
  }

  const cards = projects.map((p: any) => {
    const title = p.title || '';
    const year = p.year || '';
    const role = p.role || '';
    const background = p.background || '';
    const outcome = p.outcome || '';
    const tags = p.tags || [];
    const url = p.url || '';

    const badgesStr = badges(tags);
    const yearHtml = year ? `<span class="caption">${year}</span>` : '';
    const roleHtml = role ? `<p class="project-role caption">${role}</p>` : '';
    const bgHtml = background ? `<p class="project-background">${background}</p>` : '';
    const outcomeHtml = outcome ? `<p class="project-outcome"><strong>成果：</strong>${outcome}</p>` : '';
    const tagsHtml = badgesStr ? `<div class="project-tags">${badgesStr}</div>` : '';
    const urlHtml = url
      ? `<a href="${url}" target="_blank" class="project-link">查看项目 →</a>`
      : '';

    return `
            <div class="project-card card">
                <div class="project-header">
                    <h3 class="project-title">${title}</h3>
                    ${yearHtml}
                </div>
                ${roleHtml}
                ${bgHtml}
                ${outcomeHtml}
                ${tagsHtml}
                ${urlHtml}
            </div>
    `;
  }).join('');

  if (!cards) return '';

  return `
<section class="projects section" id="projects">
    <div class="container">
        <h2 class="section-title">作品</h2>
        <div class="projects-grid">${cards}</div>
    </div>
</section>
`;
}

function renderAwards(data: any, spec: any, dark: boolean): string {
  let awards = data.awards || [];
  if (!Array.isArray(awards)) {
    awards = awards ? [awards] : [];
  }

  const items = awards.map((a: any) => {
    const title = a.title || '';
    const year = a.year || '';
    const issuer = a.issuer || '';
    const issuerStr = issuer ? ` · ${issuer}` : '';
    return `
            <div class="award-item">
                <span class="award-title">${title}</span>
                <span class="caption">${year}${issuerStr}</span>
            </div>
    `;
  }).join('');

  if (!items) return '';

  return `
<section class="awards section" id="awards">
    <div class="container">
        <h2 class="section-title">荣誉</h2>
        <div class="awards-list">${items}</div>
    </div>
</section>
`;
}

function renderContact(data: any, spec: any, dark: boolean): string {
  const email = data.email || '';
  const links = data.links || [];

  let linksHtml = '';
  if (Array.isArray(links)) {
    linksHtml = links.map((link: any) => {
      if (typeof link === 'object' && link !== null) {
        const platform = link.platform || '';
        const url = link.url || '';
        if (url) {
          return `<a href="${url}" target="_blank" class="contact-link">${platform}</a>`;
        }
      } else if (typeof link === 'string' && link.includes('|')) {
        const [platform, url] = link.split('|').map((s: string) => s.trim());
        return `<a href="${url}" target="_blank" class="contact-link">${platform}</a>`;
      }
      return '';
    }).join('');
  }

  return `
<section class="contact section" id="contact">
    <div class="container-narrow">
        <h2 class="section-title">联系我</h2>
        <p class="contact-email">
            <a href="mailto:${email}" class="btn btn-primary">${email}</a>
        </p>
        <div class="contact-links">${linksHtml}</div>
    </div>
</section>
`;
}

function renderSocial(data: any, spec: any, dark: boolean): string {
  const links = data.links || [];

  let items = '';
  if (Array.isArray(links)) {
    items = links.map((link: any) => {
      if (typeof link === 'object' && link !== null) {
        const platform = link.platform || '';
        const url = link.url || '';
        if (url) {
          return `<a href="${url}" target="_blank" class="social-link">${platform}</a>`;
        }
      } else if (typeof link === 'string' && link.includes('|')) {
        const [platform, url] = link.split('|').map((s: string) => s.trim());
        return `<a href="${url}" target="_blank" class="social-link">${platform}</a>`;
      }
      return '';
    }).join('');
  }

  if (!items) return '';

  return `
<section class="social section" id="social">
    <div class="container">
        <h2 class="section-title">社交</h2>
        <div class="social-grid">${items}</div>
    </div>
</section>
`;
}

function renderBlog(data: any, spec: any, dark: boolean): string {
  let posts = data.posts || [];
  if (!Array.isArray(posts)) {
    posts = posts ? [posts] : [];
  }

  const postsHtml = posts.map((p: any) => {
    const title = p.title || '';
    const date = p.date || '';
    const excerpt = p.excerpt || '';
    const url = p.url || '#';
    const tags = p.tags || [];
    const badgesStr = badges(tags);

    const dateHtml = date ? `<div class="post-meta caption">${date}</div>` : '';
    const excerptHtml = excerpt ? `<p class="post-excerpt">${excerpt}</p>` : '';
    const tagsHtml = badgesStr ? `<div class="post-tags">${badgesStr}</div>` : '';

    return `
            <article class="blog-post card">
                ${dateHtml}
                <h3 class="post-title"><a href="${url}">${title}</a></h3>
                ${excerptHtml}
                ${tagsHtml}
            </article>
    `;
  }).join('');

  if (!postsHtml) return '';

  return `
<section class="blog section" id="blog">
    <div class="container">
        <h2 class="section-title">博客</h2>
        <div class="blog-list">${postsHtml}</div>
    </div>
</section>
`;
}

function renderNewsletter(data: any, spec: any, dark: boolean): string {
  const headline = data.headline || '订阅我的 newsletter';
  const placeholder = data.placeholder || '你的邮箱';
  const cta = data.cta || '订阅';

  return `
<section class="newsletter section" id="newsletter">
    <div class="container-narrow">
        <div class="newsletter-box card">
            <h2 class="newsletter-headline">${headline}</h2>
            <form class="newsletter-form" onsubmit="return false;">
                <input type="email" placeholder="${placeholder}" class="newsletter-input">
                <button type="submit" class="btn btn-primary">${cta}</button>
            </form>
        </div>
    </div>
</section>
`;
}

// ============================================================
// Module Registry
// ============================================================

const MODULE_RENDERERS: Record<string, (data: any, spec: any, dark: boolean) => string> = {
  hero_featured: renderHeroFeatured,
  hero_story: renderHeroStory,
  about: renderAbout,
  story: renderStory,
  skills: renderSkills,
  projects: renderProjects,
  awards: renderAwards,
  contact: renderContact,
  social: renderSocial,
  blog: renderBlog,
  newsletter: renderNewsletter,
};

// ============================================================
// Navigation
// ============================================================

function renderNav(moduleNames: string[], dark: boolean): string {
  const navItems: Record<string, [string, string]> = {
    hero_featured: ['作品', '#projects'],
    hero_story: ['故事', '#story'],
    about: ['关于', '#about'],
    skills: ['技能', '#skills'],
    projects: ['作品', '#projects'],
    awards: ['荣誉', '#awards'],
    blog: ['博客', '#blog'],
    contact: ['联系', '#contact'],
  };

  const links = moduleNames
    .filter(mod => mod in navItems)
    .map(mod => {
      const [label, href] = navItems[mod];
      return `<a href="${href}" class="nav-link">${label}</a>`;
    })
    .join('');

  return `
<nav class="site-nav">
    <div class="container nav-inner">
        <span class="nav-brand"></span>
        <div class="nav-links">${links}</div>
    </div>
</nav>
`;
}

function renderFooter(data?: any, dark = false): string {
  const year = data?.year || new Date().getFullYear();
  return `
<footer class="site-footer">
    <div class="container">
        <p class="caption">© ${year} · 用 <a href="#">Personal IP Website Generator</a> 生成</p>
    </div>
</footer>
`;
}

// ============================================================
// Additional CSS (from html_renderer.py lines 500-893)
// ============================================================

const MODULE_STYLES = `
body {
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    margin: 0;
}

/* ---- Nav ---- */
.site-nav {
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
}

.nav-links {
    display: flex;
    gap: 24px;
}

.nav-link {
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 500;
    transition: color 0.2s;
    text-decoration: none;
}
.nav-link:hover {
    color: var(--text-primary);
}

/* Hero */
.hero {
    min-height: 70vh;
    display: flex;
    align-items: center;
}

.hero .display {
    margin-bottom: 16px;
}

.hero-subtitle {
    font-size: 20px;
    color: var(--text-secondary);
    margin-bottom: 32px;
}

.hero-cta {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.featured-projects {
    margin: 32px 0;
}

.project-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}

/* Hero Story */
.hero-story {
    min-height: 60vh;
    display: flex;
    align-items: center;
    text-align: center;
}

.hero-label {
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 24px;
}

.hero-headline {
    margin-bottom: 16px;
}

/* About */
.about-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 48px;
    align-items: start;
}

@media (max-width: 640px) {
    .about-grid {
        grid-template-columns: 1fr;
    }
}

.about-photo {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--border);
}

.about-headline {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
    color: var(--text-primary);
}

.about-bio p {
    margin-bottom: 12px;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* Story Timeline */
.story-timeline {
    display: flex;
    flex-direction: column;
    gap: 48px;
    margin-top: 40px;
}

.story-phase h3 {
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 12px;
    font-weight: 600;
}

.story-phase p {
    color: var(--text-secondary);
    margin-bottom: 8px;
    line-height: 1.8;
}

/* Skills */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 32px;
}

.skill-cat-name {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--text-primary);
}

.skill-items {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

/* Projects */
.project-card {
    margin-bottom: 0;
}

.project-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 8px;
}

.project-title {
    font-size: 20px;
    font-weight: 600;
}

.project-role {
    margin-bottom: 12px;
}

.project-background,
.project-outcome {
    color: var(--text-secondary);
    margin-bottom: 12px;
    line-height: 1.6;
}

.project-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
}

.project-link {
    font-size: 14px;
    font-weight: 500;
}

/* Awards */
.awards-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.award-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
}

.award-title {
    font-weight: 500;
}

/* Contact */
.contact {
    text-align: center;
}

.contact-email {
    margin: 32px 0;
}

.contact-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
}

.contact-link {
    font-size: 15px;
    color: var(--text-secondary);
}
.contact-link:hover {
    color: var(--accent);
}

/* Social */
.social-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.social-link {
    padding: 12px 24px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-weight: 500;
    transition: all 0.2s;
}
.social-link:hover {
    border-color: var(--accent);
    color: var(--accent);
}

/* Blog */
.blog-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.post-meta {
    margin-bottom: 8px;
}

.post-title {
    font-size: 22px;
    margin-bottom: 8px;
}

.post-title a {
    color: var(--text-primary);
}
.post-title a:hover {
    color: var(--accent);
}

.post-excerpt {
    color: var(--text-secondary);
    margin-bottom: 12px;
}

.post-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

/* Newsletter */
.newsletter-box {
    text-align: center;
    padding: 48px 32px;
}

.newsletter-headline {
    margin-bottom: 24px;
}

.newsletter-form {
    display: flex;
    gap: 12px;
    max-width: 480px;
    margin: 0 auto;
    flex-wrap: wrap;
    justify-content: center;
}

.newsletter-input {
    flex: 1;
    min-width: 240px;
    padding: 10px 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--bg);
    color: var(--text-primary);
    font-size: 15px;
}

/* Section Title */
.section-title {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 40px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}

/* Footer */
.site-footer {
    padding: 48px 0;
    border-top: 1px solid var(--border);
    text-align: center;
}

.site-footer .caption {
    color: var(--text-tertiary);
}

.site-footer a {
    color: var(--text-secondary);
}

/* Scroll Animations */
.section {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}
.section.visible {
    opacity: 1;
    transform: translateY(0);
}
`;

// ============================================================
// Main Render Function
// ============================================================

/**
 * Render complete HTML page.
 *
 * @param designSystem - Design system name (e.g. "linear.app", "notion")
 * @param content - Dict keyed by module name, each containing module data
 * @param selectedModules - Ordered list of module names to render
 * @param productType - "portfolio" or "personal_site"
 */
export function renderPage(options: RenderPageOptions): string {
  const {
    designSystem,
    content,
    selectedModules,
    productType = 'portfolio',
  } = options;

  const spec = getSpec(designSystem);
  const bg = spec.colors?.bg || '#ffffff';
  const dark = isDark(bg);

  const css = buildCss(designSystem);
  const nav = renderNav(selectedModules, dark);

  // Render modules
  let modulesHtml = '';
  for (const modName of selectedModules) {
    const modData = content[modName] || {};
    const renderer = MODULE_RENDERERS[modName];
    if (renderer && modData && Object.keys(modData).length > 0) {
      modulesHtml += renderer(modData, spec, dark);
    }
  }

  if (!modulesHtml) {
    modulesHtml = `
        <div class="section container">
            <p style="text-align:center; color: var(--text-secondary); padding: 80px 0;">
                还没有内容。运行交互式 CLI 来填充内容。
            </p>
        </div>
    `;
  }

  // Meta description from about bio
  let metaDesc = '';
  const aboutData = content['about'];
  if (aboutData && typeof aboutData === 'object') {
    const bio = aboutData.bio || '';
    metaDesc = bio.slice(0, 160);
  }

  const headline = content['about']?.headline
    || content['hero_featured']?.title
    || content['hero_story']?.headline
    || '我的个人网站';

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${headline}</title>
    <meta name="description" content="${metaDesc}">
    <style>
${css}

${MODULE_STYLES}
    </style>
</head>
<body>
    ${nav}
    ${modulesHtml}
    ${renderFooter(content['footer'], dark)}

    <script>
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll(".section").forEach(section => {
        observer.observe(section);
    });
    </script>
</body>
</html>`;

  return html;
}
