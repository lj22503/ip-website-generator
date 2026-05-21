# Personal IP Site Generator — 产品规格书

## 产品概述

**一句话**：上传简历/文档 → AI 提取7个模块 → 选择设计系统 → 生成专属个人网站 HTML。

**产品形态**：两条并行路径
- `skill/` — Hermes Skill 安装版（本地运行，CLI 交互）
- `saas/` — Vercel 部署版（Web UI，浏览器直接使用）

**Vercel 部署地址**：`https://ip-website-generator-saas.vercel.app`

---

## 核心架构：Surface × Design System × Component × Template

```
用户场景（Surface）
    ↓
设计系统（Design System） — 54 套视觉风格（popular-web-designs）
    ↓
内容模块（Module） — 7 个内容区块（hero/story/skills/projects/...）
    ↓
外部模板资产（Template） — 44 个 MIT 模板（AI-Animation-Skill）
```

---

## Monorepo 结构

```
ip-website-generator/
├── SPEC.md
├── README.md
├── pyproject.toml
├── .gitignore
│
├── skill/                          # Skill 版本（本地 Python CLI）
│   ├── core.py                    # 主入口（argparse CLI，含 demo 数据）
│   ├── cli.py                     # 交互式 CLI（import 路径需修复）
│   ├── surfaces.py                # Surface 抽象层（4 种用途场景）
│   ├── template_registry.py        # 外部模板资产注册表（11 类，44 个）
│   ├── fetch_templates.py          # 下载 AI-Animation-Skill 模板的脚本
│   ├── __init__.py
│   │
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── renderer.py             # HTML 渲染器（11 个模块渲染函数）
│   │   └── css_builder.py         # CSS 构建器（54 design systems，920行）
│   │
│   ├── narrative/
│   │   ├── __init__.py
│   │   ├── generator.py            # 叙事生成器（4层素材→故事）
│   │   └── mbti_styles.py         # MBTI 16型 → 叙事风格映射
│   │
│   ├── design_systems/
│   │   ├── __init__.py
│   │   ├── registry.py            # 设计系统注册表（54 套元数据）
│   │   └── loader.py
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   └── registry.py            # 内容模块注册表
│   │
│   ├── templates/                  # [待下载] 外部模板资产目录
│   │   ├── ppt-level2/            #  26 个 PPT 动画模板
│   │   ├── ppt-basic/             #   4 个 PPT 基础模板
│   │   └── animation/             #  14 个流程图动画模板
│   │
│   ├── data/
│   │   └── hermes_7modules.json   # Hermes 完整7模块示例数据
│   │
│   ├── examples/                   # 示例 HTML（Hermes 本人内容）
│   │   ├── hermes_personal_site.html
│   │   ├── hermes_portfolio_linear.html
│   │   └── hermes_career_stripe.html
│   │
│   ├── style_packages/             # [未提交] Claude design encapsulation
│   │   ├── SKILL.md
│   │   ├── claude-design-encapsulation.html
│   │   └── claude-design-encapsulation.md
│   │
│   └── design_md_generator.py    # DESIGN.md 生成工具
│
└── saas/                          # SaaS 版本（Next.js + FastAPI）
    ├── main.py
    ├── api/routes.py
    ├── css_builder.py
    ├── html_renderer.py
    ├── renderer.py
    ├── cli.py
    │
    ├── nextjs/
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx
    │   │   ├── page.module.css
    │   │   ├── globals.css
    │   │   └── api/
    │   │       ├── designs/route.ts
    │   │       └── generate/route.ts
    │   ├── lib/
    │   │   ├── css-builder.ts
    │   │   ├── mbti-styles.ts
    │   │   └── renderer.ts
    │   └── types/index.ts
    │
    ├── public/
    │   ├── examples/
    │   └── screenshots/
    │
    └── rendering_modules/
        ├── hero_soul.py
        └── soul_module.py
```

---

## Surface 层（用途场景）

| ID | 名称 | 描述 | 推荐设计系统 |
|----|------|------|------------|
| `landing` | 产品落地页 | 单页产品/个人IP展示 | linear.app, notion, vercel |
| `story` | 个人叙事站 | 故事驱动，适合思想领袖 | notion, claude, airbnb |
| `portfolio` | 作品集 | 项目展示为主 | linear.app, figma, framer |
| `resume` | 数字简历 | 经历和能力为主 | notion, apple, stripe |

---

## 外部模板资产（MIT License — AI-Animation-Skill）

| 类别 | 数量 | 用途 |
|------|------|------|
| PPT-L2 系列1-9 | 26 | 各主题 PPT 动画模板 |
| PPT 基础 | 4 | 通用演示模板 |
| 流程图动画 | 14 | 科普动画、流程说明 |

下载命令：`python skill/core.py --fetch-templates`

---

## 已完成 ✅

### Skill 版本
- `core.py` 完整 CLI（`--list-designs` / `--list-surfaces` / `--list-templates` / `--demo` / `--preview` / `--design` / `--surface`)
- `rendering/renderer.py` — `render_page()` 函数，支持 11 个模块渲染
- `rendering/css_builder.py` — 54 套设计系统完整 CSS 变量
- `surfaces.py` — Surface 抽象层（4 种用途场景，Surface × Template 矩阵）
- `template_registry.py` — 外部模板资产注册表（11 类，44 个文件）
- `fetch_templates.py` — 模板下载脚本
- `hero-label` CSS bug 修复（caption 混用 → 独立样式）
- Demo 模式可正常运行，输出 20,775 bytes 完整 HTML

### SaaS 版本
- `nextjs/app/page.tsx` — 3步向导 UI
- `nextjs/app/api/generate/route.ts` — POST `/api/generate` 生成 HTML
- `nextjs/app/api/designs/route.ts` — GET `/api/designs` 返回设计系统列表

---

## 待修复 🔴

### Skill 版本
- [x] `skill/html_templates/developerfolio/template.html` — story 区块 body 已有，导航栏缺少链接 | ✅ 已修复 → 加条件链接 |
- [ ] `skill/cli.py` — import 路径全部写错
  - `from mbti_styles` → `from narrative.mbti_styles`
  - `from narrative_generator` → `from narrative.generator`
  - `from html_renderer` → `from rendering.renderer`

### SaaS 版本
- [ ] `/api/generate` 响应字段名不一致
- [ ] `saas/nextjs/lib/css-builder.ts` — 仅 10 套设计系统，缺少 44 套

---

## 未完成 🔨

### Skill 版本
- [ ] 下载并集成 44 个外部模板到渲染管线
- [ ] Skill 版本与 Hermes Agent 集成（`SKILL.md` 格式）
- [ ] Surface 层接入 render_page（`--surface` 参数生效）

### SaaS 版本
- [ ] Vercel 部署后 bug 修复并上线
- [ ] `saas/nextjs/lib/css-builder.ts` 补充 44 套设计系统至 54 套
- [ ] 落地页 `personal-ip-site/index.html` 与 SaaS 集成或合并

### 产品层
- [ ] 用户上传简历 → AI 提取 7 模块（当前手动填表）
- [ ] 部署后监控 / 错误追踪

---

## 七模块框架（内部内容架构）

1. **Soul** — 价值观/使命/热情/信念
2. **Framework** — 方法论/决策逻辑/学习方式/工作流
3. **Skills** — 硬技能/软技能/行业经验
4. **Work** — 代表作/内容/知识体系/证书
5. **Timeline** — 经历/成长曲线/未来方向
6. **Resources** — 人脉/信息工具/影响力
7. **Form** — 外在呈现/品牌关键词/他人评价/氛围

---

## Git Commits

| Commit | 内容 |
|--------|------|
| `95b0d8f` | Initial monorepo: skill/ + saas/ tracks |
| `5ed8d6e` | Add: example HTMLs, Hermes 7-module data, SPEC.md |
| `ac5f23d` | feat(saas): Add Next.js frontend with TypeScript ports |
| `21a991d` | Update: SPEC.md full status + README.md |
| `25669ad` | feat: add DESIGN.md generator with awesome-design-md format migration |
| `90ea6e0` | feat: MiniMax LLM integration + reasoning trace filter |
| `HEAD` | refactor: add Surface/Template abstraction layer + 44 MIT templates |

**未提交文件**：
- `skill/claude-design-encapsulation.html`
- `skill/claude-design-encapsulation.md`
- `skill/style_packages/SKILL.md`
