from pathlib import Path

import arrow

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.core.standard import DesksetError

STAND_DATE_FORMAT = 'YYYYMMDD'

ERR_INCORRECT_DATE_FORMAT = DesksetError(code=2000, message=_t('Incorrect Date Format'))


# 日记解析
# 以日记文件夹作根目录，操作相对路径
class DiaryParser:
    def __init__(self, relpath_format: str = 'YYYY年/MM月/YYYY年MM月DD日.md', language: str = config.language):
        """
        1、relpath_format 相对路径 + 日期格式
        - 例：日期 20241224 => YYYY年/MM月/YYYY年MM月DD日.md => 2024年/12月/2024年12月24日.md
        2、language 日期语言
        - 例：zh-cn 星期天、en Sunday
        3、注意事项：arrow 同一格式标记不能出现两次，否则会报错。但是，为了能在子文件夹中创建日记，目录、主名各自进行两次计算\n
        - 例：YYYY年/MM月/YYYY年MM月DD日 两次计算 YYYY年/MM月、YYYY年MM月DD日
        """
        # 相对路径 = 目录 / 主名 + 后缀
        self._dir_format  = str(Path(relpath_format).parent)  # 目录格式，默认 YYYY年/MM月
        self._stem_format = str(Path(relpath_format).stem)    # 主名格式，默认 YYYY年MM月DD日
        self._extn        = str(Path(relpath_format).suffix)  # 后缀，默认 .md
        self._language = language  # 日期语言，

        self._encoding = config.encoding

    # 获取文件（相对路径）中的日记
    def get_diarys(self, files: list[str]) -> list[dict[str, str]]:
        diarys: list[dict[str, str]] = []

        for file in files:
            # 后缀不能进入判断：.md 中 m、d 会被看作 月、日
            dir  = str(Path(file).parent)
            stem = str(Path(file).stem)

            # 检查目录、主名是否匹配日期格式，并计算标准日期，为否判断下一个文件
            try:
                arrow.get(dir, self._dir_format, locale=self._language)
                date = arrow.get(stem, self._stem_format, locale=self._language).format(STAND_DATE_FORMAT)
            except arrow.parser.ParserError:
                continue

            diarys.append({
                    'date': date,
                    'path': file
                })

        return sorted(diarys, key=lambda item : item['date'])

    # 输入日期（格式：标准日期格式 STAND_DATE_FORMAT），返回日记相对路径
    def get_diary_relpath(self, date: str) -> str:
        try:
            dir  = arrow.get(date, STAND_DATE_FORMAT, locale=self._language).format(self._dir_format,  locale=self._language)
            stem = arrow.get(date, STAND_DATE_FORMAT, locale=self._language).format(self._stem_format, locale=self._language)
            extn = self._extn
        except arrow.parser.ParserError:
            raise ERR_INCORRECT_DATE_FORMAT

        return str(Path(dir) / (stem + extn))
