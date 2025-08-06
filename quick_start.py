#!/usr/bin/env python3
"""
快速启动脚本
同时执行爬虫和启动Web服务器
"""

import sys
import os
import threading
import time
import subprocess
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduler import CrawlerScheduler
from database import Database
from config import Config

def run_crawler():
    """在后台运行爬虫"""
    try:
        print("🕷️ 后台爬虫开始执行...")
        scheduler = CrawlerScheduler()
        scheduler.run_manual_crawl()
        print("✅ 后台爬虫执行完成")
    except Exception as e:
        print(f"❌ 后台爬虫执行失败: {e}")

def run_web_server():
    """启动Web服务器"""
    try:
        print("🌐 启动Web服务器...")
        from web_app import app
        app.run(host=Config.HOST, port=Config.PORT, debug=False)
    except Exception as e:
        print(f"❌ Web服务器启动失败: {e}")

def main():
    print("=" * 60)
    print("🚀 蓝牙技术文章聚合平台 - 快速启动")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 初始化数据库
        print("📊 初始化数据库...")
        db = Database()
        db.init_database()
        print("✅ 数据库初始化完成")
        
        # 启动后台爬虫线程
        print("🕷️ 启动后台爬虫...")
        crawler_thread = threading.Thread(target=run_crawler, daemon=True)
        crawler_thread.start()
        
        # 等待一下让爬虫开始
        time.sleep(2)
        
        print()
        print("🌐 启动Web服务器...")
        print(f"   服务器地址: http://{Config.HOST}:{Config.PORT}")
        print("   按 Ctrl+C 停止服务器")
        print()
        
        # 启动Web服务器
        run_web_server()
        
    except KeyboardInterrupt:
        print("\n\n🛑 用户停止服务")
        print("👋 再见！")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 