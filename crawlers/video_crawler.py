import requests
import json
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from datetime import datetime, timedelta
import time
from .base_crawler import BaseCrawler
from config import Config

class VideoCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_type = "video"
        self.youtube_api_key = None  # 可以后续添加YouTube API密钥
    
    def crawl(self, keywords: List[str]) -> List[Dict]:
        """爬取视频内容"""
        print("开始爬取视频内容...")
        
        # 爬取YouTube
        self._crawl_youtube(keywords)
        
        # 爬取Bilibili
        self._crawl_bilibili(keywords)
        
        # 爬取其他视频网站
        self._crawl_other_video_sites(keywords)
        
        print(f"视频爬取完成，共获取 {len(self.articles)} 个视频")
        return self.articles
    
    def _crawl_youtube(self, keywords: List[str]):
        """爬取YouTube视频"""
        print("爬取YouTube视频...")
        
        # YouTube搜索URL
        for keyword in keywords:
            search_url = f"https://www.youtube.com/results?search_query={keyword}"
            try:
                html = self.get_page(search_url)
                if not html:
                    continue
                
                # 提取视频信息
                video_data = self._extract_youtube_videos(html, keyword)
                for video in video_data:
                    self.add_article(video)
                
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                print(f"爬取YouTube失败 {keyword}: {e}")
                continue
    
    def _extract_youtube_videos(self, html: str, keyword: str) -> List[Dict]:
        """从YouTube页面提取视频信息"""
        videos = []
        
        try:
            # 查找YouTube的初始数据
            pattern = r'var ytInitialData = ({.*?});'
            match = re.search(pattern, html)
            if match:
                data = json.loads(match.group(1))
                videos = self._parse_youtube_data(data, keyword)
            else:
                # 备用方法：使用BeautifulSoup解析
                videos = self._parse_youtube_html(html, keyword)
        except Exception as e:
            print(f"解析YouTube数据失败: {e}")
        
        return videos
    
    def _parse_youtube_data(self, data: Dict, keyword: str) -> List[Dict]:
        """解析YouTube JSON数据"""
        videos = []
        
        try:
            # 查找视频内容
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            
            for content in contents:
                if 'itemSectionRenderer' in content:
                    items = content['itemSectionRenderer'].get('contents', [])
                    for item in items:
                        if 'videoRenderer' in item:
                            video = item['videoRenderer']
                            video_info = {
                                'title': video.get('title', {}).get('runs', [{}])[0].get('text', ''),
                                'content': video.get('descriptionSnippet', {}).get('runs', [{}])[0].get('text', ''),
                                'url': f"https://www.youtube.com/watch?v={video.get('videoId', '')}",
                                'source_type': self.source_type,
                                'source_name': 'YouTube',
                                'publish_date': self._parse_youtube_date(video.get('publishedTimeText', {}).get('simpleText', '')),
                                'keywords': self.extract_keywords(video.get('title', {}).get('runs', [{}])[0].get('text', '')),
                                'sentiment': 'neutral',
                                'video_id': video.get('videoId', ''),
                                'duration': video.get('lengthText', {}).get('simpleText', ''),
                                'view_count': video.get('viewCountText', {}).get('simpleText', ''),
                                'channel': video.get('ownerText', {}).get('runs', [{}])[0].get('text', '')
                            }
                            videos.append(video_info)
        except Exception as e:
            print(f"解析YouTube JSON数据失败: {e}")
        
        return videos[:10]  # 限制返回数量
    
    def _parse_youtube_html(self, html: str, keyword: str) -> List[Dict]:
        """使用BeautifulSoup解析YouTube HTML"""
        videos = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找视频链接
            video_links = soup.find_all('a', href=re.compile(r'/watch\?v='))
            
            for link in video_links[:10]:
                video_id = link.get('href', '').split('v=')[1].split('&')[0] if 'v=' in link.get('href', '') else ''
                if video_id:
                    title = link.get('title', '') or link.get_text().strip()
                    
                    video_info = {
                        'title': title,
                        'content': f"YouTube视频: {title}",
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'source_type': self.source_type,
                        'source_name': 'YouTube',
                        'publish_date': datetime.now().strftime('%Y-%m-%d'),
                        'keywords': self.extract_keywords(title),
                        'sentiment': 'neutral',
                        'video_id': video_id
                    }
                    videos.append(video_info)
        except Exception as e:
            print(f"解析YouTube HTML失败: {e}")
        
        return videos
    
    def _crawl_bilibili(self, keywords: List[str]):
        """爬取Bilibili视频"""
        print("爬取Bilibili视频...")
        
        for keyword in keywords:
            search_url = f"https://search.bilibili.com/all?keyword={keyword}"
            try:
                html = self.get_page(search_url)
                if not html:
                    continue
                
                video_data = self._extract_bilibili_videos(html, keyword)
                for video in video_data:
                    self.add_article(video)
                
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                print(f"爬取Bilibili失败 {keyword}: {e}")
                continue
    
    def _extract_bilibili_videos(self, html: str, keyword: str) -> List[Dict]:
        """从Bilibili页面提取视频信息"""
        videos = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找视频卡片
            video_cards = soup.find_all('li', class_='video-item')
            
            for card in video_cards[:10]:
                try:
                    title_elem = card.find('a', class_='title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text().strip()
                    video_url = urljoin('https://www.bilibili.com', title_elem.get('href', ''))
                    
                    # 提取视频ID
                    video_id = video_url.split('/')[-1].split('?')[0] if video_url else ''
                    
                    # 提取其他信息
                    duration_elem = card.find('span', class_='duration')
                    duration = duration_elem.get_text().strip() if duration_elem else ''
                    
                    view_elem = card.find('span', class_='play')
                    view_count = view_elem.get_text().strip() if view_elem else ''
                    
                    author_elem = card.find('a', class_='up-name')
                    author = author_elem.get_text().strip() if author_elem else ''
                    
                    video_info = {
                        'title': title,
                        'content': f"Bilibili视频: {title}",
                        'url': video_url,
                        'source_type': self.source_type,
                        'source_name': 'Bilibili',
                        'publish_date': datetime.now().strftime('%Y-%m-%d'),
                        'keywords': self.extract_keywords(title),
                        'sentiment': 'neutral',
                        'video_id': video_id,
                        'duration': duration,
                        'view_count': view_count,
                        'channel': author
                    }
                    videos.append(video_info)
                    
                except Exception as e:
                    print(f"解析Bilibili视频卡片失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"解析Bilibili页面失败: {e}")
        
        return videos
    
    def _crawl_other_video_sites(self, keywords: List[str]):
        """爬取其他视频网站"""
        print("爬取其他视频网站...")
        
        # 这里可以添加其他视频网站的爬取逻辑
        # 由于不同网站的结构差异很大，需要针对每个网站单独处理
        
        # 示例：爬取优酷
        for keyword in keywords:
            try:
                search_url = f"https://search.youku.com/search_video/q_{keyword}"
                html = self.get_page(search_url)
                if html:
                    video_data = self._extract_youku_videos(html, keyword)
                    for video in video_data:
                        self.add_article(video)
                
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                print(f"爬取优酷失败 {keyword}: {e}")
                continue
    
    def _extract_youku_videos(self, html: str, keyword: str) -> List[Dict]:
        """从优酷页面提取视频信息"""
        videos = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 查找视频链接（需要根据实际页面结构调整）
            video_links = soup.find_all('a', href=re.compile(r'/v_show/'))
            
            for link in video_links[:5]:
                title = link.get_text().strip()
                video_url = urljoin('https://www.youku.com', link.get('href', ''))
                
                video_info = {
                    'title': title,
                    'content': f"优酷视频: {title}",
                    'url': video_url,
                    'source_type': self.source_type,
                    'source_name': '优酷',
                    'publish_date': datetime.now().strftime('%Y-%m-%d'),
                    'keywords': self.extract_keywords(title),
                    'sentiment': 'neutral'
                }
                videos.append(video_info)
                
        except Exception as e:
            print(f"解析优酷页面失败: {e}")
        
        return videos
    
    def _parse_youtube_date(self, date_text: str) -> str:
        """解析YouTube日期"""
        if not date_text:
            return datetime.now().strftime('%Y-%m-%d')
        
        # 简单的日期解析
        try:
            # 处理相对时间，如"2天前"、"1周前"等
            if '天前' in date_text:
                days = int(re.search(r'(\d+)', date_text).group(1))
                date = datetime.now() - timedelta(days=days)
                return date.strftime('%Y-%m-%d')
            elif '周前' in date_text:
                weeks = int(re.search(r'(\d+)', date_text).group(1))
                date = datetime.now() - timedelta(weeks=weeks)
                return date.strftime('%Y-%m-%d')
            elif '月前' in date_text:
                months = int(re.search(r'(\d+)', date_text).group(1))
                date = datetime.now() - timedelta(days=months*30)
                return date.strftime('%Y-%m-%d')
            else:
                return datetime.now().strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')
    
    def is_valid_article(self, title: str, content: str) -> bool:
        """重写验证方法，适配视频内容"""
        if not title or not content:
            return False
        
        # 检查标题长度
        if len(title) < 5 or len(title) > 200:
            return False
        
        # 检查内容长度（视频内容可能较短）
        if len(content) < 20:
            return False
        
        # 检查是否包含关键词
        text = f"{title} {content}".lower()
        return any(keyword.lower() in text for keyword in Config.SEARCH_KEYWORDS) 