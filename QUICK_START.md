# 快速开始指南

## 🚀 立即开始检索文章

### 方法1：立即检索文章（推荐）
```bash
# 在服务器上运行
python3 run_crawler.py
```

这个命令会：
- 立即开始爬取蓝牙相关文章
- 包括新闻、技术文章、学术论文、专利
- **新增**: 手机厂商官方网站 (苹果、三星、华为、小米等)
- **新增**: 技术公司网站 (高通、联发科、Nordic、乐鑫等)
- 显示实时进度和统计信息
- 完成后显示结果摘要

### 方法2：测试爬虫功能
```bash
# 快速测试，只爬取少量文章
python3 test_crawler.py
```

这个命令会：
- 爬取少量文章进行测试
- 验证所有爬虫功能是否正常
- **包含**: 厂商网站和技术公司测试
- 快速查看结果

### 方法2.1：专门测试厂商爬虫
```bash
# 专门测试手机厂商和技术公司爬虫
python3 test_manufacturer_crawler.py
```

这个命令会：
- 专门测试新增的厂商网站爬虫
- 测试苹果、三星、华为等厂商网站
- 测试高通、Nordic、乐鑫等技术公司
- 显示详细的爬取结果

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

### 新增数据源详细列表

#### 📱 手机厂商官方网站 (13个厂商)
- **苹果**: 开发者文档、技术新闻
- **三星**: 开发者平台、研究报告
- **华为**: 开发者社区、技术博客
- **小米**: 开发者平台、官方博客
- **OPPO**: 开放平台、技术资讯
- **vivo**: 开发者中心、产品信息
- **一加**: 官方网站、社区论坛
- **谷歌**: Android开发者、源码项目
- **索尼**: 开发者资源、产品资讯
- **LG**: 技术支持、全球资讯
- **摩托罗拉**: 开发者平台、产品信息

#### 🏢 技术公司网站 (25+个公司)

**芯片厂商**:
- 高通 (Qualcomm) - 蓝牙芯片领导者
- 联发科 (MediaTek) - 移动芯片方案
- Intel - 计算平台蓝牙技术
- AMD - 处理器集成方案
- NVIDIA - AI和连接技术
- ARM - 处理器架构
- 德州仪器 (TI) - 嵌入式方案
- 意法半导体 (ST) - MCU和传感器
- 恩智浦 (NXP) - 汽车和IoT
- 英飞凌 (Infineon) - 功率和安全
- Nordic - 低功耗蓝牙专家
- Dialog - 低功耗连接方案
- 乐鑫 (Espressif) - ESP32 WiFi+蓝牙

**软件和平台**:
- 微软 - Windows蓝牙支持
- 亚马逊 - AWS IoT和Alexa
- Facebook/Meta - AR/VR连接
- 云服务平台技术文档

**标准组织和开源**:
- 蓝牙技术联盟 (Bluetooth.org) - 官方标准
- Linux内核 - 开源蓝牙栈
- Eclipse IoT - 物联网项目
- Apache项目 - 开源技术

**技术媒体**:
- AnandTech - 硬件深度评测
- Ars Technica - 技术新闻分析
- IEEE Spectrum - 工程技术期刊
- EDN - 电子设计网络
- Embedded - 嵌入式系统
- Hackaday - 创客技术分享

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