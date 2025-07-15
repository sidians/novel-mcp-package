#!/bin/bash

# Novel MCP 部署脚本
# 用于快速部署Novel MCP系统

set -e

echo "🚀 开始部署 Novel MCP 系统..."

# 检查Python版本
echo "📋 检查系统环境..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 创建虚拟环境
echo "🔧 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "🔧 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建必要目录..."
mkdir -p src/database
mkdir -p logs
mkdir -p backups

# 检查环境变量
echo "🔍 检查环境变量..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: OPENAI_API_KEY 环境变量未设置"
    echo "   请设置您的OpenAI API密钥："
    echo "   export OPENAI_API_KEY='your-api-key'"
fi

if [ -z "$OPENAI_API_BASE" ]; then
    echo "ℹ️  信息: 使用默认的OpenAI API基础URL"
    export OPENAI_API_BASE="https://api.openai.com/v1"
fi

# 初始化数据库
echo "🗄️  初始化数据库..."
python -c "
import sys
sys.path.insert(0, '.')
from src.main import app, db
with app.app_context():
    db.create_all()
    print('数据库初始化完成')
"

# 创建启动脚本
echo "📝 创建启动脚本..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "🚀 启动 Novel MCP 服务器..."
python src/main.py
EOF

chmod +x start.sh

# 创建停止脚本
echo "📝 创建停止脚本..."
cat > stop.sh << 'EOF'
#!/bin/bash
echo "🛑 停止 Novel MCP 服务器..."
pkill -f "python src/main.py" || echo "服务器未运行"
echo "✅ 服务器已停止"
EOF

chmod +x stop.sh

# 创建备份脚本
echo "📝 创建备份脚本..."
cat > backup.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
timestamp=$(date +"%Y%m%d_%H%M%S")
backup_file="backups/novel_mcp_backup_$timestamp.tar.gz"

echo "💾 创建备份: $backup_file"
tar -czf "$backup_file" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='logs/*.log' \
    .

echo "✅ 备份完成: $backup_file"
EOF

chmod +x backup.sh

# 创建健康检查脚本
echo "📝 创建健康检查脚本..."
cat > health_check.sh << 'EOF'
#!/bin/bash
echo "🔍 检查 Novel MCP 服务状态..."

# 检查进程
if pgrep -f "python src/main.py" > /dev/null; then
    echo "✅ 服务进程运行中"
else
    echo "❌ 服务进程未运行"
    exit 1
fi

# 检查端口
if netstat -tlnp 2>/dev/null | grep -q ":5000 "; then
    echo "✅ 端口5000正在监听"
else
    echo "❌ 端口5000未监听"
    exit 1
fi

# 检查API响应
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ API响应正常"
    curl -s http://localhost:5000/health | python -m json.tool
else
    echo "❌ API无响应"
    exit 1
fi

echo "🎉 Novel MCP 服务运行正常！"
EOF

chmod +x health_check.sh

# 创建配置文件模板
echo "📝 创建配置文件..."
cat > config.env.template << 'EOF'
# Novel MCP 配置文件模板
# 复制此文件为 config.env 并填入您的配置

# OpenAI API配置
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# 服务器配置
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# 数据库配置
DATABASE_URL=sqlite:///src/database/app.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/novel_mcp.log
EOF

echo "✅ 部署完成！"
echo ""
echo "📋 下一步操作："
echo "1. 复制 config.env.template 为 config.env 并配置您的API密钥"
echo "2. 运行 ./start.sh 启动服务"
echo "3. 运行 ./health_check.sh 检查服务状态"
echo "4. 访问 http://localhost:5000/health 验证服务"
echo ""
echo "📚 更多信息请查看 README.md 和用户指南"
echo "🎉 Novel MCP 部署完成！"

