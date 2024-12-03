import os
import arrow
from send2trash import send2trash, TrashPermissionError

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.core.standard import DesksetError

ERR_DIARY_NOT_FOUND            = DesksetError(code=2000, message=_t('Diary Not Found'))
ERR_DIARY_ALREADY_EXIST        = DesksetError(code=2001, message=_t('Diary Already Exist'))
ERR_CANT_FIND_NOR_CREATE_TRASH = DesksetError(code=2002, message=_t('Cant Find Nor Create Trash'))
ERR_INCORRECT_DATE_FORMAT      = DesksetError(code=2003, message=_t('Incorrect Date Format'))


class Diary:
    def __init__(self, dir, format='YYYY-MM-DD', extn='.md'):
        self._dir      = dir
        self._format   = format
        self._extn     = extn
        self._language = config.language
        self._encoding = config.encoding

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
                    arrow.get(base_name, format, locale=self._language)  # 检查文件主名是否符合日期格式
                    diarys.append({
                        'name': name,
                        'path': path
                    })
                except arrow.parser.ParserError:  # 文件主名不匹配日期格式
                    pass

        return diarys

    def get_diary_list(self):
        """
        返回日记列表
        """
        diarys = self.__get_diarys(self._dir, self._format)
        diarys[:] = sorted(diarys, key=lambda diary: diary['name'])
        return diarys

    # 输入日期（格式：YYYYMMDD，例：20241224）
    def get_diary_path(self, date):
        try:
            # 根据日记名称日期格式 _format 得到文件主名
            base_name = arrow.get(date, 'YYYYMMDD', locale=self._language).format(self._format, locale=self._language)
        except arrow.parser.ParserError:
            raise ERR_INCORRECT_DATE_FORMAT
        return os.path.join(self._dir, base_name + self._extn)

    def read_diary(self, date):
        """
        读取日记
        """
        path = self.get_diary_path(date)
        if not os.path.exists(path):
            return ERR_DIARY_NOT_FOUND

        with open(path, 'r', encoding=self._encoding) as f:
            return f.read()

    def create_diary(self, date):
        """
        创建日记
        """
        path = self.get_diary_path(date)
        if os.path.exists(path):
            return ERR_DIARY_ALREADY_EXIST

        with open(path, 'x', encoding=self._encoding):
            return

    def write_diary(self, date, content):
        """
        写入日记
        """
        path = self.get_diary_path(date)
        if not os.path.exists(path):  # 日记不存在则不创建，直接报错
            return ERR_DIARY_NOT_FOUND

        with open(path, 'w', encoding=self._encoding) as f:
            f.write(content)
            return

    def delete_diary(self, date):
        """
        删除日记
        """
        path = self.get_diary_path(date)
        if not os.path.exists(path):
            return ERR_DIARY_NOT_FOUND

        try:
            send2trash(path)
        except TrashPermissionError:  # TrashPermissionError：根目录没有回收站，同时 send2trash 也不能创建回收站
            return ERR_DIARY_ALREADY_EXIST
