# Docker Selenium環境停止スクリプト
Write-Host "Docker Selenium環境を停止しています..." -ForegroundColor Red
Write-Host ""

Write-Host "1. 実行中のコンテナを停止中..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "2. コンテナの状態を確認中..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Docker Selenium環境が停止しました！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "再起動する場合は start.ps1 または start.bat を実行してください。" -ForegroundColor White
Write-Host ""
Read-Host "Enterキーを押して終了"
