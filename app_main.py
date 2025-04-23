from flask import Flask, render_template, request

app = Flask(__name__)
items = []
@app.route("/")
def main_page():
    return render_template("main_page.html")

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        question = request.form.get("question")
        items.append({"name": name, "email": email, "question": question})
        print(items)
    return render_template("contact_us.html")
if "__main__" == __name__:
    app.run(debug=True)