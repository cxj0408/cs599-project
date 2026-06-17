"""详细检查 SSE 流内容"""
import asyncio
import httpx
from config import CONFIG


async def inspect_sse_stream():
    """检查 SSE 流的实际内容"""
    print("=" * 70)
    print("🔍 详细检查 SSE 流")
    print("=" * 70)
    print(f"URL: {CONFIG.mcp_url}")
    print()
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print("正在建立 SSE 连接...")
            
            async with client.stream(
                "GET",
                CONFIG.mcp_url,
                headers={
                    "Authorization": f"Bearer {CONFIG.api_key}",
                    "Accept": "text/event-stream",
                }
            ) as response:
                print(f"状态码: {response.status_code}")
                print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
                print()
                
                if response.status_code != 200:
                    print(f"❌ 非 200 状态码")
                    content = await response.aread()
                    print(f"响应内容: {content.decode('utf-8', errors='ignore')[:500]}")
                    return
                
                print("✅ 连接成功,开始读取 SSE 事件...")
                print("-" * 70)
                
                # 读取前几个 SSE 事件
                event_count = 0
                max_events = 10
                buffer = ""
                
                async for chunk in response.aiter_bytes(chunk_size=1024):
                    buffer += chunk.decode('utf-8', errors='ignore')
                    
                    # 按行分割
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.rstrip('\r')
                        
                        if line:
                            print(f"[{event_count}] {line}")
                            event_count += 1
                            
                            if event_count >= max_events:
                                print("\n... (已显示前10个事件)")
                                return
                
                if buffer:
                    print(f"[{event_count}] {buffer}")
                
                print("-" * 70)
                print(f"\n总共接收到 {event_count} 个事件")
                
    except Exception as e:
        print(f"\n❌ 异常: {type(e).__name__}")
        print(f"   错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(inspect_sse_stream())
