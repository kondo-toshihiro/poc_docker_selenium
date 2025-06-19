@echo off
echo Docker Selenium環境を起動しています...
echo.

echo 1. Docker Composeでサービスを起動中...
docker-compose up -d

echo.
echo 2. サービスの起動を待機中...
timeout /t 10 /nobreak > nul

echo.
echo 3. サービスの状態を確認中...
docker-compose ps

echo.
echo ========================================
echo   Docker Selenium環境が起動しました！
echo ========================================
echo.
echo 利用可能なサービス:
echo - Selenium Grid UI: http://localhost:4444/ui/index.html
echo - VNC Viewer:       http://localhost:7900 (パスワード: secret)
echo.
echo テスト実行コマンド:
echo - 基本テスト: docker-compose exec selenium-app python selenium_test.py
echo - RPA処理:   docker-compose exec selenium-app python src/main_docker.py
echo.
echo サービス停止: docker-compose down
echo.
pause
