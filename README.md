# Personal IP Site Generator

把一个人的经历、洞见、专业能力，炼成有灵魂的个人网站。

## 源码仓库

**`/home/aiecho/ip-website-generator`**（GitHub: `lj22503/ip-website-generator`）

> 注意：workspace 下有一份副本（`.../diaolong-products/ip-website-generator`），为输出物，非源码，不得作为开发基准。

---

## 两条生成路径

### 路径A — CSS 换肤（默认）

```
content JSON → render_page() → 11个模块渲染函数 + css_builder(54套CSS)
```

```bash
python skill/core.py --design notion --demo --output /tmp/site.html
```

### 路径B — 外部完整模板（--template 参数）

```
content JSON → data_adapter.adapt() → jinja2 渲染 → 完整HTML页面
```

```bash
python skill/core.py --template developerfolio --content /tmp/lijing_content.json --output /tmp/out.html
```

三套模板：`developerfolio`（深色科技）· `alfolio`（学术侧栏）· `rahulbeniwal`（大字体作品集）

---

## 当前已知问题（必读）

### 🔴 致命 — data_adapter 写了但从未被调用

`s SKILL.md` 文件中记录的 adapter（`skill/modules/data_adapter.py`，450行，三套模板适配函数）是**死代码**。`render_html_template()` 在 `--template` 模式下直接把 raw JSON 扔给 Jinja2，adapter 从未被调用。

**后果：**
- `name` / `role` 在 JSON 根节点，模板拿到的是 `content` dict，`data.name` 永远为空
- `projects: {projects: [...]}` 嵌套结构，模板期望 flat 数组，项目卡片消失
- `story.experiences` 是 `\n\n` 分段的 plain string，模板期望 `experiences_paragraphs[]` 数组，段落全挤在一起

**修复方案：** 在 `rendering/renderer.py` 的 `render_html_template()` 里调用 `adapt(content, tpl_name)`。

### 🔴 致命 — 两套代码完全重复，各走各的

本仓库（skill/ + saas/ 双轨）与 `workspace/projects/diaolong-products/ip-website-generator`（packages/ + frontend/ 三件套）是同一个产品的两个不同演化分支，代码无法合并，必须二选一保留。

**推荐保留本仓库**（skill/ 方向更新）。

### 🟡 重大 — alfolio / rahulbeniwal 的 story 内容完全丢失

三套模板中只有 `developerfolio` 正确渲染了 `story.experiences_paragraphs` 等字段。`alfolio` 和 `rahulbeniwal` 的模板 body 没有渲染 story 三段（经历/挑战/洞察），内容被丢弃。

### 🟡 重大 — README 声称「10套设计系统」，实际有54套

文档严重落后于代码。`rendering/css_builder.py` 实际有 54 套完整 CSS 变量，README 只列了10套。

### 🟡 重大 — README 声称「OpenAI API」，实际用的是 MiniMax

LLM 接入的是 MiniMax（非 OpenAI），README 未更新。

### 🟡 重大 — skill/cli.py import 路径全部写错

```python
# 当前（错）
from narrative_generator import ...
from mbti_styles import ...
from html_renderer import ...

# 应该
from narrative.generator import ...
from narrative.mbti_styles import ...
from rendering.renderer import ...
```

### 🟢 中等 — GitHub Pages 未启用

仓库无 GitHub Pages 在线预览，每次需要本地打开 HTML 文件。

### 🟢 中等 — SPEC.md 与代码实际不符

SPEC.md 列的「已完成」状态存在 bug（如 adapter 相关），某些「待修复」实际上已部分修复。

---

## 项目结构

```
ip-website-generator/
├── skill/                              # Skill 版本（本地 Python CLI）
│   ├── core.py                         # 主入口
│   ├── cli.py                          # 交互 CLI（import路径有bug）
│   ├── surfaces.py                     # Surface 抽象层
│   ├── template_registry.py            # 44个MIT模板资产注册表
│   ├── rendering/
│   │   ├── renderer.py                 # render_page() + render_html_template()
│   │   └── css_builder.py              # 54套设计系统 CSS 变量（920行）
│   ├── modules/
│   │   └── data_adapter.py             # ⚠️ 写了但从未被调用
│   ├── html_templates/                 # 三套 Jinja2 完整模板
│   │   ├── developerfolio/template.html
│   │   ├── alfolio/template.html
│   │   └── rahulbeniwal/template.html
│   ├── narrative/
│   │   ├── generator.py               # 叙事生成器
│   │   └── mbti_styles.py             # MBTI → 叙事风格
│   ├── design_systems/
│   │   ├── registry.py                # 54套元数据
│   │   └── loader.py
│   └── examples/                       # 示例 HTML（Hermes 本人内容）
│
└── saas/                              # SaaS 版本（Next.js + FastAPI）
    ├── main.py
    ├── api/routes.py
    ├── nextjs/                        # Next.js App Router 前端
    │   ├── app/page.tsx
    │   └── app/api/generate/route.ts
    └── public/examples/
```

---

## 设计系统

`skill/rendering/css_builder.py` 实际有 **54 套**完整 CSS 变量。README 中的列表（10套）已过时。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Skill 生成引擎 | Python 3.10+ |
| LLM | MiniMax（`OPENAI_API_KEY` 环境变量实际传 MiniMax key） |
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

## 快速开始

```bash
cd /home/aiecho/ip-website-generator/skill

# 列出54套设计系统
python core.py --list-designs

# 路径A：CSS换肤（可用）
python core.py --design claude --product personal_site --demo --output /tmp/demo.html

# 路径B：三套完整模板（adapter未接入，有bug）
python core.py --template developerfolio --content /tmp/lijing_content.json --output /tmp/out.html
```
