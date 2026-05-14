# Personal IP Site Generator — Product Spec

## 产品概述

**一句话**：上传简历/文档 → AI 提取7个模块 → 选择设计系统 → 生成专属个人网站 HTML。

**两条路径**：
- `skill/` — Hermes Skill 安装版（本地运行，CLI 交互）
- `saas/` — Vercel 部署版（Web UI，API 调用）

---

## 已完成 ✅

### 代码库（Monorepo）
- `skill/` — 完整的 Python 生成引擎（24KB css_builder + renderer + 54 design systems registry）
- `saas/` — FastAPI 后端 + 路由结构（routes.py 已写，API 实现 TODO）

### 示例站（已生成，均为 Hermes 本人内容）
| 文件 | 风格 | 大小 |
|------|------|------|
| `hermes_personal_site.html` | Personal Site · Claude 暖赭 | 30KB |
| `hermes_portfolio_linear.html` | Portfolio · Linear 深黑 | 23KB |
| `hermes_career_stripe.html` | Career Archive · Stripe 紫蓝 | 18KB |
| `shot_rich_claude.png` | Claude 暖赭截图 | — |
| `shot_rich_linear.png` | Linear 深黑截图 | — |
| `shot_rich_stripe.png` | Stripe 紫蓝截图 | — |

### 设计系统
- 54 个 design systems（从 popular-web-designs skill 提取）
- CSS variables + typography + spacing 完整
- 覆盖：Claude/Linear/Stripe/Framer/Notion/Vercel/Airbnb 等

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
- [ ] `SKILL.md` — Hermes skill 格式，触发词、步骤、示例
- [ ] `skill/data/hermes_7modules.json` — Hermes 完整7模块数据（用于示例）
- [ ] `skill/scripts/generate.py` — CLI 入口（已有 cli.py，需补充）
- [ ] 复制 example HTMLs 到 `skill/examples/`

### SaaS 版本
- [ ] `saas/public/examples/` — 三个示例 HTML 文件（未复制）
- [ ] `saas/public/screenshots/` — 三个截图（未复制）
- [ ] `saas/app/page.tsx` — Next.js 前端页面（空文件）
- [ ] `saas/app/api/extract/route.ts` — POST: 文档 → 7模块 JSON
- [ ] `saas/app/api/generate/route.ts` — POST: 7模块 + design_system → HTML
- [ ] `saas/app/api/designs/route.ts` — GET: 54 design systems 列表
- [ ] `saas/lib/css-builder.ts` — CSS 生成逻辑（TypeScript 移植）
- [ ] `saas/lib/renderer.ts` — HTML 生成逻辑（TypeScript 移植）
- [ ] `saas/lib/design-systems.ts` — 54 design systems 数据（TypeScript）
- [ ] `saas/lib/llm.ts` — OpenAI API 调用封装
- [ ] `saas/package.json` — Next.js 14 + TypeScript + openai
- [ ] `saas/vercel.json` — 部署配置
- [ ] `saas/.env.example` — OPENAI_API_KEY=sk-...

### Vercel 部署
- [ ] Vercel 项目创建 + 环境变量配置
- [ ] 域名绑定（可选）

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Skill 生成引擎 | Python 3.10+ |
| SaaS 后端 | FastAPI (Python) |
| SaaS 前端 | Next.js 14 (TypeScript) |
| LLM 调用 | OpenAI API (用户自备 key) |
| 部署 | Vercel |
| 设计系统 | 54 popular design systems (CSS custom properties) |

---

## 产品路线图

1. **Phase 0（当前）**：Monorepo 建好，代码推送 GitHub
2. **Phase 1**：Skill 版本完成（SKILL.md + 7模块数据 + example 文件）
3. **Phase 2**：SaaS 前端完成（Next.js UI + 三个示例预览）
4. **Phase 3**：Vercel 部署（后端 API + 前端）
5. **Phase 4**：用户流程测试 + 迭代

---

## 触发词

**Skill 版本**：
- "生成个人网站" / "帮我做个个人网站" / "personal ip site"
- "帮我写个落地页" / "生成我的网站"

**SaaS 版本**：
- 访问 ip-website-generator.vercel.app