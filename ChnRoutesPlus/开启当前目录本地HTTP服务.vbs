'═════代═══码═══开═══始═════
'On Error Resume Next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder

if not fso.fileexists(slfFolder & "\python.exe") and not fso.fileexists(WshShell.ExpandEnvironmentStrings("%windir%\python.exe")) then WSHShell.popup "缺少Python运行时!",8,"错误":wscript.quit


lport=8000
port=lport
msg="HTTP服务已经开启"
Set regEx = New RegExp

Function RegExpTest(patrn, strng)
    Dim regEx, Match, Matches
    Set regEx = New RegExp
    regEx.Pattern = patrn
    regEx.IgnoreCase = True
    regEx.Global = True
    Set Matches = regEx.Execute(strng)
    For Each Match in Matches
        'RetStr = RetStr & "Match " & I & " found at position "
        'RetStr = RetStr & Match.FirstIndex & ". Match Value is "'
        'RetStr = RetStr & Match.Value & "'." & vbCRLF
        'RetStr=replace(strng,Match.Value,"")
        'RetStr=RetStr & Match.FirstIndex & ". Match Value is "+Match.Value+"<br>"
        RetStr=Match.Value
    Next
    RegExpTest = RetStr
End Function


c=0
Set objCimv = GetObject("winmgmts:\\.\root\cimv2")
Set colProcess = objCimv.ExecQuery("Select * from Win32_Process where name='python.exe'")
For Each objProcess in colProcess
     objCMDL=objProcess.CommandLine
     'wscript.echo objCMDL
     if InStr(objCMDL,"SimpleHTTPServer")>0 then
        'wscript.echo RegExpTest("\d+",objCMDL):wscript.quit
        if RegExpTest("\d+",objCMDL)>port then port=RegExpTest("\d+",objCMDL)
        msg=msg  & vbCrLf & "端口号:" & RegExpTest("\d+",objCMDL)
        c=c+1
     end if
Next
Set colProcess = objCimv.ExecQuery("Select * from Win32_Process where name='python27.exe'")
For Each objProcess in colProcess
    objCMDL=objProcess.CommandLine
    if InStr(objCMDL,"SimpleHTTPServer")>0 then
        if RegExpTest("\d+",objCMDL)>port then port=RegExpTest("\d+",objCMDL)
        msg=msg  & vbCrLf & "端口号:" & RegExpTest("\d+",objCMDL)
        c=c+1
    end if
Next
'wscript.echo msg:wscript.quit
if c>0 then
    port=port+1
    if WSHShell.popup(msg  & vbCrLf & "是否关闭所有端口?",8,"温馨提示",vbYesNo)=vbYes then
        port=lport
        set objCimv=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='python.exe'")
        for each objProcess in objCimv
            if InStr(objProcess.CommandLine,"SimpleHTTPServer")>0 then objProcess.terminate()
        next
        set objCimv=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='python27.exe'")
        for each objProcess in objCimv
            if InStr(objProcess.CommandLine,"SimpleHTTPServer")>0 then objProcess.terminate()
        next
    end if
    'wscript.echo port:wscript.quit
end if


if WSHShell.popup("是否开启当前目录的HTTP服务?",8,"温馨提示",vbYesNo)=vbYes then
    do
        WSHShell.run "%COMSPEC% /c " & WshShell.ExpandEnvironmentStrings("%windir%\python.exe") & " -m SimpleHTTPServer " & port,0,0
        cc=0
        Set objCimv = GetObject("winmgmts:\\.\root\cimv2")
        Set colProcess = objCimv.ExecQuery("Select * from Win32_Process where name='python.exe'")
        For Each objProcess in colProcess
             objCMDL=objProcess.CommandLine
             'wscript.echo objCMDL
             if InStr(objCMDL,"SimpleHTTPServer")>0 then
                cc=cc+1
             end if
        Next
        Set colProcess = objCimv.ExecQuery("Select * from Win32_Process where name='python27.exe'")
        For Each objProcess in colProcess
             objCMDL=objProcess.CommandLine
             if InStr(objCMDL,"SimpleHTTPServer")>0 then
                cc=cc+1
             end if
        Next
        if not cc>c then port=port+1
        if port>8050 then cc=c+10
    loop until cc>c
    WSHShell.popup "已成功开启当前目录的HTTP服务!" & vbCrLf & "端口号:" & port & vbCrLf & "按确认键将进行预览......",6,"恭喜"
    WSHShell.run "iexplore.exe http://127.0.0.1:" & port,1,0
end if


Wscript.quit
'═════代═══码═══结═══束═════

isOccupied = 0
Set oExec = WshShell.Exec("netstat -an")
Set oStdOut = oExec.StdOut
Do Until oStdOut.AtEndOfStream
    strLine = oStdOut.ReadLine
    If InStr(strLine, ":" & port) > 0 And InStrRev(strLine, "ESTABLISHED") > 0 Then
        isOccupied = 1
        Exit Do
    End If
Loop
If isOccupied Then
    MsgBox "Port " & port & " is occupied!", vbExclamation + vbSystemModal, "Busy"
Else
    MsgBox "Port " & port & " is idle!", vbInformation + vbSystemModal, "Idle"
End If


