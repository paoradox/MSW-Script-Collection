@echo off
setlocal EnableDelayedExpansion

echo MOVE OR COPY FILES IN SUB-FOLDERS TO A SINGLE FOLDER
echo.

:: Ask user for base folder name
set /p BASENAME=ENTER BASE NAME OF THE DESTINATION FOLDER: 

:: Get locale-independent date (YYYYMMDD)
for /f %%i in ('wmic os get LocalDateTime ^| find "."') do set LDT=%%i
set "TODAY=%LDT:~0,8%"

:: Append suffix
set "DESTFOLDER=%BASENAME%-compiled-%TODAY%"
set "DESTPATH=%CD%\%DESTFOLDER%"

:: Create destination folder
if not exist "%DESTPATH%" mkdir "%DESTPATH%"

echo.
:: Ask for the main directory to search
set /p MAINDIR=ENTER FULL PATH OF MAIN DIRECTORY TO SEARCH: 

if not exist "%MAINDIR%" (
    echo INVALID DIRECTORY. SCRIPT WILL EXIT.
    goto :EOF
)

echo.
echo COPYING FILES...
echo.

:: Copy files with duplicate handling
for /R "%MAINDIR%" %%F in (*) do (
    set "DESTFILE=%DESTPATH%\%%~nxF"

    if not exist "!DESTFILE!" (
        copy "%%F" "!DESTFILE!" >nul
    ) else (
        set COUNT=1
        set "NAME=%%~nF"
        set "EXT=%%~xF"

        :CHECKDUP
        set "NEWFILE=%DESTPATH%\!NAME!_!COUNT!!EXT!"
        if exist "!NEWFILE!" (
            set /A COUNT+=1
            goto CHECKDUP
        )
        copy "%%F" "!NEWFILE!" >nul
    )
)

echo.
echo OPERATION COMPLETE.
echo FILES COPIED TO:
echo %DESTPATH%
pause
