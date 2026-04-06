<!--
 * @Author: yyd
 * @Date: 2026-04-06 15:21:37
 * @LastEditTime: 2026-04-06 15:25:30
 * @FilePath: \AI_Cunstom\rule\architect_review.md
 * @Description:  架构审计模式,在写代码前，先过一遍设计模式，避免“面条代码”
-->
## Skill: Senior Architect Review
* **SOLID Principles:** Evaluate if the new feature violates the Single Responsibility or Open-Closed principle.
* **Design Pattern Suggestion:** If logic becomes complex, suggest a suitable pattern (e.g., Observer, Command, or State Machine) instead of nested IF-ELSE.
* **Decoupling:** Actively look for hard-coded dependencies and suggest moving them to config files or Event-based communication.
* **Interface First:** Prioritize defining public methods and properties (API surface) before writing private implementation logic.