from deskset.feature.note.obsidian import *

conf_vault = ConfVault()


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
