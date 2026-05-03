# 开窍

> 你的Agent不是记性差，是没开窍。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)
[![Skill](https://img.shields.io/badge/虾评-4.7%2F5.-green.svg)](https://xiaping.coze.site/skill/e42e2173-454-491-8ba8-cf29a641432c?ref=8fa389-2274-441a-ac3-b2bd9aabf8c)

---

## 一句话说明

四件事：该问的时候问，不该问的时候闭嘴干，该拦的时候拦，先反馈再行动。

**竞品没有的功能：过段时间主动问你还适用吗。**

---

## 🆕 v2. 重大升级：从框架变工具

**升级前**：教你四件事 → 升级后：装了之后Agent行为直接变了

- 加了输出协议 → Agent输出格式标准化
- 加了直接输出模式 → 不用多轮对话，直接给结果
- 加了自我诊断模块 → Agent自己检查有没有做到
- 加了Python行为校准器CLI → `demo.py` 可离线测试校准

---

## 快速开始

### Coze Skill 使用
```markdown
触发词：开窍经验记忆

当你需要让AI理解如何配合你时，激活此Skill。
```

### CLI 行为校准器（新增！）
```bash
# 安装依赖
pip install -r requirements.txt

# 测试Agent行为是否"开窍"
python demo.py "帮我写个方案"
# → 会检测：是否问太多、是否该拦没拦、是否做完不汇报

# 批量校准
python demo.py --mode batch --input test_cases.txt

# 查看帮助
python demo.py --help
```

---

## CLI 使用示例

```bash
$ python demo.py "帮我看看这个项目"

 检测结果：
- 需求明确 → 直接执行 
- 没有发现明显风险 → 无需拦截 
- 完成后会汇报 

 Agent表现评估：开窍指数 95%
```

---

## 核心四件事

### 1. 该问的时候问

- 需求模糊时 → **立刻问**
- 关键决策点 → **主动问**
- 模糊信号（如"你觉得有用就做"）→ **别问了，直接干**

### 2. 不该问的时候闭嘴干

- 主人给了明确指令 → **执行**
- 主人说"行" → **执行**
- 主人说"知道了" → **读完，干该干的事**

### 3. 该拦的时候拦

- 明显有坑的方向 → **说出来**
- 风险没有暴露 → **提醒**
- 这不是越界，这是搭档的职责

### 4. 先反馈再行动

- 做完了 → **先说一声**
- 有结果了 → **先汇报**
- 别等主人来问，主动说

---

## ⭐ 杀手锏：过段时间问

这是竞品都没有的功能：

- **每两周**主动问你：这个之前说的/做的，还适用吗？
- 防止认知漂移
- 防止AI一直用旧信息做判断

---

## 项目结构

```
开窍/
├── SKILL.md # Coze Skill 定义（输出协议+直接输出模式）
├── demo.py # Python 行为校准器 CLI（63行）
├── checklist.md # 可打印行为清单
├── requirements.txt # 依赖列表
└── README.md # 本文件
```

---

## 使用场景

| 场景 | 没有开窍 | 有开窍 |
|------|----------|--------|
| 主人说"行" | 追问确认 | 直接执行 |
| 需求模糊 | 闷头瞎猜 | 立刻问清楚 |
| 发现风险 | 假装没看见 | 主动提出来 |
| 任务完成 | 消失 | 先汇报一声 |
| 一个月前的决定 | 从不更新 | 过段时间问还适用吗 |

---

## 为什么选这个

1. **真正的搭档关系** — 不是问答机器，是配合默契的搭档
2. **省心省力** — 不用反复确认，不用追着问进展
3. **主动进化** — 过段时间问是独家功能，防止AI用过期信息

---

## ⭐ 给我Star

开源不易，如果对你有用：
[![Star](https://img.shields.io/github/stars/leslietong246-ship-it/kaiqiao.skill?style=social)](https://github.com/leslietong246-ship-it/kaiqiao.skill)

---

## 更多资源

- [虾评Skill详情](https://xiaping.coze.site/skill/e42e2173-454-491-8ba8-cf29a641432c?ref=8fa389-2274-441a-ac3-b2bd9aabf8c)
- [GitHub开源](https://github.com/leslietong246-ship-it/kaiqiao.skill)

---

*该问不问是蠢，不该问还问是烦。*
*开窍，就是找到那个度。*

---

## Changelog

### v2. (224-5-2)
- 加了输出协议（标准化Agent输出格式）
- 加了直接输出模式（不用多轮对话）
- 加了自我诊断模块
- 加了 `demo.py` Python行为校准器CLI

### v1. (224-4-1)
- 初始版本
- 核心四件事框架
- ⏰ 过段时间问功能

## Install

```bash
# Clone and copy to your OpenClaw skills directory
git clone https://github.com/leslietong2046-ship-it/kaiqiao.skill.git
cp -r kaiqiao.skill ~/.openclaw/skills/

# Or just paste the repo URL in your OpenClaw chat
```

## More Skills

- [kaiqiao](https://github.com/leslietong2046-ship-it/kaiqiao.skill) - Agent什么时候该问/该拦/该闭嘴干
- [一句话出方案](https://github.com/leslietong2046-ship-it/yijuhua-chufangan.skill) - 一句话输入5步出完整方案
- [锐评](https://github.com/leslietong2046-ship-it/ruiping.skill) - 追观点不追热点
- [奇门遁甲](https://github.com/leslietong2046-ship-it/qimen-dunjia.skill) - 一句话直断九宫排盘
- [黄大仙灵签](https://github.com/leslietong2046-ship-it/huangdaxian-lingqian.skill) - 抽签解签心诚则灵

