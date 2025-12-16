# ポモドーロタイマー Webアプリケーション アーキテクチャ設計書

## 📋 概要

本ドキュメントは、FlaskとHTML/CSS/JavaScriptを使用したポモドーロタイマーWebアプリケーションのアーキテクチャ設計をまとめたものです。テスタビリティを重視し、保守性と拡張性の高い設計を採用しています。

**作成日**: 2025年12月16日  
**技術スタック**: Flask, HTML5, CSS3, Vanilla JavaScript  
**アーキテクチャパターン**: レイヤードアーキテクチャ、リポジトリパターン、依存性注入

---

## 🏗️ プロジェクト構造

```
2025-Github-Copilot-Workshop-Python/
├── app.py                          # アプリケーションエントリーポイント
├── config.py                       # 環境別設定（dev/test/prod）
├── requirements.txt                # 本番依存関係
├── requirements-dev.txt            # 開発・テスト依存関係
├── pytest.ini                      # pytest設定
├── .coveragerc                     # カバレッジ設定
├── architecture.md                 # 本ドキュメント
│
├── pomodoro/                       # メインアプリケーションパッケージ
│   ├── __init__.py                # アプリケーションファクトリー
│   │
│   ├── api/                       # APIレイヤー（Controller）
│   │   ├── __init__.py
│   │   ├── routes.py              # ルーティング定義
│   │   └── schemas.py             # リクエスト/レスポンススキーマ
│   │
│   ├── services/                  # ビジネスロジック層
│   │   ├── __init__.py
│   │   ├── pomodoro_service.py   # タイマーロジック
│   │   └── statistics_service.py # 統計計算ロジック
│   │
│   ├── repositories/              # データアクセス層
│   │   ├── __init__.py
│   │   ├── base.py               # 抽象基底クラス
│   │   └── session_repository.py # セッションCRUD
│   │
│   ├── models/                    # ドメインモデル
│   │   ├── __init__.py
│   │   └── session.py            # セッションモデル
│   │
│   └── utils/                     # ユーティリティ
│       ├── __init__.py
│       ├── validators.py         # バリデーション関数
│       └── time_utils.py         # 時間計算関数
│
├── static/                        # 静的ファイル
│   ├── css/
│   │   └── style.css            # メインスタイルシート
│   ├── js/
│   │   ├── pomodoro.js          # メインアプリケーション
│   │   ├── timer.js             # タイマークラス（独立）
│   │   ├── api-client.js        # API通信層（独立）
│   │   ├── notification.js      # 通知機能（独立）
│   │   └── utils.js             # ユーティリティ関数
│   └── images/
│       └── favicon.ico
│
├── templates/                     # Jinjaテンプレート
│   └── index.html               # メインページ
│
└── tests/                         # テストディレクトリ
    ├── __init__.py
    ├── conftest.py               # pytest共通フィクスチャ
    │
    ├── unit/                     # ユニットテスト
    │   ├── __init__.py
    │   ├── test_services.py
    │   ├── test_repositories.py
    │   ├── test_models.py
    │   └── test_utils.py
    │
    ├── integration/              # 統合テスト
    │   ├── __init__.py
    │   └── test_api.py
    │
    ├── e2e/                      # E2Eテスト（オプション）
    │   └── test_scenarios.py
    │
    └── fixtures/                 # テストデータ
        ├── __init__.py
        ├── builders.py           # テストデータビルダー
        ├── in_memory_repository.py
        └── sample_data.py
```

---

## 🎨 アーキテクチャ概要

### アーキテクチャパターン

本アプリケーションは**レイヤードアーキテクチャ**を採用し、以下の層で構成されます：

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│     (HTML/CSS/JavaScript Frontend)      │
└─────────────────┬───────────────────────┘
                  │ HTTP/JSON
┌─────────────────▼───────────────────────┐
│          API Layer (Controller)         │
│           (Flask Routes)                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Service Layer (Business)         │
│      (PomodoroService, Statistics)      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Repository Layer (Data)           │
│        (SessionRepository)              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Database (SQLite/PostgreSQL)     │
└─────────────────────────────────────────┘
```

### 設計原則

1. **関心の分離 (Separation of Concerns)**: 各層が明確な責務を持つ
2. **依存性注入 (Dependency Injection)**: テスタビリティとモジュール性の向上
3. **インターフェース分離**: 抽象に依存し、具象に依存しない
4. **単一責任の原則**: 各クラス・関数は一つの責務のみを持つ
5. **テスト駆動開発対応**: 高いテストカバレッジを実現可能な設計

---

## 🔧 各レイヤーの詳細

### 1. Presentation Layer (フロントエンド)

**責務:**
- ユーザーインターフェースの提供
- タイマーの表示とカウントダウン
- ユーザー操作のハンドリング
- バックエンドAPIとの通信

**主要コンポーネント:**

#### `static/js/timer.js` - タイマークラス
```javascript
export class Timer {
    constructor(duration, onTick, onComplete) {
        this.duration = duration;
        this.remaining = duration;
        this.onTick = onTick;        // コールバック注入
        this.onComplete = onComplete;
    }
    
    start() { /* タイマー開始 */ }
    stop() { /* タイマー停止 */ }
    reset() { /* タイマーリセット */ }
}
```

**設計のポイント:**
- DOM操作とロジックを分離
- コールバック注入でテスト容易性を確保
- 純粋関数としてのユーティリティ実装

#### `static/js/api-client.js` - API通信層
```javascript
export class PomodoroApiClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }
    
    async createSession(sessionData) { /* ... */ }
    async getSessions() { /* ... */ }
    async getStatistics() { /* ... */ }
}
```

**設計のポイント:**
- Fetch APIをラップして再利用性を向上
- エラーハンドリングの集約
- テスト時にモック可能な設計

---

### 2. API Layer (Controller)

**責務:**
- HTTPリクエストの受け取りとレスポンス返却
- リクエストバリデーション
- サービス層への委譲

**実装例:**

```python
# pomodoro/api/routes.py
from flask import Blueprint, request, jsonify
from pomodoro.services.pomodoro_service import PomodoroService

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/sessions', methods=['POST'])
def create_session():
    """セッション作成エンドポイント"""
    data = request.get_json()
    
    # バリデーション
    if not data or 'task_name' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    # サービス層に委譲
    service = current_app.pomodoro_service
    result = service.create_session(data)
    
    return jsonify(result.to_dict()), 201

@bp.route('/sessions', methods=['GET'])
def get_sessions():
    """セッション一覧取得"""
    service = current_app.pomodoro_service
    sessions = service.get_all_sessions()
    return jsonify([s.to_dict() for s in sessions]), 200
```

**APIエンドポイント設計:**

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | メインページの提供 |
| GET | `/api/settings` | 設定の取得 |
| POST | `/api/settings` | 設定の更新 |
| POST | `/api/sessions` | セッション記録の保存 |
| GET | `/api/sessions` | セッション履歴の取得 |
| GET | `/api/sessions/<id>` | 特定セッションの取得 |
| DELETE | `/api/sessions/<id>` | セッションの削除 |
| GET | `/api/statistics` | 統計情報の取得 |

---

### 3. Service Layer (ビジネスロジック)

**責務:**
- ビジネスルールの実装
- 複雑なロジックの処理
- トランザクション管理
- データの変換と集計

**実装例:**

```python
# pomodoro/services/pomodoro_service.py
from pomodoro.models.session import Session
from pomodoro.repositories.session_repository import SessionRepository
from pomodoro.utils.validators import validate_session_duration, validate_task_name

class PomodoroService:
    """ポモドーロタイマーのビジネスロジック"""
    
    def __init__(self, session_repository: SessionRepository):
        """依存性注入によるリポジトリの受け取り"""
        self.session_repository = session_repository
    
    def create_session(self, data: dict) -> Session:
        """セッションの作成
        
        Args:
            data: セッションデータ
            
        Returns:
            作成されたSession
            
        Raises:
            ValueError: バリデーションエラー
        """
        # バリデーション
        validate_task_name(data['task_name'])
        validate_session_duration(data['duration'])
        
        # モデルの作成
        session = Session(
            task_name=data['task_name'],
            session_type=data.get('session_type', 'work'),
            duration=data['duration'],
            completed=data.get('completed', True)
        )
        
        # 永続化
        return self.session_repository.save(session)
    
    def get_all_sessions(self) -> list[Session]:
        """全セッションの取得"""
        return self.session_repository.find_all()
    
    def complete_session(self, session_id: int) -> Session:
        """セッションの完了"""
        session = self.session_repository.find_by_id(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.completed = True
        session.completed_at = datetime.now()
        return self.session_repository.save(session)
```

**設計のポイント:**
- リポジトリを依存性注入で受け取る
- 純粋なビジネスロジックのみを実装
- データベースの詳細を知らない

---

### 4. Repository Layer (データアクセス)

**責務:**
- データベース操作の抽象化
- CRUD操作の実装
- クエリの構築

**実装例:**

```python
# pomodoro/repositories/base.py
from abc import ABC, abstractmethod
from typing import List, Optional

class BaseRepository(ABC):
    """リポジトリ基底クラス"""
    
    @abstractmethod
    def save(self, entity):
        """エンティティの保存"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[any]:
        """IDによる検索"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[any]:
        """全件取得"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """削除"""
        pass

# pomodoro/repositories/session_repository.py
from pomodoro.repositories.base import BaseRepository
from pomodoro.models.session import Session

class SessionRepository(BaseRepository):
    """セッションリポジトリ"""
    
    def __init__(self, db):
        self.db = db
    
    def save(self, session: Session) -> Session:
        """セッションの保存"""
        self.db.session.add(session)
        self.db.session.commit()
        return session
    
    def find_by_id(self, id: int) -> Optional[Session]:
        """IDでセッションを検索"""
        return Session.query.get(id)
    
    def find_all(self) -> List[Session]:
        """全セッションを取得"""
        return Session.query.order_by(Session.timestamp.desc()).all()
    
    def find_by_date_range(self, start_date, end_date) -> List[Session]:
        """日付範囲でセッションを検索"""
        return Session.query.filter(
            Session.timestamp >= start_date,
            Session.timestamp <= end_date
        ).all()
    
    def delete(self, id: int) -> bool:
        """セッションの削除"""
        session = self.find_by_id(id)
        if session:
            self.db.session.delete(session)
            self.db.session.commit()
            return True
        return False
```

**設計のポイント:**
- 抽象基底クラスでインターフェースを定義
- テスト時にインメモリ実装に切り替え可能
- データベースの実装詳細をカプセル化

---

### 5. Model Layer (ドメインモデル)

**責務:**
- ビジネスエンティティの表現
- データの整合性保証
- ドメインロジックのカプセル化

**実装例:**

```python
# pomodoro/models/session.py
from datetime import datetime
from pomodoro.extensions import db

class Session(db.Model):
    """ポモドーロセッションモデル"""
    
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    session_type = db.Column(db.String(20), nullable=False)  # work/short_break/long_break
    duration = db.Column(db.Integer, nullable=False)  # 秒
    completed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, task_name: str, session_type: str, duration: int, completed: bool = False):
        self.task_name = task_name
        self.session_type = session_type
        self.duration = duration
        self.completed = completed
    
    def to_dict(self) -> dict:
        """辞書型に変換"""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'session_type': self.session_type,
            'duration': self.duration,
            'completed': self.completed,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<Session {self.id}: {self.task_name} ({self.session_type})>'
```

---

## 🧪 テスト戦略

### テストピラミッド

```
        /\
       /E2E\          少数（遅い、包括的）
      /------\        - シナリオテスト
     /  統合  \        中程度（中速、API全体）
    /----------\      - APIエンドポイントテスト
   / ユニット  \      多数（高速、詳細）
  /--------------\    - サービス、リポジトリ、ユーティリティ
```

### テストの種類と目標

| テストタイプ | 対象 | カバレッジ目標 | 実行速度 |
|------------|------|--------------|---------|
| ユニットテスト | Services, Utils, Models | 80%以上 | 高速（< 1秒） |
| 統合テスト | API Endpoints | 全エンドポイント | 中速（< 10秒） |
| E2Eテスト | ユーザーシナリオ | クリティカルパス | 低速（> 30秒） |

### テストフィクスチャ設計

```python
# tests/conftest.py
import pytest
from pomodoro import create_app
from pomodoro.extensions import db as _db

@pytest.fixture
def app():
    """テスト用Flaskアプリケーション"""
    app = create_app('testing')
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    """テストクライアント"""
    return app.test_client()

@pytest.fixture
def in_memory_repo():
    """テスト用インメモリリポジトリ"""
    from tests.fixtures.in_memory_repository import InMemorySessionRepository
    return InMemorySessionRepository()
```

### ユニットテスト例

```python
# tests/unit/test_services.py
import pytest
from unittest.mock import Mock
from pomodoro.services.pomodoro_service import PomodoroService
from pomodoro.models.session import Session

class TestPomodoroService:
    def test_create_session_success(self):
        # Arrange
        mock_repo = Mock()
        service = PomodoroService(mock_repo)
        data = {
            'task_name': 'テストタスク',
            'session_type': 'work',
            'duration': 1500,
            'completed': True
        }
        
        # Act
        result = service.create_session(data)
        
        # Assert
        mock_repo.save.assert_called_once()
        assert result.task_name == 'テストタスク'
    
    def test_create_session_invalid_duration(self):
        # Arrange
        mock_repo = Mock()
        service = PomodoroService(mock_repo)
        data = {'task_name': 'テスト', 'duration': 30}  # 短すぎる
        
        # Act & Assert
        with pytest.raises(ValueError, match="between 60 and 7200"):
            service.create_session(data)
```

---

## 🔄 データフロー

### セッション作成のフロー

```
[ユーザー: 開始ボタンクリック]
         ↓
[JavaScript: Timer.start()]
         ↓
[JavaScript: タイマー完了後]
         ↓
[JavaScript: ApiClient.createSession()]
         ↓ POST /api/sessions
[Flask: routes.create_session()]
         ↓
[Service: PomodoroService.create_session()]
         ↓ バリデーション
[Repository: SessionRepository.save()]
         ↓
[Database: INSERT]
         ↓
[Response: JSON]
         ↓
[JavaScript: UI更新]
```

---

## ⚙️ 設定管理

### 環境別設定

```python
# config.py
import os

class Config:
    """基底設定クラス"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ポモドーロタイマー設定
    WORK_DURATION = 1500        # 25分
    SHORT_BREAK_DURATION = 300  # 5分
    LONG_BREAK_DURATION = 900   # 15分
    SESSIONS_UNTIL_LONG_BREAK = 4

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pomodoro_dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    # テスト用の短い時間
    WORK_DURATION = 10
    SHORT_BREAK_DURATION = 5

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

---

## 🚀 アプリケーションファクトリーパターン

```python
# pomodoro/__init__.py
from flask import Flask
from pomodoro.extensions import db
from config import config

def create_app(config_name='default'):
    """アプリケーションファクトリー"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 拡張機能の初期化
    db.init_app(app)
    
    # 依存性の構築（DIコンテナパターン）
    with app.app_context():
        from pomodoro.repositories.session_repository import SessionRepository
        from pomodoro.services.pomodoro_service import PomodoroService
        
        session_repo = SessionRepository(db)
        pomodoro_service = PomodoroService(session_repo)
        
        # アプリケーションコンテキストに登録
        app.pomodoro_service = pomodoro_service
    
    # ブループリント登録
    from pomodoro.api import routes
    app.register_blueprint(routes.bp)
    
    # メインページのルート
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
```

---

## 📦 依存関係

### requirements.txt
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
```

### requirements-dev.txt
```
pytest==7.4.3
pytest-cov==4.1.0
pytest-flask==1.3.0
pytest-mock==3.12.0
factory-boy==3.3.0
faker==20.1.0
black==23.12.1
flake8==7.0.0
mypy==1.8.0
```

---

## 📈 実装フェーズ

### Phase 1: MVP (最小機能製品)
- [ ] プロジェクト構造のセットアップ
- [ ] 基本的なタイマー機能（25/5分）
- [ ] シンプルなUI
- [ ] 開始/停止/リセット機能

### Phase 2: コア機能
- [ ] タスク名の入力
- [ ] セッションの保存（バックエンド）
- [ ] 音声通知
- [ ] カスタム時間設定
- [ ] ユニットテストの実装

### Phase 3: 拡張機能
- [ ] セッション履歴表示
- [ ] 統計情報（日次/週次/月次）
- [ ] プログレスバー
- [ ] ダークモード
- [ ] 統合テストの実装

### Phase 4: 最適化
- [ ] パフォーマンス最適化
- [ ] E2Eテストの実装
- [ ] ドキュメント整備
- [ ] デプロイ準備

---

## 🔒 セキュリティ考慮事項

1. **CSRF保護**: Flask-WTFによるトークン検証
2. **入力バリデーション**: 全APIエンドポイントで実施
3. **SQLインジェクション対策**: ORMの使用
4. **XSS対策**: Jinjaテンプレートの自動エスケープ
5. **環境変数管理**: 機密情報を環境変数化

---

## 🎯 非機能要件

### パフォーマンス
- APIレスポンス: < 200ms (95%ile)
- ページロード: < 2秒
- タイマー精度: ±1秒以内

### スケーラビリティ
- 同時ユーザー: 1000人以上
- セッションデータ: 100万件まで対応

### 可用性
- アップタイム: 99.5%以上
- バックアップ: 日次自動バックアップ

---

## 📚 参考資料

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Dependency Injection](https://martinfowler.com/articles/injection.html)

---

## 🤝 貢献ガイドライン

1. ブランチ戦略: Git Flow
2. コミットメッセージ: Conventional Commits
3. コードレビュー: 必須
4. テストカバレッジ: 80%以上維持
5. ドキュメント: コード変更時に同時更新

---

**最終更新**: 2025年12月16日  
**バージョン**: 1.0.0  
**メンテナー**: Development Team
