"""修复 mcp 包版本问题"""
import subprocess
import sys

print("=" * 70)
print("🔧 修复 mcp 包版本")
print("=" * 70)

# 当前版本
print("\n当前 mcp 版本:")
result = subprocess.run([sys.executable, "-m", "pip", "show", "mcp"], 
                       capture_output=True, text=True)
for line in result.stdout.split('\n'):
    if line.startswith('Version:'):
        print(f"  {line}")

print("\n" + "=" * 70)
print("尝试方案 1: 升级到最新版本")
print("=" * 70)

upgrade = input("\n是否升级到最新版 mcp? (y/n): ").strip().lower()
if upgrade == 'y':
    print("\n正在升级...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "mcp"])
    print("\n✅ 升级完成!请重新运行: python test_mcp.py")
else:
    print("\n" + "=" * 70)
    print("尝试方案 2: 降级到稳定版本")
    print("=" * 70)
    print("\n推荐的稳定版本:")
    print("  - mcp==1.24.0")
    print("  - mcp==1.23.1")
    print("  - mcp==1.22.0")
    
    version = input("\n请输入要安装的版本号 (例如 1.24.0): ").strip()
    if version:
        print(f"\n正在安装 mcp=={version}...")
        subprocess.run([sys.executable, "-m", "pip", "install", f"mcp=={version}"])
        print(f"\n✅ 安装完成!请重新运行: python test_mcp.py")
    else:
        print("\n已取消")

print("\n" + "=" * 70)
