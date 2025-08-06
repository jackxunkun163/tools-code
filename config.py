import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 数据库配置
    DATABASE_PATH = 'bluetooth_articles.db'
    
    # 定时任务配置
    SCHEDULE_TIME = "08:00"  # 每天早上8点执行
    
    # 搜索关键词
    SEARCH_KEYWORDS = [
        "蓝牙", "Bluetooth", "BLE", "蓝牙技术", "蓝牙协议",
        "蓝牙开发", "蓝牙应用", "蓝牙芯片", "蓝牙耳机",
        "蓝牙音箱", "蓝牙连接", "蓝牙标准"
    ]
    
    # 新闻源配置
    NEWS_SOURCES = [
        "https://www.cnbeta.com.tw/",
        "https://www.ithome.com/",
        "https://www.engadget.com/",
        "https://www.theverge.com/",
        "https://techcrunch.com/",
        "https://www.wired.com/"
    ]
    
    # 技术文章源
    TECH_SOURCES = [
        "https://www.infoq.com/",
        "https://medium.com/",
        "https://dev.to/",
        "https://stackoverflow.com/",
        "https://github.com/"
    ]
    
    # 学术论文源
    ACADEMIC_SOURCES = [
        "arxiv.org",
        "ieee.org",
        "acm.org",
        "springer.com",
        "sciencedirect.com"
    ]
    
    # 专利搜索源
    PATENT_SOURCES = [
        "patents.google.com",
        "uspto.gov",
        "epo.org"
    ]
    
    # OpenAI配置
    OPENAI_API_KEY = "sk-DDfoY7cmJeVDa3vJHSCNtMmGMHjBQ9Yt4PFo9LXmzTseCkCFECFn"
    OPENAI_BASE_URL = "https://api.oaipro.com/v1"
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Web服务器配置
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = False
    
    # 数据保留天数
    DATA_RETENTION_DAYS = 30
    
    # 用户代理
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # 请求延迟（秒）
    REQUEST_DELAY = 1
    
    # 最大并发数
    MAX_CONCURRENT_REQUESTS = 5 