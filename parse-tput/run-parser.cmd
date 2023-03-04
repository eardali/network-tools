::%~dp0 script path comes from file system
@echo off
set winpython="D:\WPy-3710\scripts\python.bat"

set pyscript=parse_tput.py
call %winpython% %~dp0%pyscript%

echo.
pause