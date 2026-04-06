# AI_Cunstom - AI规则管理系统

一套用于管理 Cline AI 编程助手规则的工具集，支持场景化规则组合，让 AI 输出更符合你的项目规范。

## 📖 项目结构

```
AI_Cunstom/
├── config.json         # 配置文件
├── main.py             # 规则管理脚本
└── rule/               # 规则文件目录
    ├── 00_rule_priority.md    # 规则优先级说明
    ├── architect_review.md    # 架构设计审查
    ├── clean_git_doc.md       # 文档与Git规范
    ├── cocos_skills.md        # Cocos开发全流程
    ├── debugging_scientist.md # 科学调试方法
    ├── devils_advocate.md     # 批判性思维
    ├── error_handler.md       # 错误处理模式
    ├── performance_auditor.md # 性能审计
    ├── security_guard.md      # 安全审计
    └── test_first.md          # 测试驱动模式
```

## 🚀 快速开始

### 1. 配置目标项目

编辑 `config.json`：

```json
{
    "rules_dir": ".clinerules",
    "target_projects": [
        {
            "path": "D:\\YourProject",
            "include_all": "true"
        }
    ]
}
```

### 2. 运行脚本

```bash
python main.py
```

脚本会自动将规则文件拷贝到目标项目的 `.clinerules/` 目录。

## 🎯 场景化规则组合

### 按需选择规则

```json
{
    "path": "D:\\YourProject",
    "include_skills": [
        "architect_review.md",
        "test_first.md",
        "security_guard.md"
    ]
}
```

### 推荐组合

| 场景 | 推荐规则 |
|-----|---------|
| 新功能开发 | `architect_review` + `test_first` + `security_guard` |
| Bug调试 | `debugging_scientist` + `devils_advocate` + `error_handler` |
| 性能优化 | `performance_auditor` + `architect_review` |
| Cocos游戏开发 | `cocos_skills` + `performance_auditor` |

## 📋 规则说明

| 规则文件 | 用途 | 核心要点 |
|---------|------|---------|
| `architect_review.md` | 架构设计审查 | SOLID原则、设计模式、解耦 |
| `clean_git_doc.md` | 文档与Git规范 | JSDoc、Commit规范、README维护 |
| `cocos_skills.md` | Cocos开发全流程 | 版本适配、性能优化、同步架构 |
| `debugging_scientist.md` | 科学调试方法 | 根因分析、最小复现、日志策略 |
| `devils_advocate.md` | 批判性思维 | 边缘情况、安全检查、性能陷阱 |
| `error_handler.md` | 错误处理模式 | 优雅降级、错误传播策略 |
| `performance_auditor.md` | 性能审计 | 内存监控、DrawCall、泄漏检测 |
| `security_guard.md` | 安全审计 | 输入验证、敏感数据保护 |
| `test_first.md` | 测试驱动模式 | 测试覆盖、边界条件、Mock策略 |

## ⚙️ 配置选项

| 参数 | 说明 |
|-----|------|
| `rules_dir` | 目标项目中存放规则的目录名，默认 `.clinerules` |
| `target_projects` | 目标项目列表 |
| `include_all` | 是否拷贝所有规则 |
| `include_skills` | 指定要拷贝的规则文件列表 |

## 💡 设计原则

1. **精简优先**：每个规则控制在100-150字，避免上下文溢出
2. **场景触发**：按任务类型动态加载，避免规则冲突
3. **质量优先**：3条核心要点 > 10条冗长描述

## 📄 License

MIT License