#!/usr/bin/env python3
"""
Design.md Generator

Generates complete DESIGN.md files from design system registry metadata.
Transfers the rich YAML + narrative format from awesome-design-md.

Usage:
    from design_md_generator import generate_design_md
    md = generate_design_md('claude')
    print(md)
"""

import yaml
from typing import Dict, Optional


# ============================================================
# Brand Knowledge Base (extracted from awesome-design-md)
# ============================================================

BRAND_KNOWLEDGE = {
    "claude": {
        "version": "alpha",
        "name": "Claude",
        "description": 'A warm-canvas editorial interface for Anthropic\'s Claude product. The system anchors on a tinted cream canvas with serif display headlines, warm coral CTAs, and dark navy product surfaces (code editor mockups, model showcase cards). Brand voltage comes from the cream/coral pairing — deliberately warm and humanist where most AI brands use cool blue + slate. Type voice runs a slab-serif display ("Copernicus" / Tiempos Headline) for h1/h2 and a humanist sans for body. The signature Anthropic black-radial-spike mark anchors the wordmark.',
        "colors": {
            "primary": "#cc785c",
            "primary-active": "#a9583e",
            "primary-disabled": "#e6dfd8",
            "ink": "#141413",
            "body": "#3d3d3a",
            "body-strong": "#252523",
            "muted": "#6c6a64",
            "muted-soft": "#8e8b82",
            "hairline": "#e6dfd8",
            "hairline-soft": "#ebe6df",
            "canvas": "#faf9f5",
            "surface-soft": "#f5f0e8",
            "surface-card": "#efe9de",
            "surface-cream-strong": "#e8e0d2",
            "surface-dark": "#181715",
            "surface-dark-elevated": "#252320",
            "surface-dark-soft": "#1f1e1b",
            "on-primary": "#ffffff",
            "on-dark": "#faf9f5",
            "on-dark-soft": "#a09d96",
            "accent-teal": "#5db8a6",
            "accent-amber": "#e8a55a",
            "success": "#5db872",
            "warning": "#d4a017",
            "error": "#c64545",
        },
        "typography": {
            "display-xl": {"fontFamily": "Copernicus, Tiempos Headline, serif", "fontSize": 64, "fontWeight": 400, "lineHeight": 1.05, "letterSpacing": -1.5},
            "display-lg": {"fontFamily": "Copernicus, Tiempos Headline, serif", "fontSize": 48, "fontWeight": 400, "lineHeight": 1.1, "letterSpacing": -1},
            "display-md": {"fontFamily": "Copernicus, Tiempos Headline, serif", "fontSize": 36, "fontWeight": 400, "lineHeight": 1.15, "letterSpacing": -0.5},
            "display-sm": {"fontFamily": "Copernicus, Tiempos Headline, serif", "fontSize": 28, "fontWeight": 400, "lineHeight": 1.2, "letterSpacing": -0.3},
            "title-lg": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 22, "fontWeight": 500, "lineHeight": 1.3, "letterSpacing": 0},
            "title-md": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 18, "fontWeight": 500, "lineHeight": 1.4, "letterSpacing": 0},
            "title-sm": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 16, "fontWeight": 500, "lineHeight": 1.4, "letterSpacing": 0},
            "body-md": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 16, "fontWeight": 400, "lineHeight": 1.55, "letterSpacing": 0},
            "body-sm": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 14, "fontWeight": 400, "lineHeight": 1.55, "letterSpacing": 0},
            "caption": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 13, "fontWeight": 500, "lineHeight": 1.4, "letterSpacing": 0},
            "caption-uppercase": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 12, "fontWeight": 500, "lineHeight": 1.4, "letterSpacing": 1.5},
            "code": {"fontFamily": "JetBrains Mono, ui-monospace, monospace", "fontSize": 14, "fontWeight": 400, "lineHeight": 1.6, "letterSpacing": 0},
            "button": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 1, "letterSpacing": 0},
            "nav-link": {"fontFamily": "StyreneB, Inter, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 1.4, "letterSpacing": 0},
        },
        "rounded": {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "pill": 9999, "full": 9999},
        "spacing": {"xxs": 4, "xs": 8, "sm": 12, "md": 16, "lg": 24, "xl": 32, "xxl": 48, "section": 96},
        "components": {
            "button-primary": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.button}", "rounded": "{rounded.md}", "padding": "12px 20px", "height": 40},
            "button-secondary": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.button}", "rounded": "{rounded.md}", "padding": "12px 20px", "height": 40},
            "feature-card": {"backgroundColor": "{colors.surface-card}", "textColor": "{colors.ink}", "typography": "{typography.title-md}", "rounded": "{rounded.lg}", "padding": 32},
            "top-nav": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.nav-link}", "height": 64},
            "hero-band": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.display-xl}", "padding": 96},
            "text-input": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.md}", "padding": "10px 14px", "height": 40},
            "footer": {"backgroundColor": "{colors.surface-dark}", "textColor": "{colors.on-dark-soft}", "typography": "{typography.body-sm}", "padding": 64},
        },
        "overview": """Claude.com is the warmest, most editorial interface in the AI-product category. The base atmosphere is a **tinted cream canvas** (`{colors.canvas}` — #faf9f5) — distinctly warm, deliberately not the cool gray-white that every other AI brand uses. Headlines run a **slab-serif display** ("Copernicus" / Tiempos Headline) at weight 400 with negative letter-spacing, paired with **StyreneB / Inter** body sans. The combination feels like a literary publication, not a SaaS marketing page.

Brand voltage comes from the **cream + coral pairing** — coral (`{colors.primary}` — #cc785c) is the signature Anthropic accent, used on every primary CTA, on the brand wordmark, and on full-bleed callout cards. The coral is warm, slightly muted, never cyan/blue — a deliberate counter-positioning against OpenAI's cool slate, Google's saturated blue, and Microsoft's corporate cyan.

The system has three surface modes that alternate page-by-page:
1. **Cream canvas** (`{colors.canvas}`) — default body floor
2. **Light cream cards** (`{colors.surface-card}`) — feature card backgrounds
3. **Dark navy product surfaces** (`{colors.surface-dark}`) — code editor mockups, model showcase cards, pre-footer CTAs, footer itself

The dark surfaces are where Claude shows its product chrome — code blocks, terminal output, model comparison tables, agentic-flow diagrams. The cream-to-dark contrast is the page's pacing rhythm.""",
    },
    "linear.app": {
        "version": "alpha",
        "name": "Linear",
        "description": "A near-black product-focused marketing canvas built around #010102 (the deepest dark surface of any tool in this collection), light gray text (#f7f8f8), and the signature Linear lavender-blue (#5e6ad2) used as the single chromatic accent. The system reads as software-craft documentation: dense, technical, and quietly luxurious. Display type is set in the Linear custom sans (SF Pro Display fallback) at 500–700 with measured negative tracking. Cards live as charcoal panels (#0f1011) with hairline borders. The accent lavender appears on the brand mark, focus rings, and a few intentional CTAs — never decoratively. Page rhythm leans on product UI screenshots framed in dark panels rather than atmospheric color.",
        "colors": {
            "primary": "#5e6ad2",
            "on-primary": "#ffffff",
            "primary-hover": "#828fff",
            "primary-focus": "#5e69d1",
            "ink": "#f7f8f8",
            "ink-muted": "#d0d6e0",
            "ink-subtle": "#8a8f98",
            "ink-tertiary": "#62666d",
            "canvas": "#010102",
            "surface-1": "#0f1011",
            "surface-2": "#141516",
            "surface-3": "#18191a",
            "surface-4": "#191a1b",
            "hairline": "#23252a",
            "hairline-strong": "#34343a",
            "hairline-tertiary": "#3e3e44",
            "inverse-canvas": "#ffffff",
            "inverse-surface-1": "#f5f6f6",
            "inverse-surface-2": "#f6f7f7",
            "inverse-ink": "#000000",
            "brand-secure": "#7a7fad",
            "semantic-success": "#27a644",
            "semantic-overlay": "#000000",
        },
        "typography": {
            "display-xl": {"fontFamily": "Linear Display, SF Pro Display, system-ui, sans-serif", "fontSize": 80, "fontWeight": 600, "lineHeight": 1.05, "letterSpacing": -3.0},
            "display-lg": {"fontFamily": "Linear Display, SF Pro Display, system-ui, sans-serif", "fontSize": 56, "fontWeight": 600, "lineHeight": 1.10, "letterSpacing": -1.8},
            "display-md": {"fontFamily": "Linear Display, SF Pro Display, system-ui, sans-serif", "fontSize": 40, "fontWeight": 600, "lineHeight": 1.15, "letterSpacing": -1.0},
            "headline": {"fontFamily": "Linear Display, SF Pro Display, system-ui, sans-serif", "fontSize": 28, "fontWeight": 600, "lineHeight": 1.20, "letterSpacing": -0.6},
            "card-title": {"fontFamily": "Linear Display, SF Pro Display, system-ui, sans-serif", "fontSize": 22, "fontWeight": 500, "lineHeight": 1.25, "letterSpacing": -0.4},
            "subhead": {"fontFamily": "Linear Display, SF Pro Display, system-ui, sans-serif", "fontSize": 20, "fontWeight": 400, "lineHeight": 1.40, "letterSpacing": -0.2},
            "body-lg": {"fontFamily": "Linear Text, SF Pro Text, system-ui, sans-serif", "fontSize": 18, "fontWeight": 400, "lineHeight": 1.50, "letterSpacing": -0.1},
            "body": {"fontFamily": "Linear Text, SF Pro Text, system-ui, sans-serif", "fontSize": 16, "fontWeight": 400, "lineHeight": 1.50, "letterSpacing": -0.05},
            "body-sm": {"fontFamily": "Linear Text, SF Pro Text, system-ui, sans-serif", "fontSize": 14, "fontWeight": 400, "lineHeight": 1.50, "letterSpacing": 0},
            "caption": {"fontFamily": "Linear Text, SF Pro Text, system-ui, sans-serif", "fontSize": 12, "fontWeight": 400, "lineHeight": 1.40, "letterSpacing": 0},
            "button": {"fontFamily": "Linear Text, SF Pro Text, system-ui, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 1.20, "letterSpacing": 0},
            "eyebrow": {"fontFamily": "Linear Text, SF Pro Text, system-ui, sans-serif", "fontSize": 13, "fontWeight": 500, "lineHeight": 1.30, "letterSpacing": 0.4},
            "mono": {"fontFamily": "Linear Mono, ui-monospace, SF Mono, Menlo, monospace", "fontSize": 13, "fontWeight": 400, "lineHeight": 1.50, "letterSpacing": 0},
        },
        "rounded": {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "xxl": 24, "pill": 9999, "full": 9999},
        "spacing": {"xxs": 4, "xs": 8, "sm": 12, "md": 16, "lg": 24, "xl": 32, "xxl": 48, "section": 96},
        "components": {
            "button-primary": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.button}", "rounded": "{rounded.md}", "padding": "8px 14px"},
            "button-secondary": {"backgroundColor": "{colors.surface-1}", "textColor": "{colors.ink}", "typography": "{typography.button}", "rounded": "{rounded.md}", "padding": "8px 14px"},
            "pricing-card": {"backgroundColor": "{colors.surface-1}", "textColor": "{colors.ink}", "typography": "{typography.body}", "rounded": "{rounded.lg}", "padding": 24},
            "feature-card": {"backgroundColor": "{colors.surface-1}", "textColor": "{colors.ink}", "typography": "{typography.body}", "rounded": "{rounded.lg}", "padding": 24},
            "product-screenshot-card": {"backgroundColor": "{colors.surface-1}", "textColor": "{colors.ink}", "typography": "{typography.body}", "rounded": "{rounded.xl}", "padding": 24},
            "top-nav": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-sm}", "rounded": "{rounded.xs}", "height": 56},
            "text-input": {"backgroundColor": "{colors.surface-1}", "textColor": "{colors.ink}", "typography": "{typography.body}", "rounded": "{rounded.md}", "padding": "8px 12px"},
            "cta-banner": {"backgroundColor": "{colors.surface-1}", "textColor": "{colors.ink}", "typography": "{typography.headline}", "rounded": "{rounded.lg}", "padding": 48},
            "footer": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink-subtle}", "typography": "{typography.caption}", "rounded": "{rounded.xs}", "padding": "64px 32px"},
        },
        "overview": """Linear's marketing canvas is the deepest dark surface in this collection — `{colors.canvas}` is #010102, essentially pure black with a faint blue tint. On top sits a four-step surface ladder (`{colors.surface-1}` through `{colors.surface-4}`) for cards, panels, and lifted tiles, with hairline borders running from `{colors.hairline}` (#23252a) up through `{colors.hairline-strong}` and `{colors.hairline-tertiary}`. Light gray text (`{colors.ink}` #f7f8f8) carries the body and headlines.

The single chromatic accent is **Linear lavender-blue** `{colors.primary}` (#5e6ad2) — used on the brand mark, focus rings, and the primary CTA button. A lighter hover state (`{colors.primary-hover}` #828fff) and a focus-tinted variant (`{colors.primary-focus}` #5e69d1) extend the same hue. Linear avoids saturated greens, oranges, reds, etc. on the marketing canvas — the only semantic color is `{colors.semantic-success}` (#27a644) for status pills and the rare success indicator.

Display type runs Linear's custom sans (with `SF Pro Display` fallback) at weight 500–700 with negative letter-spacing scaling from -3.0px at 80px down to 0 at body. The body family is Linear's text cut, and a Linear Mono is reserved for code snippets in product screenshots.

The page rhythm is **dense product screenshots** — Linear's marketing leads with high-fidelity captures of the product UI (issue list, project view, dashboard) framed in `{colors.surface-1}` panels with `{rounded.xl}` 16px corners. The chrome is intentionally minimal so the app screenshots can do the heavy lifting.""",
    },
    "notion": {
        "version": "alpha",
        "name": "Notion",
        "description": "Notion presents itself as the all-in-one workspace through a confident, illustration-rich brand voice — anchored by a deep navy hero band ({colors.brand-navy}) decorated with brand-colored sticky-note dots and mesh wire illustrations, a signature purple pill primary CTA ({colors.primary}), and a rich palette of pastel-tinted feature cards that echo the colorful database properties of the live product. The system uses a Notion-Sans (Inter-based) typeface across every UI surface, anchors a 4-tier pricing comparison (Free / Plus / Business / Enterprise), and presents the live workspace UI mockup directly inside the hero band. Coverage spans homepage, Enterprise, Product AI, Product Agents, Startups, and Pricing surfaces.",
        "colors": {
            "primary": "#5645d4",
            "primary-pressed": "#4534b3",
            "primary-deep": "#3a2a99",
            "on-primary": "#ffffff",
            "brand-navy": "#0a1530",
            "brand-navy-deep": "#070f24",
            "brand-navy-mid": "#1a2a52",
            "link-blue": "#0075de",
            "link-blue-pressed": "#005bab",
            "brand-orange": "#dd5b00",
            "brand-orange-deep": "#793400",
            "brand-pink": "#ff64c8",
            "brand-pink-deep": "#a02e6d",
            "brand-purple": "#7b3ff2",
            "brand-purple-300": "#d6b6f6",
            "brand-purple-800": "#391c57",
            "brand-teal": "#2a9d99",
            "brand-green": "#1aae39",
            "brand-yellow": "#f5d75e",
            "brand-brown": "#523410",
            "card-tint-peach": "#ffe8d4",
            "card-tint-rose": "#fde0ec",
            "card-tint-mint": "#d9f3e1",
            "card-tint-lavender": "#e6e0f5",
            "card-tint-sky": "#dcecfa",
            "card-tint-yellow": "#fef7d6",
            "card-tint-yellow-bold": "#f9e79f",
            "card-tint-cream": "#f8f5e8",
            "card-tint-gray": "#f0eeec",
            "canvas": "#ffffff",
            "surface": "#f6f5f4",
            "surface-soft": "#fafaf9",
            "hairline": "#e5e3df",
            "hairline-soft": "#ede9e4",
            "hairline-strong": "#c8c4be",
            "ink-deep": "#000000",
            "ink": "#1a1a1a",
            "charcoal": "#37352f",
            "slate": "#5d5b54",
            "steel": "#787671",
            "stone": "#a4a097",
            "muted": "#bbb8b1",
            "on-dark": "#ffffff",
            "on-dark-muted": "#a4a097",
            "semantic-success": "#1aae39",
            "semantic-warning": "#dd5b00",
            "semantic-error": "#e03131",
        },
        "typography": {
            "hero-display": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 80, "fontWeight": 600, "lineHeight": 1.05, "letterSpacing": -2},
            "display-lg": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 56, "fontWeight": 600, "lineHeight": 1.10, "letterSpacing": -1},
            "heading-1": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 48, "fontWeight": 600, "lineHeight": 1.15, "letterSpacing": -0.5},
            "heading-2": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 36, "fontWeight": 600, "lineHeight": 1.20, "letterSpacing": -0.5},
            "heading-3": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 28, "fontWeight": 600, "lineHeight": 1.25, "letterSpacing": 0},
            "heading-4": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 22, "fontWeight": 600, "lineHeight": 1.30, "letterSpacing": 0},
            "heading-5": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 18, "fontWeight": 600, "lineHeight": 1.40, "letterSpacing": 0},
            "subtitle": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 18, "fontWeight": 400, "lineHeight": 1.50, "letterSpacing": 0},
            "body-md": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 16, "fontWeight": 400, "lineHeight": 1.55, "letterSpacing": 0},
            "body-md-medium": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 16, "fontWeight": 500, "lineHeight": 1.55, "letterSpacing": 0},
            "body-sm": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 14, "fontWeight": 400, "lineHeight": 1.50, "letterSpacing": 0},
            "body-sm-medium": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 1.50, "letterSpacing": 0},
            "caption": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 13, "fontWeight": 400, "lineHeight": 1.40, "letterSpacing": 0},
            "caption-bold": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 13, "fontWeight": 600, "lineHeight": 1.40, "letterSpacing": 0},
            "micro": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 12, "fontWeight": 500, "lineHeight": 1.40, "letterSpacing": 0},
            "micro-uppercase": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 11, "fontWeight": 600, "lineHeight": 1.40, "letterSpacing": 1},
            "button-md": {"fontFamily": "Notion Sans, Inter, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 1.30, "letterSpacing": 0},
        },
        "rounded": {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "xxl": 20, "xxxl": 24, "full": 9999},
        "spacing": {"xxs": 4, "xs": 8, "sm": 12, "md": 16, "lg": 20, "xl": 24, "xxl": 32, "xxxl": 40, "section-sm": 48, "section": 64, "section-lg": 96, "hero": 120},
        "components": {
            "button-primary": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.button-md}", "rounded": "{rounded.md}", "padding": "10px 18px"},
            "button-dark": {"backgroundColor": "{colors.ink-deep}", "textColor": "{colors.on-dark}", "typography": "{typography.button-md}", "rounded": "{rounded.md}", "padding": "10px 18px"},
            "button-secondary": {"backgroundColor": "transparent", "textColor": "{colors.ink}", "typography": "{typography.button-md}", "rounded": "{rounded.md}", "padding": "10px 18px", "border": "1px solid {colors.hairline-strong}"},
            "card-base": {"backgroundColor": "{colors.canvas}", "rounded": "{rounded.lg}", "padding": "{spacing.xl}", "border": "1px solid {colors.hairline}"},
            "card-feature": {"backgroundColor": "{colors.canvas}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}", "border": "1px solid {colors.hairline}"},
            "card-feature-yellow-bold": {"backgroundColor": "{colors.card-tint-yellow-bold}", "textColor": "{colors.charcoal}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}"},
            "card-feature-peach": {"backgroundColor": "{colors.card-tint-peach}", "textColor": "{colors.charcoal}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}"},
            "card-feature-rose": {"backgroundColor": "{colors.card-tint-rose}", "textColor": "{colors.charcoal}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}"},
            "card-feature-mint": {"backgroundColor": "{colors.card-tint-mint}", "textColor": "{colors.charcoal}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}"},
            "card-feature-sky": {"backgroundColor": "{colors.card-tint-sky}", "textColor": "{colors.charcoal}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}"},
            "card-feature-lavender": {"backgroundColor": "{colors.card-tint-lavender}", "textColor": "{colors.charcoal}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}"},
            "pricing-card": {"backgroundColor": "{colors.canvas}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}", "border": "1px solid {colors.hairline}"},
            "pricing-card-featured": {"backgroundColor": "{colors.surface}", "rounded": "{rounded.lg}", "padding": "{spacing.xxl}", "border": "2px solid {colors.primary}"},
            "text-input": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.md}", "padding": "{spacing.sm} {spacing.md}", "border": "1px solid {colors.hairline-strong}", "height": 44},
            "search-pill": {"backgroundColor": "{colors.surface}", "textColor": "{colors.steel}", "typography": "{typography.body-md}", "rounded": "{rounded.md}", "padding": "{spacing.sm} {spacing.md}", "height": 44, "border": "1px solid {colors.hairline}"},
            "pill-tab-active": {"backgroundColor": "{colors.ink-deep}", "textColor": "{colors.on-dark}", "rounded": "{rounded.full}", "border": "1px solid {colors.ink-deep}"},
            "badge-purple": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.caption-bold}", "rounded": "{rounded.full}", "padding": "4px 10px"},
            "hero-band-dark": {"backgroundColor": "{colors.brand-navy}", "textColor": "{colors.on-dark}", "rounded": "0", "padding": "{spacing.hero}"},
            "cta-banner-light": {"backgroundColor": "{colors.surface}", "textColor": "{colors.ink}", "rounded": "{rounded.lg}", "padding": "{spacing.section}"},
            "footer-region": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.charcoal}", "typography": "{typography.body-sm}", "padding": "{spacing.section} {spacing.xxl}", "border": "1px solid {colors.hairline}"},
        },
        "overview": """Notion presents itself as the all-in-one workspace through a confident, illustration-rich brand voice. The homepage opens with **"Meet the night shift."** rendered centered over a deep navy hero band ({colors.brand-navy}), decorated with brand-colored sticky-note dots and mesh wire illustrations scattered around the headline. The signature **purple pill primary CTA** ({colors.primary}) "Get Notion free" sits at the visual center, paired with an outlined "Request a demo" secondary. Below the buttons, a real Notion workspace UI mockup card (the "Ramp HQ" kanban board) breaks out of the hero band with a deep diffuse drop shadow.

Below the hero, the page cycles through a distinctive sequence of feature sections: a dense sticky-note "Keep work moving 24/7" panel with red/blue/green/purple/teal status icons; a **bold yellow** ({colors.card-tint-yellow-bold}) "Ask your on-demand assistants" banner card flanked by orange/rose/mint pastel feature tiles showing assistant UI mockups; and a "Bring all your work together" 3-column grid with brand-colored mockups (sky-blue tutorial card, light Notion calendar, brown/rust testimonial slate). The pricing page renders 4 tiers (Free / Plus / Business / Enterprise) horizontally with one tier featured (purple-bordered) and a dense feature comparison table running below.

The system uses a Notion-Sans typeface (Inter-based) across every UI surface — humanist-geometric character that pairs naturally with the colorful illustrations. Buttons are `{rounded.md}` (8px) rectangles, NOT pills — distinguishing Notion's sober rectangular geometry from competitors that use pills universally. Cards use `{rounded.lg}` (12px) consistently.""",
    },
    "stripe": {
        "version": "alpha",
        "name": "Stripe Inspired",
        "description": "An inspired interpretation of Stripe's design language — a financial-infrastructure brand built on a deep navy ink, an electric indigo primary, and a recurring atmospheric gradient mesh that occupies the upper third of nearly every marketing page. The system pairs the proprietary Sohne family at thin (300) weights with negative letter-spacing for editorial-density display headlines, and uses tabular-figure body type where money and numerics matter. Buttons are tight-radius pills, cards live on near-white surfaces, and the dashboard track flips polarity to a familiar dark-app shell.",
        "colors": {
            "primary": "#533afd",
            "primary-deep": "#4434d4",
            "primary-press": "#2e2b8c",
            "primary-soft": "#665efd",
            "primary-bg-subdued-hover": "#b9b9f9",
            "brand-dark-900": "#1c1e54",
            "ink": "#0d253d",
            "ink-secondary": "#273951",
            "ink-mute": "#64748d",
            "ink-mute-2": "#61718a",
            "on-primary": "#ffffff",
            "canvas": "#ffffff",
            "canvas-soft": "#f6f9fc",
            "canvas-cream": "#f5e9d4",
            "hairline": "#e3e8ee",
            "hairline-input": "#a8c3de",
            "ruby": "#ea2261",
            "magenta": "#f96bee",
            "lemon": "#9b6829",
            "shadow-blue": "#003770",
        },
        "typography": {
            "display-xxl": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 56, "fontWeight": 300, "lineHeight": 1.03, "letterSpacing": -1.4, "fontFeature": "ss01"},
            "display-xl": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 48, "fontWeight": 300, "lineHeight": 1.15, "letterSpacing": -0.96, "fontFeature": "ss01"},
            "display-lg": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 32, "fontWeight": 300, "lineHeight": 1.1, "letterSpacing": -0.64, "fontFeature": "ss01"},
            "display-md": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 26, "fontWeight": 300, "lineHeight": 1.12, "letterSpacing": -0.26, "fontFeature": "ss01"},
            "heading-lg": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 22, "fontWeight": 300, "lineHeight": 1.1, "letterSpacing": -0.22, "fontFeature": "ss01"},
            "heading-md": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 20, "fontWeight": 300, "lineHeight": 1.4, "letterSpacing": -0.2, "fontFeature": "ss01"},
            "heading-sm": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 18, "fontWeight": 300, "lineHeight": 1.4, "letterSpacing": 0, "fontFeature": "ss01"},
            "body-lg": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 16, "fontWeight": 300, "lineHeight": 1.4, "letterSpacing": 0, "fontFeature": "ss01"},
            "body-md": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 15, "fontWeight": 300, "lineHeight": 1.4, "letterSpacing": 0, "fontFeature": "ss01"},
            "body-tabular": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 14, "fontWeight": 300, "lineHeight": 1.4, "letterSpacing": -0.42, "fontFeature": "tnum"},
            "button-md": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 16, "fontWeight": 400, "lineHeight": 1.0, "letterSpacing": 0, "fontFeature": "ss01"},
            "button-sm": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 14, "fontWeight": 400, "lineHeight": 1.0, "letterSpacing": 0, "fontFeature": "ss01"},
            "caption": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 13, "fontWeight": 400, "lineHeight": 1.4, "letterSpacing": -0.39, "fontFeature": "tnum"},
            "micro": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 11, "fontWeight": 300, "lineHeight": 1.4, "letterSpacing": 0, "fontFeature": "ss01"},
            "micro-cap": {"fontFamily": "sohne-var, 'SF Pro Display', system-ui, -apple-system, sans-serif", "fontSize": 10, "fontWeight": 400, "lineHeight": 1.15, "letterSpacing": 0.1, "fontFeature": "ss01"},
        },
        "rounded": {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "pill": 9999},
        "spacing": {"xxs": 2, "xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "xxl": 32, "huge": 64},
        "components": {
            "button-primary-pill": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.button-md}", "rounded": "{rounded.pill}", "padding": "8px 16px"},
            "button-secondary": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.primary}", "typography": "{typography.button-md}", "rounded": "{rounded.pill}", "padding": "8px 16px"},
            "button-on-dark": {"backgroundColor": "{colors.brand-dark-900}", "textColor": "{colors.on-primary}", "typography": "{typography.button-md}", "rounded": "{rounded.pill}", "padding": "8px 16px"},
            "text-input": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.sm}", "padding": "8px 12px"},
            "card-feature-light": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": 32},
            "card-pricing": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": 32},
            "card-pricing-featured": {"backgroundColor": "{colors.brand-dark-900}", "textColor": "{colors.on-primary}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": 32},
            "card-cream-band": {"backgroundColor": "{colors.canvas-cream}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": 32},
            "card-dashboard-mockup": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-tabular}", "rounded": "{rounded.lg}", "padding": 24},
            "pill-tag-soft": {"backgroundColor": "{colors.primary-bg-subdued-hover}", "textColor": "{colors.primary-deep}", "typography": "{typography.micro-cap}", "rounded": "{rounded.pill}", "padding": "4px 8px"},
            "nav-bar-on-mesh": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.xs}", "padding": "16px 24px"},
            "footer-light": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink-mute}", "typography": "{typography.caption}", "rounded": "{rounded.xs}", "padding": "64px 24px"},
        },
        "overview": """Stripe's design language opens with the gradient mesh. A wide horizontal band of pastel cream, sherbet orange, lavender, electric indigo, and ruby pink occupies the upper third of nearly every marketing page — the brand's instantly-recognizable atmospheric backdrop. Type and product UI mockups float above it on `{colors.canvas}` (white), with the gradient acting as both decoration and visual anchor. The lower portion of the page returns to white, with feature explanations on `{colors.canvas-soft}` (a barely-tinted cool off-white) and dashboard product mockups composited as faux IDE/console panels in deep navy.

The color system has two primary roles. **Indigo** (`{colors.primary}` — `#533afd`) is the brand's signature CTA color, used sparingly: one filled pill per band. **Deep navy** (`{colors.ink}` — `#0d253d`) is the universal body text color and the fill of dashboard mockups, the featured pricing tier, and the dark-app surfaces on the dashboard track. Ruby (`{colors.ruby}`) and magenta (`{colors.magenta}`) appear inside the gradient mesh and as accent dots in product UI mockups; they are not used as button colors.

Typography is built around **Sohne** at weight 300 with negative letter-spacing — the brand's editorial-density display signature. Display sizes (32–56px) use -1.4px to -0.64px tracking; body sizes use 0; tabular caption sizes (where money and numerics matter) use the OpenType `tnum` feature plus a tightening -0.36 to -0.42px tracking. The `ss01` stylistic set is enabled across all roles.""",
    },
    "vercel": {
        "version": "alpha",
        "name": "Vercel Inspired",
        "description": "An inspired interpretation of Vercel's design language — a developer-platform brand whose surface is a stark black-and-ink duet on near-white canvas, broken at hero scale by a multi-color mesh gradient (cyan / blue / magenta / amber) that acts as the entire decorative system, paired with a custom geometric sans for headlines and a monospaced caption face for technical labels.",
        "colors": {
            "primary": "#171717",
            "on-primary": "#ffffff",
            "ink": "#171717",
            "body": "#4d4d4d",
            "mute": "#888888",
            "hairline": "#ebebeb",
            "hairline-strong": "#a1a1a1",
            "canvas": "#ffffff",
            "canvas-soft": "#fafafa",
            "canvas-soft-2": "#f5f5f5",
            "link": "#0070f3",
            "link-deep": "#0761d1",
            "link-bg-soft": "#d3e5ff",
            "success": "#0070f3",
            "error": "#ee0000",
            "error-soft": "#f7d4d6",
            "error-deep": "#c50000",
            "warning": "#f5a623",
            "warning-soft": "#ffefcf",
            "warning-deep": "#ab570a",
            "violet": "#7928ca",
            "violet-soft": "#d8ccf1",
            "violet-deep": "#4c2889",
            "cyan": "#50e3c2",
            "cyan-soft": "#aaffec",
            "cyan-deep": "#29bc9b",
            "highlight-pink": "#ff0080",
            "highlight-magenta": "#eb367f",
            "gradient-develop-start": "#007cf0",
            "gradient-develop-end": "#00dfd8",
            "gradient-preview-start": "#7928ca",
            "gradient-preview-end": "#ff0080",
            "gradient-ship-start": "#ff4d4d",
            "gradient-ship-end": "#f9cb28",
            "selection-bg": "#171717",
            "selection-fg": "#f2f2f2",
        },
        "typography": {
            "display-xl": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 48, "fontWeight": 600, "lineHeight": 48, "letterSpacing": -2.4},
            "display-lg": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 32, "fontWeight": 600, "lineHeight": 40, "letterSpacing": -1.28},
            "display-md": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 24, "fontWeight": 600, "lineHeight": 32, "letterSpacing": -0.96},
            "display-sm": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 20, "fontWeight": 600, "lineHeight": 28, "letterSpacing": -0.6},
            "body-lg": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 18, "fontWeight": 400, "lineHeight": 28, "letterSpacing": 0},
            "body-md": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 16, "fontWeight": 400, "lineHeight": 24, "letterSpacing": 0},
            "body-md-strong": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 16, "fontWeight": 500, "lineHeight": 24, "letterSpacing": 0},
            "body-sm": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 14, "fontWeight": 400, "lineHeight": 20, "letterSpacing": -0.28},
            "body-sm-strong": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 20, "letterSpacing": -0.28},
            "caption": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 12, "fontWeight": 400, "lineHeight": 16, "letterSpacing": 0},
            "caption-mono": {"fontFamily": "Geist Mono, ui-monospace, SFMono-Regular, Menlo, Monaco, monospace", "fontSize": 12, "fontWeight": 400, "lineHeight": 16, "letterSpacing": 0},
            "code": {"fontFamily": "Geist Mono, ui-monospace, SFMono-Regular, Menlo, Monaco, monospace", "fontSize": 13, "fontWeight": 400, "lineHeight": 20, "letterSpacing": 0},
            "button-md": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 14, "fontWeight": 500, "lineHeight": 20, "letterSpacing": 0},
            "button-lg": {"fontFamily": "Geist, Inter, system-ui, -apple-system, sans-serif", "fontSize": 16, "fontWeight": 500, "lineHeight": 24, "letterSpacing": 0},
        },
        "rounded": {"none": 0, "xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "pill-sm": 64, "pill": 100, "full": 9999},
        "spacing": {"xxs": 4, "xs": 8, "sm": 12, "md": 16, "lg": 24, "xl": 32, "2xl": 40, "3xl": 48, "4xl": 64, "5xl": 96, "6xl": 128, "section": 192},
        "components": {
            "nav-bar": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-sm}", "height": 64, "padding": "{spacing.sm} {spacing.lg}"},
            "nav-link": {"textColor": "{colors.body}", "typography": "{typography.body-sm}", "rounded": "{rounded.full}", "padding": "{spacing.xs} {spacing.sm}"},
            "nav-cta-signup": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.body-sm-strong}", "rounded": "{rounded.sm}", "padding": "0px {spacing.xs}", "height": 28},
            "nav-cta-login": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-sm-strong}", "rounded": "{rounded.sm}", "padding": "0px {spacing.xs}", "height": 28},
            "button-primary": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.button-lg}", "rounded": "{rounded.pill}", "padding": "0px {spacing.sm}"},
            "button-secondary": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.button-lg}", "rounded": "{rounded.pill}", "padding": "0px {spacing.sm}"},
            "button-primary-sm": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.button-md}", "rounded": "{rounded.pill}", "padding": "0px {spacing.xs}"},
            "button-secondary-sm": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.button-md}", "rounded": "{rounded.pill}", "padding": "0px {spacing.xs}"},
            "tab-ghost": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-sm}", "rounded": "{rounded.pill-sm}", "padding": "0px {spacing.md}"},
            "card-marketing": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.md}", "padding": "{spacing.lg}"},
            "card-marketing-large": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": "{spacing.xl}"},
            "card-soft": {"backgroundColor": "{colors.canvas-soft}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.md}", "padding": "{spacing.lg}"},
            "template-card": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.md}", "padding": "{spacing.md}"},
            "code-editor-mockup": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.code}", "rounded": "{rounded.md}", "padding": "{spacing.lg}"},
            "form-input": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "borderColor": "{colors.hairline}", "typography": "{typography.body-sm}", "rounded": "{rounded.sm}", "padding": "0px {spacing.sm}", "height": 40},
            "form-input-lg": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "borderColor": "{colors.hairline}", "typography": "{typography.body-md}", "rounded": "{rounded.sm}", "padding": "0px {spacing.sm}", "height": 48},
            "pricing-card": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": "{spacing.xl}"},
            "pricing-card-featured": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.body-md}", "rounded": "{rounded.lg}", "padding": "{spacing.xl}"},
            "hero-band": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.display-xl}", "padding": "{spacing.4xl} {spacing.lg}"},
            "feature-mesh-band": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.ink}", "typography": "{typography.display-lg}", "padding": "{spacing.5xl} {spacing.lg}"},
            "showcase-band-dark": {"backgroundColor": "{colors.primary}", "textColor": "{colors.on-primary}", "typography": "{typography.display-lg}", "padding": "{spacing.5xl} {spacing.lg}"},
            "footer": {"backgroundColor": "{colors.canvas}", "textColor": "{colors.body}", "typography": "{typography.body-sm}", "padding": "{spacing.4xl} {spacing.lg}"},
            "link-inline": {"textColor": "{colors.link}", "typography": "{typography.body-md}"},
        },
        "overview": """Vercel is a developer-platform brand — the page is a deployment dashboard's marketing surface, written for engineers who already know the syntax. It earns that posture with one of the cleanest stark systems on the web: near-white `{colors.canvas-soft}` body background, ink-near-black `{colors.ink}` text, a 200-step gray scale that gives every divider, border, and disabled state its own deliberate step. The only place the brand introduces colour at marketing scale is the multi-stop mesh gradient (`{colors.gradient-develop-start}` → `{colors.gradient-preview-end}` → `{colors.gradient-ship-start}` → cyan / magenta / amber) that floats in atmospheric backdrops, never miniaturised to a swatch. That gradient is the entire decoration system.

Type is the second decisive voice. The brand's own custom geometric sans (Geist) carries display, body, button — everything narrative — at weight 600 for display, 500 for buttons, 400 for body. A matching monospaced face (Geist Mono) carries technical labels: terminal mockups, code blocks, sometimes filename captions. Headlines are sentence-case with aggressive negative letter-spacing (`-2.4px` at 48 px hero) — the brand never letter-spaces positively, never goes uppercase outside of mono labels.

Surfaces use a four-step ladder: `{colors.canvas}` (pure white for cards), `{colors.canvas-soft}` 98% (the page body), `{colors.canvas-soft-2}` 95% (occasional inset region), `{colors.primary}` (the deep ink-near-black used as the polarity-flipped band when a section needs the dark mode treatment). Shadows are exceptionally subtle — every elevated card carries a stacked shadow built from `0px 1px 1px #00000005` + `0px 2px 2px #0000000a` + an inset border. Cards never float on heavy drop-shadow; they sit on the page held by hairline + soft glow.""",
    },
}


# ============================================================
# Inference Engine for Unknown Brands
# ============================================================

def infer_brand_data(registry_data: Dict) -> Dict:
    """Infer full design token data from basic registry metadata."""
    
    name = registry_data.get("name", "Unknown")
    category = registry_data.get("category", "")
    description = registry_data.get("description", "")
    tags = registry_data.get("tags", [])
    mood = registry_data.get("mood", "")
    color_scheme = registry_data.get("color_scheme", "light")
    bg_base = registry_data.get("bg_base", "#ffffff")
    text_base = registry_data.get("text_base", "#000000")
    accent_color = registry_data.get("accent_color", "#000000")
    font_primary = registry_data.get("font_primary", "Inter")
    font_mono = registry_data.get("font_mono", "JetBrains Mono")
    
    # Determine if dark mode
    is_dark = any(x in color_scheme for x in ["dark", "bold"]) or _is_dark_hex(bg_base)
    
    # Build colors based on scheme
    colors = _infer_colors(color_scheme, bg_base, text_base, accent_color, is_dark)
    
    # Build typography
    typography = _infer_typography(font_primary, font_mono, is_dark)
    
    # Standard rounded and spacing
    rounded = {"xs": 4, "sm": 6, "md": 8, "lg": 12, "xl": 16, "pill": 9999, "full": 9999}
    spacing = {"xxs": 4, "xs": 8, "sm": 12, "md": 16, "lg": 24, "xl": 32, "xxl": 48, "section": 96}
    
    # Build components
    components = _infer_components(colors, typography, rounded, is_dark)
    
    # Generate overview
    overview = _generate_overview(name, description, mood, tags, color_scheme, accent_color, is_dark)
    
    return {
        "version": "alpha",
        "name": name,
        "description": description or f"A {category} brand with {color_scheme} aesthetic.",
        "colors": colors,
        "typography": typography,
        "rounded": rounded,
        "spacing": spacing,
        "components": components,
        "overview": overview,
    }


def _is_dark_hex(hex_color: str) -> bool:
    """Check if a hex color is dark."""
    if not hex_color or not isinstance(hex_color, str):
        return False
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return False
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    except:
        return False


def _infer_colors(color_scheme: str, bg_base: str, text_base: str, accent_color: str, is_dark: bool) -> Dict:
    """Infer color palette from basic metadata."""
    
    if is_dark:
        # Dark mode color scheme
        colors = {
            "primary": accent_color,
            "on-primary": "#ffffff",
            "primary-hover": _lighten(accent_color, 20),
            "ink": text_base if text_base != "#ffffff" else "#f5f5f5",
            "body": _muted(text_base if text_base != "#ffffff" else "#d0d0d0", 30),
            "muted": _muted(text_base if text_base != "#ffffff" else "#888888", 40),
            "canvas": bg_base if bg_base else "#0a0a0a",
            "surface-1": _lighten(bg_base if bg_base else "#0a0a0a", 8),
            "surface-2": _lighten(bg_base if bg_base else "#0a0a0a", 15),
            "hairline": _lighten(bg_base if bg_base else "#0a0a0a", 20),
            "hairline-strong": _lighten(bg_base if bg_base else "#0a0a0a", 30),
            "on-dark": "#ffffff",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "error": "#ef4444",
        }
    else:
        # Light mode color scheme
        canvas = bg_base if bg_base and bg_base != "#ffffff" else "#fafafa"
        colors = {
            "primary": accent_color,
            "on-primary": "#ffffff",
            "primary-hover": _darken(accent_color, 15),
            "ink": text_base if text_base != "rgba(0,0,0,0.95)" else "#1a1a1a",
            "body": _muted(text_base if text_base != "rgba(0,0,0,0.95)" else "#4a4a4a", 20),
            "muted": _muted(text_base if text_base != "rgba(0,0,0,0.95)" else "#888888", 40),
            "canvas": canvas,
            "surface-1": _darken(canvas, 5),
            "surface-2": _darken(canvas, 10),
            "hairline": _darken(canvas, 15),
            "hairline-strong": _darken(canvas, 25),
            "on-primary": "#ffffff",
            "success": "#16a34a",
            "warning": "#d97706",
            "error": "#dc2626",
        }
        
        # Add surface variations for light mode
        if "warm" in color_scheme:
            colors["surface-cream"] = "#fef7ed"
            colors["surface-warm"] = _darken(canvas, 3)
    
    return colors


def _muted(hex_color: str, amount: int) -> str:
    """Create a muted version of a hex color."""
    hex_color = hex_color.lstrip('#') if isinstance(hex_color, str) else "888888"
    if len(hex_color) != 6:
        return "#888888"
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, min(255, r + amount)) if r > 128 else max(0, min(255, r - amount))
        g = max(0, min(255, g + amount)) if g > 128 else max(0, min(255, g - amount))
        b = max(0, min(255, b + amount)) if b > 128 else max(0, min(255, b - amount))
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return "#888888"


def _lighten(hex_color: str, amount: int) -> str:
    """Lighten a hex color."""
    hex_color = hex_color.lstrip('#') if isinstance(hex_color, str) else "000000"
    if len(hex_color) != 6:
        return "#ffffff"
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return "#ffffff"


def _darken(hex_color: str, amount: int) -> str:
    """Darken a hex color."""
    hex_color = hex_color.lstrip('#') if isinstance(hex_color, str) else "ffffff"
    if len(hex_color) != 6:
        return "#000000"
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return "#000000"


def _infer_typography(font_primary: str, font_mono: str, is_dark: bool) -> Dict:
    """Infer typography scale from font choices."""
    
    primary = font_primary if font_primary else "Inter"
    mono = font_mono if font_mono else "JetBrains Mono"
    
    # Font stacks
    sans_stack = f"{primary}, Inter, system-ui, -apple-system, sans-serif"
    mono_stack = f"{mono}, ui-monospace, SFMono-Regular, Menlo, Monaco, monospace"
    
    typography = {
        "display-xl": {"fontFamily": sans_stack, "fontSize": 56, "fontWeight": 600, "lineHeight": 1.1, "letterSpacing": -2},
        "display-lg": {"fontFamily": sans_stack, "fontSize": 40, "fontWeight": 600, "lineHeight": 1.15, "letterSpacing": -1.5},
        "display-md": {"fontFamily": sans_stack, "fontSize": 32, "fontWeight": 600, "lineHeight": 1.2, "letterSpacing": -1},
        "display-sm": {"fontFamily": sans_stack, "fontSize": 24, "fontWeight": 600, "lineHeight": 1.25, "letterSpacing": -0.5},
        "heading-lg": {"fontFamily": sans_stack, "fontSize": 22, "fontWeight": 600, "lineHeight": 1.3, "letterSpacing": 0},
        "heading-md": {"fontFamily": sans_stack, "fontSize": 18, "fontWeight": 600, "lineHeight": 1.4, "letterSpacing": 0},
        "heading-sm": {"fontFamily": sans_stack, "fontSize": 16, "fontWeight": 600, "lineHeight": 1.4, "letterSpacing": 0},
        "body-lg": {"fontFamily": sans_stack, "fontSize": 18, "fontWeight": 400, "lineHeight": 1.6, "letterSpacing": 0},
        "body-md": {"fontFamily": sans_stack, "fontSize": 16, "fontWeight": 400, "lineHeight": 1.6, "letterSpacing": 0},
        "body-sm": {"fontFamily": sans_stack, "fontSize": 14, "fontWeight": 400, "lineHeight": 1.5, "letterSpacing": 0},
        "caption": {"fontFamily": sans_stack, "fontSize": 12, "fontWeight": 400, "lineHeight": 1.4, "letterSpacing": 0},
        "button-md": {"fontFamily": sans_stack, "fontSize": 14, "fontWeight": 500, "lineHeight": 1, "letterSpacing": 0},
        "button-sm": {"fontFamily": sans_stack, "fontSize": 12, "fontWeight": 500, "lineHeight": 1, "letterSpacing": 0},
        "code": {"fontFamily": mono_stack, "fontSize": 14, "fontWeight": 400, "lineHeight": 1.6, "letterSpacing": 0},
    }
    
    return typography


def _infer_components(colors: Dict, typography: Dict, rounded: Dict, is_dark: bool) -> Dict:
    """Infer component definitions."""
    
    components = {
        "button-primary": {
            "backgroundColor": "{colors.primary}",
            "textColor": "{colors.on-primary}",
            "typography": "{typography.button-md}",
            "rounded": "{rounded.md}",
            "padding": "10px 18px",
        },
        "button-secondary": {
            "backgroundColor": "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.button-md}",
            "rounded": "{rounded.md}",
            "padding": "10px 18px",
            "border": "1px solid {colors.hairline}" if not is_dark else "1px solid {colors.hairline-strong}",
        },
        "button-ghost": {
            "backgroundColor": "transparent",
            "textColor": "{colors.ink}",
            "typography": "{typography.button-md}",
            "rounded": "{rounded.md}",
            "padding": "8px 12px",
        },
        "card-base": {
            "backgroundColor": "{colors.canvas}",
            "rounded": "{rounded.lg}",
            "padding": "{spacing.lg}",
            "border": "1px solid {colors.hairline}" if not is_dark else "1px solid {colors.hairline-strong}",
        },
        "card-feature": {
            "backgroundColor": "{colors.surface-1}" if is_dark else "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.body-md}",
            "rounded": "{rounded.lg}",
            "padding": "{spacing.xl}",
        },
        "text-input": {
            "backgroundColor": "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.body-md}",
            "rounded": "{rounded.md}",
            "padding": "10px 14px",
            "height": 40,
        },
        "top-nav": {
            "backgroundColor": "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.body-sm}",
            "height": 64,
        },
        "hero-band": {
            "backgroundColor": "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.display-xl}",
            "padding": "{spacing.section}",
        },
        "footer": {
            "backgroundColor": "{colors.surface-1}" if is_dark else "{colors.canvas}",
            "textColor": "{colors.muted}",
            "typography": "{typography.body-sm}",
            "padding": "{spacing.xl}",
        },
        "pricing-card": {
            "backgroundColor": "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.body-md}",
            "rounded": "{rounded.lg}",
            "padding": "{spacing.xl}",
        },
        "pricing-card-featured": {
            "backgroundColor": "{colors.primary}",
            "textColor": "{colors.on-primary}",
            "typography": "{typography.body-md}",
            "rounded": "{rounded.lg}",
            "padding": "{spacing.xl}",
        },
        "badge-pill": {
            "backgroundColor": "{colors.surface-1}" if is_dark else "{colors.canvas}",
            "textColor": "{colors.ink}",
            "typography": "{typography.caption}",
            "rounded": "{rounded.pill}",
            "padding": "4px 10px",
        },
    }
    
    return components


def _generate_overview(name: str, description: str, mood: str, tags: list, color_scheme: str, accent_color: str, is_dark: bool) -> str:
    """Generate an Overview narrative section."""
    
    mood_desc = mood if mood else f"{'dark' if is_dark else 'light'} aesthetic"
    tags_desc = ", ".join(tags[:4]) if tags else "modern"
    
    overview = f"""{name} is a {tags_desc} brand with a {mood_desc}. """

    if is_dark:
        overview += f"""The interface uses a deep, near-black canvas (`{{colors.canvas}}`) as the primary background, with light text (`{{colors.ink}}`) providing strong contrast. The accent color (`{{colors.primary}}` — {accent_color}) is used sparingly for primary CTAs and key interactive elements."""
    else:
        overview += f"""The interface uses a clean, light canvas (`{{colors.canvas}}`) with dark text (`{{colors.ink}}`) for readability. The accent color (`{{colors.primary}}` — {accent_color}) provides brand identity on CTAs and interactive elements."""

    if "gradient" in color_scheme:
        overview += """ A signature gradient system adds depth and brand personality to key sections."""
    
    if "warm" in color_scheme:
        overview += """ The warm color palette creates an inviting, human-centered feel."""

    if "minimal" in tags or "minimal" in color_scheme:
        overview += """ The design emphasizes whitespace, clean typography, and essential elements only — a disciplined minimal approach."""
    
    overview += f"\n\n**Key Characteristics:**\n"
    overview += f"- Brand: {name}\n"
    overview += f"- Aesthetic: {mood_desc}\n"
    overview += f"- Color scheme: {color_scheme}\n"
    overview += f"- Tags: {', '.join(tags[:5]) if tags else 'none'}\n"
    
    return overview


# ============================================================
# DESIGN.md Generator
# ============================================================

def generate_design_md(design_system_id: str, registry_data: Dict = None) -> str:
    """
    Generate a complete DESIGN.md for a design system.
    
    Args:
        design_system_id: The ID of the design system (e.g., 'claude', 'linear.app')
        registry_data: Optional registry data dict. If not provided, will try to load from registry.
    
    Returns:
        Complete DESIGN.md as a string.
    """
    # Get brand knowledge or infer from registry
    if design_system_id in BRAND_KNOWLEDGE:
        data = BRAND_KNOWLEDGE[design_system_id]
    elif registry_data:
        data = infer_brand_data(registry_data)
    else:
        # Try to load from registry
        try:
            from design_systems.registry import get_design_system
            reg = get_design_system(design_system_id)
            if reg:
                data = infer_brand_data(reg)
            else:
                raise ValueError(f"Design system '{design_system_id}' not found in registry")
        except ImportError:
            raise ValueError(f"Could not load design system '{design_system_id}' and no registry_data provided")
    
    # Build YAML frontmatter
    yaml_data = {
        "version": data.get("version", "alpha"),
        "name": data.get("name", design_system_id),
        "description": data.get("description", ""),
        "colors": data.get("colors", {}),
        "typography": data.get("typography", {}),
        "rounded": data.get("rounded", {}),
        "spacing": data.get("spacing", {}),
        "components": data.get("components", {}),
    }
    
    yaml_frontmatter = yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Build narrative sections
    overview = data.get("overview", _generate_overview(
        data.get("name", design_system_id),
        data.get("description", ""),
        "",
        [],
        "light",
        "#000000",
        False
    ))
    
    colors_desc = _generate_colors_section(yaml_data["colors"])
    typography_desc = _generate_typography_section(yaml_data["typography"])
    layout_desc = _generate_layout_section(yaml_data["spacing"])
    shapes_desc = _generate_shapes_section(yaml_data["rounded"])
    components_desc = _generate_components_section(yaml_data["components"])
    
    # Combine
    md = f"""---
{yaml_frontmatter}---

## Overview

{overview}

## Colors

{colors_desc}

## Typography

{typography_desc}

## Layout

{layout_desc}

## Shapes

{shapes_desc}

## Components

{components_desc}
"""
    
    return md


def _generate_colors_section(colors: Dict) -> str:
    """Generate Colors section narrative."""
    if not colors:
        return "Color tokens are defined in the YAML frontmatter above."
    
    sections = []
    
    # Primary & Brand
    if "primary" in colors:
        sections.append("### Brand & Primary")
        sections.append(f"- **Primary** (`{{colors.primary}}` — {colors['primary']}): Primary brand color.")
        if "primary-hover" in colors:
            sections.append(f"- **Primary Hover** (`{{colors.primary-hover}}` — {colors['primary-hover']})")
        if "on-primary" in colors:
            sections.append(f"- **On Primary** (`{{colors.on-primary}}` — {colors['on-primary']}): Text on primary surfaces.")
    
    # Surface colors
    surface_keys = [k for k in colors.keys() if k.startswith("surface") or k in ["canvas", "hairline"]]
    if surface_keys:
        sections.append("\n### Surface")
        for key in surface_keys:
            sections.append(f"- **{key.replace('-', ' ').title()}** (`{{colors.{key}}}` — {colors[key]})")
    
    # Text colors
    text_keys = [k for k in colors.keys() if k.startswith("ink") or k in ["body", "muted", "on-dark"]]
    if text_keys:
        sections.append("\n### Text")
        for key in text_keys:
            sections.append(f"- **{key.replace('-', ' ').title()}** (`{{colors.{key}}}` — {colors[key]})")
    
    # Semantic
    semantic_keys = [k for k in colors.keys() if k.startswith("success") or k.startswith("warning") or k.startswith("error")]
    if semantic_keys:
        sections.append("\n### Semantic")
        for key in semantic_keys:
            sections.append(f"- **{key.replace('-', ' ').title()}** (`{{colors.{key}}}` — {colors[key]})")
    
    return "\n".join(sections) if sections else "See color tokens in YAML frontmatter."


def _generate_typography_section(typography: Dict) -> str:
    """Generate Typography section narrative."""
    if not typography:
        return "Typography tokens are defined in the YAML frontmatter above."
    
    lines = ["### Font Family", "Primary typeface family and fallback stack.", ""]
    lines.append("### Hierarchy")
    lines.append("")
    lines.append("| Token | Size | Weight | Line Height | Letter Spacing | Use |")
    lines.append("|-------|------|--------|-------------|----------------|-----|")
    
    # Sort by size descending
    sorted_tokens = sorted(typography.items(), key=lambda x: x[1].get("fontSize", 0), reverse=True)
    
    for token, props in sorted_tokens:
        size = props.get("fontSize", "-")
        weight = props.get("fontWeight", "-")
        lh = props.get("lineHeight", "-")
        ls = props.get("letterSpacing", "-")
        use = f"`{token}` token usage"
        lines.append(f"| `{token}` | {size}px | {weight} | {lh} | {ls}px | {use} |")
    
    return "\n".join(lines)


def _generate_layout_section(spacing: Dict) -> str:
    """Generate Layout section narrative."""
    if not spacing:
        return "Spacing tokens are defined in the YAML frontmatter above."
    
    lines = ["### Spacing System", ""]
    lines.append("- **Base unit**: 4px.")
    lines.append("- **Tokens** (from front matter):")
    
    for key, val in sorted(spacing.items(), key=lambda x: x[1] if isinstance(x[1], (int, float)) else 9999):
        lines.append(f"  - `{{spacing.{key}}}` {val}px")
    
    return "\n".join(lines)


def _generate_shapes_section(rounded: Dict) -> str:
    """Generate Shapes section narrative."""
    if not rounded:
        return "Rounded tokens are defined in the YAML frontmatter above."
    
    lines = ["### Border Radius Scale", ""]
    lines.append("| Token | Value | Use |")
    lines.append("|-------|-------|-----|")
    
    for key, val in sorted(rounded.items(), key=lambda x: x[1] if isinstance(x[1], (int, float)) else 9999):
        lines.append(f"| `{{rounded.{key}}}` | {val}px | {key} corner radius |")
    
    return "\n".join(lines)


def _generate_components_section(components: Dict) -> str:
    """Generate Components section narrative."""
    if not components:
        return "Component definitions are in the YAML frontmatter above."
    
    lines = []
    
    for comp_name, props in components.items():
        lines.append(f"**`{comp_name}`**")
        if isinstance(props, dict):
            for key, val in props.items():
                lines.append(f"- **{key}**: `{val}`")
        lines.append("")
    
    return "\n".join(lines) if lines else "See component definitions in YAML frontmatter."


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python design_md_generator.py <design_system_id>")
        print("Example: python design_md_generator.py claude")
        sys.exit(1)
    
    design_id = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        md = generate_design_md(design_id)
        
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"Generated: {output_path}")
        else:
            print(md)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)