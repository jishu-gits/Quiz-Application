' Quiz Generator Desktop — Console-Free Launcher
' ================================================
' This VBScript wrapper launches the startup manager using pythonw.exe
' so that no console window is ever visible to the user.
'
' The Desktop shortcut points to this file.

Dim installDir, pythonExe, scriptPath, shell

' Resolve paths relative to this script's location
installDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName( _
    CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName))

' Try embedded Python first, fall back to system
pythonExe = installDir & "\runtime\python\pythonw.exe"
If Not CreateObject("Scripting.FileSystemObject").FileExists(pythonExe) Then
    pythonExe = "pythonw.exe"
End If

scriptPath = installDir & "\scripts\startup_manager.pyw"

' Launch without a console window (0 = hidden, False = don't wait)
Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = installDir
shell.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
