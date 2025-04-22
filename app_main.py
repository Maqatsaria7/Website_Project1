from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("main_page.html")

if "__main__" == __name__:
    app.run(debug=True)