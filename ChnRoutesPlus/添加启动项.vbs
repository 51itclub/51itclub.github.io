set WSHShell=WScript.CreateObject("WScript.Shell")
set fso=WScript.CreateObject("Scripting.FileSystemObject")
slfFolder=fso.GetParentFolderName(fso.GetFile(Wscript.ScriptFullName))
WSHShell.currentdirectory=slfFolder


main
'if fso.fileexists(slfFolder & "\vpnup.bat") then WSHShell.run "%COMSPEC% /c "& slfFolder & "\vpnup.bat",0,1



Wscript.quit



function CreateShortcut(target_path)
   set link = WSHShell.CreateShortcut(WSHShell.SpecialFolders("Startup") & "\vpnup.lnk")
   link.TargetPath = target_path
   link.Arguments = """" & WshShell.ExpandEnvironmentStrings("%windir%") & "\vpnup.vbs"""
   link.WindowStyle = 7
   link.Description = "Auto China VPN"
   link.Save
end function

function main()
    if WSHShell.Popup("�Ƿ�vpnup���뵽�����(���Ի���6�����ʧ)", 6, "VPNUP �Ի���", 1+32) = 1 then
        CreateShortcut(fso.GetSpecialFolder(1) & "\wscript.exe")
        WSHShell.Popup "�ɹ�����VPNUP��������", 5, "VPNUP �Ի���", 64
    else
        fso.deletefile WSHShell.SpecialFolders("Startup") & "\vpnup.lnk"
    end if
end function

