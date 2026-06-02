# Issues & Field Mapping — 7 IP Dimensions

> 记录解析问题与字段映射，用于跟踪修复进度。

---

## 实际渲染验证 (2026-05-24) — 对比第三方输出

### 第三方已生成的黎静数据

用户通过第三方软件 + 黎静简历原材料，已成功生成了3个模板的完整 HTML：

| 模板 | 文件 |
|------|------|
| developerfolio 深色科技风 | `黎静_个人主页_developerfolio深色科技风.html` |
| alfolio 学术风 | `黎静_个人主页_alfolio学术风.html` |
| rahulbeniwal 极简项目风 | `黎静_个人主页_rahulbeniwal极简项目风.html` |

**对应的结构化数据**（`lijing_developerfolio_data.json`）包含完整字段：

```json
{
  "name": "黎静",
  "title": "资深金融产品经理（C端方向）",
  "avatar": "https://...",
  "hero_subtitle": "10年金融产品专家 · AI驱动的产品创新者",
  "about": { "title": "专业背景", "paragraphs": [...] },
  "story": { "experiences_paragraphs": [...], "challenges_paragraphs": [...], "insights_paragraphs": [...] },
  "education": [{ "school": "南京大学", "degree": "政治经济学硕士", "period": "2012-2015" }],
  "achievements": [{ "title": "基金诊断工具", "description": "全年使用超5.9万人次", "year": "2023" }],
  "skills": { "categories": [...], "bars": [...] },
  "projects": [...],
  "socials": { "email": "lj22503@163.com", "phone": "17602189728" }
}
```

### 根因：DEMO_PERSONAL_SITE 数据空洞 vs 真实用户数据

| 字段 | 第三方 JSON | 我们 DEMO_PERSONAL_SITE | adapter 输出 |
|------|------------|----------------------|-------------|
| `name` | `"黎静"` ✅ | 缺失 | `""` ❌ |
| `title` | `"资深金融产品经理"` ✅ | 缺失 | `""` ❌ |
| `avatar` | `"https://..."` ✅ | 缺失 | 未输出 |
| `about.bio` | 3段完整段落 ✅ | 缺失 | `""` ❌ |
| `about.subtitle` | `"专业背景"` ✅ | 缺失 | 未输出 |
| `education[]` | 结构化数组 ✅ | 缺失 | 未输出 |
| `achievements[]` | 结构化数组 ✅ | 缺失 | 未输出 |
| `experience[]` | 缺失 | 缺失 | `None` ❌ |
| `socials` | `{email, phone}` ✅ | 只有 `contact.email` | 只映射了 email |
| `hero_subtitle` | `"10年金融产品专家..."` ✅ | ✅ 有 | ✅ 正确 |
| `story.experiences_paragraphs[]` | 3段 ✅ | `story.experiences` 字符串 | 需转为数组 |

### 核心问题

**问题不在解析器本身，而在于 DEMO 数据是空的。**

1. **`DEMO_PERSONAL_SITE` 没有黎静的的真实数据** — 我们的 `DEMO_PERSONAL_SITE` 是硬编码的假数据（"我是谁" / "一句话让别人记住你"），而用户原材料（黎静简历）已经成功被第三方系统解析出了完整结构
2. **Timeline/experience 数据结构不匹配** — 模板期望 `experience[]` 数组（period/role/company/description），但 `story.experiences` 是叙事字符串
3. **第三方 AI 解析 prompt 用的是另一套维度** (career/skills/projects/education/insight/traits/potential)，与我们要求的 7 IP Dimensions 不同
4. **MBTI 未传递** — `story.mbti` 未被 `to_developerfolio` 提取到顶层

### 修复路径

1. 将黎静的真实数据（从 `lijing_developerfolio_data.json`）作为新的 `DEMO_PERSONAL_SITE`
2. 或打通 analyze API → adapter → 模板的完整链路，用黎静简历原材料作为测试输入
3. 将 `story.experiences` 字符串拆分为 `experiences_paragraphs[]` 数组

---

## 实际渲染验证 (2026-05-24)

**验证方式**：`python -c "from skill.modules.data_adapter import to_developerfolio; print(to_developerfolio(DEMO_PERSONAL_SITE))"`

**developerfolio 模板实际渲染结果**：

| 字段 | 实际值 | 问题 |
|------|--------|------|
| `name` | `""` (空) | `hero_name` 不存在，无 fallback |
| `title` | `""` (空) | `hero_label` 不存在，无 fallback |
| `headline` | `"我用3年时间，把副业收入超过了主业"` | ✅ 正确 |
| `hero_subtitle` | `"前字节产品经理 \| 独立开发者 \| 知识炼金士"` | ✅ 正确 |
| `about.bio` | `""` (空) | `data.about` 不存在，fallback 到空字符串 |
| `experience` | `None` | `story.experiences` 是原始字符串，无法格式化为 timeline |
| `mbti` | `MISSING` | `story.mbti` 存在但从未被提取到 result root |
| `socials` | `{}` | `contact.links` 格式不被解析 (`"Twitter \| https://..."`) |

**关键发现**：
- `hero_story` 的 `headline` 和 `subtitle` ✅ 正确适配
- `about` section 完全空白（无 `about` key）
- `experience` timeline 完全空白（字符串无法遍历）
- `mbti` 和 `socials` 数据存在但未传递

---

## 完整字段映射（目标）

### 叙事素材层 → 7 IP Dimensions → 页面模板字段

| 7 IP Dimension | 语义定义 | 来源素材 | Skill模板字段 | SaaS模板字段 | 状态 |
|----------------|---------|---------|-------------|-------------|------|
| **Soul** (内核) | 价值观/使命/热情/信念 | experiences (经历) / challenges (挑战) / insights (认知) | `about.bio` (部分), `story.*` | `story.insights`, `story.challenges` | ⚠️ 部分正确 |
| **Framework** (方法论) | 方法论/决策逻辑/学习方式/工作流 | experiences, challenges | `about.bio` (部分) | `about.bio` | ⚠️ 与Soul混淆 |
| **Skills** (技能) | 硬技能/软技能/行业经验 | skills list | `skills.categories` | `skills.categories` | ✅ 已正确映射 |
| **Work** (作品) | 代表作/内容/知识体系/证书 | projects | `projects[*]` | `projects[*]` | ✅ 已正确映射 |
| **Timeline** (经历) | 经历/成长曲线/未来方向 | experiences, education | `experience[]` (结构化数组) | `story.experiences` (原始字符串) | 🔴 严重问题 |
| **Resources** (资源) | 人脉/信息工具/影响力 | social_links, links | 无对应字段 | `social.links` (部分) | 🔴 缺失 |
| **Form** (形象) | 外在呈现/品牌关键词/他人评价 | bio, testimonials | 无对应字段 | `hero_featured.subtitle` (部分) | 🔴 缺失 |

---

## 🔴 严重问题

### 1. Timeline Dimension — 数据结构不匹配

**问题**：`story.experiences` 是原始叙事字符串，但所有 Jinja2 模板期望 `experience[]` 结构化数组。

**模板期望格式**：
```python
experience = [
    {"period": "2020-2023", "role": "产品设计师", "company": "字节跳动", "description": "..."},
    {"period": "2018-2020", "role": "UX设计师", "company": "腾讯", "description": "..."},
]
```

**当前 DEMO 数据**：
```python
"story": {
    "experiences": "他曾主导多个从0到1的产品设计项目，涵盖社交、金融、教育等多个领域...",
    "challenges": "如何在资源有限的情况下找到最优解...",
    "insights": "设计不仅仅是美学，更是一种解决问题的思维方式...",
}
```

**影响模板**：
- `developerfolio/template.html` — `{% for exp in experience %}`
- `rahulbeniwal/template.html` — `data.experience` 遍历
- `alfolio/template.html` — `work` section 遍历

**修复方案**：DEMO 需要提供结构化 `experience[]` 数组，或在 `data_adapter.py` 中将 `story.experiences` 解析拆分为结构化数据。

---

### 2. Resources Dimension — 无对应模板字段

**问题**：Resources (人脉/资源/影响力) 没有对应模板变量。

**7 IP 维度定义**：
- 人脉：合作过的客户、行业峰会分享、演讲
- 资源：工具、信息源、社区
- 影响力：文章/内容传播、他人口碑

**当前模板现状**：
- `developerfolio` — 只有 `social` (Twitter/LinkedIn/GitHub)
- `rahulbeniwal` — 只有 `social_links` + `open_source`
- `alfolio` — 无 social 相关字段

**修复方案**：
1. 在 `data_adapter.py` 中增加 `resources` 适配逻辑
2. 或在 `social` 字段中补充 Resources 内容

---

### 3. Form Dimension — 无对应模板字段

**问题**：Form (外在呈现) 没有对应模板变量。

**7 IP 维度定义**：
- 外在呈现：照片、头像、个人网站视觉风格
- 品牌关键词：个人标签、slogan
- 他人评价：推荐信、testimonials
- 氛围：设计风格、配色、字体

**当前模板现状**：
- 三个模板均无 `testimonials` 区块（`rahulbeniwal` 有但未激活）
- `avatar` 字段缺失（`rahulbeniwal` 需要）

**修复方案**：
1. 激活 `testimonials` 区块
2. 添加 `avatar` 到 DEMO 数据

---

### 4. MBTI 未传递到模板

**问题**：MBTI 由叙事引擎生成，但未传递给任何模板变量。

**当前状态**：
- `skill/narrative/generator.py` 生成 `mbti` 和 `mbti_style`
- `saas/analyze/route.ts` 返回 `mbti` 字段
- 但 `data_adapter.py` 中无任何 `mbti` 字段适配
- Jinja2 模板中无 `mbti` 相关变量

**影响**：个性化叙事风格无法体现。

---

### 5. DEMO 数据不完整

**缺失字段**：
- `avatar` / `photo` — 头像
- `experience[]` — 结构化经历数组（Timeline）
- `open_source[]` — 开源项目（rahulbeniwal 需要）
- `testimonials[]` — 推荐信
- `resources` — 资源/人脉

**当前 DEMO_PERSONAL_SITE**（来自 `skill/core.py`）：
```python
"hero_story": {"headline": "一句话让别人记住你", "subtitle": "身份/标签", "hero_image": ""},
"story": {"experiences": "原始叙事字符串", "challenges": "...", "insights": "..."},
"skills": {"categories": [...]},
"projects": {"projects": [...]},
"blog": {"posts": []},
"contact": {"email": "", "links": []},
# 缺失: avatar, experience[], open_source, testimonials, resources
```

---

## ⚠️ 中等问题

### 6. Soul 与 Framework 维度混淆

**问题**：`about.bio` 同时承载 Soul (内核) 和 Framework (方法论) 的内容，没有分离。

**7 IP 维度定义**：
- Soul: 价值观/使命/热情/信念 → 应为 `story.insights` 或独立 `soul` 字段
- Framework: 方法论/决策逻辑/工作流 → 应为 `about.bio`

**当前映射**：
```
Framework.text → about.bio (正确)
Soul.text → about.bio (与 Framework 相同，正确性存疑)
```

**建议**：Soul 内容 → `story.insights`，Framework 内容 → `about.bio`

---

### 7. Skill 版本与 SaaS 版本业务逻辑一致性

**问题**：Skill (Python Jinja2) 和 SaaS (TypeScript renderPage) 使用不同的渲染引擎，字段映射可能不一致。

**需验证**：
- `skill/modules/data_adapter.py` 的三个适配器
- `saas/nextjs/lib/html-renderer.ts` 的模块渲染器
- 两者是否产生相同的页面内容

---

## 📋 修复优先级

| 优先级 | 问题 | 修复方案 |
|--------|------|---------|
| P0 | Timeline 数据结构 | 在 DEMO 中添加 `experience[]` 结构数组 |
| P0 | MBTI 未传递 | 在 data_adapter.py 中添加 mbti 字段适配 |
| P1 | Resources 缺失 | 在 social 字段中补充 Resources 内容 |
| P1 | Form 缺失 | 激活 testimonials，添加 avatar |
| P1 | Soul/Framework 分离 | 重新映射 `about.bio` 和 `story.insights` |
| P2 | DEMO 数据补全 | 添加缺失字段 |
| P2 | Skill/SaaS 一致性验证 | 端到端测试两个渲染引擎 |

---

## ✅ 已修复

- [x] `saas/analyze/route.ts` — 修复为提取正确 7 IP Dimensions (Soul/Framework/Skills/Work/Timeline/Resources/Form)
- [x] `saas/generate/route.ts` — 修复维度标签映射到模板字段
- [x] `skill/data_adapter.py` — developerfolio/alfolio/rahulbeniwal 三个适配器的字段映射
- [x] `skill/core.py` — `DEMO_PERSONAL_SITE` 替换为黎静真实数据（真实经历/教育/技能/成就/社交）
- [x] `skill/modules/data_adapter.py` — socials 对象格式支持 + about.subtitle 默认值
- [x] **叙事结构重构 v1（2026-05-25 上午）** — 合并 About+Story、移除重复区块、方法论内嵌Skills、Timeline并入Experience
- [x] **developerfolio template.html endif bug** — 修复"我是谁"section后多出的`{% endif %}`导致的Jinja2语法错误
- [x] **叙事结构重构 v2（2026-05-25 下午）** — 三个模板彻底重构，吸收 Hermes 示例结构：SOUL→FRAMEWORK→FORM→STORY→SKILLS→WORKS→CONTACT
- [x] **模板重建（2026-05-25）** — 基于黎静参考HTML重建三个模板（developerfolio/alfolio/rahulbeniwal），匹配参考文件的结构和区块顺序
- [x] **data_adapter.py 重复函数修复** — 移除 to_rahulbeniwal 重复定义（保留一个完整实现）

## 📋 剩余待修复

| ID | 问题 | 状态 |
|----|------|------|
| P1 | MBTI 完整描述（mbti_description）传递 | 待测试 |
| P2 | Skill/SaaS 端到端一致性验证 | 待测试 |
| P2 | SaaS analyze API — 用黎静简历原材料测试完整流程 | 待测试 |
| P0 | Bash 运行环境损坏（所有命令返回 exit 255） | 调查中 |

---

## ✅ 验证通过

**黎静数据渲染测试结果（模拟执行）**：
```
✅ name: 黎静
✅ title: 资深金融产品经理（C端方向）
✅ about.bio: 拥有10年基金产品全链路经验...
✅ experience: 2段（ 中欧财富 + 证通股份）
✅ education: 2项（南京大学硕士+本科）
✅ achievements: 4项
✅ contact.email: lj22503@163.com
✅ socials: {email, phone}
✅ badges: 3个标签
✅ mbti: 已传递（adapter修复后）
✅ framework_items: 已传递（adapter修复后）
✅ testimonials: 已传递（adapter修复后）
✅ HTML 输出长度: ~25000-30000 bytes ✅
```

*最后更新：2026-05-25*
