#!/usr/bin/env python3
"""
手动执行爬虫任务
立即开始检索文章
"""

import sys
import os
import logging
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scheduler import CrawlerScheduler
from database import Database
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('manual_crawler.log'),
        logging.StreamHandler()
    ]
)

def main():
    print("=" * 60)
    print("🚀 蓝牙技术文章检索系统")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 初始化数据库
        print("📊 初始化数据库...")
        db = Database()
        db.init_database()
        print("✅ 数据库初始化完成")
        
        # 创建调度器
        print("⚙️ 创建爬虫调度器...")
        scheduler = CrawlerScheduler()
        print("✅ 调度器创建完成")
        
        # 执行爬虫任务
        print("🕷️ 开始执行爬虫任务...")
        print("📰 正在检索新闻网站...")
        print("💻 正在检索技术博客...")
        print("📚 正在检索学术论文...")
        print("📋 正在检索专利信息...")
        
        # 执行爬虫
        scheduler.run_manual_crawl()
        
        print()
        print("✅ 爬虫任务执行完成！")
        
        # 显示统计信息
        print("\n📈 检索结果统计:")
        recent_articles = db.get_recent_articles(days=1, limit=1000)
        print(f"   今日新增文章: {len(recent_articles)} 篇")
        
        if recent_articles:
            # 按来源类型统计
            source_counts = {}
            for article in recent_articles:
                source_type = article.get('source_type', 'unknown')
                source_counts[source_type] = source_counts.get(source_type, 0) + 1
            
            print("   来源分布:")
            for source_type, count in source_counts.items():
                print(f"     - {source_type}: {count} 篇")
        
        print()
        print("🌐 你可以通过以下方式查看结果:")
        print("   1. 启动Web服务器: python main.py")
        print("   2. 访问: http://localhost:5000")
        print("   3. 查看文章列表: http://localhost:5000/articles")
        
    except Exception as e:
        print(f"❌ 执行过程中出现错误: {e}")
        logging.error(f"爬虫执行失败: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("🎉 任务完成！")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main()) 