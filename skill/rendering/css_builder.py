"""
CSS Builder — Converts design system metadata → CSS custom properties + styles.
Loads full design specs from the popular-web-designs skill templates.
"""

import json
import os
import re
from pathlib import Path

# Design system color/typographic data extracted from popular-web-designs templates
# Full templates loaded from skill via skill_view() at runtime

DESIGN_SPECS = {
    "linear.app": {
        "fonts": {
            "primary": "Inter",
            "mono": "JetBrains Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;510;590&family=JetBrains+Mono:wght@400;500&display=swap",
        },
        "colors": {
            "bg": "#08090a",
            "bg_secondary": "#0f1011",
            "surface": "#191a1b",
            "surface_hover": "#28282c",
            "text_primary": "#f7f8f8",
            "text_secondary": "#d0d6e0",
            "text_tertiary": "#8a8f98",
            "text_muted": "#62666d",
            "accent": "#7170ff",
            "accent_hover": "#828fff",
            "border": "rgba(255,255,255,0.08)",
            "border_subtle": "rgba(255,255,255,0.05)",
            "border_primary": "#23252a",
            "success": "#10b981",
        },
        "typography": {
            "display_size": "72px",
            "display_weight": "510",
            "display_letter_spacing": "-1.584px",
            "h1_size": "32px",
            "h1_weight": "400",
            "h1_ls": "-0.704px",
            "h2_size": "24px",
            "h3_size": "20px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "13px",
        },
        "spacing": "8px",
        "border_radius": "6px",
        "radius_card": "8px",
        "radius_large": "22px",
    },

    "notion": {
        "fonts": {
            "primary": "Inter",
            "mono": "JetBrains Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        },
        "colors": {
            "bg": "#ffffff",
            "bg_secondary": "#f6f5f4",
            "surface": "#ffffff",
            "text_primary": "rgba(0,0,0,0.95)",
            "text_secondary": "#31302e",
            "text_tertiary": "#615d59",
            "text_muted": "#a39e98",
            "accent": "#0075de",
            "accent_hover": "#0055aa",
            "border": "rgba(0,0,0,0.10)",
            "border_soft": "#e6e6e6",
            "success": "#1aae39",
        },
        "typography": {
            "display_size": "64px",
            "display_weight": "700",
            "display_letter_spacing": "-2.125px",
            "h1_size": "48px",
            "h1_weight": "700",
            "h1_ls": "-1.5px",
            "h2_size": "26px",
            "h3_size": "22px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "14px",
        },
        "spacing": "8px",
        "border_radius": "4px",
        "radius_card": "12px",
        "radius_large": "16px",
    },

    "stripe": {
        "fonts": {
            "primary": "Source Sans 3",
            "mono": "Source Code Pro",
            "google_link": "https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500;700&display=swap",
        },
        "colors": {
            "bg": "#ffffff",
            "bg_secondary": "#f8fafc",
            "surface": "#ffffff",
            "text_primary": "#061b31",
            "text_secondary": "#64748b",
            "text_tertiary": "#94a3b8",
            "accent": "#533afd",
            "accent_hover": "#4434d4",
            "border": "#e5edf5",
            "shadow_color": "rgba(50,50,93,0.25)",
            "success": "#15be53",
        },
        "typography": {
            "display_size": "56px",
            "display_weight": "300",
            "display_letter_spacing": "-1.4px",
            "h1_size": "32px",
            "h1_weight": "300",
            "h1_ls": "-0.64px",
            "h2_size": "26px",
            "h3_size": "22px",
            "body_size": "16px",
            "body_lh": "1.40",
            "caption_size": "13px",
        },
        "spacing": "8px",
        "border_radius": "4px",
        "radius_card": "6px",
        "radius_large": "8px",
    },

    "figma": {
        "fonts": {
            "primary": "Inter",
            "mono": "Inter",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        },
        "colors": {
            "bg": "#ffffff",
            "bg_secondary": "#f5f5f5",
            "surface": "#ffffff",
            "text_primary": "#000000",
            "text_secondary": "#333333",
            "text_tertiary": "#666666",
            "accent": "#f24e1e",
            "accent2": "#a259ff",
            "accent3": "#1abcfe",
            "accent4": "#0acf83",
            "border": "#e5e5e5",
            "success": "#0acf83",
        },
        "typography": {
            "display_size": "56px",
            "display_weight": "700",
            "display_letter_spacing": "-1px",
            "h1_size": "32px",
            "h1_weight": "700",
            "h1_ls": "-0.5px",
            "h2_size": "24px",
            "h3_size": "18px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "13px",
        },
        "spacing": "8px",
        "border_radius": "8px",
        "radius_card": "12px",
        "radius_large": "16px",
    },

    "apple": {
        "fonts": {
            "primary": "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text'",
            "mono": "'SF Mono', Menlo, Monaco, monospace",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        },
        "colors": {
            "bg": "#ffffff",
            "bg_secondary": "#f5f5f7",
            "surface": "#ffffff",
            "text_primary": "#1d1d1f",
            "text_secondary": "#86868b",
            "text_tertiary": "#6e6e73",
            "accent": "#0071e3",
            "accent_hover": "#0077ed",
            "border": "#d2d2d7",
            "success": "#34c759",
        },
        "typography": {
            "display_size": "80px",
            "display_weight": "600",
            "display_letter_spacing": "-0.02em",
            "h1_size": "48px",
            "h1_weight": "600",
            "h1_ls": "-0.02em",
            "h2_size": "32px",
            "h3_size": "24px",
            "body_size": "17px",
            "body_lh": "1.47",
            "caption_size": "12px",
        },
        "spacing": "8px",
        "border_radius": "18px",
        "radius_card": "18px",
        "radius_large": "24px",
    },

    "framer": {
        "fonts": {
            "primary": "Inter",
            "mono": "JetBrains Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        },
        "colors": {
            "bg": "#0a0a0a",
            "bg_secondary": "#141414",
            "surface": "#1a1a1a",
            "text_primary": "#ffffff",
            "text_secondary": "#999999",
            "text_tertiary": "#666666",
            "accent": "#0055ff",
            "accent_hover": "#0044dd",
            "border": "rgba(255,255,255,0.08)",
            "success": "#00c853",
        },
        "typography": {
            "display_size": "80px",
            "display_weight": "700",
            "display_letter_spacing": "-2px",
            "h1_size": "48px",
            "h1_weight": "700",
            "h1_ls": "-1px",
            "h2_size": "32px",
            "h3_size": "24px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "14px",
        },
        "spacing": "8px",
        "border_radius": "4px",
        "radius_card": "8px",
        "radius_large": "16px",
    },

    "airbnb": {
        "fonts": {
            "primary": "DM Sans",
            "mono": "DM Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap",
        },
        "colors": {
            "bg": "#ffffff",
            "bg_secondary": "#f7f7f7",
            "surface": "#ffffff",
            "text_primary": "#222222",
            "text_secondary": "#717171",
            "text_tertiary": "#b0b0b0",
            "accent": "#ff5a5f",
            "accent_hover": "#e74b51",
            "border": "#dddddd",
            "success": "#008a05",
        },
        "typography": {
            "display_size": "56px",
            "display_weight": "600",
            "display_letter_spacing": "-0.5px",
            "h1_size": "32px",
            "h1_weight": "600",
            "h1_ls": "-0.3px",
            "h2_size": "24px",
            "h3_size": "18px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "14px",
        },
        "spacing": "8px",
        "border_radius": "8px",
        "radius_card": "12px",
        "radius_large": "16px",
    },

    "spotify": {
        "fonts": {
            "primary": "DM Sans",
            "mono": "DM Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap",
        },
        "colors": {
            "bg": "#121212",
            "bg_secondary": "#181818",
            "surface": "#282828",
            "text_primary": "#ffffff",
            "text_secondary": "#b3b3b3",
            "text_tertiary": "#727272",
            "accent": "#1db954",
            "accent_hover": "#1ed760",
            "border": "rgba(255,255,255,0.10)",
            "success": "#1db954",
        },
        "typography": {
            "display_size": "56px",
            "display_weight": "700",
            "display_letter_spacing": "-1px",
            "h1_size": "32px",
            "h1_weight": "700",
            "h1_ls": "-0.5px",
            "h2_size": "24px",
            "h3_size": "18px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "14px",
        },
        "spacing": "8px",
        "border_radius": "4px",
        "radius_card": "8px",
        "radius_large": "12px",
    },

    "vercel": {
        "fonts": {
            "primary": "Inter",
            "mono": "JetBrains Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        },
        "colors": {
            "bg": "#000000",
            "bg_secondary": "#0a0a0a",
            "surface": "#111111",
            "text_primary": "#ffffff",
            "text_secondary": "#888888",
            "text_tertiary": "#555555",
            "accent": "#ffffff",
            "border": "rgba(255,255,255,0.10)",
            "success": "#00c853",
        },
        "typography": {
            "display_size": "80px",
            "display_weight": "700",
            "display_letter_spacing": "-2px",
            "h1_size": "48px",
            "h1_weight": "700",
            "h1_ls": "-1px",
            "h2_size": "32px",
            "h3_size": "20px",
            "body_size": "16px",
            "body_lh": "1.50",
            "caption_size": "14px",
        },
        "spacing": "8px",
        "border_radius": "4px",
        "radius_card": "8px",
        "radius_large": "12px",
    },

    "claude": {
        "fonts": {
            "primary": "Inter",
            "mono": "JetBrains Mono",
            "google_link": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        },
        "colors": {
            "bg": "#faf9f7",
            "bg_secondary": "#f5f3ef",
            "surface": "#ffffff",
            "text_primary": "#1c1a18",
            "text_secondary": "#6b645c",
            "text_tertiary": "#9c958b",
            "accent": "#c45d35",
            "accent_hover": "#a84e2e",
            "border": "#e8e4de",
            "success": "#2d7d46",
        },
        "typography": {
            "display_size": "56px",
            "display_weight": "600",
            "display_letter_spacing": "-1px",
            "h1_size": "40px",
            "h1_weight": "600",
            "h1_ls": "-0.5px",
            "h2_size": "28px",
            "h3_size": "20px",
            "body_size": "17px",
            "body_lh": "1.60",
            "caption_size": "14px",
        },
        "spacing": "8px",
        "border_radius": "8px",
        "radius_card": "12px",
        "radius_large": "16px",
    },
}


def get_spec(name: str) -> dict:
    """Get design spec by name. Falls back to notion."""
    return DESIGN_SPECS.get(name, DESIGN_SPECS["notion"])


def build_css(name: str, custom_overrides: dict = None) -> str:
    """
    Build complete CSS from design system name + optional overrides.
    Returns a complete <style> block.
    """
    spec = get_spec(name)
    overrides = custom_overrides or {}

    # Merge overrides
    colors = {**spec["colors"], **overrides.get("colors", {})}
    fonts = {**spec["fonts"], **overrides.get("fonts", {})}
    typo = {**spec["typography"], **overrides.get("typography", {})}

    bg = colors.get("bg", "#ffffff")
    text_primary = colors.get("text_primary", "#000000")
    text_secondary = colors.get("text_secondary", "#666666")
    accent = colors.get("accent", "#0075de")
    border = colors.get("border", "rgba(0,0,0,0.10)")
    surface = colors.get("surface", bg)
    radius = spec.get("border_radius", "4px")
    radius_card = spec.get("radius_card", "8px")

    # Determine if dark mode
    is_dark = _is_dark_background(bg)

    css = f"""
/* ============================================
   Design System: {name.upper()}
   Auto-generated by ip-website-generator
   ============================================ */

@import url('{fonts.get("google_link", "")}');

:root {{
    /* Colors */
    --bg: {bg};
    --bg-secondary: {colors.get('bg_secondary', bg)};
    --surface: {surface};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --text-tertiary: {colors.get('text_tertiary', text_secondary)};
    --accent: {accent};
    --accent-hover: {colors.get('accent_hover', accent)};
    --border: {border};
    --border-subtle: {colors.get('border_subtle', border)};
    --success: {colors.get('success', '#10b954')};

    /* Typography */
    --font-primary: {fonts.get('primary', 'Inter, system-ui, sans-serif')};
    --font-mono: {fonts.get('mono', 'JetBrains Mono, monospace')};

    /* Spacing */
    --spacing: {spec.get('spacing', '8px')};
    --radius: {radius};
    --radius-card: {radius_card};
    --radius-large: {spec.get('radius_large', '16px')};

    /* Shadows */
    --shadow-card: {colors.get('shadow', _default_shadow(bg, is_dark))};
    --shadow-hover: {colors.get('shadow_hover', _default_shadow_hover(bg, is_dark))};
}}

/* ---- Reset ---- */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: var(--font-primary);
    background-color: var(--bg);
    color: var(--text-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

a {{
    color: var(--accent);
    text-decoration: none;
    transition: color 0.2s;
}}
a:hover {{
    color: var(--accent-hover);
}}

img {{
    max-width: 100%;
    height: auto;
    display: block;
}}

/* ---- Typography ---- */
h1, h2, h3, h4 {{
    font-weight: 600;
    line-height: 1.2;
    color: var(--text-primary);
}}

.display {{
    font-size: {typo['display_size']};
    font-weight: {typo['display_weight']};
    letter-spacing: {typo['display_letter_spacing']};
    line-height: 1.0;
}}

h1 {{ font-size: {typo['h1_size']}; font-weight: {typo['h1_weight']}; letter-spacing: {typo['h1_ls']}; }}
h2 {{ font-size: {typo['h2_size']}; }}
h3 {{ font-size: {typo['h3_size']}; }}

p, li {{
    line-height: {typo['body_lh']};
}}

.caption {{
    font-size: {typo['caption_size']};
    color: var(--text-secondary);
}}

/* ---- Layout ---- */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}}

.container-narrow {{
    max-width: 720px;
    margin: 0 auto;
    padding: 0 24px;
}}

.section {{
    padding: 80px 0;
}}

/* ---- Cards ---- */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 32px;
    transition: box-shadow 0.2s, border-color 0.2s;
}}
.card:hover {{
    box-shadow: var(--shadow-hover);
    border-color: var(--border-subtle);
}}

/* ---- Buttons ---- */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: var(--radius);
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    text-decoration: none;
}}

.btn-primary {{
    background: var(--accent);
    color: {'#ffffff' if is_dark else '#ffffff'};
}}
.btn-primary:hover {{
    background: var(--accent-hover);
    color: #ffffff;
}}

.btn-secondary {{
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
}}
.btn-secondary:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

/* ---- Badges / Pills ---- */
.badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 500;
    background: {'rgba(255,255,255,0.08)' if is_dark else 'rgba(0,0,0,0.06)'};
    color: var(--text-secondary);
}}

/* ---- Grid ---- */
.grid-2 {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}}

.grid-3 {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
}}

/* ---- Dividers ---- */
.divider {{
    height: 1px;
    background: var(--border);
    margin: 48px 0;
}}

/* ---- Scroll Animations ---- */
.fade-in {{
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}}
.fade-in.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* ============================================
   Module Styles — Skills
   ============================================ */
.skills-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 32px;
}}

.skill-category {{
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.skill-cat-name {{
    font-size: {typo['caption_size']};
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-tertiary);
    margin-bottom: 4px;
}}

.skill-items {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}

.skill-items .badge {{
    font-size: 13px;
    padding: 5px 12px;
}}

/* ============================================
   Module Styles — Projects
   ============================================ */
.projects-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    align-items: stretch;
}}

.projects-grid .project-card {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 28px;
    height: 100%;
}}

.project-card {{
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.project-header {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
}}

.project-title {{
    font-size: 17px;
    font-weight: 600;
    color: var(--text-primary);
}}

.project-role {{
    font-size: 12px;
    color: var(--text-tertiary);
    margin: 0;
}}

.project-background {{
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.65;
}}

.project-outcome {{
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}}

.project-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: auto;
    padding-top: 8px;
}}

.project-link {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    font-weight: 500;
    color: var(--accent);
    margin-top: auto;
}}
.project-link:hover {{
    color: var(--accent-hover);
}}

/* ============================================
   Module Styles — Contact
   ============================================ */
.contact .container-narrow {{
    text-align: center;
}}

.contact .section-title {{
    margin-bottom: 32px;
}}

.contact-email {{
    margin-bottom: 24px;
}}

.contact-email .btn {{
    font-size: 15px;
    padding: 12px 28px;
}}

.contact-links {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}}

.contact-link {{
    font-size: 14px;
    color: var(--text-secondary);
    transition: color 0.2s;
}}
.contact-link:hover {{
    color: var(--accent);
}}

/* ============================================
   Module Styles — CTA Banner
   ============================================ */
.cta-banner {{
    text-align: center;
    padding: 80px 24px;
}}

.cta-banner h2 {{
    font-size: clamp(24px, 4vw, 36px);
    font-weight: 600;
    margin-bottom: 12px;
}}

.cta-banner p {{
    font-size: 16px;
    color: var(--text-secondary);
    margin-bottom: 32px;
}}

/* ============================================
   Module Styles — Story
   ============================================ */
.story-timeline {{
    display: flex;
    flex-direction: column;
    gap: 32px;
    margin-top: 40px;
}}

.story-phase h3 {{
    font-size: 15px;
    font-weight: 600;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    font-family: var(--font-primary);
}}

.story-phase p {{
    font-size: 16px;
    color: var(--text-secondary);
    line-height: 1.8;
}}

/* ============================================
   Module Styles — Awards
   ============================================ */
.awards-list {{
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.award-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid var(--border);
}}

.award-title {{
    font-size: 15px;
    font-weight: 500;
    color: var(--text-primary);
}}

/* ============================================
   Module Styles — Blog
   ============================================ */
.blog-list {{
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

.blog-post {{
    padding: 24px 0;
    border-bottom: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.post-title a {{
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
}}
.post-title a:hover {{
    color: var(--accent);
}}

.post-excerpt {{
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.7;
}}

.post-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}}

/* ---- Responsive ---- */
@media (max-width: 768px) {{
    .section {{ padding: 48px 0; }}
    .display {{ font-size: clamp(36px, 8vw, 56px); }}
    .container {{ padding: 0 16px; }}
    .skills-grid {{ grid-template-columns: 1fr 1fr; }}
    .projects-grid {{ grid-template-columns: 1fr; }}
}}
"""
    return css.strip()


def _is_dark_background(color: str) -> bool:
    """Check if a color is dark (for contrast decisions)."""
    color = color.lstrip("#")
    if len(color) == 3:
        color = "".join(c*2 for c in color)
    if len(color) != 6:
        return False
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    luminance = 0.299*r + 0.587*g + 0.114*b
    return luminance < 128


def _default_shadow(bg: str, is_dark: bool) -> str:
    """Get default card shadow based on background."""
    if is_dark:
        return "0 4px 20px rgba(0,0,0,0.4)"
    return "0 4px 18px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04)"


def _default_shadow_hover(bg: str, is_dark: bool) -> str:
    """Get hover shadow."""
    if is_dark:
        return "0 8px 32px rgba(0,0,0,0.5)"
    return "0 8px 30px rgba(0,0,0,0.10), 0 2px 6px rgba(0,0,0,0.06)"
