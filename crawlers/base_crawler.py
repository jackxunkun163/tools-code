import requests
import time
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from config import Config

class BaseCrawler(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT
        })
        self.articles = []
    
    def get_page(self, url: str, retries: int = 3) -> Optional[str]:
        """获取页面内容"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"获取页面失败 {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(1, 3))
                continue
        return None
    
    def extract_text(self, html: str) -> str:
        """提取纯文本内容"""
        if not html:
            return ""
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除脚本和样式标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取文本
        text = soup.get_text()
        
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        if not text:
            return []
        
        # 简单的关键词提取（可以后续优化）
        keywords = []
        for keyword in Config.SEARCH_KEYWORDS:
            if keyword.lower() in text.lower():
                keywords.append(keyword)
        
        return list(set(keywords))
    
    def clean_url(self, url: str) -> str:
        """清理URL"""
        if not url:
            return ""
        
        # 移除URL参数
        parsed = urlparse(url)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        return clean_url
    
    def is_valid_article(self, title: str, content: str) -> bool:
        """检查是否为有效文章"""
        if not title or not content:
            return False
        
        # 检查标题长度
        if len(title) < 10 or len(title) > 200:
            return False
        
        # 检查内容长度
        if len(content) < 100:
            return False
        
        # 检查是否包含关键词
        text = f"{title} {content}".lower()
        return any(keyword.lower() in text for keyword in Config.SEARCH_KEYWORDS)
    
    def add_article(self, article_data: Dict):
        """添加文章到列表"""
        if self.is_valid_article(article_data.get('title', ''), article_data.get('content', '')):
            self.articles.append(article_data)
    
    @abstractmethod
    def crawl(self, keywords: List[str]) -> List[Dict]:
        """爬取文章的具体实现"""
        pass
    
    def get_articles(self) -> List[Dict]:
        """获取爬取的文章"""
        return self.articles.copy() 