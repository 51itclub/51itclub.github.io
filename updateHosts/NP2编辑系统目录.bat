@echo off
set path=%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem
pushd "%~dp0"
start notepad2 "%systemroot%\system32\drivers\etc\hosts"
popd
::echo ��������˳�...
::pause >nul
exit