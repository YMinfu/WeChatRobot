#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import os
import signal
import time
from argparse import ArgumentParser

from wcferry import Wcf

from configuration import Config
from constants import ChatType
from robot import Robot, __version__


def main(chat_type: int):
    config = Config()
    wcf = Wcf(debug=True)

    def handler(sig, frame):
        wcf.cleanup()  # 退出前清理环境
        exit(0)

    # 注册 SIGINT 和 SIGTERM 信号处理
    signal.signal(signal.SIGINT, handler)  # 处理 Ctrl+C
    signal.signal(signal.SIGTERM, handler)  # 处理终止信号

    # 定义守护进程的监控逻辑
    def daemon_monitor(parent_pid: int):
        print(f"Daemon process started, monitoring parent PID: {parent_pid}")
        while True:
            # 检查主进程是否存活
            if not is_process_alive(parent_pid):
                print("Main process terminated, performing cleanup")
                wcf.cleanup()  # 退出前清理环境
                break
            time.sleep(1)  # 每秒检查一次
        print("Daemon process exiting")

    # 检查进程是否存活（跨平台实现）
    def is_process_alive(pid: int) -> bool:
        try:
            if os.name == 'posix':  # Linux/Unix
                os.kill(pid, 0)  # 发送信号 0 检查进程存在
            else:  # Windows
                import psutil
                return psutil.pid_exists(pid)
            return True
        except (OSError, psutil.NoSuchProcess):
            return False

    # 创建守护进程
    daemon_process = multiprocessing.Process(
        target=daemon_monitor,
        args=(os.getpid(),),  # 传递主进程 PID
        daemon=True  # 设置为守护进程
    )
    daemon_process.start()

    # 程序主逻辑（例如事件循环）
    try:
        robot = Robot(config, wcf, chat_type)
        robot.LOG.info(f"WeChatRobot【{__version__}】成功启动···")

        # 接收消息
        # robot.enableRecvMsg()     # 可能会丢消息？
        robot.enableReceivingMsg()  # 加队列

        # 机器人启动发送测试消息
        # robot.sendTextMsg("机器人启动成功！\n绘画功能使用说明：\n• 智谱绘画：牛智谱[描述]\n• 阿里绘画：牛阿里[描述]\n• 谷歌绘画：牛谷歌[描述]\n实例：\n牛阿里 画一张家乡\n@XX 牛阿里 画一张家乡\n聊天时直接发送消息即可", "filehelper")
        # 每天 7 点发送天气预报
        # robot.onEveryTime("07:00", robot.weatherReport)
        # 每天 7:30 发送新闻
        # robot.onEveryTime("07:30", robot.newsReport)
        # 每天 16:30 提醒发日报周报月报
        # robot.onEveryTime("16:30", ReportReminder.remind, robot=robot)

        # 让机器人一直跑
        robot.keepRunningAndBlockProcess()

    except KeyboardInterrupt:
        handler(signal.SIGINT, None)  # 手动调用清理


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-c', type=int, default=0, help=f'选择模型参数序号: {ChatType.help_hint()}')
    args = parser.parse_args().c
    main(args)
