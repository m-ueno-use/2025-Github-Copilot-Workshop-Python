from flask import Flask, render_template
from config import Config


def create_app() -> Flask:
    """最小のFlaskアプリケーションを生成して返します。

    Step1 要件:
    - ルート `/` でテンプレートを返す
    - `templates/` と `static/` を既定の場所で使用
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    # 開発用の簡易実行（ホットリロードはFlask標準のdebugで）
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
