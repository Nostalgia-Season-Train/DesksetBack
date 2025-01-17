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

        # 确保每行只被压入一次：
        # - 每次压入前，判断 i < len(lines)
        # - 每次压入后，i++
        # 注：len(lines: list[str]) 时间开销 O(1)，无需临时变量
        i = 0
        while i < len(lines):
            # [:-1] 去掉换行符
            if lines[i][:-1] == self._heading:
                break
            before.append(lines[i])
            i += 1

        if i < len(lines):
            content.append(lines[i])
            i += 1
        while i < len(lines):
            # 是否进入其他标题
            if lines[i][0] == '#':
                break
            content.append(lines[i])
            i += 1

        if i < len(lines):
            after.append(lines[i])
            i += 1
        while i < len(lines):
            after.append(lines[i])
            i += 1

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
        for item in list_items:  # 注意：mistune 会去掉行尾空格
            try:
                # 只取开头的时间
                if len(item) < len(self._format):
                    continue
                item_date = item[0: len(self._format)]

                # arrow 格式化时间，没有报错代表格式正确，是一条动态
                activity_create = arrow.get(item_date, self._format).format(self._format)
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
