<!--
 * @Author: yyd
 * @Date: 2026-04-06 15:22:32
 * @LastEditTime: 2026-04-06 15:24:39
 * @FilePath: \AI_Cunstom\rule\clean_git_doc.md
 * @Description:  工程规范模式,自动化高质量的注释和提交记录，维持项目“整洁度”。
-->
## Skill：文档与 Git 规范
- **文档标准**：每个新增公共函数都应提供对应语言的注释（如 JS/TS 的 JSDoc、Python 的 docstring），说明参数、返回值和可能错误。
- **提交信息**：给出代码后，建议标准提交信息格式：`feat/fix/refactor(scope): description`。
- **README 同步**：若变更引入新配置或公共 API，提醒同步更新项目 `README`。