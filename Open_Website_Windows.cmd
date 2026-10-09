@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 goto use_py
where python >nul 2>nul
if not errorlevel 1 goto use_python
echo Python 3 was not found. Install Python 3, or follow START_HERE.txt.
pause
exit /b 1

:use_py
set "website_python=py -3"
goto run_site

:use_python
set "website_python=python"

:run_site
echo Opening the website at http://127.0.0.1:8000/
echo Keep this window open. Closing it stops the local server.
start "" "http://127.0.0.1:8000/"
%website_python% -m http.server 8000 --bind 127.0.0.1 --directory dist
pause
