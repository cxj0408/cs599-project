"""
配置中心 —— 统一管理环境变量、LLM 实例、MCP 连接参数。
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi

load_dotenv()

# ========== 修复 langchain_community ChatTongyi 流式 tool_calls 的 KeyError ==========
# 上游 bug: subtract_client_response 访问 prev_function["name"] / ["arguments"]
# 前没有检查 key 是否存在。流式首个 tool_call chunk 可能不含这些 key。


def _patched_subtract(self, resp, prev_resp):
    import json

    resp_copy = json.loads(json.dumps(resp))
    message = resp_copy["output"]["choices"][0]["message"]
    prev_message = json.loads(json.dumps(prev_resp))["output"]["choices"][0]["message"]

    message["content"] = message["content"].replace(
        prev_message.get("content", "") or "", ""
    )

    if message.get("tool_calls") and prev_message.get("tool_calls"):
        for index, tool_call in enumerate(message["tool_calls"]):
            function = tool_call["function"]
            prev_function = prev_message["tool_calls"][index]["function"]

            if "name" in function and "name" in prev_function:
                function["name"] = function["name"].replace(prev_function["name"], "")
            if "arguments" in function and "arguments" in prev_function:
                function["arguments"] = function["arguments"].replace(
                    prev_function["arguments"], ""
                )

    return resp_copy


ChatTongyi.subtract_client_response = _patched_subtract
# ========== 修复结束 ==========


@dataclass
class Config:
    """全局配置，单例语义 —— 模块级 CONFIG 实例"""

    # API 密钥
    api_key: str = field(
        default_factory=lambda: os.getenv("DASHSCOPE_API_KEY", "")
    )

    # LLM
    model_name: str = "qwen3-max"
    temperature: float = 0.7

    # MCP 连接（阿里百炼高德地图）
    # 注意: 阿里百炼使用 streamable-http 协议 (POST + SSE 混合)
    mcp_transport: str = field(
        default_factory=lambda: os.getenv("MCP_TRANSPORT", "streamable_http")
    )
    mcp_url: str = field(
        default_factory=lambda: os.getenv(
            "MCP_URL",
            "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp"  # streamable-http 端点
        )
    )

    # MCP result cache (Redis). Fail-open when Redis is unavailable.
    cache_enabled: bool = field(
        default_factory=lambda: os.getenv("MCP_CACHE_ENABLED", "true").lower()
        not in {"0", "false", "no", "off"}
    )
    redis_url: str = field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )
    redis_key_prefix: str = field(
        default_factory=lambda: os.getenv("MCP_CACHE_KEY_PREFIX", "travel-agent:mcp")
    )
    redis_socket_timeout: float = field(
        default_factory=lambda: float(os.getenv("REDIS_SOCKET_TIMEOUT", "1.5"))
    )
    cacheable_mcp_tools: set[str] = field(default_factory=lambda: {
        "maps_weather",
        "maps_search_detail",
    })
    mcp_cache_ttls: dict[str, int] = field(default_factory=lambda: {
        "maps_weather": int(os.getenv("MCP_WEATHER_CACHE_TTL", str(60 * 60 * 6))),
        "maps_search_detail": int(os.getenv("MCP_SEARCH_DETAIL_CACHE_TTL", str(60 * 60 * 24 * 7))),
    })

    # 工具领域映射
    tool_domains: dict = field(default_factory=lambda: {
        "poi":     ["maps_text_search", "maps_search_detail"],
        "weather": ["maps_weather"],
        "route":   [
            "maps_direction_walking_by_address",
            "maps_direction_driving_by_address",
            "maps_direction_transit_integrated_by_address",
        ],
    })

    # 自动检查初始化
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("请配置 DASHSCOPE_API_KEY")

    # 创建模型实例对象
    def create_llm(self) -> ChatTongyi:
        return ChatTongyi(
            model=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
            streaming=True,          # ← 启用水龙头，流式输出最远走到这里
        )


CONFIG = Config()
