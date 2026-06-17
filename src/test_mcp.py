"""测试 MCP 连接"""
import asyncio
from config import CONFIG
from mcp_client import McpClientManager


async def test_mcp_connection():
    print("=" * 60)
    print("测试 MCP 连接")
    print("=" * 60)
    print(f"API Key: {CONFIG.api_key[:20]}...")
    print(f"MCP URL: {CONFIG.mcp_url}")
    print(f"缓存启用: {CONFIG.cache_enabled}")
    print()
    
    try:
        manager = McpClientManager()
        print("✅ MCP 客户端管理器创建成功")
        
        print("\n正在获取工具列表...")
        tools = await manager.get_all_tools()
        print(f"✅ 成功获取 {len(tools)} 个工具:")
        for tool in tools:
            print(f"   - {tool.name}")
        
        print("\n✅ 所有测试通过!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mcp_connection())
