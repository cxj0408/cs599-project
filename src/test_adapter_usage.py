"""测试 langchain-mcp-adapters 的不同用法"""
import asyncio
from config import CONFIG


async def test_adapter_v1():
    """测试方式 1: 使用字典配置 (当前方式)"""
    print("=" * 70)
    print("测试方式 1: MultiServerMCPClient with dict config")
    print("=" * 70)
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        client = MultiServerMCPClient({
            "amap-server": {
                "transport": "http",
                "url": CONFIG.mcp_url,
                "headers": {
                    "Authorization": f"Bearer {CONFIG.api_key}",
                }
            }
        })
        
        print("✅ 客户端创建成功")
        print("   正在获取工具...")
        
        tools = await client.get_tools()
        print(f"✅ 成功! 获取到 {len(tools)} 个工具")
        for tool in tools[:3]:
            print(f"   - {tool.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}")
        print(f"   错误: {str(e)[:300]}")
        import traceback
        traceback.print_exc()
        return False


async def test_adapter_v2():
    """测试方式 2: 使用单独的 MCPClient"""
    print("\n" + "=" * 70)
    print("测试方式 2: 直接使用 MCPClient")
    print("=" * 70)
    
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
        
        print(f"URL: {CONFIG.mcp_url}")
        
        async with streamablehttp_client(
            url=CONFIG.mcp_url,
            headers={
                "Authorization": f"Bearer {CONFIG.api_key}",
            }
        ) as (read_stream, write_stream, _):
            print("✅ streamablehttp_client 连接成功")
            
            async with ClientSession(read_stream, write_stream) as session:
                print("   正在初始化会话...")
                await session.initialize()
                
                print("   正在获取工具列表...")
                tools = await session.list_tools()
                
                print(f"✅ 成功! 获取到 {len(tools.tools)} 个工具:")
                for tool in tools.tools[:5]:
                    print(f"   - {tool.name}: {tool.description[:50]}")
                
        return True
        
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}")
        print(f"   错误: {str(e)[:300]}")
        import traceback
        traceback.print_exc()
        return False


async def test_adapter_v3():
    """测试方式 3: 使用 SSE transport"""
    print("\n" + "=" * 70)
    print("测试方式 3: 使用 SSE transport")
    print("=" * 70)
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        # 尝试 SSE URL (如果支持)
        sse_url = CONFIG.mcp_url.replace("/mcp", "/sse")
        print(f"尝试 SSE URL: {sse_url}")
        
        client = MultiServerMCPClient({
            "amap-server": {
                "transport": "sse",
                "url": sse_url,
                "headers": {
                    "Authorization": f"Bearer {CONFIG.api_key}",
                }
            }
        })
        
        print("✅ 客户端创建成功")
        print("   正在获取工具...")
        
        tools = await client.get_tools()
        print(f"✅ 成功! 获取到 {len(tools)} 个工具")
        
        return True
        
    except Exception as e:
        print(f"❌ 失败: {type(e).__name__}")
        print(f"   错误: {str(e)[:300]}")
        return False


async def main():
    print("🔍 测试 langchain-mcp-adapters 不同用法\n")
    
    results = []
    
    # 测试方式 1
    r1 = await test_adapter_v1()
    results.append(("方式 1 (dict config)", r1))
    
    # 测试方式 2
    r2 = await test_adapter_v2()
    results.append(("方式 2 (direct MCP)", r2))
    
    # 测试方式 3
    r3 = await test_adapter_v3()
    results.append(("方式 3 (SSE)", r3))
    
    # 总结
    print("\n" + "=" * 70)
    print("📊 测试结果总结")
    print("=" * 70)
    
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{name:30s} {status}")
    
    successful = [name for name, s in results if s]
    if successful:
        print(f"\n💡 建议: 使用 {successful[0]}")
    else:
        print("\n⚠️  所有方式都失败了")


if __name__ == "__main__":
    asyncio.run(main())
