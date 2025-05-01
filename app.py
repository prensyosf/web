from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)

# إنشاء قاعدة البيانات تلقائيًا عند التشغيل
def init_db():
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute("SELECT * FROM videos")
    videos = c.fetchall()
    conn.close()
    if videos:
        video = random.choice(videos)
        return render_template("index.html", video=video)
    else:
        return render_template("index.html", video=None)

@app.route('/add', methods=['GET', 'POST'])
def add_video():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        conn = sqlite3.connect('videos.db')
        c = conn.cursor()
        c.execute("INSERT INTO videos (title, url) VALUES (?, ?)", (title, url))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
