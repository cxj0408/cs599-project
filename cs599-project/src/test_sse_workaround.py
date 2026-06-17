"""尝试使用不同的 MCP 会话创建方式"""
import asyncio
from config import CONFIG


async def test_with_explicit_session():
    """显式创建 SSE 会话"""
    print("=" * 70)
    print("🔍 测试显式 SSE 会话创建")
    print("=" * 70)
    
    try:
        from mcp.client.sse import sse_client
        from mcp import ClientSession
        
        print(f"URL: {CONFIG.mcp_url}")
        print(f"Headers: Authorization: Bearer {CONFIG.api_key[:20]}...")
        print()
        
        # 手动管理 SSE 连接
        print("正在建立 SSE 连接...")
        
        # 不使用 async with,而是手动管理
        streams = sse_client(
            url=CONFIG.mcp_url,
            headers={
                "Authorization": f"Bearer {CONFIG.api_key}",
            }
        )
        
        # 进入上下文
        read_stream, write_stream = await streams.__aenter__()
        
        print("✅ SSE 连接建立成功")
        print(f"   Read stream: {read_stream}")
        print(f"   Write stream: {write_stream}")
        
        # 创建会话
        print("\n正在创建 MCP 会话...")
        session = ClientSession(read_stream, write_stream)
        await session.__aenter__()
        
        print("✅ MCP 会话创建成功")
        
        # 初始化
        print("\n正在初始化会话...")
        init_result = await session.initialize()
        print(f"✅ 初始化成功: {init_result}")
        
        # 获取工具列表
        print("\n正在获取工具列表...")
        tools_result = await session.list_tools()
        print(f"✅ 获取到 {len(tools_result.tools)} 个工具:")
        
        for tool in tools_result.tools[:5]:
            print(f"   - {tool.name}: {tool.description[:60]}")
        
        if len(tools_result.tools) > 5:
            print(f"   ... 还有 {len(tools_result.tools) - 5} 个工具")
        
        # 清理
        await session.__aexit__(None, None, None)
        await streams.__aexit__(None, None, None)
        
        print("\n✅ 测试成功!")
        return True
        
    except Exception as e:
        print(f"\n❌ 失败: {type(e).__name__}")
        print(f"   错误: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_with_langchain_adapter():
    """使用 langchain-mcp-adapters 但添加重试逻辑"""
    print("\n" + "=" * 70)
    print("🔍 测试带重试的 langchain-mcp-adapters")
    print("=" * 70)
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        print("正在创建客户端...")
        client = MultiServerMCPClient({
            "amap-server": {
                "transport": "sse",
                "url": CONFIG.mcp_url,
                "headers": {
                    "Authorization": f"Bearer {CONFIG.api_key}",
                }
            }
        })
        
        print("✅ 客户端创建成功")
        print("正在获取工具 (最多重试3次)...")
        
        # 重试逻辑
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"\n  尝试 {attempt}/{max_retries}...")
                tools = await client.get_tools()
                print(f"\n✅ 成功! 获取到 {len(tools)} 个工具")
                for tool in tools[:3]:
                    print(f"   - {tool.name}")
                return True
            except Exception as e:
                print(f"  ❌ 尝试 {attempt} 失败: {type(e).__name__}")
                if attempt < max_retries:
                    print(f"     等待 2 秒后重试...")
                    await asyncio.sleep(2)
                else:
                    raise
        
    except Exception as e:
        print(f"\n❌ 最终失败: {type(e).__name__}")
        print(f"   错误: {str(e)[:300]}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("尝试不同的 MCP 连接方式\n")
    
    # 测试 1: 显式会话
    r1 = await test_with_explicit_session()
    
    # 测试 2: 带重试的适配器
    if not r1:
        r2 = await test_with_langchain_adapter()
    
    print("\n" + "=" * 70)
    if r1 or r2:
        print("✅ 至少有一种方式成功了!")
    else:
        print("❌ 所有方式都失败了")
        print("\n💡 建议: 尝试降级 mcp 包版本")
        print("   pip install mcp==1.24.0")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
