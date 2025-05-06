from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("main_page.html")

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        question = request.form.get("question")
        with sqlite3.connect('fitnessproject.db') as conn:
            conn.execute('''
                INSERT INTO contacts (name, email, question) VALUES (?, ?, ?)
            ''', (name, email, question))
    return render_template("contact_us.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/make_a_post", methods=["GET", "POST"])
def make_a_post():
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        description = request.form.get("description")
        information = request.form.get("information")
        category = request.form.get("category")
        with sqlite3.connect('fitnessproject.db') as conn:
            conn.execute('''
                INSERT INTO posts (title, author, description, information, category) 
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, description, information, category))
    return render_template("make_a_post.html")

@app.route("/workouts", methods=["GET"])
def workouts():
    with sqlite3.connect('fitnessproject.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT * FROM posts WHERE category = ?
        ''', ("TRAINING",))
        posts = c.fetchall()
    return render_template("workouts.html", posts=posts)


@app.route("/nutrition", methods=["GET"])
def nutrition():
    with sqlite3.connect('fitnessproject.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT * FROM posts WHERE category = ?
        ''', ("NUTRITION",))
        posts = c.fetchall()
    return render_template("nutrition.html", posts=posts)


@app.route("/supplement", methods=["GET"])
def supplement():
    with sqlite3.connect('fitnessproject.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT * FROM posts WHERE category = ?
        ''', ("SUPPLEMENTS",))
        posts = c.fetchall()
    return render_template("supplement.html", posts=posts)



if __name__ == "__main__":  # <-- correct comparison operator
    app.run(debug=True)
