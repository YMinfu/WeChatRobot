@echo off
call .env\Scripts\activate
python kill_wechat.py
python main.py -c 0
cmd /k