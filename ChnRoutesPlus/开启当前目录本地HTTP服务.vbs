'On Error Resume Next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder

c=0
Set objCimv = GetObject("winmgmts:\\.\root\cimv2")
Set colProcess = objCimv.ExecQuery("Select * from Win32_Process where name='python.exe'")
For Each objProcess in colProcess
     objCMDL=objProcess.CommandLine
     if InStr(objCMDL,"SimpleHTTPServer")>0 then
        c=c+1
     end if
Next
Set colProcess = objCimv.ExecQuery("Select * from Win32_Process where name='python27.exe'")
For Each objProcess in colProcess
     objCMDL=objProcess.CommandLine
     if InStr(objCMDL,"SimpleHTTPServer")>0 then
        c=c+1
     end if
Next
if c>1 then
if MsgBox("发现HTTP服务已经开启,是否强制关闭并重新开启当前目录的HTTP服务?",vbYesNo,"温馨提示")=vbYes then
    set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='python.exe'")
    for each i in c
        i.terminate()
    next
    set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='python27.exe'")
    for each i in c
    i.terminate()
    next
    WSHShell.run "%COMSPEC% /c python.exe -m SimpleHTTPServer 8000",0,0
else
    wscript.quit
end if
end if







Wscript.quit






