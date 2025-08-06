#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝牙技术文章聚合平台主程序
"""

import os
import sys
import logging
import threading
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduler import CrawlerScheduler
from web_app import app
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bluetooth_aggregator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def start_scheduler():
    """启动定时任务调度器"""
    try:
        scheduler = CrawlerScheduler()
        scheduler_thread = scheduler.start_scheduler()
        logger.info("定时任务调度器启动成功")
        return scheduler, scheduler_thread
    except Exception as e:
        logger.error(f"启动定时任务调度器失败: {e}")
        return None, None

def start_web_server():
    """启动Web服务器"""
    try:
        logger.info(f"启动Web服务器: http://{Config.HOST}:{Config.PORT}")
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG,
            use_reloader=False  # 避免重复启动
        )
    except Exception as e:
        logger.error(f"启动Web服务器失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("蓝牙技术文章聚合平台")
    print("=" * 60)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"配置信息:")
    print(f"  - 数据库: {Config.DATABASE_PATH}")
    print(f"  - 定时任务: 每天 {Config.SCHEDULE_TIME}")
    print(f"  - Web服务器: {Config.HOST}:{Config.PORT}")
    print(f"  - 数据保留: {Config.DATA_RETENTION_DAYS} 天")
    print("=" * 60)
    
    # 检查OpenAI API密钥
    if not Config.OPENAI_API_KEY:
        logger.warning("未设置OpenAI API密钥，AI总结功能将不可用")
        print("警告: 未设置OpenAI API密钥，AI总结功能将不可用")
    
    # 启动定时任务调度器
    scheduler, scheduler_thread = start_scheduler()
    if not scheduler:
        logger.error("无法启动定时任务调度器，程序退出")
        return
    
    # 启动Web服务器（在新线程中）
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    try:
        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭程序...")
        if scheduler:
            scheduler.stop_scheduler()
        logger.info("程序已关闭")
        print("程序已关闭")

if __name__ == "__main__":
    main() 