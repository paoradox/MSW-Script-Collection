@echo off
setlocal EnableDelayedExpansion
color 0A
title Advanced Printer Management Tool
 
:MENU
cls
echo ============================================================
echo          ADVANCED PRINTER MANAGEMENT TOOL
echo ============================================================
echo.
echo  --- BASIC OPTIONS ---
echo   [1]  View Installed Printers
echo   [2]  Open Printer Settings
echo   [3]  Restart Print Spooler
echo   [4]  Clear Print Queue
echo   [5]  Open Devices and Printers
echo   [6]  Print Test Page
echo   [7]  Show Printer Status
echo   [8]  Open Print Management
echo   [9]  Open Scanner Settings
echo   [10] Full Printer Repair
echo.
echo  --- ADVANCED OPTIONS ---
echo   [11] Set Default Printer
echo   [12] Export Printer List to File
echo   [13] View Installed Printer Drivers
echo   [14] Remove a Printer
echo   [15] Add a Network Printer (by IP)
echo   [16] Check Spooler Service Status
echo   [17] Force Kill All Print Jobs (Nuclear Clear)
echo   [18] Backup Printer Configuration
echo   [19] View Printer Event Logs
echo   [20] Run Windows Printer Troubleshooter
echo   [21] Enable a Printer
echo   [22] Disable a Printer
echo   [23] Ping Printer / Network Printer Diagnostics
echo   [24] View Printer Driver Details
echo   [25] Reinstall Print Spooler Service
echo   [26] Open Printer Ports Settings
echo   [27] View Shared Printers on Network
echo   [28] Toggle Printer Sharing
echo.
echo   [0]  Exit
echo.
echo ============================================================
set /p choice="  Enter your choice: "
 
if "%choice%"=="1"  goto VIEW_PRINTERS
if "%choice%"=="2"  goto OPEN_SETTINGS
if "%choice%"=="3"  goto RESTART_SPOOLER
if "%choice%"=="4"  goto CLEAR_QUEUE
if "%choice%"=="5"  goto DEVICES_PRINTERS
if "%choice%"=="6"  goto TEST_PAGE
if "%choice%"=="7"  goto PRINTER_STATUS
if "%choice%"=="8"  goto PRINT_MANAGEMENT
if "%choice%"=="9"  goto SCANNER_SETTINGS
if "%choice%"=="10" goto FULL_REPAIR
if "%choice%"=="11" goto SET_DEFAULT
if "%choice%"=="12" goto EXPORT_LIST
if "%choice%"=="13" goto VIEW_DRIVERS
if "%choice%"=="14" goto REMOVE_PRINTER
if "%choice%"=="15" goto ADD_NETWORK
if "%choice%"=="16" goto SPOOLER_STATUS
if "%choice%"=="17" goto NUCLEAR_CLEAR
if "%choice%"=="18" goto BACKUP_CONFIG
if "%choice%"=="19" goto EVENT_LOGS
if "%choice%"=="20" goto TROUBLESHOOTER
if "%choice%"=="21" goto ENABLE_PRINTER
if "%choice%"=="22" goto DISABLE_PRINTER
if "%choice%"=="23" goto PING_PRINTER
if "%choice%"=="24" goto DRIVER_DETAILS
if "%choice%"=="25" goto REINSTALL_SPOOLER
if "%choice%"=="26" goto PRINTER_PORTS
if "%choice%"=="27" goto NETWORK_PRINTERS
if "%choice%"=="28" goto TOGGLE_SHARING
if "%choice%"=="0"  goto EXIT
echo  Invalid choice. Try again.
pause
goto MENU
 
:: ============================================================
:: BASIC OPTIONS
:: ============================================================
 
:VIEW_PRINTERS
cls
echo ============================================================
echo  INSTALLED PRINTERS
echo ============================================================
wmic printer get name,default,status,portname | more
echo.
pause
goto MENU
 
:OPEN_SETTINGS
cls
echo  Opening Printer Settings...
start ms-settings:printers
pause
goto MENU
 
:RESTART_SPOOLER
cls
echo ============================================================
echo  RESTARTING PRINT SPOOLER
echo ============================================================
echo  Stopping Print Spooler...
net stop spooler
echo  Starting Print Spooler...
net start spooler
echo  Done! Print Spooler restarted successfully.
pause
goto MENU
 
:CLEAR_QUEUE
cls
echo ============================================================
echo  CLEARING PRINT QUEUE
echo ============================================================
echo  Stopping spooler...
net stop spooler >nul 2>&1
echo  Deleting queued jobs...
del /Q /F /S "%systemroot%\System32\spool\PRINTERS\*.*" >nul 2>&1
echo  Starting spooler...
net start spooler >nul 2>&1
echo  Print queue cleared successfully!
pause
goto MENU
 
:DEVICES_PRINTERS
cls
echo  Opening Devices and Printers...
start control printers
pause
goto MENU
 
:TEST_PAGE
cls
echo ============================================================
echo  PRINT TEST PAGE
echo ============================================================
echo  Available printers:
wmic printer get name
echo.
set /p pname="  Enter exact printer name: "
wmic printer where name="%pname%" call PrintTestPage
echo  Test page sent to: %pname%
pause
goto MENU
 
:PRINTER_STATUS
cls
echo ============================================================
echo  PRINTER STATUS
echo ============================================================
wmic printer get name,status,default,WorkOffline,PrinterState | more
echo.
pause
goto MENU
 
:PRINT_MANAGEMENT
cls
echo  Opening Print Management...
start printmanagement.msc
pause
goto MENU
 
:SCANNER_SETTINGS
cls
echo  Opening Scanner Settings...
start ms-settings:printers
start wiaacmgr.exe -SelectDevice
pause
goto MENU
 
:FULL_REPAIR
cls
echo ============================================================
echo  FULL PRINTER REPAIR
echo ============================================================
echo  [Step 1/5] Stopping Print Spooler...
net stop spooler >nul 2>&1
echo  [Step 2/5] Clearing print queue...
del /Q /F /S "%systemroot%\System32\spool\PRINTERS\*.*" >nul 2>&1
echo  [Step 3/5] Resetting spooler dependencies...
sc config spooler depend= RPCSS >nul 2>&1
echo  [Step 4/5] Starting Print Spooler...
net start spooler >nul 2>&1
echo  [Step 5/5] Running system file check (sfc /scannow)...
sfc /scannow
echo.
echo  Full printer repair complete!
pause
goto MENU
 
:: ============================================================
:: ADVANCED OPTIONS
:: ============================================================
 
:SET_DEFAULT
cls
echo ============================================================
echo  SET DEFAULT PRINTER
echo ============================================================
echo  Available printers:
wmic printer get name
echo.
set /p pname="  Enter exact printer name to set as default: "
wmic printer where name="%pname%" call SetDefaultPrinter
echo  Default printer set to: %pname%
pause
goto MENU
 
:EXPORT_LIST
cls
echo ============================================================
echo  EXPORT PRINTER LIST
echo ============================================================
set outfile=%USERPROFILE%\Desktop\PrinterList.txt
echo Printer List - %date% %time% > "%outfile%"
echo ============================================================ >> "%outfile%"
wmic printer get name,portname,status,default,driverName >> "%outfile%"
echo.
echo  Exported to: %outfile%
pause
goto MENU
 
:VIEW_DRIVERS
cls
echo ============================================================
echo  INSTALLED PRINTER DRIVERS
echo ============================================================
wmic printdriver get name,version,supportedplatform | more
echo.
pause
goto MENU
 
:REMOVE_PRINTER
cls
echo ============================================================
echo  REMOVE A PRINTER
echo ============================================================
echo  Available printers:
wmic printer get name
echo.
set /p pname="  Enter exact printer name to remove: "
echo  Are you sure you want to remove: %pname%?
set /p confirm="  Type YES to confirm: "
if /i "%confirm%"=="YES" (
    wmic printer where name="%pname%" delete
    echo  Printer removed successfully.
) else (
    echo  Cancelled.
)
pause
goto MENU
 
:ADD_NETWORK
cls
echo ============================================================
echo  ADD NETWORK PRINTER BY IP
echo ============================================================
set /p ipaddr="  Enter printer IP address (e.g. 192.168.1.100): "
set /p pname="  Enter a name for this printer: "
set portname=IP_%ipaddr%
echo  Adding TCP/IP port...
cscript %systemroot%\System32\Printing_Admin_Scripts\en-US\prnport.vbs -a -r %portname% -h %ipaddr% -o raw -n 9100 >nul 2>&1
echo  Port added. Opening Add Printer wizard...
rundll32 printui.dll,PrintUIEntry /in /n "\\%ipaddr%"
echo  If wizard didn't open, please add manually via Devices and Printers.
pause
goto MENU
 
:SPOOLER_STATUS
cls
echo ============================================================
echo  SPOOLER SERVICE STATUS
echo ============================================================
sc query spooler
echo.
echo  Spooler startup type:
sc qc spooler | findstr START_TYPE
echo.
pause
goto MENU
 
:NUCLEAR_CLEAR
cls
echo ============================================================
echo  NUCLEAR PRINT QUEUE CLEAR
echo ============================================================
echo  WARNING: This will terminate ALL print jobs and restart the spooler.
set /p confirm="  Type YES to confirm: "
if /i "%confirm%"=="YES" (
    net stop spooler >nul 2>&1
    taskkill /F /IM spoolsv.exe >nul 2>&1
    del /Q /F /S "%systemroot%\System32\spool\PRINTERS\*.*" >nul 2>&1
    net start spooler >nul 2>&1
    echo  All print jobs forcefully cleared and spooler restarted!
) else (
    echo  Cancelled.
)
pause
goto MENU
 
:BACKUP_CONFIG
cls
echo ============================================================
echo  BACKUP PRINTER CONFIGURATION
echo ============================================================
set backupfile=%USERPROFILE%\Desktop\PrinterBackup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt
echo Printer Backup - %date% %time% > "%backupfile%"
echo. >> "%backupfile%"
echo == PRINTERS == >> "%backupfile%"
wmic printer get name,portname,driverName,status,default,shared >> "%backupfile%"
echo. >> "%backupfile%"
echo == DRIVERS == >> "%backupfile%"
wmic printdriver get name,version >> "%backupfile%"
echo. >> "%backupfile%"
echo == PORTS == >> "%backupfile%"
wmic printerport get name,description,portnumber >> "%backupfile%"
echo  Backup saved to: %backupfile%
pause
goto MENU
 
:EVENT_LOGS
cls
echo ============================================================
echo  PRINTER EVENT LOGS (Last 20 Entries)
echo ============================================================
wevtutil qe "Microsoft-Windows-PrintService/Operational" /c:20 /rd:true /f:text 2>nul | more
if errorlevel 1 (
    echo  Enabling PrintService log and retrying...
    wevtutil sl "Microsoft-Windows-PrintService/Operational" /e:true
    wevtutil qe "Microsoft-Windows-PrintService/Operational" /c:20 /rd:true /f:text | more
)
pause
goto MENU
 
:TROUBLESHOOTER
cls
echo  Launching Windows Printer Troubleshooter...
msdt.exe /id PrinterDiagnostic
pause
goto MENU
 
:ENABLE_PRINTER
cls
echo ============================================================
echo  ENABLE A PRINTER
echo ============================================================
echo  Available printers:
wmic printer get name,status
echo.
set /p pname="  Enter exact printer name to enable: "
wmic printer where name="%pname%" set WorkOffline=FALSE
echo  Printer enabled: %pname%
pause
goto MENU
 
:DISABLE_PRINTER
cls
echo ============================================================
echo  DISABLE A PRINTER
echo ============================================================
echo  Available printers:
wmic printer get name,status
echo.
set /p pname="  Enter exact printer name to disable: "
wmic printer where name="%pname%" set WorkOffline=TRUE
echo  Printer disabled (set offline): %pname%
pause
goto MENU
 
:PING_PRINTER
cls
echo ============================================================
echo  NETWORK PRINTER DIAGNOSTICS
echo ============================================================
set /p ipaddr="  Enter printer IP address: "
echo.
echo  --- Ping Test ---
ping -n 4 %ipaddr%
echo.
echo  --- Traceroute ---
tracert -d -h 5 %ipaddr%
echo.
echo  --- Port 9100 (RAW Print) Check ---
powershell -command "Test-NetConnection -ComputerName %ipaddr% -Port 9100 | Select-Object ComputerName,TcpTestSucceeded"
echo.
echo  --- Port 80 (Web UI) Check ---
powershell -command "Test-NetConnection -ComputerName %ipaddr% -Port 80 | Select-Object ComputerName,TcpTestSucceeded"
pause
goto MENU
 
:DRIVER_DETAILS
cls
echo ============================================================
echo  PRINTER DRIVER DETAILS
echo ============================================================
wmic printdriver get name,driverPath,version,supportedplatform,monitorName | more
echo.
pause
goto MENU
 
:REINSTALL_SPOOLER
cls
echo ============================================================
echo  REINSTALL PRINT SPOOLER SERVICE
echo ============================================================
echo  WARNING: This will stop, unregister, and re-register the spooler.
set /p confirm="  Type YES to confirm: "
if /i "%confirm%"=="YES" (
    echo  Stopping spooler...
    net stop spooler >nul 2>&1
    echo  Unregistering spooler DLL...
    regsvr32 /s /u "%systemroot%\System32\spoolsv.exe" >nul 2>&1
    echo  Clearing spool folder...
    del /Q /F /S "%systemroot%\System32\spool\PRINTERS\*.*" >nul 2>&1
    echo  Restoring default service config...
    sc config spooler start= auto >nul 2>&1
    sc config spooler depend= RPCSS >nul 2>&1
    echo  Starting spooler...
    net start spooler >nul 2>&1
    echo  Done! Spooler reinstalled/restored.
) else (
    echo  Cancelled.
)
pause
goto MENU
 
:PRINTER_PORTS
cls
echo ============================================================
echo  PRINTER PORTS
echo ============================================================
echo  -- Active Printer Ports --
wmic printerport get name,description,portnumber,type | more
echo.
echo  Opening Printer Ports in Print Management...
start printmanagement.msc
pause
goto MENU
 
:NETWORK_PRINTERS
cls
echo ============================================================
echo  SHARED PRINTERS ON NETWORK
echo ============================================================
echo  Scanning for shared printers (this may take a moment)...
net view 2>nul | findstr /V "^$" | more
echo.
echo  -- Mapped Network Printers --
wmic printer where "network=true" get name,portname,status | more
echo.
pause
goto MENU
 
:TOGGLE_SHARING
cls
echo ============================================================
echo  TOGGLE PRINTER SHARING
echo ============================================================
echo  Available printers:
wmic printer get name,shared
echo.
set /p pname="  Enter exact printer name: "
set /p sharechoice="  Share this printer? (YES/NO): "
if /i "%sharechoice%"=="YES" (
    set /p sharename="  Enter share name (no spaces): "
    wmic printer where name="%pname%" set Shared=TRUE,ShareName="%sharename%"
    echo  Printer shared as: %sharename%
) else (
    wmic printer where name="%pname%" set Shared=FALSE
    echo  Printer sharing disabled for: %pname%
)
pause
goto MENU
 
:EXIT
cls
echo.
echo  Goodbye! Printer Manager closed.
echo.
timeout /t 2 >nul
exit /b 0