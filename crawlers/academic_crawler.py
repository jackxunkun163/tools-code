import requests
import arxiv
from typing import List, Dict
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime, timedelta
from .base_crawler import BaseCrawler
from config import Config

class AcademicCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_type = "academic"
    
    def crawl(self, keywords: List[str]) -> List[Dict]:
        """爬取学术论文和专利"""
        print("开始爬取学术论文和专利...")
        
        # 爬取arXiv论文
        self._crawl_arxiv(keywords)
        
        # 爬取Google Patents
        self._crawl_patents(keywords)
        
        # 爬取IEEE论文
        self._crawl_ieee(keywords)
        
        print(f"学术论文和专利爬取完成，共获取 {len(self.articles)} 篇文章")
        return self.articles
    
    def _crawl_arxiv(self, keywords: List[str]):
        """爬取arXiv论文"""
        try:
            for keyword in keywords[:5]:  # 限制关键词数量
                # 构建搜索查询
                search_query = f"all:{keyword}"
                
                # 搜索论文
                search = arxiv.Search(
                    query=search_query,
                    max_results=20,
                    sort_by=arxiv.SortCriterion.SubmittedDate
                )
                
                for result in search.results():
                    try:
                        # 提取论文信息
                        title = result.title
                        abstract = result.summary
                        authors = [author.name for author in result.authors]
                        published_date = result.published.strftime('%Y-%m-%d') if result.published else ""
                        pdf_url = result.pdf_url
                        arxiv_url = result.entry_id
                        
                        # 检查是否包含关键词
                        if self._contains_keywords(title + " " + abstract, keywords):
                            article_data = {
                                'title': title,
                                'content': f"摘要: {abstract}\n\n作者: {', '.join(authors)}",
                                'url': arxiv_url,
                                'source_type': self.source_type,
                                'source_name': 'arXiv',
                                'publish_date': published_date,
                                'keywords': self.extract_keywords(title + " " + abstract),
                                'sentiment': 'neutral'
                            }
                            
                            self.add_article(article_data)
                        
                        time.sleep(Config.REQUEST_DELAY)
                        
                    except Exception as e:
                        print(f"处理arXiv论文失败: {e}")
                        continue
                
                time.sleep(Config.REQUEST_DELAY)
                
        except Exception as e:
            print(f"爬取arXiv失败: {e}")
    
    def _crawl_patents(self, keywords: List[str]):
        """爬取Google Patents"""
        try:
            for keyword in keywords[:3]:  # 限制关键词数量
                # Google Patents搜索URL
                search_url = f"https://patents.google.com/?q={keyword}&language=ENGLISH"
                html = self.get_page(search_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 查找专利链接
                    patent_links = soup.select('a[data-result="patent"]')
                    
                    for link in patent_links[:10]:  # 限制专利数量
                        patent_url = "https://patents.google.com" + link.get('href')
                        
                        try:
                            patent_html = self.get_page(patent_url)
                            if patent_html:
                                patent_data = self._extract_patent_data(patent_html, patent_url, keyword)
                                if patent_data:
                                    self.add_article(patent_data)
                            
                            time.sleep(Config.REQUEST_DELAY)
                            
                        except Exception as e:
                            print(f"处理专利失败 {patent_url}: {e}")
                            continue
                
                time.sleep(Config.REQUEST_DELAY)
                
        except Exception as e:
            print(f"爬取Google Patents失败: {e}")
    
    def _crawl_ieee(self, keywords: List[str]):
        """爬取IEEE论文"""
        try:
            for keyword in keywords[:3]:  # 限制关键词数量
                # IEEE Xplore搜索URL
                search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={keyword}"
                html = self.get_page(search_url)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 查找论文链接
                    paper_links = soup.select('a[data-testid="title"]')
                    
                    for link in paper_links[:10]:  # 限制论文数量
                        paper_url = "https://ieeexplore.ieee.org" + link.get('href')
                        
                        try:
                            paper_html = self.get_page(paper_url)
                            if paper_html:
                                paper_data = self._extract_ieee_paper_data(paper_html, paper_url, keyword)
                                if paper_data:
                                    self.add_article(paper_data)
                            
                            time.sleep(Config.REQUEST_DELAY)
                            
                        except Exception as e:
                            print(f"处理IEEE论文失败 {paper_url}: {e}")
                            continue
                
                time.sleep(Config.REQUEST_DELAY)
                
        except Exception as e:
            print(f"爬取IEEE失败: {e}")
    
    def _extract_patent_data(self, html: str, url: str, keyword: str) -> Dict:
        """提取专利数据"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取专利标题
        title_elem = soup.select_one('span[itemprop="title"]')
        title = title_elem.get_text().strip() if title_elem else ""
        
        # 提取专利摘要
        abstract_elem = soup.select_one('div[itemprop="abstract"]')
        abstract = abstract_elem.get_text().strip() if abstract_elem else ""
        
        # 提取申请人
        assignee_elem = soup.select_one('span[itemprop="assignee"]')
        assignee = assignee_elem.get_text().strip() if assignee_elem else ""
        
        # 提取发明人
        inventors = []
        inventor_elems = soup.select('span[itemprop="inventor"]')
        for elem in inventor_elems:
            inventors.append(elem.get_text().strip())
        
        # 提取申请日期
        filing_date_elem = soup.select_one('time[itemprop="filingDate"]')
        filing_date = filing_date_elem.get_text().strip() if filing_date_elem else ""
        
        content = f"摘要: {abstract}\n\n申请人: {assignee}\n发明人: {', '.join(inventors)}"
        
        return {
            'title': f"专利: {title}",
            'content': content,
            'url': url,
            'source_type': self.source_type,
            'source_name': 'Google Patents',
            'publish_date': filing_date,
            'keywords': self.extract_keywords(title + " " + abstract),
            'sentiment': 'neutral'
        }
    
    def _extract_ieee_paper_data(self, html: str, url: str, keyword: str) -> Dict:
        """提取IEEE论文数据"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取论文标题
        title_elem = soup.select_one('h1[data-testid="title"]')
        title = title_elem.get_text().strip() if title_elem else ""
        
        # 提取论文摘要
        abstract_elem = soup.select_one('div[data-testid="abstract"]')
        abstract = abstract_elem.get_text().strip() if abstract_elem else ""
        
        # 提取作者
        authors = []
        author_elems = soup.select('a[data-testid="author"]')
        for elem in author_elems:
            authors.append(elem.get_text().strip())
        
        # 提取发表日期
        date_elem = soup.select_one('span[data-testid="publication-date"]')
        publish_date = date_elem.get_text().strip() if date_elem else ""
        
        content = f"摘要: {abstract}\n\n作者: {', '.join(authors)}"
        
        return {
            'title': f"IEEE论文: {title}",
            'content': content,
            'url': url,
            'source_type': self.source_type,
            'source_name': 'IEEE Xplore',
            'publish_date': publish_date,
            'keywords': self.extract_keywords(title + " " + abstract),
            'sentiment': 'neutral'
        }
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含关键词"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords) 