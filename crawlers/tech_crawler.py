import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
from .base_crawler import BaseCrawler
from config import Config

class TechCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_type = "tech"
    
    def crawl(self, keywords: List[str]) -> List[Dict]:
        """爬取技术文章"""
        print("开始爬取技术文章...")
        
        # 爬取技术博客
        self._crawl_tech_blogs(keywords)
        
        # 爬取GitHub
        self._crawl_github(keywords)
        
        # 爬取Stack Overflow
        self._crawl_stackoverflow(keywords)
        
        print(f"技术文章爬取完成，共获取 {len(self.articles)} 篇文章")
        return self.articles
    
    def _crawl_tech_blogs(self, keywords: List[str]):
        """爬取技术博客"""
        tech_sites = [
            "https://www.infoq.com/",
            "https://medium.com/",
            "https://dev.to/",
            "https://css-tricks.com/",
            "https://www.smashingmagazine.com/"
        ]
        
        for site_url in tech_sites:
            try:
                html = self.get_page(site_url)
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                article_links = self._find_tech_article_links(soup, site_url)
                
                for link in article_links[:15]:  # 限制每个网站的文章数量
                    try:
                        article_html = self.get_page(link)
                        if not article_html:
                            continue
                        
                        article_data = self._extract_tech_article_data(article_html, link, site_url)
                        if article_data and self._contains_keywords(article_data['title'] + " " + article_data['content'], keywords):
                            self.add_article(article_data)
                        
                        time.sleep(Config.REQUEST_DELAY)
                        
                    except Exception as e:
                        print(f"处理技术文章失败 {link}: {e}")
                        continue
                
            except Exception as e:
                print(f"爬取技术博客失败 {site_url}: {e}")
                continue
    
    def _crawl_github(self, keywords: List[str]):
        """爬取GitHub相关项目"""
        try:
            # 搜索GitHub上的蓝牙相关项目
            for keyword in keywords[:5]:  # 限制关键词数量
                search_url = f"https://github.com/search?q={keyword}&type=repositories"
                html = self.get_page(search_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    repo_links = soup.select('a[data-testid="result-repo-link"]')
                    
                    for link in repo_links[:5]:  # 限制每个关键词的仓库数量
                        repo_url = urljoin("https://github.com", link.get('href'))
                        
                        try:
                            repo_html = self.get_page(repo_url)
                            if repo_html:
                                repo_data = self._extract_github_repo_data(repo_html, repo_url, keyword)
                                if repo_data:
                                    self.add_article(repo_data)
                            
                            time.sleep(Config.REQUEST_DELAY)
                            
                        except Exception as e:
                            print(f"处理GitHub仓库失败 {repo_url}: {e}")
                            continue
                
                time.sleep(Config.REQUEST_DELAY)
                
        except Exception as e:
            print(f"爬取GitHub失败: {e}")
    
    def _crawl_stackoverflow(self, keywords: List[str]):
        """爬取Stack Overflow问答"""
        try:
            for keyword in keywords[:3]:  # 限制关键词数量
                search_url = f"https://stackoverflow.com/search?q={keyword}"
                html = self.get_page(search_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    question_links = soup.select('.question-hyperlink')
                    
                    for link in question_links[:10]:  # 限制每个关键词的问题数量
                        question_url = urljoin("https://stackoverflow.com", link.get('href'))
                        
                        try:
                            question_html = self.get_page(question_url)
                            if question_html:
                                question_data = self._extract_stackoverflow_data(question_html, question_url, keyword)
                                if question_data:
                                    self.add_article(question_data)
                            
                            time.sleep(Config.REQUEST_DELAY)
                            
                        except Exception as e:
                            print(f"处理Stack Overflow问题失败 {question_url}: {e}")
                            continue
                
                time.sleep(Config.REQUEST_DELAY)
                
        except Exception as e:
            print(f"爬取Stack Overflow失败: {e}")
    
    def _find_tech_article_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """查找技术文章链接"""
        links = []
        
        # 技术博客常见的文章链接选择器
        selectors = [
            'a[href*="/article/"]',
            'a[href*="/post/"]',
            'a[href*="/blog/"]',
            'a[href*="/tutorial/"]',
            'a[href*="/guide/"]',
            '.post-title a',
            '.article-title a',
            '.blog-title a',
            'h1 a', 'h2 a', 'h3 a'
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
    
    def _extract_tech_article_data(self, html: str, url: str, source_name: str) -> Dict:
        """提取技术文章数据"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title = ""
        title_selectors = [
            'h1', '.post-title', '.article-title', '.blog-title',
            '.entry-title', '.title', 'title'
        ]
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                break
        
        # 提取内容
        content = ""
        content_selectors = [
            '.post-content', '.article-content', '.blog-content',
            '.entry-content', '.content', 'article', '.post-body'
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
            '.publish-date', '.post-date', '.blog-date',
            'time', '.date', '.timestamp', '.meta-date'
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
    
    def _extract_github_repo_data(self, html: str, url: str, keyword: str) -> Dict:
        """提取GitHub仓库数据"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取仓库名称
        title_elem = soup.select_one('h1 strong a')
        title = title_elem.get_text().strip() if title_elem else ""
        
        # 提取描述
        description_elem = soup.select_one('.repository-meta-content')
        description = description_elem.get_text().strip() if description_elem else ""
        
        # 提取README内容
        readme_elem = soup.select_one('#readme .markdown-body')
        readme_content = self.extract_text(str(readme_elem)) if readme_elem else ""
        
        content = f"{description}\n\n{readme_content}"
        
        return {
            'title': f"GitHub项目: {title}",
            'content': content,
            'url': url,
            'source_type': self.source_type,
            'source_name': 'GitHub',
            'publish_date': "",
            'keywords': self.extract_keywords(title + " " + content),
            'sentiment': 'neutral'
        }
    
    def _extract_stackoverflow_data(self, html: str, url: str, keyword: str) -> Dict:
        """提取Stack Overflow数据"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取问题标题
        title_elem = soup.select_one('.question-hyperlink')
        title = title_elem.get_text().strip() if title_elem else ""
        
        # 提取问题内容
        question_elem = soup.select_one('.question .post-text')
        question_content = self.extract_text(str(question_elem)) if question_elem else ""
        
        # 提取答案内容
        answers = []
        answer_elems = soup.select('.answer .post-text')
        for answer_elem in answer_elems[:3]:  # 只取前3个答案
            answer_content = self.extract_text(str(answer_elem))
            if answer_content:
                answers.append(answer_content)
        
        content = f"问题: {question_content}\n\n答案: {' '.join(answers)}"
        
        return {
            'title': f"Stack Overflow: {title}",
            'content': content,
            'url': url,
            'source_type': self.source_type,
            'source_name': 'Stack Overflow',
            'publish_date': "",
            'keywords': self.extract_keywords(title + " " + content),
            'sentiment': 'neutral'
        }
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含关键词"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords) 