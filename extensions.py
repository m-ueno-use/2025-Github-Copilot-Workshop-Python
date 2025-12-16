"""将来の拡張用プレースホルダー。

Step1 ではDB等の拡張は未導入だが、
後続ステップで初期化コードを集約できるようモジュールを用意。
"""

try:
    # 後続フェーズ向け（未インストールでも動くようガード）
    from flask_sqlalchemy import SQLAlchemy  # type: ignore

    db = SQLAlchemy()
except Exception:  # pragma: no cover - 依存未導入の環境でも動作させるため
    db = None  # ダミー（Step1では未使用）
