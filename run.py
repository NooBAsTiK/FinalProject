from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_mysqldb import MySQL
import random
import string
from cryptography.fernet import Fernet
from secret.secret import key
from login.login import (host_encrypt, user_encrypt,
                         password_encrypt, database_encrypt)

# Для получения данных нужно воспользоваться утилитой
super_mega_key = key
cipher = Fernet(super_mega_key)

def decrypt_value(cipher, encrypted_value):
    return cipher.decrypt(encrypted_value).decode()
app = Flask(__name__)

# Настройки подключения к базе данных
app.config['MYSQL_HOST'] = decrypt_value(cipher, host_encrypt)
app.config['MYSQL_USER'] = decrypt_value(cipher, user_encrypt)
app.config['MYSQL_PASSWORD'] = decrypt_value(cipher, password_encrypt)
app.config['MYSQL_DB'] = decrypt_value(cipher, database_encrypt)

mysql = MySQL(app)

def generate_random_nickname():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.before_request
def ensure_user():
    user_id = request.cookies.get('user_id')
    if not user_id:
        nickname = generate_random_nickname()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nickname) VALUES (%s)", (nickname,))
        mysql.connection.commit()
        user_id = cur.lastrowid
        resp = make_response(redirect(request.url))
        resp.set_cookie('user_id', str(user_id))
        return resp

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT articles.id, articles.title
        FROM articles
        GROUP BY articles.id
    """)
    articles = cur.fetchall()
    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        content = request.form.get('content')
        cur.execute("INSERT INTO comments (article_id, user_id, content) VALUES (%s, %s, %s)", (article_id, user_id, content))
        mysql.connection.commit()
    cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cur.fetchone()
    cur.execute("""
        SELECT comments.content, users.nickname
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.article_id = %s
    """, (article_id,))
    comments = cur.fetchall()
    return render_template('article.html', article=article, comments=comments)

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        title = request.form.get('title')
        content = request.form.get('content')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles (title, content, user_id) VALUES (%s, %s, %s)", (title, content, user_id))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('publish.html')

if __name__ == '__main__':
    app.run(debug=True)