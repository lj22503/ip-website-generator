# IP Website Generator — Monorepo Spec v1

## Overview

Two-track monorepo for Personal IP Website Generator:

| Track | Purpose | Target Users |
|-------|---------|-------------|
| **skill/** | Standalone AI skill for local/offline use | Developers, designers who want self-hosted solution |
| **saas/** | Web SaaS platform with API + hosting | End users who want managed hosted experience |

## Architecture

```
ip-website-generator/
├── SPEC.md                          ← This spec
├── README.md                         ← Quick start
├── LICENSE
│
├── skill/                           ← ⭐ Self-hosted skill track
│   ├── __init__.py
│   ├── core.py                      ← Entry point (app.py)
│   ├── cli.py                       ← Interactive CLI
│   ├── design_systems/
│   │   ├── __init__.py
│   │   ├── registry.py             ← 54 design system metadata
│   │   └── loader.py               ← Loading utilities
│   ├── modules/
│   │   ├── __init__.py
│   │   └── registry.py             ← Content module definitions
│   ├── narrative/
│   │   ├── __init__.py
│   │   ├── generator.py            ← 8-knives evaluation, de-AI
│   │   └── mbti_styles.py          ← MBTI→style mapping
│   └── rendering/
│       ├── __init__.py
│       ├── css_builder.py          ← Design system → CSS variables
│       └── renderer.py             ← HTML rendering
│
├── saas/                            ← 🌐 SaaS platform track
│   ├── __init__.py
│   ├── main.py                      ← FastAPI entry point
│   ├── cli.py                       ← Admin CLI
│   ├── renderer.py                  ← Legacy HTML renderer
│   ├── css_builder.py              ← CSS builder
│   ├── html_renderer.py             ← Full page renderer
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py               ← REST endpoints
│   │   └── auth.py                  ← Auth utilities
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              ← Pydantic models
│   ├── templates/                   ← HTML templates
│   └── static/                      ← CSS, JS, assets
│
├── shared/                          ← Shared code between tracks
│   ├── __init__.py
│   ├── design_systems/              ← Same as skill/design_systems
│   ├── modules/                     ← Same as skill/modules
│   └── narrative/                   ← Same as skill/narrative
│
└── tests/                           ← Shared tests
```

## Skill Track

Self-contained Python skill that runs entirely locally.

### Usage

```bash
# Interactive CLI
python -m skill.core

# Generate from config
python -m skill.core --config mysite.json --design linear.app

# List designs
python -m skill.core --list-designs

# Demo output
python -m skill.core --demo
```

### Design Systems (54)

From popular-web-designs skill:
- Linear, Notion, Stripe, Figma, Apple, Vercel, Framer
- Claude, ElevenLabs, SpaceX, Supabase, Raycast
- Airbnb, Spotify, Coinbase, Revolut, Mintlify
- ... (54 total)

### Content Modules

**Portfolio modules:**
- hero_featured (required) — 精选封面
- about (required) — 关于我
- skills (required) — 技能
- projects (required) — 作品/项目
- contact (required) — 联系
- awards (optional) — 荣誉/奖项
- clients (optional) — 客户/合作伙伴

**Personal site modules:**
- All portfolio modules +
- hero_story (required) — 故事封面
- story (required) — 我的故事 (MBTI-driven)
- blog (optional) — 博客/文章
- life (optional) — 生活瞬间

### MBTI Narrative System

| MBTI | Style | Description |
|------|-------|-------------|
| INFJ | 隐喻型 | 深度疗愈，文学感 |
| INFP | 自传型 | 真诚柔软 |
| ENFJ | 鼓舞型 | 召唤行动 |
| ENFP | 即兴型 | 跳跃生动 |
| INTJ | 战略型 | 冷静洞察 |
| ENTP | 颠覆型 | 爱挑战 |
| ESFP | 表演型 | 活在当下 |
| ISFJ | 守护型 | 温暖务实 |

**Quality pipeline:**
1. 8-knives evaluation (8 dimensions)
2. De-AI-ization detection (7 rules)
3. Ethical review (3 principles)

## SaaS Track

FastAPI-based web platform with:
- REST API for generation
- User authentication
- Custom domain support
- Template marketplace

### API Endpoints

```
POST /api/v1/generate     — Generate website
GET  /api/v1/designs      — List design systems
GET  /api/v1/templates    — List templates
POST /api/v1/preview      — Preview generation
GET  /api/v1/status/{id}  — Check generation status
```

## Shared Spec

The three layers remain unified across both tracks:

```
┌────────────────────────────────────────────┐
│  Style Layer: 54 design systems            │
│  → skill/rendering + saas/css_builder      │
├────────────────────────────────────────────┤
│  Content Layer: Modular content blocks     │
│  → skill/modules + shared/modules           │
├────────────────────────────────────────────┤
│  Narrative Layer: MBTI-driven generation   │
│  → skill/narrative + shared/narrative       │
└────────────────────────────────────────────┘
```
