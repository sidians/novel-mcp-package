import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.database_init import db

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# 启用CORS支持
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 导入路由
from src.routes.user import user_bp
from src.routes.novel import novel_bp
from src.routes.mcp import mcp_bp

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(novel_bp, url_prefix='/api')
app.register_blueprint(mcp_bp, url_prefix='/api/mcp')

# 导入模型以确保表被创建
from src.models.user import User
from src.models.novel import Novel, Chapter, Character, Setting, Outline

# 创建数据库目录
os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    """健康检查端点"""
    return {'status': 'healthy', 'message': 'Novel MCP Server is running'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

