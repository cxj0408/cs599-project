# 🔧 MCP 500 错误解决方案

## 问题症状

```
httpx.HTTPStatusError: Server error '500 Internal Server Error' 
for url 'https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse'
```

## 根本原因

**阿里百炼的 MCP 服务需要先在控制台手动开通,否则调用时会返回 500 错误。**

---

## ✅ 解决步骤

### 第一步:开通高德地图 MCP 服务

1. **访问阿里百炼控制台**
   ```
   https://bailian.console.aliyun.com/
   ```

2. **登录阿里云账号**
   - 使用你创建 API Key 的同一个账号

3. **进入 MCP 市场**
   - 在左侧菜单找到 "MCP" 或 "MCP 市场"
   - 或者访问: `https://bailian.console.aliyun.com/?tab=mcp`

4. **找到高德地图服务**
   - 搜索 "高德地图" 或 "Amap Maps"
   - 或直接访问: `https://bailian.console.aliyun.com/?tab=mcp#/mcp-market/detail/amap-maps`

5. **开通服务**
   - 点击 "立即开通" 或 "启用" 按钮
   - 阅读并同意服务协议
   - 确认开通

6. **等待生效**
   - 开通后可能需要等待 1-5 分钟生效
   - 刷新页面确认服务状态为 "已开通" 或 "Enabled"

---

### 第二步:验证开通状态

运行诊断脚本:
```powershell
python check_sse_response.py
```

如果开通成功,应该看到:
```
✅ GET 请求成功!
Content-Type: text/event-stream
```

如果还是 500 错误:
- 等待几分钟后重试
- 确认使用的是正确的 API Key
- 检查是否在正确的区域开通(通常是"华东1-杭州")

---

### 第三步:测试 MCP 连接

```powershell
python test_mcp.py
```

成功输出示例:
```
✅ MCP 客户端管理器创建成功
🔍 正在从 MCP 服务器获取工具列表...
✅ 成功获取 15 个工具
   - maps_weather
   - maps_text_search
   - maps_search_detail
   - maps_direction_walking_by_address
   ...
```

---

### 第四步:启动应用

```powershell
streamlit run app.py
```

---

## 🔍 常见问题

### Q1: 找不到 MCP 市场入口?

**A:** 
- 确保你的阿里云账号已实名认证
- 尝试直接访问: `https://bailian.console.aliyun.com/?tab=mcp`
- 如果还是看不到,联系阿里云客服确认你的账号是否有权限

### Q2: 开通后还是 500 错误?

**A:**
1. **等待生效**: 开通后需要 1-5 分钟生效
2. **清除缓存**: 重启 Python 进程
3. **检查 API Key**: 确认使用的是开通服务时的那个账号的 API Key
4. **检查区域**: 确认服务开通的区域和 API Key 的区域一致

### Q3: 如何确认服务已开通?

**A:**
在阿里百炼控制台的 "我的应用" 或 "已开通服务" 中查看,应该能看到 "高德地图 MCP" 或 "Amap Maps"。

### Q4: 是否需要付费?

**A:**
- 高德地图 MCP 服务本身可能是免费的或有免费额度
- 但调用高德地图 API 可能会产生费用(取决于使用量)
- 建议在控制台查看定价说明

---

## 📞 仍然无法解决?

请提供以下信息:

1. `python check_sse_response.py` 的输出
2. 阿里百炼控制台中 MCP 服务的开通状态截图
3. 你的 API Key 前 20 个字符(用于确认格式)
4. 是否看到任何错误消息或提示

---

## 💡 重要提示

- **必须先开通服务,才能调用 MCP 端点**
- **开通和使用必须是同一个阿里云账号**
- **API Key 必须有调用该服务的权限**
- **某些服务可能有地域限制**
