"""快速验证 SSE 配置"""
import asyncio
from config import CONFIG

print("=" * 70)
print("✅ 配置验证")
print("=" * 70)
print(f"MCP Transport: {CONFIG.mcp_transport}")
print(f"MCP URL: {CONFIG.mcp_url}")
print(f"API Key: {CONFIG.api_key[:20]}...")
print(f"Cache Enabled: {CONFIG.cache_enabled}")
print()

# 验证配置是否正确
if CONFIG.mcp_transport == "streamable_http":
    print("✅ Transport 配置正确 (streamable_http)")
else:
    print(f"⚠️  Transport 应该是 'streamable_http',当前是 '{CONFIG.mcp_transport}'")

if "/mcp" in CONFIG.mcp_url and "/sse" not in CONFIG.mcp_url:
    print("✅ URL 配置正确 (streamable-http 端点)")
else:
    print(f"⚠️  URL 应该是 /mcp 端点,当前是: {CONFIG.mcp_url}")

print("\n" + "=" * 70)
print("现在请运行: python test_mcp.py")
print("=" * 70)
