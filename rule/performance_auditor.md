<!--
 * @Author: yyd
 * @Date: 2026-04-06 15:23:12
 * @LastEditTime: 2026-04-06 15:24:22
 * @FilePath: \AI_Cunstom\rule\performance_auditor.md
 * @Description:  性能审计员,专门针对你提到的 GPU Instancing 和渲染优化。
-->
## Skill：性能审计员
- **分配监控**：严格减少 `update()` 与高频循环中的对象创建，优先建议预分配策略。
- **DrawCall 守卫**：当 UI 布局或节点结构可能破坏合批（如材质混用、ZIndex 交错）时必须预警。
- **内存泄漏检查**：使用事件总线或全局计时器时，必须同时给出 `off` / `destroy` 清理逻辑。