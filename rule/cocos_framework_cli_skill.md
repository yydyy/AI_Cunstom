# cocosFrameworkCli 开发约束 Skill

## 1. 适用范围
- 本 Skill 适用于目标工程中已接入该框架脚本体系的代码（通常可见 `Script/App.ts`、`global.d.ts`、`$app`、`$gb`、`registerApp/registerView` 等特征）。
- 当任务涉及 Cocos 业务代码、管理器扩展、UI/事件/控制器注册时，优先遵循本 Skill。
- 目标是保证 AI 生成代码与框架既有约定一致，避免破坏 `$app`/`$gb` 生态和类型生成链路。

## 2. 全局对象与入口约定（强约束）
- 统一通过全局 `$app` 访问系统能力，不自行创建平行全局对象。
- `$app` 是 `App & IAppExtend`，扩展能力应通过 `registerApp` + 类型扩展注入，而不是直接改 `App` 主体。
- `$gb` 作为基础工具集合使用，核心包含：
  - `SingleFunc`
  - `SingletonProxy`
  - `Identifiable`
  - `registerView`
  - `registerCtrlId`
  - `registerEvent`
  - `registerApp`
- 禁止绕开框架做“裸单例”或“手写全局挂载”。

## 3. 管理器与模块扩展规范
- 新增管理器默认流程：
  1. 使用 `@$gb.Identifiable` 标识类。
  2. 使用 `SingleFunc` 或 `SingletonProxy` 包装。
  3. 通过 `$gb.registerApp("xxx", Manager)` 挂载到 `$app`。
  4. 由生成脚本更新 `types/d.ts/GenerateAppExtend.d.ts`，补齐类型。
- 选择建议：
  - 倾向 `SingleFunc`：保留类继承语义，常规推荐。
  - 使用 `SingletonProxy`：明确需要“多次 new 仍同实例”时使用。
- 高频调用路径（如 `update`）避免重复 `$app.xxx` 链式读取，先缓存引用再使用。

## 4. 自动生成文件约束（强约束）
- 目录 `template/Script/types/d.ts` 下文件视为“工具生成产物”，禁止手工改业务逻辑。
- 涉及以下映射变更时，必须通过装饰器/注册函数触发生成，不直接改 d.ts：
  - App 扩展映射：`GenerateAppExtend.d.ts`
  - Bundle 映射：`GenerateBundleExtend.d.ts`
  - Event 映射：`GenerateEventExtend.d.ts`
  - View 映射：`GenerateViewExtend.d.ts`
  - CtrlId 映射：`GenerateCtrlIdExtend.d.ts`
- 若用户要求新增事件、界面、控制器、bundle，AI 应优先修改“源定义代码”，并提醒执行对应 npm 生成命令。

## 5. UI / Ctrl / Event 约定
- View 必须通过 `registerView({...})` 体系声明，确保 UI ID 与路径可被工具识别。
- Ctrl 必须使用 `registerCtrlId(...)` 参与类型映射，避免字符串散落。
- 事件定义优先 `registerEvent<T>(...)`，事件参数类型必须显式声明，避免 `any`。
- 业务代码内，界面开关与事件分发优先使用 `$app.view`、`$app.dispatch`，避免旁路总线。

## 5.1 Bundle 新增规则（强约束）
- 新增 Bundle 名称必须通过 `registerBundle("bundleName")` 进行注册，不直接手改 `Bundles` 常量或 `GenerateBundleExtend.d.ts`。
- Bundle 命名使用小写英文，建议按业务域命名（如 `battle`、`login`、`shop`），禁止随意缩写和无语义命名。
- 涉及 Bundle 资源路径时，统一遵循框架约定格式（如 `bundleName.xx/xxx`），避免硬编码散落。
- 新增/修改 Bundle 后，必须执行对应生成命令更新类型映射，确保 `BundleIdType` 自动收敛。
- 业务代码中涉及 Bundle 加载，优先走 `$app.load` 相关接口，不直接分散调用底层 bundle API。

## 6. 资源、异步与生命周期规范（Cocos 重点）
- 资源加载优先走 `$app.load`，避免分散使用原生加载 API 造成释放链不一致。
- 需要生命周期绑定的资源，必须传入 `lifeTarget` 并遵守 `ReleaseType` 语义。
- 异步回调或延时逻辑执行前，必须校验节点/组件有效性（如 `isValid`）。
- 计时器统一使用 `$app.timer` / `$app.uiTool` 调度接口，禁止无归属的裸 `setTimeout`。

## 7. 编码输出要求（给 AI 的执行指令）
- 生成代码时必须优先复用现有框架能力，不重复造轮子。
- 新增功能时优先给出“最小改动方案”，保持与现有目录和命名风格一致。
- 任何不确定 API（尤其 Cocos 版本差异）必须显式标注并请求确认，不可臆测。
- 当用户需求与框架约定冲突时，先警告风险，再提供兼容实现路径。

## 8. 推荐任务模板
- 新增 App 管理器：
  - 生成 `Extend/mgr/XXXMgr.ts`
  - `@$gb.Identifiable` + `SingleFunc/SingletonProxy`
  - `$gb.registerApp("xxx", XXXMgr)`
  - 提醒执行 app-extend 类型生成命令
- 新增 Bundle：
  - 在源定义代码中调用 `registerBundle("xxx")`
  - 资源引用统一使用 `bundleName.xx/xxx` 规则
  - 提醒执行 bundle-extend 类型生成命令
- 新增界面：
  - 新建 View 脚本并使用 `registerView`
  - 使用 `UiId` 体系访问
  - 提醒执行 view-map 类型生成命令
- 新增事件：
  - 在事件定义处 `registerEvent<T>`
  - 业务层通过 `$app.dispatch` 收发
  - 提醒执行 event-type 生成命令
