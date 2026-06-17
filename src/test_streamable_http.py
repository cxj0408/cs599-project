"""测试 streamable-http transport"""
import asyncio
from config import CONFIG


async def test_streamable_http():
    """测试 streamable-http 方式"""
    print("=" * 70)
    print("🔍 测试 streamable-http transport")
    print("=" * 70)
    print(f"Transport: {CONFIG.mcp_transport}")
    print(f"URL: {CONFIG.mcp_url}")
    print()
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        print("正在创建 MCP 客户端...")
        client = MultiServerMCPClient({
            "amap-server": {
                "transport": CONFIG.mcp_transport,
                "url": CONFIG.mcp_url,
                "headers": {
                    "Authorization": f"Bearer {CONFIG.api_key}",
                }
            }
        })
        
        print("✅ 客户端创建成功")
        print("\n正在获取工具列表...")
        
        tools = await client.get_tools()
        
        print(f"\n✅ 成功! 获取到 {len(tools)} 个工具:")
        for tool in tools[:10]:
            print(f"   - {tool.name}")
        
        if len(tools) > 10:
            print(f"   ... 还有 {len(tools) - 10} 个工具")
        
        print("\n✅ 测试成功!")
        return True
        
    except Exception as e:
        print(f"\n❌ 失败: {type(e).__name__}")
        print(f"   错误: {str(e)[:500]}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_streamable_http())
    
    if not result:
        print("\n" + "=" * 70)
        print("💡 如果 streamable_http 也失败,可能需要:")
        print("   1. 检查阿里百炼控制台的服务开通状态")
        print("   2. 联系阿里云技术支持确认正确的调用方式")
        print("   3. 查看官方文档的最新示例代码")
        print("=" * 70)
