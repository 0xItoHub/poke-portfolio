from flask import Flask, render_template, request, jsonify
import requests
from pokemon_names import get_english_name, get_suggestions

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    pokemon_data = None
    error_message = None
    search_term = None

    if request.method == "POST":
        name = request.form.get("name")
        search_term = name
        if name:
            name = name.strip()
            # 日本語名を英語名に変換
            english_name = get_english_name(name)
            search_name = english_name.lower()

            try:
                response = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{search_name}"
                )

                if response.status_code == 200:
                    pokemon_data = response.json()
                else:
                    error_message = f"ポケモン「{name}」は見つかりませんでした。"
            except requests.RequestException:
                error_message = "APIへの接続中にエラーが発生しました。しばらくしてから再度お試しください。"
        else:
            error_message = "ポケモンの名前を入力してください。"

    return render_template(
        "index.html", pokemon=pokemon_data, error=error_message, search_term=search_term
    )


@app.route("/api/suggestions")
def api_suggestions():
    query = request.args.get("q", "")
    suggestions = get_suggestions(query)
    return jsonify(suggestions)


if __name__ == "__main__":
    app.run(debug=True)
