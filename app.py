from flask import Flask, render_template, request
import requests
from pokemon_names import get_english_name

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    pokemon_data = None
    error_message = None
    debug_info = None

    if request.method == "POST":
        name = request.form.get("name")
        if name:
            name = name.strip()
            # 日本語名を英語名に変換
            english_name = get_english_name(name)
            search_name = english_name.lower()

            try:
                print(f"検索中のポケモン: {name} -> {search_name}")  # デバッグ用
                response = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{search_name}"
                )
                print(f"APIレスポンスステータス: {response.status_code}")  # デバッグ用

                if response.status_code == 200:
                    pokemon_data = response.json()
                    print(
                        f"取得したポケモンデータ: {pokemon_data.get('name', 'N/A')}"
                    )  # デバッグ用
                else:
                    error_message = f"ポケモン '{name}' が見つかりませんでした。ステータスコード: {response.status_code}"
                    print(f"APIエラー: {response.text}")  # デバッグ用
            except requests.RequestException as e:
                error_message = f"APIリクエストエラー: {str(e)}"
                print(f"リクエスト例外: {e}")  # デバッグ用
        else:
            error_message = "ポケモンの名前を入力してください。"

    return render_template(
        "index.html", pokemon=pokemon_data, error=error_message, debug=debug_info
    )


if __name__ == "__main__":
    app.run(debug=True)
