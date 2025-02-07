from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        ai_response = f"AI thinks: {random.choice(['Great idea!', 'Try again!', 'Interesting!'])}"
        return render_template("index.html", user_input=user_input, ai_response=ai_response)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
