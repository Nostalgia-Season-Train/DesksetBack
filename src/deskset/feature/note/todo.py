import mistune
from mistune.renderers.markdown import MarkdownRenderer

from deskset.core.text_file import TextFile


# 打卡/任务/待办解析器
class TodoParser:
    def __init__(self, heading: str = '# 打卡') -> None:
        self._heading = heading

    def get_todos(self, file: TextFile) -> list[dict[str]]:
        """解析文件中的任务：- [ ] 任务"""
        # 暂不考虑次级任务：    - [ ] 次级任务
        content = file.read()

        ast_tokens = mistune.create_markdown(renderer='ast')(''.join(content[1:]))
        ast_back_markdown = MarkdownRenderer()

        list_items: list[str] = []
        try:
            for token in ast_tokens:
                if token['type'] == 'list':
                    for list_children in token['children']:
                        if list_children['type'] == 'list_item':
                            list_items.append(ast_back_markdown(list_children['children'], mistune.BlockState()))
        except KeyError:
            pass

        todos: list[dict[str]] = []
        for item in list_items:
            if item[0] == '[' and item[2] == ']':
                todos.append({'content': item.strip('\n')})

        return todos
