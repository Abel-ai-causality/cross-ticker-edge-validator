#!/usr/bin/env python3
"""
Cross-Ticker Edge Validator Agent

Validate the reasonableness of causal edges between two tickers.
Extract edges and context from Neo4j, use Claude 4.6 (Sonnet) to judge edge validity.
"""

import os
import sys
import json
import requests
from typing import Optional
from dataclasses import dataclass

# Add abel-triple-fusion to path to use its environment
sys.path.insert(0, '/Users/zeyu/abel/abel-triple-fusion')
from app.core.config import get_config
from neo4j import GraphDatabase


@dataclass
class EdgeValidationResult:
    """Edge validation result"""
    source: str
    target: str
    relationship: str
    action: str  # KEEP, REMOVE, MODIFY
    reason: str
    confidence: float
    suggestions: Optional[str] = None


class ClaudeClient:
    """Simple Claude API client (using requests)"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-sonnet-4-6"  # Claude Sonnet 4.6

    def create_message(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
        """Send message to Claude"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        return data["content"][0]["text"]


class CrossTickerEdgeValidator:
    """Cross-Ticker Edge Validation Agent"""

    def __init__(
        self,
        neo4j_uri: str = "neo4j://10.16.176.189:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "eY6WaJ9OZYTLvwlW7cDqle1d2",
        anthropic_api_key: Optional[str] = None,
    ):
        # Neo4j connection
        self.neo4j_driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password),
            connection_acquisition_timeout=15
        )

        # Claude client
        api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API Key is required")
        self.claude = ClaudeClient(api_key=api_key)

    def close(self):
        """Close connections"""
        self.neo4j_driver.close()

    def get_node_by_name(self, name: str) -> Optional[dict]:
        """Get node by specified name"""
        with self.neo4j_driver.session(database='neo4j') as session:
            result = session.run("""
                MATCH (n:CausalNodeV2 {name: $name})
                RETURN n.name as name, n.id as id, n.description as description,
                       n.full_name as full_name, n.in_reach_1 as in_reach_1,
                       n.out_reach_1 as out_reach_1
                LIMIT 1
            """, name=name)
            record = result.single()
            return dict(record) if record else None

    def get_edge_between(self, source_name: str, target_name: str) -> Optional[dict]:
        """Get edge between two nodes"""
        with self.neo4j_driver.session(database='neo4j') as session:
            result = session.run("""
                MATCH (a:CausalNodeV2 {name: $source})-[r]-(b:CausalNodeV2 {name: $target})
                RETURN type(r) as rel_type, r.weight as weight, r.tau as tau,
                       startNode(r).name as from_node, endNode(r).name as to_node
                LIMIT 1
            """, source=source_name, target=target_name)
            record = result.single()
            return dict(record) if record else None

    def get_node_neighbors(self, node_name: str, limit: int = 10) -> dict:
        """Get node neighbors (incoming and outgoing edges)"""
        with self.neo4j_driver.session(database='neo4j') as session:
            # Outgoing edges
            out_result = session.run("""
                MATCH (n:CausalNodeV2 {name: $name})-[r]->(other)
                RETURN other.name as target, type(r) as rel, r.weight as weight, r.tau as tau
                ORDER BY abs(r.tau) DESC
                LIMIT $limit
            """, name=node_name, limit=limit)
            out_edges = [dict(r) for r in out_result]

            # Incoming edges
            in_result = session.run("""
                MATCH (other)-[r]->(n:CausalNodeV2 {name: $name})
                RETURN other.name as source, type(r) as rel, r.weight as weight, r.tau as tau
                ORDER BY abs(r.tau) DESC
                LIMIT $limit
            """, name=node_name, limit=limit)
            in_edges = [dict(r) for r in in_result]

            return {"out_edges": out_edges, "in_edges": in_edges}

    def build_validation_prompt(
        self,
        source_node: dict,
        target_node: dict,
        edge: dict,
        source_context: dict,
        target_context: dict
    ) -> str:
        """Build LLM validation prompt"""

        prompt = f"""You are a financial causality expert. Your task is to evaluate whether a causal edge between two financial tickers is logically reasonable or just statistical correlation.

## Source Node
- Name: {source_node.get('name')}
- Full Name: {source_node.get('full_name')}
- Description: {source_node.get('description', 'N/A')}

## Target Node
- Name: {target_node.get('name')}
- Full Name: {target_node.get('full_name')}
- Description: {target_node.get('description', 'N/A')}

## The Edge to Validate
- Direction: {edge.get('from_node')} -> {edge.get('to_node')}
- Relationship Type: {edge.get('rel_type')}
- Statistical Weight: {edge.get('weight')}
- Time Lag (tau): {edge.get('tau')} days

## Source Node Context (Top Connections)
Outgoing edges:
"""
        for e in source_context['out_edges'][:5]:
            prompt += f"  - {e['target']}: {e['rel']}, tau={e['tau']}, weight={e['weight']:.4f}\n"

        prompt += f"""
Incoming edges:
"""
        for e in source_context['in_edges'][:5]:
            prompt += f"  - {e['source']}: {e['rel']}, tau={e['tau']}, weight={e['weight']:.4f}\n"

        prompt += f"""
## Target Node Context (Top Connections)
Outgoing edges:
"""
        for e in target_context['out_edges'][:5]:
            prompt += f"  - {e['target']}: {e['rel']}, tau={e['tau']}, weight={e['weight']:.4f}\n"

        prompt += f"""
Incoming edges:
"""
        for e in target_context['in_edges'][:5]:
            prompt += f"  - {e['source']}: {e['rel']}, tau={e['tau']}, weight={e['weight']:.4f}\n"

        prompt += """
## Your Task
Evaluate whether this causal edge is REASONABLE based on:
1. Business/domain logic (does the relationship make economic sense?)
2. Industry knowledge (are these sectors related?)
3. The statistical evidence vs. potential spurious correlation

Respond in JSON format:
{
  "action": "KEEP|REMOVE|MODIFY",
  "confidence": 0.0-1.0,
  "reason": "detailed explanation of your reasoning",
  "suggestions": "if MODIFY, suggest what the relationship should be"
}

Guidelines:
- KEEP: The edge represents a genuine causal relationship
- REMOVE: The edge is spurious correlation with no logical basis
- MODIFY: The edge has some validity but wrong direction or relationship type
"""
        return prompt

    def validate_edge(
        self,
        source_ticker: str,
        target_ticker: str,
        source_field: str = "close_price",
        target_field: str = "close_price"
    ) -> EdgeValidationResult:
        """
        Validate edge between two tickers

        Args:
            source_ticker: Source ticker (e.g., "SSTK")
            target_ticker: Target ticker (e.g., "ETHUSD")
            source_field: Field name (default "close_price")
            target_field: Field name (default "close_price")
        """
        # Build full node names
        source_name = f"{source_ticker}_{source_field}"
        target_name = f"{target_ticker}_{target_field}"

        print(f"🔍 Finding nodes: {source_name} and {target_name}")

        # Get node info
        source_node = self.get_node_by_name(source_name)
        target_node = self.get_node_by_name(target_name)

        if not source_node:
            return EdgeValidationResult(
                source=source_name,
                target=target_name,
                relationship="N/A",
                action="ERROR",
                reason=f"Source node {source_name} not found in graph",
                confidence=0.0
            )

        if not target_node:
            return EdgeValidationResult(
                source=source_name,
                target=target_name,
                relationship="N/A",
                action="ERROR",
                reason=f"Target node {target_name} not found in graph",
                confidence=0.0
            )

        print(f"✅ Found nodes: {source_node.get('name')} <-> {target_node.get('name')}")

        # Get edge info
        edge = self.get_edge_between(source_name, target_name)

        if not edge:
            return EdgeValidationResult(
                source=source_name,
                target=target_name,
                relationship="NONE",
                action="NO_EDGE",
                reason="No direct edge found between these nodes",
                confidence=1.0
            )

        print(f"✅ Found edge: {edge.get('from_node')} -[{edge.get('rel_type')}]-> {edge.get('to_node')} (tau={edge.get('tau')}, weight={edge.get('weight')})")

        # Get context
        print("📊 Extracting node context...")
        source_context = self.get_node_neighbors(source_name, limit=10)
        target_context = self.get_node_neighbors(target_name, limit=10)

        # Build prompt
        prompt = self.build_validation_prompt(
            source_node, target_node, edge, source_context, target_context
        )

        # Call Claude
        print("🤖 Calling Claude for validation...")
        try:
            response_text = self.claude.create_message(prompt, max_tokens=2000, temperature=0.2)

            # Parse response
            content = response_text
            # Extract JSON
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result_json = json.loads(content[json_start:json_end])
            else:
                result_json = json.loads(content)

            return EdgeValidationResult(
                source=edge.get('from_node'),
                target=edge.get('to_node'),
                relationship=edge.get('rel_type'),
                action=result_json.get('action', 'UNKNOWN'),
                reason=result_json.get('reason', 'No reason provided'),
                confidence=result_json.get('confidence', 0.5),
                suggestions=result_json.get('suggestions')
            )

        except Exception as e:
            return EdgeValidationResult(
                source=edge.get('from_node'),
                target=edge.get('to_node'),
                relationship=edge.get('rel_type'),
                action="ERROR",
                reason=f"Failed to parse LLM response: {str(e)}",
                confidence=0.0
            )

    def print_result(self, result: EdgeValidationResult):
        """Print validation result"""
        print("\n" + "=" * 60)
        print("🎯 EDGE VALIDATION RESULT")
        print("=" * 60)
        print(f"Source:      {result.source}")
        print(f"Target:      {result.target}")
        print(f"Relation:    {result.relationship}")
        print(f"Action:      {result.action}")
        print(f"Confidence:  {result.confidence:.2%}")
        print(f"\nReason:\n{result.reason}")
        if result.suggestions:
            print(f"\nSuggestions:\n{result.suggestions}")
        print("=" * 60)


    def get_all_outgoing_edges(self, ticker: str, field: str = "close_price", limit: int = 50) -> list[dict]:
        """Get all outgoing edges for specified ticker"""
        node_name = f"{ticker}_{field}"
        with self.neo4j_driver.session(database='neo4j') as session:
            result = session.run("""
                MATCH (n:CausalNodeV2 {name: $name})-[r]->(other)
                RETURN n.name as source, other.name as target, type(r) as rel,
                       r.weight as weight, r.tau as tau,
                       other.description as target_desc, other.full_name as target_full
                ORDER BY abs(r.tau) DESC
                LIMIT $limit
            """, name=node_name, limit=limit)
            return [dict(r) for r in result]

    def get_all_incoming_edges(self, ticker: str, field: str = "close_price", limit: int = 50) -> list[dict]:
        """Get all incoming edges for specified ticker"""
        node_name = f"{ticker}_{field}"
        with self.neo4j_driver.session(database='neo4j') as session:
            result = session.run("""
                MATCH (other)-[r]->(n:CausalNodeV2 {name: $name})
                RETURN other.name as source, n.name as target, type(r) as rel,
                       r.weight as weight, r.tau as tau,
                       other.description as source_desc, other.full_name as source_full
                ORDER BY abs(r.tau) DESC
                LIMIT $limit
            """, name=node_name, limit=limit)
            return [dict(r) for r in result]

    def validate_single_ticker_edges(
        self,
        ticker: str,
        mode: str = "out",  # "out" or "in"
        top_n: int = 10,
        field: str = "close_price"
    ) -> list[EdgeValidationResult]:
        """
        Batch validate all edges for a single ticker

        Args:
            ticker: Ticker to validate (e.g., "NVDA")
            mode: "out" for outgoing edges, "in" for incoming edges
            top_n: Validate top N edges (sorted by abs(tau))
            field: Field name
        """
        results = []

        if mode == "out":
            edges = self.get_all_outgoing_edges(ticker, field, limit=top_n)
            print(f"📤 {ticker} outgoing edges (Top {len(edges)}):")
        else:
            edges = self.get_all_incoming_edges(ticker, field, limit=top_n)
            print(f"📥 {ticker} incoming edges (Top {len(edges)}):")

        if not edges:
            print(f"  No {'outgoing' if mode == 'out' else 'incoming'} edges found for {ticker}")
            return results

        # Print overview
        for i, e in enumerate(edges[:5], 1):
            direction = f"{e['source']} -> {e['target']}"
            print(f"  {i}. {direction} (tau={e['tau']}, weight={e['weight']:.4f})")

        print(f"\nStarting validation of top {min(top_n, len(edges))} edges...\n")

        # Validate each edge
        for i, edge in enumerate(edges[:top_n], 1):
            print(f"[{i}/{min(top_n, len(edges))}] Validating: {edge['source']} -> {edge['target']}")

            # Get node info
            source_node = self.get_node_by_name(edge['source'])
            target_node = self.get_node_by_name(edge['target'])

            if not source_node or not target_node:
                print(f"  ⚠️  Cannot get node info, skipping")
                continue

            # Get context
            source_context = self.get_node_neighbors(edge['source'], limit=5)
            target_context = self.get_node_neighbors(edge['target'], limit=5)

            # Build prompt
            edge_info = {
                'from_node': edge['source'],
                'to_node': edge['target'],
                'rel_type': edge['rel'],
                'weight': edge['weight'],
                'tau': edge['tau']
            }

            prompt = self.build_validation_prompt(
                source_node, target_node, edge_info, source_context, target_context
            )

            # Call Claude
            try:
                response_text = self.claude.create_message(prompt, max_tokens=1500, temperature=0.2)

                # Parse JSON
                content = response_text
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    result_json = json.loads(content[json_start:json_end])
                else:
                    result_json = json.loads(content)

                result = EdgeValidationResult(
                    source=edge['source'],
                    target=edge['target'],
                    relationship=edge['rel'],
                    action=result_json.get('action', 'UNKNOWN'),
                    reason=result_json.get('reason', 'No reason')[:100] + "...",
                    confidence=result_json.get('confidence', 0.5)
                )
                results.append(result)

                action_emoji = {"KEEP": "✅", "REMOVE": "❌", "MODIFY": "⚠️"}.get(result.action, "❓")
                print(f"  {action_emoji} {result.action} (confidence: {result.confidence:.0%})")

            except Exception as e:
                print(f"  ❌ Validation failed: {str(e)[:50]}")
                results.append(EdgeValidationResult(
                    source=edge['source'],
                    target=edge['target'],
                    relationship=edge['rel'],
                    action="ERROR",
                    reason=str(e)[:100],
                    confidence=0.0
                ))

        return results

    def print_batch_summary(self, ticker: str, mode: str, results: list[EdgeValidationResult]):
        """Print batch validation results summary"""
        print("\n" + "=" * 70)
        print(f"📊 {ticker} {'outgoing' if mode == 'out' else 'incoming'} edges validation summary")
        print("=" * 70)

        if not results:
            print("No validation results")
            return

        # Statistics
        keep = sum(1 for r in results if r.action == "KEEP")
        remove = sum(1 for r in results if r.action == "REMOVE")
        modify = sum(1 for r in results if r.action == "MODIFY")
        error = sum(1 for r in results if r.action in ["ERROR", "UNKNOWN"])

        print(f"\nTotal: {len(results)} edges")
        print(f"  ✅ KEEP:    {keep} ({keep/len(results):.0%})")
        print(f"  ❌ REMOVE:  {remove} ({remove/len(results):.0%})")
        print(f"  ⚠️  MODIFY:  {modify} ({modify/len(results):.0%})")
        print(f"  ❓ ERROR:   {error} ({error/len(results):.0%})")

        # List suspicious edges (REMOVE)
        if remove > 0:
            print(f"\n🔍 Recommended suspicious edges to remove:")
            for r in results:
                if r.action == "REMOVE":
                    print(f"  ❌ {r.source[:25]:25} -> {r.target[:25]:25} ({r.confidence:.0%})")

        # List high confidence KEEP
        high_conf_keep = [r for r in results if r.action == "KEEP" and r.confidence > 0.8]
        if high_conf_keep:
            print(f"\n✅ High confidence reasonable edges:")
            for r in high_conf_keep[:5]:
                print(f"  ✅ {r.source[:25]:25} -> {r.target[:25]:25} ({r.confidence:.0%})")

        print("=" * 70)


def main():
    """Main function - example usage"""
    import argparse

    parser = argparse.ArgumentParser(description="Cross-Ticker Edge Validator")
    parser.add_argument("ticker", help="Ticker to analyze (e.g., NVDA)")
    parser.add_argument("--target", help="Target ticker for single edge validation (optional)")
    parser.add_argument("--mode", choices=["out", "in"], default="out",
                       help="Mode: 'out' for outgoing edges, 'in' for incoming edges")
    parser.add_argument("--top", type=int, default=10, help="Number of top edges to validate")
    parser.add_argument("--api-key", help="Anthropic API Key (or set ANTHROPIC_API_KEY env var)")

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Please provide Anthropic API Key:")
        print("   Option 1: Set ANTHROPIC_API_KEY environment variable")
        print("   Option 2: Use --api-key parameter")
        sys.exit(1)

    # Create validator
    validator = CrossTickerEdgeValidator(
        anthropic_api_key=api_key,
        neo4j_uri="neo4j://10.16.176.189:7687",
        neo4j_user="neo4j",
        neo4j_password="eY6WaJ9OZYTLvwlW7cDqle1d2"
    )

    try:
        if args.target:
            # Single edge validation mode
            print(f"\n🔎 Validating single edge: {args.ticker} -> {args.target}")
            result = validator.validate_edge(args.ticker, args.target)
            validator.print_result(result)
        else:
            # Batch single-ticker validation mode
            print(f"\n🔎 Batch validating {args.ticker} {'outgoing' if args.mode == 'out' else 'incoming'} edges (Top {args.top})")
            results = validator.validate_single_ticker_edges(
                ticker=args.ticker,
                mode=args.mode,
                top_n=args.top
            )
            validator.print_batch_summary(args.ticker, args.mode, results)

    finally:
        validator.close()


if __name__ == "__main__":
    main()
