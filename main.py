from flask import Flask, request, jsonify
from flask_cors import CORS

from core.setting import setting
from core.diary import diary
from core.custom_io import DSS_exchange

FRONT_ADDRESS = "http://localhost:5173"


# 初始化服务器
app = Flask(__name__)
app.json.sort_keys = False
app.json.ensure_ascii=False
CORS(app, origins=[FRONT_ADDRESS])


@app.route("/diary", methods=["POST"])
def diary_component():
    data = request.get_json()
    return DSS_exchange(diary, data)

@app.route("/setting", methods=["POST"])
def ref():
    setting.refresh()
    return {
            'message': 'FILE_NO_EXIST',
            'content': '成功刷新配置！'
    }

if __name__ == '__main__':
    app.run(debug=True)
