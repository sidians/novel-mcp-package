from flask import Blueprint, jsonify, request
from src.models.novel import Novel, Chapter, Character, Setting, Outline
from src.database_init import db

novel_bp = Blueprint('novel', __name__)

# 小说管理
@novel_bp.route('/novels', methods=['GET'])
def get_novels():
    """获取所有小说"""
    novels = Novel.query.all()
    return jsonify([novel.to_dict() for novel in novels])

@novel_bp.route('/novels', methods=['POST'])
def create_novel():
    """创建新小说"""
    data = request.json
    novel = Novel(
        title=data['title'],
        description=data.get('description', '')
    )
    db.session.add(novel)
    db.session.commit()
    return jsonify(novel.to_dict()), 201

@novel_bp.route('/novels/<int:novel_id>', methods=['GET'])
def get_novel(novel_id):
    """获取特定小说"""
    novel = Novel.query.get_or_404(novel_id)
    return jsonify(novel.to_dict())

@novel_bp.route('/novels/<int:novel_id>', methods=['PUT'])
def update_novel(novel_id):
    """更新小说信息"""
    novel = Novel.query.get_or_404(novel_id)
    data = request.json
    novel.title = data.get('title', novel.title)
    novel.description = data.get('description', novel.description)
    db.session.commit()
    return jsonify(novel.to_dict())

@novel_bp.route('/novels/<int:novel_id>', methods=['DELETE'])
def delete_novel(novel_id):
    """删除小说"""
    novel = Novel.query.get_or_404(novel_id)
    db.session.delete(novel)
    db.session.commit()
    return '', 204

# 章节管理
@novel_bp.route('/novels/<int:novel_id>/chapters', methods=['GET'])
def get_chapters(novel_id):
    """获取小说的所有章节"""
    chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number).all()
    return jsonify([chapter.to_dict() for chapter in chapters])

@novel_bp.route('/novels/<int:novel_id>/chapters', methods=['POST'])
def create_chapter(novel_id):
    """创建新章节"""
    data = request.json
    chapter = Chapter(
        novel_id=novel_id,
        chapter_number=data['chapter_number'],
        title=data['title'],
        content=data['content'],
        summary=data.get('summary', '')
    )
    db.session.add(chapter)
    db.session.commit()
    return jsonify(chapter.to_dict()), 201

@novel_bp.route('/chapters/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    """获取特定章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    return jsonify(chapter.to_dict())

@novel_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    """更新章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.json
    chapter.title = data.get('title', chapter.title)
    chapter.content = data.get('content', chapter.content)
    chapter.summary = data.get('summary', chapter.summary)
    db.session.commit()
    return jsonify(chapter.to_dict())

@novel_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    """删除章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return '', 204

# 人物管理
@novel_bp.route('/novels/<int:novel_id>/characters', methods=['GET'])
def get_characters(novel_id):
    """获取小说的所有人物"""
    characters = Character.query.filter_by(novel_id=novel_id).all()
    return jsonify([character.to_dict() for character in characters])

@novel_bp.route('/novels/<int:novel_id>/characters', methods=['POST'])
def create_character(novel_id):
    """创建新人物"""
    data = request.json
    character = Character(
        novel_id=novel_id,
        name=data['name'],
        description=data.get('description', ''),
        personality=data.get('personality', ''),
        background=data.get('background', ''),
        relationships=data.get('relationships', '')
    )
    db.session.add(character)
    db.session.commit()
    return jsonify(character.to_dict()), 201

@novel_bp.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    """更新人物信息"""
    character = Character.query.get_or_404(character_id)
    data = request.json
    character.name = data.get('name', character.name)
    character.description = data.get('description', character.description)
    character.personality = data.get('personality', character.personality)
    character.background = data.get('background', character.background)
    character.relationships = data.get('relationships', character.relationships)
    db.session.commit()
    return jsonify(character.to_dict())

@novel_bp.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    """删除人物"""
    character = Character.query.get_or_404(character_id)
    db.session.delete(character)
    db.session.commit()
    return '', 204

# 世界观设定管理
@novel_bp.route('/novels/<int:novel_id>/settings', methods=['GET'])
def get_settings(novel_id):
    """获取小说的所有世界观设定"""
    settings = Setting.query.filter_by(novel_id=novel_id).all()
    return jsonify([setting.to_dict() for setting in settings])

@novel_bp.route('/novels/<int:novel_id>/settings', methods=['POST'])
def create_setting(novel_id):
    """创建新的世界观设定"""
    data = request.json
    setting = Setting(
        novel_id=novel_id,
        name=data['name'],
        type=data.get('type', ''),
        description=data.get('description', '')
    )
    db.session.add(setting)
    db.session.commit()
    return jsonify(setting.to_dict()), 201

@novel_bp.route('/settings/<int:setting_id>', methods=['PUT'])
def update_setting(setting_id):
    """更新世界观设定"""
    setting = Setting.query.get_or_404(setting_id)
    data = request.json
    setting.name = data.get('name', setting.name)
    setting.type = data.get('type', setting.type)
    setting.description = data.get('description', setting.description)
    db.session.commit()
    return jsonify(setting.to_dict())

@novel_bp.route('/settings/<int:setting_id>', methods=['DELETE'])
def delete_setting(setting_id):
    """删除世界观设定"""
    setting = Setting.query.get_or_404(setting_id)
    db.session.delete(setting)
    db.session.commit()
    return '', 204

# 大纲管理
@novel_bp.route('/novels/<int:novel_id>/outlines', methods=['GET'])
def get_outlines(novel_id):
    """获取小说的所有大纲"""
    outlines = Outline.query.filter_by(novel_id=novel_id).order_by(Outline.section_number).all()
    return jsonify([outline.to_dict() for outline in outlines])

@novel_bp.route('/novels/<int:novel_id>/outlines', methods=['POST'])
def create_outline(novel_id):
    """创建新的大纲"""
    data = request.json
    outline = Outline(
        novel_id=novel_id,
        section_number=data['section_number'],
        title=data['title'],
        content=data['content'],
        status=data.get('status', 'planned')
    )
    db.session.add(outline)
    db.session.commit()
    return jsonify(outline.to_dict()), 201

@novel_bp.route('/outlines/<int:outline_id>', methods=['PUT'])
def update_outline(outline_id):
    """更新大纲"""
    outline = Outline.query.get_or_404(outline_id)
    data = request.json
    outline.title = data.get('title', outline.title)
    outline.content = data.get('content', outline.content)
    outline.status = data.get('status', outline.status)
    db.session.commit()
    return jsonify(outline.to_dict())

@novel_bp.route('/outlines/<int:outline_id>', methods=['DELETE'])
def delete_outline(outline_id):
    """删除大纲"""
    outline = Outline.query.get_or_404(outline_id)
    db.session.delete(outline)
    db.session.commit()
    return '', 204

