import json
import re
from typing import Dict, List, Any
from src.models.novel import Novel, Chapter, Character, Setting, Outline
from src.database_init import db

class KnowledgeManager:
    """知识库管理智能体"""
    
    def __init__(self):
        self.knowledge_cache = {}
    
    def get_relevant_knowledge(self, novel_id: int, context: str) -> Dict[str, Any]:
        """根据上下文获取相关知识"""
        try:
            # 获取小说基本信息
            novel = Novel.query.get(novel_id)
            if not novel:
                raise ValueError(f"小说ID {novel_id} 不存在")
            
            # 获取所有相关信息
            characters = Character.query.filter_by(novel_id=novel_id).all()
            settings = Setting.query.filter_by(novel_id=novel_id).all()
            outlines = Outline.query.filter_by(novel_id=novel_id).all()
            recent_chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number.desc()).limit(3).all()
            
            # 基于上下文筛选相关信息
            relevant_characters = self._filter_relevant_characters(characters, context)
            relevant_settings = self._filter_relevant_settings(settings, context)
            relevant_outlines = self._filter_relevant_outlines(outlines, context)
            
            return {
                'novel': novel.to_dict(),
                'characters': [char.to_dict() for char in relevant_characters],
                'settings': [setting.to_dict() for setting in relevant_settings],
                'outlines': [outline.to_dict() for outline in relevant_outlines],
                'recent_chapters': [chapter.to_dict() for chapter in recent_chapters]
            }
            
        except Exception as e:
            print(f"获取知识时出错: {e}")
            return {}
    
    def _filter_relevant_characters(self, characters: List[Character], context: str) -> List[Character]:
        """筛选相关人物"""
        relevant = []
        context_lower = context.lower()
        
        for char in characters:
            # 检查人物名字是否在上下文中
            if char.name.lower() in context_lower:
                relevant.append(char)
            # 检查人物描述是否与上下文相关
            elif self._calculate_relevance(char.description or '', context) > 0.3:
                relevant.append(char)
        
        # 如果没有找到相关人物，返回主要人物
        if not relevant and characters:
            relevant = characters[:3]  # 返回前3个人物
        
        return relevant
    
    def _filter_relevant_settings(self, settings: List[Setting], context: str) -> List[Setting]:
        """筛选相关设定"""
        relevant = []
        context_lower = context.lower()
        
        for setting in settings:
            # 检查设定名称是否在上下文中
            if setting.name.lower() in context_lower:
                relevant.append(setting)
            # 检查设定描述是否与上下文相关
            elif self._calculate_relevance(setting.description or '', context) > 0.3:
                relevant.append(setting)
        
        return relevant
    
    def _filter_relevant_outlines(self, outlines: List[Outline], context: str) -> List[Outline]:
        """筛选相关大纲"""
        relevant = []
        
        for outline in outlines:
            if self._calculate_relevance(outline.content, context) > 0.2:
                relevant.append(outline)
        
        return relevant
    
    def _calculate_relevance(self, text1: str, text2: str) -> float:
        """计算两个文本的相关性（简单的关键词匹配）"""
        if not text1 or not text2:
            return 0.0
        
        # 提取关键词
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        # 计算交集比例
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def update_knowledge_base(self, novel_id: int):
        """更新知识库"""
        # 清除缓存
        if novel_id in self.knowledge_cache:
            del self.knowledge_cache[novel_id]
        
        # 重新构建知识索引（这里可以添加更复杂的索引逻辑）
        print(f"知识库已更新：小说ID {novel_id}")
    
    def get_knowledge_summary(self, novel_id: int) -> Dict[str, Any]:
        """获取知识库摘要"""
        try:
            novel = Novel.query.get(novel_id)
            if not novel:
                raise ValueError(f"小说ID {novel_id} 不存在")
            
            # 统计信息
            chapter_count = Chapter.query.filter_by(novel_id=novel_id).count()
            character_count = Character.query.filter_by(novel_id=novel_id).count()
            setting_count = Setting.query.filter_by(novel_id=novel_id).count()
            outline_count = Outline.query.filter_by(novel_id=novel_id).count()
            
            # 计算总字数
            chapters = Chapter.query.filter_by(novel_id=novel_id).all()
            total_words = sum(len(chapter.content) for chapter in chapters)
            
            # 获取最新章节
            latest_chapter = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number.desc()).first()
            
            return {
                'novel_title': novel.title,
                'novel_description': novel.description,
                'statistics': {
                    'chapter_count': chapter_count,
                    'character_count': character_count,
                    'setting_count': setting_count,
                    'outline_count': outline_count,
                    'total_words': total_words
                },
                'latest_chapter': latest_chapter.to_dict() if latest_chapter else None,
                'last_updated': novel.updated_at.isoformat() if novel.updated_at else None
            }
            
        except Exception as e:
            print(f"获取知识库摘要时出错: {e}")
            return {}

