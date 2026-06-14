"""
飞机射击小游戏 - Flask 服务端
运行: python app.py
浏览器访问: http://127.0.0.1:5000
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """游戏主页"""
    return render_template("index.html")


if __name__ == "__main__":
    print("=" * 50)
    print("  Plane Shooting Game Started!")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
