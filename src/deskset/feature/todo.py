import arrow
import mistune
from mistune.renderers.markdown import MarkdownRenderer

from deskset.core.text_file import TextFile


# 打卡/任务/待做解析器
class TodoParser:
    def __init__(self, heading: str = '# 打卡') -> None:
        self._heading = heading

    def _get_content_under_title(self, lines: list[str]) -> tuple[list[str], list[str], list[str]]:
        before  = []
        content = []
        after   = []

        lines = iter(lines)

        for line in lines:
            if line[:-1] == self._heading:
                break
            before.append(line)

        content.append(line)
        for line in lines:
            if line[0] == '#':
                break
            content.append(line)

        after.append(line)
        for line in lines:
            after.append(line)

        return before, content, after

    def get_todos(self, file: TextFile) -> list[dict[str]]:
        _, content, _ = self._get_content_under_title(file.read())

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
