<!--
 * @Author: yyd
 * @Date: 2026-04-06 15:21:09
 * @LastEditTime: 2026-04-06 15:21:15
 * @FilePath: \AI_Cunstom\rule\debugging_scientist.md
 * @Description:  调试专家模式,防止 AI “瞎猜”错误原因，强制它用科学方法论定位问题。
-->
## Skill: Scientific Debugging
* **Root Cause Analysis (RCA):** Before fixing, hypothesize 3 possible reasons for the bug. 
* **Minimum Reproducible Example:** If a fix is complex, suggest how to isolate the issue in a clean scene or script.
* **Log-First Approach:** Always suggest strategic `console.log` or `cc.log` points with unique identifiers to trace data flow before changing logic.
* **Regression Check:** When a fix is provided, explicitly state which other modules might be affected by this change.