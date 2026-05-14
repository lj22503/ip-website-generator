# Personal IP Site Generator

把一个人的经历、洞见、专业能力，炼成有灵魂的个人网站。

## 两条路径

### Skill 版本（本地运行）
```bash
cd skill
python cli.py
# 输入简历/文档 → AI 提取7模块 → 选择设计系统 → 生成HTML
```

### SaaS 版本（Vercel 部署）
```bash
cd saas/nextjs
npm install
npm run dev   # 本地开发

# 部署到 Vercel（连接 GitHub 即可）
```

## 产品流程

1. **上传**：粘贴简历/文档，或上传 PDF
2. **AI 提取**：从内容中提取 7 个模块（Soul/Framework/Skills/Work/Timeline/Resources/Form）
3. **选择设计系统**：从 54 个流行设计系统（Claude/Linear/Stripe/Notion...）中选一个
4. **生成**：输出完整的单页 HTML，可以直接下载

## 设计系统

当前支持 10 个（TypeScript / SaaS）：notion, linear.app, stripe, figma, apple, framer, airbnb, spotify, vercel, claude

Python skill 版本完整支持 54 个。

## 示例

在 `skill/examples/` 和 `saas/public/examples/` 目录下有三个 Hermes 本人的示例网站：

- `hermes_personal_site.html` — Claude 暖赭风格
- `hermes_portfolio_linear.html` — Linear 深黑风格
- `hermes_career_stripe.html` — Stripe 紫蓝风格

## 环境变量

```bash
# SaaS 版本
OPENAI_API_KEY=sk-...   # 需要 OpenAI API key 才能运行
```

## 技术栈

- Skill: Python 3.10+, 54 design systems
- SaaS 前端: Next.js 14, TypeScript
- SaaS 后端: FastAPI + Next.js API Routes
- LLM: OpenAI API
- 部署: Vercel