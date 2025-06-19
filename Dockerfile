FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とインストール
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# ユーザーディレクトリを作成
RUN mkdir -p /home/user/downloads && \
    chmod 755 /home/user/downloads

# デフォルトコマンド
CMD ["python", "-u", "selenium_test.py"]
