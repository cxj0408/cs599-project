# 故障排除指南

## 常见问题

### 1. ExceptionGroup: unhandled errors in a TaskGroup

**症状:**
```
ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
File ".../mcp/client/streamable_http.py", line 647, in streamable_http_client
    async with anyio.create_task_group() as tg:
```

**原因分析:**
这个错误通常由以下原因引起:
1. MCP 服务器连接失败（网络问题或 API Key 无效）
2. `langchain-mcp-adapters` 或 `mcp` 包版本不兼容
3. HTTP 请求被防火墙或代理阻止

**解决步骤:**

#### 步骤 1: 运行环境诊断
```bash
python check_env.py
```

检查输出中是否有 ❌ 标记的项目。

#### 步骤 2: 验证 API Key
确保 `.env` 文件中的 `DASHSCOPE_API_KEY` 是有效的：
- 登录阿里百炼控制台: https://dashscope.console.aliyun.com/
- 确认 API Key 未过期且有足够配额

#### 步骤 3: 测试网络连接
```bash
ping dashscope.aliyuncs.com
```

如果无法 ping 通，检查防火墙设置。

#### 步骤 4: 更新依赖包
```bash
pip install --upgrade langchain langchain-community langchain-mcp-adapters mcp anyio
```

#### 步骤 5: 查看详细错误信息
运行测试脚本获取详细错误:
```bash
python test_mcp.py
```

这会显示具体的异常信息和堆栈跟踪。

---

### 2. Redis 连接失败

**症状:**
```
redis.exceptions.ConnectionError: Error connecting to localhost:6379
```

**解决方案:**
在 `.env` 文件中禁用缓存:
```env
MCP_CACHE_ENABLED=false
```

或者安装并启动 Redis 服务。

---

### 3. ModuleNotFoundError

**症状:**
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案:**
安装缺失的依赖:
```bash
pip install -r requirements.txt
```

---

### 4. Streamlit 启动失败

**症状:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**解决方案:**
```bash
pip install streamlit
streamlit run app.py
```

---

## 调试技巧

### 启用详细日志
在运行应用前设置环境变量:
```bash
# PowerShell
$env:LANGCHAIN_VERBOSE="true"
python app.py

# CMD
set LANGCHAIN_VERBOSE=true
python app.py
```

### 检查 MCP 工具加载
运行独立测试:
```bash
python test_mcp.py
```

### 查看完整堆栈跟踪
修改后的代码会自动打印详细的异常信息，包括:
- 异常类型
- 错误消息
- 可能的原因分析
- 建议的解决方案

---

## 联系支持

如果以上步骤都无法解决问题，请提供以下信息:
1. `python check_env.py` 的完整输出
2. `python test_mcp.py` 的错误信息
3. Python 版本: `python --version`
4. 关键依赖版本: `pip list | findstr "langchain mcp"`
