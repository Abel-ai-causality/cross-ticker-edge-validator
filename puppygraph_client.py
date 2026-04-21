#!/usr/bin/env python3
"""
PuppyGraph HTTP API Client
Supports Cypher and Gremlin queries
"""

import os
import requests
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class PuppyGraphConfig:
    """PuppyGraph连接配置"""
    base_url: str
    username: str
    password: str


class PuppyGraphClient:
    """
    PuppyGraph HTTP API 客户端

    示例:
        client = PuppyGraphClient("https://puppygraph-sit.abel.ai", "puppygraph", "password")

        # 执行Cypher查询
        result = client.cypher("MATCH (n) RETURN count(n) as count")
        print(result)

        # 执行Gremlin查询
        result = client.gremlin("g.V().count()")
        print(result)
    """

    def __init__(self, base_url: str, username: str, password: str):
        """
        初始化PuppyGraph客户端

        Args:
            base_url: PuppyGraph实例的URL, 例如 "https://puppygraph-sit.abel.ai"
            username: 用户名
            password: 密码
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            auth=(self.username, self.password),
            headers={"Content-Type": "application/json"},
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    def cypher(self, query: str, timeout: int = 30) -> List[Dict[str, Any]]:
        """
        执行Cypher查询

        Args:
            query: Cypher查询语句
            timeout: 查询超时时间(秒)

        Returns:
            查询结果列表,每个元素是一个字典,包含Keys和Values

        示例:
            >>> client.cypher("MATCH (n) RETURN count(n) as count")
            [{'Keys': ['count'], 'Values': ['100']}]
        """
        payload = {
            "query": query,
            "timeout": timeout
        }
        return self._request("POST", "/submitCypher", json=payload)

    def gremlin(self, query: str, timeout: int = 30) -> Any:
        """
        执行Gremlin查询

        Args:
            query: Gremlin查询语句
            timeout: 查询超时时间(秒)

        Returns:
            查询结果

        示例:
            >>> client.gremlin("g.V().count()")
        """
        payload = {
            "query": query,
            "timeout": timeout
        }
        return self._request("POST", "/submitGremlin", json=payload)

    def status(self) -> Dict[str, Any]:
        """
        获取PuppyGraph服务状态

        Returns:
            服务状态信息,包含版本、健康状态等
        """
        return self._request("GET", "/status")

    def profile(self) -> Dict[str, Any]:
        """
        获取用户配置信息

        Returns:
            用户配置信息
        """
        return self._request("GET", "/profile")

    def get_schema(self) -> Dict[str, Any]:
        """
        获取图的Schema信息

        Returns:
            包含节点类型和关系类型的Schema定义
        """
        return self._request("GET", "/schema")


# Predefined environment configs (credentials read from environment variables)
def _get_env_config(env: str) -> PuppyGraphConfig:
    """Build config for an environment from environment variables.

    Required env vars:
      - PUPPYGRAPH_{ENV}_URL       (defaults provided)
      - PUPPYGRAPH_{ENV}_USER      (defaults to 'puppygraph')
      - PUPPYGRAPH_{ENV}_PASSWORD  (REQUIRED - no default)
    """
    env_upper = env.upper()
    default_url = (
        "https://puppygraph-sit.abel.ai" if env == "sit"
        else "https://puppygraph.abel.ai"
    )
    password = os.getenv(f"PUPPYGRAPH_{env_upper}_PASSWORD", "")
    if not password:
        raise ValueError(
            f"PUPPYGRAPH_{env_upper}_PASSWORD environment variable is required"
        )
    return PuppyGraphConfig(
        base_url=os.getenv(f"PUPPYGRAPH_{env_upper}_URL", default_url),
        username=os.getenv(f"PUPPYGRAPH_{env_upper}_USER", "puppygraph"),
        password=password,
    )


def get_sit_config() -> PuppyGraphConfig:
    return _get_env_config("sit")


def get_prod_config() -> PuppyGraphConfig:
    return _get_env_config("prod")


def create_client_from_config(config: PuppyGraphConfig) -> PuppyGraphClient:
    """Create client from config."""
    return PuppyGraphClient(
        base_url=config.base_url,
        username=config.username,
        password=config.password,
    )


if __name__ == "__main__":
    # Smoke test - requires PUPPYGRAPH_SIT_PASSWORD env var
    print("Testing PuppyGraph API client (SIT environment)\n")

    client = create_client_from_config(get_sit_config())

    print("1. Status check...")
    try:
        print(f"   Status: {client.status()}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n2. Node count...")
    try:
        result = client.cypher("MATCH (n) RETURN count(n) as node_count")
        print(f"   Nodes: {result}")
    except Exception as e:
        print(f"   Error: {e}")

    print("\n3. Edge count...")
    try:
        result = client.cypher("MATCH ()-[r]->() RETURN count(r) as edge_count")
        print(f"   Edges: {result}")
    except Exception as e:
        print(f"   Error: {e}")
