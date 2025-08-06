import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import Config

class Database:
    def __init__(self, db_path: str = Config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建文章表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    summary TEXT,
                    url TEXT UNIQUE,
                    source_type TEXT NOT NULL,
                    source_name TEXT,
                    publish_date TEXT,
                    keywords TEXT,
                    sentiment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建统计表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    total_articles INTEGER DEFAULT 0,
                    news_count INTEGER DEFAULT 0,
                    tech_count INTEGER DEFAULT 0,
                    academic_count INTEGER DEFAULT 0,
                    patent_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建关键词表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT UNIQUE,
                    frequency INTEGER DEFAULT 1,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def insert_article(self, article_data: Dict) -> bool:
        """插入文章数据"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO articles 
                    (title, content, summary, url, source_type, source_name, 
                     publish_date, keywords, sentiment, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article_data.get('title', ''),
                    article_data.get('content', ''),
                    article_data.get('summary', ''),
                    article_data.get('url', ''),
                    article_data.get('source_type', ''),
                    article_data.get('source_name', ''),
                    article_data.get('publish_date', ''),
                    json.dumps(article_data.get('keywords', []), ensure_ascii=False),
                    article_data.get('sentiment', ''),
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"插入文章失败: {e}")
            return False
    
    def get_recent_articles(self, days: int = 7, limit: int = 100) -> List[Dict]:
        """获取最近的文章"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM articles 
                WHERE created_at >= datetime('now', '-{} days')
                ORDER BY created_at DESC
                LIMIT ?
            '''.format(days), (limit,))
            
            articles = []
            for row in cursor.fetchall():
                article = dict(row)
                article['keywords'] = json.loads(article['keywords']) if article['keywords'] else []
                articles.append(article)
            
            return articles
    
    def get_articles_by_source_type(self, source_type: str, limit: int = 50) -> List[Dict]:
        """根据来源类型获取文章"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM articles 
                WHERE source_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (source_type, limit))
            
            articles = []
            for row in cursor.fetchall():
                article = dict(row)
                article['keywords'] = json.loads(article['keywords']) if article['keywords'] else []
                articles.append(article)
            
            return articles
    
    def update_statistics(self, date: str, stats: Dict):
        """更新统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO statistics 
                (date, total_articles, news_count, tech_count, academic_count, patent_count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                date,
                stats.get('total_articles', 0),
                stats.get('news_count', 0),
                stats.get('tech_count', 0),
                stats.get('academic_count', 0),
                stats.get('patent_count', 0)
            ))
            
            conn.commit()
    
    def get_statistics(self, days: int = 30) -> List[Dict]:
        """获取统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM statistics 
                WHERE date >= date('now', '-{} days')
                ORDER BY date DESC
            '''.format(days))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def update_keyword_frequency(self, keywords: List[str]):
        """更新关键词频率"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for keyword in keywords:
                cursor.execute('''
                    INSERT OR REPLACE INTO keywords (keyword, frequency, last_updated)
                    VALUES (?, COALESCE((SELECT frequency + 1 FROM keywords WHERE keyword = ?), 1), ?)
                ''', (keyword, keyword, datetime.now().isoformat()))
            
            conn.commit()
    
    def get_top_keywords(self, limit: int = 20) -> List[Dict]:
        """获取热门关键词"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM keywords 
                ORDER BY frequency DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def cleanup_old_data(self, days: int = Config.DATA_RETENTION_DAYS):
        """清理旧数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 删除旧文章
            cursor.execute('''
                DELETE FROM articles 
                WHERE created_at < datetime('now', '-{} days')
            '''.format(days))
            
            # 删除旧统计
            cursor.execute('''
                DELETE FROM statistics 
                WHERE date < date('now', '-{} days')
            '''.format(days))
            
            conn.commit()
    
    def get_article_count_by_date(self, days: int = 7) -> List[Dict]:
        """获取每日文章数量"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM articles 
                WHERE created_at >= datetime('now', '-{} days')
                GROUP BY DATE(created_at)
                ORDER BY date DESC
            '''.format(days))
            
            return [dict(row) for row in cursor.fetchall()] 