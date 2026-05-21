# 开发工作流规则

## 每次修复的固定流程

1. **修复** — 改一处，commit message 描述改了什么
2. **测试** — 用 `python -c "..."` 验证 adapter 输出，或 `render_html_template()` 验证 HTML 生成
3. **通过** → 更新 README + SPEC.md（描述本次修复解决了什么问题）→ 推送 GitHub
4. **失败** → 重新修，再次测试，直到通过，再更新文档

## 禁止事项

- 不允许同时修复多个独立问题（无法定位报错来源）
- 不通过验证不推送（避免污染 GitHub 历史）
- README / SPEC.md 不留「待修复」「未知」等悬空状态

## commit message 格式

```
type: 简短描述

body（可选）：验证方式
```

type: `fix` | `feat` | `docs` | `refactor`
