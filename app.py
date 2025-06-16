from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    pokemon_data = None
    if request.method == "POST":
        name = request.form.get("name").lower()
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        if response.status_code == 200:
            pokemon_data = response.json()
    return render_template("index.html", pokemon=pokemon_data)


if __name__ == "__main__":
    app.run(debug=True)
