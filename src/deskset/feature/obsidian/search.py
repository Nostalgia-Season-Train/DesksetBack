from typing import Optional

from deskset.core.standard import DesksetError

from pathlib import Path
from deskset.core.root_path import RootPath


class Search:
    def __init__(self, vault_path: str, excludes: list[str] = ['.obsidian', '.git']) -> None:
        if not Path(Path(vault_path) / '.obsidian').is_dir():
            raise DesksetError(message=f'{vault_path} 不是 Obsidian 仓库')

        # 仓库路径、要排除的文件/文件夹
        self._vault = vault_path
        self._excludes = excludes

        # Obsidian URI 交互
        from .obsidian import ObsidianManager
        self._obsidian = ObsidianManager(self._vault)

        # 缓存
        self._cache: Optional[RootPath] = None

    def search(self, query: str) -> list[str]:
        # 查询结束，释放内存 + 保证下次查询刷新
        if query == '':
            self._cache = None
            return []

        if self._cache == None:
            self._cache = RootPath(self._vault, self._excludes).get_files()

        first = []  # .md 优先
        last  = []
        for file in self._cache:
            relpath = str(file['relpath'])
            if query.lower() not in relpath.lower():  # 忽略大小写：lower() 全部转为小写
                continue
            if relpath.endswith('.md'):
                first.append(file)
            else:
                last.append(file)
        # 对 Obsidian 搜索结果如何排序的研究：笔记 = .md 文件
          # 最近笔记：首位
          # 一般笔记：升序排序
          # 日记笔记：降序排序，让新日记在旧日记之前，相当于 sorted(reverse=True)
          # 附件文件：末位
        # 各自排序，保证 .md 优先级不变
        first[:] = sorted(first, key=lambda file : file['name'])
        last[:]  = sorted(last,  key=lambda file : file['name'])
        result = [str(file['relpath']) for file in first] + [str(file['relpath']) for file in last]
        return result

    def open_in_obsidian(self, relpath: str) -> None:
        path = Path(self._vault) / relpath
        if path.is_file():
            self._obsidian.open_note_by_path(str(path))


class EmptySearch:
    def __init__(self, vault_path: str, excludes: list[str] = ['.obsidian', '.git']) -> None:
        pass

    def search(self, query: str) -> list[str]:
        return []

    def open_in_obsidian(self, relpath: str) -> None:
        pass
