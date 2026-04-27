#!/usr/bin/env python3
"""
Benchmark v2: Validator Accuracy with Wikidata Ground Truth
============================================================

Builds the labeled benchmark dataset PROGRAMMATICALLY from Wikidata
SPARQL queries. No hardcoded labels - everything comes from the
public Wikidata knowledge base maintained by the global community.

Ground truth sources:
1. **P452 (industry)**: Industry classification on Wikidata
2. **P749 (parent organization)** / **P355 (subsidiary)**:
   Corporate parent-subsidiary relationships (cleaner than P127/P1830
   which include passive institutional shareholdings like Vanguard/BlackRock)
3. **Different industry codes + no ownership relationship**: Negative pairs

Why this is more rigorous than v1:
- All labels come from Wikidata (community-maintained, not LLM-generated)
- Each Wikidata claim has source citations
- Fully programmatic and reproducible
- Independent of LLM training data

References:
- Wikidata SPARQL endpoint: https://query.wikidata.org
- Property P249 (ticker symbol): https://www.wikidata.org/wiki/Property:P249
- Property P452 (industry): https://www.wikidata.org/wiki/Property:P452
- Property P127 (owned by): https://www.wikidata.org/wiki/Property:P127
"""

import os
import sys
import json
import time
import requests
import random
from datetime import datetime
from collections import Counter, defaultdict

sys.path.insert(0, '/Users/zeyu/abel_2')
from edge_validator_balanced import EdgeValidatorBalanced


# ============================================================================
# WIKIDATA SPARQL CLIENT
# ============================================================================

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "AbelEdgeValidator/2.0 (https://github.com/Abel-ai-causality/cross-ticker-edge-validator)"


def sparql_query(query: str, timeout: int = 60) -> list:
    """Execute SPARQL query against Wikidata."""
    resp = requests.get(
        WIKIDATA_ENDPOINT,
        params={"query": query, "format": "json"},
        headers={"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["results"]["bindings"]


def get_value(binding, key, default=""):
    """Extract value from SPARQL binding."""
    return binding.get(key, {}).get("value", default)


def get_qid(binding, key):
    """Extract Q-id from a Wikidata URI binding."""
    val = get_value(binding, key, "")
    return val.split("/")[-1] if val else ""


# ============================================================================
# DATASET BUILDERS (all programmatic from Wikidata)
# ============================================================================

def fetch_us_listed_companies(limit: int = 200) -> list:
    """Fetch US-listed companies with ticker, industry, and Q-id from Wikidata."""
    query = f"""
    SELECT DISTINCT ?company ?companyLabel ?ticker ?industry ?industryLabel WHERE {{
      ?company p:P414 ?stmt .
      ?stmt ps:P414 ?exchange ;
            pq:P249 ?ticker .
      ?exchange wdt:P17 wd:Q30 .  # US-based exchange
      ?company wdt:P452 ?industry .
      FILTER(STRLEN(?ticker) <= 5)  # Standard ticker length
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" }}
    }}
    LIMIT {limit * 5}
    """
    print(f"📡 Fetching US-listed companies from Wikidata...")
    rows = sparql_query(query)

    # Group by (ticker, qid) - one company can have multiple industries
    companies = {}
    for r in rows:
        ticker = get_value(r, "ticker")
        qid = get_qid(r, "company")
        name = get_value(r, "companyLabel")
        industry_qid = get_qid(r, "industry")
        industry_label = get_value(r, "industryLabel")
        key = (ticker, qid)
        if key not in companies:
            companies[key] = {
                "ticker": ticker,
                "qid": qid,
                "name": name,
                "industries": []
            }
        companies[key]["industries"].append({
            "qid": industry_qid,
            "label": industry_label
        })

    result = list(companies.values())
    print(f"   ✓ Found {len(result)} unique US-listed companies with industry data")
    return result


def fetch_corporate_relationships(qids: list) -> dict:
    """Fetch corporate parent-subsidiary relationships from Wikidata.

    Properties used (cleaner than P127/P1830 which include passive shareholdings):
    - P749 (parent organization): A is a subsidiary of B
    - P355 (has subsidiary): A is the parent of B

    These are the cleanest signals for corporate hierarchy, excluding
    asset-manager institutional holdings (e.g., Vanguard owns 7% of NVDA).

    Returns: dict mapping company_qid -> set of related QIDs (any direction)
    """
    if not qids:
        return {}

    # Build VALUES clause
    values_clause = " ".join(f"wd:{q}" for q in qids)

    query = f"""
    SELECT ?source ?related ?prop WHERE {{
      VALUES ?source {{ {values_clause} }}
      VALUES ?prop {{ wdt:P749 wdt:P355 }}
      ?source ?prop ?related .
    }}
    """
    print(f"📡 Fetching corporate relationships for {len(qids)} companies...")
    try:
        rows = sparql_query(query, timeout=90)
    except Exception as e:
        print(f"   ⚠️  Query failed: {e}")
        return {}

    relationships = defaultdict(set)
    for r in rows:
        src_qid = get_qid(r, "source")
        rel_qid = get_qid(r, "related")
        if src_qid and rel_qid:
            relationships[src_qid].add(rel_qid)
            # Symmetric for our purposes (parent/subsidiary both create a link)
            relationships[rel_qid].add(src_qid)

    print(f"   ✓ Found {sum(len(v) for v in relationships.values())} relationships")
    return dict(relationships)


def build_positive_same_industry(companies: list, n_samples: int = 20) -> list:
    """Build positive pairs from companies sharing AT LEAST ONE industry Q-id."""
    # Index: industry_qid -> list of (ticker, qid, name)
    by_industry = defaultdict(list)
    for c in companies:
        for ind in c["industries"]:
            if ind["qid"]:
                by_industry[ind["qid"]].append(c)

    # Sample pairs
    pairs = []
    seen_pairs = set()
    industry_keys = list(by_industry.keys())
    random.seed(42)
    random.shuffle(industry_keys)

    for ind_qid in industry_keys:
        company_list = by_industry[ind_qid]
        if len(company_list) < 2:
            continue
        # Find the industry label for description
        ind_label = next((i["label"] for c in company_list
                         for i in c["industries"]
                         if i["qid"] == ind_qid), "?")
        # Pick pair within this industry
        for i in range(len(company_list)):
            for j in range(i + 1, len(company_list)):
                a = company_list[i]
                b = company_list[j]
                # Avoid same company different ticker
                if a["qid"] == b["qid"]:
                    continue
                # Use frozenset to avoid duplicates regardless of direction
                pair_key = frozenset([a["ticker"], b["ticker"]])
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)
                pairs.append({
                    "source": a["ticker"],
                    "target": b["ticker"],
                    "source_name": a["name"],
                    "target_name": b["name"],
                    "category": "same_industry",
                    "expected": "KEEP",
                    "label": f"Both in '{ind_label}' (Wikidata P452={ind_qid})",
                    "evidence": {
                        "type": "P452 (industry)",
                        "shared_industry_qid": ind_qid,
                        "shared_industry_label": ind_label,
                    }
                })
                if len(pairs) >= n_samples:
                    return pairs
    return pairs


def build_positive_corporate_relationship(companies: list, relationships: dict,
                                          n_samples: int = 10) -> list:
    """Build positive pairs from documented corporate ownership relationships."""
    qid_to_company = {c["qid"]: c for c in companies}
    pairs = []
    seen = set()

    for src_qid, rel_qids in relationships.items():
        if src_qid not in qid_to_company:
            continue
        src = qid_to_company[src_qid]
        for rel_qid in rel_qids:
            if rel_qid not in qid_to_company:
                continue
            tgt = qid_to_company[rel_qid]
            # Skip same ticker (e.g., dual listings of same company)
            if src["ticker"] == tgt["ticker"]:
                continue
            pair_key = frozenset([src["ticker"], tgt["ticker"]])
            if pair_key in seen:
                continue
            seen.add(pair_key)
            pairs.append({
                "source": src["ticker"],
                "target": tgt["ticker"],
                "source_name": src["name"],
                "target_name": tgt["name"],
                "category": "corporate_relationship",
                "expected": "KEEP",
                "label": "Documented corporate parent-subsidiary relationship "
                         "(Wikidata P749/P355)",
                "evidence": {
                    "type": "P749/P355 (parent-subsidiary)",
                    "source_qid": src_qid,
                    "target_qid": rel_qid,
                }
            })
            if len(pairs) >= n_samples:
                return pairs
    return pairs


def build_negative_unrelated(companies: list, relationships: dict,
                             positive_industry_qids: set,
                             n_samples: int = 20) -> list:
    """Build negative pairs: different industries + no ownership relationship.

    Stricter requirement: NO shared industry Q-id between the two companies.
    """
    pairs = []
    seen = set()
    random.seed(123)
    shuffled = companies.copy()
    random.shuffle(shuffled)

    attempts = 0
    max_attempts = len(shuffled) * 20

    while len(pairs) < n_samples and attempts < max_attempts:
        attempts += 1
        a = random.choice(shuffled)
        b = random.choice(shuffled)
        if a["qid"] == b["qid"]:
            continue
        pair_key = frozenset([a["ticker"], b["ticker"]])
        if pair_key in seen:
            continue

        # Must have NO shared industry Q-id
        a_inds = {i["qid"] for i in a["industries"] if i["qid"]}
        b_inds = {i["qid"] for i in b["industries"] if i["qid"]}
        if a_inds & b_inds:
            continue

        # Must have NO documented corporate relationship
        a_related = relationships.get(a["qid"], set())
        if b["qid"] in a_related:
            continue

        seen.add(pair_key)
        a_ind_label = next((i["label"] for i in a["industries"] if i["label"]),
                           "?")
        b_ind_label = next((i["label"] for i in b["industries"] if i["label"]),
                           "?")
        pairs.append({
            "source": a["ticker"],
            "target": b["ticker"],
            "source_name": a["name"],
            "target_name": b["name"],
            "category": "unrelated",
            "expected": "REMOVE",
            "label": f"No shared industry ('{a_ind_label}' vs '{b_ind_label}'), "
                     f"no documented corporate parent-subsidiary relationship",
            "evidence": {
                "type": "no shared P452, no P749/P355",
                "source_industries": list(a_inds),
                "target_industries": list(b_inds),
            }
        })

    return pairs


# ============================================================================
# RUNNER
# ============================================================================

def run_benchmark(n_per_category: dict = None):
    """Build dataset from Wikidata, run validator, compute metrics."""
    if n_per_category is None:
        n_per_category = {"same_industry": 20, "corporate": 10, "unrelated": 20}

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not set")
        sys.exit(1)

    # ==== Step 1: Fetch companies from Wikidata ====
    companies = fetch_us_listed_companies(limit=200)
    if not companies:
        print("❌ No companies fetched from Wikidata")
        sys.exit(1)

    # ==== Step 2: Fetch corporate relationships ====
    qids = [c["qid"] for c in companies]
    # Wikidata sometimes timeouts on large VALUES clauses; chunk it
    relationships = {}
    chunk_size = 50
    for i in range(0, len(qids), chunk_size):
        chunk = qids[i:i + chunk_size]
        chunk_rels = fetch_corporate_relationships(chunk)
        for k, v in chunk_rels.items():
            relationships.setdefault(k, set()).update(v)
        time.sleep(1)  # be polite to Wikidata

    # ==== Step 3: Build labeled pairs ====
    print(f"\n🔨 Building benchmark dataset...")
    pos_industry = build_positive_same_industry(
        companies, n_per_category["same_industry"]
    )
    pos_corp = build_positive_corporate_relationship(
        companies, relationships, n_per_category["corporate"]
    )

    positive_industry_qids = set()
    for p in pos_industry:
        positive_industry_qids.add(p["evidence"]["shared_industry_qid"])

    neg = build_negative_unrelated(
        companies, relationships, positive_industry_qids,
        n_per_category["unrelated"]
    )

    benchmark = pos_industry + pos_corp + neg
    print(f"   ✓ Same-industry: {len(pos_industry)}")
    print(f"   ✓ Corporate-relationship: {len(pos_corp)}")
    print(f"   ✓ Unrelated: {len(neg)}")
    print(f"   Total: {len(benchmark)} pairs")

    # ==== Step 4: Run validator ====
    validator = EdgeValidatorBalanced(
        openrouter_api_key=api_key,
        env="prod",
        model="anthropic/claude-sonnet-4-6",
    )

    print(f"\n{'='*70}")
    print(f"🧪 Running Edge Validator on {len(benchmark)} Wikidata-labeled pairs")
    print(f"{'='*70}\n")

    results = []
    for i, pair in enumerate(benchmark, 1):
        src = f"{pair['source']}_volume"
        tgt = f"{pair['target']}_volume"
        print(f"[{i}/{len(benchmark)}] {pair['category']}: "
              f"{pair['source']} ({pair['source_name'][:25]}) "
              f"→ {pair['target']} ({pair['target_name'][:25]})")
        print(f"  Expected: {pair['expected']} | {pair['label'][:80]}")

        try:
            result = validator.validate_edge(src, tgt)
            verdict = result.get('verdict', 'UNKNOWN')
            confidence = result.get('confidence', 0)
            reasoning = result.get('reasoning', '')[:200]
            match = (verdict == pair['expected'] or
                     (pair['expected'] == 'KEEP' and verdict == 'MODIFY'))
            pair_result = {
                **pair,
                "actual_verdict": verdict,
                "confidence": confidence,
                "reasoning": reasoning,
                "match": match,
            }
            results.append(pair_result)
            icon = "✅" if match else "❌"
            print(f"  {icon} Got: {verdict} ({confidence}%)")
        except Exception as e:
            print(f"  💥 Error: {e}")
            results.append({**pair, "actual_verdict": "ERROR",
                            "error": str(e), "match": False})
        print()

    return results


def compute_metrics(results):
    """Compute confusion matrix and metrics."""
    metrics = {}
    for strictness in ['strict', 'lenient']:
        tp = fp = tn = fn = 0
        for r in results:
            actual = r.get('actual_verdict', 'UNKNOWN')
            expected = r['expected']
            if strictness == 'strict':
                kept = actual == 'KEEP'
            else:
                kept = actual in ('KEEP', 'MODIFY')

            if expected == 'KEEP':
                if kept:
                    tp += 1
                else:
                    fn += 1
            else:
                if kept:
                    fp += 1
                else:
                    tn += 1

        total = tp + fp + tn + fn
        accuracy = (tp + tn) / total if total > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) \
            if (precision + recall) > 0 else 0
        metrics[strictness] = {
            "tp": tp, "fp": fp, "tn": tn, "fn": fn, "total": total,
            "accuracy": accuracy, "precision": precision,
            "recall": recall, "specificity": specificity, "f1": f1,
        }

    by_category = {}
    for cat in ['same_industry', 'corporate_relationship', 'unrelated']:
        cat_results = [r for r in results if r['category'] == cat]
        if not cat_results:
            continue
        cat_correct = sum(1 for r in cat_results if r.get('match'))
        by_category[cat] = {
            "total": len(cat_results),
            "correct": cat_correct,
            "accuracy": cat_correct / len(cat_results),
            "verdict_distribution": dict(Counter(
                r.get('actual_verdict', 'UNKNOWN') for r in cat_results
            ))
        }
    return metrics, by_category


def main():
    results = run_benchmark()
    metrics, by_category = compute_metrics(results)

    # Print summary
    print(f"\n{'='*70}")
    print(f"📊 BENCHMARK RESULTS (Wikidata Ground Truth)")
    print(f"{'='*70}")

    for mode in ['strict', 'lenient']:
        m = metrics[mode]
        print(f"\n--- {mode.upper()} ({'KEEP only' if mode=='strict' else 'KEEP+MODIFY'}) ---")
        print(f"  Accuracy:    {m['accuracy']*100:.1f}%")
        print(f"  Precision:   {m['precision']*100:.1f}%")
        print(f"  Recall:      {m['recall']*100:.1f}%")
        print(f"  Specificity: {m['specificity']*100:.1f}%")
        print(f"  F1:          {m['f1']*100:.1f}%")
        print(f"  TP={m['tp']}, FP={m['fp']}, TN={m['tn']}, FN={m['fn']}")

    print(f"\n--- PER-CATEGORY ---")
    for cat, info in by_category.items():
        print(f"\n  {cat} (n={info['total']}, acc={info['accuracy']*100:.1f}%):")
        for v, n in info['verdict_distribution'].items():
            print(f"    {v}: {n}")

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "metadata": {
            "timestamp": timestamp,
            "model": "anthropic/claude-sonnet-4-6",
            "ground_truth_source": "Wikidata SPARQL (P452 industry, P749/P355 parent-subsidiary)",
            "wikidata_endpoint": WIKIDATA_ENDPOINT,
            "total_pairs": len(results),
        },
        "metrics": metrics,
        "by_category": by_category,
        "detailed_results": results,
    }
    out_path = f"/Users/zeyu/abel_2/validation_results/benchmark_wikidata_{timestamp}.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n💾 Saved: {out_path}")
    return output


if __name__ == "__main__":
    main()
