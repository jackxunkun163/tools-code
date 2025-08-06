# 快速开始指南

## 🚀 立即开始检索文章

### 方法1：立即检索文章（推荐）
```bash
# 在服务器上运行
python3 run_crawler.py
```

这个命令会：
- 立即开始爬取蓝牙相关文章
- 显示实时进度和统计信息
- 完成后显示结果摘要

### 方法2：测试爬虫功能
```bash
# 快速测试，只爬取少量文章
python3 test_crawler.py
```

这个命令会：
- 爬取少量文章进行测试
- 验证爬虫功能是否正常
- 快速查看结果

### 方法3：快速启动（爬虫+Web界面）
```bash
# 后台爬虫 + Web服务器
python3 quick_start.py
```

这个命令会：
- 在后台执行爬虫任务
- 同时启动Web服务器
- 可以立即查看结果

### 方法4：完整启动
```bash
# 定时爬虫 + Web服务器
python3 main.py
```

这个命令会：
- 启动定时任务（每天早上8点爬取）
- 启动Web服务器
- 适合长期运行

## 📊 查看结果

启动Web服务器后，访问：
- **主页**: http://localhost:5000
- **文章列表**: http://localhost:5000/articles
- **统计分析**: http://localhost:5000/statistics

## 🔧 配置说明

### 环境变量配置
编辑 `.env` 文件：
```bash
# OpenAI API配置
OPENAI_API_KEY=sk-DDfoY7cmJeVDa3vJHSCNtMmGMHjBQ9Yt4PFo9LXmzTseCkCFECFn
OPENAI_BASE_URL=https://api.oaipro.com/v1

# Web服务器配置
HOST=0.0.0.0
PORT=5000
DEBUG=False

# 定时任务配置
SCHEDULE_TIME=08:00

# 数据保留天数
DATA_RETENTION_DAYS=30
```

### 爬虫配置
在 `config.py` 中可以修改：
- 搜索关键词
- 目标网站
- 爬取频率
- 并发数量

## 📈 监控和日志

### 查看日志
```bash
# 查看爬虫日志
tail -f manual_crawler.log

# 查看系统日志
tail -f bluetooth_aggregator.log
```

### 数据库操作
```bash
# 查看数据库
sqlite3 bluetooth_articles.db

# 备份数据库
cp bluetooth_articles.db backup/bluetooth_articles_$(date +%Y%m%d).db
```

## 🛠️ 故障排除

### 常见问题

1. **爬虫无法启动**
   ```bash
   # 检查依赖
   pip3 install -r requirements.txt
   
   # 检查网络连接
   curl -I https://www.google.com
   ```

2. **Web界面无法访问**
   ```bash
   # 检查端口
   netstat -tlnp | grep 5000
   
   # 检查防火墙
   sudo ufw status
   ```

3. **API调用失败**
   ```bash
   # 检查API密钥
   python3 -c "from config import Config; print(Config.OPENAI_API_KEY[:10])"
   ```

### 性能优化

1. **增加并发数**
   ```python
   # 修改 config.py
   MAX_CONCURRENT_REQUESTS = 10
   ```

2. **调整请求延迟**
   ```python
   # 修改 config.py
   REQUEST_DELAY = 0.5
   ```

## 📞 获取帮助

如果遇到问题：
1. 查看日志文件
2. 运行测试脚本
3. 检查配置文件
4. 查看系统资源使用情况

---

**推荐使用顺序**：
1. 先运行 `python3 test_crawler.py` 测试功能
2. 再运行 `python3 run_crawler.py` 开始检索
3. 最后运行 `python3 main.py` 启动完整服务 