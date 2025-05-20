@echo off
python -m venv .env
call .env\Scripts\activate
pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
