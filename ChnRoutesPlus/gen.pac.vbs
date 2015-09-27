'On Error Resume Next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder

if not fso.fileexists(slfFolder & "\python.exe") and not fso.fileexists(WshShell.ExpandEnvironmentStrings("%windir%\python.exe")) then WSHShell.popup "缺少Python运行时!",8,"错误":wscript.quit

WSHShell.run "%COMSPEC% /c python.exe chnroutesplus.py -p pac",0,0

WSHShell.run "%COMSPEC% /c python.exe flora_pac_yaleh_mod.py",0,0

WSHShell.run "%COMSPEC% /c python.exe gfwlist2pacplus.py -f gfwlist.pac -p ""PROXY 192.168.2.1:8118;PROXY 192.168.2.1:8087;PROXY 127.0.0.1:8087;PROXY 127.0.0.1:8118;SOCKS5 192.168.2.1:1080;SOCKS5 127.0.0.1:1080;SOCKS5 127.0.0.1:48102;SOCKS5 127.0.0.1:65500;SOCKS5 127.0.0.1:7070;DIRECT""",0,0

Wscript.quit





