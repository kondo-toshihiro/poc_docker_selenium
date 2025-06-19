# Docker Selenium環境起動スクリプト
Write-Host "Docker Selenium環境を起動しています..." -ForegroundColor Green
Write-Host ""

Write-Host "1. Docker Composeでサービスを起動中..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "2. サービスの起動を待機中..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "3. サービスの状態を確認中..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Selenium環境が起動しました！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "利用可能なサービス:" -ForegroundColor White
Write-Host "- Selenium Grid UI: http://localhost:4444/ui/index.html" -ForegroundColor Gray
Write-Host "- VNC Viewer:       http://localhost:7900 (パスワード: secret)" -ForegroundColor Gray
Write-Host ""
Write-Host "テスト実行コマンド:" -ForegroundColor White
Write-Host "- 基本テスト: docker-compose exec selenium-app python selenium_test.py" -ForegroundColor Gray
Write-Host "- RPA処理:   docker-compose exec selenium-app python src/main_docker.py" -ForegroundColor Gray
Write-Host ""
Write-Host "サービス停止: docker-compose down" -ForegroundColor White
Write-Host ""
Read-Host "Enterキーを押して終了"
