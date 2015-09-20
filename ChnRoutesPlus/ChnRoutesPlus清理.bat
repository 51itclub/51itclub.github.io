@echo off&SETLOCAL ENABLEDELAYEDEXPANSION
set path=%path%;%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem;"%~dp0";"%cd:"=%"
set ERRORLEVEL=
pushd "%~dp0"

title ChnRoutesPlus清理
pause

call :mydel test.txt
call :mydel route.dat
call :mydel routes.txt
call :mydel vpnup.bat
call :mydel ip-up
call :mydel vpndown.bat
call :mydel ip-down
call :mydel vpnup_linux.sh
call :mydel vpnup_android.sh
call :mydel vpnup-win.bat
call :mydel vpnup-winp.bat
call :mydel ip-up_mac
call :mydel vpndown_linux.sh
call :mydel vpndown_android.sh
call :mydel vpndown-win.bat
call :mydel vpndown-winp.bat
call :mydel ip-down_mac

echo 清理完毕!

popd
echo 任意键退出...
if not "%~1"=="-s" pause >nul
REM ENDLOCAL
exit

:mydel
if exist "%~1" echo file:%~nx1
del /f /q "%~1" 2>nul
goto :EOF

