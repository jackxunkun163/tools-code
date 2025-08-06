#!/usr/bin/env python3
"""
测试手机厂商和技术公司爬虫
快速测试新添加的厂商爬虫功能
"""

import sys
import os
import logging
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawlers.manufacturer_crawler import ManufacturerCrawler
from database import Database
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_manufacturer_sites():
    """测试手机厂商网站爬虫"""
    print("📱 测试手机厂商网站爬虫...")
    try:
        crawler = ManufacturerCrawler()
        articles = crawler.crawl_manufacturer_sites(limit=10)  # 只爬取10篇文章
        print(f"✅ 手机厂商爬虫成功，获取 {len(articles)} 篇文章")
        
        # 显示获取的文章
        for i, article in enumerate(articles[:5], 1):
            print(f"  {i}. {article['title'][:60]}...")
            print(f"     来源: {article['source']}")
            print(f"     URL: {article['url']}")
            print()
        
        return articles
    except Exception as e:
        print(f"❌ 手机厂商爬虫失败: {e}")
        return []

def test_tech_company_sites():
    """测试技术公司网站爬虫"""
    print("🏢 测试技术公司网站爬虫...")
    try:
        crawler = ManufacturerCrawler()
        articles = crawler.crawl_tech_company_sites(limit=10)  # 只爬取10篇文章
        print(f"✅ 技术公司爬虫成功，获取 {len(articles)} 篇文章")
        
        # 显示获取的文章
        for i, article in enumerate(articles[:5], 1):
            print(f"  {i}. {article['title'][:60]}...")
            print(f"     来源: {article['source']}")
            print(f"     URL: {article['url']}")
            print()
        
        return articles
    except Exception as e:
        print(f"❌ 技术公司爬虫失败: {e}")
        return []

def test_specific_sites():
    """测试特定网站的爬取"""
    print("🎯 测试特定网站爬取...")
    
    test_sites = [
        ("苹果开发者", "https://developer.apple.com/"),
        ("高通开发者", "https://developer.qualcomm.com/"),
        ("蓝牙官方", "https://www.bluetooth.com/"),
        ("Nordic半导体", "https://www.nordic.com/"),
        ("乐鑫科技", "https://www.espressif.com/")
    ]
    
    crawler = ManufacturerCrawler()
    all_articles = []
    
    for name, url in test_sites:
        try:
            print(f"\n🔍 测试 {name}: {url}")
            articles = crawler._crawl_single_tech_company_site(url, limit=3)
            print(f"   获取 {len(articles)} 篇文章")
            
            for article in articles:
                print(f"   - {article['title'][:50]}...")
            
            all_articles.extend(articles)
            
        except Exception as e:
            print(f"   ❌ 失败: {e}")
    
    return all_articles

def main():
    print("=" * 70)
    print("🧪 手机厂商和技术公司爬虫测试")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 初始化数据库
        print("📊 初始化数据库...")
        db = Database()
        db.init_database()
        print("✅ 数据库初始化完成")
        
        all_articles = []
        
        # 测试手机厂商网站
        print("\n" + "="*50)
        manufacturer_articles = test_manufacturer_sites()
        all_articles.extend(manufacturer_articles)
        
        # 测试技术公司网站
        print("\n" + "="*50)
        tech_company_articles = test_tech_company_sites()
        all_articles.extend(tech_company_articles)
        
        # 测试特定网站
        print("\n" + "="*50)
        specific_articles = test_specific_sites()
        all_articles.extend(specific_articles)
        
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
            source_type_counts = {}
            
            for article in all_articles:
                source = article.get('source', 'unknown')
                source_type = article.get('source_type', 'unknown')
                
                source_counts[source] = source_counts.get(source, 0) + 1
                source_type_counts[source_type] = source_type_counts.get(source_type, 0) + 1
            
            print("\n   按来源统计:")
            for source, count in sorted(source_counts.items()):
                print(f"     - {source}: {count} 篇")
            
            print("\n   按类型统计:")
            for source_type, count in sorted(source_type_counts.items()):
                print(f"     - {source_type}: {count} 篇")
        
        print("\n🌐 查看结果:")
        print("   1. 启动Web服务器: python main.py")
        print("   2. 访问: http://localhost:5000")
        print("   3. 查看新增的厂商文章")
        
        # 显示新数据源的网站列表
        print(f"\n📋 新增数据源统计:")
        print(f"   手机厂商网站: {len(Config.PHONE_MANUFACTURER_SOURCES)} 个")
        print(f"   技术公司网站: {len(Config.TECH_COMPANY_SOURCES)} 个")
        
        print("\n主要厂商包括:")
        manufacturers = ["苹果", "三星", "华为", "小米", "OPPO", "vivo", "一加", "谷歌"]
        for mfg in manufacturers:
            print(f"   ✓ {mfg}")
        
        print("\n主要技术公司包括:")
        tech_companies = ["高通", "联发科", "Intel", "ARM", "Nordic", "乐鑫", "蓝牙官方"]
        for company in tech_companies:
            print(f"   ✓ {company}")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        logging.error(f"测试失败: {e}")
        return 1
    
    print()
    print("=" * 70)
    print("🎉 厂商爬虫测试完成！")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    exit(main())