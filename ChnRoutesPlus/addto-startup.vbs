'�T�T�T�T�T���T�T�T��T�T�T���T�T�Tʼ�T�T�T�T�T
On Error Resume Next
set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder

strSendTo =WshShell.SpecialFolders("SendTo")      '�����ļ��С����͵���
strDesktop = WshShell.SpecialFolders("Desktop")   '�����ļ��С����桱
strFavorites = WshShell.SpecialFolders("Favorites")  '�����ļ��С��ղؼС�
strProgram = WshShell.SpecialFolders("AllUsersPrograms")
strStartup =WshShell.SpecialFolders("Startup")

Set Args = WScript.Arguments
allarg=""
for each arg in args
  allarg=allarg&arg
next

if not fso.fileexists(slfFolder & "\python.exe") and not fso.fileexists(WshShell.ExpandEnvironmentStrings("%windir%\python.exe")) and instr(allarg,"-s")<1 then WSHShell.popup "ȱ��Python����ʱ!",8,"����":wscript.quit




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








choice=1
if instr(allarg,"-s")>0 then choice=1 else choice=WSHShell.Popup("���������(���Ի���6�����ʧ)", 6, "��ܰ��ʾ", 1+32)
if choice = 1 then
    'tosu "gen.pac.vbs","����PAC","����PAC"
    tosu "gen.win.vbs","����WIN","����WIN"
    'tosu "gen.winfc.vbs","����WINFC","����WINFC"
    'tosuex "vpnup-win.bat","VPNUP","����·�ɿ���","-s"
    tosu "vpnup-win.vbs","VPNUP","����·�ɿ���"
    if instr(allarg,"-s")<1 then WSHShell.Popup "�ɹ�����������", 5, "��ܰ��ʾ", 64
else
    'fso.deletefile WSHShell.SpecialFolders("Startup") & "\����PAC.lnk"
    fso.deletefile WSHShell.SpecialFolders("Startup") & "\����WIN.lnk"
    'fso.deletefile WSHShell.SpecialFolders("Startup") & "\����WINFC.lnk"
    fso.deletefile WSHShell.SpecialFolders("Startup") & "\VPNUP.lnk"
end if











Wscript.quit
'�T�T�T�T�T���T�T�T��T�T�T��T�T�T���T�T�T�T�T


'�����˵�
sub tosu(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="none" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strStartup & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '����һ����ݷ�ʽ����
  oShellLink.Windowstyle = 7
  oShellLink.Description = description '���ÿ�ݷ�ʽ������
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
  if strpath="none" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strStartup & "\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '����һ����ݷ�ʽ����
  if not agu="" then oShellLink.Arguments = agu
  oShellLink.Windowstyle = 7
  oShellLink.Description = description '���ÿ�ݷ�ʽ������
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
  'set c=getobject("winmgmts:\\.\root\cimv2").execquery("select * from win32_process where name='" & fso.GetBaseName(strPath) & "." & fso.GetExtensionName(strPath) & "'")
  'for each i in c
  '  i.terminate()
  'next
  WSHShell.currentdirectory=fso.GetParentFolderName(strPath)
  'WshShell.run """" & strpath & """",,0
end sub


'��ʼ�˵�
sub tosm(exename,lnkname,description)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="none" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strProgram & "\ʵ�ù���\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '����һ����ݷ�ʽ����
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '���ÿ�ݷ�ʽ������
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub
sub tosmex(exename,lnkname,description,agu)
  strpath = fm(exename)
  'wscript.echo strpath
  if strpath="none" or not fso.fileexists(strpath) then exit sub

  set oShellLink = WshShell.CreateShortcut(strProgram & "\ʵ�ù���\" & lnkname & ".lnk")
  oShellLink.TargetPath =strpath '����һ����ݷ�ʽ����
  if not agu="" then oShellLink.Arguments = agu
  oShellLink.Windowstyle = 1
  oShellLink.Description = description '���ÿ�ݷ�ʽ������
  oShellLink.WorkingDirectory = fso.GetParentFolderName(strPath)
  oShellLink.Save
end sub

function cv(exename)
  if right(exename,4)=".exe" then cv=left(exename,len(exename)-4) & ".fkt" else cv=exename
  'wscript.echo cv:wscript.quit
end function

function gn(en)
  gn=right(en,len(en)-instrrev(en,"\"))
  'wscript.echo gn:wscript.quit
end function

function gp(en)
  gp=nxg(left(en,instrrev(en,"\")))
  'wscript.echo gp:wscript.quit
end function

function nxg(str)
    tmpstr= replace(str,"\\","\")
    nxg= replace(tmpstr,"\\","\")
end function

function fm(exename)
  strpath="none"
  if instr(exename,":")<1 then
      if instr(exename,"\")<1 then exename="\\"&exename

      if instr(exename,"\\")>0 then
        strpath = nxg("D:\Program Files\ʵ�ù���\" & exename)
          'wscript.echo gp(strpath):wscript.quit
          if instr(strpath,"*.")>0 then
            set fods = fso.getfolder(gp(strpath))
            tm = "none"
            'snow = 0
            set fis=fods.files
            for each fi in fis
                'wscript.echo instrrev(strpath,"*.")-1
                if instr(fi.path,left(strpath,instrrev(strpath,"*.")-1))>0 and right(strpath,len(strpath)-instrrev(strpath,"."))=right(fi.name,len(fi.name)-instrrev(fi.name,".")) then
                    if tm="none" or tm < fi.datelastmodified then
                        tm = fi.datelastmodified
                        fp = fi.path
                        'fn=fi.name
                    end if
                    'snow = snow +1
                    'wscript.echo fp
                end if
            next
            strpath = fp
            'if snow > 20 then fso.deletefile fp
            'Wscript.echo fp&snow&fn
          end if
          fp1=nxg(slfFolder & "\" & gp(exename) & "\" & gn(strpath))
          fp2=nxg(slfFolder & "\"&gs&"\" & gp(exename) & "\" & gn(strpath))
          fp3=nxg(slfFolder & "\" & gp(exename) & "\" & cv(gn(strpath)))
          fp4=nxg(slfFolder & "\"&gs&"\" & gp(exename) & "\" & cv(gn(strpath)))
          fp5=nxg(slfFolder & "\D\" & gp(exename) & "\" & gn(strpath))
          fp6=nxg(slfFolder & "\D\" & gp(exename) & "\" & cv(gn(strpath)))
          if not fso.fileexists(fp1) and not fso.fileexists(fp2) and not fso.fileexists(fp3) and not fso.fileexists(fp4) and not fso.fileexists(fp5) and not fso.fileexists(fp6) then strpath="none"
          'Wscript.echo fp1&vbCrlf&fp2&vbCrlf&fp3&vbCrlf&fp4&vbCrlf&fp5&vbCrlf&fp6&vbCrlf&strpath
      end if

       if not fso.fileexists(strpath) and fso.folderexists("%ProgramFiles%") then
            strpath = nxg(WshShell.ExpandEnvironmentStrings("%ProgramFiles%\ʵ�ù���\" & exename ))
          if instr(strpath,"*.")>0 then
            set fods = fso.getfolder(gp(strpath))
            tm = "none"
            'snow = 0
            set fis=fods.files
            for each fi in fis
                'wscript.echo instrrev(strpath,"*.")-1
                if instr(fi.path,left(strpath,instrrev(strpath,"*.")-1))>0 and right(strpath,len(strpath)-instrrev(strpath,"."))=right(fi.name,len(fi.name)-instrrev(fi.name,".")) then
                    if tm="none" or tm < fi.datelastmodified then
                        tm = fi.datelastmodified
                        fp = fi.path
                        'fn=fi.name
                    end if
                    'snow = snow +1
                    'wscript.echo fp
                end if
            next
            strpath = fp
            'if snow > 20 then fso.deletefile fp
            'Wscript.echo fp&snow&fn
          end if
          fp1=nxg(slfFolder & "\" & gp(exename) & "\" & gn(strpath))
          fp2=nxg(slfFolder & "\"&gs&"\" & gp(exename) & "\" & gn(strpath))
          fp3=nxg(slfFolder & "\" & gp(exename) & "\" & cv(gn(strpath)))
          fp4=nxg(slfFolder & "\"&gs&"\" & gp(exename) & "\" & cv(gn(strpath)))
          if not fso.fileexists(fp1) and not fso.fileexists(fp2) and not fso.fileexists(fp3) and not fso.fileexists(fp4) then strpath="none"
          'Wscript.echo fp1&vbCrlf&fp2&vbCrlf&fp3&vbCrlf&fp4&vbCrlf&strpath
        end if

      if not fso.fileexists(strpath) then
        strpath = nxg(WshShell.ExpandEnvironmentStrings("%systemdrive%\Program Files\ʵ�ù���\" & exename ))
          if instr(strpath,"*.")>0 then
            set fods = fso.getfolder(gp(strpath))
            tm = "none"
            'snow = 0
            set fis=fods.files
            for each fi in fis
                'wscript.echo instrrev(strpath,"*.")-1
                if instr(fi.path,left(strpath,instrrev(strpath,"*.")-1))>0 and right(strpath,len(strpath)-instrrev(strpath,"."))=right(fi.name,len(fi.name)-instrrev(fi.name,".")) then
                    if tm="none" or tm < fi.datelastmodified then
                        tm = fi.datelastmodified
                        fp = fi.path
                        'fn=fi.name
                    end if
                    'snow = snow +1
                    'wscript.echo fp
                end if
            next
            strpath = fp
            'if snow > 20 then fso.deletefile fp
            'Wscript.echo fp&snow&fn
          end if
          fp1=nxg(slfFolder & "\" & gp(exename) & "\" & gn(strpath))
          fp2=nxg(slfFolder & "\"&gs&"\" & gp(exename) & "\" & gn(strpath))
          fp3=nxg(slfFolder & "\" & gp(exename) & "\" & cv(gn(strpath)))
          fp4=nxg(slfFolder & "\"&gs&"\" & gp(exename) & "\" & cv(gn(strpath)))
          if not fso.fileexists(fp1) and not fso.fileexists(fp2) and not fso.fileexists(fp3) and not fso.fileexists(fp4) then strpath="none"
          'Wscript.echo fp1&vbCrlf&fp2&vbCrlf&fp3&vbCrlf&fp4&vbCrlf&strpath
      end if

if not fso.fileexists(strpath) then
          strpath=nxg(slfFolder & "\" & gn(exename))
          if instr(strpath,"*.")>0 then
            set fods = fso.getfolder(slfFolder)
            tm = "none"
            'snow = 0
            set fis=fods.files
            for each fi in fis
                'wscript.echo instrrev(strpath,"*.")-1
                if instr(fi.path,left(strpath,instrrev(strpath,"*.")-1))>0 and right(strpath,len(strpath)-instrrev(strpath,"."))=right(fi.name,len(fi.name)-instrrev(fi.name,".")) then
                    if tm="none" or tm < fi.datelastmodified then
                        tm = fi.datelastmodified
                        fp = fi.path
                        'fn=fi.name
                    end if
                    'snow = snow +1
                    'wscript.echo fp
                end if
            next
            strpath = fp
            'if snow > 20 then fso.deletefile fp
            'Wscript.echo fp&snow&fn
          end if
      end if


  else
    strpath = nxg(exename)
          if instr(strpath,"*.")>0 then
            set fods = fso.getfolder(gp(strpath))
            tm = "none"
            'snow = 0
            set fis=fods.files
            for each fi in fis
                'wscript.echo instrrev(strpath,"*.")-1
                if instr(fi.path,left(strpath,instrrev(strpath,"*.")-1))>0 and right(strpath,len(strpath)-instrrev(strpath,"."))=right(fi.name,len(fi.name)-instrrev(fi.name,".")) then
                    if tm="none" or tm < fi.datelastmodified then
                        tm = fi.datelastmodified
                        fp = fi.path
                        'fn=fi.name
                    end if
                    'snow = snow +1
                    'wscript.echo fp
                end if
            next
            strpath = fp
            'if snow > 20 then fso.deletefile fp
            'Wscript.echo fp&snow&fn
          end if
  end if

  if not fso.fileexists(strpath) then fm="none":exit function
  fm=strpath
  'wscript.echo strpath
end function

