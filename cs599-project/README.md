# 🧳 智能旅行助手 (AI Travel Agent)

## 项目简介
基于 Multi-Agent 架构的智能旅行规划系统，集成高德地图 MCP 服务，输入目的地、日期和偏好，AI 自动调用天气查询、景点搜索、酒店推荐、路线规划等工具，生成包含完整行程和预算的旅行方案。

## 方向
**方向一：Agentic AI 原生开发**

本项目从零开始构建多层 Agent 系统，包括总控编排 Agent、领域专家 Agent（天气/景点/酒店），通过 MCP 协议集成外部工具服务，实现自主决策和任务分解。

## 技术栈
- **LLM**: 通义千问 qwen3-max (阿里百炼 DashScope API)
- **Agent 框架**: LangChain + LangGraph
- **MCP 协议**: langchain-mcp-adapters 0.2.2 + mcp 1.24.0
- **Web 界面**: Streamlit 1.58.0
- **配置管理**: python-dotenv
- **运行环境**: Python 3.12+
- **缓存**: Redis (可选，默认禁用)

## 目录结构

```
travel-agent-main/
├── agents/                      # Agent 核心模块
│   ├── planner.py              # 总控编排 Agent：协调子 Agent，整合结果
│   └── specialist.py           # 领域专家 Agent：POI搜索/天气查询/酒店推荐
├── config.py                    # 配置中心：API Key、模型参数、MCP 连接配置
├── mcp_client.py                # MCP 客户端管理器：单例模式，按领域分发工具
├── mcp_cache.py                 # Redis 缓存层：可选功能，缓存 MCP 工具调用结果
├── prompts.py                   # System Prompt 集中管理：5 个 Agent 提示词
├── render.py                    # 渲染引擎：JSON 解析 + CLI/Web 格式化输出
├── Agent.py                     # CLI 入口：命令行交互模式
├── app.py                       # Web 入口：Streamlit 图形界面
├── .env                         # 环境变量配置（不提交到版本控制）
├── requirements.txt             # Python 依赖清单
└── README.md                    # 项目文档
```

### 核心模块职责

| 模块 | 职责 |
|------|------|
| `agents/planner.py` | TripPlanner 总控 Agent，负责加载 MCP 工具、创建子 Agent、包装为 Tool、执行流式输出 |
| `agents/specialist.py` | SpecialistAgent 领域专家，封装单一职责的 ReAct Agent（天气/景点/酒店） |
| `mcp_client.py` | McpClientManager 单例，管理与阿里百炼 MCP 服务器的连接，按领域分发工具 |
| `config.py` | Config 配置中心，统一管理 API Key、模型参数、MCP 连接参数，包含 ChatTongyi Monkey-Patch |
| `prompts.py` | 集中管理 5 个 System Prompt，便于调优和版本管理 |
| `render.py` | 将 Planner 输出的 JSON 转换为可视化格式（CLI Unicode / Web Markdown） |
| `app.py` | Streamlit Web 界面，侧边栏参数输入 + 主区域结果展示 + Markdown 导出 |

## 环境搭建

### 1. 依赖安装

```bash
# 创建虚拟环境
conda create -n travel-agent python=3.12
conda activate travel-agent

# 安装核心依赖
pip install langchain langchain-community langchain-mcp-adapters==0.2.2
pip install streamlit python-dotenv dashscope
pip install mcp==1.24.0

# 可选：Redis 缓存支持（如需要启用缓存）
pip install redis
```

### 2. 环境变量配置

在项目根目录创建 `.env` 文件（**不要硬编码 API Key**）：

```env
# 阿里百炼 API Key（必需）
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# MCP 缓存配置（可选，默认禁用）
MCP_CACHE_ENABLED=false
# REDIS_URL=redis://localhost:6379/0

# MCP 服务配置（可选，使用默认值即可）
# MCP_TRANSPORT=streamable_http
# MCP_URL=https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/mcp
```

> ⚠️ **重要提示**：
> 1. **必须先在阿里百炼控制台开通高德地图 MCP 服务**，否则会返回 500 错误
>    - 访问：https://bailian.console.aliyun.com/?tab=mcp
>    - 找到 "高德地图 (Amap Maps)" MCP 服务
>    - 点击 "立即开通" 并确认
>    - 等待 1-5 分钟生效
> 2. API Key 申请地址：https://dashscope.console.aliyun.com/

### 3. 启动步骤

#### Web 模式（推荐）

```bash
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`，在侧边栏填写旅行参数，点击"开始规划"。

#### CLI 模式

```bash
python Agent.py
```

修改 `Agent.py` 中 `main()` 函数的 `user_input` 变量来自定义查询内容。

### 4. 验证安装

运行诊断脚本确认配置正确：

```bash
# 环境检查
python check_env.py

# MCP 连接测试
python test_mcp.py

# 配置验证
python verify_config.py
```

成功输出示例：
```
✅ MCP 客户端管理器创建成功
✅ 成功获取 15 个工具:
   - maps_weather
   - maps_text_search
   - maps_direction_walking
   ...
```

## 项目状态

- [x] Proposal - 项目提案完成
- [x] MVP - 最小可行产品完成
  - [x] Multi-Agent 架构实现
  - [x] MCP 工具集成（15 个高德地图工具）
  - [x] CLI 和 Web 双界面
  - [x] 流式输出支持
  - [x] Markdown 导出功能
  - [x] 完整的错误处理和诊断工具
- 
[ ] Final - 最终版本
  - [ ] 性能优化（响应速度、Token 消耗）
  - [ ] 更多 MCP 服务集成（餐饮、机票、酒店预订）
  - [ ] 用户偏好学习（基于历史行程推荐）
  - [ ] 多语言支持
  - [ ] 移动端适配
  - [ ] Docker 容器化部署
---

---


## 技术亮点

1. **三层 Agent 架构**: Planner (总控) → SpecialistAgent (领域) → MCP Tools (底层 API)
2. **子 Agent 作为 Tool**: 通过 `@tool` 装饰器将 SpecialistAgent 封装为 LangChain Tool
3. **Streamable-HTTP 协议**: 正确使用阿里百炼的 MCP 实现方式
4. **单例模式**: McpClientManager 保证全局唯一 MCP 连接
5. **Monkey-Patch**: 修复 langchain_community 的流式 tool_calls bug
6. **Fail-Open 设计**: Redis 缓存失败时自动降级，不影响核心功能

