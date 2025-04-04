from pathlib import Path

from deskset.feature.note.obsidian import *

class Manager(ConfVaultObserver):
    def __init__(self, conf_vault: ConfVault) -> None:
        conf_vault.attach(self)
        self.refresh(conf_vault)

    def update(self, conf_vault: ConfVault) -> None:
        self.refresh(conf_vault)

    def refresh(self, conf_vault: ConfVault) -> None:
        vault_path = conf_vault.path
        if not (Path(vault_path) / '.obsidian').is_dir():
            self.is_init = False
            return
        self.is_init = True
        self.conf_noteapi = ConfNoteAPI(vault_path)

conf_vault = ConfVault()
manager = Manager(conf_vault)


from fastapi import APIRouter
from deskset.router.unify import DesksetRepJSON
from deskset.router.unify import DesksetReqFolder

router_obsidian_manager = APIRouter(
    prefix='/obsidian-manager', tags=['Obsidian'],
    default_response_class=DesksetRepJSON
)

@router_obsidian_manager.get('/vault/get-path')
def get_vault_path():
    return conf_vault.path

@router_obsidian_manager.post('/vault/set-path')
def set_vault_path(req: DesksetReqFolder):
    conf_vault.path = req.path
