

function CreateShortcut(target_path)
{
   wsh = new ActiveXObject('WScript.Shell');

   link = wsh.CreateShortcut(wsh.SpecialFolders("Startup") + '\\shadowsocks.lnk');
   link.TargetPath = target_path;
   //link.Arguments = '"' + wsh.CurrentDirectory + '\\proxy.py"';
   //link.WindowStyle = 7;
   link.Description = 'shadowsocks代理';
   link.WorkingDirectory = wsh.CurrentDirectory;
   link.Save();

   link = wsh.CreateShortcut(wsh.SpecialFolders("Startup") + '\\privoxy4shadowsocks.lnk');
   link.TargetPath = '"' + wsh.CurrentDirectory + '\\privoxy.exe"';
   //link.Arguments = '"' + wsh.CurrentDirectory + '\\proxy.py"';
   //link.WindowStyle = 7;
   link.Description = 'SOCKS代理转HTTP';
   link.WorkingDirectory = wsh.CurrentDirectory;
   link.Save();
}

function main()
{
   wsh = new ActiveXObject('WScript.Shell');
   fso = new ActiveXObject('Scripting.FileSystemObject');

   if(wsh.Popup('是否将shadowsocks.exe加入到启动项？(本对话框6秒后消失)', 6, 'shadowsocks 对话框', 1+32) == 1) {
       CreateShortcut('"' + wsh.CurrentDirectory + '\\shadowsocks.exe"');
       wsh.Popup('成功加入shadowsocks到启动项', 5, 'shadowsocks 对话框', 64);
   }
}

main();
