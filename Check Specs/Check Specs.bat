@ECHO OFF 
:: This batch file details Windows, hardware, and networking configuration.
TITLE My System Info
ECHO Please wait... Checking system information.
:: Section 1: Windows information
ECHO ==========================
ECHO WINDOWS INFO
ECHO ==========================
net config workstation | findstr /c:"Full Computer name"
systeminfo | findstr /c:"OS Name"
systeminfo | findstr /c:"OS Version"
systeminfo | findstr /c:"System Type"
:: Section 2: Hardware information.
ECHO ==========================
ECHO HARDWARE INFO
ECHO ==========================
systeminfo | findstr /c:"Total Physical Memory"
wmic cpu get name
wmic diskdrive get name,model,size
wmic path win32_videocontroller get name
:: Section 3: Networking information.
ECHO ==========================
ECHO NETWORK INFO
ECHO ==========================
ipconfig | findstr IPv4
ipconfig | findstr IPv6
PAUSE