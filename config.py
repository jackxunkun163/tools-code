import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 数据库配置
    DATABASE_PATH = 'bluetooth_articles.db'
    
    # 定时任务配置
    SCHEDULE_TIME = "06:00"  # 每天早上8点执行
    
    # 搜索关键词
    SEARCH_KEYWORDS = [
        "蓝牙", "Bluetooth", "br/edr", "蓝牙技术", "蓝牙协议",
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
    
    # 手机厂商官方技术网站
    PHONE_MANUFACTURER_SOURCES = [
        # 苹果
        "https://developer.apple.com/",
        "https://developer.apple.com/documentation/",
        "https://developer.apple.com/news/",
        
        # 三星
        "https://developer.samsung.com/",
        "https://news.samsung.com/global/",
        "https://research.samsung.com/",
        
        # 华为
        "https://developer.huawei.com/",
        "https://www.huawei.com/cn/corporate-information/",
        "https://www.hisilicon.com/",
        
        # 小米
        "https://dev.mi.com/",
        "https://blog.mi.com/",
        "https://www.mi.com/global/",
        
        # OPPO
        "https://open.oppomobile.com/",
        "https://www.oppo.com/cn/about-us/news/",
        
        # vivo
        "https://dev.vivo.com.cn/",
        "https://www.vivo.com/",
        
        # 一加
        "https://www.oneplus.com/",
        "https://forums.oneplus.com/",
        
        # 谷歌
        "https://developers.google.com/",
        "https://android-developers.googleblog.com/",
        "https://source.android.com/",
        
        # 索尼
        "https://developer.sony.com/",
        "https://www.sony.com/electronics/",
        
        # LG
        "https://gscs.lge.com/",
        "https://www.lg.com/global/",
        
        # 摩托罗拉
        "https://developer.motorola.com/",
        "https://www.motorola.com/"
    ]
    
    # 主要技术公司官方网站
    TECH_COMPANY_SOURCES = [
        # 芯片厂商
        "https://www.qualcomm.com/",
        "https://developer.qualcomm.com/",
        "https://www.broadcom.com/",
        "https://www.mediatek.com/",
        "https://www.intel.com/",
        "https://www.amd.com/",
        "https://www.nvidia.com/",
        "https://www.arm.com/",
        "https://www.cypress.com/",
        "https://www.ti.com/",
        "https://www.st.com/",
        "https://www.nxp.com/",
        "https://www.microchip.com/",
        "https://www.infineon.com/",
        "https://www.nordic.com/",
        "https://www.dialog-semiconductor.com/",
        "https://www.espressif.com/",
        
        # 软件和平台公司
        "https://developers.google.com/",
        "https://developer.apple.com/",
        "https://docs.microsoft.com/",
        "https://developer.microsoft.com/",
        "https://aws.amazon.com/",
        "https://developer.amazon.com/",
        "https://developers.facebook.com/",
        "https://developer.twitter.com/",
        "https://developer.linkedin.com/",
        "https://cloud.google.com/",
        "https://azure.microsoft.com/",
        
        # 开源社区和标准组织
        "https://www.bluetooth.com/",
        "https://www.bluetooth.org/",
        "https://www.kernel.org/",
        "https://git.kernel.org/",
        "https://lwn.net/",
        "https://www.linuxfoundation.org/",
        "https://www.eclipse.org/",
        "https://apache.org/",
        
        # 技术媒体和博客
        "https://www.anandtech.com/",
        "https://arstechnica.com/",
        "https://spectrum.ieee.org/",
        "https://www.edn.com/",
        "https://www.embedded.com/",
        "https://hackaday.com/",
        "https://www.electronicsweekly.com/"
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