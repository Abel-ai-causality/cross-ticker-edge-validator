# Cross-Ticker Edge Validator Agent

Automatically validate the reasonableness of causal edges between financial tickers using LLM, distinguishing true causal relationships from statistical noise.

> **⚡ Latest Update (2026-04-21)**: Added **Balanced Validator v2** for PuppyGraph (via OpenRouter). The new validator uses a refined prompt that produces a reasonable KEEP/MODIFY/REMOVE distribution (~33%/33%/14%) instead of the original 0%/0%/100% over-strict output. See [BALANCED_VALIDATION_REPORT.md](./BALANCED_VALIDATION_REPORT.md) for full results across 6 key tickers (NVDA, GOOGL, MSFT, TSLA, AAPL, AMZN).

## Background Problem

Causal discovery algorithms in causal graphs may produce numerous **spurious correlation** edges:
- SSTK (Shutterstock) → ETHUSD (Ethereum): How could a stock price "cause" cryptocurrency price?
- NVDA → WDCUSD: How could a GPU company "cause" Western Digital's stock price?

While these edges are statistically significant, they lack **domain logic** support. This Agent uses LLM combined with domain knowledge to automatically identify and flag suspicious edges.

---

## Two Validator Variants

| File | Graph Backend | LLM Provider | Prompt Style | Use When |
|------|---------------|--------------|--------------|----------|
| `cross_ticker_edge_validator.py` | Neo4j (Bolt) | Anthropic (direct) | Strict (mechanism-only) | Legacy Neo4j deployment |
| **`edge_validator_balanced.py`** ⭐ | **PuppyGraph (HTTP)** | **OpenRouter (DeepSeek etc.)** | **Balanced v2** | **Current production (recommended)** |

The project's graph layer migrated from Neo4j to **PuppyGraph** (HTTP API on port 443); the LLM layer moved to **OpenRouter** so we can compare DeepSeek / Qwen / Claude / etc. without SDK lock-in.

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
python cross_ticker_edge_validator.py SSTK --target ETHUSD --api-key "sk-..."
```

**Parameters:**
- `SSTK`: Source ticker (positional argument)
- `--target ETHUSD`: Target ticker
- `--api-key "..."`: Anthropic API Key

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

---

# Balanced Validator v2 (PuppyGraph + OpenRouter) ⭐

The rest of this README documents the **new** `edge_validator_balanced.py`, which is the recommended entry point for current production.

## Why Balanced v2?

Earlier iterations of the prompt were either too strict (REMOVE 100% of edges because "no direct causal mechanism") or too lenient (KEEP 100% of edges). Volume correlations between stocks are often driven by **sector co-movement, ETF flows, and macro factors** — not just direct business relationships. Balanced v2 encodes this reality.

### Verdict distribution on 120 incoming edges across 6 key tickers

| Verdict | Count | % |
|---------|-------|---|
| ✅ KEEP | 40 | 33.3% |
| ⚠️ MODIFY | 40 | 33.3% |
| ❌ REMOVE | 17 | 14.2% |
| 💥 ERROR | 18 | 15.0% |
| ❓ UNKNOWN | 5 | 4.2% |

See [BALANCED_VALIDATION_REPORT.md](./BALANCED_VALIDATION_REPORT.md) for per-ticker breakdown and edge-level judgments.

## Quick Start (Balanced v2)

### 1. Install dependencies

```bash
pip install requests
# Python 3.11+ recommended
```

### 2. Set environment variables

```bash
# OpenRouter LLM (required)
export OPENROUTER_API_KEY="sk-or-v1-..."

# PuppyGraph password (required - pick one based on env)
export PUPPYGRAPH_PROD_PASSWORD="..."    # for --env prod
export PUPPYGRAPH_SIT_PASSWORD="..."     # for --env sit

# Optional overrides
export PUPPYGRAPH_PROD_URL="https://puppygraph.abel.ai"
export PUPPYGRAPH_PROD_USER="puppygraph"
```

### 3. Run validation

```bash
# Incoming edges (what influences NVDA's volume)
python edge_validator_balanced.py NVDA \
  --field volume \
  --mode in \
  --top 20 \
  --env prod \
  --model deepseek/deepseek-chat

# Outgoing edges (what NVDA's volume influences)
python edge_validator_balanced.py NVDA \
  --field volume \
  --mode out \
  --top 20 \
  --env prod
```

Results are saved as JSON to `./validation_results/validation_{TICKER}_{FIELD}_{MODE}_{TIMESTAMP}.json`.

## Architecture (Balanced v2)

```
┌──────────────────────┐
│    PuppyGraph        │
│  (CausalNodeV3)      │
│   HTTP API :443      │
└──────────┬───────────┘
           │ Cypher via /submitCypher
           ▼
┌──────────────────────┐
│ puppygraph_client.py │  ← HTTP client (no Bolt protocol)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│ edge_validator_balanced.py   │
│  - DISTINCT edge query       │
│  - Balanced v2 prompt        │
│  - Retry (up to 3 attempts)  │
│  - Markdown-aware parser     │
└──────────┬───────────────────┘
           │ /chat/completions
           ▼
┌──────────────────────┐
│    OpenRouter        │
│ (DeepSeek / Qwen /   │
│  Claude / Nemotron)  │
└──────────────────────┘
```

## Key Design Choices

### 1. **DEFAULT TO KEEP** principle
The prompt explicitly instructs the LLM: _"When in doubt, prefer KEEP or MODIFY over REMOVE."_ This reflects that stock volumes correlate for many legitimate reasons (sector rotations, index flows) beyond direct business relationships.

### 2. Edge deduplication with `DISTINCT`
PuppyGraph's `CAUSES` relationship can have duplicates between the same node pair at different taus. The validator uses `RETURN DISTINCT source.node_name, target.node_name` to ensure each returned edge is a unique ticker pair.

### 3. Resilient parsing + retry
LLM responses occasionally return empty content or truncated output. The validator:
- Retries up to 2 times on empty/malformed responses
- Accepts markdown formats (`**Verdict:**`, `## Verdict`)
- Falls back to keyword matching if structured fields are missing
- Never crashes on `NoneType.split()` — returns `ERROR` verdict with diagnostic message

### 4. Environment-variable credentials
No secrets in code. Credentials are read from environment variables (`PUPPYGRAPH_*_PASSWORD`, `OPENROUTER_API_KEY`) — safe to commit to public repos.

## Sample Output

```
======================================================================
🎯 Balanced Edge Validator (OpenRouter)
======================================================================
Ticker: NVDA
Field: volume
Mode: in
Top: 20
Env: prod
======================================================================

📥 Found 20 incoming edges

[1/20] ADI_volume → NVDA_volume
  ✅ KEEP (90%) - Same sector (semiconductors)...
[2/20] AAPL_volume → NVDA_volume
  ✅ KEEP (85%) - Both mega-cap tech, major NVDA customer...
[3/20] RTX_volume → NVDA_volume
  ✅ KEEP (80%) - Defense industry uses NVIDIA GPUs...
...
[18/20] SON_volume → NVDA_volume
  ❌ REMOVE (85%) - Small packaging company, no connection...

======================================================================
📊 Summary Statistics
======================================================================
  ✅ KEEP:     10 (50.0%)
  ⚠️  MODIFY:   6 (30.0%)
  ❌ REMOVE:   2 (10.0%)
  💥 ERROR:    2 (10.0%)
  ────────────────
  📊 Total:   20

💾 Results saved to: ./validation_results/validation_NVDA_volume_in_20260421_122734.json
```
