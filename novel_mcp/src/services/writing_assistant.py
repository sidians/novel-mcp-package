import os
import json
from typing import Dict, List, Any
import openai

class WritingAssistant:
    """写作助手智能体"""
    
    def __init__(self):
        # 使用环境变量中的API配置
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        self.model = "gpt-3.5-turbo"
    
    def generate_content(self, knowledge: Dict[str, Any], context: str, requirements: str = "") -> Dict[str, str]:
        """生成章节内容"""
        try:
            # 构建提示词
            prompt = self._build_generation_prompt(knowledge, context, requirements)
            
            # 调用AI生成内容
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的小说创作助手，擅长根据背景信息创作高质量的小说章节。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # 解析生成的内容
            return self._parse_generated_content(content)
            
        except Exception as e:
            print(f"生成内容时出错: {e}")
            # 返回示例内容
            return {
                'title': '新章节',
                'content': '这是一个示例章节内容。由于AI服务暂时不可用，这里显示的是默认内容。',
                'summary': '示例章节摘要。'
            }
    
    def improve_content(self, content: Dict[str, str], feedback: str, knowledge: Dict[str, Any]) -> Dict[str, str]:
        """根据反馈改进内容"""
        try:
            prompt = f"""
请根据以下反馈改进章节内容：

原始内容：
标题：{content.get('title', '')}
正文：{content.get('content', '')}

反馈意见：{feedback}

背景信息：{json.dumps(knowledge, ensure_ascii=False, indent=2)}

请提供改进后的内容，格式如下：
标题：[改进后的标题]
正文：[改进后的正文]
摘要：[改进后的摘要]
"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的小说编辑，擅长根据反馈改进内容质量。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.6
            )
            
            improved_content = response.choices[0].message.content
            return self._parse_generated_content(improved_content)
            
        except Exception as e:
            print(f"改进内容时出错: {e}")
            return content  # 返回原始内容
    
    def suggest_plot_development(self, knowledge: Dict[str, Any], current_context: str) -> List[str]:
        """建议情节发展"""
        try:
            prompt = f"""
基于以下背景信息和当前情况，请提供3个可能的情节发展建议：

背景信息：{json.dumps(knowledge, ensure_ascii=False, indent=2)}

当前情况：{current_context}

请提供3个不同的发展方向，每个建议应该：
1. 符合已建立的世界观和人物设定
2. 推进主要情节发展
3. 具有足够的戏剧冲突
4. 保持逻辑连贯性

格式：
建议1：[详细描述]
建议2：[详细描述]
建议3：[详细描述]
"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个经验丰富的小说策划师，擅长设计引人入胜的情节发展。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.8
            )
            
            suggestions_text = response.choices[0].message.content
            return self._parse_suggestions(suggestions_text)
            
        except Exception as e:
            print(f"生成情节建议时出错: {e}")
            return [
                "建议1：深入探索主角的内心冲突，通过一个重要的选择来推进角色发展。",
                "建议2：引入新的次要角色或势力，为故事增加复杂性和新的可能性。",
                "建议3：回到之前埋下的伏笔，通过揭示隐藏信息来推动情节发展。"
            ]
    
    def _build_generation_prompt(self, knowledge: Dict[str, Any], context: str, requirements: str) -> str:
        """构建生成提示词"""
        prompt = f"""
请根据以下信息创作一个小说章节：

小说背景：
{json.dumps(knowledge.get('novel', {}), ensure_ascii=False, indent=2)}

人物信息：
{json.dumps(knowledge.get('characters', []), ensure_ascii=False, indent=2)}

世界观设定：
{json.dumps(knowledge.get('settings', []), ensure_ascii=False, indent=2)}

大纲信息：
{json.dumps(knowledge.get('outlines', []), ensure_ascii=False, indent=2)}

最近章节：
{json.dumps(knowledge.get('recent_chapters', []), ensure_ascii=False, indent=2)}

创作要求：
{context}

特殊要求：
{requirements}

请创作一个章节，包含：
1. 引人入胜的标题
2. 1500-2000字的正文内容
3. 简洁的章节摘要

格式要求：
标题：[章节标题]
正文：[章节正文内容]
摘要：[章节摘要]
"""
        return prompt
    
    def _parse_generated_content(self, content: str) -> Dict[str, str]:
        """解析生成的内容"""
        result = {'title': '', 'content': '', 'summary': ''}
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('标题：'):
                result['title'] = line[3:].strip()
                current_section = 'title'
            elif line.startswith('正文：'):
                result['content'] = line[3:].strip()
                current_section = 'content'
            elif line.startswith('摘要：'):
                result['summary'] = line[3:].strip()
                current_section = 'summary'
            elif current_section and line:
                if current_section == 'content':
                    result['content'] += '\n' + line
                elif current_section == 'summary':
                    result['summary'] += '\n' + line
        
        # 如果解析失败，使用整个内容作为正文
        if not result['content'] and content:
            result['content'] = content
            result['title'] = '新章节'
            result['summary'] = '章节摘要'
        
        return result
    
    def _parse_suggestions(self, suggestions_text: str) -> List[str]:
        """解析情节建议"""
        suggestions = []
        lines = suggestions_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('建议') and '：' in line:
                suggestion = line.split('：', 1)[1].strip()
                if suggestion:
                    suggestions.append(suggestion)
        
        # 如果解析失败，返回默认建议
        if not suggestions:
            suggestions = [
                "深入探索主角的内心冲突，通过一个重要的选择来推进角色发展。",
                "引入新的次要角色或势力，为故事增加复杂性和新的可能性。",
                "回到之前埋下的伏笔，通过揭示隐藏信息来推动情节发展。"
            ]
        
        return suggestions[:3]  # 最多返回3个建议

