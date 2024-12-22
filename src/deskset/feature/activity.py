import arrow
import mistune
from mistune.renderers.markdown import MarkdownRenderer

from deskset.core.text_file import TextFile


# 动态解析器：解析文本文件中的动态
class ActivityParser:
    def __init__(self, heading: str = '# 动态', format: str = 'HH:mm:ss') -> None:
        self._heading = heading  # 动态所在标题 heading
        self._format  = format   # 动态时间格式 format

    def _get_content_under_title(self, lines: list[str]) -> tuple[list[str], list[str], list[str]]:
        before  = []  # 动态之前的行
        content = []  # 动态内容
        after   = []  # 动态之后的行

        lines = iter(lines)  # 以迭代器遍历

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

    def get_activitys(self, file: TextFile) -> list[dict[str, str]]:
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

        activitys: list[dict[str, str]] = []
        for item in list_items:
            try:
                activity_create = arrow.get(item, self._format).format(self._format)
                activitys.append({'create': activity_create,
                                  'content': item[len(activity_create):].strip(' \n')})
            except arrow.parser.ParserError:
                pass

        return activitys

    # 注：每次修改都是
    # 1、拆分文件 => 动态内容
    # 2、拆分动态
    # 3、增删改
    # 4、合并动态
    # 5、还原文件

    # 编辑，没有则创建
    def edit_activity(self, content, date, activity):
        pass

    def delete_activity(self, content, date):
        pass
