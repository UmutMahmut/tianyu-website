from flask import Flask

def create_app():
    print("正在创建 Flask 应用...")  # 调试信息
    app = Flask(__name__)
    app.secret_key = 'any-secret-key'
    
    print("正在导入 routes...")  # 调试信息
    from .routes import main
    print("routes 导入成功！")  # 调试信息
    
    print("正在注册蓝图...")  # 调试信息
    app.register_blueprint(main)
    print("蓝图注册成功！")  # 调试信息
    
    # 打印所有注册的路由
    print("已注册的路由：")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    return app