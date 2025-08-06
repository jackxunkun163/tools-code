#!/usr/bin/env python3
"""
测试爬虫脚本
快速测试爬虫功能，只爬取少量文章
"""

import sys
import os
import logging
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawlers.news_crawler import NewsCrawler
from crawlers.tech_crawler import TechCrawler
from crawlers.academic_crawler import AcademicCrawler
from crawlers.manufacturer_crawler import ManufacturerCrawler
from database import Database
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_news_crawler():
    """测试新闻爬虫"""
    print("📰 测试新闻爬虫...")
    try:
        crawler = NewsCrawler()
        articles = crawler.crawl_news_sites(limit=5)  # 只爬取5篇文章
        print(f"✅ 新闻爬虫成功，获取 {len(articles)} 篇文章")
        return articles
    except Exception as e:
        print(f"❌ 新闻爬虫失败: {e}")
        return []

def test_tech_crawler():
    """测试技术文章爬虫"""
    print("💻 测试技术文章爬虫...")
    try:
        crawler = TechCrawler()
        articles = crawler.crawl_tech_sites(limit=3)  # 只爬取3篇文章
        print(f"✅ 技术文章爬虫成功，获取 {len(articles)} 篇文章")
        return articles
    except Exception as e:
        print(f"❌ 技术文章爬虫失败: {e}")
        return []

def test_academic_crawler():
    """测试学术论文爬虫"""
    print("📚 测试学术论文爬虫...")
    try:
        crawler = AcademicCrawler()
        articles = crawler.crawl_academic_sites(limit=2)  # 只爬取2篇文章
        print(f"✅ 学术论文爬虫成功，获取 {len(articles)} 篇文章")
        return articles
    except Exception as e:
        print(f"❌ 学术论文爬虫失败: {e}")
        return []

def test_manufacturer_crawler():
    """测试手机厂商爬虫"""
    print("📱 测试手机厂商爬虫...")
    try:
        crawler = ManufacturerCrawler()
        articles = crawler.crawl_manufacturer_sites(limit=5)  # 只爬取5篇文章
        print(f"✅ 手机厂商爬虫成功，获取 {len(articles)} 篇文章")
        return articles
    except Exception as e:
        print(f"❌ 手机厂商爬虫失败: {e}")
        return []

def test_tech_company_crawler():
    """测试技术公司爬虫"""
    print("🏢 测试技术公司爬虫...")
    try:
        crawler = ManufacturerCrawler()
        articles = crawler.crawl_tech_company_sites(limit=5)  # 只爬取5篇文章
        print(f"✅ 技术公司爬虫成功，获取 {len(articles)} 篇文章")
        return articles
    except Exception as e:
        print(f"❌ 技术公司爬虫失败: {e}")
        return []

def main():
    print("=" * 60)
    print("🧪 蓝牙技术文章爬虫测试")
    print("=" * 60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 初始化数据库
        print("📊 初始化数据库...")
        db = Database()
        db.init_database()
        print("✅ 数据库初始化完成")
        
        all_articles = []
        
        # 测试各种爬虫
        print("\n🕷️ 开始测试爬虫...")
        
        # 测试新闻爬虫
        news_articles = test_news_crawler()
        all_articles.extend(news_articles)
        
        # 测试技术文章爬虫
        tech_articles = test_tech_crawler()
        all_articles.extend(tech_articles)
        
        # 测试学术论文爬虫
        academic_articles = test_academic_crawler()
        all_articles.extend(academic_articles)
        
        # 测试手机厂商爬虫
        manufacturer_articles = test_manufacturer_crawler()
        all_articles.extend(manufacturer_articles)
        
        # 测试技术公司爬虫
        tech_company_articles = test_tech_company_crawler()
        all_articles.extend(tech_company_articles)
        
        # 保存到数据库
        print(f"\n💾 保存文章到数据库...")
        saved_count = 0
        for article in all_articles:
            try:
                db.insert_article(article)
                saved_count += 1
            except Exception as e:
                print(f"⚠️ 保存文章失败: {e}")
        
        print(f"✅ 成功保存 {saved_count} 篇文章到数据库")
        
        # 显示统计信息
        print("\n📈 测试结果统计:")
        print(f"   总爬取文章: {len(all_articles)} 篇")
        print(f"   成功保存: {saved_count} 篇")
        
        if all_articles:
            # 按来源类型统计
            source_counts = {}
            for article in all_articles:
                source_type = article.get('source_type', 'unknown')
                source_counts[source_type] = source_counts.get(source_type, 0) + 1
            
            print("   来源分布:")
            for source_type, count in source_counts.items():
                print(f"     - {source_type}: {count} 篇")
        
        print()
        print("🌐 查看结果:")
        print("   1. 启动Web服务器: python main.py")
        print("   2. 访问: http://localhost:5000")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        logging.error(f"测试失败: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("🎉 测试完成！")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main()) 