from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import Database
from summarizer import Summarizer
from datetime import datetime, timedelta
import json
import logging
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bluetooth_articles_secret_key'

# 初始化数据库和总结器
db = Database()
summarizer = Summarizer()

# 配置日志
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    """主页"""
    try:
        # 获取最近7天的文章
        recent_articles = db.get_recent_articles(days=7, limit=50)
        
        # 获取统计数据
        stats = db.get_statistics(days=7)
        
        # 获取热门关键词
        top_keywords = db.get_top_keywords(limit=15)
        
        # 获取每日文章数量
        daily_counts = db.get_article_count_by_date(days=7)
        
        # 生成今日总结
        today_articles = db.get_recent_articles(days=1, limit=100)
        if today_articles:
            summary = summarizer.generate_summary(today_articles)
        else:
            summary = {
                'daily_summary': '今日暂无新文章',
                'keyword_analysis': {'chinese_keywords': [], 'english_keywords': {}},
                'trend_analysis': {'source_types': {}, 'keyword_trends': {}},
                'hot_topics': [],
                'total_articles': 0,
                'source_distribution': {}
            }
        
        return render_template('index.html',
                             articles=recent_articles[:10],
                             stats=stats,
                             top_keywords=top_keywords,
                             daily_counts=daily_counts,
                             summary=summary)
    except Exception as e:
        logging.error(f"主页加载失败: {e}")
        return render_template('error.html', error=str(e))

@app.route('/articles')
def articles():
    """文章列表页面"""
    try:
        page = request.args.get('page', 1, type=int)
        source_type = request.args.get('source_type', '')
        days = request.args.get('days', 7, type=int)
        
        # 获取文章
        if source_type:
            articles = db.get_articles_by_source_type(source_type, limit=100)
        else:
            articles = db.get_recent_articles(days=days, limit=100)
        
        # 分页
        per_page = 20
        start = (page - 1) * per_page
        end = start + per_page
        paginated_articles = articles[start:end]
        
        total_pages = (len(articles) + per_page - 1) // per_page
        
        return render_template('articles.html',
                             articles=paginated_articles,
                             page=page,
                             total_pages=total_pages,
                             source_type=source_type,
                             days=days)
    except Exception as e:
        logging.error(f"文章列表页面加载失败: {e}")
        return render_template('error.html', error=str(e))

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    """文章详情页面"""
    try:
        # 这里需要扩展数据库方法来获取单篇文章
        # 暂时返回错误页面
        return render_template('error.html', error="文章详情功能开发中")
    except Exception as e:
        logging.error(f"文章详情页面加载失败: {e}")
        return render_template('error.html', error=str(e))

@app.route('/statistics')
def statistics():
    """统计页面"""
    try:
        days = request.args.get('days', 30, type=int)
        
        # 获取统计数据
        stats = db.get_statistics(days=days)
        
        # 获取热门关键词
        top_keywords = db.get_top_keywords(limit=20)
        
        # 获取每日文章数量
        daily_counts = db.get_article_count_by_date(days=days)
        
        # 按来源类型统计
        source_stats = {}
        for stat in stats:
            source_stats['news'] = source_stats.get('news', 0) + stat.get('news_count', 0)
            source_stats['tech'] = source_stats.get('tech', 0) + stat.get('tech_count', 0)
            source_stats['academic'] = source_stats.get('academic', 0) + stat.get('academic_count', 0)
        
        return render_template('statistics.html',
                             stats=stats,
                             top_keywords=top_keywords,
                             daily_counts=daily_counts,
                             source_stats=source_stats,
                             days=days)
    except Exception as e:
        logging.error(f"统计页面加载失败: {e}")
        return render_template('error.html', error=str(e))

@app.route('/api/articles')
def api_articles():
    """API: 获取文章列表"""
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 50, type=int)
        source_type = request.args.get('source_type', '')
        
        if source_type:
            articles = db.get_articles_by_source_type(source_type, limit=limit)
        else:
            articles = db.get_recent_articles(days=days, limit=limit)
        
        return jsonify({
            'success': True,
            'data': articles,
            'total': len(articles)
        })
    except Exception as e:
        logging.error(f"API获取文章失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics')
def api_statistics():
    """API: 获取统计数据"""
    try:
        days = request.args.get('days', 30, type=int)
        stats = db.get_statistics(days=days)
        top_keywords = db.get_top_keywords(limit=20)
        daily_counts = db.get_article_count_by_date(days=days)
        
        return jsonify({
            'success': True,
            'data': {
                'stats': stats,
                'top_keywords': top_keywords,
                'daily_counts': daily_counts
            }
        })
    except Exception as e:
        logging.error(f"API获取统计数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summary')
def api_summary():
    """API: 获取总结"""
    try:
        days = request.args.get('days', 1, type=int)
        articles = db.get_recent_articles(days=days, limit=100)
        
        if articles:
            summary = summarizer.generate_summary(articles)
        else:
            summary = {
                'daily_summary': '暂无文章',
                'keyword_analysis': {'chinese_keywords': [], 'english_keywords': {}},
                'trend_analysis': {'source_types': {}, 'keyword_trends': {}},
                'hot_topics': [],
                'total_articles': 0,
                'source_distribution': {}
            }
        
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logging.error(f"API获取总结失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/search')
def search():
    """搜索页面"""
    try:
        query = request.args.get('q', '')
        if not query:
            return redirect(url_for('articles'))
        
        # 这里需要实现搜索功能
        # 暂时重定向到文章列表
        return redirect(url_for('articles'))
    except Exception as e:
        logging.error(f"搜索页面加载失败: {e}")
        return render_template('error.html', error=str(e))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="服务器内部错误"), 500

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG) 