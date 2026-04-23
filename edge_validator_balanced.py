#!/usr/bin/env python3
"""PuppyGraph 边验证器 (Balanced版本) - 使用 OpenRouter LLM 验证边

这个版本使用平衡的验证标准：
1. 区分统计相关性与因果机制
2. 需要合理的因果路径，不只是市场相关性
3. 更谨慎地使用 MODIFY
4. 移除缺乏因果基础的边
"""

import os
import sys
import json
import base64
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional


class EdgeValidatorBalanced:
    """使用 PuppyGraph HTTP API 和 OpenRouter LLM 验证边（平衡版本）"""
    
    def __init__(self, openrouter_api_key: str, env: str = "sit", model: str = "anthropic/claude-sonnet-4-6",
                 output_dir: str = "./validation_results"):
        self.openrouter_api_key = openrouter_api_key
        self.env = env
        self.model = model
        self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # PuppyGraph 配置
        # PuppyGraph configuration (credentials from environment variables)
        if env == "sit":
            self.puppy_url = os.getenv(
                "PUPPYGRAPH_SIT_URL", "https://puppygraph-sit.abel.ai"
            )
            self.puppy_user = os.getenv("PUPPYGRAPH_SIT_USER", "puppygraph")
            self.puppy_pass = os.getenv("PUPPYGRAPH_SIT_PASSWORD", "")
        else:
            self.puppy_url = os.getenv(
                "PUPPYGRAPH_PROD_URL", "https://puppygraph.abel.ai"
            )
            self.puppy_user = os.getenv("PUPPYGRAPH_PROD_USER", "puppygraph")
            self.puppy_pass = os.getenv("PUPPYGRAPH_PROD_PASSWORD", "")

        if not self.puppy_pass:
            raise ValueError(
                f"PuppyGraph password not set. "
                f"Please set PUPPYGRAPH_{env.upper()}_PASSWORD environment variable."
            )
    
    def query_puppy(self, cypher: str) -> List[Dict]:
        """执行 Cypher 查询"""
        credentials = base64.b64encode(f"{self.puppy_user}:{self.puppy_pass}".encode()).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }
        resp = requests.post(
            f"{self.puppy_url}/submitCypher",
            json={"query": cypher},
            headers=headers,
            timeout=30
        )
        resp.raise_for_status()
        raw_results = resp.json()
        
        # 转换 Keys/Values 格式为字典
        results = []
        for row in raw_results:
            keys = row.get("Keys", [])
            values = row.get("Values", [])
            data = dict(zip(keys, values))
            results.append(data)
        return results
    
    def get_outgoing_edges(self, ticker: str, field: str, limit: int = 50) -> List[Dict]:
        """获取指定 field 的出边（DISTINCT 去重，避免同一 source->target 的重复边）"""
        node_pattern = f"{ticker}_{field}"
        query = f"""
        MATCH (source)-[r:CAUSES]->(target)
        WHERE source.node_name = '{node_pattern}'
        RETURN DISTINCT
               source.node_name as source,
               target.node_name as target
        LIMIT {limit}
        """
        return self.query_puppy(query)

    def get_incoming_edges(self, ticker: str, field: str, limit: int = 50) -> List[Dict]:
        """获取指定 field 的入边（DISTINCT 去重，避免同一 source->target 的重复边）"""
        node_pattern = f"{ticker}_{field}"
        query = f"""
        MATCH (source)-[r:CAUSES]->(target)
        WHERE target.node_name = '{node_pattern}'
        RETURN DISTINCT
               source.node_name as source,
               target.node_name as target
        LIMIT {limit}
        """
        return self.query_puppy(query)
    
    def call_openrouter(self, system_prompt: str, user_prompt: str) -> Dict:
        """Call OpenRouter API with model verification"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://abel.ai",
            "X-Title": "Abel Edge Validator (Balanced)"
        }

        # Force specific model - no fallback
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 800,  # Increased for detailed reasoning
            "provider": {
                "order": ["Anthropic"],  # Force Anthropic provider for Claude models
                "allow_fallbacks": False  # Do NOT fallback to other models
            }
        }

        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=90  # Increased timeout for Claude
        )

        if resp.status_code == 403:
            raise RuntimeError(
                f"Claude Sonnet 4.6 is not available in your region (403 Forbidden). "
                f"Model requested: {self.model}. "
                f"Consider using a different model or VPN."
            )
        elif resp.status_code != 200:
            print(f"OpenRouter Error: {resp.status_code}")
            print(f"Response: {resp.text[:500]}")

        resp.raise_for_status()
        result = resp.json()

        # Verify actual model used
        actual_model = result.get("model", "unknown")
        if self.model not in actual_model and "claude" not in actual_model.lower():
            print(f"⚠️  Warning: Expected {self.model}, but got {actual_model}")

        return result
    
    def get_balanced_system_prompt(self) -> str:
        """返回平衡的系统提示词 v3 - 要求具体的业务层面原因"""
        return """You are an expert financial causal graph validator. Your task is to evaluate whether a volume-based causal edge between two stocks is reasonable, providing SPECIFIC and DETAILED business-level reasoning.

## KEY PRINCIPLE

Volume correlations between stocks can be legitimate when there is a concrete business link. Generic reasons like "same sector" or "market correlation" are INSUFFICIENT. You must identify the SPECIFIC mechanism.

## VERDICT RULES

### KEEP (strong, specific business link):
Use KEEP only when you can articulate a SPECIFIC business relationship:

**Valid KEEP reasons (examples of specificity required):**
- **Direct supplier-customer with quantifiable relationship**: "GOOGL → NVDA because Google Cloud purchases NVIDIA A100/H100 GPUs for AI training, representing ~$X billion in annual revenue"
- **Clear competitive dynamic**: "AMD ↔ NVDA because both compete for datacenter GPU market share, with AMD MI300X directly challenging NVIDIA H100"
- **Supply chain dependency**: "ENTG → NVDA because Entegris supplies ultra-pure chemicals essential for NVIDIA's chip manufacturing process"
- **Joint product/technology**: "KLAC → NVDA because KLA's inspection equipment is used in NVIDIA's foundry partner (TSMC) facilities"

### MODIFY (weak or indirect link):
Use MODIFY when there is some connection but it's indirect or overstated:

**Valid MODIFY reasons:**
- **Indirect supply chain**: "TXN → NVDA because Texas Instruments supplies analog chips that go into NVIDIA-based systems, but not directly into NVIDIA's products"
- **Sector correlation without direct link**: "INTC → NVDA because both are semiconductor companies affected by same fab capacity constraints, but don't compete directly in GPUs"
- **Index/ETF effect**: "UNH → NVDA because both are S&P 500 components and move with index flows, but no business relationship"

### REMOVE (no specific business link):
Use REMOVE when you cannot identify a concrete business relationship:

**Valid REMOVE reasons:**
- **Completely unrelated businesses**: "SON → NVDA because Sonoco is a packaging company with zero business relationship to NVIDIA's GPU/AI business"
- **No supply chain connection**: "HAFC → NVDA because Hanmi Financial is a small regional bank with no lending or business relationship to NVIDIA"
- **Geographic/industry mismatch**: "LITB → NVDA because LightInTheBox is a Chinese e-commerce SMB with no connection to NVIDIA's enterprise GPU business"

## FORBIDDEN VAGUE REASONINGS (NEVER USE THESE):

❌ "Same sector" - specify WHAT they do in that sector
❌ "Market correlation" - explain WHY they correlate
❌ "Customer relationship" - specify WHAT the customer buys and for what purpose
❌ "Tech company" - explain the SPECIFIC tech area and relationship
❌ "Related industries" - articulate the EXACT supply chain or competitive link

## REASONING REQUIREMENTS

Your Reasoning MUST include:
1. What each company SPECIFICALLY does (e.g., "GOOGL operates Google Cloud Platform providing AI/ML infrastructure")
2. The EXACT nature of their relationship (e.g., "GOOGL purchases NVIDIA GPUs to power their TPUs and AI training clusters")
3. WHY this would cause volume co-movement (e.g., "when GOOGL announces expanded AI capacity, they increase GPU orders, driving NVDA volume")

## OUTPUT FORMAT

Verdict: <KEEP|MODIFY|REMOVE>
Confidence: <0-100>
Reasoning: <2-3 sentences with SPECIFIC business details. Format: "[Source company] [specific business] → [Target company] [specific business]. [Exact relationship nature]. [Why volume co-moves].">

**REMEMBER: VAGUE REASONINGS ARE UNACCEPTABLE. If you cannot provide specific business details, use MODIFY or REMOVE.**
"""
    
    def validate_edge(self, source: str, target: str, weight: Any = None, 
                      confidence: Any = None, driver: Any = None) -> Dict:
        """使用 LLM 验证边（平衡版本）"""
        system_prompt = self.get_balanced_system_prompt()
        
        user_prompt = f"""Validate the following causal edge with a balanced, mechanism-focused approach:

Source: {source}
Target: {target}
Weight: {weight if weight else 'N/A'}
Confidence: {confidence if confidence else 'N/A'}
Driver: {driver if driver else 'N/A'}

Consider:
1. Is there a specific causal mechanism (not just correlation)?
2. What is the transmission channel for this causation?
3. Is this a direct relationship or driven by confounding factors?
4. Would a rational market participant expect this causation?

Provide your verdict following the format in the system prompt."""
        
        # 最多重试 2 次
        max_retries = 2
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                result = self.call_openrouter(system_prompt, user_prompt)

                # 防御性检查：response 结构
                if not result or "choices" not in result or not result["choices"]:
                    last_error = f"Invalid API response structure: {str(result)[:200]}"
                    continue

                message = result["choices"][0].get("message") or {}
                content = message.get("content")

                # 如果 content 是 None 或空，重试
                if not content or not isinstance(content, str):
                    last_error = f"Empty/invalid content: {type(content).__name__}"
                    continue

                # 解析结果
                verdict = "UNKNOWN"
                confidence_score = 0
                reasoning = ""
                suggestion = ""

                # 尝试多种解析方式
                for line in content.split("\n"):
                    line_stripped = line.strip()
                    if not line_stripped:
                        continue

                    # 匹配 Verdict (支持多种格式: "Verdict:", "**Verdict:**", "## Verdict")
                    line_lower = line_stripped.lower()
                    if "verdict" in line_lower and ":" in line_stripped:
                        v = line_stripped.split(":", 1)[-1].strip().upper()
                        # 去除 markdown 标记
                        v = v.replace("*", "").replace("`", "").strip()
                        if "KEEP" in v:
                            verdict = "KEEP"
                        elif "REMOVE" in v:
                            verdict = "REMOVE"
                        elif "MODIFY" in v:
                            verdict = "MODIFY"
                    elif "confidence" in line_lower and ":" in line_stripped:
                        try:
                            c = line_stripped.split(":", 1)[-1].strip()
                            c = c.replace("%", "").replace("*", "").strip()
                            # 提取数字
                            import re as re_mod
                            match = re_mod.search(r'\d+', c)
                            if match:
                                confidence_score = int(match.group())
                        except Exception:
                            pass
                    elif "reasoning" in line_lower and ":" in line_stripped:
                        reasoning = line_stripped.split(":", 1)[-1].strip()
                    elif "suggestion" in line_lower and ":" in line_stripped:
                        suggestion = line_stripped.split(":", 1)[-1].strip()

                # 如果 reasoning 为空，尝试从内容中提取
                if not reasoning:
                    # 取第一个非空且非结构化行作为 reasoning
                    for line in content.split("\n"):
                        line_stripped = line.strip()
                        if (line_stripped and
                                not any(kw in line_stripped.lower()
                                        for kw in ["verdict", "confidence", "suggestion"])
                                and len(line_stripped) > 20):
                            reasoning = line_stripped
                            break
                    if not reasoning:
                        reasoning = content[:200]

                # 如果找不到明确的判决，从内容中推断
                if verdict == "UNKNOWN":
                    content_upper = content.upper()
                    # 优先匹配明确的 Verdict 格式
                    import re as re_mod
                    m = re_mod.search(r'\bVERDICT\s*[:：]\s*(KEEP|MODIFY|REMOVE)', content_upper)
                    if m:
                        verdict = m.group(1)
                    elif "KEEP" in content_upper and "REMOVE" not in content_upper:
                        verdict = "KEEP"
                    elif "REMOVE" in content_upper:
                        verdict = "REMOVE"
                    elif "MODIFY" in content_upper:
                        verdict = "MODIFY"
                    elif "KEEP" in content_upper:
                        verdict = "KEEP"

                return {
                    "verdict": verdict,
                    "confidence": confidence_score,
                    "reasoning": (reasoning[:300] + "..."
                                  if len(reasoning) > 300 else reasoning),
                    "suggestion": suggestion,
                    "raw_response": content,
                    "validated_at": datetime.now().isoformat(),
                    "attempts": attempt + 1
                }
            except Exception as e:
                last_error = str(e)
                continue

        # 所有重试都失败
        return {
            "verdict": "ERROR",
            "confidence": 0,
            "reasoning": f"API call failed after {max_retries + 1} attempts: {last_error}",
            "suggestion": "",
            "raw_response": "",
            "validated_at": datetime.now().isoformat(),
            "attempts": max_retries + 1
        }
    
    def save_results_to_json(self, results: List[Dict], ticker: str, field: str, mode: str):
        """保存详细结果到 JSON 文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/validation_{ticker}_{field}_{mode}_{timestamp}.json"
        
        output_data = {
            "metadata": {
                "ticker": ticker,
                "field": field,
                "mode": mode,
                "env": self.env,
                "model": self.model,
                "total_edges": len(results),
                "timestamp": datetime.now().isoformat()
            },
            "statistics": {
                "KEEP": sum(1 for r in results if r.get("verdict") == "KEEP"),
                "REMOVE": sum(1 for r in results if r.get("verdict") == "REMOVE"),
                "MODIFY": sum(1 for r in results if r.get("verdict") == "MODIFY"),
                "ERROR": sum(1 for r in results if r.get("verdict") not in ["KEEP", "REMOVE", "MODIFY"])
            },
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        return filename
    
    def run(self, ticker: str, field: str, mode: str, top: int):
        """运行验证"""
        print(f"=" * 70)
        print(f"🚀 PuppyGraph Edge Validator (BALANCED MODE)")
        print(f"=" * 70)
        print(f"Ticker: {ticker}")
        print(f"Field: {field}")
        print(f"Mode: {mode}")
        print(f"Top: {top}")
        print(f"Env: {self.env}")
        print(f"Output Dir: {self.output_dir}")
        print(f"=" * 70)
        
        # 获取边
        if mode == "out":
            edges = self.get_outgoing_edges(ticker, field, top)
            print(f"\n📤 Found {len(edges)} outgoing edges for {ticker}_{field}")
        else:
            edges = self.get_incoming_edges(ticker, field, top)
            print(f"\n📥 Found {len(edges)} incoming edges for {ticker}_{field}")
        
        if not edges:
            print(f"⚠️ No matching edges found")
            return []
        
        # 验证每条边
        results = []
        for i, edge in enumerate(edges, 1):
            source = edge.get("source", "") or "Unknown"
            target = edge.get("target", "") or "Unknown"
            weight = edge.get("weight") or "N/A"
            confidence = edge.get("confidence") or "N/A"
            driver = edge.get("driver") or "N/A"
            
            print(f"\n{'─' * 70}")
            print(f"[{i}/{len(edges)}] {source} → {target}")
            print(f"    Weight: {weight} | Confidence: {confidence} | Driver: {driver}")
            print(f"{'─' * 70}")
            
            result = self.validate_edge(source, target, weight, confidence, driver)
            result["source"] = source
            result["target"] = target
            result["original_weight"] = weight
            result["original_confidence"] = confidence
            result["original_driver"] = driver
            results.append(result)
            
            verdict = result.get("verdict", "UNKNOWN")
            reasoning = result.get("reasoning", "")
            conf = result.get("confidence", 0)
            suggestion = result.get("suggestion", "")
            
            icon = {"KEEP": "✅", "REMOVE": "❌", "MODIFY": "⚠️", "ERROR": "💥", "UNKNOWN": "❓"}.get(verdict, "❓")
            print(f"{icon} Verdict: {verdict}")
            print(f"📝 Reasoning: {reasoning}")
            if suggestion:
                print(f"💡 Suggestion: {suggestion}")
            print(f"📈 Confidence: {conf}%")
        
        # 汇总统计
        print(f"\n{'=' * 70}")
        print("📊 Summary Statistics")
        print(f"{'=' * 70}")
        
        keep = sum(1 for r in results if r.get("verdict") == "KEEP")
        remove = sum(1 for r in results if r.get("verdict") == "REMOVE")
        modify = sum(1 for r in results if r.get("verdict") == "MODIFY")
        error = sum(1 for r in results if r.get("verdict") not in ["KEEP", "REMOVE", "MODIFY"])
        
        print(f"  ✅ KEEP:    {keep} ({keep/len(results)*100:.1f}%)")
        print(f"  ❌ REMOVE:  {remove} ({remove/len(results)*100:.1f}%)")
        print(f"  ⚠️  MODIFY:  {modify} ({modify/len(results)*100:.1f}%)")
        print(f"  💥 ERROR:   {error} ({error/len(results)*100:.1f}%)")
        print(f"  ─────────────")
        print(f"  📊 Total:    {len(results)}")
        
        # 保存结果到 JSON
        json_file = self.save_results_to_json(results, ticker, field, mode)
        
        # 打印一些有趣的发现
        print(f"\n{'=' * 70}")
        print("🔍 Notable Findings")
        print(f"{'=' * 70}")
        
        remove_results = [r for r in results if r.get("verdict") == "REMOVE"]
        if remove_results:
            print("\n❌ Edges marked for REMOVAL:")
            for r in remove_results[:5]:
                print(f"  - {r['source']} → {r['target']}: {r.get('reasoning', 'No reasoning')[:60]}...")
        
        modify_results = [r for r in results if r.get("verdict") == "MODIFY"]
        if modify_results:
            print("\n⚠️  Edges marked for MODIFICATION:")
            for r in modify_results[:5]:
                print(f"  - {r['source']} → {r['target']}")
                if r.get('suggestion'):
                    print(f"    Suggestion: {r.get('suggestion', '')[:80]}...")
        
        return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PuppyGraph Edge Validator (Balanced) with OpenRouter")
    parser.add_argument("ticker", help="Ticker to analyze (e.g., NVDA)")
    parser.add_argument("--field", default="volume", help="Field to analyze (e.g., volume, price)")
    parser.add_argument("--mode", choices=["in", "out"], default="out", help="Mode: 'out' for outgoing, 'in' for incoming")
    parser.add_argument("--top", type=int, default=50, help="Number of top edges to validate (default: 50)")
    parser.add_argument("--env", default="sit", choices=["sit", "prod"], help="Environment: sit or prod")
    parser.add_argument("--model", default="nvidia/nemotron-3-super-120b-a12b", help="OpenRouter model to use")
    parser.add_argument("--output-dir", default="./validation_results", help="Directory to save JSON results")
    
    args = parser.parse_args()
    
    # 获取 API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Please set OPENROUTER_API_KEY environment variable")
        sys.exit(1)
    
    # 创建验证器并运行
    validator = EdgeValidatorBalanced(api_key, args.env, args.model, args.output_dir)
    validator.run(args.ticker, args.field, args.mode, args.top)
