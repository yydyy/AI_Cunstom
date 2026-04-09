<!--
 * @Author: yyd
 * @Date: 2026-04-06 20:20:00
 * @LastEditTime: 2026-04-06 20:20:20
 * @FilePath: \AI_Cunstom\rule\security_guard.md
 * @Description:  安全审计模式,防止常见安全漏洞，保护敏感数据
-->
## Skill：安全守卫
- **输入校验**：永远不要直接信任用户输入，处理前必须清洗与校验。
- **敏感数据保护**：禁止硬编码 API Key、密码、Token，统一使用环境变量或安全存储。
