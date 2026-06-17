"""测试阿里百炼 MCP 服务的不同端点"""
import httpx
import asyncio

API_KEY = "sk-3cd555ae15114d8e98423f7255e881f8"

# 可能的端点列表
ENDPOINTS = [
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp",
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/http",
]

async def test_endpoint(url):
    """测试单个端点"""
    print(f"\n{'='*60}")
    print(f"测试端点: {url}")
    print('='*60)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 尝试 GET 请求（SSE 通常支持）
            response = await client.get(
                url,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Accept": "text/event-stream"
                }
            )
            print(f"GET 响应状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ 端点可用！")
                return True
            else:
                print(f"❌ 响应内容: {response.text[:200]}")
                
    except Exception as e:
        print(f"❌ 错误: {type(e).__name__}: {e}")
    
    return False

async def main():
    print(" 开始测试阿里百炼 MCP 端点...")
    
    results = {}
    for endpoint in ENDPOINTS:
        results[endpoint] = await test_endpoint(endpoint)
    
    print("\n" + "="*60)
    print("测试结果汇总:")
    print("="*60)
    for endpoint, success in results.items():
        status = "✅ 可用" if success else "❌ 不可用"
        print(f"{status} - {endpoint}")

if __name__ == "__main__":
    asyncio.run(main())
