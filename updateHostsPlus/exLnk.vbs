'on error resume next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder

strSendTo =WshShell.SpecialFolders("SendTo")      '特殊文件夹“发送到”
strDesktop = WshShell.SpecialFolders("Desktop")   '特殊文件夹“桌面”
strFavorites = WshShell.SpecialFolders("Favorites")  '特殊文件夹“收藏夹”
strProgram = WshShell.SpecialFolders("AllUsersPrograms")
strStartup =WshShell.SpecialFolders("Startup")
if fso.folderexists(strProgram & "\实用工具") then
  'fso.deleteFolder strProgram & "\实用工具",1
else
    fso.CreateFolder strProgram & "\实用工具"
end if



strComputer = "."
Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
Set colOperatingSystems = objWMIService.ExecQuery("Select * from Win32_OperatingSystem")
for each objOperatingSystem in colOperatingSystems
    'wscript.echo "@" & objOperatingSystem.Version & "@"
    'if instr(objOperatingSystem.Caption,"Windows 7")>0 then IsWin7=1
    if instr(objOperatingSystem.Version,"5.1")>0 then
        gs="Winxp"
    elseif instr(objOperatingSystem.Version,"6.1")>0 then
        gs="Win7"
    elseif instr(objOperatingSystem.Version,"6.")>0 then
        gs="Win8"
    elseif instr(objOperatingSystem.Version,"10.")>0 then
        gs="Win10"
    else
        gs="Winxp"
    end if
next


is64bit=0
strPID = WshShell.ExpandEnvironmentStrings("%PROCESSOR_IDENTIFIER%")
'wscript.echo lcase(left(strPID,3)):Wscript.quit
if not lcase(left(strPID,3))="x86" then is64bit=1
'wscript.echo is64bit:Wscript.quit
'call cv("UltraISO.exe")




tosue "VPN\真心QQ金牌网吧代理\\exLnk.vbs","VPN.真心QQ金牌网吧代理.更新链接","VPN.真心QQ金牌网吧代理.更新链接"
tosm "VPN\真心QQ金牌网吧代理\\真心QQ金牌网吧*.exe","VPN.真心QQ金牌网吧代理","真心QQ金牌网吧代理"
tozm "VPN\真心QQ金牌网吧代理\\真心QQ金牌网吧*.exe","VPN.真心QQ金牌网吧代理","真心QQ金牌网吧代理"

'wscript.echo fm("VPN\真心QQ金牌网吧代理\\真心QQ金牌网吧*.exe")
wscript.quit


function fm(exename)
    strpath="[none]"
    if instr(exename,":")<1 then
        if instr(exename,"\\")>0 then
            strpath = nxg("D:\Program Files\实用工具\" & exename)
            'wscript.echo gp(exename):wscript.quit
            if instr(exename,"*")>0 and instr(exename,"*")<instr(exename,"\\") then wscript.echo "第一个路径参数有误!":wscript.quit
            if instr(exename,"*")>instr(exename,"\\") and fso.folderexists(gp(strpath)) then
                set fods = fso.getfolder(gp(strpath))
                tm = "[none]"
                fp = "[none]"
                fn = "[none]"
                set fis=fods.files
                for each fi in fis
                    if instr(fi.path,left(strpath,instr(strpath,"*")-1))>0 then
                        if right(strpath,1)="*" or instr(replace(fi.path,left(strpath,instr(strpath,"*")-1),""),right(strpath,len(strpath)-instrrev(strpath,"*")))>0 then
                            if tm="[none]" or tm < fi.datelastmodified then
                                tm = fi.datelastmodified
                                fp = fi.path
                                fn=fi.name
                            end if
                        end if
                        'wscript.echo fn:wscript.quit
                    end if
                next
                if fn<>"[none]" then strpath = fp:exename=gp(exename) & "\" & fn
                'wscript.echo exename:wscript.quit
            end if
            if not fso.fileexists(strpath) and WshShell.ExpandEnvironmentStrings("%ProgramFiles%")<>"%ProgramFiles%" and instr(WshShell.ExpandEnvironmentStrings("%ProgramFiles%"),WshShell.ExpandEnvironmentStrings("%systemdrive%"))<1 then
                strpath = nxg(WshShell.ExpandEnvironmentStrings("%ProgramFiles%\实用工具\" & exename ))
                'wscript.echo gp(exename):wscript.quit
                if instr(exename,"*")>0 and instr(exename,"*")<instr(exename,"\\") then wscript.echo "第一个路径参数有误!":wscript.quit
                if instr(exename,"*")>instr(exename,"\\") and fso.folderexists(gp(strpath)) then
                    set fods = fso.getfolder(gp(strpath))
                    tm = "[none]"
                    fp = "[none]"
                    fn = "[none]"
                    set fis=fods.files
                    for each fi in fis
                        if instr(fi.path,left(strpath,instr(strpath,"*")-1))>0 then
                            if right(strpath,1)="*" or instr(replace(fi.path,left(strpath,instr(strpath,"*")-1),""),right(strpath,len(strpath)-instrrev(strpath,"*")))>0 then
                                if tm="[none]" or tm < fi.datelastmodified then
                                    tm = fi.datelastmodified
                                    fp = fi.path
                                    fn=fi.name
                                end if
                            end if
                            'wscript.echo fn:wscript.quit
                        end if
                    next
                    if fn<>"[none]" then strpath = fp:exename=gp(exename) & "\" & fn
                    'wscript.echo exename:wscript.quit
                end if
            end if
        end if
        if not fso.fileexists(strpath) then
            strpath = nxg(WshShell.ExpandEnvironmentStrings("%systemdrive%\Program Files\实用工具\" & exename ))
            if instr(exename,"*")>0 and instr(exename,"*")<instr(exename,"\") then wscript.echo "第一个路径参数有误!":wscript.quit
            if instr(strpath,"*")>instr(exename,"\") and fso.folderexists(gp(strpath)) then
                set fods = fso.getfolder(gp(strpath))
                tm = "[none]"
                fp = "[none]"
                fn = "[none]"
                set fis=fods.files
                for each fi in fis
                    if instr(fi.path,left(strpath,instr(strpath,"*")-1))>0 then
                        if right(strpath,1)="*" or instr(replace(fi.path,left(strpath,instr(strpath,"*")-1),""),right(strpath,len(strpath)-instrrev(strpath,"*")))>0 then
                            if tm="[none]" or tm < fi.datelastmodified then
                                tm = fi.datelastmodified
                                fp = fi.path
                                fn=fi.name
                            end if
                        end if
                        'wscript.echo fn:wscript.quit
                    end if
                next
                if fn<>"[none]" then strpath = fp:exename=gp(exename) & "\" & fn
                'wscript.echo exename:wscript.quit
            end if
        end if

        if not fso.fileexists(strpath) then
            strpath=nxg(slfFolder & "\" & gn(exename))
            if instr(exename,"*")>0 and instr(exename,"*")<instr(exename,"\") then wscript.echo "第一个路径参数有误!":wscript.quit
            if instr(strpath,"*")>instr(exename,"\") and fso.folderexists(gp(strpath)) then
                set fods = fso.getfolder(gp(strpath))
                tm = "[none]"
                fp = "[none]"
                fn = "[none]"
                set fis=fods.files
                for each fi in fis
                    if instr(fi.path,left(strpath,instr(strpath,"*")-1))>0 then
                        if right(strpath,1)="*" or instr(replace(fi.path,left(strpath,instr(strpath,"*")-1),""),right(strpath,len(strpath)-instrrev(strpath,"*")))>0 then
                            if tm="[none]" or tm < fi.datelastmodified then
                                tm = fi.datelastmodified
                                fp = fi.path
                                fn=fi.name
                            end if
                        end if
                        'wscript.echo fn:wscript.quit
                    end if
                next
                if fn<>"[none]" then strpath = fp:exename=gp(exename) & "\" & fn
                'wscript.echo exename:wscript.quit
            end if
        end if
    else
        strpath = nxg(exename)
        if instr(exename,"*")>0 and instr(exename,"*")<instr(exename,"\") then wscript.echo "第一个路径参数有误!":wscript.quit
        if instr(strpath,"*")>instr(exename,"\") and fso.folderexists(gp(strpath)) then
            set fods = fso.getfolder(gp(strpath))
            tm = "[none]"
            fp = "[none]"
            fn = "[none]"
            set fis=fods.files
            for each fi in fis
                if instr(fi.path,left(strpath,instr(strpath,"*")-1))>0 then
                    if right(strpath,1)="*" or instr(replace(fi.path,left(strpath,instr(strpath,"*")-1),""),right(strpath,len(strpath)-instrrev(strpath,"*")))>0 then
                        if tm="[none]" or tm < fi.datelastmodified then
                            tm = fi.datelastmodified
                            fp = fi.path
                            fn=fi.name
                        end if
                    end if
                    'wscript.echo fn:wscript.quit
                end if
            next
            if fn<>"[none]" then strpath = fp:exename=gp(exename) & "\" & fn
            'wscript.echo exename:wscript.quit
        end if
    end if

    if not fso.fileexists(strpath) then fm="[none]":exit function
    fm=strpath
    'wscript.echo strpath
end function



'开始菜单
sub tosm(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strProgram & "\实用工具\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub

function cv(exename)
  if right(exename,4)=".exe" then cv=left(exename,len(exename)-4) & ".fkt" else cv=exename
  'wscript.echo cv:wscript.quit
end function

function gn(en)
  if instr(en,"\")>0 then gn=right(en,len(en)-instrrev(en,"\")) else gn=en
  'wscript.echo gn:wscript.quit
end function

function gp(en)
  if instr(en,"\")>0 then gp=nxg(left(en,instrrev(en,"\"))) else gp=slfFolder
  'wscript.echo gp:wscript.quit
end function

function nxg(str)
    tmpstr= replace(str,"\\","\")
    tmpstr= replace(tmpstr,"\\","\")
    tmpstr= replace(tmpstr,"\\","\")
    tmpstr= replace(tmpstr,"\\","\")
    nxg= replace(tmpstr,"\\","\")
end function




'发送到菜单
sub tost(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strSendTo & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub
sub tostex(exename,lnkname,description,agu)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strSendTo & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  if not agu="" then oShellLink.Arguments = agu
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub


'桌面
sub tozm(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strDesktop & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub
sub tozmex(exename,lnkname,description,agu)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strDesktop & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  if not agu="" then oShellLink.Arguments = agu
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub

'启动菜单
sub tosu(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strStartup & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  oShellLink.Windowstyle = 7
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
  set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='" & fso.GetBaseName(strPath) & "." & fso.GetExtensionName(strPath) & "'")
  for each i in c
    i.terminate()
  next
  WSHShell.currentdirectory=fso.GetParentFolderName(strPath)
  WshShell.run """" & strpath & """",,0
end sub
sub tosue(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strStartup & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  oShellLink.Windowstyle = 7
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
  'set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='" & fso.GetBaseName(strPath) & "." & fso.GetExtensionName(strPath) & "'")
  'for each i in c
  '  i.terminate()
  'next
  WSHShell.currentdirectory=fso.GetParentFolderName(strPath)
  'WshShell.run """" & strpath & """",,0
end sub
sub tosuex(exename,lnkname,description,agu)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strStartup & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '创建一个快捷方式对象
  if not agu="" then oShellLink.Arguments = agu
  oShellLink.Windowstyle = 7
  oShellLink.Description = description '设置快捷方式的描述
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
  'set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='" & fso.GetBaseName(strPath) & "." & fso.GetExtensionName(strPath) & "'")
  'for each i in c
  '  i.terminate()
  'next
  WSHShell.currentdirectory=fso.GetParentFolderName(strPath)
  'WshShell.run """" & strpath & """",,0
end sub


'justrun仅仅执行
sub jrun(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  WSHShell.currentdirectory=fso.GetParentFolderName(strPath)
  set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='" & fso.GetBaseName(strPath) & "." & fso.GetExtensionName(strPath) & "'")
  for each i in c
    i.terminate()
  next
  WshShell.run """" & strpath & """",,0
end sub
sub jrunex(exename,lnkname,description,agu)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="[none]" or not fso.fileexists(strpath) then exit sub

  WSHShell.currentdirectory=fso.GetParentFolderName(strPath)
  set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='" & fso.GetBaseName(strPath) & "." & fso.GetExtensionName(strPath) & "'")
  for each i in c
    i.terminate()
  next
  if not agu="" then WshShell.run """" & strpath & """ " & agu,,0
end sub
