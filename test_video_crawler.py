#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频爬虫测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawlers.video_crawler import VideoCrawler
from config import Config

def test_video_crawler():
    """测试视频爬虫"""
    print("=" * 60)
    print("视频爬虫测试")
    print("=" * 60)
    
    # 创建视频爬虫实例
    crawler = VideoCrawler()
    
    # 测试关键词
    test_keywords = ["蓝牙", "Bluetooth"]
    
    print(f"测试关键词: {test_keywords}")
    print("开始爬取视频内容...")
    
    try:
        # 执行爬取
        articles = crawler.crawl(test_keywords)
        
        print(f"\n爬取完成，共获取 {len(articles)} 个视频")
        print("\n" + "=" * 60)
        
        # 显示结果
        for i, article in enumerate(articles[:5], 1):  # 只显示前5个
            print(f"\n视频 {i}:")
            print(f"  标题: {article.get('title', 'N/A')}")
            print(f"  来源: {article.get('source_name', 'N/A')}")
            print(f"  类型: {article.get('source_type', 'N/A')}")
            print(f"  URL: {article.get('url', 'N/A')}")
            print(f"  关键词: {article.get('keywords', [])}")
            if article.get('video_id'):
                print(f"  视频ID: {article.get('video_id')}")
            if article.get('duration'):
                print(f"  时长: {article.get('duration')}")
            if article.get('view_count'):
                print(f"  播放量: {article.get('view_count')}")
            if article.get('channel'):
                print(f"  频道: {article.get('channel')}")
            print(f"  发布日期: {article.get('publish_date', 'N/A')}")
        
        if len(articles) > 5:
            print(f"\n... 还有 {len(articles) - 5} 个视频")
        
        print("\n" + "=" * 60)
        print("测试完成")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_sites():
    """测试特定网站"""
    print("\n" + "=" * 60)
    print("测试特定网站")
    print("=" * 60)
    
    crawler = VideoCrawler()
    
    # 测试YouTube
    print("\n测试YouTube...")
    try:
        html = crawler.get_page("https://www.youtube.com/results?search_query=蓝牙")
        if html:
            videos = crawler._extract_youtube_videos(html, "蓝牙")
            print(f"YouTube测试成功，获取 {len(videos)} 个视频")
        else:
            print("YouTube测试失败：无法获取页面")
    except Exception as e:
        print(f"YouTube测试失败: {e}")
    
    # 测试Bilibili
    print("\n测试Bilibili...")
    try:
        html = crawler.get_page("https://search.bilibili.com/all?keyword=蓝牙")
        if html:
            videos = crawler._extract_bilibili_videos(html, "蓝牙")
            print(f"Bilibili测试成功，获取 {len(videos)} 个视频")
        else:
            print("Bilibili测试失败：无法获取页面")
    except Exception as e:
        print(f"Bilibili测试失败: {e}")

if __name__ == "__main__":
    # 运行基本测试
    success = test_video_crawler()
    
    # 运行特定网站测试
    test_specific_sites()
    
    if success:
        print("\n✅ 视频爬虫测试通过")
    else:
        print("\n❌ 视频爬虫测试失败") 