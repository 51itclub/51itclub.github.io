@echo off
set path=%path%;%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem;"%~dp0";"%cd:"=%"
set ERRORLEVEL=
pushd "%~dp0"

title VPN智能路由开启
echo 正在查询当前网关，请稍候
setlocal EnableDelayedExpansion
for /F "tokens=3,4" %%i in ('route print ^| findstr "\<0.0.0.0\>"') do (set "gw=%%i"&(if "!gw:.=!"=="!gw!" set "gw=%%j")&(if "!gwf!"=="" set "gwf=%%i"&set "iof=%%j"))
if "!iof:.=!"=="!iof!" set "iof=none"
if "!gwf:.=!"=="!gwf!" set "gwf=none"
if "!gwf:.=!"=="!gwf!" if not "!iof!"=="none" set "gwf=!iof!"
rem echo %iof%
echo %gw% >>gw.txt
if not "!gwf!"=="none" echo %gwf% >>gw.txt
echo 当前网关:%gw%
echo 原网关:%gwf%
echo 接下来将开启智能路由
echo 注意需要以管理员身份运行
pause
rem tracert 183.60.45.20
rem route print
rem ipconfig /flushdns

rem set gwl=%gw%
rem set gwl=192.168.5.1
rem route CHANGE 0.0.0.0 mask 0.0.0.0 %gwl% metric 1
rem route CHANGE 192.168.5.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.1.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.2.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.137.0 mask 255.255.255.0 %gw% metric 1
rem route CHANGE 192.168.3.0 mask 255.255.255.0 %gw% metric 1

ipconfig /flushdns >nul
rem if not "!gwf!"=="none" if not "!iof!"=="none" route CHANGE 0.0.0.0 mask 0.0.0.0 %gwf% metric 20
if not "!gwf!"=="none" set "gw=!fwf!"

