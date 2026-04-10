<!--
 * @Author: yyd
 * @Description: cocosFrameworkCli 框架开发指南 - 整合类型扩展与开发约束
-->

# cocosFrameworkCli 框架开发指南

> **背景**：本项目使用 `cocosFrameworkCli` 框架（通过 `npm run ins` 安装），在 `Script/Extend/prototype` 下扩展了 Cocos 引擎类型的原型方法，并在 `Script/global.d.ts` 中声明了全局类型。

---

## 1. 全局对象与入口约定（强约束）

### 1.1 核心全局对象
- 统一通过全局 `$app` 访问系统能力，不自行创建平行全局对象
- `$app` 是 `App & IAppExtend`，扩展能力通过 `registerApp` + 类型扩展注入
- `$gb` 作为基础工具集合，核心包含：
  - `SingleFunc`、`SingletonProxy`、`Identifiable`
  - `registerView`、`registerCtrlId`、`registerEvent`、`registerApp`

### 1.2 禁止行为
- 禁止绕开框架做"裸单例"或"手写全局挂载"
- 禁止重复 `$app.xxx` 链式读取（高频调用路径先缓存引用）

---

## 2. 全局类型定义 (global.d.ts)

### 2.1 基础类型工具

| 类型 | 定义 | 用途 |
|-----|------|------|
| `valueof<T>` | `T[keyof T]` | 获取对象类型的 value 类型 |
| `BaseType` | `number \| string` | 基础类型别名 |
| `UiIdType` | `valueof<typeof UiId>` | UI ID 类型 |
| `CtrlIdType` | `valueof<typeof CtrlId>` | 控制器 ID 类型 |

### 2.2 Window 接口扩展

```typescript
interface Window {
    $app: AppType                                    // 全局应用管理器
    $forEach: <T>(callback, param, target?, isReversed?) => void  // 通用遍历
    CONDITION_ASSET: (condition, isDebugger?, ...args) => void   // 条件断言
    gRegisterClass: InstanceType<typeof Rgclass>    // 类/函数注册中心
}
```

### 2.3 全局常量（可直接使用）

```typescript
const $app: AppType
const $forEach: <T>(...) => void
const CONDITION_ASSET: (condition, ...) => void
const gRegisterClass: InstanceType<typeof Rgclass>
```

---

## 3. cc 命名空间扩展

### 3.1 cc.Node 扩展

| 方法 | 签名 | 说明 |
|-----|------|------|
| `onPixel` | `<T>(type, callback, target?, threshold?, useCapture?) => T` | 像素级点击注册（透明区域不响应） |
| `onceOnPixel` | `<T>(type, callback, target?, threshold?, useCapture?) => T` | 像素级单次点击 |
| `offPixel` | `(type, callback?, target?, useCapture?) => void` | 取消像素点击监听 |
| `getComponentOrAdd` | `<T>(type: { prototype: T }) => T` | 获取组件，不存在则自动添加 |
| `getChildComponentByName` | `<T>(name: string, type) => T` | 按名称获取子节点组件 |
| `getComponentInstallof` | `<T>(type: T \| string) => T` | instanceof 方式获取（处理装饰器导致的类型问题） |

### 3.2 cc.Component 扩展

| 方法 | 说明 |
|-----|------|
| `getComponentOrAdd<T>(type)` | 同 Node 方法 |
| `getChildComponentByName<T>(childName, type)` | 同 Node 方法 |
| `getComponentInstallof<T>(type)` | 同 Node 方法 |

### 3.3 cc.Sprite 扩展

| 方法 | 签名 | 说明 |
|-----|------|------|
| `setAutoSpriteFrame` | `(path, lifeTarget?, releaseType?, immediatelyClearOld?) => Promise<void>` | 自动加载 SpriteFrame 并绑定生命周期 |

**参数说明**：
- `path`: `bundleName.folder/assetName` 格式，如 `"ui.common/btn_ok"`
- `lifeTarget`: 生命周期对象（默认自身），销毁时自动释放资源
- `releaseType`: 释放类型枚举
- `immediatelyClearOld`: 是否立即释放旧资源（默认 false）

### 3.4 cc.SpriteFrame 扩展

| 属性/方法 | 签名 | 说明 |
|----------|------|------|
| `setAutoTexture` | `(path, lifeTarget?, releaseType?, clearOld?, params?) => Promise<void>` | 自动加载 Texture2D 并绑定生命周期 |
| `_rect` | `cc.Rect` | 内部矩形属性 |
| `_texture` | `cc.Texture2D` | 内部纹理属性 |

### 3.5 cc.Vec2 / cc.Vec3 扩展 (ccVec.ts)

| 方法 | 说明 | 示例 |
|-----|------|------|
| `vec2.toVec3(z?)` | Vec2 转 Vec3，z 默认为 0 | `const v3 = pos.toVec3(100)` |
| `vec3.toVec2()` | Vec3 转 Vec2，抛弃 z 值 | `const v2 = pos.toVec2()` |

---

## 4. 装饰器与工具

### 4.1 自动绑定装饰器 (Deserialize.ts)

| 装饰器 | 用途 | 示例 |
|-------|------|------|
| `@autoBindAttribute(nodeName, classType?)` | 自动绑定单个节点属性 | `@autoBindAttribute("btn_ok", cc.Button) btnOk: cc.Button` |
| `@autoBindAttributes(nodeName, ...classTypes)` | 自动绑定多个组件类型 | `@autoBindAttributes("icon", cc.Sprite, cc.Button) icon: cc.Sprite` |

### 4.2 单例工具

| 装饰器/函数 | 用途 | 示例 |
|------------|------|------|
| `SingleFunc(target)` | 单例工厂函数 | `const MyClass = SingleFunc(class { ... })` |
| `SingletonProxy(classCtor, ...args)` | 单例代理（修改 constructor） | `const MySingle = SingletonProxy(MyClass)` |

### 4.3 注册装饰器

| 装饰器/函数 | 用途 | 示例 |
|------------|------|------|
| `registerClass(id)` | 注册类到全局 | `@registerClass(100) class MyClass {}` |
| `registerCtrlId(id)` | 注册控制器 ID | `@registerCtrlId("BattleCtrl") class BattleCtrl {}` |
| `registerEvent<T>(id)` | 注册事件类型（仅类型标记） | `registerEvent<(data: string) => void>("EVENT")` |
| `registerView(info)` | 注册界面定义 | `@registerView({ uid: "MainView", path: "..." })` |
| `registerApp(key, singleton)` | 注册单例到 $app | `registerApp("battle", BattleMgr)` |
| `registerBundle("bundleName")` | 注册 Bundle 名称 | 必须通过此方式注册，禁止直接修改 `GenerateBundleExtend.d.ts` |

### 4.4 异步安全

```typescript
// Promise 扩展
await promise.isValid(this)  // 检查生命周期，无效时静默返回

// 装饰器
@SafeAsync
async loadRes() { }  // 自动捕获异步中断错误
```

### 4.5 安全延时

```typescript
setTimeOutSafe(() => { }, 3000)
setTimeOutSafe(() => { }, 1000, "ui")     // 分组管理
setTimeOutSafe(() => { }, 2000, "network")
clearTimeoutSafe("ui")      // 清除指定分组
clearTimeoutSafe()          // 清除所有
```

---

## 5. CoreScripts.d.ts 扩展类型

### 5.1 增强数组 ccArray

```typescript
const arr = ccArray(1, 2, 3);
arr.firstOne                    // 获取第一个元素
arr.lastOne                     // 获取最后一个元素
arr.isEmpty                     // 判断是否为空
arr.pushCheck(ele)              // 去重添加
arr.reverseForEach(cb)          // 倒序遍历（返回 true 可中断）
arr.checkCCValid()              // 检查 Cocos 对象有效性
arr.isEqual(other, compareType?, ignoreOrder?, exAry?)  // 深度比较
```

### 5.2 分类日志 clog

```typescript
clog.log("普通日志")
clog.error("错误")
clog.net("网络日志")      // 网络层
clog.model("数据日志")    // 数据/控制层
clog.view("视图日志")     // UI 层
clog.setTags(tagMask)     // 按位运算设置要显示的日志类型
```

### 5.3 字符串扩展

```typescript
"%s上学了".format("小金鱼")     // 格式化字符串
"123".toNumber()              // 转为数字
"1,2,3".toAry(",", true)      // 转数组，true 表示转数字数组
"prefab/name".clonePrefab(lifeTarget?, parent?, name?)  // 克隆预制体
"prefab/name".clonePrefabScript<T>(T, lifeTarget?, parent?, name?)  // 克隆并返回脚本
"abc".lastChar()              // 获取最后一个字符
```

### 5.4 数字扩展

```typescript
const num = 12345
num.toNumber()           // 返回自身
num.transShowZh()        // 转换为 "1.2万" / "1.2亿" 中文显示
num.transShowEn()        // 转换为 "1.2W" / "1.2Y" 英文显示
```

### 5.5 类注册中心 gRegisterClass

```typescript
// 注册
gRegisterClass.setClass(100, MyClass)

// 获取
const Cls = gRegisterClass.getClassById<MyClass>(100)
const id = gRegisterClass.getIdByTarget(MyClass)

// 销毁钩子
gRegisterClass.registerDestroyHook(comp, fn)
```

---

## 6. 管理器与模块扩展规范

### 6.1 新增管理器流程

1. 创建 `Extend/mgr/XXXMgr.ts`
2. 使用 `@$gb.Identifiable` 标识类
3. 使用 `SingleFunc` 或 `SingletonProxy` 包装
4. 通过 `$gb.registerApp("xxx", XXXMgr)` 挂载到 `$app`
5. **提醒用户**：执行 `npm run app-extend` 更新类型

### 6.2 选择建议

- **SingleFunc**：保留类继承语义，常规推荐
- **SingletonProxy**：明确需要"多次 new 仍同实例"时使用

---

## 7. 自动生成文件约束（强约束）

目录 `template/Script/types/d.ts` 下文件视为**工具生成产物**，禁止手工修改。

### 必须通过装饰器触发生成

| 映射类型 | 文件 | 修改方式 | 生成命令 |
|---------|------|---------|---------|
| App 扩展 | `GenerateAppExtend.d.ts` | `registerApp` | `npm run app-extend` |
| Bundle 映射 | `GenerateBundleExtend.d.ts` | `registerBundle` | `npm run bundle-extend` |
| Event 映射 | `GenerateEventExtend.d.ts` | `registerEvent<T>` | `npm run event-type` |
| View 映射 | `GenerateViewExtend.d.ts` | `registerView` | `npm run view-map` |
| CtrlId 映射 | `GenerateCtrlIdExtend.d.ts` | `registerCtrlId` | - |

---

## 8. UI / Ctrl / Event / Bundle 约定

### 8.1 View 约定
- 必须通过 `registerView({...})` 体系声明
- 确保 UI ID 与路径可被工具识别
- 业务代码内优先使用 `$app.view` 开关界面

### 8.2 Ctrl 约定
- 必须使用 `registerCtrlId(...)` 参与类型映射
- 避免字符串散落

### 8.3 Event 约定
- 优先 `registerEvent<T>(...)`
- 事件参数类型必须显式声明，避免 `any`
- 业务层通过 `$app.dispatch` 收发

### 8.4 Bundle 新增规则（强约束）

- **必须通过 `registerBundle("bundleName")` 注册**，禁止直接修改 `Bundles` 常量或 `GenerateBundleExtend.d.ts`
- Bundle 命名使用小写英文，按业务域命名（如 `battle`、`login`、`shop`）
- 资源路径统一遵循 `bundleName.xx/xxx` 格式
- 业务代码中优先走 `$app.load` 相关接口

---

## 9. 资源、异步与生命周期规范

### 9.1 资源加载
- 优先走 `$app.load`，避免分散使用原生加载 API
- 需要生命周期绑定的资源，必须传入 `lifeTarget` 并遵守 `ReleaseType` 语义

### 9.2 异步安全
- 异步回调或延时逻辑执行前，必须校验节点/组件有效性（如 `isValid`）
- 计时器统一使用 `$app.timer` / `$app.uiTool`，禁止裸 `setTimeout`

---

## 10. 必须使用扩展 API 的场景

| 场景 | 推荐做法 | 避免 |
|-----|---------|------|
| 获取组件不存在时 | `getComponentOrAdd<T>(type)` | `getComponent ?? addComponent` |
| 不规则点击区域 | `onPixel` / `onceOnPixel` | `on` / `once` |
| 加载显示图片 | `setAutoSpriteFrame(path, this)` | `resources.load` + 手动释放 |
| 遍历各种集合 | `$forEach(cb, collection)` | 手写 for 循环 |
| 单例管理 | `SingleFunc` / `registerApp` | 全局变量 |
| 装饰器导致 instanceof 失效 | `getComponentInstallof` | `instanceof` |

---

## 11. 典型代码示例

```typescript
// ===== 自动绑定示例 =====
export class MainView extends BaseView {
    @autoBindAttribute("btn_start", cc.Button)
    btnStart: cc.Button
    
    @autoBindAttribute("avatar", cc.Sprite)
    avatar: cc.Sprite

    async setAvatar(url: string) {
        // 使用扩展方法自动管理资源生命周期
        await this.avatar.setAutoSpriteFrame(url, this)
    }
}

// ===== 组件获取示例 =====
// 不存在则自动添加
const anim = this.getComponentOrAdd(cc.Animation)

// 获取子节点组件
const icon = this.getChildComponentByName("icon", cc.Sprite)

// ===== 像素点击示例 =====
this.node.onPixel(
    cc.Node.EventType.TOUCH_END, 
    this.onClick, 
    this, 
    10  // 透明度阈值
)

// ===== 遍历示例 =====
$forEach((value, key) => {
    console.log(key, value)
}, someMap, this, false)

// ===== 新增管理器模板 =====
@$gb.Identifiable
class MyMgr {
    init() { }
}
const MyMgrSingle = SingleFunc(MyMgr)
$gb.registerApp("my", MyMgrSingle)
// 提醒：执行 npm run app-extend 更新类型
```

---

## 12. 文件位置参考

| 文件 | 说明 |
|-----|------|
| `Script/global.d.ts` | 全局类型声明 |
| `Script/types/CoreScripts.d.ts` | CoreScripts 模块类型 |
| `Script/Extend/prototype/ccVec.ts` | Vec2/Vec3 扩展 |
| `Script/Extend/prototype/Deserialize.ts` | 节点/Sprite 扩展 + 装饰器 |
| `Script/Extend/prototype/Symbol.ts` | Symbol 扩展 |
