@echo off
title AI Website + API Restriction Manager (Final v7)
color 0A

:: =========================================================
:: ADMIN CHECK
:: =========================================================
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ==========================================
    echo Administrator required. Restarting...
    echo ==========================================
    echo.

    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit
)

:: =========================================================
:: PATHS
:: =========================================================
set "HOSTS=%SystemRoot%\System32\drivers\etc\hosts"
set "TEMPFILE=%temp%\hosts_temp.txt"

:: =========================================================
:: STARTUP INFO
:: =========================================================
cls
echo ==========================================
echo SYSTEM HOSTS FILE LOCATION
echo ==========================================
echo %HOSTS%
echo ==========================================
echo.
pause

:: =========================================================
:: MENU
:: =========================================================
:MENU
cls
echo ==========================================
echo   AI WEBSITE + API BLOCK MANAGER
echo ==========================================
echo.
echo HOST FILE:
echo %HOSTS%
echo.
echo [Y] Add Restrictions
echo [N] Remove Restrictions
echo [X] Exit
echo.

set /p CHOICE=Select option: 

if /I "%CHOICE%"=="Y" goto ADD
if /I "%CHOICE%"=="N" goto REMOVE
if /I "%CHOICE%"=="X" goto END

goto MENU

:: =========================================================
:: ADD BLOCKS
:: =========================================================
:ADD
cls
echo ==========================================
echo MODIFYING HOST FILE:
echo %HOSTS%
echo ==========================================
echo.
echo Adding AI domains + API endpoints...
echo.

:: Add header once
findstr /I /C:"# AI BLOCK LIST" "%HOSTS%" >nul
if %errorLevel% neq 0 (
    echo.>>"%HOSTS%"
    echo # AI BLOCK LIST>>"%HOSTS%"
)

:: AI websites
call :ADDLINE chatgpt.com
call :ADDLINE openai.com
call :ADDLINE claude.ai
call :ADDLINE gemini.google.com
call :ADDLINE notebooklm.google.com
call :ADDLINE perplexity.ai
call :ADDLINE copilot.microsoft.com
call :ADDLINE grok.com
call :ADDLINE poe.com
call :ADDLINE character.ai

:: AI APIs
call :ADDLINE api.openai.com
call :ADDLINE platform.openai.com
call :ADDLINE api.anthropic.com
call :ADDLINE generativelanguage.googleapis.com
call :ADDLINE api.perplexity.ai
call :ADDLINE api.deepseek.com
call :ADDLINE api.mistral.ai
call :ADDLINE api.replicate.com

ipconfig /flushdns >nul

echo.
echo ==========================================
echo HOST FILE UPDATED:
echo %HOSTS%
echo ==========================================
echo AI BLOCKS SUCCESSFULLY ADDED
echo ==========================================
pause
goto MENU

:: =========================================================
:: REMOVE BLOCKS (FULL CLEAN FIXED)
:: =========================================================
:REMOVE
cls
echo ==========================================
echo MODIFYING HOST FILE:
echo %HOSTS%
echo ==========================================
echo.
echo Removing ALL AI entries + header... PLEASE WAIT...
echo.

(
for /f "delims=" %%A in (%HOSTS%) do (

    echo %%A | findstr /I ^
    "chatgpt.com openai.com claude.ai gemini.google.com notebooklm.google.com perplexity.ai copilot.microsoft.com grok.com poe.com character.ai api.openai.com platform.openai.com api.anthropic.com generativelanguage.googleapis.com api.perplexity.ai api.deepseek.com api.mistral.ai api.replicate.com" >nul

    if errorlevel 1 (
        echo %%A | findstr /I "# AI BLOCK LIST" >nul
        if errorlevel 1 (
            echo %%A
        )
    )
)
) > "%TEMPFILE%"

copy /Y "%TEMPFILE%" "%HOSTS%" >nul
del "%TEMPFILE%"

ipconfig /flushdns >nul

echo.
echo ==========================================
echo HOST FILE UPDATED:
echo %HOSTS%
echo ==========================================
echo ALL AI BLOCKS + HEADER REMOVED
echo ==========================================
pause
goto MENU

:: =========================================================
:: ADD FUNCTION (NO DUPLICATES)
:: =========================================================
:ADDLINE
findstr /I /C:"127.0.0.1 %~1" "%HOSTS%" >nul
if %errorLevel% neq 0 (
    echo 127.0.0.1 %~1>>"%HOSTS%"
    echo Added: %~1
) else (
    echo Already exists: %~1
)
exit /b

:: =========================================================
:: EXIT
:: =========================================================
:END
echo.
echo ==========================================
echo HOST FILE LOCATION:
echo %HOSTS%
echo ==========================================
echo Exiting program...
pause
exit