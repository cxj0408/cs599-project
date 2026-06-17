"""检查详细的包版本信息"""
import subprocess
import sys

packages = [
    "langchain-mcp-adapters",
    "dashscope", 
    "mcp",
    "anyio",
    "python-dotenv",
    "redis",
]

print("=" * 70)
print("📦 详细依赖版本检查")
print("=" * 70)

for pkg in packages:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", pkg],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode == 0:
            # 提取版本信息
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    print(f"✅ {pkg:30s} {line.split(':')[1].strip()}")
                    break
        else:
            print(f"❌ {pkg:30s} 未安装")
    except Exception as e:
        print(f"⚠️  {pkg:30s} 检查失败: {e}")

print("\n" + "=" * 70)
