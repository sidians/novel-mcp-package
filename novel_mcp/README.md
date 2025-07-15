# Novel MCP - AI小说创作智能助手

Novel MCP是一个专为AI小说创作设计的多智能体协作平台(Multi-Agent Collaboration Platform)，通过智能知识库管理、内容生成和质量审核，解决AI创作中的知识遗忘和内容连贯性问题。

## 🌟 核心特性

### 智能知识库管理
- 结构化存储小说的人物、世界观、大纲等信息
- 基于上下文的智能知识检索
- 动态知识更新和版本管理

### 多智能体协作
- **知识库管理智能体**：负责知识检索和管理
- **写作助手智能体**：负责内容生成和优化  
- **内容审核智能体**：负责质量检查和一致性分析

### 内容质量保证
- 多维度内容质量评估
- 人物一致性检查
- 情节逻辑连贯性分析
- 世界观设定一致性验证

### 易于集成
- RESTful API接口设计
- 支持与Cherry Studio等AI工具集成
- 跨平台部署支持

## 🚀 快速开始

### 系统要求
- Python 3.8+
- 4GB+ RAM
- 稳定的网络连接（用于AI服务）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd novel_mcp
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"
```

5. **启动服务**
```bash
python src/main.py
```

服务将在 http://localhost:5000 启动

### 基础使用示例

1. **创建小说项目**
```bash
curl -X POST http://localhost:5000/api/novels \
  -H "Content-Type: application/json" \
  -d '{"title": "我的小说", "description": "小说描述"}'
```

2. **添加人物设定**
```bash
curl -X POST http://localhost:5000/api/novels/1/characters \
  -H "Content-Type: application/json" \
  -d '{"name": "主角", "description": "人物描述", "personality": "性格特征"}'
```

3. **生成章节内容**
```bash
curl -X POST http://localhost:5000/api/mcp/generate-chapter \
  -H "Content-Type: application/json" \
  -d '{"novel_id": 1, "context": "创作上下文", "requirements": "特殊要求"}'
```

## 📖 详细文档

- [用户指南](novel_mcp_user_guide.md) - 完整的使用指南和最佳实践
- [API文档](novel_mcp_user_guide.md#api接口说明) - 详细的API接口说明
- [架构设计](mcp_architecture.md) - 系统架构和设计理念
- [演示报告](novel_mcp_demo.md) - 功能演示和测试结果

## 🔧 与Cherry Studio集成

Novel MCP可以无缝集成到Cherry Studio中，提供专业的小说创作能力：

1. 在Cherry Studio中配置Novel MCP为自定义AI服务提供商
2. 设置API基础URL为 `http://localhost:5000/api`
3. 使用自然语言指令调用Novel MCP功能

详细集成步骤请参考[用户指南](novel_mcp_user_guide.md#与cherry-studio集成)。

## 🏗️ 项目结构

```
novel_mcp/
├── src/
│   ├── main.py              # 主应用入口
│   ├── database_init.py     # 数据库初始化
│   ├── models/              # 数据模型
│   │   ├── user.py
│   │   └── novel.py
│   ├── routes/              # API路由
│   │   ├── user.py
│   │   ├── novel.py
│   │   └── mcp.py
│   └── services/            # 核心服务
│       ├── knowledge_manager.py
│       ├── writing_assistant.py
│       └── content_reviewer.py
├── requirements.txt         # 依赖包列表
├── README.md               # 项目说明
└── docs/                   # 文档目录
```

## 🤝 贡献指南

我们欢迎社区贡献！请参考以下方式参与：

1. **报告问题**：在GitHub Issues中报告bug或提出功能请求
2. **代码贡献**：Fork项目，创建分支，提交Pull Request
3. **文档改进**：帮助改进文档和教程
4. **社区支持**：在论坛中帮助其他用户

## 📄 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

## 🆘 技术支持

- **文档**：查看[用户指南](novel_mcp_user_guide.md)和[常见问题](novel_mcp_user_guide.md#常见问题解答)
- **社区**：加入我们的用户论坛
- **邮件**：support@novel-mcp.com

## 🎯 路线图

### v1.1 (计划中)
- [ ] Web用户界面
- [ ] 更多AI模型支持
- [ ] 高级情节分析功能

### v1.2 (计划中)
- [ ] 多用户支持
- [ ] 云端部署方案
- [ ] 移动端适配

### v2.0 (远期规划)
- [ ] 实时协作编辑
- [ ] 智能插图生成
- [ ] 多语言支持

---

**Novel MCP** - 让AI创作更智能，让故事更连贯！

---
### ModelScope 一键部署配置
```yaml
service:
  name: novel-mcp
  image: python:3.11-slim
  port: 5000
  command: |
    pip install -r requirements.txt &&
    python src/main.py
  env:
    GEMINI_API_KEY: ${MODELSCOPE_API_KEY}

