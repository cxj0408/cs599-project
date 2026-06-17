"""检查 langchain-mcp-adapters 版本和兼容性"""
import subprocess
import sys

print("=" * 70)
print("📦 检查关键依赖版本")
print("=" * 70)

packages = ["mcp", "langchain-mcp-adapters", "anyio", "httpx"]

for pkg in packages:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", pkg],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        version = None
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                version = line.split(':')[1].strip()
                break
        print(f"✅ {pkg:30s} {version}")
    else:
        print(f"❌ {pkg:30s} 未安装")

print("\n" + "=" * 70)
print("💡 建议的兼容版本组合:")
print("=" * 70)
print("  mcp==1.24.0")
print("  langchain-mcp-adapters==0.2.2")
print("  anyio>=4.5,<5.0")
print("  httpx>=0.27,<1.0")
print("\n如果问题持续,尝试:")
print("  pip install --upgrade langchain-mcp-adapters")
print("=" * 70)
