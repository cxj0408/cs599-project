"""
简单测试阿里百炼 MCP 服务连接
使用 requests 库（如果有的话）或 urllib
"""
import urllib.request
import urllib.error
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# 可能的端点列表
URLS_TO_TEST = [
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp",
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
    "https://dashscope.aliyuncs.com/api/v1/mcp/amap-maps",
    "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps",
]

def test_url(url: str):
    """测试单个 URL"""
    print(f"\n{'='*60}")
    print(f"测试 URL: {url}")
    print(f"{'='*60}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        # 创建请求
        req = urllib.request.Request(url, headers=headers, method='GET')
        
        # 发送请求
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            content_type = response.headers.get('Content-Type', 'N/A')
            body = response.read().decode('utf-8', errors='ignore')[:300]
            
            print(f"GET 请求:")
            print(f"  状态码: {status_code}")
            print(f"  Content-Type: {content_type}")
            
            if status_code == 200:
                print(f"  ✅ 成功!")
                print(f"  响应预览: {body[:200]}")
                return True
            else:
                print(f"  ⚠️  状态码: {status_code}")
                print(f"  响应: {body[:200]}")
                
    except urllib.error.HTTPError as e:
        status_code = e.code
        body = e.read().decode('utf-8', errors='ignore')[:300]
        
        print(f"HTTP 错误:")
        print(f"  状态码: {status_code}")
        
        if status_code == 404:
            print(f"  ❌ 端点不存在 (404)")
        elif status_code == 401:
            print(f"  ❌ API Key 无效 (401)")
        elif status_code == 500:
            print(f"  ❌ 服务器内部错误 (500)")
            print(f"     可能原因: 未开通高德地图 MCP 服务")
            print(f"  错误详情: {body[:200]}")
        else:
            print(f"  ⚠️  其他错误: {status_code}")
            print(f"  响应: {body[:200]}")
            
    except urllib.error.URLError as e:
        print(f"  ❌ 连接失败: {e.reason}")
    except Exception as e:
        print(f"  ❌ 请求失败: {type(e).__name__}: {e}")
    
    return False


def main():
    print("=" * 60)
    print("阿里百炼 MCP 端点诊断工具")
    print("=" * 60)
    print(f"API Key: {API_KEY[:20]}...")
    print(f"待测试端点数量: {len(URLS_TO_TEST)}")
    
    results = []
    for url in URLS_TO_TEST:
        success = test_url(url)
        results.append((url, success))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    successful_urls = [url for url, success in results if success]
    
    if successful_urls:
        print(f"\n✅ 找到可用的端点 ({len(successful_urls)} 个):")
        for url in successful_urls:
            print(f"  - {url}")
        print(f"\n💡 建议在 .env 文件中设置:")
        print(f"  MCP_URL={successful_urls[0]}")
        print(f"  MCP_TRANSPORT=sse  # 或 streamable_http")
    else:
        print("\n❌ 所有端点都不可用")
        print("\n可能的原因:")
        print("  1. API Key 无效或未开通高德地图 MCP 服务")
        print("  2. 网络连接问题")
        print("  3. 端点地址已变更")
        print("\n建议操作:")
        print("  1. 登录阿里百炼控制台确认服务已开通")
        print("     https://bailian.console.aliyun.com/")
        print("  2. 检查 API Key 是否有效")
        print("  3. 查看阿里百炼文档获取最新的 MCP 端点地址")


if __name__ == "__main__":
    main()
