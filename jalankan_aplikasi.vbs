Set WshShell = CreateObject("WScript.Shell")
' Menjalankan FastAPI di background (tanpa terminal)
WshShell.Run "cmd /c uvicorn api:app --host 0.0.0.0 --port 8000", 0, False

' Menjalankan Streamlit di background (tanpa terminal)
WshShell.Run "cmd /c streamlit run app.py --server.address 0.0.0.0 --server.port 8501", 0, False
