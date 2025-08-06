# 蓝牙技术文章聚合平台

一个运行在国外服务器上的自动化程序，每天定时抓取全网关于"蓝牙"的文章，包括新闻、技术文章、论坛文章、论文、专利等，并对搜索结果进行归纳总结，通过网页进行呈现。

## 功能特性

### 🔍 多源文章抓取
- **新闻网站**: 抓取各大科技新闻网站的最新蓝牙相关新闻
- **技术博客**: 收集技术博客和开发网站的蓝牙技术文章
- **学术论文**: 爬取arXiv、IEEE等学术平台的蓝牙相关论文
- **专利信息**: 获取Google Patents等专利数据库的蓝牙专利

### 🤖 AI智能总结
- 使用OpenAI GPT模型生成每日文章总结
- 自动识别热点话题和趋势
- 关键词提取和情感分析
- 智能分类和标签化

### 📊 数据可视化
- 实时统计图表展示
- 来源分布分析
- 关键词热度排行
- 每日趋势分析

### ⏰ 自动化运行
- 每天早上8点自动执行爬取任务
- 定时清理旧数据
- 自动更新统计信息

## 系统架构

```
├── 爬虫模块 (crawlers/)
│   ├── base_crawler.py      # 基础爬虫类
│   ├── news_crawler.py      # 新闻爬虫
│   ├── tech_crawler.py      # 技术文章爬虫
│   └── academic_crawler.py  # 学术论文爬虫
├── 数据处理模块
│   ├── database.py          # 数据库操作
│   └── summarizer.py        # AI总结生成
├── 定时任务模块
│   └── scheduler.py         # 任务调度器
├── Web界面模块
│   ├── web_app.py           # Flask应用
│   └── templates/           # HTML模板
└── 配置文件
    ├── config.py            # 系统配置
    └── requirements.txt     # 依赖包
```

## 安装部署

### 1. 环境要求
- Python 3.8+
- SQLite3
- 国外服务器（推荐美国、欧洲等地区）

### 2. 安装依赖
```bash
# 克隆项目
git clone <repository_url>
cd bluetooth-articles-aggregator

# 安装Python依赖
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp env_example.txt .env

# 编辑配置文件
nano .env
```

主要配置项：
- `OPENAI_API_KEY`: OpenAI API密钥（用于AI总结功能）
- `OPENAI_BASE_URL`: OpenAI API基础URL（默认https://api.oaipro.com/v1）
- `HOST`: Web服务器监听地址（建议0.0.0.0）
- `PORT`: Web服务器端口（默认5000）
- `SCHEDULE_TIME`: 定时任务执行时间（默认08:00）

### 4. 启动服务
```bash
# 启动主程序
python main.py
```

程序启动后会：
- 自动创建数据库和表结构
- 启动定时任务调度器
- 启动Web服务器
- 开始监听指定端口

### 5. 访问Web界面
打开浏览器访问：`http://your_server_ip:5000`

## 使用说明

### Web界面功能
- **首页**: 展示最新文章、统计数据、AI总结
- **文章列表**: 浏览所有文章，支持筛选和搜索
- **统计分析**: 查看详细的统计图表和数据

### 定时任务
- 每天早上8点自动执行爬取任务
- 自动生成每日总结报告
- 更新统计数据和关键词分析

### 手动执行
```bash
# 手动执行一次爬取任务
python -c "from scheduler import CrawlerScheduler; CrawlerScheduler().run_manual_crawl()"
```

## 数据来源

### 新闻网站
- CNBeta
- IT之家
- Engadget
- The Verge
- TechCrunch
- Wired

### 技术博客
- InfoQ
- Medium
- Dev.to
- GitHub
- Stack Overflow

### 学术平台
- arXiv
- IEEE Xplore
- Google Patents

## 技术栈

- **后端**: Python 3.8+, Flask
- **数据库**: SQLite3
- **爬虫**: Requests, BeautifulSoup, Selenium
- **AI**: OpenAI GPT API
- **前端**: Bootstrap 5, Chart.js
- **定时任务**: APScheduler

## 注意事项

1. **合规性**: 请确保遵守目标网站的robots.txt和使用条款
2. **频率限制**: 程序已内置请求延迟，避免对目标网站造成压力
3. **数据存储**: 定期备份数据库文件
4. **API限制**: OpenAI API有使用限制，请注意配额管理

## 故障排除

### 常见问题

1. **爬取失败**
   - 检查网络连接
   - 确认目标网站可访问
   - 查看日志文件

2. **AI总结失败**
   - 检查OpenAI API密钥是否正确
   - 确认API配额是否充足

3. **Web界面无法访问**
   - 检查防火墙设置
   - 确认端口是否开放
   - 查看服务器日志

### 日志文件
- `bluetooth_aggregator.log`: 主程序日志
- `crawler.log`: 爬虫模块日志

## 许可证

本项目仅供学习和研究使用，请勿用于商业用途。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题或建议，请通过GitHub Issues联系。 