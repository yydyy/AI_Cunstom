# AI_Cunstom - AI规则管理系统

一套用于管理多种 AI 编程助手规则的工具集，支持 **Cline**、**Kimi**、**Cursor**、**Windsurf**、**Claude** 等多种格式，每个格式可以有独立的项目配置和 Skill 集合。

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

编辑 `config.json`，每个格式可以有独立的项目和 Skill 配置：

```json
{
    "formats": {
        "cline": {
            "enabled": true,
            "output_dir": ".clinerules",
            "projects": [
                {
                    "path": "D:\\ProjectA",
                    "include_all": true
                }
            ]
        },
        "kimi": {
            "enabled": true,
            "output_dir": ".kimi/skills",
            "projects": [
                {
                    "path": "D:\\ProjectA",
                    "include_skills": ["architect_review.md", "test_first.md"]
                },
                {
                    "path": "D:\\ProjectB",
                    "include_all": true
                }
            ]
        },
        "cursor": {
            "enabled": false,
            "output_dir": ".cursor/rules",
            "file_extension": ".mdc",
            "projects": []
        },
        "cursor_single": {
            "enabled": false,
            "output_file": ".cursorrules",
            "projects": []
        },
        "windsurf": {
            "enabled": false,
            "output_file": ".windsurfrules",
            "projects": []
        },
        "claude": {
            "enabled": false,
            "output_file": "CLAUDE.md",
            "projects": []
        }
    }
}
```

### 2. 运行脚本

```bash
python main.py
```

脚本会自动将规则文件按各格式配置部署到对应项目。

## 🤖 支持的 AI 格式

| 格式 | 配置名 | 输出路径 | 说明 |
|-----|--------|---------|------|
| **Cline** | `cline` | `.clinerules/` | 目录下直接放 `.md` 文件 |
| **Kimi** | `kimi` | `.kimi/skills/` | 子目录结构，每个 skill 一个子文件夹包含 `SKILL.md` |
| **Cursor** | `cursor` | `.cursor/rules/` | 目录下放 `.mdc` 文件（带 frontmatter） |
| **Cursor (单文件)** | `cursor_single` | `.cursorrules` | 合并所有 skill 到一个文件 |
| **Windsurf** | `windsurf` | `.windsurfrules` | 合并所有 skill 到一个文件 |
| **Claude** | `claude` | `CLAUDE.md` | 合并所有 skill 到一个文件 |

## 📋 配置示例

### 示例 1: 不同项目使用不同格式

```json
{
    "formats": {
        "cline": {
            "enabled": true,
            "output_dir": ".clinerules",
            "projects": [
                {"path": "D:\\WebProject", "include_all": true}
            ]
        },
        "kimi": {
            "enabled": true,
            "output_dir": ".kimi/skills",
            "projects": [
                {"path": "D:\\GameProject", "include_skills": ["cocos_skills.md", "performance_auditor.md"]}
            ]
        },
        "cursor": {
            "enabled": true,
            "output_dir": ".cursor/rules",
            "projects": [
                {"path": "D:\\AIPythonProject", "include_skills": ["architect_review.md", "test_first.md", "security_guard.md"]}
            ]
        }
    }
}
```

### 示例 2: 同一项目使用多个格式

```json
{
    "formats": {
        "cline": {
            "enabled": true,
            "output_dir": ".clinerules",
            "projects": [
                {"path": "D:\\MyProject", "include_all": true}
            ]
        },
        "cursor_single": {
            "enabled": true,
            "output_file": ".cursorrules",
            "projects": [
                {"path": "D:\\MyProject", "include_skills": ["architect_review.md"]}
            ]
        },
        "kimi": {
            "enabled": true,
            "output_dir": ".kimi/skills",
            "projects": [
                {"path": "D:\\MyProject", "include_skills": ["debugging_scientist.md", "error_handler.md"]}
            ]
        }
    }
}
```

运行后会同时在 `D:\MyProject` 生成：
```
MyProject/
├── .clinerules/              # Cline: 所有规则
│   ├── architect_review.md
│   ├── debugging_scientist.md
│   ├── error_handler.md
│   └── ...
├── .cursorrules              # Cursor: 只有架构审查
└── .kimi/skills/             # Kimi: 只有调试相关
    ├── debugging_scientist/SKILL.md
    └── error_handler/SKILL.md
```

### 示例 3: 同一项目不同格式使用不同 Skill 集合

```json
{
    "formats": {
        "cline": {
            "enabled": true,
            "output_dir": ".clinerules",
            "projects": [
                {
                    "path": "D:\\FullStackProject",
                    "include_skills": [
                        "architect_review.md",
                        "test_first.md",
                        "security_guard.md",
                        "clean_git_doc.md"
                    ]
                }
            ]
        },
        "kimi": {
            "enabled": true,
            "output_dir": ".kimi/skills",
            "projects": [
                {
                    "path": "D:\\FullStackProject",
                    "include_skills": [
                        "architect_review.md",
                        "test_first.md"
                    ]
                }
            ]
        }
    }
}
```

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

### 使用全部规则

```json
{
    "path": "D:\\YourProject",
    "include_all": true
}
```

### 推荐组合

| 场景 | 推荐规则 |
|-----|---------|
| 新功能开发 | `architect_review` + `test_first` + `security_guard` |
| Bug调试 | `debugging_scientist` + `devils_advocate` + `error_handler` |
| 性能优化 | `performance_auditor` + `architect_review` |
| Cocos游戏开发 | `cocos_skills` + `performance_auditor` |
| Cocos Framework 项目 | `cocos_framework_proto` + `cocos_skills` |
| 代码审查 | `architect_review` + `devils_advocate` + `security_guard` |

## 📚 规则说明

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
| `cocos_framework_proto.md` | Cocos Framework 类型扩展 | Vec/Sprite/Node 原型扩展、装饰器 |

## ⚙️ 配置选项详解

### formats 配置

| 格式 | 参数 | 说明 | 默认值 |
|-----|------|------|--------|
| `cline` | `enabled` | 是否启用 | `false` |
| | `output_dir` | 输出目录名 | `.clinerules` |
| | `projects` | 该格式的项目列表 | `[]` |
| `kimi` | `enabled` | 是否启用 | `false` |
| | `output_dir` | 输出目录名 | `.kimi/skills` |
| | `projects` | 该格式的项目列表 | `[]` |
| `cursor` | `enabled` | 是否启用 | `false` |
| | `output_dir` | 输出目录名 | `.cursor/rules` |
| | `file_extension` | 文件扩展名 | `.mdc` |
| | `projects` | 该格式的项目列表 | `[]` |
| `cursor_single` | `enabled` | 是否启用 | `false` |
| | `output_file` | 输出文件名 | `.cursorrules` |
| | `projects` | 该格式的项目列表 | `[]` |
| `windsurf` | `enabled` | 是否启用 | `false` |
| | `output_file` | 输出文件名 | `.windsurfrules` |
| | `projects` | 该格式的项目列表 | `[]` |
| `claude` | `enabled` | 是否启用 | `false` |
| | `output_file` | 输出文件名 | `CLAUDE.md` |
| | `projects` | 该格式的项目列表 | `[]` |

### projects 配置项

| 参数 | 说明 |
|-----|------|
| `path` | 目标项目路径（绝对路径） |
| `include_all` | 是否拷贝所有规则文件到该项目 |
| `include_skills` | 指定要拷贝的规则文件列表（优先级高于 `include_all`） |

### 兼容旧配置

如果使用的是旧版配置（配置了 `rules_dir` 和全局 `target_projects`），脚本会自动迁移：

```json
{
    "rules_dir": ".clinerules",
    "target_projects": [
        {"path": "D:\\Project", "include_all": true}
    ]
}
```

会自动转换为启用 `cline` 格式，并将 `target_projects` 迁移到 `formats.cline.projects`。

## 💡 设计原则

1. **格式独立**: 每个 AI 格式有自己的项目列表和 Skill 集合
2. **灵活组合**: 同一项目可以为不同 AI 配置不同的 Skill
3. **按需部署**: 只为需要的 AI 工具生成配置
4. **精简优先**: 每个规则控制在100-150字，避免上下文溢出

## 📄 License

MIT License
