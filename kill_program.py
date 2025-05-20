import psutil

tasklist = ['wechat.exe']

for proc in psutil.process_iter(['name']):
    if proc.info['name'].lower() in [task.lower() for task in tasklist]:
        try:
            proc.terminate()  # 尝试优雅地终止进程
            proc.wait(timeout=3)  # 等待进程终止，最多等待 3 秒
            print(f"已终止进程: {proc.info['name']} (PID: {proc.pid})")
        except psutil.NoSuchProcess:
            print(f"进程 {proc.info['name']} 已不存在")
        except psutil.Timeout:
            proc.kill()  # 如果超时，强制杀死进程
            print(f"已强制杀死进程: {proc.info['name']} (PID: {proc.pid})")
        except psutil.AccessDenied:
            print(f"无权限终止进程: {proc.info['name']} (PID: {proc.pid})")