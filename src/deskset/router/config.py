# === 输入验证 ===
from pydantic import BaseModel, field_validator

from pathlib import Path
from deskset.core.standard import DesksetError

class ReqStr(BaseModel):  # 确保写入配置文件之后，再去检查
    path: str


# === 路由 ===
from fastapi import APIRouter, Depends
from deskset.router.access import check_token

from deskset.presenter.format import format_return

from deskset.feature.conf_app import conf_app

router_config = APIRouter(prefix='/v0/config', tags=['配置'], dependencies=[Depends(check_token)])

@router_config.get('/app-obsidian-vault')
def get_vault_path():
    return format_return(conf_app.obsidian_vault)

@router_config.post('/app-obsidian-vault')
def set_vault_path(vault: ReqStr):
    conf_app.obsidian_vault = vault.path
    if Path(Path(conf_app.obsidian_vault) / '.obsidian').is_dir():
        return format_return(f'设置 Obsidian 仓库成功：{conf_app.obsidian_vault}')
    else:
        raise DesksetError(message=f'设置 Obsidian 仓库失败：{conf_app.obsidian_vault} 不是 Obsidian 仓库')
