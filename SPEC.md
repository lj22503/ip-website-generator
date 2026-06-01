# Personal IP Site Generator — 产品规格书

## 产品概述

**一句话**：上传简历/文档 → AI 提取7个模块 → 选择设计系统 → 生成专属个人网站 HTML。

**产品形态**：两条并行路径
- `skill/` — Hermes Skill 安装版（本地运行，CLI 交互）
- `saas/` — Vercel 部署版（Web UI，浏览器直接使用）

**最新修复**：
- `skill/core.py` 所有 `open(args.content)` 添加 `encoding="utf-8"`，解决 Windows GBK 环境下读取 UTF-8 中文 JSON 失败问题。
- 三套 Jinja2 模板（developerfolio / alfolio / rahulbeniwal）全部可基于 `test_data_all_fields.json` 生成苏轼完整样例。
- `adapter_output.json` 加入 `.gitignore`。
- **SaaS 新增模板模式**：`/api/generate` 支持 `template` 参数（developerfolio / alfolio / rahulbeniwal），使用纯 TypeScript 字符串模板引擎渲染完整 HTML，与 Skill 逻辑一致。Step3 UI 新增模板选择 Tab。
- `saas/nextjs/next.config.js` 配置 webpack 支持 `.html` 文件作为 `asset/source` 模块直接导入。
- **SaaS 修复 template-renderer.ts 嵌套 for 循环 bug**：原 `processFor` 用非贪婪正则 `([\s\S]*?)` 捕获 body，嵌套场景下会错误地在内层 `{% endfor %}` 就停止；改用 `findMatchingEndfor` 找匹配 endfor 实现嵌套正确性。同时修复字符串元素早期返回 bug（`if (!isObj(item)) return toStr(item)` 导致内层循环 `<span class="skill-tag">{{ item }}</span>` 整体被跳过），改为 `itemMap = isObj(item) ? item : {}` 确保 primitive 类型也走完整渲染流程。

**Vercel 部署地址**：`https://ip-website-generator-saas.vercel.app`

---

## 核心架构：双轨并行

```
skill/                          saas/
  ↓ Python CLI                   ↓ Next.js + TypeScript
  本地运行                       Vercel 部署
  rendering/ 渲染引擎             nextjs/lib/ 渲染器（TS 端口）
```

**独立维护，不互通**：
- `skill/rendering/` — Python 原版（本地 CLI）
- `saas/nextjs/lib/` — TypeScript 端口版（Vercel Serverless）
- 两套代码独立演进，不要混用，不要让 saas 调用 skill 的 Python

## Surface × Design System × Component × Template

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
│   │   └── css_builder.py         # CSS 构建器（29 design systems，~1400行）
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
└── saas/                          # SaaS 版本（Next.js 全栈，2026-05-22 重构）
    ├── vercel.json                # Vercel 构建配置（根目录部署）
    ├── main.py                    # FastAPI 入口（已废弃，保留参考）
    ├── api/routes.py              # FastAPI 路由（已废弃）
    ├── css_builder.py             # Python CSS 构建器（已端口，保留参考）
    ├── html_renderer.py           # Python HTML 渲染器（已端口，保留参考）
    ├── renderer.py                # Python 渲染引擎（已端口，保留参考）
    │
    ├── nextjs/                    # Next.js 14 前端（纯 TypeScript，无 Python 依赖）
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── app/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx           # 3步向导 UI
    │   │   ├── page.module.css
    │   │   ├── globals.css
    │   │   └── api/
    │   │       ├── designs/route.ts  # GET /api/designs
    │   │       └── generate/route.ts # POST /api/generate → renderPage()
    │   └── lib/
    │       ├── css-builder.ts     # 10 套设计系统 CSS（从 css_builder.py 端口）
    │       └── html-renderer.ts   # 11 个模块渲染器（从 html_renderer.py 端口）
    │
    ├── public/
    │   ├── examples/
    │   └── screenshots/
    │
    └── rendering_modules/
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
- [x] `nextjs/app/page.tsx` — 3步向导 UI
- [x] `nextjs/app/api/generate/route.ts` — POST `/api/generate` 生成 HTML
- [x] `nextjs/app/api/designs/route.ts` — GET `/api/designs` 返回设计系统列表
- [x] `nextjs/lib/html-renderer.ts` — 11 个模块渲染器（TypeScript 端口完成）
- [x] `nextjs/lib/css-builder.ts` — 10 套设计系统 CSS（TypeScript 端口完成）
- [x] `nextjs/` — 纯 TypeScript，移除 Python 依赖，Vercel Serverless 兼容
- [x] `vercel.json` — 根目录部署配置，指向 `saas/nextjs/`
- [x] GitHub → Vercel 自动部署链路（push master 触发）
- [ ] Vercel 项目绑定 GitHub 分支（需 Vercel Dashboard 操作）

---

## 待修复 🔴

### Skill 版本
- [x] `skill/html_templates/developerfolio/template.html` — story 区块 body 已有，导航栏缺少链接 | ✅ 已修复 → 加条件链接 |
- [x] `skill/cli.py` — import 路径 | ✅ 已确认正确（narrative.mbti_styles / narrative.generator / rendering.renderer）|
| 2026-05 | registry 声称54套，实际只有10套CSS | ✅ 已修复 → 29套CSS注入 + README同步 |

### SaaS 版本
- [x] `/api/generate` 响应字段名一致 ✅ 2026-05-22 → `renderPage()` 返回 `html_base64`
- [x] `saas/nextjs/lib/css-builder.ts` 10 套设计系统 ✅ 2026-05-22 端口完成（10套，完整实现）
- [x] SaaS `/api/generate` 支持 template 参数 + Step3 UI 模板选择器 ✅ 2026-05-26

---

## 未完成 🔨

### Skill 版本
- [ ] 下载并集成 44 个外部模板到渲染管线
- [ ] Skill 版本与 Hermes Agent 集成（`SKILL.md` 格式）
- [ ] Surface 层接入 render_page（`--surface` 参数生效）

### SaaS 版本
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

## 叙事结构重构（2026-05-25）

### 问题诊断
- **About + Story 重复** — About 应从 Story 提取精华，非独立全文
- **Framework 单独成区块** — 方法论应融入 Skills 内作为子项
- **Timeline + Experience 重复** — 两者都是经历，合并为一个
- **Soul/Identity/Challenge 引述碎片化** — 合并精简

### 解决方案
| 问题 | 解决方案 |
|------|---------|
| About + Story 重复 | 合并为「我是谁」：bio 做简介 + story 三段（经历/挑战/洞见）做细节 |
| 独立 SOUL 大声明区块 | 移除，soul_statement 在 Identity Stats Grid 左上角展示一行 |
| 独立 FRAMEWORK 大区块 | 方法论卡片下沉到 SKILLS 模块底部 |
| 独立 TIMELINE 区块 | 移除，experience 模块本身就是时间线 |
| 重复的 CHALLENGE QUOTE | 保留为轻量横条，引述核心挑战 |

### 各模板最终区块顺序

**developerfolio**（深色科技风）：
`HERO → Identity Stats → 我是谁 → 技能(含方法论) → 职业经历 → 教育 → 项目 → 成就 → 文章 → 评价 → 联系 → FOOTER`

**alfolio**（学术风）：
`侧栏(含头像/MBTI/关键词) → 我是谁 → 技能(含方法论) → 职业经历 → 联系方式 → 评价`

**rahulbeniwal**（极简项目风）：
`HERO → Identity Stats → 我是谁 → 挑战引述 → 项目 → 技能(含方法论) → 职业经历 → 联系 → 评价 → FOOTER`

### Adapter 字段传递（三个适配器同步）
- `mbti` — 从 `story.mbti` 提取
- `soul_statement` — 从 `story.insights` 提取
- `challenge_quote` — 从 `story.challenges` 提取
- `framework_items` — 优先独立字段，回退从 `about.bio` 拆分段落
- `stats` — `{mbti, skills, years, availability}` (to_alfolio/to_rahulbeniwal 新增)
- `testimonials` / `resources` — 直通传递

### 数据缺失自动隐藏
所有新增区块均为 `{% if data.xxx %}` 条件渲染，数据缺失时区块自动隐藏不报错。

---

## 叙事结构重构 v2（2026-05-25 下午）

### 核心理念
以 Hermes 三个示例（`hermes_personal_site.html` 等）为基准，重构模板结构：
- SOUL（内核）：价值观/原则卡片/最深挑战
- FRAMEWORK（方法论）：方法论卡片网格
- FORM（风格）：相处方式/MBTI
- STORY（故事）：成长轨迹时间线
- SKILLS（技能）：技能分类
- WORKS（作品）：项目卡片

### developerfolio 区块结构（参考 Hermes 示例）
```
HERO → SOUL（原则+最深挑战）→ FRAMEWORK（方法论网格）→ FORM（MBTI）→ STORY（成长轨迹）→ SKILLS（技能图谱）→ WORKS（项目作品）→ CONTACT → FOOTER
```

### 关键字段映射
| Hermes 数据字段 | developerfolio 模板变量 |
|---------------|----------------------|
| `story.insights` | `data.story.insights` → Soul 大声明 |
| `form.keywords[]` | `data.form.keywords` → 原则卡片 |
| `story.deepest_challenge` | `data.story.deepest_challenge` → 深挑战引述 |
| `framework_items[]` | `data.framework_items` → 方法论卡片 |
| `mbti` / `mbti_description` | `data.mbti` / `data.mbti_description` → MBTI 卡片 |
| `form.interaction_styles[]` | `data.form.interaction_styles` → 相处方式列表 |
| `story.timeline[]` | `data.story.timeline` → 故事时间线 |
| `skills.categories[]` | `data.skills.categories` → 技能标签 |
| `projects[]` | `data.projects` → 项目卡片 |

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
| `23d549a` | fix: add CSS specs for 19 missing design systems, update count 10→29 |
| `308e7dc` | feat: add GitHub Pages deploy workflow |
| `7cef693` | feat(saas): port Python renderer to TypeScript, full Vercel deployment |

**未提交文件**：
- `skill/claude-design-encapsulation.html`
- `skill/claude-design-encapsulation.md`
- `skill/style_packages/SKILL.md`
