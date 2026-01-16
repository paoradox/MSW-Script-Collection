::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJHuF90klOFtAQwuOfCOIA7I/5OH+4f7H6Q0tVeE0fZvIk4iHI+9d40brFQ==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJHuF90klOFtAQwuOfDnqVOZcoNr+6MmLq0gTQKJ0OL/a2b+LNPNToQXNUbMA/1sTpNkZAlZafxGgex8gpmFOoW2BMsqVsl2xGBvH41M1ew==
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
TITLE REGCLIENT, PACKETS AND IDEMIA BACKUP TOOL
ECHO COMPUTER : %computername%
ECHO DATE : %date%

Set mydate=%DATE:~-4%%DATE:~-7,2%%DATE:~-10,2%
Set DirName=%computername% Regclient_1.4.3_Updated_Validation ^(%mydate%^)
Set DirName2=%computername% Reg-client.1.4.4_012122 ^(%mydate%^)
Set DirName3=%computername% Regclient-checkbox-idemia1.1.7 ^(%mydate%^)

ECHO,
ECHO ====================NOTICE======================
ECHO MAKE SURE YOU TRIED UPLOADING ALL YOUR PACKETS!
ECHO,
ECHO PLEASE CLOSE THE REGCLIENT UPON USING THIS TOOL!
ECHO,
ECHO THIS WILL BACKUP THE FIRST MATCHED FOLDER FOUND.
ECHO,
ECHO PLEASE COORDINATE WITH YOUR I.S.A UPON USE!
ECHO ====================NOTICE======================
ECHO,
ECHO,

set /p answer=@%time% DO YOU INTEND TO BACKUP TODAY ^(Y/N^)? 
ECHO @%time% ANSWER : %answer%
ECHO,
IF %answer%==Y GOTO backup
IF %answer%==y GOTO backup
IF %answer%==N GOTO END
IF %answer%==n GOTO END

ECHO,
ECHO @%time% INVALID INPUT
ECHO,
GOTO END

:backup
ECHO @%time% DEFAULT REGCLIENT PATH FINDER :
IF exist C:\PhilSys_20210713\Regclient_1.4.3_Updated_Validation\* (
  ECHO C:\PhilSys_20210713\Regclient_1.4.3_Updated_Validation Exists : True
) ELSE ( ECHO C:\PhilSys_20210713\Regclient_1.4.3_Updated_Validation Exists : False )
IF exist C:\PhilSys_20210713\Reg-client.1.4.4_012122\* (
  ECHO C:\PhilSys_20210713\Reg-client.1.4.4_012122 Exists : True
) ELSE ( ECHO C:\PhilSys_20210713\Reg-client.1.4.4_012122 Exists : False )
IF exist C:\PhilSys_20220121\Reg-client.1.4.4_012122\* (
  ECHO C:\PhilSys_20220121\Reg-client.1.4.4_012122 Exists : True
) ELSE ( ECHO C:\PhilSys_20220121\Reg-client.1.4.4_012122 Exists : False )
IF exist C:\PhilSys_20230119\Regclient-checkbox-idemia1.1.7\* (
  ECHO C:\PhilSys_20230119\Regclient-checkbox-idemia1.1.7 Exists : True
) ELSE ( ECHO C:\PhilSys_20230119\Regclient-checkbox-idemia1.1.7 Exists : False )

ECHO,
ECHO @%time% DEFAULT BIOSDK PATH FINDER :
IF exist C:\PHILSYS_IDEMIA_SDK\* (
  ECHO C:\PHILSYS_IDEMIA_SDK Exists : True
) ELSE ( ECHO C:\PHILSYS_IDEMIA_SDK Exists : False )


ECHO,
ECHO @%time% REGCLIENT BACKUP INSTANTIATION :
IF exist C:\PhilSys_20210713\Regclient_1.4.3_Updated_Validation\* (
    XCOPY "C:\PhilSys_20210713\Regclient_1.4.3_Updated_Validation" "D:\%DirName3%\" /s /e /w
	ECHO,
	ECHO @%time% PHILSYS_IDEMIA BACKUP INSTANTIATION :
	XCOPY "C:\PHILSYS_IDEMIA_SDK" "D:\%DirName%\PHILSYS_IDEMIA_SDK\" /s /e /w
    ECHO,
    ECHO @%time% BACKUP SUMMARY :
    ECHO FOLDER NAME = "%DirName%"
    ECHO NEW PATH = "D:\%DirName%\"
) ELSE (
  IF exist C:\PhilSys_20210713\Reg-client.1.4.4_012122\* (
      XCOPY "C:\PhilSys_20210713\Reg-client.1.4.4_012122" "D:\%DirName3%\" /s /e /w
	  ECHO,
	  ECHO @%time% PHILSYS_IDEMIA BACKUP INSTANTIATION :
	  XCOPY "C:\PHILSYS_IDEMIA_SDK" "D:\%DirName2%\PHILSYS_IDEMIA_SDK\" /s /e /w
      ECHO,
      ECHO @%time% BACKUP SUMMARY :
      ECHO FOLDER NAME = "%DirName2%"
      ECHO NEW PATH = "D:\%DirName2%\"
    ) ELSE (
        IF exist C:\PhilSys_20220121\Reg-client.1.4.4_012122\* (
            XCOPY "C:\PhilSys_20220121\Reg-client.1.4.4_012122" "D:\%DirName2%\" /s /e /w
			ECHO,
			ECHO @%time% PHILSYS_IDEMIA BACKUP INSTANTIATION :
			XCOPY "C:\PHILSYS_IDEMIA_SDK" "D:\%DirName2%\PHILSYS_IDEMIA_SDK\" /s /e /w
            ECHO,
            ECHO @%time% BACKUP SUMMARY :
	    ECHO FOLDER NAME = "%DirName2%"
    	    ECHO NEW PATH = "D:\%DirName2%\"
    	) ELSE (
			IF exist C:\PhilSys_20230119\Regclient-checkbox-idemia1.1.7\* (
            XCOPY "C:\PhilSys_20230119\Regclient-checkbox-idemia1.1.7" "D:\%DirName3%\" /s /e /w
			ECHO,
			ECHO @%time% PHILSYS_IDEMIA BACKUP INSTANTIATION :
			XCOPY "C:\PHILSYS_IDEMIA_SDK" "D:\%DirName3%\PHILSYS_IDEMIA_SDK\" /s /e /w
            ECHO,
            ECHO @%time% BACKUP SUMMARY :
			ECHO FOLDER NAME = "%DirName3%"
    	    ECHO NEW PATH = "D:\%DirName3%\"
			) ELSE (
				ECHO,
				ECHO NO DEFAULT DIRECTORIES FOUND TO BACKUP.
				ECHO REGCLIENT, PACKETS OR IDEMIA MAY HAVE BEEN STORED SOMEWHERE ELSE.
				ECHO PLEASE DO NOT RENAME ORIGINAL FOLDERS IN C:\
	)
    )
	)
)

ECHO,
PAUSE

:END
ECHO,
ECHO @%time% USER EXITING

ECHO,
PAUSE
