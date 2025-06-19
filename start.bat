@echo off
echo Docker Selenium�����N�����Ă��܂�...
echo.

echo 1. Docker Compose�ŃT�[�r�X���N����...
docker-compose up -d

echo.
echo 2. �T�[�r�X�̋N����ҋ@��...
timeout /t 10 /nobreak > nul

echo.
echo 3. �T�[�r�X�̏�Ԃ��m�F��...
docker-compose ps

echo.
echo ========================================
echo   Docker Selenium�����N�����܂����I
echo ========================================
echo.
echo ���p�\�ȃT�[�r�X:
echo - Selenium Grid UI: http://localhost:4444/ui/index.html
echo - VNC Viewer:       http://localhost:7900 (�p�X���[�h: secret)
echo.
echo �e�X�g���s�R�}���h:
echo - ��{�e�X�g: docker-compose exec selenium-app python selenium_test.py
echo - RPA����:   docker-compose exec selenium-app python src/main_docker.py
echo.
echo �T�[�r�X��~: docker-compose down
echo.
pause
