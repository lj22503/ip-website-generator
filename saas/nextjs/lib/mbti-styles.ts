// MBTI-driven style definitions - TypeScript port from mbti_styles.py

import { MBTIStyle } from '@/types';

export const MBTI_STYLES: Record<string, MBTIStyle> = {
  "INFJ": {
    name: "隐喻型",
    description: "文学感、留白、深度疗愈",
    primary_color: "#1a2744",
    secondary_color: "#f5f0e8",
    accent_color: "#8b9dc3",
    text_color: "#2c3e50",
    bg_color: "#faf8f5",
    font_heading: "Georgia, 'Noto Serif SC', serif",
    font_body: "'Noto Serif SC', Georgia, serif",
    layout: "centered",
    hero_align: "center",
    card_style: "minimal",
    spacing: "generous",
    decorative: "quote_marks",
    animation: "subtle_fade",
    personality_traits: ["内省", "理想主义", "洞察力", "坚定"],
  },
  "INFP": {
    name: "自传型",
    description: "真诚温柔、柔和细腻",
    primary_color: "#6b5b7a",
    secondary_color: "#fef6f0",
    accent_color: "#d4a5a5",
    text_color: "#3d3d3d",
    bg_color: "#fff9f5",
    font_heading: "'LXGW WenKai', 'Noto Serif SC', serif",
    font_body: "'LXGW WenKai', 'Noto Serif SC', sans-serif",
    layout: "centered",
    hero_align: "center",
    card_style: "soft_shadow",
    spacing: "relaxed",
    decorative: "handwritten_note",
    animation: "soft_rise",
    personality_traits: ["真诚", "同理心", "创造力", "内省"],
  },
  "ENFJ": {
    name: "鼓舞型",
    description: "有号召力、行动导向",
    primary_color: "#c0392b",
    secondary_color: "#fff8f0",
    accent_color: "#e67e22",
    text_color: "#2c2c2c",
    bg_color: "#ffffff",
    font_heading: "'Noto Sans SC', sans-serif",
    font_body: "'Noto Sans SC', sans-serif",
    layout: "full_width",
    hero_align: "left",
    card_style: "bold_border",
    spacing: "balanced",
    decorative: "bold_lines",
    animation: "slide_up",
    personality_traits: ["同理心", "感染力", "责任感", "魅力"],
  },
  "ENFP": {
    name: "即兴型",
    description: "活泼跳跃、碎片化创意",
    primary_color: "#8e44ad",
    secondary_color: "#fef9e7",
    accent_color: "#27ae60",
    text_color: "#2c3e50",
    bg_color: "#fffdf7",
    font_heading: "'Noto Sans SC', sans-serif",
    font_body: "'Noto Sans SC', sans-serif",
    layout: "asymmetric",
    hero_align: "left",
    card_style: "colorful_border",
    spacing: "varied",
    decorative: "color_blocks",
    animation: "playful_bounce",
    personality_traits: ["热情", "创意", "洞察力", "适应力"],
  },
  "INTJ": {
    name: "战略型",
    description: "冷静、结构化、逻辑清晰",
    primary_color: "#1a1a2e",
    secondary_color: "#f8f9fa",
    accent_color: "#4a90d9",
    text_color: "#1a1a2e",
    bg_color: "#fafbfc",
    font_heading: "'JetBrains Mono', 'Noto Sans SC', monospace",
    font_body: "'Noto Sans SC', 'Inter', sans-serif",
    layout: "structured_grid",
    hero_align: "left",
    card_style: "grid_card",
    spacing: "compact",
    decorative: "geometric_lines",
    animation: "crisp_fade",
    personality_traits: ["独立", "战略思维", "高标准", "理性"],
  },
  "ENTP": {
    name: "颠覆型",
    description: "颠覆感、高对比、话题感",
    primary_color: "#e74c3c",
    secondary_color: "#1a1a1a",
    accent_color: "#f39c12",
    text_color: "#1a1a1a",
    bg_color: "#ffffff",
    font_heading: "'Noto Sans SC', sans-serif",
    font_body: "'Noto Sans SC', sans-serif",
    layout: "bold_contrast",
    hero_align: "left",
    card_style: "dark_card",
    spacing: "balanced",
    decorative: "diagonal_stripes",
    animation: "sharp_slide",
    personality_traits: ["创新", "辩论力", "好奇心", "魅力"],
  },
  "ESFP": {
    name: "表演型",
    description: "热情、视觉系、图片为主",
    primary_color: "#e91e63",
    secondary_color: "#fff176",
    accent_color: "#00bcd4",
    text_color: "#2c2c2c",
    bg_color: "#ffffff",
    font_heading: "'Noto Sans SC', sans-serif",
    font_body: "'Noto Sans SC', sans-serif",
    layout: "visual_heavy",
    hero_align: "full",
    card_style: "photo_card",
    spacing: "tight",
    decorative: "emoji_dots",
    animation: "bouncy_entry",
    personality_traits: ["热情", "表现力", "活在当下", "魅力"],
  },
  "ISFJ": {
    name: "守护型",
    description: "温暖、叙事性强、柔和",
    primary_color: "#5d6d7e",
    secondary_color: "#fdf5e6",
    accent_color: "#cd853f",
    text_color: "#3d3d3d",
    bg_color: "#fdfaf5",
    font_heading: "'Noto Serif SC', Georgia, serif",
    font_body: "'Noto Serif SC', Georgia, serif",
    layout: "narrative_flow",
    hero_align: "center",
    card_style: "warm_card",
    spacing: "relaxed",
    decorative: "flourish_border",
    animation: "gentle_fade",
    personality_traits: ["可靠", "忠诚", "务实", "守护"],
  },
};

export function getStyle(mbtiType: string): MBTIStyle {
  const mbti = mbtiType.toUpperCase();
  return MBTI_STYLES[mbti] || MBTI_STYLES["INFP"];
}

export function generateCss(style: MBTIStyle, mbtiType: string): string {
  const layout = style.layout || "centered";
  
  let base = `/* ============================================
   ${mbtiType} - ${style.name} 风格
   描述：${style.description}
   核心特质：${style.personality_traits.join(' ')}
   ============================================ */

:root {
    --primary: ${style.primary_color};
    --secondary: ${style.secondary_color};
    --accent: ${style.accent_color};
    --text: ${style.text_color};
    --bg: ${style.bg_color};
    --font-heading: ${style.font_heading};
    --font-body: ${style.font_body};
}

/* 重置基础样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    line-height: 1.8;
    -webkit-font-smoothing: antialiased;
}

/* 标题字体 */
h1, h2, h3 {
    font-family: var(--font-heading);
    font-weight: 700;
    line-height: 1.3;
    color: var(--primary);
}

/* ===== 布局系统 ===== */
`;

  // Layout systems
  if (layout === "centered") {
    base += `
.container { max-width: 720px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: center; padding: 80px 0 60px; }
`;
  } else if (layout === "full_width") {
    base += `
.container { max-width: 1100px; margin: 0 auto; padding: 0 32px; }
.hero { text-align: left; padding: 100px 0 80px; }
`;
  } else if (layout === "asymmetric") {
    base += `
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 80px 0 60px; }
.hero-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 48px; align-items: center; }
`;
  } else if (layout === "structured_grid") {
    base += `
.container { max-width: 960px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 60px 0 40px; }
.grid-section { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
`;
  } else if (layout === "bold_contrast") {
    base += `
.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 60px 0 40px; border-left: 6px solid var(--primary); padding-left: 32px; }
`;
  } else if (layout === "visual_heavy") {
    base += `
.container { max-width: 100%; padding: 0; }
.hero { text-align: left; padding: 0; }
.hero-full { width: 100%; height: 70vh; background: var(--primary); }
`;
  } else if (layout === "narrative_flow") {
    base += `
.container { max-width: 680px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: center; padding: 100px 0 80px; }
`;
  } else {
    base += `
.container { max-width: 960px; margin: 0 auto; padding: 0 24px; }
.hero { text-align: left; padding: 60px 0 40px; }
`;
  }

  // Animations
  const anim = style.animation || "subtle_fade";
  if (anim === "subtle_fade") {
    base += `
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: fadeInUp 0.6s ease-out forwards; }
`;
  } else if (anim === "soft_rise") {
    base += `
@keyframes softRise { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: softRise 0.8s ease-out forwards; }
`;
  } else if (anim === "slide_up") {
    base += `
@keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: slideUp 0.5s ease-out forwards; }
`;
  } else if (anim === "playful_bounce") {
    base += `
@keyframes playfulBounce { 0% { opacity: 0; transform: translateY(20px); } 60% { transform: translateY(-8px); } 100% { opacity: 1; transform: translateY(0); } }
.animate-in { animation: playfulBounce 0.6s ease-out forwards; }
`;
  } else if (anim === "crisp_fade") {
    base += `
@keyframes crispFade { from { opacity: 0; } to { opacity: 1; } }
.animate-in { animation: crispFade 0.4s ease-out forwards; }
.section { opacity: 0; }
.section.visible { animation: crispFade 0.5s ease-out forwards; }
`;
  } else if (anim === "sharp_slide") {
    base += `
@keyframes sharpSlide { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
.animate-in { animation: sharpSlide 0.4s ease-out forwards; }
`;
  } else if (anim === "bouncy_entry") {
    base += `
@keyframes bouncyEntry { 0% { opacity: 0; transform: scale(0.95); } 70% { transform: scale(1.02); } 100% { opacity: 1; transform: scale(1); } }
.animate-in { animation: bouncyEntry 0.5s ease-out forwards; }
`;
  } else {
    base += `
@keyframes gentleFade { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-in { animation: gentleFade 0.7s ease-out forwards; }
`;
  }

  // Spacing value
  const spacingMap: Record<string, string> = {
    "generous": "48px 0",
    "relaxed": "36px 0",
    "balanced": "32px 0",
    "compact": "24px 0",
    "varied": "24px 0",
    "tight": "16px 0",
  };
  const spacingVal = spacingMap[style.spacing] || "32px 0";

  // Hero section
  base += `
/* ===== Hero ===== */
.hero-name {
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.02em;
    margin-bottom: 8px;
    font-family: var(--font-heading);
}
.hero-role {
    font-size: 1.1rem;
    color: var(--accent);
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: ${spacingVal};
}
.hero-story {
    font-size: 1.15rem;
    line-height: 2;
    color: var(--text);
    max-width: 600px;
    margin: 0 auto;
    opacity: 0.9;
}
`;

  // Section styles
  base += `
/* ===== 通用Section ===== */
.section { padding: 60px 0; }
.section-title { 
    font-size: 1.8rem; 
    margin-bottom: 32px; 
    position: relative;
    display: inline-block;
}
`;

  // Card styles
  const card = style.card_style || "minimal";
  if (card === "minimal") {
    base += `
.card { 
    background: transparent;
    padding: 24px 0;
    border: none;
    box-shadow: none;
}
`;
  } else if (card === "soft_shadow") {
    base += `
.card {
    background: var(--secondary);
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
`;
  } else if (card === "bold_border") {
    base += `
.card {
    background: var(--secondary);
    padding: 28px;
    border-left: 4px solid var(--primary);
}
`;
  } else if (card === "grid_card") {
    base += `
.card {
    background: white;
    padding: 24px;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
}
`;
  } else if (card === "warm_card") {
    base += `
.card {
    background: var(--secondary);
    padding: 28px;
    border-radius: 12px;
    border: 1px solid rgba(205,133,63,0.2);
}
`;
  } else {
    base += `
.card {
    background: white;
    padding: 24px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
`;
  }

  // Decorative elements
  const deco = style.decorative || "quote_marks";
  if (deco === "quote_marks") {
    base += `
.quote-block {
    position: relative;
    padding: 0 32px;
    margin: 24px 0;
}
.quote-block::before {
    content: '"';
    font-size: 4rem;
    color: var(--accent);
    position: absolute;
    left: 0;
    top: -10px;
    font-family: Georgia, serif;
    opacity: 0.4;
}
`;
  } else if (deco === "bold_lines") {
    base += `
.section-title::after {
    content: '';
    display: block;
    width: 48px;
    height: 3px;
    background: var(--primary);
    margin-top: 12px;
}
`;
  } else if (deco === "flourish_border") {
    base += `
.section-title {
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8px;
}
`;
  }

  // Footer
  base += `
/* ===== Footer ===== */
.footer {
    text-align: center;
    padding: 40px 0;
    border-top: 1px solid rgba(0,0,0,0.08);
    font-size: 0.85rem;
    color: #888;
}
.footer a { color: var(--accent); text-decoration: none; }
`;

  return base;
}

export function recommendMbtiFromContent(
  name: string,
  role: string,
  experiences: string,
  challenges: string,
  insights: string
): { mbti: string; reason: string } {
  const combined = `${experiences} ${challenges} ${insights}`.toLowerCase();
  
  const strategicKw = ["战略", "系统", "架构", "模型", "框架", "分析", "逻辑", "规划", "长期", "本质"];
  const creativeKw = ["创意", "灵感", "感受", "体验", "直觉", "可能", "想象", "探索"];
  const socialKw = ["帮助", "团队", "他人", "影响", "连接", "赋能", "激励", "带领", "沟通"];
  const introKw = ["独自", "独立", "反思", "沉淀", "深度", "内向", "安静"];
  const actionKw = ["行动", "执行", "快", "立即", "现在", "落地", "实践"];
  const visionKw = ["愿景", "未来", "使命", "意义", "价值", "长远", "改变世界"];
  
  const scores: Record<string, number> = {
    "INTJ": 0, "INFJ": 0, "ENFJ": 0, "ENFP": 0, 
    "INFP": 0, "ENTP": 0, "ESFP": 0, "ISFJ": 0
  };
  
  for (const kw of strategicKw) {
    if (combined.includes(kw)) {
      scores["INTJ"]++;
      scores["ENTP"]++;
    }
  }
  for (const kw of creativeKw) {
    if (combined.includes(kw)) {
      scores["INFP"]++;
      scores["ENFP"]++;
    }
  }
  for (const kw of socialKw) {
    if (combined.includes(kw)) {
      scores["ENFJ"]++;
      scores["ISFJ"]++;
    }
  }
  for (const kw of introKw) {
    if (combined.includes(kw)) {
      scores["INFJ"]++;
      scores["INTJ"]++;
      scores["ISFJ"]++;
    }
  }
  for (const kw of actionKw) {
    if (combined.includes(kw)) {
      scores["ESFP"]++;
      scores["ENTP"]++;
    }
  }
  for (const kw of visionKw) {
    if (combined.includes(kw)) {
      scores["INFJ"]++;
      scores["ENFJ"]++;
    }
  }
  
  const maxMbti = Object.entries(scores).reduce(
    (max, [mbti, score]) => (score > max[1] ? [mbti, score] : max),
    ["INFP", 0]
  )[0];
  
  return {
    mbti: maxMbti,
    reason: `Based on content analysis of your experiences and insights.`,
  };
}
