<!--
 * @Author: yyd
 * @Date: 2026-04-06 20:20:00
 * @LastEditTime: 2026-04-06 20:20:34
 * @FilePath: \AI_Cunstom\rule\error_handler.md
 * @Description:  错误处理模式,构建健壮的错误处理机制，提升系统稳定性
-->
## Skill: Resilient Error Handling
* **Graceful Degradation:** Always provide fallback behavior when a feature fails.
* **Error Propagation:** Decide strategy: fail-fast for critical errors, silent-retry for transient issues.
