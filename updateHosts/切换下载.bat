@echo off&SETLOCAL ENABLEDELAYEDEXPANSION
set path=%path%;%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem;"%~dp0";"%cd:"=%"
set ERRORLEVEL=
pushd "%~dp0"

title �л����غ���
ren updateHosts.py updateHosts.tmp.py
ren updateHosts_1.py updateHosts.py
ren updateHosts.tmp.py updateHosts_1.py
echo �л����!

popd
echo ������˳�...
rem if not "%~1"=="-s" pause >nul
REM ENDLOCAL
exit
