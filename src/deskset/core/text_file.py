from typing import Callable, Any
import difflib

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.core.standard import DesksetError

ERR_FILE_NOT_FOUND       = DesksetError(code=1000, message=_t('读写错误，文件不存在'))
ERR_FILE_CHANGED_OUTSIDE = DesksetError(code=1001, message=_t('文件被外部修改'))


# 撤销/重做管理器
class DoManager:
    def __init__(self) -> None:
        self._history = {
            'undo': [],
            'redo': []
        }
        self._is_undo_or_redo = None

    # 注册撤销/重做事件，以供撤销/重做时调用
    def register(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        if self._is_undo_or_redo is None:
            self._history['undo'].append((func, args, kwargs))
            self._history['redo'] = []
        else:
            kind = 'redo' if self._is_undo_or_redo == 'undo' else 'undo'
            self._history[kind].append((func, args, kwargs))

        self._is_undo_or_redo = None

    def undo(self) -> None:
        func, args, kwargs = self._history['undo'].pop()
        self._is_undo_or_redo = 'undo'
        func(*args, **kwargs)

    def redo(self) -> None:
        func, args, kwargs = self._history['redo'].pop()
        self._is_undo_or_redo = 'redo'
        func(*args, **kwargs)


# 文本
class Text:
    def __init__(self, text: list[str]) -> None:
        self._text = text
        self._do_manager = DoManager()

    # 生成编辑码
    def _generate_edcodes(self, old_text: list[str], new_text: list[str]) -> list[tuple[str, int, int, list[str]]]:
        edcodes: list[tuple[str, int, int, list[str]]] = []

        diff_sequence = difflib.SequenceMatcher(None, old_text, new_text)
        for tag, i1, i2, j1, j2 in diff_sequence.get_opcodes():
            if   tag == 'equal'  : edcodes.append(('equal'  , i1, i2, ['']))
            elif tag == 'replace': edcodes.append(('replace', i1, i2, new_text[j1:j2]))
            elif tag == 'delete' : edcodes.append(('delete' , i1, i2, ['']))
            elif tag == 'insert' : edcodes.append(('insert' , i1, i2, new_text[j1:j2]))

        return edcodes

    # 通过编辑码更新文本
    def _edit(self, edcodes: list[tuple[str, int, int, list[str]]]) -> None:
        # 编辑后文本 text；当前文本 self._text；编辑码 edcodes
        # text = self._text + edcodes
        text: list[str] = []
        for tag, i1, i2, block in edcodes:
            if   tag == 'equal'  : text.extend(self._text[i1:i2])
            elif tag == 'replace': text.extend(block)
            elif tag == 'delete' : pass
            elif tag == 'insert' : text.extend(block)

        # 注册本次编辑的逆
        # inverse_edcodes = text -> self._text
        self._do_manager.register(self._edit, self._generate_edcodes(text, self._text))

        # 更新文本
        self._text = text

    def undo(self) -> None:
        self._do_manager.undo()

    def redo(self) -> None:
        self._do_manager.redo()

    def get(self) -> list[str]:
        return self._text

    def set(self, text: list[str]) -> None:
        # 如果出现问题，换成下列代码以保证每次修改都由 _edit 完成
        # self._edit(self._edit_codes(text, self._text))
        self._do_manager.register(self._edit, self._generate_edcodes(text, self._text))
        self._text = text


# 文本文件
# 作用：处理文件内容
# - 1、内容读写：确保硬盘与内存中的文件内容数据一致
# - 2、内容编辑：撤销、重做
# 注：创建、删除功能，将由路径相关模块提供
class TextFile:
    def __init__(self, path):
        self._encoding = config.encoding

        try:
            with open(path, 'r', encoding=self._encoding) as file:
                self._path = path
                self._content = Text(file.readlines())
        except FileNotFoundError:
            raise ERR_FILE_NOT_FOUND

    def undo(self):
        self._content.undo()

    def redo(self):
        self._content.redo()

    # 检查外部更改
    # - 外部更改：不受 TextFile 控制文件更改。比如通过 vsc 修改文件
    def _check_outside_change(self):
        try:
            with open(self._path, 'r', encoding=self._encoding) as file:
                text = file.readlines()
                if difflib.SequenceMatcher(None, self._content.get(), text).ratio() != 1:
                    self._content.set(text)
                    return True
                else:
                    return False
        except FileNotFoundError:
            raise ERR_FILE_NOT_FOUND

    def read(self):
        self._check_outside_change()
        return self._content.get()

    def write(self, content):
        if self._check_outside_change():
            raise ERR_FILE_CHANGED_OUTSIDE
        self._content.set(content)

        try:
            with open(self._path, 'r+', encoding=self._encoding) as f:
                f.write(self._content.get())
        except FileNotFoundError:
            raise ERR_FILE_NOT_FOUND


# test_textfile = TextFile('')

# while True:
#     get_input = input()
#     if   get_input == '1':
#         print('检查更改：')
#         test_textfile._check_outside_change()
#     elif get_input == '2':
#         print('当前文本：')
#         print(test_textfile._content.get())
#     elif get_input == 'u':
#         print('撤销：')
#         test_textfile.undo()
#     elif get_input == 'r':
#         print('重做：')
#         test_textfile.redo()
#     else:
#         pass
