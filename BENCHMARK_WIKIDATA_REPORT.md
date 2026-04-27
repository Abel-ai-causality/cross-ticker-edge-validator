# Edge Validator Benchmark v2 (Wikidata Ground Truth)

**Test Date**: 2026-04-27
**Model**: `anthropic/claude-sonnet-4-6` (Claude Sonnet 4.6)
**Total Pairs**: 409
**Ground Truth Source**: Wikidata SPARQL (P452 industry, P749/P355 parent-subsidiary)

## ⚠️ What's Different from v1

The v1 benchmark (`BENCHMARK_REPORT.md`) used **hand-picked pairs** based on the author's prior knowledge — a methodological flaw because an LLM (Claude) was being asked to validate labels another LLM (the author) had constructed, leading to circular bias and a misleadingly high accuracy (98%).

**v2 fixes this** by pulling labels **programmatically from Wikidata** via SPARQL. All ground truth comes from the public Wikidata knowledge graph (community-maintained, source-cited), not from hand-curation.

---

## 🎯 Headline Results

### Strict Metrics (KEEP only counts as positive)

| Metric | Value |
|--------|-------|
| **Accuracy** | **57.9%** (237/409) |
| **Precision** | **100.0%** |
| **Recall** | **17.7%** |
| **Specificity** | **100.0%** |
| **F1 Score** | **30.1%** |

**Confusion Matrix:**

|              | Predicted KEEP | Predicted REMOVE |
|--------------|----------------|-------------------|
| **Actual KEEP** | TP = 37 | FN = 172 |
| **Actual REMOVE** | FP = 0 | TN = 200 |

### Lenient Metrics (KEEP+MODIFY both count as positive)

| Metric | Value |
|--------|-------|
| **Accuracy** | **65.5%** |
| **Precision** | **91.5%** |
| **Recall** | **35.9%** |
| **Specificity** | **96.5%** |
| **F1 Score** | **51.5%** |

---

## 📊 v1 (hand-picked) vs v2 (Wikidata) Comparison

| Metric | v1 (hand-picked) | v2 (Wikidata) | Delta |
|--------|-----------------:|---------------:|-------:|
| Accuracy (strict) | 98.0% | 57.9% | **−40.1pp** |
| Precision | 100.0% | 100.0% | +0.0pp |
| Recall | 96.7% | 17.7% | **−79.0pp** |
| Specificity | 100.0% | 100.0% | +0.0pp |
| F1 | 98.3% | 30.1% | **−68.2pp** |

**Interpretation**: The v1 benchmark over-stated performance because it sampled obvious cases (NVDA-AMD, KO-PEP, etc.). When labels are drawn programmatically from Wikidata, the validator's true behavior is revealed: **high precision but low recall** — it never makes false KEEP decisions, but misses many subtle relationships.

---

## 📁 Per-Category Performance

### Same Wikidata Industry P452 (Expected: KEEP)

- **Total pairs**: 200
- **Accuracy**: 35.0% (70/200)
- **Verdict distribution**:
  - ✅ KEEP: 33
  - ⚠️ MODIFY: 37
  - ❌ REMOVE: 130

### Wikidata P749/P355 Parent-Subsidiary (Expected: KEEP)

- **Total pairs**: 9
- **Accuracy**: 55.6% (5/9)
- **Verdict distribution**:
  - ✅ KEEP: 4
  - ⚠️ MODIFY: 1
  - ❌ REMOVE: 4

### Different Industry + No Relationship (Expected: REMOVE)

- **Total pairs**: 200
- **Accuracy**: 96.5% (193/200)
- **Verdict distribution**:
  - ⚠️ MODIFY: 7
  - ❌ REMOVE: 193

---

## 🔬 Detailed Results

### Same Wikidata Industry P452 (Expected: KEEP) (200 pairs)

| # | Source → Target | Wikidata Evidence | Got | Conf | Match |
|---|----------------|------------------|-----|------|-------|
| 1 | **pam** (Pampa Energía) → **POM** (Pepco Holdings, Inc.) | Both in 'energy supply' (Wikidata P452=Q1341477) | REMOVE | 72% | ❌ |
| 2 | **LAZ** (Lazard) → **TROW** (T. Rowe Price) | Both in 'asset management' (Wikidata P452=Q873442) | KEEP | 72% | ✅ |
| 3 | **LAZ** (Lazard) → **KKR** (Kohlberg Kravis Robe) | Both in 'asset management' (Wikidata P452=Q873442) | KEEP | 65% | ✅ |
| 4 | **LAZ** (Lazard) → **BLK** (BlackRock) | Both in 'asset management' (Wikidata P452=Q873442) | KEEP | 72% | ✅ |
| 5 | **TROW** (T. Rowe Price) → **KKR** (Kohlberg Kravis Robe) | Both in 'asset management' (Wikidata P452=Q873442) | MODIFY | 45% | ✅ |
| 6 | **TROW** (T. Rowe Price) → **BLK** (BlackRock) | Both in 'asset management' (Wikidata P452=Q873442) | KEEP | 78% | ✅ |
| 7 | **KKR** (Kohlberg Kravis Robe) → **BLK** (BlackRock) | Both in 'asset management' (Wikidata P452=Q873442) | KEEP | 72% | ✅ |
| 8 | **BOH** (Bank of Hawaii) → **WF** (Woori Financial Grou) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 82% | ❌ |
| 9 | **BOH** (Bank of Hawaii) → **LC** (Lending Club) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 80% | ❌ |
| 10 | **BOH** (Bank of Hawaii) → **SF** (Stifel) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 72% | ❌ |
| 11 | **BOH** (Bank of Hawaii) → **MBI** (MBIA) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 82% | ❌ |
| 12 | **BOH** (Bank of Hawaii) → **CME** (CME Group) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 85% | ❌ |
| 13 | **BOH** (Bank of Hawaii) → **CACC** (Credit Acceptance) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 85% | ❌ |
| 14 | **WF** (Woori Financial Grou) → **LC** (Lending Club) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 55% | ✅ |
| 15 | **WF** (Woori Financial Grou) → **SF** (Stifel) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 42% | ✅ |
| 16 | **WF** (Woori Financial Grou) → **MBI** (MBIA) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 65% | ❌ |
| 17 | **WF** (Woori Financial Grou) → **CME** (CME Group) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 52% | ✅ |
| 18 | **WF** (Woori Financial Grou) → **CACC** (Credit Acceptance) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 35% | ✅ |
| 19 | **LC** (Lending Club) → **SF** (Stifel) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 72% | ❌ |
| 20 | **LC** (Lending Club) → **MBI** (MBIA) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 72% | ❌ |
| 21 | **LC** (Lending Club) → **CME** (CME Group) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 78% | ❌ |
| 22 | **LC** (Lending Club) → **CACC** (Credit Acceptance) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 42% | ✅ |
| 23 | **SF** (Stifel) → **MBI** (MBIA) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 42% | ✅ |
| 24 | **SF** (Stifel) → **CME** (CME Group) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 72% | ❌ |
| 25 | **SF** (Stifel) → **CACC** (Credit Acceptance) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 78% | ❌ |
| 26 | **MBI** (MBIA) → **CME** (CME Group) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 72% | ❌ |
| 27 | **MBI** (MBIA) → **CACC** (Credit Acceptance) | Both in 'finance' (Wikidata P452=Q43015) | MODIFY | 35% | ✅ |
| 28 | **CME** (CME Group) → **CACC** (Credit Acceptance) | Both in 'finance' (Wikidata P452=Q43015) | REMOVE | 82% | ❌ |
| 29 | **IBM** (IBM) → **SNX** (TD SYNNEX) | Both in 'IT service management' (Wikidata P452=Q1481411) | KEEP | 62% | ✅ |
| 30 | **IBM** (IBM) → **EDS** (Hewlett Packard Ente) | Both in 'IT service management' (Wikidata P452=Q1481411) | KEEP | 78% | ✅ |
| 31 | **SNX** (TD SYNNEX) → **EDS** (Hewlett Packard Ente) | Both in 'IT service management' (Wikidata P452=Q1481411) | REMOVE | 65% | ❌ |
| 32 | **J** (Jacobs Engineering G) → **FCN** (FTI Consulting) | Both in 'professional services industry' (Wikidata P452=Q23700345) | REMOVE | 72% | ❌ |
| 33 | **J** (Jacobs Engineering G) → **CACI** (CACI) | Both in 'professional services industry' (Wikidata P452=Q23700345) | MODIFY | 55% | ✅ |
| 34 | **J** (Jacobs Engineering G) → **ACN** (Accenture) | Both in 'professional services industry' (Wikidata P452=Q23700345) | MODIFY | 45% | ✅ |
| 35 | **FCN** (FTI Consulting) → **CACI** (CACI) | Both in 'professional services industry' (Wikidata P452=Q23700345) | KEEP | 72% | ✅ |
| 36 | **FCN** (FTI Consulting) → **ACN** (Accenture) | Both in 'professional services industry' (Wikidata P452=Q23700345) | KEEP | 72% | ✅ |
| 37 | **CACI** (CACI) → **ACN** (Accenture) | Both in 'professional services industry' (Wikidata P452=Q23700345) | KEEP | 62% | ✅ |
| 38 | **PM** (Philip Morris Intern) → **MO** (Altria) | Both in 'tobacco industry' (Wikidata P452=Q907703) | KEEP | 92% | ✅ |
| 39 | **PM** (Philip Morris Intern) → **BTI** (British American Tob) | Both in 'tobacco industry' (Wikidata P452=Q907703) | KEEP | 82% | ✅ |
| 40 | **MO** (Altria) → **BTI** (British American Tob) | Both in 'tobacco industry' (Wikidata P452=Q907703) | KEEP | 82% | ✅ |
| 41 | **WTW** (Willis Towers Watson) → **WSH** (Willis Group) | Both in 'insurance broker' (Wikidata P452=Q285759) | REMOVE | 72% | ❌ |
| 42 | **MA** (Mastercard) → **WU** (Western Union) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 43 | **MA** (Mastercard) → **IX** (Orix) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 78% | ❌ |
| 44 | **MA** (Mastercard) → **V** (Visa Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 92% | ✅ |
| 45 | **MA** (Mastercard) → **ENV** (Envestnet) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 46 | **MA** (Mastercard) → **C** (Citigroup) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 47 | **MA** (Mastercard) → **AIG** (American Internation) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 48 | **MA** (Mastercard) → **WBK** (Westpac) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 49 | **MA** (Mastercard) → **SSB** (SouthState Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 50 | **MA** (Mastercard) → **BEN** (Franklin Templeton I) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 80% | ❌ |
| 51 | **MA** (Mastercard) → **DB** (Deutsche Bank) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 52 | **MA** (Mastercard) → **HDB** (HDFC Bank) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 53 | **MA** (Mastercard) → **AAVMY** (ABN AMRO) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 54 | **MA** (Mastercard) → **CBU** (Community Bank, N.A.) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 55 | **MA** (Mastercard) → **HSBC** (HSBC) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 62% | ✅ |
| 56 | **MA** (Mastercard) → **NU** (Nubank) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 40% | ✅ |
| 57 | **MA** (Mastercard) → **BSAC** (Banco Santander-Chil) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 58 | **MA** (Mastercard) → **MTB** (M&T Bank) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 59 | **MA** (Mastercard) → **ADS** (Alliance Data) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 45% | ✅ |
| 60 | **MA** (Mastercard) → **MS** (Morgan Stanley) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 45% | ✅ |
| 61 | **MA** (Mastercard) → **SHG** (Shinhan Financial Gr) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 62 | **MA** (Mastercard) → **PIPR** (Piper Sandler Compan) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 63 | **MA** (Mastercard) → **AL** (Air Lease) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 64 | **MA** (Mastercard) → **FINN** (First National of Ne) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 65 | **MA** (Mastercard) → **EV** (Eaton Vance) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 78% | ❌ |
| 66 | **MA** (Mastercard) → **TD** (Toronto-Dominion Ban) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 67 | **MA** (Mastercard) → **RE** (Everest Re) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 68 | **MA** (Mastercard) → **TCBK** (Tri Counties Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 69 | **MA** (Mastercard) → **LDI** (LoanDepot) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 70 | **MA** (Mastercard) → **CFFN** (Capitol Federal Savi) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 71 | **MA** (Mastercard) → **WFC** (Wells Fargo) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 55% | ✅ |
| 72 | **MA** (Mastercard) → **USB** (U.S. Bancorp) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 40% | ✅ |
| 73 | **MA** (Mastercard) → **BAC** (Bank of America) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 74 | **MA** (Mastercard) → **SF** (Stifel) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 78% | ❌ |
| 75 | **MA** (Mastercard) → **EVR** (Evercore Partners) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 76 | **MA** (Mastercard) → **BR** (Broadridge Financial) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 77 | **MA** (Mastercard) → **CS** (Credit Suisse) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 78 | **MA** (Mastercard) → **AMBC** (Ambac) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 79 | **MA** (Mastercard) → **CNO** (Conseco) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 80 | **MA** (Mastercard) → **CATY** (Cathay Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 81 | **MA** (Mastercard) → **SPGI** (S&P Global) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 82 | **MA** (Mastercard) → **SOFI** (SoFi) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 83 | **MA** (Mastercard) → **NOAH** (Noah Holdings) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 84 | **MA** (Mastercard) → **BNS** (Scotiabank) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 85 | **MA** (Mastercard) → **BKKT** (Bakkt) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 86 | **MA** (Mastercard) → **BKI** (Black Knight, Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 78% | ❌ |
| 87 | **MA** (Mastercard) → **BBT** (Truist Financial) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 88 | **MA** (Mastercard) → **CG** (Carlyle Group) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 89 | **MA** (Mastercard) → **ITG** (Investment Technolog) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 90 | **MA** (Mastercard) → **XP** (XP Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 40% | ✅ |
| 91 | **MA** (Mastercard) → **BSBR** (Banco Santander (Bra) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 92 | **MA** (Mastercard) → **PNBK** (Patriot National Ban) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 93 | **MA** (Mastercard) → **CADE** (Cadence Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 94 | **MA** (Mastercard) → **NBG** (National Bank of Gre) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 95 | **MA** (Mastercard) → **SQ** (Block, Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 96 | **MA** (Mastercard) → **HOOD** (Robinhood) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 97 | **MA** (Mastercard) → **NMR** (Nomura Holdings) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 98 | **MA** (Mastercard) → **MTU** (Mitsubishi UFJ Finan) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 99 | **MA** (Mastercard) → **SWDBF** (Swedbank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 100 | **MA** (Mastercard) → **KEY** (KeyBank) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 101 | **MA** (Mastercard) → **PRI** (Primerica) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 102 | **MA** (Mastercard) → **TKYVY** (VakıfBank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 103 | **MA** (Mastercard) → **FIS** (Fidelity National In) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 104 | **MA** (Mastercard) → **BXS** (Cadence Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 105 | **MA** (Mastercard) → **NNI** (Nelnet) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 106 | **MA** (Mastercard) → **AMG** (Affiliated Managers ) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 107 | **MA** (Mastercard) → **BMTC** (Bryn Mawr Trust) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 108 | **MA** (Mastercard) → **MGI** (MoneyGram) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 109 | **MA** (Mastercard) → **RF** (Regions Financial Co) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 110 | **MA** (Mastercard) → **RY** (Royal Bank of Canada) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 111 | **MA** (Mastercard) → **OMF** (OneMain Financial) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 112 | **WU** (Western Union) → **IX** (Orix) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 113 | **WU** (Western Union) → **V** (Visa Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 55% | ✅ |
| 114 | **WU** (Western Union) → **ENV** (Envestnet) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 115 | **WU** (Western Union) → **C** (Citigroup) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 116 | **WU** (Western Union) → **AIG** (American Internation) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 117 | **WU** (Western Union) → **WBK** (Westpac) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 118 | **WU** (Western Union) → **SSB** (SouthState Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 119 | **WU** (Western Union) → **BEN** (Franklin Templeton I) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 120 | **WU** (Western Union) → **DB** (Deutsche Bank) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 62% | ✅ |
| 121 | **WU** (Western Union) → **HDB** (HDFC Bank) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 122 | **WU** (Western Union) → **AAVMY** (ABN AMRO) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 123 | **WU** (Western Union) → **CBU** (Community Bank, N.A.) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 124 | **WU** (Western Union) → **HSBC** (HSBC) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 125 | **WU** (Western Union) → **NU** (Nubank) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 62% | ✅ |
| 126 | **WU** (Western Union) → **BSAC** (Banco Santander-Chil) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 127 | **WU** (Western Union) → **MTB** (M&T Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 128 | **WU** (Western Union) → **ADS** (Alliance Data) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 78% | ❌ |
| 129 | **WU** (Western Union) → **MS** (Morgan Stanley) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 80% | ❌ |
| 130 | **WU** (Western Union) → **SHG** (Shinhan Financial Gr) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 131 | **WU** (Western Union) → **PIPR** (Piper Sandler Compan) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 132 | **WU** (Western Union) → **AL** (Air Lease) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 133 | **WU** (Western Union) → **FINN** (First National of Ne) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 134 | **WU** (Western Union) → **EV** (Eaton Vance) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 135 | **WU** (Western Union) → **TD** (Toronto-Dominion Ban) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 136 | **WU** (Western Union) → **RE** (Everest Re) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 137 | **WU** (Western Union) → **TCBK** (Tri Counties Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 138 | **WU** (Western Union) → **LDI** (LoanDepot) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 139 | **WU** (Western Union) → **CFFN** (Capitol Federal Savi) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 140 | **WU** (Western Union) → **WFC** (Wells Fargo) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 141 | **WU** (Western Union) → **USB** (U.S. Bancorp) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 142 | **WU** (Western Union) → **BAC** (Bank of America) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 143 | **WU** (Western Union) → **SF** (Stifel) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 144 | **WU** (Western Union) → **EVR** (Evercore Partners) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 145 | **WU** (Western Union) → **BR** (Broadridge Financial) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 146 | **WU** (Western Union) → **CS** (Credit Suisse) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 65% | ❌ |
| 147 | **WU** (Western Union) → **AMBC** (Ambac) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 148 | **WU** (Western Union) → **CNO** (Conseco) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 149 | **WU** (Western Union) → **CATY** (Cathay Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 150 | **WU** (Western Union) → **SPGI** (S&P Global) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 151 | **WU** (Western Union) → **SOFI** (SoFi) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 152 | **WU** (Western Union) → **NOAH** (Noah Holdings) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 153 | **WU** (Western Union) → **BNS** (Scotiabank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 154 | **WU** (Western Union) → **BKKT** (Bakkt) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 155 | **WU** (Western Union) → **BKI** (Black Knight, Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 80% | ❌ |
| 156 | **WU** (Western Union) → **BBT** (Truist Financial) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 157 | **WU** (Western Union) → **CG** (Carlyle Group) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 158 | **WU** (Western Union) → **ITG** (Investment Technolog) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 159 | **WU** (Western Union) → **XP** (XP Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 160 | **WU** (Western Union) → **BSBR** (Banco Santander (Bra) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 161 | **WU** (Western Union) → **PNBK** (Patriot National Ban) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 162 | **WU** (Western Union) → **CADE** (Cadence Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 163 | **WU** (Western Union) → **NBG** (National Bank of Gre) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 62% | ✅ |
| 164 | **WU** (Western Union) → **SQ** (Block, Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 165 | **WU** (Western Union) → **HOOD** (Robinhood) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 166 | **WU** (Western Union) → **NMR** (Nomura Holdings) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 167 | **WU** (Western Union) → **MTU** (Mitsubishi UFJ Finan) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 168 | **WU** (Western Union) → **SWDBF** (Swedbank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 169 | **WU** (Western Union) → **KEY** (KeyBank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 170 | **WU** (Western Union) → **PRI** (Primerica) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 171 | **WU** (Western Union) → **TKYVY** (VakıfBank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 172 | **WU** (Western Union) → **FIS** (Fidelity National In) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 72% | ✅ |
| 173 | **WU** (Western Union) → **BXS** (Cadence Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 174 | **WU** (Western Union) → **NNI** (Nelnet) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 88% | ❌ |
| 175 | **WU** (Western Union) → **AMG** (Affiliated Managers ) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 176 | **WU** (Western Union) → **BMTC** (Bryn Mawr Trust) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 177 | **WU** (Western Union) → **MGI** (MoneyGram) | Both in 'financial services' (Wikidata P452=Q837171) | KEEP | 82% | ✅ |
| 178 | **WU** (Western Union) → **RF** (Regions Financial Co) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 179 | **WU** (Western Union) → **RY** (Royal Bank of Canada) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 180 | **WU** (Western Union) → **OMF** (OneMain Financial) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 181 | **IX** (Orix) → **V** (Visa Inc.) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 182 | **IX** (Orix) → **ENV** (Envestnet) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 78% | ❌ |
| 183 | **IX** (Orix) → **C** (Citigroup) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 184 | **IX** (Orix) → **AIG** (American Internation) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 185 | **IX** (Orix) → **WBK** (Westpac) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 186 | **IX** (Orix) → **SSB** (SouthState Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 187 | **IX** (Orix) → **BEN** (Franklin Templeton I) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 188 | **IX** (Orix) → **DB** (Deutsche Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 189 | **IX** (Orix) → **HDB** (HDFC Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 190 | **IX** (Orix) → **AAVMY** (ABN AMRO) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 52% | ✅ |
| 191 | **IX** (Orix) → **CBU** (Community Bank, N.A.) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 88% | ❌ |
| 192 | **IX** (Orix) → **HSBC** (HSBC) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 42% | ✅ |
| 193 | **IX** (Orix) → **NU** (Nubank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 194 | **IX** (Orix) → **BSAC** (Banco Santander-Chil) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 82% | ❌ |
| 195 | **IX** (Orix) → **MTB** (M&T Bank) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 85% | ❌ |
| 196 | **IX** (Orix) → **ADS** (Alliance Data) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 197 | **IX** (Orix) → **MS** (Morgan Stanley) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 35% | ✅ |
| 198 | **IX** (Orix) → **SHG** (Shinhan Financial Gr) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 62% | ❌ |
| 199 | **IX** (Orix) → **PIPR** (Piper Sandler Compan) | Both in 'financial services' (Wikidata P452=Q837171) | REMOVE | 72% | ❌ |
| 200 | **IX** (Orix) → **AL** (Air Lease) | Both in 'financial services' (Wikidata P452=Q837171) | MODIFY | 45% | ✅ |

### Wikidata P749/P355 Parent-Subsidiary (Expected: KEEP) (9 pairs)

| # | Source → Target | Wikidata Evidence | Got | Conf | Match |
|---|----------------|------------------|-----|------|-------|
| 1 | **C** (Stellantis North Ame) → **FCAU** (Fiat Chrysler Automo) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | MODIFY | 55% | ✅ |
| 2 | **S** (Sears) → **ALL** (Allstate) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 72% | ❌ |
| 3 | **VVV** (Valvoline) → **ASH** (Ashland Inc.) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 78% | ❌ |
| 4 | **IBM** (IBM) → **RHT** (Red Hat) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 97% | ✅ |
| 5 | **SO** (Southern Company) → **mpj** (Mississippi Power) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 90% | ❌ |
| 6 | **FOX** (Fox Entertainment Gr) → **FOXA** (21st Century Fox) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 98% | ✅ |
| 7 | **CNC** (Centene Corporation) → **HNT** (Health Net) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 82% | ✅ |
| 8 | **CNC** (Centene Corporation) → **MGLN** (Magellan Health) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | KEEP | 82% | ✅ |
| 9 | **OSH** (Orchard Supply Hardw) → **LOW** (Lowe's) | Documented corporate parent-subsidiary relationship (Wikidata P749/P355) | REMOVE | 90% | ❌ |

### Different Industry + No Relationship (Expected: REMOVE) (200 pairs)

| # | Source → Target | Wikidata Evidence | Got | Conf | Match |
|---|----------------|------------------|-----|------|-------|
| 1 | **SUN** (Sunoco) → **HAS** (Hasbro) | No shared industry ('petroleum industry' vs 'game industry'), no documented corp | REMOVE | 90% | ✅ |
| 2 | **DLX** (Deluxe Corporation) → **BBY** (Best Buy) | No shared industry ('corporate services' vs 'retail'), no documented corporate p | REMOVE | 82% | ✅ |
| 3 | **ACHR** (Archer Aviation) → **NS** (NuStar Energy) | No shared industry ('aviation' vs 'petroleum industry'), no documented corporate | REMOVE | 92% | ✅ |
| 4 | **VCI** (Valassis) → **PJT** (PJT Partners) | No shared industry ('advertising' vs 'investment bank'), no documented corporate | REMOVE | 88% | ✅ |
| 5 | **CDW** (CDW) → **CADE** (Cadence Bank) | No shared industry ('business-to-business' vs 'financial services'), no document | REMOVE | 90% | ✅ |
| 6 | **SQ** (Block, Inc.) → **CLMT** (Calumet Lubricants) | No shared industry ('financial services' vs 'industrial manufacturing'), no docu | REMOVE | 85% | ✅ |
| 7 | **BK** (The Bank of New York) → **ADS** (Alliance Data) | No shared industry ('economics of banking' vs 'financial services'), no document | REMOVE | 72% | ✅ |
| 8 | **ENV** (Envestnet) → **RVBD** (Riverbed Technology) | No shared industry ('financial services' vs 'information technology'), no docume | REMOVE | 88% | ✅ |
| 9 | **U** (US Airways Group) → **WHR** (Whirlpool) | No shared industry ('aviation' vs 'home appliance industry'), no documented corp | REMOVE | 88% | ✅ |
| 10 | **OSH** (Orchard Supply Hardw) → **WOOF** (VCA Animal Hospitals) | No shared industry ('retail' vs 'veterinary medicine'), no documented corporate  | REMOVE | 88% | ✅ |
| 11 | **ROIV** (Roivant) → **NOK** (Q1418) | No shared industry ('pharmaceutical industry' vs 'computer network'), no documen | REMOVE | 85% | ✅ |
| 12 | **CABO** (Sparklight) → **AZO** (AutoZone) | No shared industry ('telecommunications' vs 'automotive industry'), no documente | REMOVE | 85% | ✅ |
| 13 | **TDY** (Teledyne Technologie) → **MON** (Monsanto) | No shared industry ('conglomerate' vs 'biotechnology'), no documented corporate  | REMOVE | 90% | ✅ |
| 14 | **POR** (Portland General Ele) → **LOW** (Lowe's) | No shared industry ('public utility' vs 'hardware store'), no documented corpora | REMOVE | 72% | ✅ |
| 15 | **EDS** (Hewlett Packard Ente) → **MNK** (Mallinckrodt Pharmac) | No shared industry ('information technology industry' vs 'pharmaceutical industr | REMOVE | 62% | ✅ |
| 16 | **RCL** (Royal Caribbean Grou) → **BIN** (Waste Connections of) | No shared industry ('cruise line' vs 'waste management'), no documented corporat | REMOVE | 78% | ✅ |
| 17 | **NPD** (China Nepstar) → **TA** (TravelCenters of Ame) | No shared industry ('pharmaceutical industry' vs 'truck stop'), no documented co | REMOVE | 85% | ✅ |
| 18 | **VICI** (Vici Properties) → **AMRB** (American River Bank) | No shared industry ('real property' vs 'bank'), no documented corporate parent-s | REMOVE | 90% | ✅ |
| 19 | **HZNP** (Horizon Therapeutics) → **ES** (Eversource Energy) | No shared industry ('pharmaceutical industry' vs 'public utility'), no documente | REMOVE | 90% | ✅ |
| 20 | **NIU** (Niu Technologies) → **MRCY** (Mercury Systems) | No shared industry ('transport industry' vs 'aerospace industry'), no documented | REMOVE | 85% | ✅ |
| 21 | **BBRY** (BlackBerry) → **BIN** (Waste Connections of) | No shared industry ('Internet of Things' vs 'waste management'), no documented c | REMOVE | 85% | ✅ |
| 22 | **ITW** (Illinois Tool Works) → **PRA** (ProAssurance) | No shared industry ('industrial manufacturing' vs 'insurance'), no documented co | REMOVE | 88% | ✅ |
| 23 | **PLTK** (Playtika) → **IDT** (IDT Corporation) | No shared industry ('video game industry' vs 'telecommunications'), no documente | REMOVE | 85% | ✅ |
| 24 | **EQT** (EQT) → **SNRZ** (Sunrise Senior Livin) | No shared industry ('petroleum industry' vs 'health care'), no documented corpor | REMOVE | 85% | ✅ |
| 25 | **BAC** (Bank of America) → **CWT** (California Water Ser) | No shared industry ('International Standard Industrial Classification' vs 'water | REMOVE | 85% | ✅ |
| 26 | **PDD** (PDD Holdings) → **PEP** (PepsiCo) | No shared industry ('e-commerce' vs 'beverage industry'), no documented corporat | REMOVE | 90% | ✅ |
| 27 | **ICO** (International Coal G) → **MSO** (Martha Stewart Livin) | No shared industry ('mining of coal' vs 'broadcasting'), no documented corporate | REMOVE | 72% | ✅ |
| 28 | **SE** (Spectra Energy) → **BPL** (Buckeye Partners) | No shared industry ('petroleum industry' vs 'petroleum'), no documented corporat | REMOVE | 92% | ✅ |
| 29 | **HOV** (K. Hovnanian Homes) → **DWA** (DreamWorks Animation) | No shared industry ('construction' vs 'film production'), no documented corporat | REMOVE | 92% | ✅ |
| 30 | **ES** (Eversource Energy) → **MIR** (Mirion Technologies) | No shared industry ('public utility' vs 'manufacturing of scientific and technic | REMOVE | 78% | ✅ |
| 31 | **LZB** (La-Z-Boy) → **EXTR** (Extreme Networks) | No shared industry ('industrial manufacturing' vs 'networking hardware'), no doc | REMOVE | 92% | ✅ |
| 32 | **ENE** (Enron) → **NSC** (Norfolk Southern Rai) | No shared industry ('energy industry' vs 'transport'), no documented corporate p | REMOVE | 62% | ✅ |
| 33 | **ECA** (Encana) → **MIK** (The Michaels Compani) | No shared industry ('petroleum industry' vs 'retail'), no documented corporate p | REMOVE | 92% | ✅ |
| 34 | **ZTO** (ZTO Express) → **ADX** (Adams Funds) | No shared industry ('logistics' vs 'investment'), no documented corporate parent | REMOVE | 90% | ✅ |
| 35 | **PDD** (PDD Holdings) → **TSN** (Tyson Foods) | No shared industry ('e-commerce' vs 'meatpacking industry'), no documented corpo | REMOVE | 85% | ✅ |
| 36 | **DF** (Dean Foods) → **HAL** (Halliburton) | No shared industry ('food industry' vs 'petroleum'), no documented corporate par | REMOVE | 95% | ✅ |
| 37 | **JEF** (Jefferies & Company) → **BXC** (BlueLinx) | No shared industry ('investment' vs 'wholesale'), no documented corporate parent | REMOVE | 85% | ✅ |
| 38 | **MESA** (Mesa Air Group) → **WFC** (Wells Fargo) | No shared industry ('aviation' vs 'financial services'), no documented corporate | REMOVE | 85% | ✅ |
| 39 | **CLF** (Cleveland-Cliffs) → **BLL** (Ball Corporation) | No shared industry ('iron and steel industry' vs 'mechanical engineering'), no d | REMOVE | 78% | ✅ |
| 40 | **DKS** (Dick's Sporting Good) → **NFE** (New Fortress Energy) | No shared industry ('retail' vs 'energy industry'), no documented corporate pare | REMOVE | 92% | ✅ |
| 41 | **CBAT** (CBAK Energy Technolo) → **HCM** (Hutchison China Medi) | No shared industry ('battery industry' vs 'biomedicine'), no documented corporat | REMOVE | 78% | ✅ |
| 42 | **BPT** (BP Prudhoe Bay Royal) → **PIPR** (Piper Sandler Compan) | No shared industry ('petroleum industry' vs 'financial services'), no documented | REMOVE | 85% | ✅ |
| 43 | **CCSC** (Country Style Cookin) → **TS** (Tenaris) | No shared industry ('food industry' vs 'mining industry'), no documented corpora | REMOVE | 82% | ✅ |
| 44 | **AMR** (Alpha Natural Resour) → **MSO** (Martha Stewart Livin) | No shared industry ('mining' vs 'broadcasting'), no documented corporate parent- | REMOVE | 72% | ✅ |
| 45 | **CNO** (Conseco) → **EQH** (Equitable Holdings) | No shared industry ('financial services' vs 'insurance'), no documented corporat | MODIFY | 40% | ❌ |
| 46 | **FE** (FirstEnergy) → **ORCL** (Oracle Corporation) | No shared industry ('electricity supply company' vs 'information technology cons | REMOVE | 85% | ✅ |
| 47 | **AGR** (Avangrid) → **TLK** (Telkom Indonesia) | No shared industry ('energy industry' vs 'telecommunications'), no documented co | REMOVE | 95% | ✅ |
| 48 | **TMH** (Team Health Holdings) → **DST** (DST Systems) | No shared industry ('health care' vs 'corporate services'), no documented corpor | REMOVE | 72% | ✅ |
| 49 | **NOAH** (Noah Holdings) → **BE** (Bloom Energy) | No shared industry ('financial services' vs 'electronics industry'), no document | REMOVE | 92% | ✅ |
| 50 | **EQH** (Equitable Holdings) → **CRC** (California Resources) | No shared industry ('insurance' vs 'petroleum industry'), no documented corporat | REMOVE | 85% | ✅ |
| 51 | **CWT** (California Water Ser) → **RP** (RealPage) | No shared industry ('water supply' vs 'property management'), no documented corp | REMOVE | 90% | ✅ |
| 52 | **NEGG** (Newegg) → **V** (Visa Inc.) | No shared industry ('retail' vs 'financial services'), no documented corporate p | REMOVE | 92% | ✅ |
| 53 | **MEAT** (Meat tech) → **CYRN** (Commtouch) | No shared industry ('food industry' vs 'software industry'), no documented corpo | REMOVE | 90% | ✅ |
| 54 | **VITC** (Vitacost) → **ASNA** (Tween Brands) | No shared industry ('e-commerce' vs 'retail'), no documented corporate parent-su | REMOVE | 88% | ✅ |
| 55 | **LGF** (Starz Entertainment) → **WSO** (Watsco) | No shared industry ('show business' vs 'heating, ventilation, and air conditioni | REMOVE | 92% | ✅ |
| 56 | **WWW** (Wolverine World Wide) → **MFC** (Manulife Financial) | No shared industry ('textile industry' vs 'insurance industry'), no documented c | REMOVE | 90% | ✅ |
| 57 | **S** (Sprint Corporation) → **XOM** (ExxonMobil) | No shared industry ('telecommunications' vs 'petroleum industry'), no documented | REMOVE | 88% | ✅ |
| 58 | **LOCO** (El Pollo Loco) → **C** (Stellantis North Ame) | No shared industry ('restaurant' vs 'automotive industry'), no documented corpor | REMOVE | 92% | ✅ |
| 59 | **EMN** (Eastman Chemical Com) → **MMM** (3M) | No shared industry ('industrial manufacturing' vs 'mining industry'), no documen | MODIFY | 35% | ❌ |
| 60 | **ZZ** (Sealy Corporation) → **SSB** (SouthState Bank) | No shared industry ('mattress' vs 'financial services'), no documented corporate | REMOVE | 72% | ✅ |
| 61 | **FIS** (Fidelity National In) → **EMN** (Eastman Chemical Com) | No shared industry ('financial services' vs 'industrial manufacturing'), no docu | REMOVE | 85% | ✅ |
| 62 | **SCL** (Stepan Company) → **ITCL** (Banco Itaú Corpbanca) | No shared industry ('chemistry' vs 'bank'), no documented corporate parent-subsi | REMOVE | 72% | ✅ |
| 63 | **WNS** (WNS Global Services) → **HMI** (Huami Corporation) | No shared industry ('information technology consulting' vs 'industrial manufactu | REMOVE | 72% | ✅ |
| 64 | **CTAS** (Cintas) → **DPS** (Dr Pepper Snapple Gr) | No shared industry ('tertiary sector of the economy' vs 'beverage industry'), no | REMOVE | 85% | ✅ |
| 65 | **BLL** (Ball Corporation) → **PLTR** (Palantir Technologie) | No shared industry ('mechanical engineering' vs 'data analytics software industr | REMOVE | 92% | ✅ |
| 66 | **CYT** (Cytec Industries) → **RNA** (Prosensa) | No shared industry ('composite material' vs 'biotechnology'), no documented corp | REMOVE | 55% | ✅ |
| 67 | **GIL** (Gildan Activewear) → **BMTC** (Bryn Mawr Trust) | No shared industry ('textile industry' vs 'financial services'), no documented c | REMOVE | 85% | ✅ |
| 68 | **CBB** (Caliber System) → **VITC** (Vitacost) | No shared industry ('trucking industry' vs 'e-commerce'), no documented corporat | REMOVE | 90% | ✅ |
| 69 | **ALV** (Autoliv) → **PDD** (PDD Holdings) | No shared industry ('automotive supplier' vs 'e-commerce'), no documented corpor | REMOVE | 92% | ✅ |
| 70 | **SONO** (Sonos) → **BW** (Babcock & Wilcox) | No shared industry ('consumer electronics industry' vs 'industrial manufacturing | REMOVE | 85% | ✅ |
| 71 | **CAN** (Canaan Creative) → **NMR** (Nomura Holdings) | No shared industry ('consumer electronics industry' vs 'financial sector'), no d | REMOVE | 82% | ✅ |
| 72 | **GXO** (GXO, Inc.) → **TCO** (Taubman Centers) | No shared industry ('logistics' vs 'real estate investment trust'), no documente | REMOVE | 85% | ✅ |
| 73 | **PTR** (PetroChina Company L) → **HKD** (AMTD Digital) | No shared industry ('petroleum industry' vs 'fintech'), no documented corporate  | REMOVE | 72% | ✅ |
| 74 | **EMMS** (Emmis Communications) → **BE** (Bloom Energy) | No shared industry ('broadcasting' vs 'electronics industry'), no documented cor | REMOVE | 92% | ✅ |
| 75 | **ACFC** (Atlantic Coast Finan) → **MESA** (Mesa Air Group) | No shared industry ('bank' vs 'aviation'), no documented corporate parent-subsid | REMOVE | 90% | ✅ |
| 76 | **ESL** (Esterline) → **EW** (Edwards Lifesciences) | No shared industry ('aerospace industry' vs 'medical device'), no documented cor | REMOVE | 55% | ✅ |
| 77 | **SPB** (Spectrum Brands) → **SW** (Smurfit Kappa Group) | No shared industry ('industrial manufacturing' vs 'product packaging industry'), | REMOVE | 72% | ✅ |
| 78 | **NFE** (New Fortress Energy) → **LSYN** (Libsyn) | No shared industry ('energy industry' vs 'podcast'), no documented corporate par | REMOVE | 97% | ✅ |
| 79 | **SNX** (Synnex) → **PEO** (Petroleum & Resource) | No shared industry ('information technology' vs 'investment'), no documented cor | REMOVE | 85% | ✅ |
| 80 | **IBM** (IBM) → **CDLX** (Cardlytics) | No shared industry ('computer industry' vs 'loyalty marketing'), no documented c | REMOVE | 85% | ✅ |
| 81 | **WELL** (Welltower) → **PK** (Park Hotels & Resort) | No shared industry ('real estate investment trust' vs 'hospitality industry'), n | REMOVE | 72% | ✅ |
| 82 | **DKS** (Dick's Sporting Good) → **ALC** (Alcon) | No shared industry ('retail' vs 'pharmaceutical industry'), no documented corpor | REMOVE | 85% | ✅ |
| 83 | **zen** (Zendesk) → **DENN** (Denny's) | No shared industry ('software industry' vs 'gastronomy'), no documented corporat | REMOVE | 85% | ✅ |
| 84 | **CYCC** (Cyclacel) → **LEA** (Lear Corporation) | No shared industry ('pharmaceutical industry' vs 'automotive supplier'), no docu | REMOVE | 90% | ✅ |
| 85 | **UAL** (United Airlines Hold) → **WF** (Woori Financial Grou) | No shared industry ('air transport' vs 'financial sector'), no documented corpor | REMOVE | 85% | ✅ |
| 86 | **DST** (DST Systems) → **MRK** (Merck & Co.) | No shared industry ('corporate services' vs 'pharmaceutical industry'), no docum | REMOVE | 90% | ✅ |
| 87 | **HL** (Hecla Mining) → **FMC** (FMC Corporation) | No shared industry ('mining' vs 'chemical industry'), no documented corporate pa | REMOVE | 85% | ✅ |
| 88 | **PHG** (Koninklijke Philips ) → **DWA** (DreamWorks Animation) | No shared industry ('consumer electronics industry' vs 'film production'), no do | REMOVE | 85% | ✅ |
| 89 | **ADBE** (Adobe) → **AIG** (American Internation) | No shared industry ('artificial intelligence' vs 'financial services'), no docum | REMOVE | 92% | ✅ |
| 90 | **CPG** (Crescent Point Energ) → **CAR** (Avis Budget Group) | No shared industry ('petroleum industry' vs 'car rental company'), no documented | REMOVE | 78% | ✅ |
| 91 | **NLSN** (Nielsen Company) → **ECA** (Encana) | No shared industry ('information industry' vs 'petroleum industry'), no document | REMOVE | 85% | ✅ |
| 92 | **ABC** (Cencora) → **O** (Realty Income Corpor) | No shared industry ('pharmaceutical industry' vs 'real estate investment trust') | REMOVE | 82% | ✅ |
| 93 | **AMT** (American Tower Corpo) → **GK** (G&K Services) | No shared industry ('real estate investment trust' vs 'tertiary sector of the ec | REMOVE | 90% | ✅ |
| 94 | **NBG** (National Bank of Gre) → **BYI** (Bally Technologies) | No shared industry ('financial sector' vs 'gambling industry'), no documented co | REMOVE | 88% | ✅ |
| 95 | **mpj** (Mississippi Power) → **PLTR** (Palantir Technologie) | No shared industry ('public utility' vs 'data analytics software industry'), no  | REMOVE | 70% | ✅ |
| 96 | **SP** (Spelling Television) → **CHA** (China Telecommunicat) | No shared industry ('television' vs 'terrestrial television'), no documented cor | REMOVE | 88% | ✅ |
| 97 | **MMNWF** (MedMen) → **MIK** (The Michaels Compani) | No shared industry ('cannabis industry' vs 'retail'), no documented corporate pa | REMOVE | 82% | ✅ |
| 98 | **LEA** (Lear Corporation) → **PCOR** (Procore) | No shared industry ('automotive supplier' vs 'construction'), no documented corp | REMOVE | 85% | ✅ |
| 99 | **TWKS** (ThoughtWorks) → **RF** (Regions Financial Co) | No shared industry ('software industry' vs 'economics of banking'), no documente | REMOVE | 85% | ✅ |
| 100 | **NFLX** (Netflix, Inc.) → **JWN** (Nordstrom) | No shared industry ('television production' vs 'retail'), no documented corporat | REMOVE | 85% | ✅ |
| 101 | **OPRA** (Opera) → **G** (Genpact) | No shared industry ('Internet industry' vs 'professional service'), no documente | REMOVE | 90% | ✅ |
| 102 | **W** (Wayfair) → **ALC** (Alcon) | No shared industry ('e-commerce' vs 'pharmaceutical industry'), no documented co | REMOVE | 92% | ✅ |
| 103 | **BHI** (Baker Hughes) → **GOLD** (Barrick Mining Corpo) | No shared industry ('petroleum industry' vs 'mining'), no documented corporate p | REMOVE | 85% | ✅ |
| 104 | **GSK** (GSK) → **CTAS** (Cintas) | No shared industry ('pharmaceutical industry' vs 'tertiary sector of the economy | REMOVE | 92% | ✅ |
| 105 | **NLSN** (Nielsen Company) → **DJT** (Trump Media & Techno) | No shared industry ('information industry' vs 'technology industry'), no documen | REMOVE | 90% | ✅ |
| 106 | **KNYJF** (Kone) → **GOLD** (Randgold Resources) | No shared industry ('engineering' vs 'mining'), no documented corporate parent-s | MODIFY | 62% | ❌ |
| 107 | **CBAT** (CBAK Energy Technolo) → **SMT** (SMART Technologies) | No shared industry ('battery industry' vs 'computing'), no documented corporate  | REMOVE | 88% | ✅ |
| 108 | **HMI** (Huami Corporation) → **KIM** (Kimco Realty) | No shared industry ('industrial manufacturing' vs 'real estate investment trust' | REMOVE | 78% | ✅ |
| 109 | **LEGN** (Legend Biotech) → **VNO** (Vornado Realty Trust) | No shared industry ('biotechnology' vs 'real estate investment trust'), no docum | REMOVE | 92% | ✅ |
| 110 | **BTI** (British American Tob) → **LEGN** (Legend Biotech) | No shared industry ('food and tobacco industry' vs 'biotechnology'), no document | REMOVE | 85% | ✅ |
| 111 | **SUI** (Sun Communities) → **AMZN** (Amazon) | No shared industry ('real estate investment trust' vs 'retail'), no documented c | REMOVE | 85% | ✅ |
| 112 | **GTW** (Gateway) → **LOB** (Live Oak Bank) | No shared industry ('computer hardware industry' vs 'bank'), no documented corpo | REMOVE | 72% | ✅ |
| 113 | **MGA** (Magna International) → **NNI** (Nelnet) | No shared industry ('automotive industry' vs 'financial services'), no documente | REMOVE | 92% | ✅ |
| 114 | **MDT** (Medtronic plc) → **EV** (Eaton Vance) | No shared industry ('medical technology industry' vs 'financial services'), no d | REMOVE | 88% | ✅ |
| 115 | **CCSC** (Country Style Cookin) → **NU** (Nubank) | No shared industry ('food industry' vs 'financial services'), no documented corp | REMOVE | 88% | ✅ |
| 116 | **PL** (Planet Labs) → **PCMI** (PC Mall, Inc.) | No shared industry ('space industry' vs 'direct marketing'), no documented corpo | REMOVE | 78% | ✅ |
| 117 | **LOCO** (El Pollo Loco) → **SSB** (SouthState Bank) | No shared industry ('restaurant' vs 'financial services'), no documented corpora | REMOVE | 85% | ✅ |
| 118 | **MESA** (Mesa Air Group) → **SOS** (Storage Computer Cor) | No shared industry ('aviation' vs 'software industry'), no documented corporate  | REMOVE | 92% | ✅ |
| 119 | **CGI** (Celadon Group) → **CLS** (Celestica) | No shared industry ('logistics' vs 'electronics'), no documented corporate paren | MODIFY | 42% | ❌ |
| 120 | **WSH** (Willis Group) → **CYRN** (Commtouch) | No shared industry ('insurance broker' vs 'software industry'), no documented co | REMOVE | 78% | ✅ |
| 121 | **SSB** (SouthState Bank) → **SUN** (Sunoco) | No shared industry ('financial services' vs 'petroleum industry'), no documented | REMOVE | 88% | ✅ |
| 122 | **SNX** (TD SYNNEX) → **CYRN** (Commtouch) | No shared industry ('IT service management' vs 'software industry'), no document | REMOVE | 90% | ✅ |
| 123 | **BABWF** (International Airlin) → **VSH** (Vishay Intertechnolo) | No shared industry ('aviation' vs 'electronics'), no documented corporate parent | REMOVE | 82% | ✅ |
| 124 | **WBK** (Westpac) → **SR** (Spire Inc.) | No shared industry ('financial services' vs 'petroleum industry'), no documented | REMOVE | 85% | ✅ |
| 125 | **PDS** (Precision Drilling) → **CLH** (Clean Harbors) | No shared industry ('petroleum industry' vs 'waste management'), no documented c | MODIFY | 52% | ❌ |
| 126 | **FINN** (First National of Ne) → **SMT** (SMART Technologies) | No shared industry ('financial services' vs 'computing'), no documented corporat | REMOVE | 62% | ✅ |
| 127 | **GLOB** (Globant) → **THG** (Hanover Insurance) | No shared industry ('software development' vs 'insurance'), no documented corpor | REMOVE | 90% | ✅ |
| 128 | **BSBR** (Banco Santander (Bra) → **RGA** (Reinsurance Group of) | No shared industry ('financial services' vs 'insurance industry'), no documented | REMOVE | 85% | ✅ |
| 129 | **CMI** (Cummins) → **AU** (AngloGold Ashanti) | No shared industry ('manufacture of machinery and equipment' vs 'mining'), no do | REMOVE | 85% | ✅ |
| 130 | **DLR** (Digital Realty Trust) → **SMG** (The Scotts Miracle-G) | No shared industry ('real estate investment trust' vs 'industrial manufacturing' | REMOVE | 90% | ✅ |
| 131 | **CLP** (Colonial Properties) → **OMC** (Omnicom Group) | No shared industry ('real estate investment trust' vs 'mass media'), no document | REMOVE | 85% | ✅ |
| 132 | **CWT** (California Water Ser) → **FMC** (FMC Corporation) | No shared industry ('water supply' vs 'chemical industry'), no documented corpor | REMOVE | 82% | ✅ |
| 133 | **MEAT** (Meat tech) → **RNA** (Prosensa) | No shared industry ('food industry' vs 'biotechnology'), no documented corporate | REMOVE | 85% | ✅ |
| 134 | **THI** (Tim Hortons) → **YELL** (Yellow Corporation) | No shared industry ('fast food' vs 'trucking industry'), no documented corporate | REMOVE | 85% | ✅ |
| 135 | **LNC** (Lincoln National Cor) → **HOV** (K. Hovnanian Homes) | No shared industry ('insurance' vs 'construction'), no documented corporate pare | REMOVE | 80% | ✅ |
| 136 | **KMI** (Kinder Morgan) → **ABC** (Cencora) | No shared industry ('petroleum industry' vs 'pharmaceutical industry'), no docum | REMOVE | 92% | ✅ |
| 137 | **ORBC** (Orbcomm) → **DIS** (The Walt Disney Comp) | No shared industry ('telecommunications' vs 'media industry'), no documented cor | REMOVE | 85% | ✅ |
| 138 | **CYCC** (Cyclacel) → **BR** (Broadridge Financial) | No shared industry ('pharmaceutical industry' vs 'financial services'), no docum | REMOVE | 90% | ✅ |
| 139 | **AMT** (American Tower Corpo) → **TROW** (T. Rowe Price) | No shared industry ('real estate investment trust' vs 'asset management'), no do | REMOVE | 85% | ✅ |
| 140 | **ARCH** (Arch Resources) → **SBL** (Symbol Technologies) | No shared industry ('mining of coal' vs 'computer hardware industry'), no docume | MODIFY | 30% | ❌ |
| 141 | **VCI** (Valassis) → **LE** (Lands' End) | No shared industry ('advertising' vs 'retail'), no documented corporate parent-s | REMOVE | 85% | ✅ |
| 142 | **IX** (Orix) → **MT** (ArcelorMittal) | No shared industry ('financial services' vs 'mining industry'), no documented co | REMOVE | 72% | ✅ |
| 143 | **RHP** (Ryman Hospitality Pr) → **CART** (Instacart) | No shared industry ('real estate investment trust' vs 'retail'), no documented c | REMOVE | 85% | ✅ |
| 144 | **SSP** (E. W. Scripps Compan) → **FIS** (Fidelity National In) | No shared industry ('broadcast television system' vs 'financial services'), no d | REMOVE | 88% | ✅ |
| 145 | **ESL** (Esterline) → **ZTO** (ZTO Express) | No shared industry ('aerospace industry' vs 'logistics'), no documented corporat | REMOVE | 92% | ✅ |
| 146 | **MATX** (Matson, Inc.) → **FSL** (Freescale Semiconduc) | No shared industry ('shipping line' vs 'central processing unit'), no documented | REMOVE | 88% | ✅ |
| 147 | **NI** (NiSource) → **CLP** (Colonial Properties) | No shared industry ('public utility' vs 'real estate investment trust'), no docu | REMOVE | 88% | ✅ |
| 148 | **GNRC** (Generac Holdings Inc) → **FOX** (Fox Corporation) | No shared industry ('industrial manufacturing' vs 'media industry'), no document | REMOVE | 85% | ✅ |
| 149 | **HWP** (Hewlett-Packard) → **BIN** (Waste Connections of) | No shared industry ('computer hardware industry' vs 'waste management'), no docu | REMOVE | 65% | ✅ |
| 150 | **RGA** (Reinsurance Group of) → **ADBE** (Adobe) | No shared industry ('insurance industry' vs 'artificial intelligence'), no docum | REMOVE | 85% | ✅ |
| 151 | **NS** (NuStar Energy) → **DNKN** (Dunkin' Brands) | No shared industry ('petroleum industry' vs 'gastronomy'), no documented corpora | REMOVE | 92% | ✅ |
| 152 | **FIS** (Fidelity National In) → **CHLN** (China Housing and La) | No shared industry ('financial services' vs 'construction'), no documented corpo | REMOVE | 92% | ✅ |
| 153 | **DOMO** (Domo) → **NPK** (National Presto Indu) | No shared industry ('business software industry' vs 'product'), no documented co | REMOVE | 92% | ✅ |
| 154 | **BOH** (Bank of Hawaii) → **FINN** (First National of Ne) | No shared industry ('finance' vs 'financial services'), no documented corporate  | REMOVE | 85% | ✅ |
| 155 | **CHA** (China Telecommunicat) → **ICON** (Iconix Brand Group) | No shared industry ('terrestrial television' vs 'textile industry'), no document | REMOVE | 88% | ✅ |
| 156 | **MIK** (Michaels) → **CVG** (Convergys) | No shared industry ('retail' vs 'customer relationship management'), no document | REMOVE | 82% | ✅ |
| 157 | **GOLD** (Barrick Mining Corpo) → **BWA** (BorgWarner) | No shared industry ('mining' vs 'automotive industry'), no documented corporate  | REMOVE | 85% | ✅ |
| 158 | **ITCL** (Banco Itaú Corpbanca) → **CRC** (California Resources) | No shared industry ('bank' vs 'petroleum industry'), no documented corporate par | REMOVE | 72% | ✅ |
| 159 | **KID** (Kid Brands) → **WHR** (Whirlpool) | No shared industry ('game industry' vs 'home appliance industry'), no documented | REMOVE | 88% | ✅ |
| 160 | **BTG** (B2Gold) → **ALB** (Albemarle Corporatio) | No shared industry ('mining' vs 'chemical industry'), no documented corporate pa | REMOVE | 85% | ✅ |
| 161 | **SCCO** (Southern Copper Corp) → **JWEL** (Jowell Global) | No shared industry ('mining' vs 'e-commerce'), no documented corporate parent-su | REMOVE | 90% | ✅ |
| 162 | **FIVN** (Five9 Inc.) → **IT** (Gartner) | No shared industry ('software industry' vs 'market research'), no documented cor | REMOVE | 72% | ✅ |
| 163 | **THS** (Isac) → **MS** (Morgan Stanley) | No shared industry ('food industry' vs 'financial services'), no documented corp | REMOVE | 85% | ✅ |
| 164 | **APH** (Amphenol) → **VAL** (Valspar) | No shared industry ('electronics' vs 'chemical industry'), no documented corpora | REMOVE | 85% | ✅ |
| 165 | **TWKS** (ThoughtWorks) → **AA** (Alcoa) | No shared industry ('software industry' vs 'aluminium industry'), no documented  | REMOVE | 88% | ✅ |
| 166 | **OKTA** (Okta) → **RL** (Ralph Lauren Corpora) | No shared industry ('software industry' vs 'commerce'), no documented corporate  | REMOVE | 95% | ✅ |
| 167 | **GSK** (GSK) → **HTHT** (H World Group Limite) | No shared industry ('pharmaceutical industry' vs 'hotel manager'), no documented | REMOVE | 90% | ✅ |
| 168 | **TALO** (Talos Energy) → **mpj** (Mississippi Power) | No shared industry ('petroleum industry' vs 'public utility'), no documented cor | REMOVE | 70% | ✅ |
| 169 | **DWA** (DreamWorks Animation) → **LEA** (Lear Corporation) | No shared industry ('film production' vs 'automotive supplier'), no documented c | REMOVE | 92% | ✅ |
| 170 | **CCSC** (Country Style Cookin) → **DIS** (The Walt Disney Comp) | No shared industry ('food industry' vs 'media industry'), no documented corporat | REMOVE | 90% | ✅ |
| 171 | **ADI** (Analog Devices) → **MTBC** (CareCloud) | No shared industry ('semiconductor industry' vs 'health information technology') | REMOVE | 90% | ✅ |
| 172 | **ICA** (Empresas ICA) → **RAD** (Rite Aid) | No shared industry ('construction' vs 'retail'), no documented corporate parent- | REMOVE | 88% | ✅ |
| 173 | **BEBE** (Bebe Stores) → **ESC** (Emeritus Assisted Li) | No shared industry ('retail' vs 'Senior living'), no documented corporate parent | REMOVE | 92% | ✅ |
| 174 | **ECA** (Encana) → **PEO** (Petroleum & Resource) | No shared industry ('petroleum industry' vs 'investment'), no documented corpora | MODIFY | 45% | ❌ |
| 175 | **LNT** (Alliant Energy) → **MDT** (Medtronic plc) | No shared industry ('public utility' vs 'medical technology industry'), no docum | REMOVE | 85% | ✅ |
| 176 | **MRCY** (Mercury Systems) → **GXO** (GXO, Inc.) | No shared industry ('aerospace industry' vs 'logistics'), no documented corporat | REMOVE | 85% | ✅ |
| 177 | **CMLS** (Cumulus Media) → **TRI** (Thomson Reuters) | No shared industry ('news media' vs 'media industry'), no documented corporate p | REMOVE | 85% | ✅ |
| 178 | **CVAC** (CureVac) → **ALTO** (Altos Computer Syste) | No shared industry ('biotechnology industry' vs 'computer hardware industry'), n | REMOVE | 82% | ✅ |
| 179 | **SJI** (South Jersey Industr) → **NSC** (Norfolk Southern Rai) | No shared industry ('energy service company' vs 'transport'), no documented corp | REMOVE | 80% | ✅ |
| 180 | **PPG** (PPG Industries) → **zen** (Zendesk) | No shared industry ('paint' vs 'software industry'), no documented corporate par | REMOVE | 90% | ✅ |
| 181 | **RF** (Regions Financial Co) → **ADI** (Analog Devices) | No shared industry ('economics of banking' vs 'semiconductor industry'), no docu | REMOVE | 88% | ✅ |
| 182 | **EH** (EHang) → **CNO** (Conseco) | No shared industry ('aerospace engineering' vs 'financial services'), no documen | REMOVE | 95% | ✅ |
| 183 | **ING** (ING Group) → **HZNP** (Horizon Therapeutics) | No shared industry ('financial service activities, except insurance and pension  | REMOVE | 85% | ✅ |
| 184 | **CNI** (Canadian National Ra) → **BTI** (British American Tob) | No shared industry ('rail freight transport' vs 'food and tobacco industry'), no | REMOVE | 85% | ✅ |
| 185 | **CG** (Carlyle Group) → **CVG** (Convergys) | No shared industry ('financial services' vs 'customer relationship management'), | REMOVE | 72% | ✅ |
| 186 | **PZE** (Petrobras Argentina) → **RHP** (Ryman Hospitality Pr) | No shared industry ('petroleum industry' vs 'real estate investment trust'), no  | REMOVE | 92% | ✅ |
| 187 | **BIN** (Waste Connections of) → **MGLN** (Magellan Health) | No shared industry ('waste management' vs 'managed care'), no documented corpora | REMOVE | 92% | ✅ |
| 188 | **IEP** (Icahn Enterprises) → **TWKS** (ThoughtWorks) | No shared industry ('conglomerate' vs 'software industry'), no documented corpor | REMOVE | 85% | ✅ |
| 189 | **FCAU** (Fiat Chrysler Automo) → **VE** (Veolia) | No shared industry ('automotive industry' vs 'Q112166112'), no documented corpor | REMOVE | 78% | ✅ |
| 190 | **POR** (Portland General Ele) → **LOCO** (El Pollo Loco) | No shared industry ('public utility' vs 'restaurant'), no documented corporate p | REMOVE | 90% | ✅ |
| 191 | **X** (U.S. Steel) → **MGLN** (Magellan Health) | No shared industry ('iron and steel industry' vs 'managed care'), no documented  | REMOVE | 92% | ✅ |
| 192 | **ITW** (Illinois Tool Works) → **HCM** (Hutchison China Medi) | No shared industry ('industrial manufacturing' vs 'biomedicine'), no documented  | REMOVE | 88% | ✅ |
| 193 | **BULL** (Groupe Bull) → **SF** (Stifel) | No shared industry ('IT systems and software consulting' vs 'investment'), no do | REMOVE | 72% | ✅ |
| 194 | **FOXA** (21st Century Fox) → **EQH** (Equitable Holdings) | No shared industry ('news media' vs 'insurance'), no documented corporate parent | REMOVE | 85% | ✅ |
| 195 | **BIN** (Waste Connections of) → **ACM** (AECOM) | No shared industry ('waste management' vs 'construction'), no documented corpora | REMOVE | 62% | ✅ |
| 196 | **TRI** (Thomson Reuters) → **ALK** (Alaska Air Group) | No shared industry ('media industry' vs 'transport'), no documented corporate pa | REMOVE | 88% | ✅ |
| 197 | **PTCT** (PTC Therapeutics) → **FOX** (Fox Corporation) | No shared industry ('pharmaceutical industry' vs 'media industry'), no documente | REMOVE | 90% | ✅ |
| 198 | **DCI** (Donaldson Company) → **ZZ** (Sealy Corporation) | No shared industry ('membrane' vs 'mattress'), no documented corporate parent-su | REMOVE | 78% | ✅ |
| 199 | **BOSC** (B.O.S. Better Online) → **RST** (Rosetta Stone) | No shared industry ('technology' vs 'software industry'), no documented corporat | REMOVE | 72% | ✅ |
| 200 | **TCBK** (Tri Counties Bank) → **SUI** (Sun Communities) | No shared industry ('financial services' vs 'real estate investment trust'), no  | REMOVE | 90% | ✅ |

---

## 💡 Honest Findings

### 1. Validator is precision-biased, not balanced

- **Precision: 100%** — When the validator says KEEP, it's almost always right
- **Recall: 18%** — But it misses many edges that Wikidata considers related
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

*Report generated from: `benchmark_wikidata_500_clean.json`*  
*Wikidata SPARQL endpoint: https://query.wikidata.org/sparql*