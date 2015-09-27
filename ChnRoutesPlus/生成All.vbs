'On Error Resume Next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder

if not fso.fileexists(slfFolder & "\python.exe") and not fso.fileexists(WshShell.ExpandEnvironmentStrings("%windir%\python.exe")) then WSHShell.popup "缺少Python运行时!",8,"错误":wscript.quit

WSHShell.run "%COMSPEC% /c python.exe chnroutesplus.py -p all -d 0",1,0



Wscript.quit





