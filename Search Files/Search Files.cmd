@echo off
setlocal EnableDelayedExpansion

echo =====================================================
echo PLACE THIS BATCH FILE AND LIST.TXT IN THE DIRECTORY
echo WHERE YOU WANT THE FILE SEARCH TO RUN.
echo =====================================================
echo.

set /p CONFIRM=DO YOU WANT TO CONTINUE? (Y/N): 

if /I not "%CONFIRM%"=="Y" (
    echo OPERATION CANCELLED.
    goto :EOF
)

echo.
echo RUNNING FILE SEARCH...
echo.

rem Read file names from file list and assemble a long string with this format:
rem "filename1.ext*" "filename2.ext*" ...
set "fileList="
for /F "delims=" %%a in (list.txt) do set fileList=!fileList! "%%a*"

rem Search the files from current directory downwards
(for /R %%a in (%fileList%) do echo %%a) > results.txt

echo.
echo SEARCH COMPLETE. RESULTS SAVED TO RESULTS.TXT
pause
