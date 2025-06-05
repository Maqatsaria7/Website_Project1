from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(seconds=10)

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
        return redirect(url_for('main_page'))
    return render_template("make_a_post.html")

@app.route("/workouts", methods=["GET"])
def workouts():
    workout_posts = []
    with sqlite3.connect('fitnessproject.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT * FROM posts WHERE category = ? ORDER BY id DESC
        ''', ("TRAINING",))
        w_posts = c.fetchall()
        for row in w_posts:
            workout_posts.append({'id': row[0], 'title': row[1], 'author': row[2], 'description': row[3], 'information': row[4]})
            print(workout_posts)
    return render_template("workouts.html", workout_posts=workout_posts)


@app.route("/nutrition", methods=["GET"])
def nutrition():
    nutrition_posts = []
    with sqlite3.connect('fitnessproject.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT * FROM posts WHERE category = ? ORDER BY id DESC
        ''', ("NUTRITION",))
        n_posts = c.fetchall()
        for row in n_posts:
            nutrition_posts.append({'id': row[0], 'title': row[1], 'author': row[2], 'description': row[3], 'information': row[4]})
    return render_template("nutrition.html", nutrition_posts=nutrition_posts)


@app.route("/supplement", methods=["GET"])
def supplement():
    supplement_posts = []
    with sqlite3.connect('fitnessproject.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT * FROM posts WHERE category = ? ORDER BY id DESC
        ''', ("SUPPLEMENTS",))
        s_posts = c.fetchall()
        for row in s_posts:
            supplement_posts.append({'id': row[0], 'title': row[1], 'author': row[2], 'description': row[3], 'information': row[4]})
    return render_template("supplement.html", supplement_posts=supplement_posts)



@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        conn = sqlite3.connect('fitnessproject.db')
        c = conn.cursor()
        c.execute("SELECT email, password FROM admins WHERE email = ?", (user_email,))
        rows = c.fetchall()
        print(rows)
        if rows:
            database_password = rows[0][1]
            if database_password == user_password:
                session.permanent = True
                session['user'] = user_email
                return redirect(url_for('admin'))
        conn.close()

    return render_template('sign_in.html')
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('sign_in'))

@app.route('/admin')
def admin():
    if 'user' in session:
        return render_template("admin.html", user=session['user'])
    else:
        return redirect(url_for('sign_in'))

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    print("ROUTE HIT")
    import sqlite3
    conn = sqlite3.connect('fitnessproject.db')
    c = conn.cursor()

    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = c.fetchone()
    conn.close()

    if row:
        viewpost = {
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'description': row[3],
            'information': row[4],
            'category': row[5]
        }
    else:
        viewpost = None

    return render_template("view_post.html", viewpost=viewpost)




@app.route('/admin/admin_posts', methods=['GET', 'POST'])
def admin_posts():
    conn = sqlite3.connect('fitnessproject.db')
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        information = request.form.get('information')
        author = request.form.get('author')
        category = request.form.get("category")

        conn.execute('''
                     INSERT INTO posts (title, description, information, author, category)
                     VALUES (?, ?, ?, ?, ?)
                     ''', (title, description, information, author, category))
        conn.commit()

    posts = []
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        posts.append({'id': row[0], 'title': row[1], 'author': row[2], 'description': row[3], 'information': row[4], 'category': row[5]})

    return render_template('admin_posts.html', posts=posts)


@app.route('/admin/admin_contacts')
def admin_contacts():
    conn = sqlite3.connect('fitnessproject.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    rows = c.fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({'id': row[0], 'name': row[1], 'email': row[2], 'question': row[3]})

    print(questions)
    return render_template('admin_contacts.html', questions=questions)


@app.route('/admin/admin_update/<int:id>', methods=["GET", "POST"])
def admin_update(id):
    posts = []
    conn = sqlite3.connect("fitnessproject.db")
    if request.method == "GET":
        c = conn.cursor()
        c.execute(''' SELECT * FROM posts WHERE id = ? ''', (id, ))
        rows = c.fetchall()
        conn.close()
        for row in rows:
            posts.append({'id': row[0], 'title': row[1], 'author': row[2], 'description': row[3], 'information': row[4], 'category': row[5]})
        return render_template("admin_update.html", post = posts[0])
    else:
        title = request.form.get("update_title")
        author = request.form.get("update_author")
        description = request.form.get("update_description")
        information = request.form.get("update_information")
        category = request.form.get("update_category")

        conn.execute('''
            UPDATE posts SET title = ?, description = ?, information = ?, author = ?, category = ? WHERE id = ?
        ''', (title, description, information, author, category, id))
        conn.commit()
        conn.close()

        return redirect(url_for("admin_posts"))

@app.route('/admin/admin_delete/<int:id>')
def admin_delete(id):
    conn = sqlite3.connect('fitnessproject.db')
    conn.execute('''
        DELETE FROM posts WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_posts'))

if __name__ == "__main__":
    app.run(debug=True)