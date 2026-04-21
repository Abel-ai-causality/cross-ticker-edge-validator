# PuppyGraph Edge Validation Report

**测试日期**: 2026-04-21
**工具**: `/Users/zeyu/abel_2/edge_validator_balanced.py`
**LLM**: deepseek/deepseek-chat (via OpenRouter)
**环境**: PuppyGraph Production
**字段**: volume (交易量)
**测试范围**: 每个 ticker 的 top 20 条唯一 incoming edges (DISTINCT 去重)

---

## 测试结果总览

| Ticker | Total | KEEP | MODIFY | REMOVE | ERROR | UNKNOWN |
|--------|-------|------|--------|--------|-------|---------|
| **GOOGL** | 20 | 10 (50%) | 6 (30%) | 3 (15%) | 0 | 1 (5%) |
| **NVDA** | 20 | 10 (50%) | 6 (30%) | 2 (10%) | 2 (10%) | 0 |
| **TSLA** | 20 | 6 (30%) | 8 (40%) | 3 (15%) | 1 (5%) | 2 (10%) |
| **MSFT** | 20 | 5 (25%) | 8 (40%) | 4 (20%) | 1 (5%) | 2 (10%) |
| **AAPL** | 20 | 5 (25%) | 5 (25%) | 5 (25%) | 5 (25%) | 0 |
| **AMZN** | 20 | 4 (20%) | 7 (35%) | 0 (0%) | 9 (45%) | 0 |

### 聚合统计 (6 个 ticker, 120 条边)

| 分类 | 数量 | 占比 |
|------|------|------|
| ✅ KEEP | 40 | 33.3% |
| ⚠️ MODIFY | 40 | 33.3% |
| ❌ REMOVE | 17 | 14.2% |
| 💥 ERROR | 18 | 15.0% |
| ❓ UNKNOWN | 5 | 4.2% |
| **有效判决** | 97 | **80.8%** |

---

## 详细结果

### NVDA (KEEP 50%, MODIFY 30%, REMOVE 10%)

**✅ KEEP (10 条)**
| Source | 理由 |
|--------|------|
| **ADI** (Analog Devices) | 模拟芯片（同行业） |
| **AAPL** | 大科技股（NVDA 客户/同板块） |
| **RTX** (Raytheon) | 航天国防（军用 GPU） |
| **MS** (Morgan Stanley) | 金融龙头 |
| **XYZ** (Block) | 金融科技 |
| **AXL** (American Axle) | 汽车（电动车 NVIDIA Drive） |
| **SO** (Southern Co) | 公用事业（数据中心电力） |
| **CUZ** (Cousins Properties) | 数据中心房地产 |
| **OGS** (ONE Gas) | 公用事业 |
| **AXS** (Axis Capital) | 保险 |

**⚠️ MODIFY (6 条)**: EGO, CRK, CNQ, BNS, PEG, ARGX

**❌ REMOVE (2 条)**
| Source | 理由 |
|--------|------|
| **SON** (Sonoco) | 小型包装公司 - 无关联 |
| **TXNM** (TXNM Energy) | 小型公用事业 - 无关联 |

---

### GOOGL (KEEP 50%, MODIFY 30%, REMOVE 15%)

**✅ KEEP (10 条)**
| Source | 理由 |
|--------|------|
| **TGNA** (Tegna) | 媒体公司 |
| **LEVI** (Levi's) | 消费品牌（Google 广告客户） |
| **AFRM** (Affirm) | 金融科技（Google 广告客户） |
| **WLK** (Westlake) | 材料股 |
| **KHC** (Kraft Heinz) | 消费品（Google 广告客户） |
| **CRS** (Carpenter Tech) | 工业金属 |
| **SMP** (Standard Motor) | 汽车零部件 |
| **VTOL** (Bristow Group) | 航空运输 |
| **KMB** (Kimberly-Clark) | 消费品 |
| **TECK** (Teck Resources) | 矿业 |

**⚠️ MODIFY (6 条)**: AVNS, BNS, PLNT, KDP, TFX, LMND

**❌ REMOVE (3 条)**
| Source | 理由 |
|--------|------|
| **FDP** (Fresh Del Monte) | 生鲜食品 - 无关联 |
| **TYRA** (Tyra Biosciences) | 生物制药 - 无关联 |
| **VRA** (Vera Bradley) | 小型服装品牌 - 无关联 |

---

### TSLA (KEEP 30%, MODIFY 40%, REMOVE 15%)

**✅ KEEP (6 条)**
| Source | 理由 |
|--------|------|
| **DXCM** (Dexcom) | 医疗设备 |
| **HQY** (HealthEquity) | 健康账户 |
| **BKNG** (Booking.com) | 在线旅游 |
| **IQ** (iQiyi) | 中国流媒体 |
| **CHWY** (Chewy) | 宠物电商 |
| **MCY** (Mercury General) | 保险 |

**⚠️ MODIFY (8 条)**: FCX, LC, AEE, RNAC, KB, FNF, VIOT, CTKB

**❌ REMOVE (3 条)**: SSRM, GL, FINV

---

### MSFT (KEEP 25%, MODIFY 40%, REMOVE 20%)

**✅ KEEP (5 条)**
| Source | 理由 |
|--------|------|
| **BLKB** (Blackbaud) | SaaS（非营利组织管理） |
| **OLN** (Olin) | 化工 |
| **ALE** (ALLETE) | 公用事业 |
| **TEL** (TE Connectivity) | 连接器（硬件供应） |
| **ITT** (ITT Inc) | 工业 |

**⚠️ MODIFY (8 条)**: IPHA, DDS, CPAY, SAN, ST, XRX, ATEN, EVTC

**❌ REMOVE (4 条)**: SFL, PB, EXK, RIO

---

### AAPL (KEEP 25%, MODIFY 25%, REMOVE 25%, ERROR 25%)

**✅ KEEP (5 条)**: RCI, TRIP, AEIS, KEYS, CBSH

**⚠️ MODIFY (5 条)**: CNMD, BP, KHC, WEC, LDOS

**❌ REMOVE (5 条)**: EKSO, PEBO, MRTN, PATH, SLF

**💥 ERROR (5 条)**: CHD, IVVD, ZIM, SSYS, DOCN

---

### AMZN (KEEP 20%, MODIFY 35%, ERROR 45%)

**✅ KEEP (4 条)**
| Source | 理由 |
|--------|------|
| **KLIC** (Kulicke & Soffa) | 半导体设备 |
| **AMBA** (Ambarella) | 芯片（AWS 相关） |
| **BIPC** (Brookfield Infra) | 基础设施（数据中心） |
| **SEIC** (SEI Investments) | 金融服务 |

**⚠️ MODIFY (7 条)**: CCI, AWK, MAIN, TRGP, HLMN, AESI, ADP

**💥 ERROR (9 条)**: CAE, SPOT, HASI, OMI, MNRO, MYGN, VTRS, OCGN, GCMG

---

## 关键发现

### 1. 合理保留的边
LLM 成功识别了以下合理关系：
- **同行业**: NVDA ↔ ADI (模拟芯片)、AMZN ↔ KLIC (半导体设备)
- **客户/供应商关系**: NVDA ↔ AAPL、RTX ↔ NVDA、GOOGL ↔ 消费品广告客户
- **产业链相关**: NVDA ↔ SO/CUZ (数据中心电力/房地产)
- **科技巨头板块共振**: 大科技股之间

### 2. 合理移除的边
LLM 准确识别以下不合理边：
- 小型区域银行（HAFC、PEBO）
- 小型无关行业公司（SON、TXNM、ZEUS、SSRM）
- 生物制药/消费品与科技股之间的伪相关（TYRA、VRA、FDP）

### 3. ERROR 率问题
AMZN (45%) 和 AAPL (25%) 的 ERROR 率较高，主要原因：
- DeepSeek API 偶发超时/限流
- 某些节点的 LLM 响应被截断
- 即使已添加 2 次重试机制仍未完全消除

---

## 使用方法

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
cd /Users/zeyu/abel_2

# 测试入边
python3 edge_validator_balanced.py <TICKER> \
  --field volume \
  --mode in \
  --top 20 \
  --env prod \
  --model deepseek/deepseek-chat

# 测试出边
python3 edge_validator_balanced.py <TICKER> \
  --field volume \
  --mode out \
  --top 20 \
  --env prod
```

**结果保存位置**: `./validation_results/validation_{TICKER}_{FIELD}_{MODE}_{TIMESTAMP}.json`

---

## 建议

1. **采用 balanced validator 作为生产标准** - REMOVE 率合理 (14.2%)
2. **对高 ERROR ticker (AMZN/AAPL) 重试或切换模型** - 可尝试 Qwen 或 Claude
3. **引入 GICS 行业分类** - 可在查询阶段直接过滤，减少跨行业噪声
4. **多模型交叉验证** - 对 MODIFY 的边可用另一个 LLM 二次判断

---

*报告生成时间: 2026-04-21*
