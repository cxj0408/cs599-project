"""
MCP 客户端管理器 —— 单例模式，全局共享高德地图 MCP 连接。
"""
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool
from config import CONFIG
from mcp_cache import RedisMcpCache, wrap_mcp_tool_with_cache


class McpClientManager:
    """
    高德地图 MCP 客户端单例。
    这是单例模式
    保证整个程序永远只有一个 McpClientManager
    保证缓存只创建一次，不重复请求
    保证客户端不重复初始化

    职责：
      1. 管理与阿里百炼 MCP 服务器的连接
      2. 按领域（poi/weather/route）分发工具子集
      3. 缓存已加载工具，避免重复请求

    用法：
      manager = McpClientManager()
      poi_tools = await manager.get_tools_for("poi")
      route_tools = await manager.get_tools_for("route")
    """

    _instance: "McpClientManager | None" = None

    def __new__(cls) -> "McpClientManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._client: MultiServerMCPClient | None = None
        self._tools_cache: dict[str, list[BaseTool]] = {}
        self._result_cache = RedisMcpCache()
        self._initialized = True

    # ==================== 连接管理 ====================

    async def _get_client(self) -> MultiServerMCPClient:
        """懒加载 MCP 客户端"""
        if self._client is None:
            print(f"🔌 正在连接 MCP 服务: {CONFIG.mcp_url}")
            print(f"   API Key: {CONFIG.api_key[:20]}...")
            print(f"   传输协议: {CONFIG.mcp_transport}")
            
            try:
                # 尝试使用 sse 或 http 传输
                # 对于 HTTPS URL,langchain-mcp-adapters 0.2.x 应该自动处理
                self._client = MultiServerMCPClient({
                    "amap-server": {
                        "transport": CONFIG.mcp_transport,
                        "url": CONFIG.mcp_url,
                        "headers": {
                            "Authorization": f"Bearer {CONFIG.api_key}",
                            "Content-Type": "application/json",
                        }
                    }
                })
                print("✅ MCP 客户端初始化成功")
            except Exception as e:
                print(f"❌ MCP 客户端初始化失败: {type(e).__name__}")
                print(f"   错误: {e}")
                print(f"\n   💡 尝试方案:")
                print(f"   1. 检查 MCP_URL 是否正确")
                print(f"   2. 尝试更改 transport 为 'sse' 或 'stdio'")
                raise
        return self._client

    # ==================== 工具获取 ====================

    async def get_all_tools(self) -> list[BaseTool]:
        """获取 MCP 服务器暴露的全部工具"""
        if "all" not in self._tools_cache:
            try:
                print("\n🔍 正在从 MCP 服务器获取工具列表...")
                client = await self._get_client()
                tools = await client.get_tools()
                self._tools_cache["all"] = [
                    wrap_mcp_tool_with_cache(t, self._result_cache)
                    if CONFIG.cache_enabled and t.name in CONFIG.cacheable_mcp_tools
                    else t
                    for t in tools
                ]
                print(f"✅ 成功获取 {len(self._tools_cache['all'])} 个工具")
                # for t in self._tools_cache["all"]:
                #     print(f"   ✓ {t.name}: {t.description[:60]}...")
            except ExceptionGroup as eg:
                # 提取 ExceptionGroup 中的真实错误
                print(f"\n❌ MCP 工具加载失败 (ExceptionGroup):")
                print(f"   异常数量: {len(eg.exceptions)}")
                for i, exc in enumerate(eg.exceptions, 1):
                    print(f"\n   异常 {i}: {type(exc).__name__}")
                    print(f"   消息: {exc}")
                    if hasattr(exc, '__traceback__'):
                        import traceback
                        tb_str = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                        # 只打印关键行
                        for line in tb_str.split('\n')[:10]:
                            if line.strip():
                                print(f"      {line}")
                
                print(f"\n   💡 可能的原因:")
                print(f"   1. API Key 无效或已过期")
                print(f"   2. 网络连接问题，无法访问: {CONFIG.mcp_url}")
                print(f"   3. MCP 服务暂时不可用")
                print(f"   4. langchain-mcp-adapters 版本不兼容")
                raise
            except Exception as e:
                print(f"\n❌ MCP 工具加载失败: {type(e).__name__}")
                print(f"   错误信息: {e}")
                print(f"\n   💡 请检查:")
                print(f"   1. 网络连接是否正常")
                print(f"   2. DASHSCOPE_API_KEY 是否有效 (当前: {CONFIG.api_key[:20]}...)")
                print(f"   3. MCP 服务地址: {CONFIG.mcp_url}")
                print(f"   4. 依赖包版本是否兼容")
                import traceback
                traceback.print_exc()
                raise
        return self._tools_cache["all"]

    async def get_tools_for(self, domain: str) -> list[BaseTool]:
        """按领域获取工具子集"""
        all_tools = await self.get_all_tools()
        target_names = set(CONFIG.tool_domains.get(domain, []))
        return [t for t in all_tools if t.name in target_names]

    # ==================== 生命周期 ====================

    async def close(self):
        """关闭 MCP 连接（如有需要）"""
        await self._result_cache.close()
        self._client = None
        self._tools_cache.clear()

    @classmethod
    def reset(cls):
        """重置单例（测试用）"""
        cls._instance = None
