# StateGragh2Function
将时序逻辑电路中的状态图转换为激励方程与输出方程，并有一定验证功能。

## Feature

- [ ] CSV读取
- [ ] 真值表达式化简
- [ ] 基本交互逻辑
- [ ] 输出
- [ ] 约束校验

## Input

### 1 一份json配置文件

```json
{
    "type":"grey",
    "input":[],
    "output":[],
    "datafile":"csv data file full path"
}
```

### 2 CSV文件（状态表）