@echo off
REM PyInstaller ile .exe yapmak icin:
REM 1. py -3.12 -m pip install pyinstaller
REM 2. Bu dosyayi calistir

py -3.12 -m PyInstaller --onefile --name "MevsimlerOyunu" --add-data "char.png;." --add-data "WİZARD.gif;." --add-data "music;music" --icon NUL --noconsole main.py

echo.
echo ========================
echo exe hazir: dist\MevsimlerOyunu.exe
echo Arkadaslarina gonderebilirsin!
echo ========================
pause
