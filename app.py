from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import sqlite3
from datetime import datetime, timedelta
import math

app = Flask(__name__)
app.secret_key = "your_secret_key"

#データベースの作成及び参照のための関数
def create_conn():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS books (isbn INTEGER PRIMARY KEY, title TEXT, author TEXT, pages INTEGER, publisher TEXT)")
    return conn

#読了予定日を格納するテーブルの作成及び参照のための関数
def create_conn_date():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS input_date (date Date)")
    return conn

#一日に読むべきページ数を格納するテーブルの作成及び参照のための関数
def create_conn_pages():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS input_pages (pages INTEGER)")
    return conn

#データベースの内容を画面に表示するための関数
def display():
    conn = create_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    c.execute("SELECT sum(pages) FROM books")
    total_pages = c.fetchone()[0]
    conn.close()
    return books,total_pages

#トップページ
@app.route("/")
def index():
    books, total_pages = display()
    return render_template("index.html", books=books, total_pages=total_pages)


#入力されたISBNコードから本を検索し,データベースに追加する関数
@app.route("/search", methods=["GET", "POST"])
def search():
    conn = create_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    c.execute("SELECT sum(pages) FROM books")
    total_pages = c.fetchone()[0]
    if request.method == "GET":
        return render_template("search.html", books=books, total_pages=total_pages)
    else:
        isbn = request.form["isbn"]

        #openBDを検索に利用
        response = requests.get("https://api.openbd.jp/v1/get?isbn=" + isbn)
        data = response.json()

        #ISBNが存在しない場合
        if data[0] is None:
            flash("No book found for ISBN {}".format(isbn), "error")
            return render_template("search.html", books=books, total_pages=total_pages)


        #本のタイトル,著者,ページ数,出版社を取得
        title = data[0]["summary"]["title"]
        contributors = data[0].get("onix", {}).get("DescriptiveDetail", {}).get("Contributor", [])
        author_list = [contributor.get("PersonName", {}).get("content", "") for contributor in contributors]
        author = ", ".join(author_list)

        #ページ数がデータベースに記載されていない場合
        if data[0]["onix"]["DescriptiveDetail"].get("Extent", None) is None:
            flash("This book is not supported. (ISBN: {})".format(isbn), "error")
            return render_template("search.html", books=books, total_pages=total_pages)
        extent = data[0]["onix"]["DescriptiveDetail"]["Extent"][0]["ExtentValue"]
        publisher = data[0]["summary"]["publisher"]

        #既にデータベースにある本のISBNを調べた場合
        c.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        existing_book = c.fetchone()
        if existing_book:
            flash("Book with ISBN \"{}\" already exists.".format(isbn), "error")
            return render_template("search.html", books=books, total_pages=total_pages)

        #値をデータベースに代入
        c.execute("INSERT INTO books (isbn, title, author, pages, publisher) VALUES (?, ?, ?, ?, ?)", (isbn, title, author, extent, publisher))
        conn.commit()
        conn.close()
        books, total_pages = display()
        return render_template("search.html", books=books, total_pages=total_pages)


#読書終了予定日の入力とページ数の計算を行う関数
@app.route("/pages", methods=["GET", "POST"])
def pages():
    conn = create_conn_date()
    c = conn.cursor()

    # データベースに書籍が存在する場合は、書籍の情報とページ数を取得する
    books, total_pages = display() if display() is not None else (None, 0)

    if request.method == "POST":
        # フォームから日付を取得
        date_input = request.form["date"]

        if date_input is None:
            flash("Invalid date format", "error")
            return render_template("pages.html", books=books, total_pages=total_pages)

        try:
            # 日付をdatetimeオブジェクトに変換
            input_date = datetime.strptime(date_input, '%Y-%m-%d')
        except ValueError:
            # 不適切な日付の場合はエラーメッセージを表示
            flash("The input date is invalid date format.", "error")
            return render_template("pages.html", books=books, total_pages=total_pages)

        today = datetime.now()
        if input_date <= today:
            # 未来の日付でない場合はエラーメッセージを表示
            flash("Date must be in the future.", "error")
            return render_template("pages.html", books=books, total_pages=total_pages)

        c.execute("SELECT * FROM input_date")
        data = c.fetchall()

        #テーブルに値があるかどうかで条件分岐
        if not data:
            c.execute("INSERT INTO input_date (date) VALUES (?)", (date_input,))
            conn.commit()
        else:
            c.execute("UPDATE input_date SET date = ?", (date_input,))
            conn.commit()

        conn.close()

        # 日数と日ごとのページ数を計算
        delta = input_date - today
        days = delta.days + 1
        pages_per_day = math.ceil(total_pages / days)

        # ページを表示
        return render_template("pages.html", books=books, total_pages=total_pages, input_date=input_date, days=days, pages_per_day=pages_per_day)

    else:
        c.execute("SELECT * FROM input_date")
        data = c.fetchone()

        #booksテーブルが空の時
        if not books:
            return render_template("pages.html")

        #読了予定日がテーブルに格納されている時
        if data:
            input_date = datetime.strptime(data[0], '%Y-%m-%d')
            delta = input_date - datetime.now()
            days = delta.days + 1
            pages_per_day = math.ceil(total_pages / days)
        else:
            input_date = None
            days = None
            pages_per_day = None

        conn.close()

        if total_pages is None:
            return render_template("pages.html")
        else:
            return render_template("pages.html", books=books, total_pages=total_pages, input_date=input_date, days=days, pages_per_day=pages_per_day)


#読書終了予定日の入力とページ数の計算を行う関数
@app.route("/days", methods=["GET", "POST"])
def days():
    books, total_pages = display()
    conn = create_conn_pages()
    c = conn.cursor()
    c.execute("SELECT * FROM input_pages")
    data = c.fetchone()  # data にアクセス

    if request.method == "POST":
        try:
            pages_per_day = int(request.form["pages_per_day"])

        # 入力が不適切な場合
        except ValueError:
            flash("Invalid pages format", "error")
            return render_template("days.html", books=books, total_pages=total_pages)

        # 一日に読むページ数が0以下の場合
        if pages_per_day <= 0:
            flash("Please enter a number greater than or equal to 1.", "error")
            return render_template("days.html", books=books, total_pages=total_pages)

        if pages_per_day is None:
            flash("Invalid pages format", "error")
            return render_template("days.html", books=books, total_pages=total_pages)

        if total_pages is None:
            flash("No books in database", "error")
            return render_template("days.html", books=books, total_pages=total_pages)

        if not data:
            c.execute("INSERT INTO input_pages (pages) VALUES (?)", (pages_per_day,))
        else:
            c.execute("UPDATE input_pages SET pages = ?", (pages_per_day,))
        conn.commit()
        conn.close()

        start_date = datetime.now()
        days = math.ceil(total_pages / pages_per_day) if pages_per_day else None  # pages_per_day が None の場合は days も None
        finish_date = start_date + timedelta(days=days) if days else None  # days が None の場合は finish_date も None

        return render_template("days.html", books=books, total_pages=total_pages, pages_per_day=pages_per_day, days=days, finish_date=finish_date)

    else:
    #GETリクエストの場合,dataの値を使用してpages_per_dayを設定する
        if data:
            pages_per_day = data[0]
        else:
            pages_per_day = None

        #booksがない場合は,ページ数を表示しない
        if not books:
            return render_template("days.html")

        start_date = datetime.now()
        days = math.ceil(total_pages / pages_per_day) if pages_per_day else None  # pages_per_day が None の場合は days も None
        finish_date = start_date + timedelta(days=days) if days else None  # days が None の場合は finish_date も None

        return render_template("days.html", books=books, total_pages=total_pages, pages_per_day=pages_per_day, days=days, finish_date=finish_date)


#データベースの要素を削除する関数
@app.route("/delete", methods=["POST"])
def delete():
    isbn = request.form.get("isbn")
    conn = create_conn()
    c = conn.cursor()
    c.execute("DELETE from books where ISBN = ?", (isbn,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)
    
if __name__ == '__main__':
    app.run(debug=True)
