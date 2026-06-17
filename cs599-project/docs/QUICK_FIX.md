# 🚀 快速诊断与修复指南

## 📋 当前状态

✅ Python 3.12.13  
✅ langchain 1.3.4  
✅ streamlit 1.58.0  
✅ langchain-mcp-adapters 0.2.2  
✅ dashscope 1.25.20  
✅ mcp 1.27.2  
✅ anyio 4.13.0  
✅ API Key 已配置  

---

## 🔧 立即执行的诊断步骤

### 步骤 1: 测试 MCP URL 连通性
```powershell
python test_mcp_urls.py
```

**目的**: 找出哪个 MCP 端点 URL 是可用的

**预期结果**: 
- 如果某个 URL 返回 200 或其他成功状态码 → 记录这个 URL
- 如果所有都返回 404 → MCP 服务路径可能不正确
- 如果返回 401/403 → API Key 有问题

---

### 步骤 2: 测试不同的 Transport 配置
```powershell
python test_transport.py
```

**目的**: 找出哪种 transport 类型可以成功连接

**会测试**:
- `http` - 标准 HTTP 传输
- `sse` - Server-Sent Events
- `streamable_http` - 流式 HTTP (langchain-mcp-adapters 0.2.x 新特性)

**预期结果**: 至少有一种 transport 能成功获取工具列表

---

### 步骤 3: 根据测试结果配置

#### 情况 A: test_mcp_urls.py 找到了可用的 URL

在 `.env` 文件中设置:
```env
MCP_URL=找到的可用URL
```

#### 情况 B: test_transport.py 找到了可用的 transport

在 `.env` 文件中设置:
```env
MCP_TRANSPORT=成功的transport类型
```

#### 情况 C: 两者都失败了

请检查:
1. **API Key 是否有效**
   - 登录 https://dashscope.console.aliyun.com/
   - 确认 API Key 未过期且有配额
   
2. **网络连接**
   ```powershell
   ping dashscope.aliyuncs.com
   ```
   
3. **防火墙/代理**
   - 如果使用代理,设置环境变量:
   ```powershell
   $env:HTTP_PROXY="http://your-proxy:port"
   $env:HTTPS_PROXY="http://your-proxy:port"
   ```

---

### 步骤 4: 完整测试
```powershell
python test_mcp.py
```

如果成功,会显示:
```
✅ MCP 客户端管理器创建成功
✅ 成功获取 X 个工具:
   - maps_weather
   - maps_text_search
   ...
```

---

### 步骤 5: 启动应用
```powershell
streamlit run app.py
```

---

## 🎯 常见问题速查

### Q1: ExceptionGroup 错误
**原因**: MCP 连接失败  
**解决**: 运行 `test_transport.py` 找到正确的 transport

### Q2: 404 Not Found
**原因**: URL 路径不正确  
**解决**: 运行 `test_mcp_urls.py` 找到正确的 URL

### Q3: 401 Unauthorized
**原因**: API Key 无效  
**解决**: 检查 `.env` 中的 DASHSCOPE_API_KEY

### Q4: Connection Timeout
**原因**: 网络问题或需要代理  
**解决**: 配置代理或检查防火墙

---

## 📞 需要帮助?

如果以上步骤都无法解决问题,请提供以下信息:

1. `python test_mcp_urls.py` 的完整输出
2. `python test_transport.py` 的完整输出
3. `python test_mcp.py` 的错误信息
4. 你的网络环境(是否需要代理?)

---

## 💡 提示

- 每次修改 `.env` 后需要重启 Python 进程
- Streamlit 会缓存 planner 实例,修改配置后需要完全停止并重新启动
- 查看控制台输出可以获得更详细的错误信息
