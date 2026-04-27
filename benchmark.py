#!/usr/bin/env python3
"""
Benchmark: Validator Accuracy Test
==================================

Tests the edge validator against a labeled dataset built from public sources:
1. GICS Sub-Industry classifications (S&P public standard)
2. Apple's published supplier list (apple.com/supplier-list)
3. NVIDIA's known customers (from public 10-K filings, earnings calls)
4. Classic pair-trading literature (Gatev et al. 2006)

For each labeled pair, we run the validator and compare its verdict against
the expected ground truth, computing precision, recall, F1, and a full
confusion matrix.

Expected behavior:
- Same GICS Sub-Industry pairs: KEEP (high recall = sensitivity)
- Known supplier-customer pairs: KEEP (validator should recognize concrete
  business relationships)
- Cross-sector unrelated pairs: REMOVE (high specificity)
"""

import os
import sys
import json
import time
from datetime import datetime
from collections import Counter

sys.path.insert(0, '/Users/zeyu/abel_2')
from edge_validator_balanced import EdgeValidatorBalanced


# ============================================================================
# BENCHMARK DATASET (all from public sources)
# ============================================================================

# Category 1: Same GICS Sub-Industry pairs (expected KEEP)
# Source: S&P GICS classifications, publicly available on Wikipedia
SAME_INDUSTRY_PAIRS = [
    # Semiconductors (GICS: 45301020)
    ("NVDA", "AMD", "Same GICS: Semiconductors"),
    ("NVDA", "INTC", "Same GICS: Semiconductors"),
    ("NVDA", "MU", "Same GICS: Semiconductors"),
    ("AMD", "QCOM", "Same GICS: Semiconductors"),
    ("INTC", "QCOM", "Same GICS: Semiconductors"),

    # Diversified Banks (GICS: 40101010)
    ("JPM", "BAC", "Same GICS: Diversified Banks"),
    ("JPM", "WFC", "Same GICS: Diversified Banks"),
    ("BAC", "C", "Same GICS: Diversified Banks"),

    # Integrated Oil & Gas (GICS: 10102010)
    ("XOM", "CVX", "Same GICS: Integrated Oil & Gas"),
    ("XOM", "COP", "Same GICS: Integrated Oil & Gas"),

    # Soft Drinks (GICS: 30201030)
    ("KO", "PEP", "Same GICS: Soft Drinks"),

    # Hypermarkets/Retail (GICS: 30101040)
    ("WMT", "COST", "Same GICS: Hypermarkets & Super Centers"),

    # Transaction & Payment Processing (GICS: 45102030)
    ("V", "MA", "Same GICS: Transaction & Payment Processing"),

    # Automobile Manufacturers (GICS: 25102010)
    ("F", "GM", "Same GICS: Automobile Manufacturers"),

    # Managed Health Care (GICS: 35102030)
    ("UNH", "CI", "Same GICS: Managed Health Care"),
    ("UNH", "ELV", "Same GICS: Managed Health Care"),

    # Drug Retail (GICS: 30101010)
    ("CVS", "WBA", "Same GICS: Drug Retail"),

    # Application Software (similar segments)
    ("UBER", "LYFT", "Same business: Ride-sharing apps"),

    # Hotels/Online Travel
    ("BKNG", "ABNB", "Similar GICS: Hotels & Travel"),

    # Beverage - Alcoholic
    ("BUD", "TAP", "Same GICS: Brewers"),
]

# Category 2: Known Supplier-Customer / Direct Business Relationships (expected KEEP)
# Source: Apple 10-K, NVIDIA 10-K, public earnings calls, supplier lists
SUPPLY_CHAIN_PAIRS = [
    # NVIDIA's foundry partners
    ("NVDA", "TSM", "TSMC fabricates NVIDIA's GPUs (public 10-K)"),
    ("AMD", "TSM", "TSMC fabricates AMD's chips (public 10-K)"),
    ("AAPL", "TSM", "TSMC fabricates Apple Silicon (public 10-K)"),

    # NVIDIA's major hyperscale customers
    ("NVDA", "MSFT", "MSFT Azure major NVIDIA customer (earnings calls)"),
    ("NVDA", "GOOGL", "Google Cloud/DeepMind major NVIDIA customer"),
    ("NVDA", "AMZN", "AWS major NVIDIA customer (earnings calls)"),
    ("NVDA", "META", "Meta major NVIDIA customer for AI training"),

    # Apple suppliers (apple.com/supplier-list)
    ("AAPL", "AVGO", "Broadcom supplies WiFi/BT chips for iPhone"),
    ("AAPL", "QCOM", "Qualcomm supplies modems for iPhone"),

    # Tesla battery supplier
    ("TSLA", "ALB", "Albemarle supplies lithium to Tesla"),
]

# Category 3: Cross-Sector Unrelated Pairs (expected REMOVE)
# Different GICS sectors, no known business overlap
UNRELATED_PAIRS = [
    # Tech vs Consumer Staples
    ("NVDA", "KO", "Chip vs Soda - no business link"),
    ("MSFT", "PEP", "Software vs Beverage - no business link"),
    ("GOOGL", "PG", "Search vs Consumer goods - no business link"),

    # Tech vs Energy
    ("AAPL", "XOM", "Consumer electronics vs Oil major"),
    ("META", "CVX", "Social media vs Oil major"),

    # Tech vs Industrial (heavy)
    ("AMZN", "CAT", "E-commerce vs Heavy construction equipment"),
    ("NFLX", "DE", "Streaming vs Agricultural equipment"),

    # Tech vs Healthcare/Pharma (different)
    ("AAPL", "PFE", "Consumer electronics vs Pharma"),
    ("META", "JNJ", "Social media vs Pharma"),

    # Retail vs Defense/Aerospace
    ("WMT", "LMT", "Discount retail vs Defense"),
    ("COST", "RTX", "Warehouse retail vs Defense electronics"),

    # Fast food vs Tech
    ("MCD", "NVDA", "Fast food vs Semiconductor"),
    ("SBUX", "AMD", "Coffee vs Semiconductor"),

    # Small unrelated companies (likely true noise)
    ("HAFC", "NVDA", "Small regional bank (Korean-American) vs NVIDIA"),
    ("MOFG", "AAPL", "Iowa community bank vs Apple"),
    ("LITB", "MSFT", "Chinese e-commerce SMB vs Microsoft"),
    ("ZEUS", "GOOGL", "Olympic Steel vs Google"),
    ("TWI", "TSLA", "Titan Tires (agriculture) vs Tesla"),
    ("BEAM", "AMZN", "Gene editing biotech vs Amazon"),
    ("EXEL", "NVDA", "Cancer therapeutics biotech vs NVIDIA"),
]


# ============================================================================
# BENCHMARK RUNNER
# ============================================================================

def run_benchmark():
    """Execute benchmark and compute metrics."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not set")
        sys.exit(1)

    validator = EdgeValidatorBalanced(
        openrouter_api_key=api_key,
        env="prod",
        model="anthropic/claude-sonnet-4-6",
        output_dir="./validation_results"
    )

    # Build full benchmark dataset
    benchmark = []
    for src, tgt, label in SAME_INDUSTRY_PAIRS:
        benchmark.append({
            "source": src, "target": tgt, "category": "same_industry",
            "expected": "KEEP", "label": label
        })
    for src, tgt, label in SUPPLY_CHAIN_PAIRS:
        benchmark.append({
            "source": src, "target": tgt, "category": "supply_chain",
            "expected": "KEEP", "label": label
        })
    for src, tgt, label in UNRELATED_PAIRS:
        benchmark.append({
            "source": src, "target": tgt, "category": "unrelated",
            "expected": "REMOVE", "label": label
        })

    print(f"=" * 70)
    print(f"🧪 Benchmark Test - Edge Validator Accuracy")
    print(f"=" * 70)
    print(f"Model: anthropic/claude-sonnet-4-6")
    print(f"Total pairs: {len(benchmark)}")
    print(f"  Same Industry: {len(SAME_INDUSTRY_PAIRS)} (expected KEEP)")
    print(f"  Supply Chain: {len(SUPPLY_CHAIN_PAIRS)} (expected KEEP)")
    print(f"  Unrelated: {len(UNRELATED_PAIRS)} (expected REMOVE)")
    print(f"=" * 70)

    # Run validator on each pair
    results = []
    for i, pair in enumerate(benchmark, 1):
        src = f"{pair['source']}_volume"
        tgt = f"{pair['target']}_volume"

        print(f"\n[{i}/{len(benchmark)}] {pair['category']}: "
              f"{pair['source']} → {pair['target']}")
        print(f"  Expected: {pair['expected']} ({pair['label']})")

        try:
            result = validator.validate_edge(src, tgt)
            verdict = result.get('verdict', 'UNKNOWN')
            confidence = result.get('confidence', 0)
            reasoning = result.get('reasoning', '')[:150]

            pair_result = {
                **pair,
                "actual_verdict": verdict,
                "confidence": confidence,
                "reasoning": reasoning,
                "match": verdict == pair['expected'] or
                       (pair['expected'] == 'KEEP' and verdict == 'MODIFY')
            }
            results.append(pair_result)

            icon = "✅" if pair_result['match'] else "❌"
            print(f"  {icon} Got: {verdict} ({confidence}%) - {reasoning[:100]}")
        except Exception as e:
            print(f"  💥 Error: {e}")
            pair_result = {**pair, "actual_verdict": "ERROR",
                           "error": str(e), "match": False}
            results.append(pair_result)

    return results


def compute_metrics(results):
    """Compute confusion matrix and metrics."""
    # Define what counts as "correct"
    # For positive (expected KEEP): KEEP or MODIFY count as correct identification
    # For negative (expected REMOVE): REMOVE counts as correct rejection

    # Strict metrics: exact match only
    # Lenient metrics: KEEP/MODIFY both accepted as "kept"
    metrics = {}

    for strictness in ['strict', 'lenient']:
        tp = fp = tn = fn = 0
        for r in results:
            actual = r.get('actual_verdict', 'UNKNOWN')
            expected = r['expected']

            if strictness == 'strict':
                kept = actual == 'KEEP'
            else:  # lenient
                kept = actual in ('KEEP', 'MODIFY')

            if expected == 'KEEP':
                if kept:
                    tp += 1
                else:
                    fn += 1
            else:  # expected REMOVE
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

    # Per-category breakdown
    by_category = {}
    for cat in ['same_industry', 'supply_chain', 'unrelated']:
        cat_results = [r for r in results if r['category'] == cat]
        cat_correct = sum(1 for r in cat_results if r.get('match'))
        by_category[cat] = {
            "total": len(cat_results),
            "correct": cat_correct,
            "accuracy": cat_correct / len(cat_results) if cat_results else 0,
            "verdict_distribution": Counter(
                r.get('actual_verdict', 'UNKNOWN') for r in cat_results
            )
        }

    return metrics, by_category


def main():
    results = run_benchmark()
    metrics, by_category = compute_metrics(results)

    # Print summary
    print(f"\n{'='*70}")
    print(f"📊 BENCHMARK RESULTS")
    print(f"{'='*70}")

    print(f"\n--- STRICT METRICS (KEEP only counts as positive) ---")
    s = metrics['strict']
    print(f"  Accuracy:     {s['accuracy']*100:.1f}%")
    print(f"  Precision:    {s['precision']*100:.1f}%")
    print(f"  Recall (TPR): {s['recall']*100:.1f}%")
    print(f"  Specificity:  {s['specificity']*100:.1f}%")
    print(f"  F1 Score:     {s['f1']*100:.1f}%")
    print(f"  Confusion: TP={s['tp']}, FP={s['fp']}, TN={s['tn']}, FN={s['fn']}")

    print(f"\n--- LENIENT METRICS (KEEP/MODIFY both count as positive) ---")
    l = metrics['lenient']
    print(f"  Accuracy:     {l['accuracy']*100:.1f}%")
    print(f"  Precision:    {l['precision']*100:.1f}%")
    print(f"  Recall (TPR): {l['recall']*100:.1f}%")
    print(f"  Specificity:  {l['specificity']*100:.1f}%")
    print(f"  F1 Score:     {l['f1']*100:.1f}%")
    print(f"  Confusion: TP={l['tp']}, FP={l['fp']}, TN={l['tn']}, FN={l['fn']}")

    print(f"\n--- PER-CATEGORY BREAKDOWN ---")
    for cat, data in by_category.items():
        print(f"\n  {cat} ({data['total']} pairs, "
              f"{data['accuracy']*100:.1f}% accuracy):")
        for v, n in data['verdict_distribution'].items():
            print(f"    {v}: {n}")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "metadata": {
            "timestamp": timestamp,
            "model": "anthropic/claude-sonnet-4-6",
            "total_pairs": len(results),
            "categories": {
                "same_industry": len(SAME_INDUSTRY_PAIRS),
                "supply_chain": len(SUPPLY_CHAIN_PAIRS),
                "unrelated": len(UNRELATED_PAIRS),
            }
        },
        "metrics": metrics,
        "by_category": {
            k: {**v, "verdict_distribution": dict(v["verdict_distribution"])}
            for k, v in by_category.items()
        },
        "detailed_results": results,
    }

    output_file = f"/Users/zeyu/abel_2/validation_results/benchmark_{timestamp}.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {output_file}")
    return output


if __name__ == "__main__":
    main()
