from deskset.core.text_file import TextFile

class NoteParser:
    def metadata_and_content(self, file: TextFile) -> tuple[list[str], str]:
        property: list[str] = []  # 笔记属性（元数据）
        content:  list[str] = []  # 笔记内容，返回时拼接成字符串

        lines = iter(file.read())

        # 返回 1：没有属性
        line = next(lines, None)
        if line != '---\n':
            return [], ''.join(file.read())

        # 计算属性
        # 忽略第一个属性分割符(---)，不处理 line
        for line in lines:
            # 特殊情况：line == '---'，没有换行且只有属性
            if line == '---\n' or line == '---':
                break
            property.append(line)
        # 忽略第二个属性分割符(---)，不处理 line

        # 返回 2：没有内容
        line = next(lines, None)  # None 默认值判断
        if line is None:
            return property, ''

        # 计算内容
        content.append(line)
        for line in lines:
            content.append(line)

        # 返回 3：有属性，有内容
        return property, ''.join(content)
