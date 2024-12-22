import os
from pathlib import Path
from send2trash import send2trash, TrashPermissionError

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.core.standard import DesksetError

ERR_FILE_NOT_FOUND     = DesksetError(code=2000, message=_t('文件不存在'))
ERR_FILE_ALREADY_EXIST = DesksetError(code=2001, message=_t('文件已存在'))
ERR_NEED_UPDATE = DesksetError(code=2002, message=_t('内存与硬盘中目录不一致，需要更新'))
ERR_CANT_FIND_NOR_CREATE_TRASH = DesksetError(code=2003, message=_t('不能找到或创建回收站'))


# 根路径
# 作用：将一个目录视作根路径进行操作
class RootPath:
    def __init__(self, root: str) -> None:
        self._encoding = config.encoding

        self._root = Path(root)
        self._folders: list[Path] = []
        self._files:   list[Path] = []

        self.update()

    def __get_entrys(self, path: Path) -> tuple[list[Path], list[Path]]:
        folders: list[Path] = []
        files:   list[Path] = []

        with os.scandir(self._root / path) as entrys:
            for entry in entrys:
                if entry.is_dir():
                    folders.append(path / entry.name)
                    # 子条目下的文件夹和文件
                    folders_in_entry, files_in_entry = self.__get_entrys(path / entry.name)
                    files.extend(files_in_entry)
                    folders.extend(folders_in_entry)
                else:
                    files.append(path / entry.name)

        return folders, files

    def update(self) -> None:
        folders, files = self.__get_entrys(Path(''))

        self._folders = folders
        self._files = files

    def get_folders(self) -> list[str]:
        return list(map(str, self._folders))

    def get_files(self) -> list[str]:
        return list(map(str, self._files))

    def get_abspath(self, path: str) -> str:
        if Path(path) not in self._files:
            raise ERR_FILE_NOT_FOUND
        return str(self._root / path)

    def create_file(self, path: str) -> None:
        path = self._root / path
        if path in self._files:
            raise ERR_FILE_ALREADY_EXIST

        try:
            with open(path, 'x', encoding=self._encoding):
                return
        except FileExistsError:
            raise ERR_NEED_UPDATE

    def delete_file(self, path: str) -> None:
        path = self._root / path
        if path not in self._files:
            raise ERR_FILE_NOT_FOUND

        try:
            send2trash(path)
        except FileNotFoundError:
            raise ERR_NEED_UPDATE
        # TrashPermissionError：根目录没有回收站，同时 send2trash 也不能创建回收站
        except TrashPermissionError:
            raise ERR_CANT_FIND_NOR_CREATE_TRASH
