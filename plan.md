# ポモドーロタイマー 実装計画（6ステップ）

## 1) 骨組みセットアップ
- Flaskエントリ(app.py/config.py/extensions.py)、テンプレ雛形、static/js/timer.jsの純JSカウントダウンと基本CSS
- 25分タイマーがローカルで動き、開始/リセットが効くところまで

## 2) APIスケルトン & DI
- アプリファクトリとDIでPomodoroServiceとSessionRepositoryを束ねる
- `/` と `/api/sessions`(POST/GET)をダミー実装で返却し、フロントapi-client.jsはモック取得可能に

## 3) モデル・永続化（最小）
- Sessionモデル + SQLite dev設定
- SessionRepositoryをDB実装（save/find_all/delete）、create_allでテーブル生成
- ダミーAPIを実データ返却に置き換え

## 4) サービス本実装 & バリデーション
- PomodoroServiceに作業/休憩サイクル、duration範囲、task_name必須、session_type制約を実装
- 完了/削除を含めAPIを実データ連携に更新

## 5) UI連携 & 進捗表示
- タイマー完了時にPOST /api/sessionsで記録
- GET /api/statisticsで日次の回数・合計時間のみ最小実装しカード表示へ反映
- 円グラフ(SVG/CSS)を残り時間で更新

## 6) 仕上げ: 設定・通知・履歴・テスト
- GET/POST /api/settingsで作業/休憩時間を保存し設定パネルと連動
- 通知/サウンド追加、履歴一覧と削除をUIに追加
- ユニット（Timer/Service/Repo）とAPI統合テストを整備（カバレッジ目標70%）
