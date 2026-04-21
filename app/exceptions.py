from fastapi import HTTPException

class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "Custom A: bad request"):
        super().__init__(status_code=400, detail=detail)

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "Custom B: resource not found"):
        super().__init__(status_code=404, detail=detail)