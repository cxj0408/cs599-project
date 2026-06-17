"""检查 MCP 端点返回的实际内容"""
import requests
from config import CONFIG


def check_endpoint():
    print("=" * 70)
    print("🔍 检查 MCP 端点响应内容")
    print("=" * 70)
    print(f"URL: {CONFIG.mcp_url}\n")
    
    # GET 请求
    print("1. GET 请求:")
    response = requests.get(
        CONFIG.mcp_url,
        headers={
            "Authorization": f"Bearer {CONFIG.api_key}",
        },
        timeout=10
    )
    
    print(f"   状态码: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"   响应长度: {len(response.text)} 字节")
    
    if response.status_code == 200:
        print(f"\n   响应内容预览 (前1000字符):")
        print("   " + "-" * 66)
        # 显示前1000个字符
        content = response.text[:1000]
        for line in content.split('\n')[:20]:
            print(f"   {line}")
        if len(response.text) > 1000:
            print(f"   ... (还有 {len(response.text) - 1000} 字符)")
    
    print("\n" + "=" * 70)
    
    # 尝试不带 Authorization header
    print("2. GET 请求 (不带 Authorization):")
    response2 = requests.get(CONFIG.mcp_url, timeout=10)
    print(f"   状态码: {response2.status_code}")
    if response2.status_code == 200:
        print(f"   响应预览: {response2.text[:200]}")
    
    print("\n" + "=" * 70)
    
    # 尝试查看是否有文档或说明
    print("3. 检查常见 MCP 端点变体:")
    
    variants = [
        CONFIG.mcp_url,
        CONFIG.mcp_url.rstrip('/'),
        CONFIG.mcp_url + '/',
        CONFIG.mcp_url.replace('/mcp', ''),
        'https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps',
    ]
    
    for url in variants:
        try:
            resp = requests.get(url, timeout=5)
            print(f"   {url}")
            print(f"      → {resp.status_code} ({len(resp.text)} bytes)")
        except Exception as e:
            print(f"   {url}")
            print(f"      → Error: {e}")


if __name__ == "__main__":
    check_endpoint()
