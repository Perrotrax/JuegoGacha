@echo off
set "GODOT_EXE=C:\Users\perri\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64.exe"
if exist "%GODOT_EXE%" (
    start "" "%GODOT_EXE%" -e --path "%~dp0godot_project"
) else (
    godot -e --path "%~dp0godot_project"
)
