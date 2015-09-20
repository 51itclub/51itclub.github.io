'详细出处参考：http://www.jb51.net/article/29233.htm

Set objWMIServices = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
Set objWbemObjectSet = objWMIServices.ExecQuery(_
"SELECT * FROM Win32_Process WHERE " &_
"ExecutablePath='" & Replace(WScript.FullName,"\","\\") & "' and " & _
"CommandLine LIKE '%" & WScript.ScriptName & "%'")
for each objWbemObject in objWbemObjectSet
  cmdline = objWbemObject.CommandLine
next
if WScript.Arguments.Count then
  file = WScript.Arguments(0)
  if file="/?" then
    call ShowHelp()
    WScript.Quit
  end if
  Set RegEx = new RegExp
  RegEx.IgnoreCase = true
  RegEx.Global = true
  RegEx.Pattern = "\\|\/|\||\(|\)|\[|\]|\{|\}|\^|\$|\.|\*|\?|\+"
  temp1 = RegEx.Replace(WScript.ScriptName, "\$&")
  temp2 = RegEx.Replace(file, "\$&")
  RegEx.Global = false
  RegEx.Pattern = "^.*?" & temp1 & "[""\s]*" & temp2 & """?\s*"
  args = RegEx.Replace(cmdline, "")
  'WScript.Echo file, args
else
  file = "cmd.exe"
  args = "/k """ & CreateObject("WScript.Shell").CurrentDirectory & "\vpnup-win.bat" & Chr(34)
end if

'核心代码
Set sh = CreateObject("Shell.Application")
call sh.ShellExecute( file, args, , "runas" )

function ShowHelp()
  dim HelpStr
  HelpStr = "以管理员身份运行程序。" & vbCrLf _
  & vbCrLf _
  & WScript.ScriptName & " [program] [parameters]..." & vbCrLf _
  & vbCrLf _
  & "program 要运行的程序" & vbCrLf _
  & "parameters 传递给 program 的参数" & vbCrLf _
  & vbCrLf
  WScript.Echo HelpStr
end function
