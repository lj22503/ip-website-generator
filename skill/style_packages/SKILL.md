# ip-website-generator + DESIGN.md 双轨封装

## 触发条件

当用户说"引入 DESIGN.md"、"加风格包"、"封装 skill"时使用。

---

## 背景

awesome-claude-design 证明了 DESIGN.md 可以从"设计文档"升级为"AI 可执行技能定义"。ip-website-generator 当前缺少一致的设计约束层，每次生成风格随机。引入 DESIGN.md 封装模式可以解决此问题。

---

## 执行步骤

### Step 1: 建立风格包目录结构

```
skill/
├── design_md_generator.py   # 已有：品牌知识库 + 推理引擎
├── design_systems/          # 已有：设计系统加载器
├── style_packages/         # 新增：个人IP风格包
│   ├── SKILL.md            # 风格包技能定义
│   ├── README.md           # 风格说明
│   └── references/
│       └── DESIGN.md       # 设计系统文档
└── ...
```

### Step 2: 创建风格包 SKILL.md

```markdown
---
name: IP Style Package - 极客风
description: 个人IP网站极客风格包，含完整DESIGN.md和渲染规则
tags: [ip-website, design-md, style-package]
version: 1.0.0
---

# IP Style Package - 极客风

## 何时使用

用户选择「极客风」风格时，加载此包。

## 文件读取顺序

1. `references/DESIGN.md` — 设计系统定义（AI 主要读取此文件）
2. `README.md` — 风格说明和视觉参考

## 核心约束（不可绕过）

- 颜色语义绑定：DESIGN.md 中的颜色必须带角色注释
- 间距倍数：强制使用 4px/8px 几何倍数
- 字体：正文 Inter，代码 JetBrains Mono
- 禁止：纯白背景、随机颜色、非几何倍数间距

## 生成规则

生成网站时，Agent 必须：
1. 先读取 DESIGN.md 获取完整设计令牌
2. 在 HTML 中引用 CSS 变量（不得硬编码颜色值）
3. 输出「风格预览」供用户确认后再继续

## 配套资产

- `references/DESIGN.md` — 9层结构设计系统文档
- CSS 变量自动从 DESIGN.md 提取并注入
```

### Step 3: 在 core.py 中集成风格包选择

```python
# 风格包注册表
STYLE_PACKAGES = {
    "geek": {
        "name": "极客风",
        "description": "深色主题，低饱和，强调技术感和专业性",
        "path": "style_packages/geek/SKILL.md",
    },
    "warm": {
        "name": "温暖风",
        "description": "暖色调，柔和间距，亲切感强",
        "path": "style_packages/warm/SKILL.md",
    },
    "minimal": {
        "name": "简约风",
        "description": "大量留白，高对比度，极简主义",
        "path": "style_packages/minimal/SKILL.md",
    },
    "bold": {
        "name": "大胆风",
        "description": "强视觉冲击，大字体，大面积色块",
        "path": "style_packages/bold/SKILL.md",
    },
}

def generate_with_style_package(user_request, style_package):
    """基于风格包生成网站"""
    pkg = STYLE_PACKAGES.get(style_package)
    if not pkg:
        raise ValueError(f"Unknown style package: {style_package}")
    
    # 读取 DESIGN.md
    design_md_path = pkg["path"].replace("SKILL.md", "references/DESIGN.md")
    design_md = read_file(design_md_path)
    
    # 提取设计令牌
    tokens = design_md_generator.parse_design_md(design_md)
    
    # 生成 HTML（带约束）
    html = render(user_request, tokens)
    return html
```

### Step 4: 新增风格包 DESI GN.md 示例（极客风）

在 `style_packages/geek/references/DESIGN.md`：

```markdown
# DESIGN.md — 极客风个人IP网站

## 1. Visual Theme & Atmosphere

深色技术感界面，以 `#0a0a0f` 为底，配合 `#00d4ff` 青色点缀。整体感觉：专业、极客、有深度。

## 2. Color Palette & Roles

- `--bg-primary: #0a0a0f` (深空黑 - 主背景)
- `--bg-surface: #12121a` (暗紫灰 - 卡片/面板)
- `--text-primary: #e8e8ec` (亮灰 - 主文字)
- `--text-secondary: #8888a0` (中灰 - 次要文字)
- `--accent: #00d4ff` (科技青 - 强调色/CTA)
- `--accent-hover: #00b8e6` (青绿 - 悬停态)
- `--border: #1e1e2e` (暗线 - 分割线)
- `--success: #00d4aa` (翠绿 - 成功状态)
- `--error: #ff4466` (红 - 错误状态)

## 3. Typography Rules

- 主字体: Inter, -apple-system, sans-serif
- 标题: weight 600, letter-spacing -0.02em
- 正文: weight 400, line-height 1.65
- 代码: JetBrains Mono, monospace
- 字号: 14/16/18/24/32/48px（倍数系统）

## 4. Component Stylings

- 按钮主色: backgroundColor: var(--accent), rounded: 6px
- 卡片: backgroundColor: var(--bg-surface), rounded: 12px, padding: 24px
- 输入框: backgroundColor: transparent, border: 1px solid var(--border)

## 5. Layout Principles

- 桌面: 最大宽度 900px，居中
- 间距基准: 8px 倍数（8/16/24/32/48/64）
- 卡片网格: 1-2 列，gap: 24px

## 6. Depth & Elevation

- 卡片: box-shadow: 0 4px 24px rgba(0,0,0,0.4)
- 悬停: box-shadow 增强，transform: translateY(-2px)

## 7. Do's and Don'ts

✓ 始终使用 CSS 变量，不得硬编码颜色
✓ 保持 8px 间距倍数
✗ 不得使用纯白背景（#ffffff）
✗ 不得使用超出 palette 的随机颜色

## 8. Responsive Behavior

- mobile (<640px): 单列布局，padding: 20px
- tablet (640-1024px): 双列网格
- desktop (>1024px): 居中最大 900px

## 9. Agent Prompt Guide

生成网站时：
1. 读取上面所有颜色和排版规则
2. 生成 HTML 时全部使用 CSS 变量（不得硬编码）
3. 首屏生成后展示「风格预览」确认
```

---

## 验证步骤

1. 选择一个风格包（如极客风）
2. 输入简单请求："生成一个关于我的首页"
3. 验证输出包含 CSS 变量引用而非硬编码颜色
4. 验证间距是 8px 倍数
5. 验证风格预览展示正确

---

## 坑点

- **不得硬编码颜色**：生成规则必须强制使用 CSS 变量，DESIGN.md 中的颜色全部以变量形式注入
- **风格预览确认**：在完整生成前先输出预览，避免用户不满意要返工
- **DESIGN.md 解析**：使用已有的 `design_md_generator.py` 解析 YAML frontmatter 和叙事内容，提取令牌注入 CSS

---

## 关联文件

- `design_md_generator.py` — 已有品牌知识库和推理引擎
- `modules/registry.py` — 已有模块定义（7-11个内容模块）
- `rendering/renderer.py` — 渲染器，需支持 DESIGN.md 约束注入
- `style_packages/` — 新增风格包目录（每个风格包含 SKILL.md + references/DESIGN.md）