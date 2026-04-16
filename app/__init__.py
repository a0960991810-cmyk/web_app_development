import os
import sqlite3
from flask import Flask

def init_db(app):
    """根據 schema.sql 初始化資料庫"""
    db_path = os.path.join(app.instance_path, 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    
    # 確保 instance 資料夾存在才能存放 db 檔案
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 如果資料庫檔案不存在，則透過以 schema.sql 初始化
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("已初始化資料庫。")

def get_db_connection():
    """建立資料庫連線並回傳連線物件，供 Model 邏輯使用"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 讓回傳的 record 可以用 dict 的方式取值
    return conn

def create_app():
    """Flask Application Factory 啟動函數"""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev'),
    )

    # 確保 instance_path 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    init_db(app)

    # 註冊 Blueprints
    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    return app
