
ipconfig /flushdns >nul
echo ¿ªÆôÍê±Ï!
rem pause>nul
popd
exit



:rt
route CHANGE %* 2>nul
route -p add %* 2>nul
goto :EOF