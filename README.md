# FastAPI Template

FastAPI + Docker 環境のテンプレートリポジトリです。REST API の開発をすぐに始められるよう、基本的な環境構築が完了しています。

## 機能

- FastAPI + Uvicorn
- Docker/Docker Compose 対応
- CORS ミドルウェア設定済
- データ永続化のボリューム設定
- 環境変数対応

## 必要要件

- Docker
- Docker Compose

## 使い方

1. リポジトリをクローン

```bash
git clone <repository-url>
cd <repository-name>
```

2. 環境変数の設定
   `.env`ファイルを作成し、必要な環境変数を設定:

```
OPENAI_API_KEY=your-api-key
```

3. アプリケーションの起動

```bash
docker-compose up --build
```

4. API の動作確認  
   ブラウザで http://localhost:8000/docs にアクセスし、Swagger UI を確認

## 開発の進め方

1. `api/app/main.py`にエンドポイントを追加
2. 必要なパッケージは`api/requirements.txt`に追記
3. `data/`ディレクトリにデータファイルを配置
4. `vectorstore/`は永続化されたベクター DB として利用可能

## ディレクトリ構成

- `api/`: API サーバーのソースコード
- `data/`: データファイル用ディレクトリ
- `vectorstore/`: ベクターストアのデータ永続化用
