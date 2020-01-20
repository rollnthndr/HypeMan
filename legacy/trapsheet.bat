@echo off
echo %1
REM call C:\Users\DCSAdmin\Anaconda3\Scripts\activate.bat C:\Users\DCSAdmin\Anaconda3
REM C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
REM python gsheet_upload.py %1

call C:\Hypeman\env\Scripts\activate.bat
python trapsheet.py > logs\trapsheet.log