@echo off
title BIST ORACLE AI Launcher
echo BIST ORACLE Yukleniyor...
echo =======================================

set "PYTHON_EXE="

echo Python kurulumu araniyor...

:: 1. Standart python komutunu dene
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto :run
)

:: 2. Windows 'py' yonlendiricisini dene
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py"
    goto :run
)

:: 3. PATH'te yoksa, gizli uygulama dosyalarinda (C:\Users\...\AppData\Local\Programs\Python\) varsayilan yeri ara
for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        set "PYTHON_EXE=%%i\python.exe"
        goto :run
    )
)

:: Eger hicbiri bulunamazsa
echo.
echo =======================================
echo CRITIK HATA: Bilgisayarinizda Python yuklu degil veya dogru kurulamamis!
echo BIST ORACLE'i calistirmak icin Python.org adresinden Python indirmeli
echo ve kurarken en alttaki "Add Python to PATH" (veya "Add python.exe to PATH") kutusunu isaretlemelisiniz.
echo =======================================
pause
exit /b

:run
echo Python bulundu: %PYTHON_EXE%
echo.
echo 1. Gereksinimler Kontrol Ediliyor/Yukleniyor...
"%PYTHON_EXE%" -m pip install -r requirements.txt

echo.
echo 2. Oracle Web Arayuzu Baslatiliyor...
"%PYTHON_EXE%" -m streamlit run ui\streamlit_app.py

pause
