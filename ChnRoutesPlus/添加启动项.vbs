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
    if WSHShell.Popup("是否将vpnup加入到启动项？(本对话框6秒后消失)", 6, "VPNUP 对话框", 1+32) = 1 then
        CreateShortcut(fso.GetSpecialFolder(1) & "\wscript.exe")
        WSHShell.Popup "成功加入VPNUP到启动项", 5, "VPNUP 对话框", 64
    else
        fso.deletefile WSHShell.SpecialFolders("Startup") & "\vpnup.lnk"
    end if
end function

