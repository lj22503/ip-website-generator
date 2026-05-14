// Website renderer - TypeScript port from renderer.py

import { Highlight, Contact } from '@/types';
import { getStyle, generateCss, MBTIStyle } from './mbti-styles';
import { buildCss } from './css-builder';

interface RenderOptions {
  name: string;
  role: string;
  full_story: string;
  short_story: string;
  bio: string;
  mbti: string;
  design?: string;
  highlights?: Highlight[];
  contact?: Contact;
  selectedModules?: string[];
}

export function renderWebsite(options: RenderOptions): string {
  const {
    name,
    role,
    full_story,
    short_story,
    bio,
    mbti,
    design = 'notion',
    highlights = [],
    contact = {},
    selectedModules = ['hero', 'story', 'highlights', 'contact'],
  } = options;

  const style = getStyle(mbti);
  const css = generateCss(style, mbti);
  const designCss = buildCss(design);

  const highlightsHtml = renderHighlights(highlights, style);
  const contactHtml = renderContact(contact, style);
  const layout = style.layout || 'centered';

  // Hero section
  let heroHtml = '';
  if (layout === 'asymmetric') {
    heroHtml = `
<section class="hero container">
    <div>
        <p class="hero-role">${role}</p>
        <h1 class="hero-name">${name}</h1>
        <div class="mbti-badge">MBTI · ${mbti} · ${style.name}</div>
    </div>
    <div class="hero-story">${short_story}</div>
</section>`;
  } else if (layout === 'visual_heavy') {
    heroHtml = `
<div class="hero-full">
    <div class="container" style="padding-top: 15vh;">
        <p class="hero-role" style="color: rgba(255,255,255,0.7);">${role}</p>
        <h1 class="hero-name" style="color: white; font-size: 3.5rem;">${name}</h1>
        <div class="mbti-badge" style="background: rgba(255,255,255,0.2); margin-top: 16px;">MBTI · ${mbti} · ${style.name}</div>
    </div>
</div>
<section class="container" style="padding: 60px 0;">
    <p class="hero-story" style="color: white;">${short_story}</p>
</section>`;
  } else {
    heroHtml = `
<section class="hero container">
    <p class="hero-role">${role}</p>
    <h1 class="hero-name">${name}</h1>
    <div class="mbti-badge">MBTI · ${mbti} · ${style.name}</div>
    <p class="hero-story" style="margin-top: 32px;">${short_story}</p>
</section>`;
  }

  // Divider
  const dividers: Record<string, string> = {
    centered: '<div style="text-align:center; padding: 20px 0;"><span style="color: var(--accent); opacity: 0.4;">· · ·</span></div>',
    full_width: '<div style="height: 1px; background: linear-gradient(to right, transparent, var(--accent), transparent); margin: 0 auto; max-width: 600px;"></div>',
    bold_contrast: '<div style="height: 3px; background: var(--primary); width: 60px; margin: 40px auto;"></div>',
  };
  const dividerStyle = dividers[layout] || dividers.centered;

  // Build the complete HTML
  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${name} | ${role}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
${designCss}

/* ===== MBTI Style Override ===== */
${css}

/* ===== Additional Components ===== */

/* High Light Cards */
.highlight-card {
    padding: 24px;
    margin-bottom: 20px;
}
.highlight-year {
    font-size: 0.8rem;
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.highlight-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 8px;
}
.highlight-desc {
    font-size: 0.9rem;
    line-height: 1.7;
    opacity: 0.85;
}

/* Contact Section */
.contact-section {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    padding: 32px 0;
}
.contact-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--secondary);
    color: var(--text);
    border-radius: 24px;
    font-size: 0.85rem;
    text-decoration: none;
    transition: all 0.2s ease;
}
.contact-item:hover {
    background: var(--accent);
    color: white;
    transform: translateY(-2px);
}

/* Tags */
.tag {
    display: inline-block;
    padding: 4px 12px;
    background: var(--secondary);
    color: var(--text);
    border-radius: 16px;
    font-size: 0.75rem;
    margin: 4px;
    opacity: 0.8;
}

/* MBTI Badge */
.mbti-badge {
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
}

/* Scroll animations */
.section {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease-out;
}
.section.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Responsive */
@media (max-width: 768px) {
    .hero-name { font-size: 2.2rem; }
    .hero-story { font-size: 1rem; }
    .container { padding: 0 16px; }
    .section { padding: 40px 0; }
    ${layout === 'asymmetric' ? '.hero-grid { grid-template-columns: 1fr !important; }' : ''}
}

/* Footer custom */
.footer-generate {
    margin-top: 8px;
    font-size: 0.7rem;
    opacity: 0.5;
}
</style>
</head>
<body>

${heroHtml}

${dividerStyle}

${selectedModules.includes('story') ? `
<section class="section container" id="about">
    <h2 class="section-title">我的故事</h2>
    <div style="max-width: 680px; margin: 0 auto;">
        <div class="card" style="padding: 32px 0; background: transparent;">
            <div style="line-height: 2.2; font-size: 1.05rem; text-align: justify;">
                ${full_story.replace(/\n/g, '<br>')}
            </div>
        </div>
    </div>
</section>
` : ''}

${selectedModules.includes('highlights') && highlights.length > 0 ? `
<div class="container">
    ${dividerStyle}
</div>
<section class="section container" id="highlights">
    <h2 class="section-title">高光时刻</h2>
    <div class="section-content">
        ${highlightsHtml}
    </div>
</section>
` : ''}

${selectedModules.includes('contact') ? `
<div class="container">
    ${dividerStyle}
</div>
<section class="section container" id="contact">
    <h2 class="section-title">连接</h2>
    <div style="text-align: center;">
        ${contactHtml}
        <p class="bio-short" style="margin-top: 24px; font-size: 0.9rem; opacity: 0.7;">${bio}</p>
    </div>
</section>
` : ''}

<footer class="footer container">
    <p>&copy; ${name}</p>
    <p class="footer-generate">Generated by Diaolong Personal IP</p>
</footer>

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
</html>`;

  return html;
}

function renderHighlights(highlights: Highlight[], style: MBTIStyle): string {
  if (!highlights.length) return '';

  const useGrid = style.layout === 'structured_grid';
  let html = useGrid ? '<div class="grid-section">' : '<div>';

  for (const h of highlights) {
    const year = h.year ? `<p class="highlight-year">${h.year}</p>` : '';
    html += `
        <div class="card highlight-card">
            ${year}
            <h3 class="highlight-title">${h.title}</h3>
            <p class="highlight-desc">${h.description}</p>
        </div>
        `;
  }

  html += '</div>';
  return html;
}

function renderContact(contact: Contact, style: MBTIStyle): string {
  const icons: Record<string, string> = {
    email: '✉',
    wechat: '💬',
    link: '🔗',
    github: '⌨',
    twitter: '🐦',
    phone: '📞',
  };

  const items: string[] = [];

  for (const [key, value] of Object.entries(contact)) {
    if (!value) continue;
    const icon = icons[key] || '•';
    if (key === 'email') {
      items.push(`<a href="mailto:${value}" class="contact-item">${icon} ${value}</a>`);
    } else if (key === 'link') {
      items.push(`<a href="${value}" target="_blank" class="contact-item">${icon} 访问</a>`);
    } else {
      items.push(`<span class="contact-item">${icon} ${value}</span>`);
    }
  }

  return items.length > 0 ? `<div class="contact-section">${items.join('\n')}</div>` : '';
}
