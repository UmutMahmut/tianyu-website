@echo off
REM 激活 conda 环境 TDLI
CALL "C:\Users\Umut\miniconda3\Scripts\activate.bat" TDLI

REM 切换目录
cd /d C:\Users\Umut\Downloads\AstronomyInstitute (1)\AstronomyInstitute

REM 启动 Flask 网站（用 start /B 打开独立黑窗不阻塞）
start /B python run.py

REM 等待3秒，再打开网页（确保 Flask 启动完成）
timeout /t 3 >nul

REM 打开默认浏览器
start http://127.0.0.1:5000

pause
