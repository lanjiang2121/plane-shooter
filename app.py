"""
飞机射击小游戏 - Flask 服务端
运行: python app.py
浏览器访问: http://127.0.0.1:5000
"""

import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)

# 数据库路径
DATABASE = os.path.join(os.path.dirname(__file__), 'leaderboard.db')


def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """初始化数据库表"""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()


@app.route("/")
def index():
    """游戏主页"""
    return render_template("index.html")


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """获取排行榜前10名"""
    db = get_db()
    rows = db.execute(
        'SELECT score, created_at FROM leaderboard ORDER BY score DESC LIMIT 10'
    ).fetchall()
    result = []
    for row in rows:
        result.append({
            'score': row['score'],
            'date': row['created_at']
        })
    return jsonify(result)


@app.route("/api/leaderboard", methods=["POST"])
def save_score():
    """保存分数到排行榜（保留前50条）"""
    data = request.get_json()
    score = data.get('score', 0)

    if score <= 0:
        return jsonify({'ok': False, 'message': '分数必须大于0'})

    db = get_db()
    db.execute('INSERT INTO leaderboard (score) VALUES (?)', (score,))
    db.commit()

    # 清理：只保留前50条高分记录
    db.execute('''
        DELETE FROM leaderboard WHERE id NOT IN (
            SELECT id FROM leaderboard ORDER BY score DESC LIMIT 50
        )
    ''')
    db.commit()

    return jsonify({'ok': True})


if __name__ == "__main__":
    # 初始化数据库
    if not os.path.exists(DATABASE):
        init_db()
        print("数据库已初始化")
    else:
        # 确保表存在
        init_db()

    print("=" * 50)
    print("  Plane Shooting Game Started!")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
