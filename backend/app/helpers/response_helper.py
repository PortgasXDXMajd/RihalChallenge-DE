from typing import Any
from pydantic import BaseModel
from fastapi.responses import JSONResponse


class ResponseModel(BaseModel):
    message: str = "Success"
    result: int = 200
    body: Any = None

class ResponseHelper:
    @classmethod
    def error(cls, status: int = 400, msg: str = "There was an error"):
        return JSONResponse(
            status_code=status,
            content=ResponseModel(result=status, message=msg).model_dump(),
        )

    @classmethod
    def success(cls, body=True):
        return ResponseModel(body=body).model_dump()
