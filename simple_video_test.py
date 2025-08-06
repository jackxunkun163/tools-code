#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from crawlers.video_crawler import VideoCrawler
    print("✅ 视频爬虫导入成功")
    
    # 创建爬虫实例
    crawler = VideoCrawler()
    print("✅ 视频爬虫实例创建成功")
    
    # 测试基本方法
    test_html = "<html><body><h1>Test</h1></body></html>"
    text = crawler.extract_text(test_html)
    print(f"✅ 文本提取测试: {text[:20]}...")
    
    # 测试关键词提取
    keywords = crawler.extract_keywords("这是一个关于蓝牙技术的视频")
    print(f"✅ 关键词提取测试: {keywords}")
    
    print("\n🎉 视频爬虫基本功能测试通过！")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc() 