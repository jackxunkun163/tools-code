import feedparser
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime
from .base_crawler import BaseCrawler
from config import Config
import time

class NewsCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_type = "news"
    
    def crawl(self, keywords: List[str]) -> List[Dict]:
        """爬取新闻文章"""
        print("开始爬取新闻文章...")
        
        # 爬取RSS源
        self._crawl_rss_feeds(keywords)
        
        # 爬取新闻网站
        self._crawl_news_sites(keywords)
        
        print(f"新闻爬取完成，共获取 {len(self.articles)} 篇文章")
        return self.articles
    
    def _crawl_rss_feeds(self, keywords: List[str]):
        """爬取RSS源"""
        rss_feeds = [
            "https://www.cnbeta.com.tw/backend.php",
            "https://www.ithome.com/rss/",
            "https://feeds.feedburner.com/engadget",
            "https://www.theverge.com/rss/index.xml",
            "https://techcrunch.com/feed/",
            "https://www.wired.com/feed/rss"
        ]
        
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:20]:  # 限制每个源的文章数量
                    if self._contains_keywords(entry.title + " " + entry.get('summary', ''), keywords):
                        article_data = {
                            'title': entry.title,
                            'content': entry.get('summary', ''),
                            'url': entry.link,
                            'source_type': self.source_type,
                            'source_name': feed.feed.get('title', 'Unknown'),
                            'publish_date': self._parse_date(entry.get('published', '')),
                            'keywords': self.extract_keywords(entry.title + " " + entry.get('summary', '')),
                            'sentiment': 'neutral'
                        }
                        
                        # 获取完整内容
                        full_content = self._get_full_content(entry.link)
                        if full_content:
                            article_data['content'] = full_content
                        
                        self.add_article(article_data)
                
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                print(f"爬取RSS源失败 {feed_url}: {e}")
                continue
    
    def _crawl_news_sites(self, keywords: List[str]):
        """爬取新闻网站"""
        for site_url in Config.NEWS_SOURCES:
            try:
                html = self.get_page(site_url)
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # 查找文章链接
                article_links = self._find_article_links(soup, site_url)
                
                for link in article_links[:10]:  # 限制每个网站的文章数量
                    try:
                        article_html = self.get_page(link)
                        if not article_html:
                            continue
                        
                        article_data = self._extract_article_data(article_html, link, site_url)
                        if article_data and self._contains_keywords(article_data['title'] + " " + article_data['content'], keywords):
                            self.add_article(article_data)
                        
                        time.sleep(Config.REQUEST_DELAY)
                        
                    except Exception as e:
                        print(f"处理文章失败 {link}: {e}")
                        continue
                
            except Exception as e:
                print(f"爬取新闻网站失败 {site_url}: {e}")
                continue
    
    def _find_article_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """查找文章链接"""
        links = []
        
        # 常见的文章链接选择器
        selectors = [
            'a[href*="/article/"]',
            'a[href*="/news/"]',
            'a[href*="/story/"]',
            'a[href*="/post/"]',
            'h1 a', 'h2 a', 'h3 a',
            '.article-title a',
            '.news-title a',
            '.post-title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    if full_url not in links:
                        links.append(full_url)
        
        return links
    
    def _extract_article_data(self, html: str, url: str, source_name: str) -> Dict:
        """提取文章数据"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title = ""
        title_selectors = ['h1', '.article-title', '.post-title', '.news-title', 'title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                break
        
        # 提取内容
        content = ""
        content_selectors = [
            '.article-content', '.post-content', '.news-content',
            '.entry-content', '.content', 'article'
        ]
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = self.extract_text(str(content_elem))
                break
        
        if not content:
            content = self.extract_text(html)
        
        # 提取发布日期
        publish_date = ""
        date_selectors = [
            '.publish-date', '.post-date', '.news-date',
            'time', '.date', '.timestamp'
        ]
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                publish_date = date_elem.get_text().strip()
                break
        
        return {
            'title': title,
            'content': content,
            'url': url,
            'source_type': self.source_type,
            'source_name': source_name,
            'publish_date': publish_date,
            'keywords': self.extract_keywords(title + " " + content),
            'sentiment': 'neutral'
        }
    
    def _get_full_content(self, url: str) -> str:
        """获取完整内容"""
        try:
            html = self.get_page(url)
            if html:
                return self.extract_text(html)
        except:
            pass
        return ""
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含关键词"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def _parse_date(self, date_str: str) -> str:
        """解析日期字符串"""
        if not date_str:
            return ""
        
        try:
            # 尝试解析各种日期格式
            date_formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%d %b %Y',
                '%B %d, %Y'
            ]
            
            for fmt in date_formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%d')
                except:
                    continue
            
            return date_str
        except:
            return "" 