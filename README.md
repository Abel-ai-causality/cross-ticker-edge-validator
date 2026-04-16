# Cross-Ticker Edge Validator Agent

验证金融 ticker 之间因果边的合理性，使用 LLM (Claude 4.6 Sonnet) 判断边是否真实因果还是统计噪声。

## 功能

- **单条边验证**: 验证两个 ticker 之间的特定边
- **批量出边验证**: 验证一个 ticker 的所有出边
- **批量入边验证**: 验证一个 ticker 的所有入边
- **上下文感知**: 提取节点邻居子图作为验证上下文

## 安装

```bash
git clone https://github.com/Abel-ai-causality/cross-ticker-edge-validator.git
cd cross-ticker-edge-validator
```

## 依赖

- Python 3.11+
- Neo4j Python Driver
- Anthropic API Key

## 使用

### 1. 单条边验证

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
export NEO4J_URI="neo4j://10.16.176.189:7687"
export NEO4J_PASSWORD="your-password"

python cross_ticker_edge_validator.py SSTK ETHUSD
```

### 2. 批量验证出边

```bash
python cross_ticker_edge_validator.py NVDA --mode out --top 10
```

### 3. 批量验证入边

```bash
python cross_ticker_edge_validator.py NVDA --mode in --top 10
```

## 输出示例

```
======================================================================
📊 NVDA 出边验证汇总
======================================================================

总计: 2 条边
  ✅ KEEP:    0 (0%)
  ❌ REMOVE:  2 (100%)
  ⚠️  MODIFY:  0 (0%)
  ❓ ERROR:   0 (0%)

🔍 建议移除的可疑边:
  ❌ NVDA_close_price -> WDCUSD_close_price (92%)
  ❌ NVDA_close_price -> MBPUSD_close_price (87%)
======================================================================
```

## 工作原理

1. 从 Neo4j 提取指定 ticker 的节点信息和边
2. 提取节点上下文（入边/出边邻居）
3. 构建 prompt，包含：
   - 源节点和目标节点的描述
   - 边的统计属性（weight, tau）
   - 节点的因果子图上下文
4. 调用 Claude 4.6 Sonnet 判断边的合理性
5. 返回 KEEP / REMOVE / MODIFY 建议

## 验证标准

Claude 基于以下标准判断：
- 行业/业务逻辑合理性
- 经济传导机制是否存在
- 统计证据 vs 虚假相关性
- 时间延迟 (tau) 是否合理

## License

MIT
