from flask import Flask, request, render_template, Request
from main import get_info

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        data = request.json

        # getting input with name = fname in HTML form
        # first_name = request.form.get("departure")
        first_name = data['departure']
        # getting input with name = lname in HTML form
        # last_name = request.form.get("arrival")
        last_name = data['arrival']

        return get_info(first_name, last_name)

    return render_template("web.html")

if __name__ == "__main__":
    app.run()
