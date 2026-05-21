# Personal IP Site Generator

把一个人的经历、洞见、专业能力，炼成有灵魂的个人网站。

> **GitHub:** `github.com/lj22503/ip-website-generator`
> **源码目录:** `/home/aiecho/ip-website-generator`
> **workspace 副本:** `workspace/projects/diaolong-products/ip-website-generator`（packages 三件套，Vercel 部署物，不得作为开发基准）

---

## 产品定位

**做什么：** 一个人把他的叙事材料（经历、价值观、方法论、作品）提交上来，生成一个属于他自己的个人网站 HTML。

**使用场景：**

| 场景 | Surface | 模板风格 |
|------|---------|---------|
| 思想领袖 / 内容创作者 | `story` | 个人叙事站 |
| 设计师 / 开发者作品展示 | `portfolio` | 作品集 |
| 求职者数字简历 | `resume` | 数字简历 |
| 产品 / 工具推广 | `landing` | 产品落地页 |

**设计系统：** 54 套真实设计系统（Linear、Notion、Vercel、Stripe、Airbnb……），换皮肤不换内容。

---

## 工作流程

```
用户材料（简历/访谈/文档）
    ↓ LLM 提取字段
内容 JSON（统一格式）
    ↓ 根据 Surface 选择模板
数据适配层（adapter）
    ↓ 转换为模板专属 schema
Jinja2 渲染
    ↓
HTML 页面（可下载）
```

**内容输入模块（7个）：**

| 模块 | 说明 |
|------|------|
| `hero_story` | 一句话 headline + 副标题 |
| `story` | 三段式叙事：做过什么 / 遭遇过什么 / 学到什么 |
| `skills` | 技能分类（categories[].items[]） |
| `projects` | 项目作品（title/year/background/outcome/tags） |
| `experience` | 职业经历（可选） |
| `about` | 关于我 / 头像 / 简介 |
| `contact` | 联系方式 |

---

## 两条生成路径

### 路径 A — CSS 换肤（推荐，用于 story/portfolio/resume surface）

```
content JSON → render_page() → 11个模块渲染函数 + css_builder(54套CSS)
```

```bash
python skill/core.py --design claude --product personal_site --demo --output /tmp/site.html
```

### 路径 B — 外部完整模板（--template 参数）

```
content JSON → data_adapter.adapt() → Jinja2 渲染 → 完整HTML页面
```

```bash
python skill/core.py --template developerfolio --content /tmp/content.json --output /tmp/out.html
```

三套模板：`developerfolio`（深色科技）· `alfolio`（学术侧栏）· `rahulbeniwal`（大字体作品集）

---

## 快速开始

```bash
cd /home/aiecho/ip-website-generator/skill

# 列出54套设计系统
python core.py --list-designs

# 路径A：CSS换肤（内容模块渲染，可用）
python core.py --design claude --product personal_site --demo --output /tmp/demo.html

# 路径B：三套完整模板（Jinja2渲染，适配层已接入）
python core.py --template developerfolio --content /tmp/lijing_content.json --output /tmp/out.html

# 交互式 CLI
python cli.py
```

---

## 项目结构

```
ip-website-generator/
├── skill/                              # Skill 版本（主开发目录）
│   ├── core.py                         # 主入口
│   ├── cli.py                          # 交互 CLI
│   ├── surfaces.py                     # Surface 抽象层（4种用途）
│   ├── template_registry.py            # 44个MIT模板资产注册表
│   ├── rendering/
│   │   ├── renderer.py                 # render_page() + render_html_template()
│   │   └── css_builder.py              # 54套设计系统 CSS 变量（920行）
│   ├── modules/
│   │   └── data_adapter.py             # 数据适配层（450行，已接入）
│   ├── html_templates/                 # 三套 Jinja2 完整模板
│   │   ├── developerfolio/template.html
│   │   ├── alfolio/template.html
│   │   └── rahulbeniwal/template.html
│   ├── narrative/
│   │   ├── generator.py               # 叙事生成器（LLM驱动）
│   │   └── mbti_styles.py            # MBTI → 叙事风格映射
│   ├── design_systems/
│   │   ├── registry.py                # 54套元数据 + MBTI推荐
│   │   └── loader.py
│   └── examples/                       # 示例 HTML
│
└── saas/                              # SaaS 版本（Next.js + FastAPI）
    ├── main.py
    ├── api/routes.py
    └── nextjs/                        # Next.js App Router 前端
```

---

## 设计系统

`skill/rendering/css_builder.py` 有 **54 套**完整 CSS 变量，对应 popular-web-designs skill 中的真实设计系统。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Skill 生成引擎 | Python 3.10+ |
| LLM | MiniMax（`OPENAI_API_KEY` 环境变量传 MiniMax key） |
| SaaS 前端 | Next.js 14 + TypeScript |
| SaaS 后端 | FastAPI + Vercel Python Runtime |
| 模板引擎 | Jinja2 |
| 设计系统 | 54 popular design systems（完整 CSS 变量） |

---

## 环境变量

```bash
# MiniMax API Key（Skill 和 SaaS 共用）
OPENAI_API_KEY=your_minimax_key_here
```

---

## 历史问题修复记录

| 日期 | 问题 | 状态 |
|------|------|------|
| 2026-05 | `cat.items` Jinja2 dict.items() 冲突 | ✅ 已修复 → `skill_list` |
| 2026-05 | alfolio/rahulbeniwal 无 story 渲染区块 | ✅ 已修复 → 独立 story section |
| 2026-05 | adapter 中 `about` 存在时 story 被吞掉 | ✅ 已修复 → `elif` → `if` |
| 2026-05 | README 声称「10套设计系统」 | ✅ 已修正 → 54套 |
| 2026-05 | README 声称「OpenAI」 | ✅ 已修正 → MiniMax |
| 2026-05 | cli.py import 路径错误 | ✅ 已修复 |
"| 2026-05 | developerfolio 导航栏缺少 story 链接 | ✅ 已修复 → 加条件链接 |\n| 2026-05 | GitHub Pages 未启用 | ✅ 已修复 → GitHub Actions workflow 自动部署 demo |\n| 2026-05 | data_adapter 是死代码 | ❌ 误解：adapter 已接入 renderer |"
