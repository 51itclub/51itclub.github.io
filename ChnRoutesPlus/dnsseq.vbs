' KB311218 - Cannot Change the Binding Order for Remote Access Connections
' ========================================================================
' VBScript that places the \Device\NdisWanIp entry on the top in the 
' registry value Bind (multi-string) that is found under the key 
' HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Linkage\.
' If the entry already is at the top, no registry update is done.

Const HKLM = &H80000002

sComputer = "."   ' use "." for local computer

' Connect to WMI's StdRegProv class
Set oReg = GetObject("winmgmts:{impersonationLevel=impersonate}!\\" _
         & sComputer & "\root\default:StdRegProv")

' Define registry location
sKeyPath = "SYSTEM\CurrentControlSet\Services\Tcpip\Linkage"
sValueName = "Bind"

oReg.GetMultiStringValue HKLM, sKeyPath, sValueName, arValues

arValuesNew = Array()

For i = 0 To UBound(arValues)
   If i = 0 Then
      If LCase(arValues(i)) = "\device\ndiswanip" Then
         ' Entry is already first in the list, no point in continuing
         Exit For
      Else
         ' Put NdisWanIp in the first element in the new array
         ReDim Preserve arValuesNew(0)
         arValuesNew(0) = "\Device\NdisWanIp"
      End If
   End If

   ' Continue adding the rest of the elements to the new array
   If LCase(arValues(i)) <> "\device\ndiswanip" Then
      iCountNew = UBound(arValuesNew) + 1
      ReDim Preserve arValuesNew(iCountNew)
      arValuesNew(iCountNew) = arValues(i)
   End If
Next

' If there are elements to be found in the array, update the 
' registry value 
If UBound(arValuesNew) > -1 Then
   oReg.SetMultiStringValue HKLM, sKeyPath, sValueName, arValuesNew 
End If