# Cross-Ticker Edge Validator Agent

Automatically validate the reasonableness of causal edges between financial tickers using LLM (Claude 4.6 Sonnet), distinguishing true causal relationships from statistical noise.

## Background Problem

Causal discovery algorithms in causal graphs may produce numerous **spurious correlation** edges:
- SSTK (Shutterstock) → ETHUSD (Ethereum): How could a stock price "cause" cryptocurrency price?
- NVDA → WDCUSD: How could a GPU company "cause" Western Digital's stock price?

While these edges are statistically significant, they lack **domain logic** support. This Agent uses LLM combined with domain knowledge to automatically identify and flag suspicious edges.

---

## Features

### 1. Single Edge Validation
Validate whether an edge between two specific tickers exists and is reasonable.

### 2. Batch Outgoing Edge Validation
Check which other tickers a given ticker "influences" and identify anomalous outgoing relationships.

### 3. Batch Incoming Edge Validation
Check which factors influence the given ticker and identify anomalous incoming relationships.

### 4. Context-Aware Validation
Not only validates the edge itself but also extracts the node's causal subgraph as judgment context.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Accessible Neo4j instance (with CausalNodeV2 data)
- Anthropic API Key (Claude 4.6 Sonnet)

### Installation

```bash
# Clone the repository
git clone https://github.com/Abel-ai-causality/cross-ticker-edge-validator.git
cd cross-ticker-edge-validator

# Install dependencies (using abel-triple-fusion environment)
cd /path/to/abel-triple-fusion
uv add neo4j requests
```

### Environment Configuration

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."  # Your Claude API Key
```

Or specify temporarily using the `--api-key` parameter.

---

## Usage Guide

### Mode 1: Validate Single Edge

Check if an edge exists between two tickers and whether it is reasonable.

```bash
python cross_ticker_edge_validator.py SSTK ETHUSD --api-key "sk-..."
```

**Output Example:**
```
🔎 Validating edge: SSTK -> ETHUSD
🔍 Finding nodes: SSTK_close_price and ETHUSD_close_price
✅ Found nodes: SSTK_close_price <-> ETHUSD_close_price
✅ Found edge: SSTK_close_price -[CAUSES]-> ETHUSD_close_price (tau=17, weight=0.3655)
📊 Extracting node context...
🤖 Calling Claude for validation...

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

### Mode 2: Batch Outgoing Edge Validation

Validate all outgoing edges of a ticker (which other tickers it "influences").

```bash
python cross_ticker_edge_validator.py NVDA --mode out --top 10
```

**Output Example:**
```
🔎 Batch validating NVDA outgoing edges (Top 10)
📤 NVDA outgoing edges (Top 2):
  1. NVDA_close_price -> WDCUSD_close_price (tau=84, weight=-0.0036)
  2. NVDA_close_price -> MBPUSD_close_price (tau=35, weight=0.0077)

Starting validation of top 2 edges...

[1/2] Validating: NVDA_close_price -> WDCUSD_close_price
  ❌ REMOVE (confidence: 92%)
[2/2] Validating: NVDA_close_price -> MBPUSD_close_price
  ❌ REMOVE (confidence: 87%)

======================================================================
📊 NVDA Outgoing Edges Validation Summary
======================================================================

Total: 2 edges
  ✅ KEEP:    0 (0%)
  ❌ REMOVE:  2 (100%)
  ⚠️  MODIFY:  0 (0%)
  ❓ ERROR:   0 (0%)

🔍 Recommended suspicious edges to remove:
  ❌ NVDA_close_price          -> WDCUSD_close_price        (92%)
  ❌ NVDA_close_price          -> MBPUSD_close_price        (87%)
======================================================================
```

### Mode 3: Batch Incoming Edge Validation

Check which factors influence this ticker.

```bash
python cross_ticker_edge_validator.py NVDA --mode in --top 10
```

---

## How It Works

### Data Flow

```
┌─────────────────┐
│   Neo4j Graph   │
│  (CausalNodeV2) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ 1. Extract node pairs   │
│    and edge properties  │
│    - source/target      │
│    - weight, tau        │
│    - neighbor subgraph  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 2. Build LLM Prompt     │
│    - Node descriptions  │
│    - Edge statistics    │
│    - Causal context     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 3. Claude 4.6 Validation│
│    - Domain knowledge   │
│    - Business logic     │
│    - Stats vs Causal    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 4. Output Results       │
│    - KEEP/REMOVE/MODIFY │
│    - Confidence score   │
│    - Reasoning          │
└─────────────────────────┘
```

### Validation Dimensions

Claude judges edge reasonableness based on the following dimensions:

| Dimension | Description |
|-----------|-------------|
| **Industry Connection** | Do the two tickers' industries have business relations? |
| **Economic Transmission** | Is there a credible price/supply transmission mechanism? |
| **Scale Comparison** | Is the market cap difference too large? (e.g., $0.6B vs $300B+) |
| **Time Lag** | Does tau (days) make business sense? |
| **Statistical Anomaly** | Is weight significantly higher than similar edges? |
| **Subgraph Consistency** | Do the nodes' other edges support this causal relationship? |

---

## Configuration

### Neo4j Configuration

Defaults are read from `abel-triple-fusion/config.local.yaml`:

```yaml
neo4j:
  uri: "neo4j://10.16.176.189:7687"
  username: "neo4j"
  password: "your-password"
  dbname: "neo4j"
```

To customize, modify the `CrossTickerEdgeValidator` initialization parameters in the code.

### LLM Configuration

Currently uses **Claude 4.6 Sonnet**:
- Model: `claude-sonnet-4-6`
- Temperature: 0.2 (low randomness, deterministic output)
- Max Tokens: 1500-2000

---

## Output Interpretation

### Action Types

| Type | Meaning | Recommendation |
|------|---------|----------------|
| **KEEP** | Edge represents true causal relationship | Keep in graph |
| **REMOVE** | Edge is spurious correlation, no logical basis | Delete from graph |
| **MODIFY** | Edge has some validity but wrong direction/type | Modify edge properties |
| **ERROR** | Error during validation | Check logs |

### Confidence Score

- **> 90%**: High confidence, can be auto-processed
- **70-90%**: Medium confidence, suggest manual review
- **< 70%**: Low confidence, needs more context

---

## Real-World Cases

### Case 1: SSTK → ETHUSD (REMOVE, 92%)

**Problem:** How could Shutterstock's stock price "cause" ETH price?

**Claude Analysis:**
- Shutterstock ($0.64B) vs Ethereum ($300B+), scale differs by orders of magnitude
- Completely unrelated businesses (stock images vs cryptocurrency)
- 17-day delay has no reasonable explanation
- weight=0.3655 is anomalously high (other edges in graph mostly 0.01-0.08)

**Conclusion:** Statistical spurious correlation, should be deleted.

### Case 2: NVDA → WDCUSD (REMOVE, 92%)

**Problem:** How could NVIDIA "cause" Western Digital's stock price?

**Claude Analysis:**
- While both are in tech industry, direct causal relationship is weak
- 84-day delay is too long, no clear transmission mechanism
- Weight is low (-0.0036), weak signal

**Conclusion:** Spurious correlation, should be deleted.

---

## Future Roadmap

### Planned Features

- [ ] **Batch Scanning Mode**: Auto-detect all suspicious edges in graph
- [ ] **Path Validation**: Check indirect causal chains (A→B→C)
- [ ] **Community Validation**: Validate entire sector subgraphs
- [ ] **Historical Comparison**: Compare edge changes across time periods
- [ ] **Visualization Output**: Generate chart reports of suspicious edges

---

## Contributing

Welcome PRs to extend functionality:

1. Fork this repository
2. Create a feature branch
3. Submit changes
4. Create Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Contact

- **Organization**: [Abel-ai-causality](https://github.com/Abel-ai-causality)
- **Repository**: [cross-ticker-edge-validator](https://github.com/Abel-ai-causality/cross-ticker-edge-validator)

---

## Related Projects

- [abel-triple-fusion](https://github.com/Abel-ai-causality/abel-triple-fusion) - Causal graph construction and validation framework
- [Abel-skills](https://github.com/Abel-ai-causality/Abel-skills) - Abel AI Skills Collection
