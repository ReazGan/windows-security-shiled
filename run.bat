@echo off

:: =================================================================
:: Yönetici İzinlerini Kontrol Et ve İstek Gönder
:: =================================================================

:: Yönetici oturumu olup olmadığını kontrol et
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: Eğer hata kodu 0 değilse (izin yoksa), script'i yönetici olarak yeniden başlat
if '%errorlevel%' NEQ '0' (
    echo [ISTEK] Yonetici izinleri isteniyor, lutfen onaylayin...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: =================================================================
:: Programı Başlat
:: =================================================================

echo [BILGI] Yonetici izinleri onaylandi.
echo [BILGI] Windows Guvenlik Kalkani baslatiliyor...
echo.

:: Batch dosyasının bulunduğu dizine git
cd /d "%~dp0"

:: Python script'ini çalıştır (py veya python komutlarından hangisi sisteminizde tanımlıysa)
py main.py

echo.
echo [BILGI] Uygulama kapatildi. Pencereyi kapatmak icin bir tusa basin.
pause >nul
