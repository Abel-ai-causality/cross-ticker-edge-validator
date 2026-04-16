# Cross-Ticker Edge Validator Agent

使用 LLM (Claude 4.6 Sonnet) 自动验证金融 ticker 之间因果边的合理性，区分真实因果关系与统计噪声。

## 背景问题

在因果图（Causal Graph）中，因果发现算法可能产生大量**虚假相关**的边：
- SSTK (Shutterstock) → ETHUSD (Ethereum)：股价如何"导致"加密货币价格？
- NVDA → WDCUSD：显卡公司如何"导致"西部数据股价？

这些边虽然统计显著，但缺乏**领域逻辑**支撑。本 Agent 使用 LLM 结合领域知识自动识别并标记可疑边。

---

## 功能特性

### 1. 单条边验证
验证两个特定 ticker 之间的边是否存在且合理。

### 2. 批量出边验证
检查一个 ticker 影响哪些其他 ticker，识别异常传出关系。

### 3. 批量入边验证
检查哪些因素影响该 ticker，识别异常传入关系。

### 4. 上下文感知验证
不仅验证边本身，还提取节点的因果子图作为判断上下文。

---

## 快速开始

### 前提条件

- Python 3.11+
- 可访问的 Neo4j 实例（包含 CausalNodeV2 数据）
- Anthropic API Key（Claude 4.6 Sonnet）

### 安装

```bash
# 克隆仓库
git clone https://github.com/Abel-ai-causality/cross-ticker-edge-validator.git
cd cross-ticker-edge-validator

# 安装依赖（使用abel-triple-fusion的环境）
cd /path/to/abel-triple-fusion
uv add neo4j requests
```

### 配置环境变量

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."  # 你的Claude API Key
```

或使用 `--api-key` 参数临时指定。

---

## 使用指南

### 模式一：验证单条边

检查两个 ticker 之间是否存在边，以及该边是否合理。

```bash
python cross_ticker_edge_validator.py SSTK ETHUSD --api-key "sk-..."
```

**输出示例：**
```
🔎 验证边: SSTK -> ETHUSD
🔍 查找节点: SSTK_close_price 和 ETHUSD_close_price
✅ 找到节点: SSTK_close_price <-> ETHUSD_close_price
✅ 找到边: SSTK_close_price -[CAUSES]-> ETHUSD_close_price (tau=17, weight=0.3655)
📊 提取节点上下文...
🤖 调用 Claude 进行验证...

============================================================
🎯 EDGE VALIDATION RESULT
============================================================
Source:      SSTK_close_price
Target:      ETHUSD_close_price
Relation:    CAUSES
Action:      REMOVE
Confidence:  92.00%

Reason:
There is no logical causal mechanism by which Shutterstock's 
stock price would cause Ethereum's price to move 17 days later...

Suggestions:
No modification warranted — this edge should be removed entirely.
============================================================
```

### 模式二：批量验证出边

验证某 ticker 的所有出边（它"影响"哪些其他 ticker）。

```bash
python cross_ticker_edge_validator.py NVDA --mode out --top 10
```

**输出示例：**
```
🔎 批量验证 NVDA 的 出边 (Top 10)
📤 NVDA 的出边（Top 2）:
  1. NVDA_close_price -> WDCUSD_close_price (tau=84, weight=-0.0036)
  2. NVDA_close_price -> MBPUSD_close_price (tau=35, weight=0.0077)

开始验证前 2 条边...

[1/2] 验证: NVDA_close_price -> WDCUSD_close_price
  ❌ REMOVE (confidence: 92%)
[2/2] 验证: NVDA_close_price -> MBPUSD_close_price
  ❌ REMOVE (confidence: 87%)

======================================================================
📊 NVDA 出边验证汇总
======================================================================

总计: 2 条边
  ✅ KEEP:    0 (0%)
  ❌ REMOVE:  2 (100%)
  ⚠️  MODIFY:  0 (0%)
  ❓ ERROR:   0 (0%)

🔍 建议移除的可疑边:
  ❌ NVDA_close_price          -> WDCUSD_close_price        (92%)
  ❌ NVDA_close_price          -> MBPUSD_close_price        (87%)
======================================================================
```

### 模式三：批量验证入边

验证哪些因素影响该 ticker。

```bash
python cross_ticker_edge_validator.py NVDA --mode in --top 10
```

---

## 工作原理

### 数据流

```
┌─────────────────┐
│   Neo4j 图数据库  │
│  (CausalNodeV2) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  1. 提取节点对和边属性    │
│    - source/target 节点   │
│    - weight, tau         │
│    - 邻居子图 (入边/出边) │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  2. 构建 LLM Prompt      │
│    - 节点描述            │
│    - 边的统计属性        │
│    - 因果子图上下文      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  3. Claude 4.6 验证      │
│    - 领域知识判断        │
│    - 业务逻辑推理        │
│    - 统计 vs 因果区分     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  4. 输出验证结果         │
│    - KEEP/REMOVE/MODIFY  │
│    - 置信度评分          │
│    - 理由说明            │
└─────────────────────────┘
```

### 验证维度

Claude 基于以下维度判断边的合理性：

| 维度 | 说明 |
|------|------|
| **行业关联** | 两个 ticker 所属行业是否有业务往来？ |
| **经济传导** | 是否存在可信的价格/供需传导机制？ |
| **规模对比** | 市值差异是否过大？（如 $0.6B vs $300B+）|
| **时间延迟** | tau（天数）是否符合业务逻辑？ |
| **统计异常** | weight 是否远高于同类边？ |
| **子图一致性** | 节点的其他边是否支持该因果关系？ |

---

## 配置说明

### Neo4j 配置

默认从 `abel-triple-fusion/config.local.yaml` 读取：

```yaml
neo4j:
  uri: "neo4j://10.16.176.189:7687"
  username: "neo4j"
  password: "your-password"
  dbname: "neo4j"
```

如需自定义，修改代码中的 `CrossTickerEdgeValidator` 初始化参数。

### LLM 配置

当前使用 **Claude 4.6 Sonnet**：
- 模型：`claude-sonnet-4-6`
- 温度：0.2（低随机性，确定性输出）
- Max Tokens：1500-2000

---

## 输出解读

### Action 类型

| 类型 | 含义 | 处理建议 |
|------|------|---------|
| **KEEP** | 边代表真实因果关系 | 保留在图中 |
| **REMOVE** | 边是虚假相关，无逻辑基础 | 从图中删除 |
| **MODIFY** | 边有一定合理性但方向/类型错误 | 修改边属性 |
| **ERROR** | 验证过程中出错 | 检查日志 |

### Confidence 置信度

- **> 90%**: 高置信度，可自动处理
- **70-90%**: 中等置信度，建议人工复核
- **< 70%**: 低置信度，需要更多上下文

---

## 实际案例

### 案例 1：SSTK → ETHUSD（REMOVE，92%）

**问题：** Shutterstock 股价如何"导致"ETH 价格？

**Claude 分析：**
- Shutterstock ($0.64B) vs Ethereum ($300B+)，规模相差数个数量级
- 业务完全不相关（图片素材 vs 加密货币）
- 17天延迟无合理解释
- weight=0.3655 异常高（图中其他边多在 0.01-0.08）

**结论：** 统计伪相关，应删除。

### 案例 2：NVDA → WDCUSD（REMOVE，92%）

**问题：** 英伟达如何"导致"西部数据股价？

**Claude 分析：**
- 虽然同属科技行业，但直接因果关系薄弱
- 84天延迟过长，无明确传导机制
- 权重偏低 (-0.0036)，信号弱

**结论：** 虚假相关，应删除。

---

## 扩展计划

### 未来功能

- [ ] **批量筛查模式**：自动检测图中所有可疑边
- [ ] **路径验证**：检查间接因果链（A→B→C）
- [ ] **社区验证**：验证整个 sector 子图
- [ ] **历史对比**：对比不同时间段的边变化
- [ ] **可视化输出**：生成可疑边的图表报告

---

## 贡献指南

欢迎提交 PR 扩展功能：

1. Fork 本仓库
2. 创建 feature 分支
3. 提交变更
4. 创建 Pull Request

---

## License

MIT License - 详见 [LICENSE](LICENSE)

---

## 联系方式

- **组织**: [Abel-ai-causality](https://github.com/Abel-ai-causality)
- **仓库**: [cross-ticker-edge-validator](https://github.com/Abel-ai-causality/cross-ticker-edge-validator)

---

## 相关项目

- [abel-triple-fusion](https://github.com/Abel-ai-causality/abel-triple-fusion) - 因果图构建与验证框架
- [Abel-skills](https://github.com/Abel-ai-causality/Abel-skills) - Abel AI Skills 集合
