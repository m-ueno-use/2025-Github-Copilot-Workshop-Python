ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0

## ポモドーロタイマー（Step1）

Flask の最小構成を追加し、シンプルな25分タイマー（開始/リセット）を提供します。

### 起動方法

1) 依存関係をインストール

```bash
python -m pip install --upgrade pip
pip install Flask
```

2) アプリを起動

```bash
python app.py
```

3) ブラウザで http://localhost:5000 を開く

テンプレート: templates/index.html
スタイル: static/css/style.css
タイマー: static/js/timer.js

### テストの実行

開発用依存を導入してpytestを実行します。

```bash
pip install -r requirements.txt
pip install pytest
pytest
```


