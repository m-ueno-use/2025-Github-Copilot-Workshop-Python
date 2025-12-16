import os


class Config:
    """開発・学習用の最小設定。

    Step1 ではDBは未使用。今後の拡張に備え、共通キーのみ定義。
    """

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    # タイマーの既定値（秒）
    WORK_DURATION = int(os.environ.get("WORK_DURATION", 25 * 60))
