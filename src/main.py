from flask import Flask, request
from flask_cors import CORS

from src.api import DSS_exchange
from src.feature.diary import diary

FRONT_ADDRESS = "http://localhost:5173"


# 配置服务器
app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii=False
CORS(app, origins=[FRONT_ADDRESS])


# 注册路由路径
@app.route("/diary", methods=["POST"])
def diary_component():
    data = request.get_json()
    return DSS_exchange(diary, data)


# 运行程序
if __name__ == '__main__':
    app.run(debug=True)
