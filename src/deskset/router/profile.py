from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

from deskset.feature.profile import profile

router_profile = APIRouter(
    prefix='/v0/profile', tags=['个性资料'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)

@router_profile.get('')
def get():
    return profile.model_dump()
