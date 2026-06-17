"""测试不同的 MCP URL 格式"""
import os
import urllib.request
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY", "")

print("=" * 70)
print("🔍 MCP URL 连通性测试")
print("=" * 70)
print(f"API Key: {api_key[:20]}...\n")

# 可能的 URL 格式
urls_to_test = [
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp",
    "https://dashscope.aliyuncs.com/api/v1/mcp/amap-maps",
    "https://dashscope.aliyuncs.com/api/v1/mcp",
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
]

for url in urls_to_test:
    print(f"测试: {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="GET"
        )
        response = urllib.request.urlopen(req, timeout=5)
        print(f"  ✅ HTTP {response.status} - 可访问")
        # 读取少量响应内容
        content = response.read(200).decode('utf-8', errors='ignore')
        if content:
            print(f"     响应预览: {content[:100]}...")
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  HTTP {e.code}: {e.reason}")
        if e.code == 404:
            print(f"     → URL 路径不存在")
        elif e.code == 401 or e.code == 403:
            print(f"     → API Key 无效或权限不足")
        elif e.code == 405:
            print(f"     → 方法不允许 (可能需要 POST)")
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {str(e)[:100]}")
    print()

print("=" * 70)
print("💡 提示:")
print("   - 404 表示 URL 路径不正确")
print("   - 401/403 表示 API Key 问题")
print("   - 如果能访问，查看哪个 URL 返回正确的响应")
print("=" * 70)
