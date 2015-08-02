@echo off&SETLOCAL ENABLEDELAYEDEXPANSION
set path=%path%;%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem;"%~dp0";"%cd:"=%"
set ERRORLEVEL=
pushd "%~dp0"

title 切换下载核心
ren updateHosts.py updateHosts.tmp.py
ren updateHosts_1.py updateHosts.py
ren updateHosts.tmp.py updateHosts_1.py
echo 切换完毕!

popd
echo 任意键退出...
rem if not "%~1"=="-s" pause >nul
REM ENDLOCAL
exit
