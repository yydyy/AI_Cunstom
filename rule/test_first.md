<!--
 * @Author: yyd
 * @Date: 2026-04-06 20:20:00
 * @LastEditTime: 2026-04-06 20:20:09
 * @FilePath: \AI_Cunstom\rule\test_first.md
 * @Description:  测试驱动模式,确保新功能有测试覆盖，减少回归风险
-->
## Skill：测试优先思维
- **测试覆盖**：新增功能至少补一个覆盖主流程（happy path）的单元测试用例。
- **边界先行**：实现前先识别边界条件（`null`、空值、最大值、最小值）。
- **Mock 策略**：识别需隔离的外部依赖（API、数据库、文件 I/O）并明确 Mock 点。