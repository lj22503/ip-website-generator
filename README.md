# Personal IP Site Generator

把一个人的经历、洞见、专业能力，炼成有灵魂的个人网站。

## 两条路径

### Skill 版本（本地运行）
```bash
cd skill

# 列出可用设计系统
python core.py --list-designs

# Demo 模式生成示例网站
python core.py --design claude --product personal_site --demo --output /tmp/demo.html

# 指定设计系统生成
python core.py --design linear.app --product portfolio --demo --output /tmp/site.html

# 生成后浏览器预览
python core.py --design notion --demo --preview
```

### SaaS 版本（Vercel 部署）
```
https://ip-website-generator-saas.vercel.app
```
访问即用，无需安装。

---

## 产品流程

1. **上传**：粘贴简历/文档，或上传 PDF
2. **AI 提取**：从内容中提取 7 个模块（Soul/Framework/Skills/Work/Timeline/Resources/Form）
3. **选择设计系统**：从 54 套流行设计系统（Claude/Linear/Stripe/Notion...）中选一个
4. **生成**：输出完整的单页 HTML，可以直接下载

---

## 设计系统

当前支持 **10 套**（skill + SaaS 通用）：

| 名称 | 分类 | 描述 |
|------|------|------|
| `notion` | Design & Productivity | 温暖纸质感，留白呼吸 |
| `linear.app` | Developer Tools | 冷静克制，结构极强 |
| `stripe` | Fintech | 金融精致，高端克制 |
| `figma` | Design & Productivity | 活力多彩，专业有趣 |
| `apple` | Enterprise & Consumer | 极致高端，纯净大气 |
| `framer` | Design & Productivity | 大胆冲击力，设计感强 |
| `airbnb` | Enterprise & Consumer | 温暖亲切，摄影主导 |
| `spotify` | Enterprise & Consumer | 音乐感强，视觉大胆 |
| `vercel` | Developer Tools | 极简技术感，高精度 |
| `claude` | AI & ML | 温暖克制，有深度 |

Skill 版本 Python 代码含完整 54 套设计系统 CSS 变量。

---

## 示例（Hermes 本人内容）

在 `skill/examples/` 和 `saas/public/examples/` 目录下有三个示例网站：

- `hermes_personal_site.html` — Claude 暖赭风格
- `hermes_portfolio_linear.html` — Linear 深黑风格
- `hermes_career_stripe.html` — Stripe 紫蓝风格

---

## 技术栈

| 组件 | 技术 |
|------|------|
| Skill 生成引擎 | Python 3.10+ |
| SaaS 前端 | Next.js 14, TypeScript |
| SaaS 后端 | FastAPI (Python) + Next.js API Routes |
| LLM | OpenAI API（用户自备 key） |
| 部署 | Vercel |
| 设计系统 | 54 popular design systems（完整 CSS 变量） |

---

## 环境变量

```bash
# SaaS 版本（Vercel 环境变量）
OPENAI_API_KEY=***

# Skill 版本无需环境变量（纯本地运行）
```
