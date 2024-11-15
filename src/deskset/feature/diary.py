import os
import arrow

from deskset.core.config import setting
from deskset.core.standard import DesksetError

ERR_DIARY_NO_EXIST = DesksetError(code=2000, message='无此日记！')
ERR_DIARY_ALREADY_EXIST = DesksetError(code=2001, message='日记已存在！')


class Diary:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self._instance, '_is_init') == False:
            self._is_init = True

            self.refresh()

    def refresh(self):
        self._dir = setting.dir
        self._format = setting.format

        # 临时：文件格式
        self._extn = '.md'

    def __get_diarys(self, dir, format):
        """
        在 dir 目录下按 format 日期格式查找日记，并返回日记列表
        """
        diarys = []

        for name in os.listdir(dir):
            path = dir + '/' + name

            if os.path.isdir(path):
                # 待定：按格式去子目录下找日记，例：24 年/10 月/
                # diarys += self.__get_diarys(path, format)
                pass
            else:
                try:
                    base_name = os.path.splitext(name)[0]
                    arrow.get(base_name, format)  # 检查文件主名是否符合日期格式
                    diarys.append({
                        'name': name,
                        'path': path
                    })
                except arrow.parser.ParserError:  # 文件主名不匹配日期格式
                    pass

        return diarys

    def get_format_date(self):
        return arrow.now().format(self._format)

    def get_diary_list(self):
        """
        返回日记列表
        """
        diarys = self.__get_diarys(self._dir, self._format)
        diarys[:] = sorted(diarys, key=lambda diary: diary['name'])
        return diarys

    def get_today_diary(self):
        """
        查看今天日记
        """
        name = arrow.now().format(self._format) + self._extn
        path = os.path.join(self._dir, name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ERR_DIARY_NO_EXIST

    def create_today_diary(self):
        """
        创建今天日记
        """
        name = arrow.now().format(self._format) + self._extn
        path = os.path.join(self._dir, name)
        try:
            with open(path, 'x', encoding='utf-8'):
                return
        except FileExistsError:
            return ERR_DIARY_ALREADY_EXIST


diary = Diary()
