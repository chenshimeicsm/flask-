from flask import Flask, app, session, g
import config
from blueprints import qa_bp, user_bp
from exts import db, mail
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

mail.init_app(app)
migrate = Migrate(app, db)

# 在所有请求之前会执行的函数
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个user属性，这个属性就是user这个变量
            # setattr(g, "user", user)
            g.user = user
        except:
            g.user = None
# 请求来了 -> before_request -> 视图函数 -> 摄图函数中返回模板 -> context_processor
# 渲染的所有的模板都会执行这个函数
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run()
