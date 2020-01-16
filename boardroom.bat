@echo on
echo %1
REM call C:\Users\DCSAdmin\Anaconda3\Scripts\activate.bat C:\Users\DCSAdmin\Anaconda3
REM C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
REM call C:\Users\reso\Anaconda3\Scripts\activate.bat C:\Users\reso\Anaconda3
REM call C:\Users\jow\Anaconda3\Scripts\activate.bat C:\Users\jow\Anaconda3

call C:\Hypeman\env\Scripts\activate.bat
python boardroom.py > logs\boardroom_log.txt
python boardroom_compose.py > logs\boardroom_compose_log.txt