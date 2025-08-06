import openai
from typing import List, Dict
import jieba
import jieba.analyse
from collections import Counter
import re
from config import Config

class Summarizer:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
    
    def generate_summary(self, articles: List[Dict]) -> Dict:
        """为文章列表生成总结"""
        if not articles:
            return {}
        
        print("开始生成文章总结...")
        
        # 生成每日总结
        daily_summary = self._generate_daily_summary(articles)
        
        # 生成关键词分析
        keyword_analysis = self._analyze_keywords(articles)
        
        # 生成趋势分析
        trend_analysis = self._analyze_trends(articles)
        
        # 生成热点话题
        hot_topics = self._identify_hot_topics(articles)
        
        return {
            'daily_summary': daily_summary,
            'keyword_analysis': keyword_analysis,
            'trend_analysis': trend_analysis,
            'hot_topics': hot_topics,
            'total_articles': len(articles),
            'source_distribution': self._get_source_distribution(articles)
        }
    
    def _generate_daily_summary(self, articles: List[Dict]) -> str:
        """生成每日总结"""
        if not articles:
            return "今日无相关文章"
        
        # 准备文章内容
        articles_text = ""
        for i, article in enumerate(articles[:20], 1):  # 限制文章数量
            articles_text += f"{i}. {article['title']}\n"
            articles_text += f"   来源: {article['source_name']}\n"
            articles_text += f"   内容: {article['content'][:200]}...\n\n"
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的科技文章分析师，专门分析蓝牙技术相关的文章。请根据提供的文章列表，生成一份简洁明了的每日总结报告。"
                    },
                    {
                        "role": "user",
                        "content": f"请根据以下蓝牙相关文章，生成一份今日总结报告，包括主要趋势、重要发现和值得关注的内容：\n\n{articles_text}"
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"生成每日总结失败: {e}")
            return self._generate_fallback_summary(articles)
    
    def _analyze_keywords(self, articles: List[Dict]) -> Dict:
        """分析关键词"""
        all_keywords = []
        for article in articles:
            all_keywords.extend(article.get('keywords', []))
        
        # 使用jieba进行中文关键词提取
        all_text = " ".join([article['title'] + " " + article['content'] for article in articles])
        chinese_keywords = jieba.analyse.extract_tags(all_text, topK=20, withWeight=True)
        
        # 统计英文关键词
        english_keywords = Counter(all_keywords)
        
        return {
            'chinese_keywords': chinese_keywords,
            'english_keywords': dict(english_keywords.most_common(20))
        }
    
    def _analyze_trends(self, articles: List[Dict]) -> Dict:
        """分析趋势"""
        # 按来源类型统计
        source_types = {}
        for article in articles:
            source_type = article.get('source_type', 'unknown')
            source_types[source_type] = source_types.get(source_type, 0) + 1
        
        # 按关键词统计
        keyword_trends = {}
        for article in articles:
            for keyword in article.get('keywords', []):
                keyword_trends[keyword] = keyword_trends.get(keyword, 0) + 1
        
        return {
            'source_types': source_types,
            'keyword_trends': dict(sorted(keyword_trends.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def _identify_hot_topics(self, articles: List[Dict]) -> List[Dict]:
        """识别热点话题"""
        # 按标题相似性分组
        topic_groups = {}
        
        for article in articles:
            title = article['title'].lower()
            
            # 简单的主题分类
            if any(word in title for word in ['蓝牙耳机', 'earbuds', 'headphones']):
                topic = '蓝牙耳机'
            elif any(word in title for word in ['蓝牙音箱', 'speaker', 'audio']):
                topic = '蓝牙音箱'
            elif any(word in title for word in ['蓝牙协议', 'protocol', 'standard']):
                topic = '蓝牙协议'
            elif any(word in title for word in ['蓝牙开发', 'development', 'sdk']):
                topic = '蓝牙开发'
            elif any(word in title for word in ['蓝牙芯片', 'chip', 'hardware']):
                topic = '蓝牙芯片'
            else:
                topic = '其他'
            
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(article)
        
        # 生成热点话题
        hot_topics = []
        for topic, group_articles in topic_groups.items():
            if len(group_articles) >= 2:  # 至少2篇文章才算热点
                hot_topics.append({
                    'topic': topic,
                    'article_count': len(group_articles),
                    'articles': group_articles[:5]  # 只取前5篇
                })
        
        return sorted(hot_topics, key=lambda x: x['article_count'], reverse=True)
    
    def _get_source_distribution(self, articles: List[Dict]) -> Dict:
        """获取来源分布"""
        distribution = {}
        for article in articles:
            source_name = article.get('source_name', 'Unknown')
            distribution[source_name] = distribution.get(source_name, 0) + 1
        
        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
    
    def _generate_fallback_summary(self, articles: List[Dict]) -> str:
        """生成备用总结（当AI服务不可用时）"""
        summary = f"今日共收集到 {len(articles)} 篇蓝牙相关文章。\n\n"
        
        # 按来源类型统计
        source_types = {}
        for article in articles:
            source_type = article.get('source_type', 'unknown')
            source_types[source_type] = source_types.get(source_type, 0) + 1
        
        summary += "来源分布：\n"
        for source_type, count in source_types.items():
            summary += f"- {source_type}: {count} 篇\n"
        
        # 热门关键词
        all_keywords = []
        for article in articles:
            all_keywords.extend(article.get('keywords', []))
        
        keyword_count = Counter(all_keywords)
        summary += f"\n热门关键词：\n"
        for keyword, count in keyword_count.most_common(10):
            summary += f"- {keyword}: {count} 次\n"
        
        return summary
    
    def generate_article_summary(self, article: Dict) -> str:
        """为单篇文章生成摘要"""
        if not article.get('content'):
            return ""
        
        content = article['content'][:1000]  # 限制内容长度
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的文章摘要生成器，请为给定的文章生成简洁的摘要。"
                    },
                    {
                        "role": "user",
                        "content": f"请为以下文章生成一个简洁的摘要（100字以内）：\n\n标题：{article['title']}\n\n内容：{content}"
                    }
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"生成文章摘要失败: {e}")
            # 返回简单的摘要
            return article['content'][:100] + "..."
    
    def analyze_sentiment(self, text: str) -> str:
        """分析文本情感"""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个情感分析专家，请分析给定文本的情感倾向。"
                    },
                    {
                        "role": "user",
                        "content": f"请分析以下文本的情感倾向，只回答：正面、负面或中性：\n\n{text[:500]}"
                    }
                ],
                max_tokens=10,
                temperature=0.3
            )
            
            sentiment = response.choices[0].message.content.strip()
            if sentiment in ['正面', '负面', '中性']:
                return sentiment
            else:
                return '中性'
                
        except Exception as e:
            print(f"情感分析失败: {e}")
            return '中性' 