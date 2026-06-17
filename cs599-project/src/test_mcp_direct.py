"""直接测试 MCP 连接,绕过 langchain-mcp-adapters"""
import asyncio
import httpx
from config import CONFIG


async def test_mcp_direct():
    """直接使用 HTTP 请求测试 MCP 服务"""
    print("=" * 70)
    print("🔍 直接 MCP 协议测试")
    print("=" * 70)
    print(f"URL: {CONFIG.mcp_url}")
    print(f"API Key: {CONFIG.api_key[:20]}...")
    print()
    
    # MCP 协议初始化消息
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 尝试 POST 请求 (MCP 通常使用 POST)
            print("尝试 POST 请求 (MCP initialize)...")
            response = await client.post(
                CONFIG.mcp_url,
                json=init_message,
                headers={
                    "Authorization": f"Bearer {CONFIG.api_key}",
                    "Content-Type": "application/json",
                }
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ POST 请求成功!")
                try:
                    data = response.json()
                    print(f"响应内容: {data}")
                except:
                    print(f"响应文本: {response.text[:500]}")
            else:
                print(f"❌ POST 请求失败: {response.status_code}")
                print(f"响应: {response.text[:500]}")
                
    except Exception as e:
        print(f"❌ 请求失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("尝试 GET 请求...")
    print("=" * 70)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                CONFIG.mcp_url,
                headers={
                    "Authorization": f"Bearer {CONFIG.api_key}",
                }
            )
            
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ GET 请求成功!")
                print(f"响应: {response.text[:500]}")
            else:
                print(f"响应: {response.text[:500]}")
                
    except Exception as e:
        print(f"❌ GET 请求失败: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_direct())
