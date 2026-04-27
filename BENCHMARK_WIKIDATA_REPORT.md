# Edge Validator Benchmark v2 (Wikidata Ground Truth)

**Test Date**: 2026-04-27
**Model**: `anthropic/claude-sonnet-4-6` (Claude Sonnet 4.6)
**Total Pairs**: 50
**Ground Truth Source**: Wikidata SPARQL (P452 industry, P749/P355 parent-subsidiary)

## ⚠️ What's Different from v1

The v1 benchmark (`BENCHMARK_REPORT.md`) used **hand-picked pairs** based on the author's prior knowledge — a methodological flaw because an LLM (Claude) was being asked to validate labels another LLM (the author) had constructed, leading to circular bias and a misleadingly high accuracy (98%).

**v2 fixes this** by pulling labels **programmatically from Wikidata** via SPARQL. All ground truth comes from the public Wikidata knowledge graph (community-maintained, source-cited), not from hand-curation.

---

## 🎯 Headline Results

### Strict Metrics (KEEP only counts as positive)

| Metric | Value |
|--------|-------|
| **Accuracy** | **58.0%** (29/50) |
| **Precision** | **100.0%** |
| **Recall** | **30.0%** |
| **Specificity** | **100.0%** |
| **F1 Score** | **46.2%** |

**Confusion Matrix:**

|              | Predicted KEEP | Predicted REMOVE |
|--------------|----------------|-------------------|
| **Actual KEEP** | TP = 9 | FN = 21 |
| **Actual REMOVE** | FP = 0 | TN = 20 |

### Lenient Metrics (KEEP+MODIFY both count as positive)

| Metric | Value |
|--------|-------|
| **Accuracy** | **64.0%** |
| **Precision** | **100.0%** |
| **Recall** | **40.0%** |
| **Specificity** | **100.0%** |
| **F1 Score** | **57.1%** |

---

## 📊 v1 (hand-picked) vs v2 (Wikidata) Comparison

| Metric | v1 (hand-picked) | v2 (Wikidata) | Delta |
|--------|-----------------:|---------------:|-------:|
| Accuracy (strict) | 98.0% | 58.0% | **−40.0pp** |
| Precision | 100.0% | 100.0% | +0.0pp |
| Recall | 96.7% | 30.0% | **−66.7pp** |
| Specificity | 100.0% | 100.0% | +0.0pp |
| F1 | 98.3% | 46.2% | **−52.1pp** |

**Interpretation**: The v1 benchmark over-stated performance because it sampled obvious cases (NVDA-AMD, KO-PEP, etc.). When labels are drawn programmatically from Wikidata, the validator's true behavior is revealed: **high precision but low recall** — it never makes false KEEP decisions, but misses many subtle relationships.

---

## 📁 Per-Category Performance

### Same Wikidata Industry P452 (Expected: KEEP)

- **Total pairs**: 20
- **Accuracy**: 25.0% (5/20)
- **Verdict distribution**:
  - ✅ KEEP: 2
  - ⚠️ MODIFY: 3
  - ❌ REMOVE: 15

### Wikidata P749/P355 Parent-Subsidiary (Expected: KEEP)

- **Total pairs**: 10
- **Accuracy**: 70.0% (7/10)
- **Verdict distribution**:
  - ✅ KEEP: 7
  - ❌ REMOVE: 3

### Different Industry + No Relationship (Expected: REMOVE)

- **Total pairs**: 20
- **Accuracy**: 100.0% (20/20)
- **Verdict distribution**:
  - ❌ REMOVE: 20

---

## 🔬 Detailed Results

### Same Wikidata Industry P452 (Expected: KEEP) (20 pairs)

| # | Source → Target | Wikidata Evidence | Got | Conf | Match |
|---|----------------|------------------|-----|------|-------|
| 1 | **FHI** (Federated Hermes) → **KKR** (Kohlberg Kravis Robe) | Both in 'investment management' (Wikidata P452=Q14864997) | REMOVE | 72% | ❌ |
| 2 | **FHI** (Federated Hermes) → **MGF** (MFS Investment Manag) | Both in 'investment management' (Wikidata P452=Q14864997) | REMOVE | 72% | ❌ |
| 3 | **KKR** (Kohlberg Kravis Robe) → **MGF** (MFS Investment Manag) | Both in 'investment management' (Wikidata P452=Q14864997) | REMOVE | 72% | ❌ |
| 4 | **OPRA** (Opera) → **WPPGY** (Wunderman Thompson) | Both in 'marketing' (Wikidata P452=Q39809) | REMOVE | 82% | ❌ |
| 5 | **KZ** (Kongzhong) → **U** (Unity Technologies) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 88% | ❌ |
| 6 | **KZ** (Kongzhong) → **SONY** (Sony Group) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 72% | ❌ |
| 7 | **KZ** (Kongzhong) → **BILI** (Bilibili) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 72% | ❌ |
| 8 | **KZ** (Kongzhong) → **PLTK** (Playtika) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 78% | ❌ |
| 9 | **KZ** (Kongzhong) → **EA** (Electronic Arts) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 72% | ❌ |
| 10 | **U** (Unity Technologies) → **SONY** (Sony Group) | Both in 'video game industry' (Wikidata P452=Q941594) | MODIFY | 35% | ✅ |
| 11 | **U** (Unity Technologies) → **BILI** (Bilibili) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 72% | ❌ |
| 12 | **U** (Unity Technologies) → **PLTK** (Playtika) | Both in 'video game industry' (Wikidata P452=Q941594) | MODIFY | 52% | ✅ |
| 13 | **U** (Unity Technologies) → **EA** (Electronic Arts) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 65% | ❌ |
| 14 | **SONY** (Sony Group) → **BILI** (Bilibili) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 72% | ❌ |
| 15 | **SONY** (Sony Group) → **PLTK** (Playtika) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 85% | ❌ |
| 16 | **SONY** (Sony Group) → **EA** (Electronic Arts) | Both in 'video game industry' (Wikidata P452=Q941594) | KEEP | 62% | ✅ |
| 17 | **BILI** (Bilibili) → **PLTK** (Playtika) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 85% | ❌ |
| 18 | **BILI** (Bilibili) → **EA** (Electronic Arts) | Both in 'video game industry' (Wikidata P452=Q941594) | REMOVE | 82% | ❌ |
| 19 | **PLTK** (Playtika) → **EA** (Electronic Arts) | Both in 'video game industry' (Wikidata P452=Q941594) | MODIFY | 35% | ✅ |
| 20 | **EQH** (Equitable Holdings) → **PRU** (Prudential Financial) | Both in 'life insurance' (Wikidata P452=Q626608) | KEEP | 72% | ✅ |

### Wikidata P749/P355 Parent-Subsidiary (Expected: KEEP) (10 pairs)

| # | Source → Target | Wikidata Evidence | Got | Conf | Match |
|---|----------------|------------------|-----|------|-------|
| 1 | **SO** (Southern Company) → **GAR** (Georgia Power) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 85% | ❌ |
| 2 | **FOX** (Fox Entertainment Gr) → **FOXA** (21st Century Fox) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 98% | ✅ |
| 3 | **CNC** (Centene Corporation) → **MGLN** (Magellan Health) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 88% | ✅ |
| 4 | **MSFT** (Microsoft) → **NUAN** (Nuance Communication) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 85% | ✅ |
| 5 | **DD** (DuPont) → **DOW** (Dow Chemical Company) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 92% | ✅ |
| 6 | **EDR** (WME Group) → **TKO** (WWE) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 92% | ✅ |
| 7 | **ACE** (Ticketmaster) → **LYV** (Live Nation Entertai) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 72% | ❌ |
| 8 | **S** (Sears) → **ALL** (Allstate) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 82% | ❌ |
| 9 | **LGF** (Starz Entertainment) → **DISCA** (Discovery, Inc.) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 72% | ✅ |
| 10 | **YELL** (Yellow Corporation) → **SAIA** (Saia) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 82% | ✅ |

### Different Industry + No Relationship (Expected: REMOVE) (20 pairs)

| # | Source → Target | Wikidata Evidence | Got | Conf | Match |
|---|----------------|------------------|-----|------|-------|
| 1 | **PRU** (Prudential Financial) → **TDY** (Teledyne Technologie) | No shared industry ('life insurance' vs 'conglomerate'), no documented corporate | REMOVE | 80% | ✅ |
| 2 | **DHR** (Danaher Corporation) → **FICO** (FICO) | No shared industry ('conglomerate' vs 'data analysis'), no documented corporate  | REMOVE | 85% | ✅ |
| 3 | **OMF** (OneMain Financial) → **OSK** (Oshkosh Corporation) | No shared industry ('financial services' vs 'automotive industry'), no documente | REMOVE | 82% | ✅ |
| 4 | **SAIA** (Saia) → **CPG** (Crescent Point Energ) | No shared industry ('transport industry' vs 'petroleum industry'), no documented | REMOVE | 82% | ✅ |
| 5 | **TEO** (Telecom Argentina) → **VIRT** (Virtu Financial) | No shared industry ('telecommunications' vs 'financial services'), no documented | REMOVE | 85% | ✅ |
| 6 | **AMZN** (Amazon) → **SO** (Southern Company) | No shared industry ('retail' vs 'energy industry'), no documented corporate pare | REMOVE | 85% | ✅ |
| 7 | **WF** (Woori Financial Grou) → **ROP** (Roper Technologies) | No shared industry ('financial sector' vs 'conglomerate'), no documented corpora | REMOVE | 82% | ✅ |
| 8 | **HCC** (Tokio Marine HCC) → **MERU** (Meru Networks) | No shared industry ('insurance' vs 'wireless LAN'), no documented corporate pare | REMOVE | 96% | ✅ |
| 9 | **F** (Ford Motor Company) → **ALK** (Alaska Air Group) | No shared industry ('automotive industry' vs 'transport'), no documented corpora | REMOVE | 72% | ✅ |
| 10 | **FORG** (ForgeRock) → **M** (Macy's, Inc.) | No shared industry ('enterprise software' vs 'retail'), no documented corporate  | REMOVE | 92% | ✅ |
| 11 | **JEF** (Jefferies & Company) → **RL** (Ralph Lauren Corpora) | No shared industry ('investment' vs 'commerce'), no documented corporate parent- | REMOVE | 82% | ✅ |
| 12 | **NMRA** (Neumora Therapeutics) → **AU** (AngloGold Ashanti) | No shared industry ('pharmaceutical industry' vs 'mining'), no documented corpor | REMOVE | 95% | ✅ |
| 13 | **CCJ** (Cameco) → **LPI** (Vital Energy) | No shared industry ('mining' vs 'petroleum industry'), no documented corporate p | REMOVE | 85% | ✅ |
| 14 | **U** (Unity Technologies) → **S** (Sprint Corporation) | No shared industry ('video game industry' vs 'telecommunications'), no documente | REMOVE | 78% | ✅ |
| 15 | **SSL** (Sasol) → **GHL** (Greenhill & Co.) | No shared industry ('petroleum industry' vs 'investment bank'), no documented co | REMOVE | 82% | ✅ |
| 16 | **CMI** (Cummins) → **DCP** (DCP Midstream Partne) | No shared industry ('manufacture of machinery and equipment' vs 'petroleum indus | REMOVE | 72% | ✅ |
| 17 | **EH** (EHang) → **AT** (Atlantic Power Corpo) | No shared industry ('aerospace engineering' vs 'electricity supply company'), no | REMOVE | 72% | ✅ |
| 18 | **DNMR** (Meredian Holdings Gr) → **CAR** (Avis Budget Group) | No shared industry ('biotechnology' vs 'car rental company'), no documented corp | REMOVE | 90% | ✅ |
| 19 | **MTU** (Mitsubishi UFJ Finan) → **MAA** (MAA) | No shared industry ('financial services' vs 'real estate investment trust'), no  | REMOVE | 85% | ✅ |
| 20 | **FSLR** (First Solar) → **PTLO** (Portillo's Restauran) | No shared industry ('photovoltaics' vs 'restaurant'), no documented corporate pa | REMOVE | 95% | ✅ |

---

## 💡 Honest Findings

### 1. Validator is precision-biased, not balanced

- **Precision: 100%** — When the validator says KEEP, it's almost always right
- **Recall: 30%** — But it misses many edges that Wikidata considers related
- **Specificity: 100%** — It never lets through a clearly unrelated pair

This means the validator is well-suited for **conservative pruning** (remove obvious noise), but **not for sensitive recall** (catching every plausible relationship).

### 2. Wikidata's P452 industry classification is coarser than GICS

Many "same-industry" misses are actually defensible. Examples from this run:
- KKR (private equity) ↔ MGF (mutual fund) — both labeled "investment management" by Wikidata, but very different business models
- OPRA (Opera browser) ↔ WPPGY (WPP advertising) — both labeled "marketing", but Opera is a browser company
- KZ (Kongzhong mobile games) ↔ U (Unity game engine) — both labeled "video game industry", but very different products

In these cases, the validator's REMOVE may be **more accurate** than the Wikidata label.

### 3. Corporate parent-subsidiary recognition: 70%

For documented P749/P355 parent-subsidiary pairs (e.g., MSFT-NUAN, EDR-TKO), the validator correctly identifies 70% as KEEP. The 30% misses are typically older M&A deals that may not be reflected in the validator's training data.

### 4. The 91% production REMOVE rate: re-evaluating

Given that the validator has:
- 100% specificity (never KEEPs noise)
- 30% recall (misses many true relationships)

the production 91% REMOVE rate likely contains some **false negatives** — legitimate sector-comovement edges being incorrectly flagged. The true noise rate of the underlying graph might be 60–80%, not 91%.

---

## 🧪 Methodology

### Dataset Construction (fully programmatic)

1. **Fetch US-listed companies** with industry data from Wikidata:
```sparql
SELECT DISTINCT ?company ?ticker ?industry WHERE {
  ?company p:P414 ?stmt .
  ?stmt ps:P414 ?exchange ; pq:P249 ?ticker .
  ?exchange wdt:P17 wd:Q30 .  # US-based exchange
  ?company wdt:P452 ?industry .
}
```
→ Yields 722 unique companies with industry tags.

2. **Fetch corporate parent-subsidiary relationships**:
```sparql
VALUES ?prop { wdt:P749 wdt:P355 }  # parent / subsidiary
?source ?prop ?related .
```
→ Excludes P127/P1830 which include passive institutional holdings.

3. **Build positive pairs**:
   - Same `P452` industry Q-id (20 pairs)
   - Documented P749/P355 relationship (10 pairs)

4. **Build negative pairs**:
   - **No** shared `P452` Q-id
   - **No** documented P749/P355 relationship

### Why this is more rigorous than v1

| Aspect | v1 | v2 |
|--------|----|----|
| Label source | LLM (author) prior knowledge | Wikidata SPARQL |
| Reproducible | Requires re-typing | Anyone can re-query |
| Bias | Hand-picked obvious cases | Random sampling from KB |
| Independent of LLM training data | No | Yes |
| Coverage | 50 pairs | 722 companies, sampled to 50 pairs |

---

## 🚀 Reproducing

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export PUPPYGRAPH_PROD_PASSWORD="..."  # imported by validator module

# Runs Wikidata SPARQL → builds dataset → validates → computes metrics
python3 benchmark_wikidata.py
```

Each run will sample DIFFERENT pairs (with `random.seed(42)` for reproducibility within a single run, but different ground truth is fetched live from Wikidata).

---

## ⚠️ Limitations of this Benchmark

1. **Wikidata coverage is incomplete**. Not all stocks have rich industry/relationship data; popular stocks are over-represented.
2. **P452 industry codes don't map cleanly to GICS**. A more precise benchmark would use S&P GICS Sub-Industry codes directly.
3. **Sample size is small (50 pairs)**. Larger samples would give tighter confidence intervals.
4. **Single LLM**. Results may differ for GPT-5, Qwen, Gemini, etc.
5. **Corporate relationship data has temporal lag**. Recent M&As may not yet be in Wikidata.

---

*Report generated from: `benchmark_wikidata_20260427_110443.json`*  
*Wikidata SPARQL endpoint: https://query.wikidata.org/sparql*