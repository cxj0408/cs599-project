"""检查 SSE 端点的详细响应"""
import requests
from config import CONFIG


def check_sse_endpoint():
    print("=" * 70)
    print("🔍 检查 SSE 端点响应")
    print("=" * 70)
    print(f"URL: {CONFIG.mcp_url}")
    print(f"API Key: {CONFIG.api_key[:20]}...")
    print()
    
    # 尝试 GET 请求 (SSE 通常用 GET 建立连接)
    print("1. GET 请求测试:")
    try:
        response = requests.get(
            CONFIG.mcp_url,
            headers={
                "Authorization": f"Bearer {CONFIG.api_key}",
                "Accept": "text/event-stream",
            },
            timeout=10,
            stream=True  # SSE 需要流式
        )
        
        print(f"   状态码: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            print("   ✅ GET 请求成功!")
            # 读取少量 SSE 数据
            content = response.text[:500]
            print(f"   响应预览:\n{content}")
        else:
            print(f"   ❌ 失败: {response.status_code}")
            print(f"   响应: {response.text[:500]}")
            
    except Exception as e:
        print(f"   ❌ 异常: {type(e).__name__}: {e}")
    
    print("\n" + "=" * 70)
    print("2. 检查是否需要开通服务")
    print("=" * 70)
    print()
    print("💡 重要提示:")
    print("   阿里百炼的 MCP 服务需要先在控制台开通才能使用!")
    print()
    print("   开通步骤:")
    print("   1. 访问: https://bailian.console.aliyun.com/")
    print("   2. 进入 'MCP 市场' 或 'MCP 服务'")
    print("   3. 找到 '高德地图 (Amap Maps)' MCP 服务")
    print("   4. 点击 '立即开通' 或 '启用'")
    print("   5. 确认开通后等待生效(可能需要几分钟)")
    print()
    print("   开通后再运行测试!")
    print("=" * 70)


if __name__ == "__main__":
    check_sse_endpoint()
