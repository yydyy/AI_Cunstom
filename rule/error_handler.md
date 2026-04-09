<!--
 * @Author: yyd
 * @Date: 2026-04-06 20:20:00
 * @LastEditTime: 2026-04-06 20:20:34
 * @FilePath: \AI_Cunstom\rule\error_handler.md
 * @Description:  错误处理模式,构建健壮的错误处理机制，提升系统稳定性
-->
## Skill：韧性错误处理
- **优雅降级**：功能失败时必须提供可用的兜底行为。
- **错误传播策略**：明确区分关键错误（快速失败）与瞬时错误（静默重试）。
