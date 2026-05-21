# Personal IP Site Generator — 产品规格书

## 产品概述

**一句话**：上传简历/文档 → AI 提取7个模块 → 选择设计系统 → 生成专属个人网站 HTML。

**产品形态**：两条并行路径
- `skill/` — Hermes Skill 安装版（本地运行，CLI 交互）
- `saas/` — Vercel 部署版（Web UI，浏览器直接使用）

**Vercel 部署地址**：`https://ip-website-generator-saas.vercel.app`

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
│   ├── core.py                      # 主入口（ argparse CLI，含 demo 数据）
│   ├── cli.py                      # 交互式 CLI（import 路径需修复）
│   ├── __init__.py
│   │
│   ├── rendering/
│   │   ├── __init__.py
│   │   ├── renderer.py             # HTML 渲染器（render_page 函数）
│   │   └── css_builder.py         # CSS 构建器（54 design systems，920行）
│   │
│   ├── narrative/
│   │   ├── __init__.py
│   │   ├── generator.py            # 叙事生成器（4层素材→故事）
│   │   └── mbti_styles.py         # MBTI 16型 → 叙事风格映射
│   │
│   ├── design_systems/
│   │   ├── __init__.py
│   │   ├── registry.py            # 设计系统注册表
│   │   └── loader.py
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   └── registry.py            # 内容模块注册表
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
    ├── main.py                    # FastAPI 入口
    ├── api/routes.py              # FastAPI 路由
    ├── css_builder.py            # Python CSS builder（复用 skill 版）
    ├── html_renderer.py
    ├── renderer.py
    ├── cli.py
    │
    ├── nextjs/                   # Next.js 14 前端（部署到 Vercel）
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx           # 主页面（3步向导：选设计→填内容→预览下载）
    │   │   ├── page.module.css
    │   │   ├── globals.css
    │   │   └── api/
    │   │       ├── designs/route.ts   # GET: 设计系统列表
    │   │       └── generate/route.ts   # POST: 生成 HTML
    │   │
    │   ├── lib/
    │   │   ├── css-builder.ts     # TypeScript CSS builder（10套系统，642行）
    │   │   ├── mbti-styles.ts     # MBTI 叙事风格
    │   │   └── renderer.ts        # TypeScript HTML 渲染器
    │   │
    │   └── types/index.ts
    │
    ├── public/
    │   ├── examples/             # 示例 HTML（与 skill/examples 同步）
    │   │   ├── hermes_personal_site.html
    │   │   ├── hermes_portfolio_linear.html
    │   │   └── hermes_career_stripe.html
    │   └── screenshots/          # 示例截图
    │       ├── shot_hermes_personal.png
    │       ├── shot_hermes_portfolio.png
    │       └── shot_hermes_career.png
    │
    └── rendering_modules/
        ├── hero_soul.py
        └── soul_module.py
```

---

## 已完成 ✅

### Skill 版本
- `core.py` 完整 CLI（`--list-designs` / `--demo` / `--preview` / `--design` / `--product`）
- `rendering/renderer.py` — `render_page()` 函数，支持 6 个模块渲染
- `rendering/css_builder.py` — 54 套设计系统完整 CSS 变量
- `narrative/generator.py` — 叙事生成（4层素材输入）
- `narrative/mbti_styles.py` — 16型 MBTI → 叙事风格映射
- Demo 模式可正常运行，输出 954 行结构完整的 HTML

### SaaS 版本
- `nextjs/app/page.tsx` — 3步向导 UI（Step1 选设计 / Step2 填内容 / Step3 预览下载）
- `nextjs/app/api/generate/route.ts` — POST `/api/generate` 生成 HTML
- `nextjs/app/api/designs/route.ts` — GET `/api/designs` 返回设计系统列表
- `nextjs/lib/renderer.ts` — TypeScript 渲染器（端口自 Python 版）
- `nextjs/lib/css-builder.ts` — 10 套设计系统 TypeScript 版本

### 示例
- `hermes_personal_site.html` — Personal Site · Claude 暖赭风格（Hermes 本人内容）
- `hermes_portfolio_linear.html` — Portfolio · Linear 深黑风格
- `hermes_career_stripe.html` — Career Archive · Stripe 紫蓝风格

---

## 待修复 🔴（阻塞 Bug）

### Skill 版本
- [ ] `skill/cli.py` — import 路径全部写错
  - `from mbti_styles` → `from narrative.mbti_styles`
  - `from narrative_generator` → `from narrative.generator`
  - `from html_renderer` → `from rendering.renderer`
  - 注：`core.py` 绕过了这些问题，所以能正常运行，但 `cli.py` 独立使用时崩溃

### SaaS 版本
- [ ] `/api/generate` 响应字段名不一致
  - 后端返回 `html_base64`，前端 `page.tsx` 读取 `html_base64`（匹配）
  - 但 `/api/designs` 中 `DESIGN_SPECS` 只有 10 套系统，文档声称 54 套，需对齐
- [ ] `saas/nextjs/lib/css-builder.ts` — 仅 10 套设计系统，缺少 44 套

---

## 未完成 🔨

### Skill 版本
- [ ] `cli.py` 修复 import 路径后完成交互式 CLI
- [ ] Skill 版本与 Hermes Agent 集成（`SKILL.md` 格式）

### SaaS 版本
- [ ] Vercel 部署后 bug 修复并上线
- [ ] `saas/nextjs/lib/css-builder.ts` 补充 44 套设计系统至 54 套
- [ ] `saas/.env.example` — `OPENAI_API_KEY=`（目前生成不依赖 LLM，纯本地渲染）
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

**未提交文件**：
- `skill/claude-design-encapsulation.html`
- `skill/claude-design-encapsulation.md`
- `skill/style_packages/SKILL.md`
