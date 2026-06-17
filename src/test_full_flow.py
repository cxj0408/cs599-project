"""测试完整的旅行规划流程"""
import asyncio
from config import CONFIG
from agents.planner import TripPlanner


async def test_full_planning():
    """测试从创建 Planner 到生成方案的完整流程"""
    print("=" * 70)
    print("🧪 测试完整旅行规划流程")
    print("=" * 70)
    
    # 1. 创建 LLM
    print("\n1. 创建 LLM...")
    llm = CONFIG.create_llm()
    print(f"   ✅ LLM 创建成功: {CONFIG.model_name}")
    
    # 2. 创建 Planner
    print("\n2. 创建 TripPlanner...")
    planner = TripPlanner(llm)
    print("   ✅ Planner 创建成功")
    
    # 3. Build (加载 MCP 工具)
    print("\n3. 构建 Planner (加载 MCP 工具)...")
    await planner.build()
    print("   ✅ Planner 构建成功")
    
    # 4. 测试 prompt
    prompt = "杭州3日游，2026年6月15日-2026年6月17日，喜欢自然风光和美食，中等预算"
    print(f"\n4. 测试 prompt: {prompt[:50]}...")
    
    # 5. 流式输出测试
    print("\n5. 开始流式生成方案...")
    print("-" * 70)
    
    full_text = ""
    token_count = 0
    
    try:
        async for token in planner.stream(prompt):
            full_text += token
            token_count += 1
            # 只打印前100个token作为示例
            if token_count <= 100:
                print(token, end="", flush=True)
        
        print("\n" + "-" * 70)
        print(f"\n✅ 生成完成! 共 {token_count} 个 token")
        print(f"   总长度: {len(full_text)} 字符")
        
        # 6. 解析结果
        print("\n6. 解析 JSON 结果...")
        from render import parse_plan
        plan = parse_plan(full_text)
        
        if plan:
            print(f"   ✅ 解析成功!")
            print(f"   城市: {plan.get('city', 'N/A')}")
            print(f"   天数: {len(plan.get('days', []))}")
            print(f"   预算总计: ¥{plan.get('budget', {}).get('total', 0)}")
        else:
            print("   ⚠️  解析失败,返回 None")
            print(f"   原始文本预览: {full_text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 生成失败: {type(e).__name__}")
        print(f"   错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_full_planning())
    
    print("\n" + "=" * 70)
    if result:
        print("✅ 完整流程测试成功!")
        print("   Web 界面应该也能正常工作")
    else:
        print("❌ 完整流程测试失败")
        print("   请检查上面的错误信息")
    print("=" * 70)
