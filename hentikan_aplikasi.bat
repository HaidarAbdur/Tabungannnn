@echo off
echo Menghentikan server FastAPI dan Streamlit...

:: Menghentikan proses uvicorn (FastAPI)
wmic process where "name='python.exe' and commandline like '%%uvicorn%%'" call terminate >nul 2>&1

:: Menghentikan proses streamlit
wmic process where "name='python.exe' and commandline like '%%streamlit%%'" call terminate >nul 2>&1

echo Aplikasi berhasil dihentikan.
pause
