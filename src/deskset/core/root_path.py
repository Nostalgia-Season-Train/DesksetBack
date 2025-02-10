import os
from pathlib import Path
from send2trash import send2trash, TrashPermissionError

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.core.standard import DesksetError

ERR_PATH_NOT_EXIST     = DesksetError(code=2000, message=_t('路径 {} 不存在'))
ERR_FILE_NOT_EXIST     = DesksetError(code=2001, message=_t('根路径 {} 下文件 {} 不存在'))
ERR_FILE_ALREADY_EXIST = DesksetError(code=2002, message=_t('根路径 {} 下文件 {} 已存在'))
ERR_NEED_UPDATE = DesksetError(code=2003, message=_t('根路径 {} 内存与硬盘中条目不一致，需要更新'))
ERR_CANT_FIND_NOR_CREATE_TRASH = DesksetError(code=2004, message=_t('根路径 {} 不能找到或创建回收站'))


# 根路径（根目录）
# 作用：将一个路径（目录）视作根路径（根目录）进行操作
class RootPath:
    def __init__(self, root: str) -> None:
        self._encoding = config.encoding

        if not os.path.isdir(root):
            raise ERR_PATH_NOT_EXIST.insert(root)

        self._root = Path(root)
        self._folders: list[Path] = []
        self._files:   list[Path] = []

        self.update()

    def __get_entrys(self, relpath: Path) -> tuple[list[Path], list[Path]]:
        folders: list[Path] = []
        files:   list[Path] = []

        with os.scandir(self._root / relpath) as entrys:
            for entry in entrys:
                if entry.is_dir():
                    folders.append(relpath / entry.name)
                    # 子条目下的文件夹和文件
                    folders_in_entry, files_in_entry = self.__get_entrys(relpath / entry.name)
                    files.extend(files_in_entry)
                    folders.extend(folders_in_entry)
                else:
                    files.append(relpath / entry.name)

        return folders, files

    def update(self) -> None:
        folders, files = self.__get_entrys(Path(''))

        self._folders = folders
        self._files = files

    def get_folders(self) -> list[str]:
        return list(map(str, self._folders))

    def get_files(self) -> list[str]:
        return list(map(str, self._files))

    def get_abspath(self, relpath: str) -> str:
        if Path(relpath) not in self._files:
            raise ERR_FILE_NOT_EXIST.insert(self._root, relpath)
        return str(self._root / relpath)

    # 直接计算绝对路径，不去检查文件是否存在
    def calc_abspath(self, relpath: str) -> str:
        return str(self._root / relpath)

    def create_file(self, relpath: str) -> None:
        relpath = self._root / relpath
        if relpath in self._files:
            raise ERR_FILE_ALREADY_EXIST.insert(self._root, relpath)

        try:
            with open(relpath, 'x', encoding=self._encoding):
                return
        except FileExistsError:
            raise ERR_NEED_UPDATE.insert(self._root)

    def delete_file(self, relpath: str) -> None:
        relpath = self._root / relpath
        if relpath not in self._files:
            raise ERR_FILE_NOT_EXIST.insert(self._root, relpath)

        try:
            send2trash(relpath)
        except FileNotFoundError:
            raise ERR_NEED_UPDATE.insert(self._root)
        # TrashPermissionError：根目录没有回收站，同时 send2trash 也不能创建回收站
        except TrashPermissionError:
            raise ERR_CANT_FIND_NOR_CREATE_TRASH.insert(self._root)
