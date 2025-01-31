from fastapi import APIRouter
from pydantic import BaseModel

import deskset.feature.quick as quick

router_quick = APIRouter(prefix='/v0/quick', tags=['快速启动'])

class QuickOpenPath(BaseModel):
    path: str

class QuickOpenURL(BaseModel):
    url: str


@router_quick.post('/open-app-by-path')
def open_app_by_path(req: QuickOpenPath):
    quick.open_app_by_path(req.path)

@router_quick.post('/open-web-by-url')
def open_web_by_url(req: QuickOpenURL):
    quick.open_web_by_url(req.url)
