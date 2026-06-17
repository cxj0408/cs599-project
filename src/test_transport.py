"""测试不同的 MCP transport 配置"""
import asyncio
from config import CONFIG
from langchain_mcp_adapters.client import MultiServerMCPClient


async def test_transport(transport_type: str):
    """测试指定的 transport 类型"""
    print(f"\n{'='*60}")
    print(f"测试 transport: {transport_type}")
    print(f"{'='*60}")
    
    try:
        client = MultiServerMCPClient({
            "amap-server": {
                "transport": transport_type,
                "url": CONFIG.mcp_url,
                "headers": {
                    "Authorization": f"Bearer {CONFIG.api_key}",
                    "Content-Type": "application/json",
                }
            }
        })
        
        print(f"✅ 客户端创建成功")
        print(f"   正在获取工具列表...")
        
        tools = await client.get_tools()
        print(f"✅ 成功! 获取到 {len(tools)} 个工具:")
        for tool in tools[:5]:  # 只显示前5个
            print(f"   - {tool.name}")
        if len(tools) > 5:
            print(f"   ... 还有 {len(tools) - 5} 个工具")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}")
        print(f"   错误: {str(e)[:200]}")
        return False


async def main():
    print("=" * 60)
    print("🔍 MCP Transport 配置测试")
    print("=" * 60)
    print(f"MCP URL: {CONFIG.mcp_url}")
    print(f"API Key: {CONFIG.api_key[:20]}...")
    
    # 测试不同的 transport 类型
    transports_to_test = ["http", "sse", "streamable_http"]
    
    results = {}
    for transport in transports_to_test:
        success = await test_transport(transport)
        results[transport] = success
    
    # 总结
    print(f"\n{'='*60}")
    print("📊 测试结果总结")
    print(f"{'='*60}")
    
    for transport, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{transport:20s} {status}")
    
    # 建议
    successful = [t for t, s in results.items() if s]
    if successful:
        print(f"\n💡 建议: 在 .env 中设置 MCP_TRANSPORT={successful[0]}")
    else:
        print(f"\n⚠️  所有 transport 都失败了,请检查:")
        print(f"   1. MCP URL 是否正确")
        print(f"   2. API Key 是否有效")
        print(f"   3. 网络连接是否正常")


if __name__ == "__main__":
    asyncio.run(main())
