@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ver=v5.3"
title aLD3N Print Spooler Tool %ver%
mode con: cols=50 lines=19
color 07

:: ANSI colors (green highlight)
for /f %%A in ('echo prompt $E ^| cmd') do set "ESC=%%A"
set "GREEN=%ESC%[92m"
set "WHITE=%ESC%[0m"

:: --- (Admin Check) ---
fltmc >nul 2>&1 || (
  echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\GetAdmin.vbs"
  echo UAC.ShellExecute "%~fs0", "", "", "runas", 1 >> "%temp%\GetAdmin.vbs"
  cmd /u /c type "%temp%\GetAdmin.vbs" > "%temp%\GetAdminUnicode.vbs"
  cscript //nologo "%temp%\GetAdminUnicode.vbs"
  del /f /q "%temp%\GetAdmin.vbs" >nul 2>&1
  del /f /q "%temp%\GetAdminUnicode.vbs" >nul 2>&1
  exit /b
)

:menu
call :getSpoolerStatus
cls
echo.
call :center "====================================="
call :center "%GREEN%PRINT SPOOLER TOOL %ver%%WHITE%"
call :center "====================================="
call :center "Status: %GREEN%!SPOOLER_STATUS!%WHITE%"
echo.
call :center "[1] %GREEN%ENABLE%WHITE% Print Spooler"
call :center "(Auto + Restart + Clear Queue)"
echo.
call :center "[2] %GREEN%DISABLE%WHITE% Print Spooler"
call :center "(Stop + Disabled)"
echo.
call :center "[3] EXIT"
echo.
call :center "_____________________________________"
echo.

call :center "%GREEN%Select an option (1-3):%WHITE%"
set "choice="
set /p choice=

if not defined choice goto menu
if "%choice%"=="1" goto enable
if "%choice%"=="2" goto disable
if "%choice%"=="3" exit /b
goto menu


:enable
cls
echo.
call :center "====================================="
call :center "%GREEN%ENABLE%WHITE% PRINT SPOOLER"
call :center "====================================="
echo.

call :center "%GREEN%[*] Setting startup to: AUTO%WHITE%"
sc config spooler start= auto >nul
call :center "%GREEN%[*] Restarting service...%WHITE%"
net stop spooler >nul 2>&1
call :center "%GREEN%[*] Clearing print queue...%WHITE%"
del /q /f "%WINDIR%\System32\spool\PRINTERS\*" 2>nul
net start spooler >nul
echo.
call :center "%GREEN%[+] Spooler Enabled Successfully.%WHITE%"
echo.
call :center "Press any key to return to menu..."
pause >nul
goto menu


:disable
cls
echo.
call :center "====================================="
call :center "%GREEN%DISABLE%WHITE% PRINT SPOOLER"
call :center "====================================="
echo.

call :center "%GREEN%[*] Stopping service...%WHITE%"
net stop spooler >nul 2>&1
call :center "%GREEN%[*] Setting startup to: DISABLED%WHITE%"
sc config spooler start= disabled >nul
echo.
call :center "%GREEN%[+] Spooler Disabled Successfully.%WHITE%"
echo.
call :center "Press any key to return to menu..."
pause >nul
goto menu


:getSpoolerStatus
set "SPOOLER_STATUS=UNKNOWN"

:: Get START_TYPE (AUTO/DEMAND/DISABLED)
set "START_TYPE="
for /f "tokens=3" %%A in ('sc qc spooler ^| findstr /i "START_TYPE"') do set "START_TYPE=%%A"

if /i "%START_TYPE%"=="DISABLED" (
  set "SPOOLER_STATUS=DISABLED"
  exit /b
)

:: Get RUNNING/STOPPED
for /f "tokens=3 delims=: " %%A in ('sc query spooler ^| findstr /i "STATE"') do (
  if /i "%%A"=="RUNNING" set "SPOOLER_STATUS=RUNNING"
  if /i "%%A"=="STOPPED" set "SPOOLER_STATUS=STOPPED"
)

:: If enabled but not running, show ENABLED
if /i "%SPOOLER_STATUS%"=="UNKNOWN" set "SPOOLER_STATUS=ENABLED"
exit /b


:: ===================== CENTER FUNCTION (aLD3N-style) =====================
:center
set "text=%~1"

:: Auto-detect console width (fallback to 50)
set "width="
for /f "tokens=2 delims=:" %%A in ('mode con ^| find "Columns"') do set "width=%%A"
set "width=%width: =%"
if not defined width set "width=50"

setlocal EnableDelayedExpansion

:: Make a copy without ANSI color sequences for correct length calculation
set "plain=!text!"
set "plain=!plain:%ESC%[92m=!"
set "plain=!plain:%ESC%[0m=!"

:: Calculate visible length (plain)
set "len=0"
for /l %%A in (0,1,500) do (
  if "!plain:~%%A,1!"=="" (
    set "len=%%A"
    goto doneLen
  )
)
:doneLen

set /a pad=(width-len)/2
if !pad! lss 0 set "pad=0"

set "spaces="
for /l %%A in (1,1,!pad!) do set "spaces=!spaces! "

:: Print ORIGINAL (colored) text, but with correct padding
echo !spaces!!text!

endlocal
exit /b