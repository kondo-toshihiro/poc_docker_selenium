# Docker Selenium 
このリポジトリは、Docker ComposeでSelenium Gridを構築し、Pythonスクリプトでブラウザ自動化します。

## 構成

- **Selenium Hub**: Selenium Gridのハブサーバー
- **Selenium Edge Node**: Microsoft Edgeブラウザを実行するノード
- **VNC Server**: ブラウザの動作を視覚的に確認するためのVNCサーバー
- **Python App**: Seleniumスクリプトを実行するPythonアプリケーション

## 必要な環境

- Docker
- Docker Compose

## 準備
1. .envファイル作成してスクリプトと同じフォルダに保存しておく。
```bash
# WSL2 Ubuntu認証情報
WSL2_USER=toshisot
WSL2_PASSWORD=password

# Selenium Grid設定
SELENIUM_HUB_URL=http://localhost:4444/wd/hub
SELENIUM_VNC_URL=http://localhost:7900/?autoconnect=1&resize=scale&password=secret
SELENIUM_IMAGE=selenium/standalone-chrome:4.33.0-20250606

# Docker設定
DOCKER_SHAREDMEM_SIZE=2g
DOCKER_PORTS_HUB=4444:4444
DOCKER_PORTS_VNC=7900:7900
```

## 使用方法

### 1. docker起動

```bash
docker-compose up -d
```

このコマンドで以下のサービスが起動します：
- Selenium Hub (ポート: 4444)
- Selenium Edge Node
- VNC Server (ポート: 7900)
- Python App Container

### 2. Selenium Gridの確認

ブラウザで以下のURLにアクセスして、Selenium Gridの状態を確認できます：
- http://localhost:4444/ui/index.html

### 3. VNCでブラウザ動作を確認

ブラウザで以下のURLにアクセスして、実際のブラウザ動作を視覚的に確認できます：
- http://localhost:7900
- パスワード: `secret`

### 4. スクリプト実行

#### 基本テスト（Google Japan アクセステスト）

```bash
# Pythonアプリコンテナ内でテスト
docker-compose exec selenium-app python selenium_test.py
```

#### RPA実行

```bash
# メインのRPA処理を実行
docker-compose exec selenium-app python src/main_docker.py
```

### 5. 個別サービスの操作

#### 特定のサービスのみ起動

```bash
# Seleniumのみ起動
docker-compose up -d selenium-hub selenium-edge selenium-edge-vnc

# Pythonのみ起動
docker-compose up -d selenium-app
```

#### ログの確認

```bash
# 全サービスのログを確認
docker-compose logs

# 特定のサービスのログを確認
docker-compose logs selenium-hub
docker-compose logs selenium-edge
docker-compose logs selenium-app
```

#### サービスの停止

```bash
# 停止
docker-compose down

# コンテナとボリューム削除
docker-compose down -v
```

### 6. ファイルのダウンロード

ダウンロードファイルは `./downloads` に保存。

## ディレクトリ構造

```
.
├── docker-compose.yml      # Docker Compose設定
├── Dockerfile             # Pythonアプリ用Dockerfile
├── requirements.txt       # Python依存関係
├── README.md             # このファイル
├── downloads/            # ダウンロードファイル保存先
├── selenium_test.py      # 基本テストスクリプト
└── src/
    ├── main_docker.py    # メインRPAスクリプト
    └── ...               # その他のソースファイル
```

## トラブルシューティング

### ポートが使用中の場合

他のアプリケーションがポート4444や7900を使用している場合は、`docker-compose.yml`のポート設定を変更。

### コンテナが起動しない場合

```bash
# コンテナの状態を確認
docker-compose ps

# エラーログを確認
docker-compose logs [service-name]
```

### ブラウザが起動しない場合

1. Selenium Hubが正常に起動しているか確認
2. Edge Nodeが正常に登録されているか確認（http://localhost:4444/ui/index.html）
3. VNCで実際のブラウザ画面を確認（http://localhost:7900）

## 開発時の注意事項

- スクリプトを修正した場合、Pythonアプリコンテナを再起動
- 新しいPythonパッケージを追加した場合は、`requirements.txt`を更新してコンテナを再ビル

```bash
# コンテナの再ビルド
docker-compose build selenium-app
docker-compose up -d selenium-app
