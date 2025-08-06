# 部署指南

本文档详细说明如何在国外服务器上部署蓝牙技术文章聚合平台。

## 服务器要求

### 硬件要求
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 20GB以上可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **Python**: 3.8+
- **数据库**: SQLite3 (内置)
- **Web服务器**: Nginx (推荐)

## 部署步骤

### 1. 服务器准备

#### 更新系统
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

#### 安装Python和依赖
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv git curl -y

# CentOS/RHEL
sudo yum install python3 python3-pip git curl -y
```

### 2. 项目部署

#### 克隆项目
```bash
cd /opt
sudo git clone <your-repository-url> bluetooth-aggregator
sudo chown -R $USER:$USER bluetooth-aggregator
cd bluetooth-aggregator
```

#### 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 配置环境

#### 创建环境变量文件
```bash
cp env_example.txt .env
nano .env
```

配置以下关键参数：
```bash
# OpenAI API配置
OPENAI_API_KEY=your_actual_openai_api_key_here
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

#### 设置权限
```bash
chmod +x start.sh
chmod +x test_system.py
```

### 4. 测试系统

#### 运行系统测试
```bash
source venv/bin/activate
python test_system.py
```

确保所有测试都通过。

### 5. 配置Nginx (推荐)

#### 安装Nginx
```bash
# Ubuntu/Debian
sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y
```

#### 创建Nginx配置
```bash
sudo nano /etc/nginx/sites-available/bluetooth-aggregator
```

添加以下配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/bluetooth-aggregator/static;
    }
}
```

#### 启用站点
```bash
sudo ln -s /etc/nginx/sites-available/bluetooth-aggregator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. 配置防火墙

#### Ubuntu/Debian (UFW)
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

#### CentOS/RHEL (Firewalld)
```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 7. 配置系统服务

#### 创建systemd服务文件
```bash
sudo nano /etc/systemd/system/bluetooth-aggregator.service
```

使用以下配置（需要修改路径）：
```ini
[Unit]
Description=蓝牙技术文章聚合平台
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/bluetooth-aggregator
Environment=PATH=/opt/bluetooth-aggregator/venv/bin
ExecStart=/opt/bluetooth-aggregator/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### 启用服务
```bash
sudo systemctl daemon-reload
sudo systemctl enable bluetooth-aggregator
sudo systemctl start bluetooth-aggregator
sudo systemctl status bluetooth-aggregator
```

### 8. 配置SSL (可选但推荐)

#### 安装Certbot
```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx -y

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx -y
```

#### 获取SSL证书
```bash
sudo certbot --nginx -d your-domain.com
```

### 9. 监控和日志

#### 查看服务状态
```bash
sudo systemctl status bluetooth-aggregator
sudo journalctl -u bluetooth-aggregator -f
```

#### 查看应用日志
```bash
tail -f bluetooth_aggregator.log
tail -f crawler.log
```

## 维护操作

### 更新代码
```bash
cd /opt/bluetooth-aggregator
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart bluetooth-aggregator
```

### 备份数据
```bash
# 备份数据库
cp bluetooth_articles.db backup/bluetooth_articles_$(date +%Y%m%d).db

# 备份日志
tar -czf backup/logs_$(date +%Y%m%d).tar.gz *.log
```

### 清理旧数据
```bash
# 手动清理旧数据
source venv/bin/activate
python -c "from database import Database; Database().cleanup_old_data(30)"
```

## 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   sudo systemctl status bluetooth-aggregator
   sudo journalctl -u bluetooth-aggregator -n 50
   ```

2. **Web界面无法访问**
   ```bash
   # 检查端口是否监听
   netstat -tlnp | grep 5000
   
   # 检查防火墙
   sudo ufw status
   ```

3. **爬虫功能异常**
   ```bash
   # 检查网络连接
   curl -I https://www.google.com
   
   # 查看爬虫日志
   tail -f crawler.log
   ```

4. **数据库问题**
   ```bash
   # 检查数据库文件
   ls -la bluetooth_articles.db
   
   # 修复数据库
   sqlite3 bluetooth_articles.db "VACUUM;"
   ```

### 性能优化

1. **增加并发数**
   ```bash
   # 修改config.py中的MAX_CONCURRENT_REQUESTS
   MAX_CONCURRENT_REQUESTS = 10
   ```

2. **调整请求延迟**
   ```bash
   # 修改config.py中的REQUEST_DELAY
   REQUEST_DELAY = 0.5
   ```

3. **优化数据库**
   ```bash
   # 定期优化数据库
   sqlite3 bluetooth_articles.db "ANALYZE; VACUUM;"
   ```

## 安全建议

1. **定期更新系统和依赖**
2. **使用强密码和SSH密钥**
3. **配置防火墙规则**
4. **启用SSL/TLS加密**
5. **定期备份数据**
6. **监控系统资源使用**

## 监控脚本

创建一个简单的监控脚本：
```bash
#!/bin/bash
# monitor.sh

if ! systemctl is-active --quiet bluetooth-aggregator; then
    echo "服务已停止，正在重启..."
    systemctl restart bluetooth-aggregator
    echo "重启完成: $(date)" >> /var/log/bluetooth-monitor.log
fi
```

添加到crontab：
```bash
# 每5分钟检查一次
*/5 * * * * /opt/bluetooth-aggregator/monitor.sh
```

## 联系支持

如果遇到问题，请：
1. 查看日志文件
2. 运行测试脚本
3. 检查系统资源
4. 提交Issue到GitHub 