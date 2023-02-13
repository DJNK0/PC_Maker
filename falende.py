
from flask import Flask, render_template, request
import programmayes
import sys
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/", methods=["POST"])
def get_data():
    if request.form.get("gaming_btn") == "0":
        return render_template('home.html', name="gaming")
    elif request.form.get('productiviteit_btn') == '0':
        return render_template('home.html', name="productiviteit")
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
    print(request.form.get("budget"))
    budget = get_data()

