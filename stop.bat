@echo off
echo Docker Selenium環境を停止しています...
echo.

echo 1. 実行中のコンテナを停止中...
docker-compose down

echo.
echo 2. コンテナの状態を確認中...
docker-compose ps

echo.
echo ========================================
echo   Docker Selenium環境が停止しました！
echo ========================================
echo.
echo 再起動する場合は start.bat を実行してください。
echo.
pause
