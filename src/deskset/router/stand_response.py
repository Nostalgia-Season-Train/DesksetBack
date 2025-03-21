# ==== 响应 ====
from fastapi import Response
import orjson

class DesksetJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: object) -> bytes:
        response = {
            'success': True,
            'code': 0,
            'message': 'Success',
            'result': content
        }
        return orjson.dumps(response)
