"""检查项目依赖和环境配置"""
import sys
import os

print("=" * 70)
print("🔍 项目环境诊断")
print("=" * 70)

# Python 版本
print(f"\n📌 Python 版本: {sys.version}")
print(f"   路径: {sys.executable}")

# 检查关键依赖
print("\n📦 已安装的关键依赖:")
packages = [
    "langchain",
    "langchain_community",
    "langchain_mcp_adapters",
    "streamlit",
    "dotenv",
    "dashscope",
    "mcp",
    "anyio",
]

for pkg in packages:
    try:
        module = __import__(pkg.replace("-", "_"))
        version = getattr(module, "__version__", "未知")
        print(f"   ✅ {pkg:30s} {version}")
    except ImportError:
        print(f"   ❌ {pkg:30s} 未安装")

# 检查环境变量
print("\n🔑 环境变量:")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY", "")
if api_key:
    print(f"   ✅ DASHSCOPE_API_KEY: {api_key[:20]}... (长度: {len(api_key)})")
else:
    print(f"   ❌ DASHSCOPE_API_KEY: 未设置")

cache_enabled = os.getenv("MCP_CACHE_ENABLED", "true")
print(f"   📝 MCP_CACHE_ENABLED: {cache_enabled}")

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
print(f"   📝 REDIS_URL: {redis_url}")

# 测试网络连接
print("\n🌐 网络连通性测试:")
import urllib.request

# 测试基础连接
try:
    response = urllib.request.urlopen("https://dashscope.aliyuncs.com", timeout=5)
    print(f"   ✅ 可以访问 dashscope.aliyuncs.com (状态码: {response.status})")
except urllib.error.HTTPError as e:
    print(f"   ⚠️  访问 dashscope.aliyuncs.com 返回 HTTP {e.code}: {e.reason}")
    print(f"      (这可能是正常的,因为根路径可能不存在)")
except Exception as e:
    print(f"   ❌ 无法访问 dashscope.aliyuncs.com: {e}")

# 测试 MCP 端点
mcp_url = os.getenv("MCP_URL", "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp")
print(f"\n   测试 MCP 端点: {mcp_url}")
try:
    req = urllib.request.Request(mcp_url, headers={
        "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY', '')[:20]}..."
    })
    response = urllib.request.urlopen(req, timeout=10)
    print(f"   ✅ MCP 端点可访问 (状态码: {response.status})")
except urllib.error.HTTPError as e:
    print(f"   ⚠️  MCP 端点返回 HTTP {e.code}: {e.reason}")
    if e.code == 404:
        print(f"      💡 URL 路径可能不正确,请检查 MCP 服务地址")
    elif e.code == 401 or e.code == 403:
        print(f"      💡 API Key 可能无效或权限不足")
except Exception as e:
    print(f"   ❌ 无法访问 MCP 端点: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("诊断完成!")
print("=" * 70)
