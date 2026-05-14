# Personal IP Site Generator — 产品规格书

## 产品概述

**一句话**：上传简历/文档 → AI 提取7个模块 → 选择设计系统 → 生成专属个人网站 HTML。

**两条路径**：
- `skill/` — Hermes Skill 安装版（本地运行，CLI 交互）
- `saas/` — Vercel 部署版（Web UI，API 调用）

---

## 已完成 ✅

### Monorepo 结构（github.com/lj22503/ip-website-generator）
```
ip-website-generator/
├── SPEC.md              # 本文件
├── README.md
├── pyproject.toml
├── skill/               # Skill 版本（Python CLI）
│   ├── SKILL.md         # [未完成 — 暂无]
│   ├── core.py
│   ├── cli.py
│   ├── data/hermes_7modules.json  # Hermes 完整7模块示例数据
│   ├── examples/        # 3个示例HTML（Claude/Linear/Stripe风格）
│   ├── design_systems/  # 54 design systems registry
│   ├── modules/         # 内容模块定义
│   ├── narrative/       # MBTI叙事生成
│   └── rendering/       # CSS builder + renderer（920行）
└── saas/                # SaaS 版本
    ├── nextjs/          # Next.js 14 前端
    │   ├── app/
    │   │   ├── page.tsx  # 主页面（3步向导）
    │   │   ├── layout.tsx
    │   │   └── api/
    │   │       ├── designs/route.ts   # GET: 54 design systems
    │   │       └── generate/route.ts   # POST: 生成HTML
    │   ├── lib/
    │   │   ├── css-builder.ts  # TypeScript CSS生成（642行，10个design systems）
    │   │   ├── mbti-styles.ts  # MBTI样式
    │   │   └── renderer.ts     # TypeScript HTML渲染
    │   ├── package.json
    │   └── tsconfig.json
    ├── public/           # 静态文件
    │   ├── examples/      # 3个示例HTML（Claude/Linear/Stripe风格）
    │   └── screenshots/   # 3个示例截图
    ├── main.py           # FastAPI入口
    ├── api/routes.py     # FastAPI路由
    ├── css_builder.py    # Python CSS builder（复用skill版）
    └── renderer.py       # Python renderer（复用skill版）
```

### 示例站（Hermes 本人内容）
| 文件 | 风格 | 大小 |
|------|------|------|
| `hermes_personal_site.html` | Personal Site · Claude 暖赭 | 30KB |
| `hermes_portfolio_linear.html` | Portfolio · Linear 深黑 | 23KB |
| `hermes_career_stripe.html` | Career Archive · Stripe 紫蓝 | 18KB |
| `shot_hermes_personal.png` | Claude 暖赭截图 | — |
| `shot_hermes_portfolio.png` | Linear 深黑截图 | — |
| `shot_hermes_career.png` | Stripe 紫蓝截图 | — |

### 设计系统
- Python: `skill/rendering/css_builder.py` — 920行，54个design systems完整CSS变量
- TypeScript: `saas/nextjs/lib/css-builder.ts` — 642行，10个design systems（notion, linear.app, stripe, figma, apple, framer, airbnb, spotify, vercel, claude）

### 七模块框架（内部内容架构）
1. **Soul** — 价值观/使命/热情/信念
2. **Framework** — 方法论/决策逻辑/学习方式/工作流
3. **Skills** — 硬技能/软技能/行业经验
4. **Work** — 代表作/内容/知识体系/证书
5. **Timeline** — 经历/成长曲线/未来方向
6. **Resources** — 人脉/信息工具/影响力
7. **Form** — 外在呈现/品牌关键词/他人评价/氛围

---

## 未完成 🔨

### Skill 版本
- [ ] `SKILL.md` — Hermes skill 格式（触发词、步骤、7模块说明、示例）
- [ ] `skill/cli.py` — 补充完整CLI交互（已有骨架）

### SaaS 版本
- [ ] `saas/nextjs/lib/css-builder.ts` — **仅10个design systems**，需补充至54个（可以从 Python css_builder.py 提取剩余44个）
- [ ] `saas/nextjs/lib/renderer.ts` — **基础版本**，需与 Python renderer.py 对齐
- [ ] `saas/nextjs/app/page.tsx` — 需要接入 example HTML 预览（tab切换设计系统）
- [ ] `saas/.env.example` — OPENAI_API_KEY=
- [ ] `saas/nextjs/.env.local` — 本地开发用

### Vercel 部署
- [ ] 创建 Vercel 项目（连接 GitHub repo）
- [ ] 配置环境变量（OPENAI_API_KEY）
- [ ] vercel.json 配置（Node 18，API route 支持）
- [ ] 域名绑定（可选）

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Skill 生成引擎 | Python 3.10+ |
| SaaS 后端 | FastAPI (Python) + Next.js API Routes |
| SaaS 前端 | Next.js 14 (TypeScript) |
| LLM 调用 | OpenAI API（用户自备 key） |
| 部署 | Vercel |
| 设计系统 | 54 popular design systems |

---

## 触发词

**Skill 版本**：
- "生成个人网站" / "帮我做个个人网站" / "personal ip site"
- "帮我写个落地页" / "生成我的网站"

**SaaS 版本**：
- 访问部署后的 Vercel 域名

---

## Git Commits

| Commit | 内容 |
|--------|------|
| `95b0d8f` | Initial monorepo: skill/ + saas/ tracks |
| `5ed8d6e` | Add: example HTMLs, Hermes 7-module data, SPEC.md |
| `ac5f23d` | feat(saas): Add Next.js frontend with TypeScript ports |