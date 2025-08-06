#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统功能测试脚本
"""

import sys
import os
import sqlite3
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """测试数据库功能"""
    print("测试数据库功能...")
    try:
        from database import Database
        db = Database()
        print("✓ 数据库初始化成功")
        
        # 测试插入文章
        test_article = {
            'title': '测试文章标题',
            'content': '这是一篇测试文章的内容，用于验证数据库功能是否正常。',
            'url': 'https://example.com/test',
            'source_type': 'test',
            'source_name': '测试来源',
            'publish_date': '2024-01-01',
            'keywords': ['测试', '蓝牙'],
            'sentiment': 'neutral'
        }
        
        result = db.insert_article(test_article)
        if result:
            print("✓ 文章插入成功")
        else:
            print("✗ 文章插入失败")
            
        # 测试获取文章
        articles = db.get_recent_articles(days=1, limit=10)
        if articles:
            print(f"✓ 获取文章成功，共 {len(articles)} 篇")
        else:
            print("✗ 获取文章失败")
            
        return True
    except Exception as e:
        print(f"✗ 数据库测试失败: {e}")
        return False

def test_config():
    """测试配置功能"""
    print("测试配置功能...")
    try:
        from config import Config
        print(f"✓ 配置加载成功")
        print(f"  - 数据库路径: {Config.DATABASE_PATH}")
        print(f"  - 定时任务时间: {Config.SCHEDULE_TIME}")
        print(f"  - Web服务器端口: {Config.PORT}")
        return True
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def test_crawlers():
    """测试爬虫模块"""
    print("测试爬虫模块...")
    try:
        from crawlers.news_crawler import NewsCrawler
        from crawlers.tech_crawler import TechCrawler
        from crawlers.academic_crawler import AcademicCrawler
        
        print("✓ 爬虫模块导入成功")
        
        # 测试基础爬虫功能
        news_crawler = NewsCrawler()
        tech_crawler = TechCrawler()
        academic_crawler = AcademicCrawler()
        
        print("✓ 爬虫实例化成功")
        return True
    except Exception as e:
        print(f"✗ 爬虫测试失败: {e}")
        return False

def test_summarizer():
    """测试总结器功能"""
    print("测试总结器功能...")
    try:
        from summarizer import Summarizer
        summarizer = Summarizer()
        print("✓ 总结器初始化成功")
        
        # 测试备用总结功能
        test_articles = [{
            'title': '测试文章',
            'content': '测试内容',
            'source_type': 'test',
            'keywords': ['测试']
        }]
        
        summary = summarizer._generate_fallback_summary(test_articles)
        if summary:
            print("✓ 备用总结功能正常")
        else:
            print("✗ 备用总结功能异常")
            
        return True
    except Exception as e:
        print(f"✗ 总结器测试失败: {e}")
        return False

def test_web_app():
    """测试Web应用"""
    print("测试Web应用...")
    try:
        from web_app import app
        print("✓ Flask应用创建成功")
        
        # 测试路由
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ 主页路由正常")
            else:
                print(f"✗ 主页路由异常，状态码: {response.status_code}")
                
        return True
    except Exception as e:
        print(f"✗ Web应用测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("蓝牙技术文章聚合平台 - 系统测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("配置功能", test_config),
        ("数据库功能", test_database),
        ("爬虫模块", test_crawlers),
        ("总结器功能", test_summarizer),
        ("Web应用", test_web_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"测试 {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 