#!/usr/bin/env python3
"""
Cross-Ticker Edge Validator Agent

验证两个 ticker 之间因果边的合理性。
使用 Neo4j 提取边和上下文，用 Claude 4.6 (Sonnet) 判断边是否合理。
"""

import os
import sys
import json
import requests
from typing import Optional
from dataclasses import dataclass

# 添加 abel-triple-fusion 到路径以使用其环境
sys.path.insert(0, '/Users/zeyu/abel/abel-triple-fusion')
from app.core.config import get_config
from neo4j import GraphDatabase


@dataclass
class EdgeValidationResult:
    """边验证结果"""
    source: str
    target: str
    relationship: str
    action: str  # KEEP, REMOVE, MODIFY
    reason: str
    confidence: float
    suggestions: Optional[str] = None


class ClaudeClient:
    """简单的 Claude API 客户端（使用 requests）"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-sonnet-4-6"  # Claude Sonnet 4.6

    def create_message(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
        """发送消息到 Claude"""
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
    """跨 Ticker 边验证 Agent"""

    def __init__(
        self,
        neo4j_uri: str = "neo4j://10.16.176.189:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "eY6WaJ9OZYTLvwlW7cDqle1d2",
        anthropic_api_key: Optional[str] = None,
    ):
        # Neo4j 连接
        self.neo4j_driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password),
            connection_acquisition_timeout=15
        )

        # Claude 客户端
        api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("需要提供 Anthropic API Key")
        self.claude = ClaudeClient(api_key=api_key)

    def close(self):
        """关闭连接"""
        self.neo4j_driver.close()

    def get_node_by_name(self, name: str) -> Optional[dict]:
        """获取指定名称的节点"""
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
        """获取两个节点之间的边"""
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
        """获取节点的邻居（入边和出边）"""
        with self.neo4j_driver.session(database='neo4j') as session:
            # 出边
            out_result = session.run("""
                MATCH (n:CausalNodeV2 {name: $name})-[r]->(other)
                RETURN other.name as target, type(r) as rel, r.weight as weight, r.tau as tau
                ORDER BY abs(r.tau) DESC
                LIMIT $limit
            """, name=node_name, limit=limit)
            out_edges = [dict(r) for r in out_result]

            # 入边
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
        """构建 LLM 验证 prompt"""

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
        验证两个 ticker 之间的边

        Args:
            source_ticker: 源 ticker (如 "SSTK")
            target_ticker: 目标 ticker (如 "ETHUSD")
            source_field: 字段名 (默认 "close_price")
            target_field: 字段名 (默认 "close_price")
        """
        # 构建完整节点名
        source_name = f"{source_ticker}_{source_field}"
        target_name = f"{target_ticker}_{target_field}"

        print(f"🔍 查找节点: {source_name} 和 {target_name}")

        # 获取节点信息
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

        print(f"✅ 找到节点: {source_node.get('name')} <-> {target_node.get('name')}")

        # 获取边信息
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

        print(f"✅ 找到边: {edge.get('from_node')} -[{edge.get('rel_type')}]-> {edge.get('to_node')} (tau={edge.get('tau')}, weight={edge.get('weight')})")

        # 获取上下文
        print("📊 提取节点上下文...")
        source_context = self.get_node_neighbors(source_name, limit=10)
        target_context = self.get_node_neighbors(target_name, limit=10)

        # 构建 prompt
        prompt = self.build_validation_prompt(
            source_node, target_node, edge, source_context, target_context
        )

        # 调用 Claude
        print("🤖 调用 Claude 进行验证...")
        try:
            response_text = self.claude.create_message(prompt, max_tokens=2000, temperature=0.2)

            # 解析响应
            content = response_text
            # 提取 JSON
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
        """打印验证结果"""
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
        """获取指定 ticker 的所有出边"""
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
        """获取指定 ticker 的所有入边"""
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
        批量验证单个 ticker 的所有边

        Args:
            ticker: 要验证的 ticker (如 "NVDA")
            mode: "out" 验证出边，"in" 验证入边
            top_n: 验证前 N 条边（按 tau 绝对值排序）
            field: 字段名
        """
        results = []

        if mode == "out":
            edges = self.get_all_outgoing_edges(ticker, field, limit=top_n)
            print(f"📤 {ticker} 的出边（Top {len(edges)}）:")
        else:
            edges = self.get_all_incoming_edges(ticker, field, limit=top_n)
            print(f"📥 {ticker} 的入边（Top {len(edges)}）:")

        if not edges:
            print(f"  未找到 {ticker} 的{'出' if mode == 'out' else '入'}边")
            return results

        # 打印概览
        for i, e in enumerate(edges[:5], 1):
            direction = f"{e['source']} -> {e['target']}"
            print(f"  {i}. {direction} (tau={e['tau']}, weight={e['weight']:.4f})")

        print(f"\n开始验证前 {min(top_n, len(edges))} 条边...\n")

        # 逐条验证
        for i, edge in enumerate(edges[:top_n], 1):
            print(f"[{i}/{min(top_n, len(edges))}] 验证: {edge['source']} -> {edge['target']}")

            # 获取节点信息
            source_node = self.get_node_by_name(edge['source'])
            target_node = self.get_node_by_name(edge['target'])

            if not source_node or not target_node:
                print(f"  ⚠️  无法获取节点信息，跳过")
                continue

            # 获取上下文
            source_context = self.get_node_neighbors(edge['source'], limit=5)
            target_context = self.get_node_neighbors(edge['target'], limit=5)

            # 构建 prompt
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

            # 调用 Claude
            try:
                response_text = self.claude.create_message(prompt, max_tokens=1500, temperature=0.2)

                # 解析 JSON
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
                print(f"  ❌ 验证失败: {str(e)[:50]}")
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
        """打印批量验证结果汇总"""
        print("\n" + "=" * 70)
        print(f"📊 {ticker} {'出' if mode == 'out' else '入'}边验证汇总")
        print("=" * 70)

        if not results:
            print("无验证结果")
            return

        # 统计
        keep = sum(1 for r in results if r.action == "KEEP")
        remove = sum(1 for r in results if r.action == "REMOVE")
        modify = sum(1 for r in results if r.action == "MODIFY")
        error = sum(1 for r in results if r.action in ["ERROR", "UNKNOWN"])

        print(f"\n总计: {len(results)} 条边")
        print(f"  ✅ KEEP:    {keep} ({keep/len(results):.0%})")
        print(f"  ❌ REMOVE:  {remove} ({remove/len(results):.0%})")
        print(f"  ⚠️  MODIFY:  {modify} ({modify/len(results):.0%})")
        print(f"  ❓ ERROR:   {error} ({error/len(results):.0%})")

        # 列出可疑边（REMOVE）
        if remove > 0:
            print(f"\n🔍 建议移除的可疑边:")
            for r in results:
                if r.action == "REMOVE":
                    print(f"  ❌ {r.source[:25]:25} -> {r.target[:25]:25} ({r.confidence:.0%})")

        # 列出高置信度 KEEP
        high_conf_keep = [r for r in results if r.action == "KEEP" and r.confidence > 0.8]
        if high_conf_keep:
            print(f"\n✅ 高置信度合理的边:")
            for r in high_conf_keep[:5]:
                print(f"  ✅ {r.source[:25]:25} -> {r.target[:25]:25} ({r.confidence:.0%})")

        print("=" * 70)


def main():
    """主函数 - 示例用法"""
    import argparse

    parser = argparse.ArgumentParser(description="Cross-Ticker Edge Validator")
    parser.add_argument("ticker", help="Ticker to analyze (e.g., NVDA)")
    parser.add_argument("--target", help="Target ticker for single edge validation (optional)")
    parser.add_argument("--mode", choices=["out", "in"], default="out",
                       help="Mode: 'out' for outgoing edges, 'in' for incoming edges")
    parser.add_argument("--top", type=int, default=10, help="Number of top edges to validate")
    parser.add_argument("--api-key", help="Anthropic API Key (or set ANTHROPIC_API_KEY env var)")

    args = parser.parse_args()

    # 获取 API key
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ 请提供 Anthropic API Key：")
        print("   方式1: 设置环境变量 ANTHROPIC_API_KEY")
        print("   方式2: 使用 --api-key 参数")
        sys.exit(1)

    # 创建验证器
    validator = CrossTickerEdgeValidator(
        anthropic_api_key=api_key,
        neo4j_uri="neo4j://10.16.176.189:7687",
        neo4j_user="neo4j",
        neo4j_password="eY6WaJ9OZYTLvwlW7cDqle1d2"
    )

    try:
        if args.target:
            # 单条边验证模式
            print(f"\n🔎 验证单条边: {args.ticker} -> {args.target}")
            result = validator.validate_edge(args.ticker, args.target)
            validator.print_result(result)
        else:
            # 批量单边验证模式
            print(f"\n🔎 批量验证 {args.ticker} 的 {'出' if args.mode == 'out' else '入'}边 (Top {args.top})")
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
