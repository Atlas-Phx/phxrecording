@REM ********************** Script requirements **********************
@REM - Python 3.12 or later installed and made callable from commandline (added to PATH)

@REM ********************** Usage **********************
@REM - Set the paths correctly according to their locations and save
@REM - Run command with full recording path, targeting folder, start, stop in sequence. e.g.:
@REM   phxrecshrink.bat C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213 C:\Users\xwork\Work\Phx\Data\ 1715188093 1715191693

@ECHO off
IF "%1" == "" GOTO usage
SET SOURCE_PATH=%1
IF "%2" == "" GOTO usage
SET DEST_FOLDER=%2
IF "%3" == "" GOTO usage
SET NEW_START=%3
IF "%4" == "" GOTO usage
SET NEW_STOP=%4
IF not "%5" == "" GOTO usage

@REM 1. Make the new folder with new recording ID
SET PHXRECORDING_FOLDER_PATH=%~dp0
CD %PHXRECORDING_FOLDER_PATH%
SET SOURCE_REC_ID=%SOURCE_PATH:~-23%
SET INSTRUMENT_ID=%SOURCE_REC_ID:~0,5%
SET REC_FOLDER_NAME=
FOR /f %%a IN ('python %PHXRECORDING_FOLDER_PATH%\phxrecid.py -i %INSTRUMENT_ID% -s %NEW_START%') DO @SET REC_FOLDER_NAME=%%a
ECHO New recording name: %REC_FOLDER_NAME%
SET DEST_PATH=%DEST_FOLDER%%REC_FOLDER_NAME%\
MKDIR %DEST_PATH%

@REM 2. Modify and copy new recmeta.json
ECHO Copying recmeta...
python %PHXRECORDING_FOLDER_PATH%phxrecmetamodstartstop.py -i %SOURCE_PATH%\recmeta.json -o %DEST_PATH%recmeta.json -s %NEW_START% -e %NEW_STOP%
ECHO Done.

@REM 3. Modify and copy new stats binary file
ECHO Making new stats...
FOR /f %%b IN ('python %PHXRECORDING_FOLDER_PATH%\phxrecstart.py -i %SOURCE_PATH%') DO @SET ORG_START=%%b
SET /a "START_MIN=(%NEW_START%-%ORG_START%)/60"
SET /a "STOP_MIN=(%NEW_STOP%-%ORG_START%)/60"
python %PHXRECORDING_FOLDER_PATH%phxstatsfile\phxstatsshrink.py -i %SOURCE_PATH%\stats -o %DEST_PATH%\stats -s %START_MIN% -e %STOP_MIN%
ECHO Done.

@REM 4. Copy other needed files
ECHO Copying data files....
@REM 4.1 Create needed folders
CD %SOURCE_PATH%
DEL tmp.txt
DIR *. /b /d > tmp.txt
FOR /F "tokens=*" %%c IN (tmp.txt) DO MKDIR %DEST_PATH%\%%c
@REM 4.2 Copy files
CD %PHXRECORDING_FOLDER_PATH%
DEL tmp.txt
python %PHXRECORDING_FOLDER_PATH%phxrecshrinkfilelist.py -i %SOURCE_PATH% -s %NEW_START% -e %NEW_STOP% >> tmp.txt
FOR /F "tokens=*" %%d IN (tmp.txt) DO COPY %SOURCE_PATH%\%%d %DEST_PATH%\%%d
python %PHXRECORDING_FOLDER_PATH%phxrecshrinkfinish.py -i %SOURCE_PATH% -o %DEST_PATH% -s %NEW_START% -e %NEW_STOP%
ECHO Done.
ECHO New recording created at %DEST_PATH%
ECHO off
GOTO :eof

:usage
ECHO Error in script usage. The correct usage is:
ECHO     %0 [recording folder full path] [start unix timestamp] [stop unix timestamp]
ECHO:
ECHO For example:
ECHO     %0 C:\Users\xwork\Work\Phx\Data\10766_2024-05-08-170213 C:\Users\xwork\Work\Phx\Data\ 1715188093 1715191693
GOTO :eof