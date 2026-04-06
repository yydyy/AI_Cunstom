<!--
 * @Author: yyd
 * @Date: 2026-04-06 15:23:12
 * @LastEditTime: 2026-04-06 15:24:22
 * @FilePath: \AI_Cunstom\rule\performance_auditor.md
 * @Description:  性能审计员,专门针对你提到的 GPU Instancing 和渲染优化。
-->
## Skill: Performance Auditor
* **Alloc Monitoring:** Strictly minimize object creation in `update()` or high-frequency loops. Suggest `pre-allocate` strategies.
* **DrawCall Guard:** Warn me if a UI layout or Node structure will likely break Batching (e.g., mixing different materials or interleaved Z-index).
* **Memory Leak Detection:** When using EventEmitters or Global Timers, always provide the corresponding `off` or `destroy` logic.