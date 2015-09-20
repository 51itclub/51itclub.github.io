'On Error Resume Next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder


WSHShell.run "%COMSPEC% /c """ & slfFolder & "\python27.exe"" chnroutesplus.py -p all -d 0",1,0



Wscript.quit





