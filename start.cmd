@echo off
call .env\Scripts\activate
@REM python kill_program.py
python main.py -c 0
cmd /k