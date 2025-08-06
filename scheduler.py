import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from database import Database
from crawlers.news_crawler import NewsCrawler
from crawlers.tech_crawler import TechCrawler
from crawlers.academic_crawler import AcademicCrawler
from crawlers.manufacturer_crawler import ManufacturerCrawler
from summarizer import Summarizer
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

class CrawlerScheduler:
    def __init__(self):
        self.db = Database()
        self.summarizer = Summarizer()
        self.is_running = False
        
    def start_scheduler(self):
        """启动定时任务调度器"""
        logging.info("启动定时任务调度器...")
        
        # 设置每天早上8点执行爬取任务
        schedule.every().day.at(Config.SCHEDULE_TIME).do(self.run_daily_crawl)
        
        # 设置每天凌晨2点清理旧数据
        schedule.every().day.at("02:00").do(self.cleanup_old_data)
        
        self.is_running = True
        
        # 启动调度器线程
        scheduler_thread = threading.Thread(target=self._run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        logging.info(f"定时任务调度器已启动，将在每天 {Config.SCHEDULE_TIME} 执行爬取任务")
        
        return scheduler_thread
    
    def _run_scheduler(self):
        """运行调度器循环"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def run_daily_crawl(self):
        """执行每日爬取任务"""
        try:
            logging.info("开始执行每日爬取任务...")
            start_time = datetime.now()
            
            # 执行爬取任务
            all_articles = self._crawl_all_sources()
            
            # 生成总结
            summary = self.summarizer.generate_summary(all_articles)
            
            # 保存到数据库
            self._save_results(all_articles, summary)
            
            # 更新统计数据
            self._update_statistics(all_articles)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logging.info(f"每日爬取任务完成，耗时: {duration}")
            logging.info(f"共收集到 {len(all_articles)} 篇文章")
            
        except Exception as e:
            logging.error(f"每日爬取任务失败: {e}")
    
    def _crawl_all_sources(self) -> List[Dict]:
        """爬取所有来源的文章"""
        all_articles = []
        
        # 爬取新闻
        try:
            logging.info("开始爬取新闻...")
            news_crawler = NewsCrawler()
            news_articles = news_crawler.crawl(Config.SEARCH_KEYWORDS)
            all_articles.extend(news_articles)
            logging.info(f"新闻爬取完成，获取 {len(news_articles)} 篇文章")
        except Exception as e:
            logging.error(f"新闻爬取失败: {e}")
        
        # 爬取技术文章
        try:
            logging.info("开始爬取技术文章...")
            tech_crawler = TechCrawler()
            tech_articles = tech_crawler.crawl(Config.SEARCH_KEYWORDS)
            all_articles.extend(tech_articles)
            logging.info(f"技术文章爬取完成，获取 {len(tech_articles)} 篇文章")
        except Exception as e:
            logging.error(f"技术文章爬取失败: {e}")
        
        # 爬取学术论文和专利
        try:
            logging.info("开始爬取学术论文和专利...")
            academic_crawler = AcademicCrawler()
            academic_articles = academic_crawler.crawl(Config.SEARCH_KEYWORDS)
            all_articles.extend(academic_articles)
            logging.info(f"学术论文和专利爬取完成，获取 {len(academic_articles)} 篇文章")
        except Exception as e:
            logging.error(f"学术论文和专利爬取失败: {e}")
        
        # 爬取手机厂商和技术公司网站
        try:
            logging.info("开始爬取手机厂商和技术公司网站...")
            manufacturer_crawler = ManufacturerCrawler()
            
            # 爬取手机厂商网站
            manufacturer_articles = manufacturer_crawler.crawl_manufacturer_sites(limit=30)
            all_articles.extend(manufacturer_articles)
            logging.info(f"手机厂商网站爬取完成，获取 {len(manufacturer_articles)} 篇文章")
            
            # 爬取技术公司网站
            tech_company_articles = manufacturer_crawler.crawl_tech_company_sites(limit=50)
            all_articles.extend(tech_company_articles)
            logging.info(f"技术公司网站爬取完成，获取 {len(tech_company_articles)} 篇文章")
            
        except Exception as e:
            logging.error(f"手机厂商和技术公司网站爬取失败: {e}")
        
        return all_articles
    
    def _save_results(self, articles: List[Dict], summary: Dict):
        """保存结果到数据库"""
        try:
            # 保存文章
            saved_count = 0
            for article in articles:
                if self.db.insert_article(article):
                    saved_count += 1
            
            logging.info(f"成功保存 {saved_count} 篇文章到数据库")
            
            # 保存总结（可以扩展数据库来存储总结）
            logging.info("总结生成完成")
            
        except Exception as e:
            logging.error(f"保存结果失败: {e}")
    
    def _update_statistics(self, articles: List[Dict]):
        """更新统计数据"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # 按来源类型统计
            stats = {
                'total_articles': len(articles),
                'news_count': len([a for a in articles if a.get('source_type') == 'news']),
                'tech_count': len([a for a in articles if a.get('source_type') == 'tech']),
                'academic_count': len([a for a in articles if a.get('source_type') == 'academic'])
            }
            
            self.db.update_statistics(today, stats)
            
            # 更新关键词频率
            all_keywords = []
            for article in articles:
                all_keywords.extend(article.get('keywords', []))
            
            if all_keywords:
                self.db.update_keyword_frequency(all_keywords)
            
            logging.info(f"统计数据更新完成: {stats}")
            
        except Exception as e:
            logging.error(f"更新统计数据失败: {e}")
    
    def cleanup_old_data(self):
        """清理旧数据"""
        try:
            logging.info("开始清理旧数据...")
            self.db.cleanup_old_data(Config.DATA_RETENTION_DAYS)
            logging.info("旧数据清理完成")
        except Exception as e:
            logging.error(f"清理旧数据失败: {e}")
    
    def run_manual_crawl(self):
        """手动执行爬取任务"""
        logging.info("手动执行爬取任务...")
        self.run_daily_crawl()
    
    def stop_scheduler(self):
        """停止调度器"""
        self.is_running = False
        logging.info("定时任务调度器已停止")
    
    def get_next_run_time(self) -> str:
        """获取下次运行时间"""
        next_run = schedule.next_run()
        if next_run:
            return next_run.strftime('%Y-%m-%d %H:%M:%S')
        return "未设置"

if __name__ == "__main__":
    # 测试调度器
    scheduler = CrawlerScheduler()
    
    # 启动调度器
    scheduler_thread = scheduler.start_scheduler()
    
    try:
        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("正在停止调度器...")
        scheduler.stop_scheduler()
        print("调度器已停止") 