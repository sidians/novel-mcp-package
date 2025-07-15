from flask import Blueprint, jsonify, request
from src.models.novel import Novel, Chapter, Character, Setting, Outline
from src.database_init import db
from src.services.knowledge_manager import KnowledgeManager
from src.services.writing_assistant import WritingAssistant
from src.services.content_reviewer import ContentReviewer

mcp_bp = Blueprint('mcp', __name__)

@mcp_bp.route('/generate-chapter', methods=['POST'])
def generate_chapter():
    """生成新章节"""
    try:
        data = request.json
        novel_id = data['novel_id']
        context = data['context']
        requirements = data.get('requirements', '')
        
        # 初始化各个智能体
        knowledge_manager = KnowledgeManager()
        writing_assistant = WritingAssistant()
        content_reviewer = ContentReviewer()
        
        # 获取相关知识
        knowledge = knowledge_manager.get_relevant_knowledge(novel_id, context)
        
        # 生成内容
        generated_content = writing_assistant.generate_content(
            knowledge=knowledge,
            context=context,
            requirements=requirements
        )
        
        # 审核内容
        review_result = content_reviewer.review_content(
            content=generated_content,
            knowledge=knowledge
        )
        
        # 如果审核不通过，进行迭代优化
        iterations = 1
        while not review_result['approved'] and iterations < 3:
            generated_content = writing_assistant.improve_content(
                content=generated_content,
                feedback=review_result['feedback'],
                knowledge=knowledge
            )
            review_result = content_reviewer.review_content(
                content=generated_content,
                knowledge=knowledge
            )
            iterations += 1
        
        return jsonify({
            'success': True,
            'content': generated_content,
            'review_result': review_result,
            'iterations': iterations,
            'knowledge_used': knowledge
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/analyze-consistency', methods=['POST'])
def analyze_consistency():
    """分析内容一致性"""
    try:
        data = request.json
        novel_id = data['novel_id']
        
        content_reviewer = ContentReviewer()
        consistency_report = content_reviewer.analyze_consistency(novel_id)
        
        return jsonify({
            'success': True,
            'consistency_report': consistency_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/update-knowledge', methods=['POST'])
def update_knowledge():
    """更新知识库"""
    try:
        data = request.json
        novel_id = data['novel_id']
        
        knowledge_manager = KnowledgeManager()
        knowledge_manager.update_knowledge_base(novel_id)
        
        return jsonify({
            'success': True,
            'message': '知识库更新完成'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/get-knowledge-summary', methods=['GET'])
def get_knowledge_summary():
    """获取知识库摘要"""
    try:
        novel_id = request.args.get('novel_id', type=int)
        if not novel_id:
            return jsonify({'error': '缺少novel_id参数'}), 400
        
        knowledge_manager = KnowledgeManager()
        summary = knowledge_manager.get_knowledge_summary(novel_id)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/suggest-next-plot', methods=['POST'])
def suggest_next_plot():
    """获取情节建议"""
    try:
        data = request.json
        novel_id = data['novel_id']
        current_context = data['current_context']
        
        knowledge_manager = KnowledgeManager()
        writing_assistant = WritingAssistant()
        
        # 获取相关知识
        knowledge = knowledge_manager.get_relevant_knowledge(novel_id, current_context)
        
        # 生成情节建议
        suggestions = writing_assistant.suggest_plot_development(
            knowledge=knowledge,
            current_context=current_context
        )
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

