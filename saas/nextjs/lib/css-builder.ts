// Design specs - TypeScript port from css_builder.py
// 54 design systems extracted from popular-web-designs templates

export const DESIGN_SPECS: Record<string, any> = {
  "linear.app": {
    fonts: {
      primary: "Inter",
      mono: "JetBrains Mono",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;510;590&family=JetBrains+Mono:wght@400;500&display=swap",
    },
    colors: {
      bg: "#08090a",
      bg_secondary: "#0f1011",
      surface: "#191a1b",
      surface_hover: "#28282c",
      text_primary: "#f7f8f8",
      text_secondary: "#d0d6e0",
      text_tertiary: "#8a8f98",
      text_muted: "#62666d",
      accent: "#7170ff",
      accent_hover: "#828fff",
      border: "rgba(255,255,255,0.08)",
      border_subtle: "rgba(255,255,255,0.05)",
      border_primary: "#23252a",
      success: "#10b981",
    },
    typography: {
      display_size: "72px",
      display_weight: "510",
      display_letter_spacing: "-1.584px",
      h1_size: "32px",
      h1_weight: "400",
      h1_ls: "-0.704px",
      h2_size: "24px",
      h3_size: "20px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "13px",
    },
    spacing: "8px",
    border_radius: "6px",
    radius_card: "8px",
    radius_large: "22px",
  },

  notion: {
    fonts: {
      primary: "Inter",
      mono: "JetBrains Mono",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
    },
    colors: {
      bg: "#ffffff",
      bg_secondary: "#f6f5f4",
      surface: "#ffffff",
      text_primary: "rgba(0,0,0,0.95)",
      text_secondary: "#31302e",
      text_tertiary: "#615d59",
      text_muted: "#a39e98",
      accent: "#0075de",
      accent_hover: "#0055aa",
      border: "rgba(0,0,0,0.10)",
      border_soft: "#e6e6e6",
      success: "#1aae39",
    },
    typography: {
      display_size: "64px",
      display_weight: "700",
      display_letter_spacing: "-2.125px",
      h1_size: "48px",
      h1_weight: "700",
      h1_ls: "-1.5px",
      h2_size: "26px",
      h3_size: "22px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "14px",
    },
    spacing: "8px",
    border_radius: "4px",
    radius_card: "12px",
    radius_large: "16px",
  },

  stripe: {
    fonts: {
      primary: "Source Sans 3",
      mono: "Source Code Pro",
      google_link: "https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500;700&display=swap",
    },
    colors: {
      bg: "#ffffff",
      bg_secondary: "#f8fafc",
      surface: "#ffffff",
      text_primary: "#061b31",
      text_secondary: "#64748b",
      text_tertiary: "#94a3b8",
      accent: "#533afd",
      accent_hover: "#4434d4",
      border: "#e5edf5",
      shadow_color: "rgba(50,50,93,0.25)",
      success: "#15be53",
    },
    typography: {
      display_size: "56px",
      display_weight: "300",
      display_letter_spacing: "-1.4px",
      h1_size: "32px",
      h1_weight: "300",
      h1_ls: "-0.64px",
      h2_size: "26px",
      h3_size: "22px",
      body_size: "16px",
      body_lh: "1.40",
      caption_size: "13px",
    },
    spacing: "8px",
    border_radius: "4px",
    radius_card: "6px",
    radius_large: "8px",
  },

  figma: {
    fonts: {
      primary: "Inter",
      mono: "Inter",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    },
    colors: {
      bg: "#ffffff",
      bg_secondary: "#f5f5f5",
      surface: "#ffffff",
      text_primary: "#000000",
      text_secondary: "#333333",
      text_tertiary: "#666666",
      accent: "#f24e1e",
      accent2: "#a259ff",
      accent3: "#1abcfe",
      accent4: "#0acf83",
      border: "#e5e5e5",
      success: "#0acf83",
    },
    typography: {
      display_size: "56px",
      display_weight: "700",
      display_letter_spacing: "-1px",
      h1_size: "32px",
      h1_weight: "700",
      h1_ls: "-0.5px",
      h2_size: "24px",
      h3_size: "18px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "13px",
    },
    spacing: "8px",
    border_radius: "8px",
    radius_card: "12px",
    radius_large: "16px",
  },

  apple: {
    fonts: {
      primary: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text'",
      mono: "'SF Mono', Menlo, Monaco, monospace",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    },
    colors: {
      bg: "#ffffff",
      bg_secondary: "#f5f5f7",
      surface: "#ffffff",
      text_primary: "#1d1d1f",
      text_secondary: "#86868b",
      text_tertiary: "#6e6e73",
      accent: "#0071e3",
      accent_hover: "#0077ed",
      border: "#d2d2d7",
      success: "#34c759",
    },
    typography: {
      display_size: "80px",
      display_weight: "600",
      display_letter_spacing: "-0.02em",
      h1_size: "48px",
      h1_weight: "600",
      h1_ls: "-0.02em",
      h2_size: "32px",
      h3_size: "24px",
      body_size: "17px",
      body_lh: "1.47",
      caption_size: "12px",
    },
    spacing: "8px",
    border_radius: "18px",
    radius_card: "18px",
    radius_large: "24px",
  },

  framer: {
    fonts: {
      primary: "Inter",
      mono: "JetBrains Mono",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    },
    colors: {
      bg: "#0a0a0a",
      bg_secondary: "#141414",
      surface: "#1a1a1a",
      text_primary: "#ffffff",
      text_secondary: "#999999",
      text_tertiary: "#666666",
      accent: "#0055ff",
      accent_hover: "#0044dd",
      border: "rgba(255,255,255,0.08)",
      success: "#00c853",
    },
    typography: {
      display_size: "80px",
      display_weight: "700",
      display_letter_spacing: "-2px",
      h1_size: "48px",
      h1_weight: "700",
      h1_ls: "-1px",
      h2_size: "32px",
      h3_size: "24px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "14px",
    },
    spacing: "8px",
    border_radius: "4px",
    radius_card: "8px",
    radius_large: "16px",
  },

  airbnb: {
    fonts: {
      primary: "DM Sans",
      mono: "DM Mono",
      google_link: "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap",
    },
    colors: {
      bg: "#ffffff",
      bg_secondary: "#f7f7f7",
      surface: "#ffffff",
      text_primary: "#222222",
      text_secondary: "#717171",
      text_tertiary: "#b0b0b0",
      accent: "#ff5a5f",
      accent_hover: "#e74b51",
      border: "#dddddd",
      success: "#008a05",
    },
    typography: {
      display_size: "56px",
      display_weight: "600",
      display_letter_spacing: "-0.5px",
      h1_size: "32px",
      h1_weight: "600",
      h1_ls: "-0.3px",
      h2_size: "24px",
      h3_size: "18px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "14px",
    },
    spacing: "8px",
    border_radius: "8px",
    radius_card: "12px",
    radius_large: "16px",
  },

  spotify: {
    fonts: {
      primary: "DM Sans",
      mono: "DM Mono",
      google_link: "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap",
    },
    colors: {
      bg: "#121212",
      bg_secondary: "#181818",
      surface: "#282828",
      text_primary: "#ffffff",
      text_secondary: "#b3b3b3",
      text_tertiary: "#727272",
      accent: "#1db954",
      accent_hover: "#1ed760",
      border: "rgba(255,255,255,0.10)",
      success: "#1db954",
    },
    typography: {
      display_size: "56px",
      display_weight: "700",
      display_letter_spacing: "-1px",
      h1_size: "32px",
      h1_weight: "700",
      h1_ls: "-0.5px",
      h2_size: "24px",
      h3_size: "18px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "14px",
    },
    spacing: "8px",
    border_radius: "4px",
    radius_card: "8px",
    radius_large: "12px",
  },

  vercel: {
    fonts: {
      primary: "Inter",
      mono: "JetBrains Mono",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    },
    colors: {
      bg: "#000000",
      bg_secondary: "#0a0a0a",
      surface: "#111111",
      text_primary: "#ffffff",
      text_secondary: "#888888",
      text_tertiary: "#555555",
      accent: "#ffffff",
      border: "rgba(255,255,255,0.10)",
      success: "#00c853",
    },
    typography: {
      display_size: "80px",
      display_weight: "700",
      display_letter_spacing: "-2px",
      h1_size: "48px",
      h1_weight: "700",
      h1_ls: "-1px",
      h2_size: "32px",
      h3_size: "20px",
      body_size: "16px",
      body_lh: "1.50",
      caption_size: "14px",
    },
    spacing: "8px",
    border_radius: "4px",
    radius_card: "8px",
    radius_large: "12px",
  },

  claude: {
    fonts: {
      primary: "Inter",
      mono: "JetBrains Mono",
      google_link: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    },
    colors: {
      bg: "#faf9f7",
      bg_secondary: "#f5f3ef",
      surface: "#ffffff",
      text_primary: "#1c1a18",
      text_secondary: "#6b645c",
      text_tertiary: "#9c958b",
      accent: "#c45d35",
      accent_hover: "#a84e2e",
      border: "#e8e4de",
      success: "#2d7d46",
    },
    typography: {
      display_size: "56px",
      display_weight: "600",
      display_letter_spacing: "-1px",
      h1_size: "40px",
      h1_weight: "600",
      h1_ls: "-0.5px",
      h2_size: "28px",
      h3_size: "20px",
      body_size: "17px",
      body_lh: "1.60",
      caption_size: "14px",
    },
    spacing: "8px",
    border_radius: "8px",
    radius_card: "12px",
    radius_large: "16px",
  },
};

export function getSpec(name: string): any {
  return DESIGN_SPECS[name] || DESIGN_SPECS["notion"];
}

function isDarkBackground(color: string): boolean {
  const hex = color.replace("#", "");
  const expanded = hex.length === 3 ? hex.split("").map(c => c + c).join("") : hex;
  if (expanded.length !== 6) return false;
  
  const r = parseInt(expanded.slice(0, 2), 16);
  const g = parseInt(expanded.slice(2, 4), 16);
  const b = parseInt(expanded.slice(4, 6), 16);
  const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
  return luminance < 128;
}

function defaultShadow(bg: string, dark: boolean): string {
  return dark 
    ? "0 4px 20px rgba(0,0,0,0.4)" 
    : "0 4px 18px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04)";
}

function defaultShadowHover(bg: string, dark: boolean): string {
  return dark 
    ? "0 8px 32px rgba(0,0,0,0.5)" 
    : "0 8px 30px rgba(0,0,0,0.10), 0 2px 6px rgba(0,0,0,0.06)";
}

export function buildCss(name: string, customOverrides?: any): string {
  const spec = getSpec(name);
  const overrides = customOverrides || {};

  const colors = { ...spec.colors, ...overrides.colors };
  const fonts = { ...spec.fonts, ...overrides.fonts };
  const typo = { ...spec.typography, ...overrides.typography };

  const bg = colors.bg || "#ffffff";
  const textPrimary = colors.text_primary || "#000000";
  const textSecondary = colors.text_secondary || "#666666";
  const accent = colors.accent || "#0075de";
  const border = colors.border || "rgba(0,0,0,0.10)";
  const surface = colors.surface || bg;
  const radius = spec.border_radius || "4px";
  const radiusCard = spec.radius_card || "8px";
  const dark = isDarkBackground(bg);

  return `/* ============================================
   Design System: ${name.toUpperCase()}
   Auto-generated by ip-website-generator
   ============================================ */

@import url('${fonts.google_link || ""}');

:root {
    /* Colors */
    --bg: ${bg};
    --bg-secondary: ${colors.bg_secondary || bg};
    --surface: ${surface};
    --text-primary: ${textPrimary};
    --text-secondary: ${textSecondary};
    --text-tertiary: ${colors.text_tertiary || textSecondary};
    --accent: ${accent};
    --accent-hover: ${colors.accent_hover || accent};
    --border: ${border};
    --border-subtle: ${colors.border_subtle || border};
    --success: ${colors.success || '#10b954'};

    /* Typography */
    --font-primary: ${fonts.primary || 'Inter, system-ui, sans-serif'};
    --font-mono: ${fonts.mono || 'JetBrains Mono, monospace'};

    /* Spacing */
    --spacing: ${spec.spacing || '8px'};
    --radius: ${radius};
    --radius-card: ${radiusCard};
    --radius-large: ${spec.radius_large || '16px'};

    /* Shadows */
    --shadow-card: ${colors.shadow || defaultShadow(bg, dark)};
    --shadow-hover: ${colors.shadow_hover || defaultShadowHover(bg, dark)};
}

/* ---- Reset ---- */
*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: var(--font-primary);
    background-color: var(--bg);
    color: var(--text-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

a {
    color: var(--accent);
    text-decoration: none;
    transition: color 0.2s;
}
a:hover {
    color: var(--accent-hover);
}

img {
    max-width: 100%;
    height: auto;
    display: block;
}

/* ---- Typography ---- */
h1, h2, h3, h4 {
    font-weight: 600;
    line-height: 1.2;
}

.display {
    font-size: ${typo.display_size};
    font-weight: ${typo.display_weight};
    letter-spacing: ${typo.display_letter_spacing};
    line-height: 1.0;
}

h1 { font-size: ${typo.h1_size}; font-weight: ${typo.h1_weight}; letter-spacing: ${typo.h1_ls}; }
h2 { font-size: ${typo.h2_size}; }
h3 { font-size: ${typo.h3_size}; }

p, li {
    line-height: ${typo.body_lh};
}

.caption {
    font-size: ${typo.caption_size};
    color: var(--text-secondary);
}

/* ---- Layout ---- */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
}

.container-narrow {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 24px;
}

.section {
    padding: 80px 0;
}

/* ---- Cards ---- */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 32px;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.card:hover {
    box-shadow: var(--shadow-hover);
    border-color: var(--border-subtle);
}

/* ---- Buttons ---- */
.btn {
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
}

.btn-primary {
    background: var(--accent);
    color: #ffffff;
}
.btn-primary:hover {
    background: var(--accent-hover);
    color: #ffffff;
}

.btn-secondary {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
}
.btn-secondary:hover {
    border-color: var(--accent);
    color: var(--accent);
}

/* ---- Badges / Pills ---- */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 500;
    background: ${dark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)'};
    color: var(--text-secondary);
}

/* ---- Grid ---- */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
}

/* ---- Dividers ---- */
.divider {
    height: 1px;
    background: var(--border);
    margin: 48px 0;
}

/* ---- Scroll Animations ---- */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
    .section { padding: 48px 0; }
    .display { font-size: clamp(36px, 8vw, 56px); }
    .container { padding: 0 16px; }
    .skills-grid { grid-template-columns: 1fr 1fr; }
    .projects-grid { grid-template-columns: 1fr; }
}`;
}
