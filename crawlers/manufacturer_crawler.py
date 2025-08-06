#!/usr/bin/env python3
"""
手机厂商和技术公司爬虫
专门爬取各大手机厂商和技术公司的蓝牙相关技术文章
"""

import requests
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict
import re
from datetime import datetime

from .base_crawler import BaseCrawler
from config import Config

class ManufacturerCrawler(BaseCrawler):
    """手机厂商和技术公司爬虫"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
    def crawl_manufacturer_sites(self, limit: int = 50) -> List[Dict]:
        """爬取手机厂商网站"""
        articles = []
        
        self.logger.info("开始爬取手机厂商网站...")
        
        for source in Config.PHONE_MANUFACTURER_SOURCES[:10]:  # 限制数量以避免过多请求
            try:
                self.logger.info(f"正在爬取: {source}")
                site_articles = self._crawl_single_manufacturer_site(source, limit // 10)
                articles.extend(site_articles)
                
                if len(articles) >= limit:
                    break
                    
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                self.logger.error(f"爬取 {source} 失败: {e}")
                continue
        
        self.logger.info(f"手机厂商网站爬取完成，获得 {len(articles)} 篇文章")
        return articles
    
    def crawl_tech_company_sites(self, limit: int = 50) -> List[Dict]:
        """爬取技术公司网站"""
        articles = []
        
        self.logger.info("开始爬取技术公司网站...")
        
        for source in Config.TECH_COMPANY_SOURCES[:15]:  # 限制数量
            try:
                self.logger.info(f"正在爬取: {source}")
                site_articles = self._crawl_single_tech_company_site(source, limit // 15)
                articles.extend(site_articles)
                
                if len(articles) >= limit:
                    break
                    
                time.sleep(Config.REQUEST_DELAY)
                
            except Exception as e:
                self.logger.error(f"爬取 {source} 失败: {e}")
                continue
        
        self.logger.info(f"技术公司网站爬取完成，获得 {len(articles)} 篇文章")
        return articles
    
    def _crawl_single_manufacturer_site(self, url: str, limit: int) -> List[Dict]:
        """爬取单个手机厂商网站"""
        articles = []
        
        try:
            # 针对不同厂商使用不同的爬取策略
            if "apple.com" in url:
                articles = self._crawl_apple_site(url, limit)
            elif "samsung.com" in url:
                articles = self._crawl_samsung_site(url, limit)
            elif "huawei.com" in url or "hisilicon.com" in url:
                articles = self._crawl_huawei_site(url, limit)
            elif "mi.com" in url:
                articles = self._crawl_xiaomi_site(url, limit)
            elif "developer.qualcomm.com" in url:
                articles = self._crawl_qualcomm_site(url, limit)
            else:
                # 通用爬取策略
                articles = self._crawl_generic_site(url, limit)
                
        except Exception as e:
            self.logger.error(f"爬取 {url} 失败: {e}")
            
        return articles
    
    def _crawl_single_tech_company_site(self, url: str, limit: int) -> List[Dict]:
        """爬取单个技术公司网站"""
        articles = []
        
        try:
            # 针对不同公司使用不同的爬取策略
            if "qualcomm.com" in url:
                articles = self._crawl_qualcomm_site(url, limit)
            elif "bluetooth.com" in url or "bluetooth.org" in url:
                articles = self._crawl_bluetooth_org_site(url, limit)
            elif "nordic.com" in url:
                articles = self._crawl_nordic_site(url, limit)
            elif "espressif.com" in url:
                articles = self._crawl_espressif_site(url, limit)
            elif "anandtech.com" in url:
                articles = self._crawl_anandtech_site(url, limit)
            else:
                # 通用爬取策略
                articles = self._crawl_generic_site(url, limit)
                
        except Exception as e:
            self.logger.error(f"爬取 {url} 失败: {e}")
            
        return articles
    
    def _crawl_apple_site(self, url: str, limit: int) -> List[Dict]:
        """爬取苹果开发者网站"""
        articles = []
        
        try:
            # 搜索苹果开发者文档中的蓝牙相关内容
            search_urls = [
                "https://developer.apple.com/documentation/corebluetooth",
                "https://developer.apple.com/documentation/externalaccessory",
                "https://developer.apple.com/news/"
            ]
            
            for search_url in search_urls:
                response = self._make_request(search_url)
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 查找文档链接
                    links = soup.find_all('a', href=True)
                    for link in links[:limit]:
                        href = link.get('href')
                        title = link.get_text(strip=True)
                        
                        if self._is_bluetooth_related(title) and href:
                            full_url = urljoin(search_url, href)
                            article = {
                                'title': title,
                                'url': full_url,
                                'source': 'Apple Developer',
                                'source_type': 'manufacturer',
                                'description': self._extract_description(soup, link),
                                'published_date': datetime.now().isoformat(),
                                'keywords': ['蓝牙', 'iOS', '苹果', 'CoreBluetooth']
                            }
                            articles.append(article)
                            
                            if len(articles) >= limit:
                                break
                
                if len(articles) >= limit:
                    break
                    
        except Exception as e:
            self.logger.error(f"爬取Apple网站失败: {e}")
            
        return articles
    
    def _crawl_samsung_site(self, url: str, limit: int) -> List[Dict]:
        """爬取三星开发者网站"""
        articles = []
        
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找新闻和文档链接
                content_selectors = [
                    'a[href*="bluetooth"]',
                    'a[href*="connectivity"]',
                    '.news-item a',
                    '.article-item a'
                ]
                
                for selector in content_selectors:
                    links = soup.select(selector)
                    for link in links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get('href')
                        
                        if self._is_bluetooth_related(title) and href:
                            full_url = urljoin(url, href)
                            article = {
                                'title': title,
                                'url': full_url,
                                'source': 'Samsung Developer',
                                'source_type': 'manufacturer',
                                'description': self._extract_description(soup, link),
                                'published_date': datetime.now().isoformat(),
                                'keywords': ['蓝牙', 'Android', '三星', 'Galaxy']
                            }
                            articles.append(article)
                            
                            if len(articles) >= limit:
                                break
                
        except Exception as e:
            self.logger.error(f"爬取Samsung网站失败: {e}")
            
        return articles
    
    def _crawl_huawei_site(self, url: str, limit: int) -> List[Dict]:
        """爬取华为开发者网站"""
        articles = []
        
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找技术文档和新闻
                links = soup.find_all('a', href=True)
                for link in links[:limit * 2]:
                    title = link.get_text(strip=True)
                    href = link.get('href')
                    
                    if self._is_bluetooth_related(title) and href:
                        full_url = urljoin(url, href)
                        article = {
                            'title': title,
                            'url': full_url,
                            'source': 'Huawei Developer',
                            'source_type': 'manufacturer',
                            'description': self._extract_description(soup, link),
                            'published_date': datetime.now().isoformat(),
                            'keywords': ['蓝牙', 'HarmonyOS', '华为', '鸿蒙']
                        }
                        articles.append(article)
                        
                        if len(articles) >= limit:
                            break
                
        except Exception as e:
            self.logger.error(f"爬取Huawei网站失败: {e}")
            
        return articles
    
    def _crawl_xiaomi_site(self, url: str, limit: int) -> List[Dict]:
        """爬取小米开发者网站"""
        articles = []
        
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找博客文章和技术文档
                content_selectors = [
                    '.blog-item a',
                    '.doc-item a',
                    'a[href*="bluetooth"]'
                ]
                
                for selector in content_selectors:
                    links = soup.select(selector)
                    for link in links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get('href')
                        
                        if self._is_bluetooth_related(title) and href:
                            full_url = urljoin(url, href)
                            article = {
                                'title': title,
                                'url': full_url,
                                'source': 'Xiaomi Developer',
                                'source_type': 'manufacturer',
                                'description': self._extract_description(soup, link),
                                'published_date': datetime.now().isoformat(),
                                'keywords': ['蓝牙', 'MIUI', '小米', 'Android']
                            }
                            articles.append(article)
                            
                            if len(articles) >= limit:
                                break
                
        except Exception as e:
            self.logger.error(f"爬取Xiaomi网站失败: {e}")
            
        return articles
    
    def _crawl_qualcomm_site(self, url: str, limit: int) -> List[Dict]:
        """爬取高通开发者网站"""
        articles = []
        
        try:
            # 高通蓝牙相关页面
            bluetooth_urls = [
                "https://developer.qualcomm.com/hardware/bluetooth",
                "https://developer.qualcomm.com/software/bluetooth",
                url
            ]
            
            for search_url in bluetooth_urls:
                response = self._make_request(search_url)
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 查找技术文档和白皮书
                    content_selectors = [
                        '.resource-item a',
                        '.doc-link',
                        'a[href*="bluetooth"]',
                        'a[href*="connectivity"]'
                    ]
                    
                    for selector in content_selectors:
                        links = soup.select(selector)
                        for link in links[:limit]:
                            title = link.get_text(strip=True)
                            href = link.get('href')
                            
                            if title and href:
                                full_url = urljoin(search_url, href)
                                article = {
                                    'title': title,
                                    'url': full_url,
                                    'source': 'Qualcomm Developer',
                                    'source_type': 'tech_company',
                                    'description': self._extract_description(soup, link),
                                    'published_date': datetime.now().isoformat(),
                                    'keywords': ['蓝牙', 'Qualcomm', '高通', '芯片', 'SoC']
                                }
                                articles.append(article)
                                
                                if len(articles) >= limit:
                                    break
                    
                    if len(articles) >= limit:
                        break
                
        except Exception as e:
            self.logger.error(f"爬取Qualcomm网站失败: {e}")
            
        return articles
    
    def _crawl_bluetooth_org_site(self, url: str, limit: int) -> List[Dict]:
        """爬取蓝牙官方网站"""
        articles = []
        
        try:
            # 蓝牙官方网站的主要页面
            bluetooth_pages = [
                "https://www.bluetooth.com/learn-about-bluetooth/",
                "https://www.bluetooth.com/bluetooth-resources/",
                "https://www.bluetooth.com/specifications/",
                url
            ]
            
            for page_url in bluetooth_pages:
                response = self._make_request(page_url)
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 查找规范、白皮书和学习资源
                    content_selectors = [
                        '.resource-item a',
                        '.spec-item a',
                        '.learn-item a',
                        'a[href*="specification"]',
                        'a[href*="whitepaper"]'
                    ]
                    
                    for selector in content_selectors:
                        links = soup.select(selector)
                        for link in links[:limit]:
                            title = link.get_text(strip=True)
                            href = link.get('href')
                            
                            if title and href:
                                full_url = urljoin(page_url, href)
                                article = {
                                    'title': title,
                                    'url': full_url,
                                    'source': 'Bluetooth.org',
                                    'source_type': 'standard',
                                    'description': self._extract_description(soup, link),
                                    'published_date': datetime.now().isoformat(),
                                    'keywords': ['蓝牙', 'Bluetooth', '标准', '规范', '官方']
                                }
                                articles.append(article)
                                
                                if len(articles) >= limit:
                                    break
                    
                    if len(articles) >= limit:
                        break
                
        except Exception as e:
            self.logger.error(f"爬取Bluetooth.org网站失败: {e}")
            
        return articles
    
    def _crawl_nordic_site(self, url: str, limit: int) -> List[Dict]:
        """爬取Nordic半导体网站"""
        articles = []
        
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Nordic专注于低功耗蓝牙
                content_selectors = [
                    'a[href*="bluetooth"]',
                    'a[href*="ble"]',
                    'a[href*="nrf"]',
                    '.blog-item a',
                    '.resource-item a'
                ]
                
                for selector in content_selectors:
                    links = soup.select(selector)
                    for link in links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get('href')
                        
                        if title and href and ('bluetooth' in title.lower() or 'ble' in title.lower()):
                            full_url = urljoin(url, href)
                            article = {
                                'title': title,
                                'url': full_url,
                                'source': 'Nordic Semiconductor',
                                'source_type': 'tech_company',
                                'description': self._extract_description(soup, link),
                                'published_date': datetime.now().isoformat(),
                                'keywords': ['蓝牙', 'BLE', 'Nordic', '低功耗', 'nRF']
                            }
                            articles.append(article)
                            
                            if len(articles) >= limit:
                                break
                
        except Exception as e:
            self.logger.error(f"爬取Nordic网站失败: {e}")
            
        return articles
    
    def _crawl_espressif_site(self, url: str, limit: int) -> List[Dict]:
        """爬取乐鑫科技网站"""
        articles = []
        
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 乐鑫的ESP32系列支持蓝牙
                content_selectors = [
                    'a[href*="bluetooth"]',
                    'a[href*="esp32"]',
                    'a[href*="esp-idf"]',
                    '.doc-item a',
                    '.blog-item a'
                ]
                
                for selector in content_selectors:
                    links = soup.select(selector)
                    for link in links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get('href')
                        
                        if title and href and ('bluetooth' in title.lower() or 'esp32' in title.lower()):
                            full_url = urljoin(url, href)
                            article = {
                                'title': title,
                                'url': full_url,
                                'source': 'Espressif Systems',
                                'source_type': 'tech_company',
                                'description': self._extract_description(soup, link),
                                'published_date': datetime.now().isoformat(),
                                'keywords': ['蓝牙', 'ESP32', 'Espressif', '乐鑫', 'WiFi']
                            }
                            articles.append(article)
                            
                            if len(articles) >= limit:
                                break
                
        except Exception as e:
            self.logger.error(f"爬取Espressif网站失败: {e}")
            
        return articles
    
    def _crawl_anandtech_site(self, url: str, limit: int) -> List[Dict]:
        """爬取AnandTech技术媒体网站"""
        articles = []
        
        try:
            # AnandTech搜索蓝牙相关文章
            search_url = f"{url}search?q=bluetooth"
            response = self._make_request(search_url)
            
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找搜索结果中的文章
                content_selectors = [
                    '.search-result a',
                    '.article-item a',
                    'a[href*="review"]'
                ]
                
                for selector in content_selectors:
                    links = soup.select(selector)
                    for link in links[:limit]:
                        title = link.get_text(strip=True)
                        href = link.get('href')
                        
                        if title and href and self._is_bluetooth_related(title):
                            full_url = urljoin(url, href)
                            article = {
                                'title': title,
                                'url': full_url,
                                'source': 'AnandTech',
                                'source_type': 'tech_media',
                                'description': self._extract_description(soup, link),
                                'published_date': datetime.now().isoformat(),
                                'keywords': ['蓝牙', 'Bluetooth', '技术评测', '硬件']
                            }
                            articles.append(article)
                            
                            if len(articles) >= limit:
                                break
                
        except Exception as e:
            self.logger.error(f"爬取AnandTech网站失败: {e}")
            
        return articles
    
    def _crawl_generic_site(self, url: str, limit: int) -> List[Dict]:
        """通用网站爬取策略"""
        articles = []
        
        try:
            response = self._make_request(url)
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 通用选择器，查找包含蓝牙关键词的链接
                all_links = soup.find_all('a', href=True)
                
                for link in all_links[:limit * 3]:  # 检查更多链接
                    title = link.get_text(strip=True)
                    href = link.get('href')
                    
                    if self._is_bluetooth_related(title) and href:
                        full_url = urljoin(url, href)
                        domain = urlparse(url).netloc
                        
                        article = {
                            'title': title,
                            'url': full_url,
                            'source': domain,
                            'source_type': 'general',
                            'description': self._extract_description(soup, link),
                            'published_date': datetime.now().isoformat(),
                            'keywords': self._extract_keywords_from_title(title)
                        }
                        articles.append(article)
                        
                        if len(articles) >= limit:
                            break
                
        except Exception as e:
            self.logger.error(f"通用爬取 {url} 失败: {e}")
            
        return articles
    
    def _is_bluetooth_related(self, text: str) -> bool:
        """检查文本是否与蓝牙相关"""
        if not text:
            return False
            
        text_lower = text.lower()
        bluetooth_keywords = [
            'bluetooth', '蓝牙', 'ble', 'br/edr', 'low energy',
            'wireless', '无线', 'connectivity', '连接',
            'pairing', '配对', 'beacon', 'mesh'
        ]
        
        return any(keyword in text_lower for keyword in bluetooth_keywords)
    
    def _extract_description(self, soup: BeautifulSoup, link) -> str:
        """提取文章描述"""
        try:
            # 尝试从链接附近找到描述文本
            parent = link.parent
            if parent:
                # 查找同级或父级元素中的描述
                desc_text = parent.get_text(strip=True)
                if len(desc_text) > len(link.get_text(strip=True)) + 10:
                    return desc_text[:200] + "..." if len(desc_text) > 200 else desc_text
            
            # 如果没有找到，使用标题作为描述
            return link.get_text(strip=True)
            
        except Exception:
            return ""
    
    def _extract_keywords_from_title(self, title: str) -> List[str]:
        """从标题中提取关键词"""
        keywords = ['蓝牙', 'Bluetooth']
        
        title_lower = title.lower()
        additional_keywords = {
            'android': 'Android',
            'ios': 'iOS',
            'wireless': '无线',
            'connectivity': '连接',
            'chip': '芯片',
            'soc': 'SoC',
            'review': '评测',
            'development': '开发',
            'specification': '规范'
        }
        
        for key, value in additional_keywords.items():
            if key in title_lower:
                keywords.append(value)
        
        return keywords