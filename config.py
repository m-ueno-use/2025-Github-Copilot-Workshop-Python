import os
import secrets

class Config:
    """開発・学習用の最小設定。

    Step1 ではDBは未使用。今後の拡張に備え、共通キーのみ定義。
    """

    # WARNING: In production, you MUST set the SECRET_KEY environment variable to a strong, unpredictable value.
    # For development, a random key is generated if not set.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(32)
    # タイマーの既定値（秒）
    WORK_DURATION = int(os.environ.get("WORK_DURATION", 25 * 60))
