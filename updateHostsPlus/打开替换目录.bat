@echo off
set path=%SystemRoot%;%SystemRoot%\system32;%SystemRoot%\System32\Wbem
start explorer /e,/select,"%systemroot%\system32\drivers\etc\hosts"
exit