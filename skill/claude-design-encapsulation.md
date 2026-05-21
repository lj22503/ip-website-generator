# Claude Design 封装模式深度拆解

## 文档信息

- **输出路径**: `skill/claude-design-encapsulation.html`
- **数据来源**: GitHub/VoltAgent/awesome-claude-design, Web Search
- **生成时间**: 2026-05-17

---

## 核心结论（一句话）

> **将设计系统从"给人类阅读的文档"转变为"给 AI 执行的操作指令"**

---

## 关键架构

```
DESIGN.md（技能定义层）
  ├── 9层叙事结构（Overview/Colors/Typography/.../Do's&Donts）
  └── Agent Prompt Guide（给AI看的执行约束）
       ↓ Claude Design（Opus 4.7驱动）
  ├── colors_and_type.css（CSS变量+字体刻度）
  ├── preview/（颜色/字体/间距/组件预览卡）
  ├── UI Kit（完整营销页面HTML）
  └── SKILL.md（可复用技能文件）
```

---

## 与普通 Coding Agent 的本质差异

| | 普通 Agent | DESIGN.md + Agent |
|---|---|---|
| 风格 | 每次随机 | 精确一致 |
| 颜色 | 乱配或偏好 | 语义绑定 |
| 间距 | 随意 | 4px/8px倍数强制 |
| 组件 | 模糊堆积 | 明确规则 |
| 约束 | 无 | 硬性审美红线 |

**一句话总结**：普通 Agent 是"画家"——每次创作风格随机。DESIGN.md + Agent 是"熟练工"——严格按设计规范执行。

---

## 对 ip-website-generator 的落地价值

```
现在：
  用户选风格 → Agent自由生成 → 每次风格随机

引入 DESIGN.md 后：
  用户选风格包 → DESIGN.md注入约束 → Agent精准生成
                                        ↓
                               风格预览确认 → 用户确认 → 输出
```

### 实施4阶段

1. **Phase 1**: 整理 3-5 个示范性 DESIGN.md（个人IP风格包）
2. **Phase 2**: 封装为 ip-website-generator 的 skill（双轨：README.md + SKILL.md）
3. **Phase 3**: 在生成 prompt 中引用 DESIGN.md 约束
4. **Phase 4**: 输出时附「风格预览」确认步骤

### 核心坑点

- **不得硬编码颜色**：生成规则必须强制使用 CSS 变量，DESIGN.md 中的颜色全部以变量形式注入
- **风格预览确认**：在完整生成前先输出预览，避免用户不满意要返工
- **DESIGN.md 解析**：使用已有的 `design_md_generator.py` 解析 YAML frontmatter 和叙事内容，提取令牌注入 CSS

---

## 关联文件

- `design_md_generator.py` — 已有品牌知识库和推理引擎（claude/linear/notion/stripe/vercel 5个品牌数据）
- `style_packages/SKILL.md` — 新增风格包技能封装方案
- `modules/registry.py` — 已有模块定义（7-11个内容模块）
- `rendering/renderer.py` — 渲染器，需支持 DESIGN.md 约束注入