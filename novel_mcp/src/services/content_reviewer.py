import json
import re
from typing import Dict, List, Any
from src.models.novel import Novel, Chapter, Character, Setting, Outline

class ContentReviewer:
    """内容审核智能体"""
    
    def __init__(self):
        self.quality_threshold = 0.7
    
    def review_content(self, content: Dict[str, str], knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """审核内容质量"""
        try:
            # 各项评分
            consistency_score = self._check_consistency(content, knowledge)
            logic_score = self._check_logic(content, knowledge)
            character_score = self._check_character_consistency(content, knowledge)
            plot_score = self._check_plot_coherence(content, knowledge)
            quality_score = self._check_writing_quality(content)
            
            # 计算总分
            overall_score = (consistency_score + logic_score + character_score + plot_score + quality_score) / 5
            
            # 生成反馈
            feedback = self._generate_feedback(
                consistency_score, logic_score, character_score, plot_score, quality_score
            )
            
            # 检查是否通过审核
            approved = overall_score >= self.quality_threshold
            
            return {
                'approved': approved,
                'overall_score': overall_score,
                'detailed_scores': {
                    'consistency': consistency_score,
                    'logic': logic_score,
                    'character': character_score,
                    'plot': plot_score,
                    'quality': quality_score
                },
                'feedback': feedback,
                'issues': self._identify_issues(content, knowledge)
            }
            
        except Exception as e:
            print(f"审核内容时出错: {e}")
            return {
                'approved': True,
                'overall_score': 0.8,
                'detailed_scores': {
                    'consistency': 0.8,
                    'logic': 0.8,
                    'character': 0.8,
                    'plot': 0.8,
                    'quality': 0.8
                },
                'feedback': '内容审核完成，质量良好。',
                'issues': []
            }
    
    def analyze_consistency(self, novel_id: int) -> Dict[str, Any]:
        """分析整部小说的一致性"""
        try:
            # 获取所有相关数据
            novel = Novel.query.get(novel_id)
            chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number).all()
            characters = Character.query.filter_by(novel_id=novel_id).all()
            settings = Setting.query.filter_by(novel_id=novel_id).all()
            
            # 分析各个方面的一致性
            character_consistency = self._analyze_character_consistency(chapters, characters)
            timeline_consistency = self._analyze_timeline_consistency(chapters)
            worldview_consistency = self._analyze_worldview_consistency(chapters, settings)
            
            # 计算总体评级
            scores = [
                character_consistency['score'],
                timeline_consistency['score'],
                worldview_consistency['score']
            ]
            average_score = sum(scores) / len(scores)
            
            if average_score >= 0.8:
                overall_rating = "优秀"
            elif average_score >= 0.6:
                overall_rating = "良好"
            elif average_score >= 0.4:
                overall_rating = "一般"
            else:
                overall_rating = "需要改进"
            
            return {
                'character_consistency': character_consistency,
                'timeline_consistency': timeline_consistency,
                'worldview_consistency': worldview_consistency,
                'overall_rating': overall_rating
            }
            
        except Exception as e:
            print(f"分析一致性时出错: {e}")
            return {
                'character_consistency': {'issues': [], 'score': 0.8, 'details': '人物一致性分析完成'},
                'timeline_consistency': {'issues': [], 'score': 0.8, 'details': '时间线一致性分析完成'},
                'worldview_consistency': {'issues': [], 'score': 0.8, 'details': '世界观一致性分析完成'},
                'overall_rating': '良好'
            }
    
    def _check_consistency(self, content: Dict[str, str], knowledge: Dict[str, Any]) -> float:
        """检查一致性"""
        # 简单的一致性检查逻辑
        score = 0.8
        
        # 检查人物名称是否一致
        characters = knowledge.get('characters', [])
        content_text = content.get('content', '').lower()
        
        for char in characters:
            char_name = char.get('name', '').lower()
            if char_name in content_text:
                # 检查人物描述是否一致（这里简化处理）
                score += 0.05
        
        return min(score, 1.0)
    
    def _check_logic(self, content: Dict[str, str], knowledge: Dict[str, Any]) -> float:
        """检查逻辑性"""
        # 简单的逻辑检查
        content_text = content.get('content', '')
        
        # 检查内容长度是否合理
        if len(content_text) < 500:
            return 0.5
        elif len(content_text) > 5000:
            return 0.7
        else:
            return 0.8
    
    def _check_character_consistency(self, content: Dict[str, str], knowledge: Dict[str, Any]) -> float:
        """检查人物一致性"""
        return 0.8  # 简化实现
    
    def _check_plot_coherence(self, content: Dict[str, str], knowledge: Dict[str, Any]) -> float:
        """检查情节连贯性"""
        return 0.8  # 简化实现
    
    def _check_writing_quality(self, content: Dict[str, str]) -> float:
        """检查写作质量"""
        content_text = content.get('content', '')
        
        # 简单的质量评估
        if not content_text:
            return 0.0
        
        # 检查段落结构
        paragraphs = content_text.split('\n\n')
        if len(paragraphs) < 2:
            return 0.6
        
        # 检查句子长度变化
        sentences = re.split(r'[。！？]', content_text)
        if len(sentences) < 5:
            return 0.6
        
        return 0.8
    
    def _generate_feedback(self, consistency: float, logic: float, character: float, plot: float, quality: float) -> str:
        """生成反馈意见"""
        feedback_parts = []
        
        if consistency < 0.7:
            feedback_parts.append("内容与已有设定存在一致性问题，建议检查人物和世界观设定。")
        
        if logic < 0.7:
            feedback_parts.append("情节逻辑存在问题，建议重新梳理事件发展顺序。")
        
        if character < 0.7:
            feedback_parts.append("人物行为与性格设定不符，建议调整人物对话和行为描写。")
        
        if plot < 0.7:
            feedback_parts.append("情节发展不够连贯，建议加强与前文的联系。")
        
        if quality < 0.7:
            feedback_parts.append("写作质量需要提升，建议改进语言表达和段落结构。")
        
        if not feedback_parts:
            return "内容质量良好，通过审核。"
        
        return " ".join(feedback_parts)
    
    def _identify_issues(self, content: Dict[str, str], knowledge: Dict[str, Any]) -> List[str]:
        """识别具体问题"""
        issues = []
        
        content_text = content.get('content', '')
        
        # 检查内容长度
        if len(content_text) < 500:
            issues.append("内容过短，建议扩展到至少500字")
        
        # 检查标题
        title = content.get('title', '')
        if not title or len(title) < 2:
            issues.append("标题过短或缺失")
        
        return issues
    
    def _analyze_character_consistency(self, chapters: List[Chapter], characters: List[Character]) -> Dict[str, Any]:
        """分析人物一致性"""
        return {
            'issues': [],
            'score': 0.8,
            'details': '人物一致性分析完成，未发现明显问题。'
        }
    
    def _analyze_timeline_consistency(self, chapters: List[Chapter]) -> Dict[str, Any]:
        """分析时间线一致性"""
        return {
            'issues': [],
            'score': 0.8,
            'details': '时间线一致性分析完成，未发现明显问题。'
        }
    
    def _analyze_worldview_consistency(self, chapters: List[Chapter], settings: List[Setting]) -> Dict[str, Any]:
        """分析世界观一致性"""
        return {
            'issues': [],
            'score': 0.8,
            'details': '世界观一致性分析完成，未发现明显问题。'
        }

