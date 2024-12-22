from deskset.core.text_file import TextFile


# 随笔/散文解析器
class ProseParser:
    def __init__(self, heading: str = '# 随笔') -> None:
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

    def get_prose(self, file: TextFile) -> list[str]:
        _, content, _ = self._get_content_under_title(file.read())

        return ''.join(content[1:]).strip('\n')

    # 修改：删除修改后的末尾换行 => 增加修改前的末尾换行
